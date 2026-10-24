# Retail Sales Analytics

**A Sri Lankan retail Business Intelligence portfolio project** using Python,
CSV, Power Query, DAX, and Power BI. It combines reproducible synthetic data,
calculated business insights, and a documented plan for a three-page sales report.
All monetary values use **Sri Lankan rupees (LKR)**.

**5,000 order lines · 2,453 orders · 30 products · 9 regions · 4 channels**

> **Current status:** Python data generation, profiling, and insight generation
> have run successfully. Power Query scripts, DAX measures, the report theme, and
> dashboard specifications are prepared. **No Power BI dashboard has been opened,
> refreshed, rendered, or verified in Desktop. No PBIP or PBIX report exists.**

**Review the project:** [Calculated insights](docs/business_insights.md) ·
[Data quality profile](docs/data_profile.md) ·
[Page specifications](#three-dashboard-pages) ·
[Desktop build steps](docs/powerbi_desktop_build_steps.md).

## Business problem

Retail transaction files contain useful detail, but managers need a clear view of
sales trends, profitability, product performance, and regional/channel results.
This project explores how a BI workflow can answer:

- What revenue remains after discounts, and what profit remains after product costs?
- Which months, products, and categories contribute the most sales?
- Which regions and channels perform strongly, and where should margins be reviewed?
- How many distinct orders were placed, and what is their average value?

The intended users are business owners, sales managers, and product managers.
The scenario is fictional; it does not represent an actual retailer's results.

## Objectives

1. Generate repeatable synthetic retail data and inspect its quality.
2. Prepare reusable Power Query transformations and a clear star-schema design.
3. Define consistent sales, profit, order, and time-intelligence measures.
4. Specify a readable, interactive report and produce source-backed recommendations.

## Completed work and Desktop work

| Deliverable | Evidence in this repository | Status |
| --- | --- | --- |
| Reproducible dataset | [Generator](scripts/generate_data.py) and [raw CSVs](data/raw/) | Generated successfully |
| Data quality profile | [Profiler](scripts/profile_data.py) and [data profile](docs/data_profile.md) | Executed; current profile reports no missing values or key errors |
| Business insights | [Insight generator](scripts/generate_insights.py) and [findings](docs/business_insights.md) | Calculated from CSVs |
| Power Query, DAX, theme | [Queries](powerbi/queries/), [measures](powerbi/measures/), [theme](powerbi/theme/retail_theme.json) | Source assets prepared; Desktop testing pending |
| Model and report design | [Model guide](docs/data_model.md), three page specifications, [design system](docs/design_system.md) | Documented; Desktop implementation pending |
| Working report and screenshots | [Desktop build instructions](docs/powerbi_desktop_build_steps.md) | PBIP/PBIR/TMDL creation, refresh, rendering, and reopening pending |
| Final source and data review | [Final handover](docs/final_handover.md) | Data, reproducibility, source references, theme schemas, and repository checks passed; Desktop acceptance pending |

These statuses distinguish executed Python analysis from supporting materials
awaiting Power BI Desktop. The existing model diagram and wireframes describe the
intended report; they are not screenshots of a finished dashboard.

## Tools

| Tool | Role |
| --- | --- |
| Python | Seeded synthetic data generation, CSV profiling, and calculated insights |
| CSV | Portable source fact and dimension tables |
| Power Query M | Prepared data import, types, text cleaning, key checks, and line calculations |
| DAX | Prepared core KPIs and date comparisons |
| Power BI Desktop | Planned model/report assembly and verification in Windows |
| Git and GitHub | Versioned scripts, data, design specifications, and documentation |

The three current Python scripts use only the standard library.
[requirements.txt](requirements.txt) records pandas for future data preparation;
it is not required to run those scripts.

## Synthetic dataset

Sales cover **2025-01-01 through 2026-09-30**. The generator uses the fixed seed
**20250930**. No personal names, emails, phone numbers, or real customer records
are included. Prices and costs are illustrative LKR values.

| Existing CSV | Rows | Grain |
| --- | ---: | --- |
| [fact_sales.csv](data/raw/fact_sales.csv) | 5,000 | One product line within an order |
| [dim_products.csv](data/raw/dim_products.csv) | 30 | One product, with category and readable label |
| [dim_customers.csv](data/raw/dim_customers.csv) | 700 | One anonymous synthetic customer, with segment and region |
| [dim_regions.csv](data/raw/dim_regions.csv) | 9 | One Sri Lankan province/region, with a representative city |
| [dim_channels.csv](data/raw/dim_channels.csv) | 4 | Physical Store, Online Store, Mobile App, or Telephone Order |

An order can contain several product lines. Region describes the customer's
assigned region; its city is a representative label, not independently measured
city sales. The 2026 sales period is incomplete, so full-year comparisons need care.

The [data README](data/README.md) explains generation assumptions, and the
[data dictionary](docs/data_dictionary.md) defines every source column. The
[data/processed/](data/processed/) folder is reserved; no processed CSVs exist yet.

## Project structure

```text
Retail-Sales-Business-Performance-Dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── raw/
│   │   ├── fact_sales.csv
│   │   ├── dim_products.csv
│   │   ├── dim_customers.csv
│   │   ├── dim_regions.csv
│   │   └── dim_channels.csv
│   └── processed/                   # Reserved; .gitkeep only
├── scripts/
│   ├── generate_data.py
│   ├── profile_data.py
│   └── generate_insights.py
├── powerbi/
│   ├── queries/                     # Five M source scripts
│   ├── measures/
│   │   ├── core_measures.dax
│   │   └── time_measures.dax
│   └── theme/
│       └── retail_theme.json
└── docs/
    ├── project_plan.md
    ├── data_dictionary.md
    ├── data_profile.md
    ├── business_insights.md
    ├── data_model.md
    ├── dax_guide.md
    ├── design_system.md
    ├── power_query_setup.md
    ├── powerbi_desktop_build_steps.md
    ├── page_01_executive_overview.md
    ├── page_02_product_performance.md
    ├── page_03_regional_channel.md
    ├── report_interactions.md
    ├── interview_prep.md
    ├── cv_project_description.md
    ├── final_handover.md
    └── screenshots/                 # .gitkeep only; no screenshots yet
```

The tree lists existing files and folders. Empty folders use `.gitkeep` so Git
preserves them. See [the project plan](docs/project_plan.md) for scope and naming.

## Star schema

The intended model places **FactSales** at the center, with one row per order
line and `SalesLineID` as its key. `OrderID` groups lines belonging to one order.

| Dimension key: one side | FactSales key: many side |
| --- | --- |
| DimProducts[ProductID] | FactSales[ProductID] |
| DimCustomers[CustomerID] | FactSales[CustomerID] |
| DimRegions[RegionID] | FactSales[RegionID] |
| DimChannels[ChannelID] | FactSales[ChannelID] |
| DimDate[Date] | FactSales[OrderDate] |

Configure all five planned relationships as active, **one-to-many**, with
**single-direction filtering from dimension to fact**. Keep DimCustomers[RegionID] as reference
information without another active region-to-customer relationship.

[The model guide](docs/data_model.md) provides a Mermaid diagram and the DAX for
DimDate: one row per day from **2025-01-01 through 2026-12-31**, including days
without sales. It also explains marking the Date table and chronological month
sorting. The table and relationships still need to be created in Desktop.

## Measures and calculation rules

The M scripts define these line calculations for FactSales; Desktop execution is pending:

```text
GrossSales = Quantity × UnitPrice
NetSales   = GrossSales − DiscountAmount
TotalCost  = Quantity × UnitCost
LineProfit = NetSales − TotalCost
```

DiscountAmount is a complete line discount and is deducted once. Monetary
measures sum these prepared columns; unit prices are not multiplied a second time.
Total Profit excludes rent, wages, and other operating expenses; it means profit
after product costs in this project.

| Core measure | Definition |
| --- | --- |
| Gross Revenue | Sum of GrossSales |
| Total Revenue | Sum of NetSales, after discounts |
| Total Cost | Sum of TotalCost |
| Total Profit | Sum of LineProfit |
| Profit Margin % | Total Profit ÷ Total Revenue |
| Total Orders | Distinct count of OrderID |
| Units Sold | Sum of Quantity |
| Average Order Value | Total Revenue ÷ distinct orders |
| Total Discount | Sum of DiscountAmount |

[core_measures.dax](powerbi/measures/core_measures.dax) contains these nine measures.
[time_measures.dax](powerbi/measures/time_measures.dax) adds **Sales Previous Month,
Sales MoM Change, Sales MoM %, Sales Previous Year, Sales YoY %, and Sales YTD**.
The [DAX guide](docs/dax_guide.md) documents formats, blank comparisons, and
partial-period assumptions. All DAX definitions await Desktop evaluation.

## Three dashboard pages

These are complete build specifications; the visuals have not been built or
verified in Desktop. Each page uses the navy/teal [theme](powerbi/theme/retail_theme.json)
and a 16:9 layout described in the [design system](docs/design_system.md).

| Planned page and specification | Main content |
| --- | --- |
| [Executive Overview](docs/page_01_executive_overview.md) | Revenue, profit, margin, orders, and AOV cards; monthly revenue; category/channel sales; region ranking |
| [Product Performance](docs/page_02_product_performance.md) | Units, revenue, and margin cards; Top 10 products; category revenue vs profit; low-margin review table; category trends |
| [Regional & Channel](docs/page_03_regional_channel.md) | Regional revenue, orders, and AOV cards; region/representative-city and channel bars; monthly regional trends; region-by-category matrix |

The [interaction guide](docs/report_interactions.md) specifies synchronized Date,
Category, Region, and Channel slicers, a local Product slicer, native page
navigation, revenue/profit/orders tooltips, and reset bookmarks. Product Performance's
below-28% margin threshold is a demonstration review rule, not a real business target.

## Setup and reproduction

The five CSVs, [data profile](docs/data_profile.md), and
[business insights](docs/business_insights.md) are included, so you can review the
results immediately. To reproduce them, use Python 3 and run these commands from
the repository's root folder; no third-party Python packages are required:

```sh
python3 scripts/generate_data.py
python3 scripts/profile_data.py
python3 scripts/generate_insights.py
```

On Windows, use `py` in place of `python3` if that is your Python launcher.
The generator replaces the five raw CSVs using the fixed seed. Profiling writes
the data profile; insight generation writes the business insights. Those two
scripts preserve source CSVs. No Power BI installation is needed for this analysis.

For the Power BI build, use **Windows Power BI Desktop** and follow
[powerbi_desktop_build_steps.md](docs/powerbi_desktop_build_steps.md). It explains
how to load the five M queries, set the **DataFolder** parameter to the local
[data/raw/](data/raw/) folder, create DimDate and relationships, add measures,
import the theme, build pages, and save/reopen a genuine PBIP using PBIR and TMDL.
The [Power Query guide](docs/power_query_setup.md) provides the detailed import steps.
Changing computers requires updating DataFolder and refreshing in Desktop.

The [final handover](docs/final_handover.md) records the completed review, exact
remaining Desktop actions, screenshot capture, and GitHub publishing steps.
[Interview preparation](docs/interview_prep.md) and the
[CV project entry](docs/cv_project_description.md) describe the work without
claiming a finished or verified Desktop report.

## Calculated business insights

**These figures are from synthetic portfolio data, not real business results.**
They come from the checked-in [generated insights](docs/business_insights.md),
calculated directly from the CSVs with decimal arithmetic and distinct order counts.

| Metric | Calculated result |
| --- | ---: |
| Total Revenue | LKR 12,348,732.29 |
| Total Profit | LKR 3,460,061.52 |
| Profit Margin % | 28.02% |
| Total Orders | 2,453 |
| Average Order Value | LKR 5,034.13 |

- **April 2026** had the highest monthly net revenue: **LKR 962,743.97**.
- **Small Appliances** contributed **48.66%** of net revenue.
- **Western** contributed **29.10%** of net revenue.
- **Physical Store** contributed **62.03%** of net revenue.

The full report contains five factual findings and three recommendations for the
fictional scenario. These calculations do not demonstrate that a dashboard was
executed in Power BI or establish causes such as stockouts or campaign effects.

## Screenshots

| Page | Screenshot placeholder |
| --- | --- |
| Executive Overview | Pending Desktop build and capture |
| Product Performance | Pending Desktop build and capture |
| Regional & Channel | Pending Desktop build and capture |

[docs/screenshots/](docs/screenshots/) currently contains only `.gitkeep`.
Genuine screenshots will be added after the actual pages render in Desktop.
There are no stock images, mock screenshots, or links to nonexistent image files.

## Key learning outcomes

The completed supporting materials demonstrate practice in:

- Reproducible synthetic data generation and a clear fact/dimension data contract.
- Checking missing values, primary keys, foreign keys, and order-line consistency.
- Calculating net revenue, profit, weighted margin, and distinct order metrics correctly.
- Designing reusable M/DAX assets, a star schema, and consistent visual interactions.
- Writing business findings backed by computed values and documenting their limits.

Hands-on Desktop model assembly, visualization, refresh, and interaction testing
are the next practical milestone before presenting this as a completed dashboard.

## Future improvements

- Finish and verify the Desktop report, then add genuine page screenshots.
- Extend the synthetic dataset to complete comparison years.
- Add synthetic sales targets and variance analysis.
- Explore repeat purchases and customer-segment performance.
- Add a product drill-through page and a documented refresh workflow.

This is a self-directed learning and BI internship portfolio project. Its strength
is a traceable path from synthetic source records to calculations, design choices,
and a clearly documented implementation plan.
