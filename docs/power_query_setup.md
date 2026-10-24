# Power Query Setup

These steps must be performed manually in **Power BI Desktop on Windows**.
The M scripts are prepared, but have not been run, refreshed, or verified in
Desktop. No PBIX or PBIP was created for this step.

## 1. Locate the data folder

Copy the complete project folder to the Windows computer. Keep the five generated
CSV files together in `data\raw`. In File Explorer, open that folder, click the
address bar, and copy its full Windows path. Example:

```text
C:\Projects\Retail-Sales-Business-Performance-Dashboard\data\raw
```

Use your actual path. This must be the folder containing `fact_sales.csv` and the
four dimension CSVs, not the project root, `data`, or a CSV filename. The scripts
accept a trailing slash or backslash, but it is not required.

## 2. Create the DataFolder parameter

1. Open Power BI Desktop and create a blank report, or use the project's existing
   report if you have already created one.
2. On the **Home** ribbon, select **Transform data** to open Power Query Editor.
3. In Power Query Editor, select **Home → Manage Parameters → New Parameter**.
4. Fill in the following settings and select **OK**.

| Setting | Value |
| --- | --- |
| Name | `DataFolder` (exact spelling and capitalization) |
| Description | Folder containing the five raw Retail Sales Analytics CSV files |
| Required | Checked |
| Type | Text |
| Suggested Values | Any value |
| Current Value | Paste your full `data\raw` folder path without quotation marks |

If `DataFolder` already exists, edit its Current Value instead of creating another
parameter. It is a text parameter, not a table to load. Microsoft documents these
settings in [Using parameters](https://learn.microsoft.com/en-us/power-query/power-query-query-parameters).

## 3. Create the five queries in this order

File names use lowercase snake_case; query names inside Desktop use the exact
names in this table. These plural dimension names are the project's current
standard and replace the earlier singular names in the initial plan.

| Order | M script in the project | Query name in Desktop | Source CSV |
| ---: | --- | --- | --- |
| 1 | `powerbi/queries/dim_regions.m` | `DimRegions` | `dim_regions.csv` |
| 2 | `powerbi/queries/dim_products.m` | `DimProducts` | `dim_products.csv` |
| 3 | `powerbi/queries/dim_channels.m` | `DimChannels` | `dim_channels.csv` |
| 4 | `powerbi/queries/dim_customers.m` | `DimCustomers` | `dim_customers.csv` |
| 5 | `powerbi/queries/fact_sales.m` | `FactSales` | `fact_sales.csv` |

For **each row**, complete these steps before moving to the next row:

1. Open the `.m` file in a text editor such as Notepad. Copy its complete contents,
   including the comment, `let`, and final `in` expression.
2. In Power Query Editor, select **Home → New Source → Other Sources → Blank Query**.
3. Right-click the new query in the left Queries pane, select **Rename**, and enter
   the exact query name from the table.
4. With that query selected, choose **View → Advanced Editor**.
5. Select all existing code in the editor and paste the complete `.m` script.
   Paste code, not the file path, and do not include Markdown code fences.
6. Select **Done**. Allow the preview to finish. If prompted for the local files'
   privacy level, choose **Organizational** consistently for this project's sources.
7. Right-click the table query and ensure **Enable load** is checked.

If a query already exists, select it and replace its Advanced Editor contents
instead of adding a duplicate. If you previously created singular dimension
queries, rename those to the plural names above and replace their code in the
same order. Query names are case-sensitive in the M references.

The `.m` files are source code: use the Advanced Editor paste method, rather than
importing them as Text/CSV data. Microsoft's [Advanced Editor guide](https://learn.microsoft.com/en-us/power-query/power-query-ui#the-advanced-editor)
describes editing the complete query expression.

`DimCustomers` references `DimRegions`. `FactSales` references all four dimension
queries. Create dimensions first so these references resolve. These query joins
clean keys; they do not create relationships in the Power BI model.

## 4. Understand the cleaning and new columns

All queries read UTF-8, comma-delimited CSVs, promote the first row to headers,
select the required columns, trim text, and turn empty text into null. This trims
`Category` labels in `DimProducts` as well as other labels and identifiers.
Missing required CSV columns cause a visible error so schema changes are noticed.

- Dimensions keep text types and remove rows with errors or missing required
  values. Customers with an unmatched RegionID are also removed.
- FactSales uses Text for identifiers, Date for OrderDate, Whole Number for
  Quantity, and Fixed Decimal Number for money. ISO dates and `en-US` numeric
  parsing match the files' decimal points regardless of Windows regional settings.
  These parsing settings do not change the currency from LKR.
- FactSales removes type errors, missing fields, fractional/nonpositive quantities,
  nonpositive prices, negative costs, costs at or above selling price, discounts
  below zero or above gross line amount, and dates outside the project's
  2025-01-01 through 2026-09-30 coverage. If the project period changes later,
  update the date limits in `fact_sales.m`.
- FactSales removes rows with unmatched product, customer, region, or channel
  keys, and rows whose region disagrees with the customer's region.
- Identical duplicate rows are removed. Conflicting records sharing a primary
  key stop the query with an error; correct the source rather than arbitrarily
  keeping one. Repeated OrderID values are expected and are retained.

FactSales adds these **Power Query columns**, all as Fixed Decimal Number:

| Column | Formula | Meaning |
| --- | --- | --- |
| GrossSales | `Quantity * UnitPrice` | LKR line sales before discounts |
| NetSales | `GrossSales - DiscountAmount` | LKR line revenue after discounts |
| TotalCost | `Quantity * UnitCost` | LKR line cost |
| LineProfit | `NetSales - TotalCost` | LKR line profit |

DiscountAmount is already a line total and is subtracted once. `TotalCost` is a
column; the planned DAX measure `Total Cost` is a separate, spaced name. Model
currency display formatting and DAX measures will be handled in later steps.
The queries read raw CSVs and do not create processed CSVs or change source files.

## 5. Apply and perform a quick manual check

1. In Power Query Editor, select **Home → Close & Apply** and wait for loading.
2. In Desktop's Table view (called Data view in some versions), select each table
   and compare its row count with the expected counts below. The Power Query
   preview may display only a sample; it is not proof of the complete row count.
3. Check that FactSales contains the four new columns. The first raw sales line,
   `SL000001`, should have GrossSales **252.00**, NetSales **226.80**, TotalCost
   **196.56**, and LineProfit **30.24** LKR.

| Table | Expected rows for the current clean CSV files |
| --- | ---: |
| DimRegions | 9 |
| DimProducts | 30 |
| DimChannels | 4 |
| DimCustomers | 700 |
| FactSales | 5,000 |

These are expected results from the inspected source files, not Desktop-verified
results. If rows disappear unexpectedly, review Applied Steps and run
`python3 scripts/profile_data.py` from the project root. The
[data profile](data_profile.md) describes raw inputs; it is not a report of M execution.
Keep model relationships and report design for their later project steps.
Save the actual report under `powerbi/` when you perform this setup in Desktop.

## 6. Move the project to another Windows computer

1. Copy the project and any actual report files to the other computer, preserving
   the relative folders and the five CSV filenames.
2. Open the actual report in Desktop and select **Transform data**.
3. Select **Home → Manage Parameters**, choose `DataFolder`, and replace its
   Current Value with the new computer's full `data\raw` path. Select **OK**.
4. Select **Close & Apply**, then **Home → Refresh** in Desktop. Save the report
   after the refresh succeeds. No M code or individual CSV paths need editing.

For a file-not-found error, check DataFolder and the filenames. For a query-name
error, check exact plural names and creation order. If privacy settings need
correction, use Desktop **File → Options and settings → Data source settings**
and edit the relevant file sources' permissions consistently. Do not disable
privacy checks to hide a configuration problem.

Desktop execution, refresh, and verification are still **pending** until a person
performs these steps in Windows.
