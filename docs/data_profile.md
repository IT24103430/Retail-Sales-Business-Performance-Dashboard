# Data Profile

Source: the five CSV files in `data/raw/`. All data is synthetic; money is in LKR.
Regenerate this report with `python3 scripts/profile_data.py`. No source files are changed.

## Rows, missing values, and primary keys

| File | Rows | Missing cells | Duplicate primary-key rows |
| --- | ---: | ---: | ---: |
| `fact_sales.csv` | 5,000 | 0 | 0 |
| `dim_products.csv` | 30 | 0 | 0 |
| `dim_customers.csv` | 700 | 0 | 0 |
| `dim_regions.csv` | 9 | 0 | 0 |
| `dim_channels.csv` | 4 | 0 | 0 |

Missing means an empty or whitespace-only field; all CSV columns were checked.
Duplicate counts are extra rows beyond the first occurrence of each nonblank primary key.
Missing primary keys are included in missing cells.

Columns with missing values:

- None.

## Foreign keys

| Source column | Referenced key | Invalid rows |
| --- | --- | ---: |
| `fact_sales.ProductID` | `dim_products.ProductID` | 0 |
| `fact_sales.CustomerID` | `dim_customers.CustomerID` | 0 |
| `fact_sales.RegionID` | `dim_regions.RegionID` | 0 |
| `fact_sales.ChannelID` | `dim_channels.ChannelID` | 0 |
| `dim_customers.RegionID` | `dim_regions.RegionID` | 0 |

Invalid foreign keys include blank values and keys absent from the referenced dimension.

## Sales coverage

- Observed date range: **2025-01-01 to 2026-09-30** (valid dates only).
- Unique orders: **2,453** (nonblank OrderID values).
- Repeated OrderID values are expected because an order can contain multiple lines.

## Basic generation checks

| Check | Issues |
| --- | ---: |
| Invalid or missing order dates | 0 |
| Dates outside 2025-01-01 to 2026-09-30 | 0 |
| Rows with invalid or missing numeric values | 0 |
| Nonpositive quantities | 0 |
| Nonpositive unit prices | 0 |
| Negative unit costs | 0 |
| Unit cost greater than or equal to unit price | 0 |
| Discounts below zero or above gross line amount | 0 |
| Orders with inconsistent date, customer, region, or channel | 0 |
| Fact/customer region mismatches (matched customers only) | 0 |

## Basic revenue estimates

Totals use 5,000 fact rows with parseable, finite numeric values; other quality issues are not filtered out.
AOV uses all nonblank distinct orders. Review quality issues before using these estimates.

| Metric | LKR |
| --- | ---: |
| Gross sales | 12,892,276.50 |
| Line discounts | 543,544.21 |
| Net revenue (Total Revenue) | 12,348,732.29 |
| Total cost | 8,888,670.77 |
| Total profit | 3,460,061.52 |
| Average order value | 5,034.13 |

Profit margin: **28.02%**.

Gross sales = sum(Quantity × UnitPrice); net revenue = gross sales − line discounts.
Total cost = sum(Quantity × UnitCost); total profit = net revenue − total cost.
Average order value = net revenue ÷ unique orders; profit margin = total profit ÷ net revenue.
Amounts are calculated with decimal arithmetic and displayed to two decimal places.
These are synthetic-data estimates before tax, delivery fees, or other operating expenses.
This profile is a basic data inspection; Power BI Desktop validation remains pending.
