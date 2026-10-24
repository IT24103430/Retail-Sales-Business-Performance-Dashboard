"""Calculate factual insights from synthetic raw CSVs and write a Markdown report.

Run from the project root: python3 scripts/generate_insights.py
Uses only the Python standard library. Source files are never changed.
"""

import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_PATH = PROJECT_DIR / "docs" / "business_insights.md"


def read_csv(filename, required_columns):
    path = RAW_DIR / filename
    if not path.is_file():
        raise SystemExit(f"Missing source file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(required_columns) - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{filename}: missing columns {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise SystemExit(f"{filename}: no data rows; existing insights were not replaced.")
    return rows


def read_dimension(filename, key, required_columns):
    """Use unique dimension keys so label lookups cannot multiply sales rows."""
    dimension = {}
    for row in read_csv(filename, [key, *required_columns]):
        if any(not (row.get(column) or "").strip() for column in [key, *required_columns]):
            raise SystemExit(f"{filename}: blank required key or label.")
        if row[key] in dimension:
            raise SystemExit(f"{filename}: duplicate primary key {row[key]}.")
        dimension[row[key]] = row
    return dimension


def new_metrics():
    return {
        "gross": Decimal("0"), "discount": Decimal("0"),
        "revenue": Decimal("0"), "cost": Decimal("0"), "profit": Decimal("0"),
        "units": 0, "orders": set(),
    }


def accumulate(metrics, amounts, quantity, order_id):
    for name, amount in amounts.items():
        metrics[name] += amount
    metrics["units"] += quantity
    metrics["orders"].add(order_id)


def money(value):
    return f"LKR {value:,.2f}"


def percentage(numerator, denominator):
    return f"{numerator / denominator:.2%}" if denominator else "N/A"


def revenue_leader(groups):
    # Deterministic ties: earliest YYYY-MM, alphabetical category, or dimension key.
    return sorted(groups.items(), key=lambda item: (-item[1]["revenue"], item[0]))[0]


def calculate():
    products = read_dimension("dim_products.csv", "ProductID", ["ProductName", "Category"])
    regions = read_dimension("dim_regions.csv", "RegionID", ["RegionName", "City"])
    channels = read_dimension("dim_channels.csv", "ChannelID", ["ChannelName"])
    customers = read_dimension("dim_customers.csv", "CustomerID", ["RegionID"])
    for customer in customers.values():
        if customer["RegionID"] not in regions:
            raise SystemExit("dim_customers.csv: RegionID missing from dim_regions.csv.")

    rows = read_csv("fact_sales.csv", [
        "SalesLineID", "OrderID", "OrderDate", "ProductID", "CustomerID", "RegionID",
        "ChannelID", "Quantity", "UnitPrice", "UnitCost", "DiscountAmount",
    ])
    total = new_metrics()
    groups = {name: defaultdict(new_metrics) for name in ("month", "category", "product", "region", "channel")}
    dates = []
    seen_lines = set()
    order_details = {}
    for row_number, row in enumerate(rows, start=2):
        try:
            if None in row or any(not (value or "").strip() for value in row.values()):
                raise ValueError("blank or malformed source row")
            line_id, order_id = row["SalesLineID"], row["OrderID"]
            if line_id in seen_lines:
                raise ValueError(f"duplicate SalesLineID {line_id}")
            seen_lines.add(line_id)
            for column, dimension in (
                ("ProductID", products), ("CustomerID", customers),
                ("RegionID", regions), ("ChannelID", channels),
            ):
                if row[column] not in dimension:
                    raise ValueError(f"unmatched {column} {row[column]}")
            if customers[row["CustomerID"]]["RegionID"] != row["RegionID"]:
                raise ValueError("fact region differs from the customer's region")
            order_date = date.fromisoformat(row["OrderDate"])
            details = (order_date, row["CustomerID"], row["RegionID"], row["ChannelID"])
            if order_id in order_details and order_details[order_id] != details:
                raise ValueError(f"inconsistent shared details for order {order_id}")
            order_details[order_id] = details
            quantity = int(row["Quantity"])
            price, cost, discount = [Decimal(row[column]) for column in (
                "UnitPrice", "UnitCost", "DiscountAmount"
            )]
            if not all(value.is_finite() for value in (price, cost, discount)):
                raise ValueError("nonfinite money value")
            gross = quantity * price
            if quantity <= 0 or price <= 0 or cost < 0 or not 0 <= discount <= gross:
                raise ValueError("invalid quantity, price, cost, or line discount")
        except (ValueError, InvalidOperation) as error:
            raise SystemExit(f"fact_sales.csv, CSV row {row_number}: {error}") from error

        # These are exactly the existing FactSales Power Query column formulas.
        revenue = gross - discount
        line_cost = quantity * cost
        amounts = {
            "gross": gross, "discount": discount, "revenue": revenue,
            "cost": line_cost, "profit": revenue - line_cost,
        }
        dates.append(order_date)
        accumulate(total, amounts, quantity, order_id)
        keys = {
            "month": order_date.strftime("%Y-%m"),
            "category": products[row["ProductID"]]["Category"].strip(),
            "product": row["ProductID"], "region": row["RegionID"], "channel": row["ChannelID"],
        }
        for name, key in keys.items():
            accumulate(groups[name][key], amounts, quantity, order_id)

    return total, groups, products, regions, channels, dates, len(rows)


def build_report(total, groups, products, regions, channels, dates, line_count):
    best_month, month_metrics = revenue_leader(groups["month"])
    best_category, category_metrics = revenue_leader(groups["category"])
    best_region, region_metrics = revenue_leader(groups["region"])
    best_channel, channel_metrics = revenue_leader(groups["channel"])
    top_products = sorted(groups["product"].items(), key=lambda item: (-item[1]["revenue"], item[0]))[:3]
    positive_categories = [(key, metrics) for key, metrics in groups["category"].items() if metrics["revenue"] > 0]
    weakest = min(positive_categories, key=lambda item: (item[1]["profit"] / item[1]["revenue"], item[0])) if positive_categories else None

    year, month = map(int, best_month.split("-"))
    previous_month = f"{year - 1}-12" if month == 1 else f"{year}-{month - 1:02d}"
    previous = groups["month"].get(previous_month)
    if previous is not None and previous["revenue"]:
        change = (month_metrics["revenue"] - previous["revenue"]) / previous["revenue"]
        monthly_comparison = f" Its revenue change from {previous_month} was {change:+.2%}."
    else:
        monthly_comparison = " A previous-calendar-month percentage comparison is unavailable."

    order_count = len(total["orders"])
    aov = money(total["revenue"] / order_count) if order_count else "N/A"
    product_list = "; ".join(
        f"{products[key]['ProductName']} ({key}): {money(metrics['revenue'])}"
        for key, metrics in top_products
    )
    top_product_revenue = sum((metrics["revenue"] for _, metrics in top_products), Decimal("0"))
    region_name = regions[best_region]["RegionName"]
    channel_name = channels[best_channel]["ChannelName"]
    figures = [
        ("Gross Revenue", money(total["gross"])),
        ("Total Discount", money(total["discount"])),
        ("Total Revenue (after discount)", money(total["revenue"])),
        ("Total Cost", money(total["cost"])),
        ("Total Profit", money(total["profit"])),
        ("Profit Margin %", percentage(total["profit"], total["revenue"])),
        ("Total Orders (distinct OrderID)", f"{order_count:,}"),
        ("Units Sold", f"{total['units']:,}"),
        ("Average Order Value", aov),
    ]
    margin_review = (
        f"Review unit costs and line discounts in **{weakest[0]}**, whose margin is "
        f"{percentage(weakest[1]['profit'], weakest[1]['revenue'])}, compared with the "
        f"overall {percentage(total['profit'], total['revenue'])}; test pricing or discount changes in the fictional scenario."
        if weakest else
        "Review products with zero net revenue before making margin-based pricing or discount recommendations."
    )
    return "\n".join([
        "# Business Insights — Synthetic Portfolio Data", "",
        "**All results below come from synthetic portfolio data, not real business results.**",
        "The findings describe the generated Sri Lankan retail scenario; they do not establish real demand or causes.",
        "",
        f"Coverage: **{min(dates).isoformat()} through {max(dates).isoformat()}**, "
        f"**{line_count:,} order lines**, **{order_count:,} distinct orders**. Money is LKR.",
        "", "## Calculated metrics", "",
        "| Metric | Calculated value |", "| --- | ---: |",
        *(f"| {label} | {value} |" for label, value in figures),
        "", "## Five factual findings", "",
        f"1. **Monthly sales:** {best_month} had the highest observed monthly net revenue, "
        f"{money(month_metrics['revenue'])}, with profit of {money(month_metrics['profit'])}." + monthly_comparison,
        f"2. **Strongest category by revenue:** {best_category} generated {money(category_metrics['revenue'])}, "
        f"{percentage(category_metrics['revenue'], total['revenue'])} of total net revenue, and "
        f"{money(category_metrics['profit'])} profit; its margin was "
        f"{percentage(category_metrics['profit'], category_metrics['revenue'])}.",
        f"3. **Top products by revenue:** {product_list}. Together these {len(top_products)} products "
        f"accounted for {percentage(top_product_revenue, total['revenue'])} of total net revenue.",
        f"4. **Leading region by revenue:** {region_name} generated {money(region_metrics['revenue'])}, "
        f"{percentage(region_metrics['revenue'], total['revenue'])} of net revenue, with "
        f"{len(region_metrics['orders']):,} distinct orders. "
        f"{regions[best_region]['City']} is its representative city label, not an independently measured city market.",
        f"5. **Leading channel by revenue:** {channel_name} generated {money(channel_metrics['revenue'])}, "
        f"{percentage(channel_metrics['revenue'], total['revenue'])} of net revenue, with "
        f"{len(channel_metrics['orders']):,} distinct orders and a "
        f"{percentage(channel_metrics['profit'], channel_metrics['revenue'])} margin.",
        "", "## Three recommendations for the fictional scenario", "",
        f"1. **Review product availability:** Prioritize a mock availability and replenishment review for "
        f"{best_category} and the revenue-leading products above; inventory and stockout data would be needed to justify purchasing changes.",
        f"2. **Investigate margin:** {margin_review}",
        f"3. **Evaluate regional and channel plans:** Use {region_name} and {channel_name} as starting "
        "points for a small fictional assortment or channel experiment, comparing the same calendar months and "
        "accounting for regional/channel coverage before extending the plan elsewhere.",
        "", "## Calculation notes and limits", "",
        "- Sources: `data/raw/fact_sales.csv` and the four `dim_*.csv` files in the same folder. "
        "Products/categories, region labels, and channel labels are looked up using unique dimension keys; customer and region keys are checked.",
        "- GrossSales = Quantity × UnitPrice; NetSales = GrossSales − DiscountAmount; "
        "TotalCost = Quantity × UnitCost; LineProfit = NetSales − TotalCost. DiscountAmount is a line total, subtracted once.",
        "- Totals aggregate every validated source line once. Orders use distinct OrderID; "
        "margin = total profit ÷ net revenue; AOV = net revenue ÷ distinct orders. "
        "Distinct order counts across categories/products are not additive.",
        "- Decimal arithmetic preserves monetary precision; rounding to two decimal places happens only for display. "
        "A zero denominator is shown as N/A. Invalid rows or duplicate keys stop generation instead of silently changing totals.",
        "- Leaders use net revenue. Ties use earliest month or alphabetical category/key order; one leader is shown. "
        "Top product lists contain up to three products with observed sales.",
        "- Monthly totals use observed order dates. Calendar months with no rows have no observed revenue; "
        "the script does not invent zero sales or compare against the last nonblank month. "
        "Boundary months may be partial; the supplied dataset ends in September 2026, so 2026 is not a complete sales year.",
        "- Tax, delivery fees, operating expenses, inventory, campaign effects, and real customer information are not modeled. "
        "Recommendations are suggestions for a portfolio exercise, not evidence of actual business problems.",
        "",
        "Regenerate from the project root with `python3 scripts/generate_insights.py`. "
        "This report is calculated from CSVs; it is not evidence of Power BI Desktop execution.", "",
    ])


def main():
    report = build_report(*calculate())
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_DIR)} from the current raw CSV files.")


if __name__ == "__main__":
    main()
