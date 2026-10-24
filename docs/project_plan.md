# Retail Sales Analytics — Project Plan

## Business objective

Use synthetic Sri Lankan retail sales data to explain sales trends, product profitability, and regional performance. Help a retail team decide which products and regions need attention. All monetary values use Sri Lankan rupees (LKR); no real customer information is used.

## Target users

- Business owners and managers reviewing overall performance.
- Sales and regional managers comparing regions and trends.
- Product managers reviewing category sales and profit.
- Beginner BI learners and portfolio reviewers following the workflow.

## Deliverables

- Python scripts in `scripts/` for reproducible synthetic data generation and preparation.
- Raw CSV data in `data/raw/` and cleaned CSV data in `data/processed/`.
- Power Query M files in `powerbi/queries/`, DAX definitions in `powerbi/measures/`, and a JSON theme in `powerbi/theme/`.
- A Power BI report in `powerbi/`, created and checked in Desktop in a later step.
- Setup guidance in `README.md`, business findings in `docs/`, and actual report screenshots in `docs/screenshots/`.

## Dashboard pages

| Page | Main questions and visuals |
| --- | --- |
| Executive Overview | Five KPIs: revenue, profit, margin, orders, and average order value; monthly revenue, category and channel revenue, and region ranking, with date/category/region/channel slicers. See `docs/page_01_executive_overview.md`. |
| Product Performance | Units, revenue, and margin KPIs; Top 10 products, category revenue vs profit, low-margin review table, and monthly category revenue, with shared date/category/region/channel slicers and a local product slicer. See `docs/page_02_product_performance.md`. |
| Regional & Channel | Regional revenue, orders, and AOV KPIs; region/representative-city and channel revenue, monthly regional trends, and region-by-category revenue matrix. See `docs/page_03_regional_channel.md`. |

Use date, region, and category filters where relevant. Planned KPIs are Total Revenue, Total Cost, Total Profit, Profit Margin %, Total Orders, Average Order Value, Sales MoM %, Sales YoY %, and Sales YTD.

## Consistent file naming

- Use lowercase `snake_case` for scripts, CSV files, documentation, query files, measure files, themes, and screenshots.
- Raw data paths: `data/raw/fact_sales.csv`, `data/raw/dim_products.csv`, `data/raw/dim_customers.csv`, `data/raw/dim_regions.csv`, and `data/raw/dim_channels.csv`. Reserve `data/processed/` for prepared outputs; keep one canonical file per table at each stage.
- Use descriptive script names such as `scripts/generate_data.py`; avoid names such as `final_v2.py`.
- Keep core measure definitions in `powerbi/measures/core_measures.dax`, time-intelligence definitions in `powerbi/measures/time_measures.dax`, and the single theme in `powerbi/theme/retail_theme.json`.
- Target the actual Desktop-generated project at `powerbi/RetailSalesAnalytics.pbip`, using enhanced PBIR and TMDL. Follow `docs/powerbi_desktop_build_steps.md` and keep one report source. No PBIP or PBIX has been created.
- Name screenshots `executive_overview.png`, `product_performance.png`, and `regional_channel.png`.
- Preserve fact columns: `SalesLineID`, `OrderID`, `OrderDate`, `ProductID`, `CustomerID`, `RegionID`, `ChannelID`, `Quantity`, `UnitPrice`, `UnitCost`, and `DiscountAmount`. Dimension labels live in the dimension files; see `data/README.md` for their columns. Revenue subtracts line discounts from gross sales.
- Use `FactSales`, `DimDate`, `DimProducts`, `DimCustomers`, `DimRegions`, and `DimChannels` for model tables. Keep measure names consistent with the README.

## Current status

Folder setup, synthetic data generation, the data dictionary, and the basic profile are complete. The five Power Query scripts and `docs/power_query_setup.md` are prepared, including GrossSales, NetSales, TotalCost, and LineProfit fact columns. The generator creates 5,000 order lines for 2025-01-01 through 2026-09-30. The star schema and DimDate instructions are in `docs/data_model.md`. The nine core DAX measures are prepared in `powerbi/measures/core_measures.dax` and six time-intelligence measures in `powerbi/measures/time_measures.dax`, with formatting, usage, and period assumptions in `docs/dax_guide.md`. The theme is prepared in `powerbi/theme/retail_theme.json`, with layout and formatting rules in `docs/design_system.md`. Page build specifications are in `docs/page_01_executive_overview.md`, `docs/page_02_product_performance.md`, and `docs/page_03_regional_channel.md`; none is an implemented page. Regional & Channel uses built-in visuals, existing measures, and representative city labels rather than actual city-level sales. Product Performance reuses existing measures and defines a demonstration low-margin review threshold of 28%. Report-wide slicer synchronization, native navigation, tooltips, and reset-bookmark instructions are in `docs/report_interactions.md`. Executing queries and measures, importing the theme, configuring interactions in Desktop, the report, and screenshots remain pending. Power BI Desktop work is pending; no PBIX or PBIP has been created or verified.

The PBIP readiness review found no Desktop-generated scaffold. Existing CSV/M/DAX/theme assets are preserved; matching committed bytes were restored for cloud-only source placeholders. `docs/powerbi_desktop_build_steps.md` gives the exact fallback build sequence and expected official structure. Actual PBIP/PBIR/TMDL generation, model refresh, report rendering, and Desktop reopening remain pending; no unsupported project metadata was introduced. Local Git metadata still requires its iCloud files to download before local synchronization.

Calculated synthetic business findings and recommendations are generated by `scripts/generate_insights.py` in `docs/business_insights.md`, using the existing CSVs and matching the project revenue/profit definitions. These are source-data insights, not verified Power BI report results.
