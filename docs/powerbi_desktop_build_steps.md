# Build Retail Sales Analytics in Power BI Desktop

## Review outcome: source assets ready, Desktop project pending

The repository contains no `.pbip`, `.pbix`, `definition.pbir`, `definition.pbism`,
or `.tmdl` scaffold to preserve or extend. This workspace runs macOS ARM64;
.NET SDK **10.0.400** is present, but Power BI Desktop and its local
model/refresh/rendering engine are not available. No callable Power BI tools,
PowerShell, pbi-tools, or Wine were found. The SDK alone does not provide a
Power BI report renderer. There is no existing Desktop-generated report metadata
to reuse.

Microsoft supports programmatic PBIR/TMDL editing, but a schema-valid JSON file
alone does not establish that queries, DAX, report bindings, resources, and
interactions work together. This step uses the requested Desktop-build fallback
rather than presenting an unverified generated project as working. All existing
source assets are preserved; no PBIP/PBIR/TMDL or PBIX artifact was fabricated.

| Component | Completed in the repository | Still requires Desktop |
| --- | --- | --- |
| Synthetic CSVs | Five files; 5,000 sales lines, 30 products, 700 customers, nine regions, four channels | Import and refresh in the model |
| Power Query | Five M scripts; CSV headers match their selected columns; configurable DataFolder reference | Create the parameter, load queries, evaluate cleaning and calculated columns |
| Model | Documented six-table star schema and contiguous DimDate DAX | Create tables, mark dates, configure five relationships |
| Measures | Nine core and six time measures, with distinct names and documented formats | Create, evaluate, and format the 15 measures |
| Theme | `powerbi/theme/retail_theme.json` parses as JSON | Import, register resources, and inspect rendering |
| Report | Three page specifications and report-wide interaction instructions | Build visuals, slicer synchronization, navigation, tooltips, reset bookmarks |
| PBIP/PBIR/TMDL | Official formats reviewed; target structure described below | Let Desktop generate the actual project files and verify reopening |

The current source check confirmed that the five M queries select the actual
CSV headers and share DataFolder-based paths, all 15 measure definitions have
unique names, and the model, theme, page and interaction assets exist. No PBIP/PBIR
descriptors or TMDL model files were available for schema/model-load validation.
These checks do not execute M or DAX and do not connect or refresh a Desktop model.

For the comprehensive source/data review results, verified source-based totals,
GitHub status, and remaining Desktop acceptance checks, see
[final_handover.md](final_handover.md). The source files are preserved and local
Git metadata has been reconciled with GitHub. Desktop work remains pending.

## 1. Prepare a supported Windows environment

1. Use the current standard **Power BI Desktop for Windows**, rather than the
   Report Server edition. Make the full current repository available locally,
   including the existing `data`, `scripts`, `powerbi`, and `docs` folders.
2. Use a short local project path. For example, if the project is at
   `C:\BI\RetailSalesAnalytics`, its raw data folder is
   `C:\BI\RetailSalesAnalytics\data\raw`. Use your actual location throughout.
3. Ensure the five CSVs have actual local contents, not cloud-only placeholders.
   The generated files already exist; do not create another dataset or rerun the
   generator simply to start Desktop.
4. Check **File → Options and settings → Options → Preview features** only if
   your installed release does not expose the required formats. Older releases
   may show **Power BI Project (.pbip) save option**, **Store semantic model using
   TMDL format**, and **Store reports using enhanced metadata format (PBIR)**.
   Enable the applicable available options and restart when prompted. Current
   Desktop uses PBIR by default; absence of an old preview checkbox is not itself
   an error. If an older build cannot save the required formats, update Desktop.

PBIP structure and Windows limitations are documented in Microsoft's
[project overview](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview).
For current PBIR behavior, see [the report format documentation](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report#convert-existing-report-to-pbir).

If an actual `powerbi\RetailSalesAnalytics.pbip` has been created since this
review, open that project and update it instead of making another report/model.
Preserve its generated files and identifiers. Otherwise start a blank report.

## 2. Connect the existing CSVs through DataFolder

1. Select **Home → Transform data** to open Power Query Editor.
2. Select **Home → Manage Parameters → New Parameter**. Create:

   | Setting | Value |
   | --- | --- |
   | Name | `DataFolder` |
   | Required | Checked |
   | Type | Text |
   | Suggested Values | Any value |
   | Current Value | Your full raw-data directory, for example `C:\BI\RetailSalesAnalytics\data\raw`, without quotation marks |

3. For each row below, create **Home → New Source → Other Sources → Blank Query**,
   rename it exactly, choose **View → Advanced Editor**, replace all code with
   the corresponding `.m` file's complete contents, and select **Done**.

   | Order | Query name | Existing source file |
   | ---: | --- | --- |
   | 1 | `DimRegions` | `powerbi/queries/dim_regions.m` |
   | 2 | `DimProducts` | `powerbi/queries/dim_products.m` |
   | 3 | `DimChannels` | `powerbi/queries/dim_channels.m` |
   | 4 | `DimCustomers` | `powerbi/queries/dim_customers.m` |
   | 5 | `FactSales` | `powerbi/queries/fact_sales.m` |

4. Keep **Enable load** on for these five tables. DataFolder is a scalar
   parameter, not a sixth query table. Reuse any correctly named existing query
   instead of adding a duplicate. The order matters because customers reference
   regions and FactSales references all four dimensions.
5. If file-source privacy is requested, use the same appropriate level for these
   synthetic local CSVs, such as Organizational. Select **Close & Apply** and
   allow import to complete; resolve any error before continuing.

The M scripts already set types, trim text, clean invalid rows, check keys, and
add **GrossSales, NetSales, TotalCost, and LineProfit**. Do not recreate these as
DAX columns or subtract discounts from NetSales again. The expected table row
counts are in the status table above; Desktop must confirm them after import.
See [Power Query setup](power_query_setup.md) for cleaning rules and troubleshooting.

Moving the project later requires changing **DataFolder** in Manage Parameters
and refreshing. It does not require editing the five M scripts, CSV filenames,
or a separate absolute path in every table.

## 3. Create the star schema and DimDate

1. In **File → Options and settings → Options → Current File → Data Load**,
   turn off **Auto date/time** for this explicit-date-table model.
2. Select **Modeling → New table**. Copy the complete `DimDate =` expression from
   [data_model.md](data_model.md#create-the-contiguous-dimdate-table), paste it,
   and press Enter. Keep this as one table, not another CSV or query.
3. Confirm `DimDate[Date]` and `FactSales[OrderDate]` have data type **Date**.
   DimDate should contain 730 unique daily rows, 2025-01-01 through 2026-12-31,
   covering full years around the available sales period.
4. Right-click **DimDate → Mark as date table → Mark as date table**, choose
   **Date**, and confirm. In releases that group it under **Calendar options**,
   open that menu to reach the setting.
5. In Report view's Data pane, select **DimDate[MonthName]**, then
   **Column tools → Sort by column → MonthNumber**. Set **YearMonth → YearMonthSort**
   in the same way.
6. In **Model view → Manage relationships**, create or correct these links:

   | Dimension, one side | Fact, many side | Settings |
   | --- | --- | --- |
   | DimProducts[ProductID] | FactSales[ProductID] | Active, 1:*, Single dimension → fact |
   | DimCustomers[CustomerID] | FactSales[CustomerID] | Active, 1:*, Single dimension → fact |
   | DimRegions[RegionID] | FactSales[RegionID] | Active, 1:*, Single dimension → fact |
   | DimChannels[ChannelID] | FactSales[ChannelID] | Active, 1:*, Single dimension → fact |
   | DimDate[Date] | FactSales[OrderDate] | Active, 1:*, Single dimension → fact |

Use Text for the ID keys on both sides. Remove automatically detected
dimension-to-dimension relationships, particularly a DimRegions-to-DimCustomers
link. Customer RegionID remains reference information. Keep the five links above,
with no many-to-many or bidirectional relationship. The full model reasoning is
in [data_model.md](data_model.md).

## 4. Add the existing measures

1. Right-click **FactSales → New measure**. Copy one definition at a time from
   [core_measures.dax](../powerbi/measures/core_measures.dax), in file order,
   starting at its measure name and `=`. Press Enter after each definition.
2. Repeat for all six definitions in
   [time_measures.dax](../powerbi/measures/time_measures.dax), after the core
   definitions exist. Keep FactSales as their home table. Replace any existing
   correctly named measure rather than creating another version.
3. Apply the model-level formats in [dax_guide.md](dax_guide.md): LKR with two
   decimals for money, `#,##0` for counts, and `0.00%` for percentages. Keep
   measures numeric. The measure **Total Cost** is distinct from the column
   **TotalCost**.

Expected measures, exactly once each:

| Core (9) | Time intelligence (6) |
| --- | --- |
| Gross Revenue; Total Revenue; Total Cost; Total Profit; Profit Margin %; Total Orders; Units Sold; Average Order Value; Total Discount | Sales Previous Month; Sales MoM Change; Sales MoM %; Sales Previous Year; Sales YoY %; Sales YTD |

The `.dax` files are copy-ready individual measure definitions, not complete DAX
queries or importable TMDL model files. The classic time measures depend on the
marked DimDate and its active relationship. Respect the documented blank and
partial-year assumptions.

## 5. Save a genuine PBIP scaffold under powerbi

1. Choose **File → Save as**, browse to this repository's **powerbi** folder,
   select **Power BI Project files (*.pbip)**, and name the project
   **RetailSalesAnalytics.pbip**. Do not just rename another file's extension.
2. Let Desktop generate its report and semantic-model folders. If the semantic
   model is initially TMSL (`model.bim`), use the installed release's TMDL
   conversion workflow: enable **Store semantic model using TMDL format** if
   offered, reopen/save the PBIP, and accept **Upgrade** when prompted. Preserve
   a committed checkpoint before converting an existing project. If conversion
   is unavailable, update Desktop rather than hand-editing a descriptor version.
3. Confirm the semantic model is saved as **definition/*.tmdl**, not only a
   TMDL editor script under **TMDLScripts/**. Current Desktop saves reports in
   enhanced **PBIR**, with the report definition split under **Report/definition/**.
   An older release may require the PBIR option before saving/converting.

The following is the **expected Desktop-generated structure**, not files created
by this review. Desktop may also create optional documented files and use
different generated IDs or resource filenames; keep those valid files.

```text
powerbi/
├── queries/                         # Existing M source assets
├── measures/                        # Existing DAX source assets
├── theme/retail_theme.json           # Existing canonical theme asset
├── RetailSalesAnalytics.pbip         # Generated by Desktop
├── RetailSalesAnalytics.Report/
│   ├── definition.pbir
│   ├── definition/
│   │   ├── version.json
│   │   ├── report.json
│   │   ├── pages/
│   │   │   ├── pages.json
│   │   │   └── <page-id>/
│   │   │       ├── page.json
│   │   │       └── visuals/<visual-id>/visual.json
│   │   └── bookmarks/               # After reset bookmarks are created
│   └── StaticResources/             # Theme resources registered by Desktop
└── RetailSalesAnalytics.SemanticModel/
    ├── definition.pbism
    └── definition/
        ├── database.tmdl
        ├── model.tmdl
        ├── expressions.tmdl         # Includes the DataFolder parameter
        ├── relationships.tmdl
        └── tables/                  # Six model tables and their metadata
```

The PBIP points to the Report folder. `definition.pbir` should reference the
semantic model with a **relative byPath** value such as
`../RetailSalesAnalytics.SemanticModel`. That reference connects report metadata
to the model; **DataFolder** separately locates the CSVs. Accept Desktop's
schema/version declarations and generated IDs instead of inventing replacements.
See Microsoft's [report-folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)
and [semantic-model-folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)
documentation for the two formats.

## 6. Import the theme and build the three pages

1. Select **Design → Import theme**, choose the existing
   `powerbi/theme/retail_theme.json`, and confirm import. In an older ribbon use
   **View → Themes → Browse for themes**. Save so Desktop registers the theme's
   report resource references. Keep the canonical source theme as well as the
   resource copy Desktop requires; do not manually guess resource-package JSON.
2. Rename/order the report pages as shown below, reusing the initial blank page.
   Set each page's **Canvas settings → Type → Custom → 1600 × 900**.
3. On every page, set and lock the page-level Date bounds **2025-01-01 through
   2026-09-30**. Build the native visuals using the exact fields, filters, sorting,
   and formatting in each linked specification:

   | Page | Required content / specification |
   | --- | --- |
   | Executive Overview | Five KPI cards; monthly revenue, category/channel revenue, and region ranking — [Page 01](page_01_executive_overview.md) |
   | Product Performance | Units/revenue/margin cards; Top 10 products, category revenue vs profit, below-28% review table, and category trends — [Page 02](page_02_product_performance.md) |
   | Regional & Channel | Revenue/orders/AOV cards; region/representative-city and channel bars, monthly region small multiples, region-by-category matrix — [Page 03](page_03_regional_channel.md) |

All three pages use shared Date, Category, Region, and Channel controls; Product
Performance also has a local Product control. Region City labels are
representative metadata, not independently measured city sales. The 28% product
review threshold is a synthetic demonstration assumption, not a business target.

## 7. Configure shared interactions

Follow [report_interactions.md](report_interactions.md), the authoritative
report-wide interaction guide:

1. In **View → Sync slicers**, synchronize and show the four shared controls on
   all pages; keep Product local. Use one control per field per page.
2. Use **Format → Edit interactions** for chart cross-filtering and stable slicer
   lists; retain the Category-to-Product cascade on Product Performance.
3. Insert a native **Buttons → Navigator → Page navigator** on each page. Use
   page navigation, not filter-capturing bookmarks, for moving between pages.
4. Add revenue/profit/distinct-orders tooltip measures to native chart tooltips
   where supported. Keep native table/matrix hover behavior where there is no
   editable tooltip field well.
5. Create the three reset bookmarks and buttons with the exact names/options in
   that guide. Reset shared selections and the active page's local selections;
   do not claim it resets stored chart selections on all other pages.
6. Restore default dates, All categorical selections, no analytical selection,
   and Executive Overview as the starting page. Save again.

## 8. Reopen and confirm the generated formats

1. Save all changes and close Desktop. In File Explorer, confirm the actual
   PBIP, Report/definition.pbir, Report/definition folder, SemanticModel/
   definition.pbism, and SemanticModel/definition/*.tmdl files exist.
2. In PBIR, a `report.json` **inside Report/definition/** is documented and
   supported. A single **Report/report.json** is the legacy layout; it is not
   evidence of an enhanced PBIR report. Descriptor versions alone do not prove
   that the selected definition formats were used.
3. Open **powerbi/RetailSalesAnalytics.pbip** in Desktop, allow loading, set
   DataFolder for this computer if needed, and select **Home → Refresh**.
4. Perform one quick reconciliation with default slicers and no chart selection:
   FactSales 5,000 rows; Total Orders 2,453; Total Revenue LKR 12,348,732.29;
   Total Profit LKR 3,460,061.52. Check that all three pages appear and navigation,
   shared slicers, and one reset button behave as specified. These are expected
   results from the source profile, not completed Desktop tests.
5. Record the actual Desktop version and the successful open/refresh result in
   the project status only after doing it. Capture genuine screenshots in
   `docs/screenshots/` only after the pages render. Complete the Desktop acceptance
   checks in [final_handover.md](final_handover.md) before changing the project status.

## Supported editing boundary after the scaffold exists

Use the `$schema` references **in the generated PBIR files** when validating later
JSON edits against Microsoft's [published schemas](https://github.com/microsoft/json-schemas/tree/main/fabric).
TMDL uses the [TMDL grammar and Tabular Object Model](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview),
not a made-up JSON schema. Desktop or an appropriate TOM/TMDL tool must load the
model metadata; JSON parsing cannot validate its DAX or M execution.

Preserve names and generated reference IDs when editing supported files. Let
Desktop manage diagrams, internal layout files, resource registration, slicer
groups, and bookmarks. Do not edit undocumented legacy report JSON, invent
fields, manually inflate format versions, or treat a DAX/TMDL script tab as a
saved semantic model. Apply Power Query changes before saving so unapplied
changes do not overwrite a later model edit.

Keep generated definitions and required registered resources in Git. The root
`.gitignore` already excludes local cache/settings files under `.pbi/`; it does
not exclude PBIP/PBIR/TMDL source definitions. Keep one actual report source,
not parallel PBIX and PBIP copies. If PBIX is ever explicitly needed, export it
through Desktop; this step produces no PBIX.

**Completed in this environment:** repository/tool inventory, source-contract
checks, review of Microsoft's format documentation, and this Desktop build path.
All existing CSV/M/DAX/theme and page-specification assets are preserved.
**Pending:** actual PBIP/PBIR/TMDL generation, data connection/refresh, model
loading, all three rendered pages, interactions, reopen verification, and
screenshots in Windows Desktop.
