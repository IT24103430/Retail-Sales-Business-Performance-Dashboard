# Interview preparation

These answers describe this repository. Python data generation, profiling and
insight calculation have run. Power BI source assets and report specifications
are prepared; Desktop model assembly, refresh and dashboard verification are pending.

## 1. What business problem does this project address?

Retail Sales Analytics explores sales, product profitability, regional performance
and sales channels for a fictional Sri Lankan retailer. The planned three report
pages help a manager compare these areas using LKR metrics.

## 2. What data did you use?

The Python generator uses a fixed random seed to create 5,000 synthetic order
lines from 1 January 2025 to 30 September 2026. Customer records use anonymous
labels and segments, with no names, emails or phone numbers.

## 3. What is a star schema, and what is the fact table's grain?

A star schema connects a central fact table to descriptive dimension tables.
Here, each FactSales row represents one product line in an order; DimProducts,
DimCustomers, DimRegions, DimChannels and the planned DimDate describe those rows.

## 4. How should the relationships work?

Each dimension's unique key connects to the matching FactSales key in an active
one-to-many relationship; DimDate[Date] connects to FactSales[OrderDate]. Filters
flow in one direction, from dimensions to FactSales, so a category or date
selection limits the sales used in calculations.

## 5. What does Power Query do in this project?

The prepared M scripts import the CSVs through a configurable DataFolder path,
set column types, trim text labels and remove invalid rows. They also define
GrossSales, NetSales, TotalCost and LineProfit before the data enters the model.

## 6. What is DAX used for?

DAX defines measures such as Total Revenue and Profit Margin % that recalculate
for the current filters. The prepared time measures use a contiguous DimDate
table for previous-period comparisons and year-to-date sales; they still need
evaluation in Power BI Desktop.

## 7. What is the difference between revenue and profit?

GrossSales is Quantity × UnitPrice, and NetSales subtracts DiscountAmount once
per line. LineProfit subtracts Quantity × UnitCost from NetSales; Total Profit
sums this product-cost profit and does not subtract operating expenses.

## 8. How do you avoid counting a multi-item order more than once?

Total Orders uses DISTINCTCOUNT(FactSales[OrderID]), because an order can have
several lines. Average Order Value divides Total Revenue by Total Orders using
DIVIDE, which safely returns blank when the denominator is zero.

## 9. How will slicers help users explore the report?

Slicers let users select the data included in visuals and measures. The interaction
guide specifies shared Date, Category, Region and Channel slicers across the three
pages, with a Product slicer local to Product Performance; Desktop setup is pending.

## 10. What business insight can you explain with evidence?

The Python analysis calculates LKR 12,348,732.29 in total revenue after discounts;
Small Appliances contributes 48.66% of it. This suggests reviewing availability of
that category in a business scenario, but these are synthetic portfolio findings,
not real sales results or proof that a recommendation improved performance.

For supporting detail, see the [data dictionary](data_dictionary.md),
[model guide](data_model.md), [DAX guide](dax_guide.md),
[interaction guide](report_interactions.md) and
[calculated business insights](business_insights.md).
