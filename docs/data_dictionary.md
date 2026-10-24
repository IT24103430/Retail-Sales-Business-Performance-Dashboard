# Data Dictionary

This dictionary describes the five generated CSV files in `data/raw/`, inspected
for this step. All records are synthetic and monetary values are Sri Lankan
rupees (LKR). See [the current data profile](data_profile.md) for observed counts,
coverage, quality checks, and totals.

CSV stores text representations. The types below are the intended Power Query /
Power BI types: **Text**, **Date**, **Whole Number**, and **Fixed Decimal Number**.
Keep identifiers as Text to preserve their prefixes and leading zeros. Monetary
source values have two decimal places; display money as LKR with two decimals.
All columns are required and should have no blank values. PK means primary key;
FK means foreign key.

## fact_sales.csv → FactSales

Grain: one product line within an order. `SalesLineID` identifies a line;
`OrderID` can repeat. Lines in an order share date, customer, region, and channel.

| Column | Data type | Meaning | Key / relationship |
| --- | --- | --- | --- |
| SalesLineID | Text | Unique sales-line label, such as `SL000001`. | PK of FactSales. |
| OrderID | Text | Order label, such as `ORD00001`. Use distinct count for total orders. | Groups lines; not a PK and no separate order table exists. |
| OrderDate | Date | Order date in `YYYY-MM-DD` format, within 2025-01-01 through 2026-09-30 inclusive. | Planned many-to-one link to `DimDate[Date]`; DimDate has not been created. |
| ProductID | Text | Product sold, such as `P008`. | FK → `dim_products.ProductID`. |
| CustomerID | Text | Synthetic customer making the purchase, such as `C0662`. | FK → `dim_customers.CustomerID`. |
| RegionID | Text | Customer's region for the order, including online sales. Not a store location. | FK → `dim_regions.RegionID`; matches the selected customer's RegionID. |
| ChannelID | Text | Channel used for the order, such as `CH01`. | FK → `dim_channels.ChannelID`. |
| Quantity | Whole Number | Positive number of sale units; a packaged product counts as one unit. | Numeric fact; no relationship. |
| UnitPrice | Fixed Decimal Number | LKR selling price of one sale unit before discount; positive. | Numeric fact; no relationship. |
| UnitCost | Fixed Decimal Number | LKR purchase cost of one sale unit; nonnegative and below UnitPrice in this generator. Excludes operating expenses. | Numeric fact; no relationship. |
| DiscountAmount | Fixed Decimal Number | Total LKR discount for the whole line, not per unit; generated at 0–20% of Quantity × UnitPrice. | Numeric fact; no relationship. |

## dim_products.csv → DimProducts

Grain: one fictional retail product. Prices stay in the fact because transaction
prices can vary over time.

| Column | Data type | Meaning | Key / relationship |
| --- | --- | --- | --- |
| ProductID | Text | Unique product identifier, such as `P001`. | PK; referenced by `fact_sales.ProductID`. |
| ProductName | Text | Readable product and pack size, such as `Samba Rice 5 kg`. Fictional catalogue item. | Descriptive attribute. |
| Category | Text | Product group: Groceries, Beverages, Household, Personal Care, Stationery, or Small Appliances. | Descriptive attribute used to group products. |

## dim_customers.csv → DimCustomers

Grain: one synthetic customer. No personal names, contact details, or addresses
are stored. Customers can exist in the dimension without having a sales order.

| Column | Data type | Meaning | Key / relationship |
| --- | --- | --- | --- |
| CustomerID | Text | Unique synthetic customer identifier, such as `C0001`. | PK; referenced by `fact_sales.CustomerID`. |
| CustomerLabel | Text | Anonymous display label, such as `Synthetic customer 0001`. | Descriptive attribute, not a person's name. |
| CustomerSegment | Text | Fictional customer group: Household, Student, or Small Business. | Descriptive attribute used to group customers. |
| RegionID | Text | Assigned customer region; stable across this generated dataset. | FK → `dim_regions.RegionID`; reference information, not an extra active model relationship. |

## dim_regions.csv → DimRegions

Grain: one Sri Lankan province used as a sales region. The city is a representative
city for that region, not a verified customer location or physical branch.

| Column | Data type | Meaning | Key / relationship |
| --- | --- | --- | --- |
| RegionID | Text | Unique region identifier, such as `R01`. | PK; referenced by `fact_sales.RegionID` and `dim_customers.RegionID`. |
| RegionName | Text | Readable region/province label, such as Western or Central. | Descriptive attribute. |
| City | Text | Representative city label, such as Colombo or Kandy. | Descriptive attribute; not an additional geographic grain. |

## dim_channels.csv → DimChannels

Grain: one sales channel.

| Column | Data type | Meaning | Key / relationship |
| --- | --- | --- | --- |
| ChannelID | Text | Unique channel identifier, such as `CH01`. | PK; referenced by `fact_sales.ChannelID`. |
| ChannelName | Text | Physical Store, Online Store, Mobile App, or Telephone Order. | Descriptive attribute. |

## Columns added by Power Query

These columns are defined in `powerbi/queries/fact_sales.m` and do not exist in the
raw CSV. After the query runs, FactSales will have its original 11 columns plus
these four. M execution in Desktop is pending; see [the setup guide](power_query_setup.md).

| Column | Data type | Meaning / formula | Relationship |
| --- | --- | --- | --- |
| GrossSales | Fixed Decimal Number | LKR gross line sales: `Quantity * UnitPrice`. | Numeric fact; none. |
| NetSales | Fixed Decimal Number | LKR revenue after discount: `GrossSales - DiscountAmount`. | Numeric fact; none. |
| TotalCost | Fixed Decimal Number | LKR line cost: `Quantity * UnitCost`. | Numeric fact; none. |
| LineProfit | Fixed Decimal Number | LKR line profit: `NetSales - TotalCost`. | Numeric fact; none. |

`TotalCost` is a column; the planned `Total Cost` measure has a space in its name.
Current dimension query/model names use plurals: DimProducts, DimCustomers,
DimRegions, and DimChannels. CSV filenames and identifiers remain unchanged.

## Relationships

The intended Power BI relationships are one-to-many with single-direction
filtering from each dimension to FactSales. These are design instructions;
no Power BI report or relationships have been created or verified in Desktop.

| One side | Many side | Intended use |
| --- | --- | --- |
| DimProducts[ProductID] | FactSales[ProductID] | Active product filtering. |
| DimCustomers[CustomerID] | FactSales[CustomerID] | Active customer and segment filtering. |
| DimRegions[RegionID] | FactSales[RegionID] | Active regional filtering. |
| DimChannels[ChannelID] | FactSales[ChannelID] | Active channel filtering. |
| DimDate[Date] | FactSales[OrderDate] | Planned active date filtering after DimDate is built. |

The CSV-level link `dim_customers.RegionID → dim_regions.RegionID` is checked by
the profiler. Keep it as reference information without another active model
relationship: region filtering already reaches FactSales directly and should
have one active path.

## Revenue definitions

- Gross line amount = Quantity × UnitPrice.
- Net line revenue = gross line amount − DiscountAmount.
- Line cost = Quantity × UnitCost.
- Line profit = net line revenue − line cost.
- Total Revenue = sum of net line revenue; Total Profit = Total Revenue − Total Cost.
- Average Order Value = Total Revenue ÷ distinct OrderID count.
- Profit Margin % = Total Profit ÷ Total Revenue.

DiscountAmount is subtracted once per line. All financial outputs describe
synthetic sales before tax, delivery fees, and other operating expenses; returns
are not modeled. Date coverage ending in September means 2026 is a partial year.
