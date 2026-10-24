# Core DAX Measures

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
