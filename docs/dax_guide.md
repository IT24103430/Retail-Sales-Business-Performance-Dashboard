# DAX Measures

The nine definitions in [core_measures.dax](../powerbi/measures/core_measures.dax)
are the canonical core measures. They use FactSales and its existing Power Query
columns; no additional datasets or calculated columns are needed. Complete the
[Power Query setup](power_query_setup.md) and [data model setup](data_model.md)
first. Measures have been written but not executed or verified in Desktop.

## Meaning and formatting

Every measure uses the rows remaining under the current report filters.

| Measure | Simple explanation | Display format |
| --- | --- | --- |
| Gross Revenue | Adds GrossSales to show sales before discounts. | LKR currency, thousands separator, 2 decimals |
| Total Revenue | Adds NetSales to show revenue after discounts. | LKR currency, thousands separator, 2 decimals |
| Total Cost | Adds TotalCost to show the cost of the units sold. | LKR currency, thousands separator, 2 decimals |
| Total Profit | Adds LineProfit to show revenue after discounts minus product costs. | LKR currency, thousands separator, 2 decimals |
| Profit Margin % | Divides total profit by total revenue to show the share of revenue kept as profit. | Percentage, 2 decimals (`0.00%`) |
| Total Orders | Counts distinct OrderID values so each order is counted once within the current filters. | Whole number, thousands separator, 0 decimals (`#,##0`) |
| Units Sold | Adds Quantity to show how many sale units were sold. | Whole number, thousands separator, 0 decimals (`#,##0`) |
| Average Order Value | Divides total revenue by distinct orders to show revenue per order. | LKR currency, thousands separator, 2 decimals |
| Total Discount | Adds DiscountAmount to show the total discounts given across sales lines. | LKR currency, thousands separator, 2 decimals |

## Add the measures in Desktop

1. Open the actual project report in Power BI Desktop on Windows.
2. Right-click **FactSales** in the Data pane and choose **New measure**.
3. Open `powerbi/measures/core_measures.dax` in a text editor and copy the first
   definition, starting at `Gross Revenue =` and ending at its expression.
4. Replace the formula bar contents with that definition and press Enter.
5. Repeat **New measure** for each remaining definition, in file order. Paste
   one measure at a time; the complete file is not a single DAX query or measure.
6. If a named measure already exists from earlier README examples, select it and
   replace its formula instead of creating another version. Keep each exact name.

Use **New measure**, not New column or New table. Keep FactSales as the home table
for these measures. `Total Cost` is a measure, while `FactSales[TotalCost]` is a
column; the space distinguishes their names. Microsoft describes this workflow
in [Create measures](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures).

## Set the model formats

In **Model view**, select a measure and open the **Properties** pane. Under
**Formatting**, choose **Format → Custom** and enter the applicable format string.
Repeat for all nine measures. Format labels may vary slightly between Desktop
versions; the model-level Format property is the setting to use.

For the six LKR currency measures, use:

```text
"LKR" #,##0.00;-"LKR" #,##0.00
```

The first section formats positive values and zero; the second formats negative
values. For example, revenue of 1234.5 displays as **LKR 1,234.50**. Use `0.00%`
for Profit Margin % and `#,##0` for Total Orders and Units Sold. Percentage
formatting displays the ratio as a percent; do not multiply the DAX ratio by 100.
Keep the measures numeric and apply formatting through model properties rather
than using DAX FORMAT. If a visual abbreviates values as K or M, set its **Display
units → None** when full amounts are needed. See Microsoft's
[custom format strings guide](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-custom-format-strings).

## Keep totals consistent

- GrossSales already contains Quantity × UnitPrice, and TotalCost already contains
  Quantity × UnitCost; sum these columns without multiplying by Quantity again.
- NetSales already deducts DiscountAmount, so Total Revenue must not deduct the
  discount a second time. Total Profit also agrees with Total Revenue − Total Cost.
- Total Orders counts distinct OrderID values, rather than counting fact rows.
  An order containing three products is still one order in an unfiltered total.
- A single order can appear in several product or category groups. Each group's
  distinct order count is valid, but adding those counts can exceed the grand
  total because the total counts each order once across all selected groups.
- Under a product/category filter, Average Order Value means selected line
  revenue divided by orders containing those selected lines; it does not retrieve
  the full basket revenue for those orders.
- Profit Margin % and Average Order Value are ratios of totals, not averages of
  row-level ratios. DIVIDE returns blank for a zero or blank denominator; empty
  selections remain blank rather than showing a fabricated ratio.

The functions follow Microsoft's definitions of
[SUM](https://learn.microsoft.com/en-us/dax/sum-function-dax),
[DISTINCTCOUNT](https://learn.microsoft.com/en-us/dax/distinctcount-function-dax),
and [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax).

For a quick manual reconciliation after loading the current unfiltered dataset,
expect **Total Orders = 2,453**, **Total Revenue = LKR 12,348,732.29**, and
**Total Profit = LKR 3,460,061.52**, matching the [raw data profile](data_profile.md).
These are source-based expectations, not Desktop-verified results. Creating the
measures, applying formats, and checking results in Desktop remain pending.

## Time-intelligence measures

After adding the core measures, create the six definitions in
[time_measures.dax](../powerbi/measures/time_measures.dax) one at a time using the
same **New measure** method, in file order. All six use `[Total Revenue]`, so
"Sales" means revenue **after discounts**, consistent with the core measures.
Reuse the LKR format above for money and `0.00%` for percentages.

| Measure | Simple explanation | Display format |
| --- | --- | --- |
| Sales Previous Month | Shows net revenue for the selected dates shifted back one calendar month. | LKR, 2 decimals |
| Sales MoM Change | Shows current net revenue minus the previous month's net revenue when both are available. | LKR, 2 decimals |
| Sales MoM % | Shows the monthly revenue change divided by the previous month's net revenue. | Percentage, 2 decimals |
| Sales Previous Year | Shows net revenue for the selected dates shifted back one calendar year. | LKR, 2 decimals |
| Sales YoY % | Shows the change from the prior-year period divided by that period's net revenue. | Percentage, 2 decimals |
| Sales YTD | Accumulates net revenue from January 1 through the latest selected date in its year. | LKR, 2 decimals |

Assumptions and blank handling:

- Mark the contiguous **DimDate** as the Date table and use its active, single
  `1:*` relationship from `DimDate[Date]` to `FactSales[OrderDate]`, as documented
  in [the model guide](data_model.md). Use DimDate fields for slicers and axes;
  product, customer, region, and channel filters continue to apply.
- Use **DimDate[YearMonth]** rows or one complete month selection for MoM, and the
  same contiguous period in each year for YoY. DATEADD shifts the actual selected
  dates; it does not find the last nonblank month. A partial-month selection is
  shifted as selected dates, subject to DATEADD's calendar/month-end rules.
  Noncontiguous selections, such as January and March without February, can
  cause DATEADD errors even though the full DimDate table is contiguous.
- Previous-period measures return blank if there are no matching sales. MoM
  Change, MoM %, and YoY % also return blank if current sales are blank; missing
  sales are not converted to zero or a false negative growth rate. January 2025
  has no previous month in this dataset, and 2025 has no prior-year sales.
- A genuine previous-period revenue of zero allows an LKR change, but DIVIDE
  leaves the growth percentage blank because division by zero is undefined.
- YTD uses a calendar year ending December 31 and the latest selected date,
  rather than today's date or the latest sales date. It can carry accumulated
  sales into October–December 2026 despite no sales in those months. In a total
  covering several years, it returns YTD for the latest selected year, not a
  sum of yearly YTD values.
- Sales end **2026-09-30**, while DimDate ends **2026-12-31**. For a fair 2026
  year-to-date comparison, select January–September 2026 so the previous-year
  measure covers January–September 2025. Selecting the whole of 2026 instead
  compares its available nine months with all of 2025; these measures do not
  automatically align incomplete periods. Grand totals recalculate the selected
  date range; they do not add or average the displayed monthly growth rates.

These formulas use classic date-column
[DATEADD](https://learn.microsoft.com/en-us/dax/dateadd-function-dax),
[DATESYTD](https://learn.microsoft.com/en-us/dax/datesytd-function-dax), and
[DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax).
Creating and checking the time measures in Desktop remains pending.
