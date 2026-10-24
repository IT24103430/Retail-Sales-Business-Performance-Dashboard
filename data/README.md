# Synthetic Retail Data

All records are fictional and use Sri Lankan retail settings. Customer labels are
anonymous synthetic identifiers; there are no personal names or contact details.
Prices and costs are illustrative LKR amounts, not market price observations.

Run from the project root:

```sh
python3 scripts/generate_data.py
```

The generator uses the Python standard library and seed `20250930`. Rerunning with
the same code and Python version replaces the five raw CSVs with the same data.
`processed/` is reserved for later preparation work.

| Raw file | Grain and columns |
| --- | --- |
| `raw/fact_sales.csv` | 5,000 order lines: SalesLineID, OrderID, OrderDate, ProductID, CustomerID, RegionID, ChannelID, Quantity, UnitPrice, UnitCost, DiscountAmount. |
| `raw/dim_products.csv` | 30 products: ProductID, ProductName, Category. |
| `raw/dim_customers.csv` | 700 synthetic customers: CustomerID, CustomerLabel, CustomerSegment, RegionID. |
| `raw/dim_regions.csv` | Nine regions: RegionID, RegionName, City. City is a representative city for the region. |
| `raw/dim_channels.csv` | Four channels: ChannelID, ChannelName. |

Orders cover **2025-01-01 through 2026-09-30**, inclusive. Each order has one to four
distinct products and shares one date, customer, region, and channel. Fact RegionID
uses the customer's region, including for online orders. Keys come directly from
the dimensions. Quantities are positive; unit cost is below unit price.

Money is stored to two decimal places without currency symbols. `DiscountAmount`
is the total line discount, not a per-unit value; it is 0–20% of gross line amount.
Gross sales = Quantity × UnitPrice; net revenue = gross sales − DiscountAmount;
cost = Quantity × UnitCost; profit = net revenue − cost. No tax, delivery fees,
returns, or real-world sales claims are included.

April/December peaks, weekend demand, regional mix, and a small 2026 price uplift
are generation assumptions for analysis practice. Actual report findings must be
calculated from the generated data.

Column types and relationships are documented in the
[data dictionary](../docs/data_dictionary.md). Generate the
[data profile](../docs/data_profile.md) from the current raw files with:

```sh
python3 scripts/profile_data.py
```

The profiler reports row counts, coverage, missing values, key issues, basic
generation checks, and revenue estimates without changing the CSV files.

Generate the [calculated synthetic business insights](../docs/business_insights.md)
from the current CSVs with:

```sh
python3 scripts/generate_insights.py
```

This writes five factual findings, a metrics table, and three portfolio
recommendations. It preserves all source CSVs and does not require Power BI Desktop.
