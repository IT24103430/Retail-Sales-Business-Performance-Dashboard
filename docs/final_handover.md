# Retail Sales Analytics — final handover

Review date: **25 October 2026**. Review environment: **Python 3.14.7 on macOS
(Darwin ARM64)**.

**Source and data review completed. Power BI Desktop verification is pending.**
Power BI Desktop was not available or used. No dashboard has been opened,
refreshed, rendered, or verified there. No PBIP, PBIR, TMDL, or PBIX artifact
exists in this repository at handover.

## 1. What was actually completed

- One organized repository with five synthetic CSVs, three executable Python
  scripts, a data dictionary, a generated quality profile and calculated insights.
- Five Power Query M scripts using one configurable `DataFolder` parameter;
  nine core and six time-intelligence DAX measure definitions; one report theme.
- A documented six-table star schema, DimDate expression, three page
  specifications, design rules and report interaction instructions.
- A truthful README, interview Q&A and CV project description. The report and
  screenshots are explicitly marked pending.
- This comprehensive review. No defects were found in the current dataset or
  KPI calculations that required changing the working scripts. Documentation
  corrections clarify that processed CSVs are not produced, align the shared
  slicer order and replace outdated Git synchronization statements.

Cleaning remains in the M source; `data/processed/` and `docs/screenshots/`
contain only `.gitkeep`. See the [README](../README.md) for the file tree and
[business insights](business_insights.md) for the five calculated findings and
three fictional business recommendations.

## 2. What was tested

### Executed checks and results

| Area | Result and scope |
| --- | --- |
| Structure | Required folders and canonical files exist; no duplicate datasets or report projects. All local Markdown links and linked headings resolve. |
| CSV contract | Exact headers, row counts, required values and trimmed labels checked across all five CSVs; no malformed rows or missing cells. |
| Primary keys | SalesLineID and all four dimension keys are unique and nonblank; zero duplicates. OrderID intentionally repeats across lines. |
| Foreign keys | All four fact-to-dimension links and customer-to-region source link match; zero invalid keys. Fact/customer regions agree. |
| Orders and values | Orders have consistent date/customer/region/channel and one to four lines. Quantities are positive integers; costs are nonnegative and below prices; discounts stay between zero and gross line sales. |
| Date coverage | Exact endpoints 2025-01-01 and 2026-09-30; all 21 months have sales. There are 620 observed sales dates in the 638-day interval; missing transaction days are valid. |
| DimDate design | An independently generated 730-day calendar from 2025-01-01 through 2026-12-31 is contiguous and covers every fact date. The documented DAX table has not been evaluated in Desktop. |
| Reproducibility | Rebuilt the seeded generator output in memory; all five serialized CSVs matched the existing files byte for byte without overwriting the data. |
| Python scripts | All three scripts compile. Re-ran the profiler and insight generator successfully; both generated reports remained byte-identical. |
| Financial reconciliation | Independently calculated line amounts with Decimal arithmetic; reconciled totals and month/category/product/region/channel groups against the insight script. Confirmed the README figures and reported leaders. |
| Power Query | Static inspection: all five DataFolder-based paths, filenames, headers, query dependencies, types and four calculated-column formulas agree with the source contract. No hardcoded computer path in M. Not an M refresh test. |
| DAX | Static inspection: exactly 15 unique measures; column and measure references resolve to the intended model. Reviewed distinct-order logic, ratios, time comparisons and blank guards. Not a DAX engine test. |
| Theme | JSON parsed and passed Microsoft's report-theme schemas 2.114 and 2.159 using a temporary JSON Schema validator. No application dependency was added. Desktop import remains pending. |
| Color contrast | Specified navy/teal/slate text pairs exceed 4.5:1 on white/light gray; six chart colors exceed 3:1 on white. Rendered accessibility and layout still need inspection. |
| GitHub content | Before review edits, all 42 source files matched GitHub main by Git blob hash. No tracked caches, temporary files, OS junk or common credential signatures were found in current source files; this was not a historical secret scan. |
| Git and ignore rules | Fetched GitHub main, aligned the older local branch/index without changing source bytes, and confirmed a clean baseline. Ignore checks retain all actual sources and representative PBIP/PBIR/TMDL definitions/resources while excluding local caches/settings. |

The theme checks used Microsoft's published
[2.114 schema](https://github.com/microsoft/powerbi-desktop-samples/blob/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.114.json) and
[2.159 schema](https://github.com/microsoft/powerbi-desktop-samples/blob/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.159.json).
Schema acceptance does not establish successful theme rendering.

### Source-derived reconciliation baseline

These are **synthetic portfolio results**, calculated from the current CSVs.
They are expected Desktop results with the full sales period, All categorical
slicers and no analytical selection; they are not observed Desktop results.

| Table | Expected imported rows |
| --- | ---: |
| FactSales | 5,000 |
| DimProducts | 30 |
| DimCustomers | 700 |
| DimRegions | 9 |
| DimChannels | 4 |
| DimDate, after creating it in Desktop | 730 |

| Measure | Expected value |
| --- | ---: |
| Gross Revenue | LKR 12,892,276.50 |
| Total Discount | LKR 543,544.21 |
| Total Revenue | LKR 12,348,732.29 |
| Total Cost | LKR 8,888,670.77 |
| Total Profit | LKR 3,460,061.52 |
| Profit Margin % | 28.02% |
| Total Orders | 2,453 |
| Units Sold | 11,699 |
| Average Order Value | LKR 5,034.13 |

Revenue subtracts the complete line discount once. Profit subtracts product costs
and excludes operating expenses. Orders are distinct OrderID values: adding the
six category order counts gives 4,409, which correctly exceeds the overall 2,453
because baskets can span categories. Ratios must be recalculated from totals.

## 3. What still needs Power BI Desktop on Windows

All model import/refresh, M evaluation, DimDate creation, relationships, DAX
evaluation, theme import, page construction, interactions, reopening and screenshot
capture remain pending. The Python results do not verify these activities.

PBIP/PBIR/TMDL validation was **not applicable** because no such files exist.
After Desktop generates them, validate PBIR JSON against each file's declared
`$schema`, retain generated IDs and references, and load the TMDL model through
Desktop or an appropriate TOM/TMDL tool. TMDL is a model grammar, not JSON; JSON
validation cannot test DAX, M, refresh or rendering. These boundaries follow
Microsoft's [PBIR documentation](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)
and [TMDL documentation](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview).

## 4. Exact order of final manual actions

Follow these steps in order. The [Desktop build guide](powerbi_desktop_build_steps.md)
contains the full copy/paste instructions; reuse its existing assets.

1. **Prepare Windows and the files.** Use standard Power BI Desktop for Windows,
   not the Report Server edition. Keep the latest repository in one local folder,
   for example `C:\BI\RetailSalesAnalytics`; ensure the CSVs are downloaded.
   Keep the generated dataset. Regeneration is optional, not a Desktop prerequisite.
2. **Open or start the report.** If a genuine
   `powerbi\RetailSalesAnalytics.pbip` now exists, open it and preserve its files.
   Otherwise start a blank report. Enable the supported PBIP/TMDL options if the
   installed release requires them, restarting if prompted; update Desktop if the
   needed formats are unavailable. Turn off Current File → Data Load → Auto
   date/time for this model. Microsoft's [PBIP guide](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
   describes project saving and supported files.
3. **Configure the source path.** Open Home → Transform data. In Power Query
   Editor, use Home → Manage Parameters → New Parameter: name `DataFolder`,
   Required on, Type Text, Suggested Values Any value. Set Current Value to
   `C:\BI\RetailSalesAnalytics\data\raw`, adjusted to your actual folder, with no
   quotes. Update an existing parameter instead of duplicating it.
4. **Load the five queries in dependency order.** Create/reuse Blank Queries
   named `DimRegions`, `DimProducts`, `DimChannels`, `DimCustomers`, then
   `FactSales`. Paste each matching `.m` file from `powerbi/queries/` into its
   Advanced Editor. Keep Enable load on for the five tables; DataFolder is a
   scalar parameter. Use consistent source privacy settings if prompted.
5. **Apply and reconcile the import.** Choose Close & Apply, then Home → Refresh.
   Resolve errors and confirm the five source row counts above. Check Text keys,
   Date OrderDate, Whole Number Quantity, and Fixed Decimal money. FactSales must
   have GrossSales, NetSales, TotalCost and LineProfit. For `SL000001`, these are
   respectively LKR 252.00, 226.80, 196.56 and 30.24. Do not recreate the columns.
6. **Create dates and relationships.** Paste the complete DimDate New table
   expression from [data_model.md](data_model.md). Mark DimDate as the Date table
   using Date; sort MonthName by MonthNumber and YearMonth by YearMonthSort.
   Create the five active 1:* relationships listed there, with single filtering
   from dimensions to FactSales. Remove unintended automatic links, including
   DimRegions-to-DimCustomers. Confirm 730 unique contiguous date rows.
7. **Create and format measures.** Add the nine definitions from
   [core_measures.dax](../powerbi/measures/core_measures.dax), then the six from
   [time_measures.dax](../powerbi/measures/time_measures.dax), one New measure at
   a time. Reuse existing exact names. Follow [dax_guide.md](dax_guide.md): money
   `"LKR" #,##0.00;-"LKR" #,##0.00`, counts `#,##0`, ratios `0.00%`. Keep values
   numeric; `Total Cost` is a measure and `TotalCost` is a column.
8. **Import the theme and save a real project.** Choose Design → Import theme
   (older releases: View → Themes → Browse for themes), and select
   `powerbi/theme/retail_theme.json`. Save as
   `powerbi\RetailSalesAnalytics.pbip` using the actual Power BI Project file
   type. Ensure Desktop stores enhanced PBIR and a TMDL semantic model, following
   the build guide. Preserve Desktop-generated definitions and theme resources.
   Do not rename a file extension to simulate a project.
9. **Build the three pages.** Use a 1600 × 900 canvas and follow the exact visual
   assignments in [Executive Overview](page_01_executive_overview.md),
   [Product Performance](page_02_product_performance.md) and
   [Regional & Channel](page_03_regional_channel.md), in that order. Put the
   inclusive 2025-01-01–2026-09-30 Date bounds on every page and lock them.
10. **Configure interactions.** Follow [report_interactions.md](report_interactions.md):
    synchronize and show Date, Category, Region and Channel on every page;
    keep Product local to Product Performance. Set analytical interactions to
    Filter, leave slicer lists stable except Category → Product, add the native
    page navigator and chart tooltips. Create the three named reset bookmarks
    with Data on, All visuals, Display off and Current page off; bind each
    page's Reset filters button to its matching bookmark.
11. **Check the actual measures and visuals.** Use the acceptance checks below.
    Temporarily add a Table visual for measures not otherwise visible, then
    remove it after checking. Fix discrepancies before capturing screenshots.
12. **Save, close and reopen.** Confirm actual `.pbip`, Report/`definition.pbir`,
    Report/`definition/`, SemanticModel/`definition.pbism` and semantic-model
    `definition/*.tmdl` files exist. Open the saved PBIP, refresh again and confirm
    all three pages and the default totals. Validate generated JSON schemas where
    tools support them; a successful Desktop load is also required.
13. **Record evidence, then capture and publish.** Record the actual Desktop
    version, validation date, observed results and unresolved issues here. Update
    README/CV status only for work actually completed; use sections 5 and 6 below.

### Desktop acceptance checks — all pending

- **Totals:** At defaults and with no chart selection, reconcile all nine core
  measures with the baseline. Confirm each table's rows and the five relationships.
- **Time measures:** Select the complete April 2026 date range, all other slicers
  All. Expected revenue is LKR 962,743.97, Previous Month LKR 631,781.15,
  MoM Change LKR 330,962.82, MoM 52.39%, Previous Year LKR 858,777.52,
  YoY 12.11%, and YTD LKR 2,573,168.53. January 2025 previous-month/year and
  growth comparisons should be blank. These are source-calculated expectations.
- **Filter propagation:** Select Western, Online Store and Groceries for the
  full sales period. Expected revenue is LKR 149,716.86, profit LKR 39,581.49
  and orders 80. Shared controls must retain their selections across pages.
  A Product selection must affect only Product Performance. Check chart filtering,
  revenue/profit/orders tooltips, page navigation and each page's reset button.
- **Visual checks:** Monthly axes run chronologically across both years. Top 10
  and below-28% filters affect only their specified visuals. At defaults, the
  regional matrix grand total equals the revenue card. Verify labels, signs,
  LKR/percentage formats, scroll access, contrast, tab order and readable cards
  with no overlaps or clipped text. City labels must remain representative regions.
- **Comparison limits:** Use contiguous dates. For 2026 YoY, compare the same
  January–September periods; available revenue is LKR 5,029,286.07 in 2026 versus
  LKR 5,225,429.93 in 2025 for those months. Full-year and partial-year selections
  are not interchangeable. Clear temporary selections and restore defaults.

## 5. Capture authentic screenshots

Only after the pages successfully render and the checks pass:

1. Reset each page, set the full sales period and All categorical selections,
   clear chart selections, and wait for rendering. Use Fit to page and maximize
   the report area; dismiss menus and incidental tooltips.
2. Use Windows Snipping Tool (`Win+Shift+S`) to capture the actual report canvas,
   including page title, slicer context, KPI cards and charts. Cropping empty
   window borders is fine; do not alter displayed numbers or substitute mockups.
3. Save these PNGs in the existing `docs/screenshots/` folder:

   | Page | Filename to create after capture |
   | --- | --- |
   | Executive Overview | `executive_overview.png` |
   | Product Performance | `product_performance.png` |
   | Regional & Channel | `regional_channel.png` |

4. Inspect the saved images for readable text. Add relative Markdown image links
   to README only after the files exist, with captions stating the capture date
   and filter context. Screenshots demonstrate appearance; record refresh and
   interaction checks separately.

No screenshot was created or verified during this review.

## 6. Publish this project on GitHub

Continue using the existing repository:
[Retail-Sales-Business-Performance-Dashboard](https://github.com/IT24103430/Retail-Sales-Business-Performance-Dashboard).
Keep one project folder and the existing history. GitHub hosts the source and
screenshots; it does not render the PBIP as an interactive report.

After completing the Windows work, run these commands from the project root in
its Git checkout. First inspect the changes; do not create another repository.

```sh
git status --short
git diff --check
git diff --stat
git add README.md .gitignore requirements.txt data scripts powerbi docs
git diff --cached --stat
git commit -m "Complete Desktop report validation and add authentic screenshots"
git push origin main
git status --short
```

Use that completion message only after the stated Desktop work is done. Include
the actual generated PBIP/PBIR/TMDL definitions, required registered theme resources
and genuine screenshots. Retain CSVs, M/DAX assets and documentation. Exclude
virtual environments, caches, `.pbi/localSettings.json`, `.pbi/cache.abf` and
temporary files. Apply pending Power Query changes before saving the project.

If another commit reaches GitHub first, integrate it before pushing; do not force
push over the existing history. If no Git client is available, use the existing
repository's **Add file → Upload files** to upload changed source files/folders,
preserving their paths and excluding ignored local artifacts, then commit to main.

Finally inspect GitHub's main branch: check the commit, folder structure, README
images and source files. A blank final `git status --short` means the local working
tree is clean. Keep the project marked **Desktop verification pending** until the
manual acceptance results have actually been recorded successfully.
