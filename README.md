# Retail Sales Analytics

A **Business Intelligence portfolio project** focused on transforming retail transaction data into clear, interactive dashboards that support data-driven decisions.

This project is designed to demonstrate practical skills in **data preparation, data modeling, DAX, data visualization, and business analysis** for a Business Intelligence internship.

> **Project status:** Initial folder structure and project plan created. Data generation, transformation, and dashboard development are pending. No Power BI report has been created or verified.

The project uses synthetic Sri Lankan retail data. All monetary values use Sri Lankan rupees (LKR). See [the project plan](docs/project_plan.md) for scope and naming conventions.

## Project Overview

Retail businesses generate sales data every day, but raw spreadsheets make it difficult to identify trends, profitable products, and regional performance. This project uses **Microsoft Power BI** to turn retail sales records into actionable insights.

The dashboard is intended to answer questions such as:

- How much revenue and profit did the business generate?
- Are sales increasing or decreasing over time?
- Which products and categories perform best?
- Which regions contribute the most revenue?
- What is the average order value?

## Project Objectives

1. Prepare and clean a retail sales dataset using Power Query.
2. Create a reliable data model using fact and dimension tables.
3. Build business KPIs with DAX measures.
4. Design interactive dashboards with filters and visualizations.
5. Summarize key findings and business recommendations.

## Tools and Technologies

| Tool | Purpose |
| --- | --- |
| **Power BI Desktop** | Build the data model, measures, and dashboards |
| **Power Query** | Clean and transform data |
| **DAX** | Calculate KPIs and time-based metrics |
| **CSV** | Store raw and processed data |
| **Python** | Generate and prepare reproducible synthetic sales data |
| **Git & GitHub** | Version control and portfolio presentation |

## Dataset

The proposed dataset contains **5,000 synthetic retail sales records** in a Sri Lankan retail context. Python will generate the data; no real customer information will be used.

**Planned raw file:** `data/raw/retail_sales.csv`  
**Planned processed file:** `data/processed/retail_sales_clean.csv`

| Column | Description |
| --- | --- |
| `OrderID` | Unique order identifier (may repeat across order line items) |
| `OrderDate` | Date of the transaction |
| `CustomerID` | Anonymous customer identifier |
| `ProductID` | Unique product identifier |
| `ProductName` | Name of the item sold |
| `Category` | Product category |
| `Region` | Sales region |
| `Quantity` | Number of units sold |
| `UnitPrice` | Selling price per unit |
| `UnitCost` | Cost per unit |

**Data note:** Revenue and profit should be calculated from the numeric columns rather than assumed to exist in the source file. Unit prices, unit costs, revenue, and profit use LKR throughout the report.

## Data Preparation

Planned cleaning and transformation steps in **Power Query**:

- Correct column data types, especially dates and numeric values.
- Check for missing order IDs, dates, product IDs, and prices.
- Remove exact duplicate transaction rows when appropriate.
- Validate that quantities and prices are sensible.
- Standardize category and region values.
- Prepare fact and dimension tables for analysis.

## Data Model

A **star schema** is recommended:

- **FactSales:** Order line items, dates, IDs, quantities, unit prices, and unit costs.
- **DimDate:** Calendar dates, month, quarter, and year.
- **DimProduct:** Product details and categories.
- **DimCustomer:** Anonymous customer identifiers.
- **DimRegion:** Region identifiers and names.

Link each dimension to `FactSales` with an appropriate **one-to-many relationship**. Use a dedicated, continuous date table for time intelligence.

> If the data is initially stored in one CSV file, create the dimension tables from distinct values, add surrogate IDs where needed, and confirm that each dimension key is unique.

## Key Performance Indicators (KPIs)

| KPI | Definition |
| --- | --- |
| Total Revenue | Sum of `Quantity × UnitPrice` |
| Total Cost | Sum of `Quantity × UnitCost` |
| Total Profit | Total Revenue − Total Cost |
| Profit Margin | Total Profit ÷ Total Revenue |
| Total Orders | Distinct count of order IDs |
| Average Order Value | Total Revenue ÷ Total Orders |
| Monthly Revenue Growth | Percentage change from the previous month |

### Example DAX Measures

The following examples assume the fact table is named `FactSales` and the calendar table is `DimDate`.

```dax
Total Revenue =
SUMX(
    FactSales,
    FactSales[Quantity] * FactSales[UnitPrice]
)

Total Cost =
SUMX(
    FactSales,
    FactSales[Quantity] * FactSales[UnitCost]
)

Total Profit =
[Total Revenue] - [Total Cost]

Profit Margin % =
DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders =
DISTINCTCOUNT(FactSales[OrderID])

Average Order Value =
DIVIDE([Total Revenue], [Total Orders], 0)

Previous Month Revenue =
CALCULATE(
    [Total Revenue],
    DATEADD(DimDate[Date], -1, MONTH)
)

Monthly Revenue Growth % =
DIVIDE(
    [Total Revenue] - [Previous Month Revenue],
    [Previous Month Revenue]
)
```

**Important:** Format percentage measures as percentages in Power BI. For meaningful month-over-month comparisons, use a proper date table and display the measures in a monthly date context.

## Dashboard Pages

### 1. Executive Overview

A high-level view of business performance:

- KPI cards: Revenue, Profit, Orders, and Average Order Value
- Monthly revenue trend line
- Revenue by category
- Top-performing products
- Date, region, and category slicers

### 2. Product Performance

Explore which products drive sales:

- Top 10 products by revenue
- Revenue and profit by category
- Quantity sold by product
- Product profitability comparisons

### 3. Regional Sales Analysis

Compare performance across regions:

- Revenue and profit by region
- Regional share of total revenue
- Monthly trends by region
- Interactive filters for categories and dates

## Dashboard Screenshots

Add actual screenshots after building the report in Power BI Desktop:

| Page | Screenshot to add |
| --- | --- |
| Executive Overview | `docs/screenshots/executive_overview.png` |
| Product Performance | `docs/screenshots/product_performance.png` |
| Regional Sales Analysis | `docs/screenshots/regional_sales_analysis.png` |

> Screenshots are not included yet. Do not use stock dashboard images as evidence of completed project work.

## Repository Structure

```text
Retail-Sales-Business-Performance-Dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
├── powerbi/
│   ├── queries/
│   ├── measures/
│   └── theme/
└── docs/
    ├── project_plan.md
    └── screenshots/
```

Empty folders contain `.gitkeep` files so Git preserves the structure. Add the actual Power BI report files only when they have been created in Desktop.

## Getting Started

From the project root, create a Python environment and install dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

Data generation scripts, CSV files, Power Query queries, DAX files, and a theme will be added in later steps. See [the project plan](docs/project_plan.md) for their intended locations.

Building, refreshing, and validating the report in Power BI Desktop are pending. Desktop requires a Windows environment; no report has been opened or verified for this setup step.

## Validation Checklist

Before presenting this project to recruiters, verify that:

- [ ] The dataset loads without errors.
- [ ] The data types and relationships are correct.
- [ ] Revenue = sum of quantity × unit price.
- [ ] Profit = revenue − cost.
- [ ] Order counts use distinct order IDs.
- [ ] Date, product, and region slicers filter the expected visuals.
- [ ] Monthly calculations are accurate for the selected date range.
- [ ] All dashboard pages are readable and professionally formatted.
- [ ] Actual dashboard screenshots are added to `docs/screenshots/`.
- [ ] Key business findings are recorded in `docs/business_insights.md`.

## Business Insights

After completing the dashboard, replace these prompts with **findings backed by your report**:

1. **Sales trend:** Which month had the highest revenue, and what was the change from the previous month?
2. **Product performance:** Which category contributed most to revenue and profit?
3. **Regional performance:** Which region performed best, and where might improvement be possible?

Add a short recommendation alongside each finding. Because the dataset is synthetic, present these findings as a **demonstration of analytical skills**, not as real-world company results.

## Possible Future Improvements

- Introduce sales targets and variance analysis.
- Add year-over-year comparisons.
- Add customer segmentation and repeat-purchase analysis.
- Automate dataset refresh when using a supported published environment.
- Include a separate drill-through page for product details.

## About This Project

This is a self-directed portfolio project created to practice the end-to-end **Business Intelligence workflow**: importing data, cleaning it, designing a model, creating measures, developing dashboards, and interpreting results.

**Author:** Add your name and GitHub profile URL here.

**Note:** If you used Codex or another AI tool, be prepared to explain the data model, DAX measures, dashboard design decisions, and business insights in your own words during interviews.
