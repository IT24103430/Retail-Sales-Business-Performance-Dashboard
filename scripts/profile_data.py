"""Read the five raw CSVs and replace docs/data_profile.md with a short profile.

Run from the project root: python3 scripts/profile_data.py
Uses only the Python standard library. Source CSVs are never changed.
"""

import csv
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_PATH = PROJECT_DIR / "docs" / "data_profile.md"
PRIMARY_KEYS = {
    "fact_sales": "SalesLineID",
    "dim_products": "ProductID",
    "dim_customers": "CustomerID",
    "dim_regions": "RegionID",
    "dim_channels": "ChannelID",
}
FOREIGN_KEYS = [
    ("fact_sales", "ProductID", "dim_products"),
    ("fact_sales", "CustomerID", "dim_customers"),
    ("fact_sales", "RegionID", "dim_regions"),
    ("fact_sales", "ChannelID", "dim_channels"),
    ("dim_customers", "RegionID", "dim_regions"),
]


def load_table(table):
    path = RAW_DIR / f"{table}.csv"
    if not path.is_file():
        raise SystemExit(f"Missing input: {path}. Run scripts/generate_data.py first.")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = reader.fieldnames or []
    if PRIMARY_KEYS[table] not in columns:
        raise SystemExit(f"Missing primary key column in {path.name}.")
    return columns, rows


def is_missing(value):
    return value is None or not value.strip()


def profile_sales(sales, customers):
    """Count simple generation issues and calculate totals with exact decimals."""
    checks = Counter({
        "Invalid or missing order dates": 0,
        "Dates outside 2025-01-01 to 2026-09-30": 0,
        "Rows with invalid or missing numeric values": 0,
        "Nonpositive quantities": 0,
        "Nonpositive unit prices": 0,
        "Negative unit costs": 0,
        "Unit cost greater than or equal to unit price": 0,
        "Discounts below zero or above gross line amount": 0,
        "Orders with inconsistent date, customer, region, or channel": 0,
        "Fact/customer region mismatches (matched customers only)": 0,
    })
    totals = {name: Decimal("0") for name in ("gross", "discount", "cost")}
    dates = []
    orders = defaultdict(set)
    customer_regions = {row["CustomerID"]: row["RegionID"] for row in customers}
    included_rows = 0
    for row in sales:
        try:
            order_date = date.fromisoformat(row.get("OrderDate") or "")
        except ValueError:
            checks["Invalid or missing order dates"] += 1
        else:
            dates.append(order_date)
            if not date(2025, 1, 1) <= order_date <= date(2026, 9, 30):
                checks["Dates outside 2025-01-01 to 2026-09-30"] += 1

        if not is_missing(row.get("OrderID")):
            orders[row["OrderID"]].add(tuple(
                row.get(column) for column in ("OrderDate", "CustomerID", "RegionID", "ChannelID")
            ))
        customer_id = row.get("CustomerID")
        if customer_id in customer_regions and row.get("RegionID") != customer_regions[customer_id]:
            checks["Fact/customer region mismatches (matched customers only)"] += 1

        try:
            quantity = int(row.get("Quantity") or "")
            price, cost, discount = [
                Decimal(row.get(column) or "")
                for column in ("UnitPrice", "UnitCost", "DiscountAmount")
            ]
            if not all(value.is_finite() for value in (price, cost, discount)):
                raise ValueError("Nonfinite monetary value")
        except (ValueError, InvalidOperation):
            checks["Rows with invalid or missing numeric values"] += 1
            continue

        gross = quantity * price
        checks["Nonpositive quantities"] += quantity <= 0
        checks["Nonpositive unit prices"] += price <= 0
        checks["Negative unit costs"] += cost < 0
        checks["Unit cost greater than or equal to unit price"] += cost >= price
        checks["Discounts below zero or above gross line amount"] += not 0 <= discount <= gross
        totals["gross"] += gross
        totals["discount"] += discount
        totals["cost"] += quantity * cost
        included_rows += 1

    checks["Orders with inconsistent date, customer, region, or channel"] = sum(
        len(details) > 1 for details in orders.values()
    )
    return dates, len(orders), included_rows, checks, totals


def main():
    tables = {table: load_table(table) for table in PRIMARY_KEYS}
    lines = [
        "# Data Profile", "",
        "Source: the five CSV files in `data/raw/`. All data is synthetic; money is in LKR.",
        "Regenerate this report with `python3 scripts/profile_data.py`. No source files are changed.",
        "", "## Rows, missing values, and primary keys", "",
        "| File | Rows | Missing cells | Duplicate primary-key rows |",
        "| --- | ---: | ---: | ---: |",
    ]
    missing_details = []
    for table, (columns, rows) in tables.items():
        missing = {
            column: sum(is_missing(row.get(column)) for row in rows)
            for column in columns
        }
        keys = Counter(
            row[PRIMARY_KEYS[table]] for row in rows
            if not is_missing(row.get(PRIMARY_KEYS[table]))
        )
        duplicates = sum(count - 1 for count in keys.values())
        lines.append(
            f"| `{table}.csv` | {len(rows):,} | {sum(missing.values()):,} | {duplicates:,} |"
        )
        missing_details.extend(
            f"- `{table}.{column}`: {count:,}" for column, count in missing.items() if count
        )
    lines += [
        "", "Missing means an empty or whitespace-only field; all CSV columns were checked.",
        "Duplicate counts are extra rows beyond the first occurrence of each nonblank primary key.",
        "Missing primary keys are included in missing cells.", "",
        "Columns with missing values:", "",
        *(missing_details or ["- None."]),
        "", "## Foreign keys", "",
        "| Source column | Referenced key | Invalid rows |",
        "| --- | --- | ---: |",
    ]
    for source, column, target in FOREIGN_KEYS:
        valid_keys = {
            row[PRIMARY_KEYS[target]] for row in tables[target][1]
            if not is_missing(row.get(PRIMARY_KEYS[target]))
        }
        invalid = sum(row.get(column) not in valid_keys for row in tables[source][1])
        lines.append(
            f"| `{source}.{column}` | `{target}.{PRIMARY_KEYS[target]}` | {invalid:,} |"
        )
    lines += ["", "Invalid foreign keys include blank values and keys absent from the referenced dimension."]

    dates, order_count, included, checks, totals = profile_sales(
        tables["fact_sales"][1], tables["dim_customers"][1]
    )
    date_range = f"{min(dates).isoformat()} to {max(dates).isoformat()}" if dates else "Unavailable"
    lines += [
        "", "## Sales coverage", "",
        f"- Observed date range: **{date_range}** (valid dates only).",
        f"- Unique orders: **{order_count:,}** (nonblank OrderID values).",
        "- Repeated OrderID values are expected because an order can contain multiple lines.",
        "", "## Basic generation checks", "",
        "| Check | Issues |", "| --- | ---: |",
        *(f"| {label} | {count:,} |" for label, count in checks.items()),
    ]

    revenue = totals["gross"] - totals["discount"]
    profit = revenue - totals["cost"]
    amounts = [
        ("Gross sales", totals["gross"]),
        ("Line discounts", totals["discount"]),
        ("Net revenue (Total Revenue)", revenue),
        ("Total cost", totals["cost"]),
        ("Total profit", profit),
        ("Average order value", revenue / order_count if order_count else None),
    ]
    lines += [
        "", "## Basic revenue estimates", "",
        f"Totals use {included:,} fact rows with parseable, finite numeric values; other quality issues are not filtered out.",
        "AOV uses all nonblank distinct orders. Review quality issues before using these estimates.",
        "", "| Metric | LKR |", "| --- | ---: |",
        *(f"| {label} | {amount:,.2f} |" if amount is not None else f"| {label} | N/A |"
          for label, amount in amounts),
        "",
        f"Profit margin: **{profit / revenue:.2%}**." if revenue else "Profit margin: N/A (zero net revenue).",
        "",
        "Gross sales = sum(Quantity × UnitPrice); net revenue = gross sales − line discounts.",
        "Total cost = sum(Quantity × UnitCost); total profit = net revenue − total cost.",
        "Average order value = net revenue ÷ unique orders; profit margin = total profit ÷ net revenue.",
        "Amounts are calculated with decimal arithmetic and displayed to two decimal places.",
        "These are synthetic-data estimates before tax, delivery fees, or other operating expenses.",
        "This profile is a basic data inspection; Power BI Desktop validation remains pending.",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
