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
| Executive Overview | Revenue, profit, order count, average order value, monthly revenue trend, and category contribution. |
| Product Performance | Top products, units sold, category revenue, and product profitability. |
| Regional Sales Analysis | Regional revenue, profit, revenue share, and monthly regional trends. |

Use date, region, and category filters where relevant. Planned KPIs are Total Revenue, Total Cost, Total Profit, Profit Margin %, Total Orders, Average Order Value, Sales MoM %, Sales YoY %, and Sales YTD.

## Consistent file naming

- Use lowercase `snake_case` for scripts, CSV files, documentation, query files, measure files, themes, and screenshots.
- Raw data paths: `data/raw/fact_sales.csv`, `data/raw/dim_products.csv`, `data/raw/dim_customers.csv`, `data/raw/dim_regions.csv`, and `data/raw/dim_channels.csv`. Reserve `data/processed/` for prepared outputs; keep one canonical file per table at each stage.
- Use descriptive script names such as `scripts/generate_data.py`; avoid names such as `final_v2.py`.
- Keep core measure definitions in `powerbi/measures/core_measures.dax`, time-intelligence definitions in `powerbi/measures/time_measures.dax`, and the single theme in `powerbi/theme/retail_theme.json`.
- Name the report `RetailSalesAnalytics.pbix` or `RetailSalesAnalytics.pbip` when it is actually created. Document the chosen format and keep one report source.
- Name screenshots `executive_overview.png`, `product_performance.png`, and `regional_sales_analysis.png`.
- Preserve fact columns: `SalesLineID`, `OrderID`, `OrderDate`, `ProductID`, `CustomerID`, `RegionID`, `ChannelID`, `Quantity`, `UnitPrice`, `UnitCost`, and `DiscountAmount`. Dimension labels live in the dimension files; see `data/README.md` for their columns. Revenue subtracts line discounts from gross sales.
- Use `FactSales`, `DimDate`, `DimProducts`, `DimCustomers`, `DimRegions`, and `DimChannels` for model tables. Keep measure names consistent with the README.

## Current status

Folder setup, synthetic data generation, the data dictionary, and the basic profile are complete. The five Power Query scripts and `docs/power_query_setup.md` are prepared, including GrossSales, NetSales, TotalCost, and LineProfit fact columns. The generator creates 5,000 order lines for 2025-01-01 through 2026-09-30. The star schema and DimDate instructions are in `docs/data_model.md`. The nine core DAX measures are prepared in `powerbi/measures/core_measures.dax` and six time-intelligence measures in `powerbi/measures/time_measures.dax`, with formatting, usage, and period assumptions in `docs/dax_guide.md`. The theme is prepared in `powerbi/theme/retail_theme.json`, with layout and formatting rules in `docs/design_system.md`. Executing queries and measures, importing the theme in Desktop, the report, and screenshots remain pending. Power BI Desktop work is pending; no PBIX or PBIP has been created or verified.
