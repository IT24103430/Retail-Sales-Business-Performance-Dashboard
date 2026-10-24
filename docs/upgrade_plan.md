# Retail Sales Analytics — upgrade plan

Enhance the existing project in place; preserve names, paths and working code.
This is an inventory, not a comprehensive audit. Keep the earlier review in
[final_handover.md](final_handover.md); reserve enhancement QA for **prompt 30**.

## Existing dataset and query names

| Canonical CSV | Rows | Exact query name | Existing M source |
| --- | ---: | --- | --- |
| `data/raw/fact_sales.csv` | 5,000 | FactSales | `powerbi/queries/fact_sales.m` |
| `data/raw/dim_products.csv` | 30 | DimProducts | `powerbi/queries/dim_products.m` |
| `data/raw/dim_customers.csv` | 700 | DimCustomers | `powerbi/queries/dim_customers.m` |
| `data/raw/dim_regions.csv` | 9 | DimRegions | `powerbi/queries/dim_regions.m` |
| `data/raw/dim_channels.csv` | 4 | DimChannels | `powerbi/queries/dim_channels.m` |

- Fact grain is **one product line within an order**, keyed by SalesLineID.
  There are **2,453 distinct orders**, with one to four lines per order.
- Sales cover **2025-01-01 through 2026-09-30**. Keep synthetic Sri Lankan data,
  LKR, anonymous customers and representative city labels.
- All five M sources use `DataFolder`. FactSales defines GrossSales, NetSales,
  TotalCost and LineProfit. Deduct the complete line discount once; count
  distinct OrderID values. Profit excludes operating expenses.
- `data/processed/` has no datasets. Do not regenerate CSVs for this planning step.

## Features already present and gaps

| Feature | Existing work | Missing or pending |
| --- | --- | --- |
| Python workflow | Generator, profiler and insight script; included CSVs, profile and findings | Extend only for a requested feature. |
| Power Query | Five cleaning/type scripts, DataFolder references and setup guide | Parameter creation and query execution in Desktop. |
| Model/date | Six-table star schema; five 1:* single-direction links; contiguous DimDate DAX for 2025-01-01–2026-12-31 with sorting | Actual tables, date marking, relationships and runtime checks. |
| DAX | Nine core and six time measures, formats and assumptions | Desktop creation/evaluation; new analytics only when requested. |
| Report/portfolio | Three page specifications, theme, interaction guide, README, dictionary, interview/CV materials and handover | Rendered pages, tested interactions and authentic screenshots. |
| Power BI project | M/DAX/theme source assets | No PBIP, PBIX, PBIR descriptors or TMDL model files exist. |

**Canonical measures to reuse:**

- `powerbi/measures/core_measures.dax`: Gross Revenue, Total Revenue, Total Cost,
  Total Profit, Profit Margin %, Total Orders, Units Sold, Average Order Value
  and Total Discount.
- `powerbi/measures/time_measures.dax`: Sales Previous Month, Sales MoM Change,
  Sales MoM %, Sales Previous Year, Sales YoY % and Sales YTD.

Customer segments exist; a dedicated customer page, targets, budgets, returns and
inventory are absent. Additional data/features require a future prompt; do not
invent results from unavailable fields.

## Exact files to extend for prompts 19–30

The content of prompts **19–29 has not been supplied**. Route each requested
enhancement through this map; no numbered feature backlog is assumed.

| Prompt / requested enhancement | Exact existing files to extend as needed |
| --- | --- |
| 19–29: source-data or quality changes | `scripts/generate_data.py`, `scripts/profile_data.py`, `data/README.md`, `docs/data_dictionary.md`; update only affected canonical CSVs listed above and regenerate `docs/data_profile.md` when data changes. |
| 19–29: import or cleaning changes | The affected M source listed above and `docs/power_query_setup.md`; retain DataFolder and query names. |
| 19–29: model, date or relationship changes | `docs/data_model.md`, affected existing M sources and `docs/powerbi_desktop_build_steps.md`; update `docs/data_dictionary.md` if columns change. |
| 19–29: business or time measures | `powerbi/measures/core_measures.dax` for business measures, `powerbi/measures/time_measures.dax` for time measures, and `docs/dax_guide.md`; reuse the 15 existing names instead of adding duplicates. |
| 19–29: Executive Overview | `docs/page_01_executive_overview.md`; extend an existing measures file only if the requested visual needs a new calculation. |
| 19–29: Product Performance | `docs/page_02_product_performance.md`; reuse existing product/category fields and measures. |
| 19–29: Regional & Channel | `docs/page_03_regional_channel.md`; retain the representative-city meaning and built-in visuals. |
| 19–29: slicers, navigation, tooltips or reset behavior | `docs/report_interactions.md` and the affected page specification; synchronize shared Date/Category/Region/Channel controls, keeping Product local. |
| 19–29: styling or accessibility | `powerbi/theme/retail_theme.json`, `docs/design_system.md` and the affected page specification. |
| 19–29: new findings or portfolio documentation | `scripts/generate_insights.py`, its generated `docs/business_insights.md`, `README.md`, `docs/interview_prep.md` and `docs/cv_project_description.md`, only where the requested change affects them. |
| 30: comprehensive enhancement review | Run/review the existing scripts as relevant; update `docs/data_profile.md`, `docs/business_insights.md`, `docs/final_handover.md` and `README.md`. Review any actual generated Power BI definitions and record executed checks separately from pending Desktop checks. |

Update `docs/project_plan.md` only when an enhancement changes agreed scope.
Keep documentation links and source definitions aligned with the implementation;
avoid second datasets, replacement scripts and parallel report projects.

## Desktop actions that remain manual

Follow [powerbi_desktop_build_steps.md](powerbi_desktop_build_steps.md) on Windows:

1. Create/reuse the actual report, set DataFolder, load the existing queries and
   apply/refresh the data.
2. Create DimDate and the five relationships; mark/sort dates and create/format
   the measures. Import the existing theme.
3. Build the three pages, configure interactions and save the genuine project
   under `powerbi/` using PBIP, enhanced PBIR and TMDL where supported. The target
   `powerbi/RetailSalesAnalytics.pbip` is a **future Desktop output**, not an
   existing file. Preserve Desktop-generated files and identifiers once present.
4. Open/refresh the saved project, inspect visuals and interactions, record the
   actual results, then capture screenshots in `docs/screenshots/`.

No Power BI Desktop runtime is available here. Source/documentation work can
continue; model execution and visual checks remain pending. Never claim an
untested PBIP/PBIX or source definition is a verified working dashboard.
