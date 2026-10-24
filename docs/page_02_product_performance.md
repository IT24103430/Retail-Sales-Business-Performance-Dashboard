# Page 02 — Product Performance

**Purpose:** Help a product manager identify revenue leaders, compare category
profitability, and review products with weaker margins. **Report page name:**
`Product Performance`. This is a specification; Desktop implementation and
verification are pending. No dashboard screenshot is created.

Use the existing [model](data_model.md), [core measures](../powerbi/measures/core_measures.dax),
and [design system](design_system.md). All measure names below already exist.
**No additional DAX measures, calculated columns, or datasets are required.**

## Layout and defaults

Use a **1600 × 900 px custom canvas (16:9)**, matching the Executive Overview,
with 24 px margins, 16 px gutters, white surfaces, and a light-gray background.
Place the three KPI cards above a two-column chart grid. Give the Top 10 and
low-margin table panels extra height if product labels require it; allow table
scrolling instead of shrinking text. Keep chart titles at 14 pt, labels at
11–12 pt, and KPI values around 28 pt.

```text
+----------------------------------------------------------------------------+
| Retail Sales Analytics | Product Performance                                |
| Synthetic data | LKR | Sales coverage: 01 Jan 2025 - 30 Sep 2026               |
+----------------------------------------------------------------------------+
| S1 Category                         | S2 Product (search enabled)            |
+------------------------+--------------------------+------------------------+
| K1 Units Sold          | K2 Total Revenue         | K3 Profit Margin %     |
+-------------------------------------+--------------------------------------+
| C1 Top 10 products by revenue        | C2 Revenue vs profit by category     |
| Horizontal bars                     | Clustered horizontal bars            |
+-------------------------------------+--------------------------------------+
| T1 Low-margin products              | C3 Monthly revenue by category       |
| Product-level table                 | Line chart                           |
+-------------------------------------+--------------------------------------+
| Low-margin review threshold: below 28% | Revenue is after discounts           |
+----------------------------------------------------------------------------+
```

- Apply a **page-level** `DimDate[Date]` filter from **2025-01-01 through
  2026-09-30**, inclusive. This is the full available sales period; 2026 is partial.
  The fixed coverage subtitle describes available data, not today's date.
- Default both slicers to All, with no chart/table selection. Keep these slicers
  local to this page; do not automatically inherit Page 01 selections.
- All analytical visuals receive the page filter and both slicers. Keep Top N
  and low-margin filters **local to their own visuals**, never at page level.
- Revenue is `[Total Revenue]` after discounts. Profit is `[Total Profit]`.
  Margin is `[Profit Margin %]`, recalculated as profit divided by revenue,
  rather than an average of product or line percentages.

## Slicers

| ID / title | Type and exact field | Settings and sorting | Business question |
| --- | --- | --- | --- |
| S1 — Category | Dropdown: `DimProducts[Category]` | All by default; multi-select and Select all enabled; exclude blanks; alphabetical | Which categories should be compared? |
| S2 — Product | Searchable dropdown: `DimProducts[ProductName]` | All by default; multi-select and Select all enabled; exclude blanks; alphabetical | Which products need a closer look? |

Both slicers filter every KPI, chart, and table. Set Category → Product to
**Filter**, so the product list follows the selected category; set Product →
Category to **None**. These fields are in the same dimension and need no new
relationship. If an existing product selection conflicts with a new category,
clear Product and select again; an empty intersection correctly gives no sales.

## KPI cards

Create separate **Card** visuals with one measure each and no visual-level
filter beyond shared context. Use the exact measure name as the visible label,
once per card. Cards receive filters but have no outgoing interactions.

| ID / title | Exact value | Format | Business question |
| --- | --- | --- | --- |
| K1 — Units Sold | `[Units Sold]` | Whole number: `#,##0` | How many sale units were sold for the selection? |
| K2 — Total Revenue | `[Total Revenue]` | LKR, thousands separator, 2 decimals | How much revenue did the selection generate after discounts? |
| K3 — Profit Margin % | `[Profit Margin %]` | Percentage: `0.00%` | How much of the selection's revenue remains after product costs? |

Keep blank results blank or show an em dash. Use Display units **None** for
cards and tables, and the LKR format `"LKR" #,##0.00;-"LKR" #,##0.00` from the
[DAX guide](dax_guide.md). Units are sale units: one packaged product is one unit.

## Charts and table

### C1 — Top 10 products by revenue

- **Type / fields:** Clustered horizontal bar chart. Y-axis:
  `DimProducts[ProductName]`; X-axis: `[Total Revenue]`; no legend.
  Tooltips: `DimProducts[ProductID]`, `DimProducts[Category]`, `[Units Sold]`,
  `[Total Profit]`, and `[Profit Margin %]`.
- **Filters:** In Filters on this visual, set ProductName to **Top N → Top 10**,
  put `[Total Revenue]` in **By value**, and select **Apply filter**. Also require
  `[Total Revenue] > 0`. Product names are distinct in the current catalogue;
  the product key remains ProductID.
- **Sort / style:** Revenue descending, largest at the top; navy bars, zero
  baseline, readable product labels. Use full LKR tooltips; an axis scaled to
  millions must say **Revenue (LKR millions)**. The title remains
  **Top 10 products by revenue** even when slicers leave fewer products.
- **Scope:** Recalculate the leaders within the selected category/products and
  period. Other visuals retain all selected products, including those outside
  the Top 10. Native Top N can retain ties at the cutoff; do not add an artificial
  ranking measure just to discard tied products.
- **Question:** Which products drive the most revenue within the selection?

### C2 — Revenue vs profit by category

- **Type / fields:** Clustered horizontal bar chart. Y-axis:
  `DimProducts[Category]`; X-axis values: `[Total Revenue]` and `[Total Profit]`.
  Legend: the two measure series. Tooltips: `[Units Sold]` and `[Profit Margin %]`.
- **Filters / sorting:** Shared context; Category is not blank and
  `[Total Revenue]` is not blank. Include all matching categories, sorted by
  `[Total Revenue]` descending. Do not apply C1's Top 10 filter here.
- **Style:** Revenue navy `#17324D`, profit teal `#007A75`; one shared LKR scale
  with a zero baseline. Keep measure names in the legend and allow space for
  negative profit if it occurs. Do not use a second axis or stack profit on top
  of revenue because profit is already part of revenue.
- **Question:** Which categories produce strong sales and how much profit do
  those sales generate?

### T1 — Low-margin products (below 28%)

- **Type / fields:** Table, one row per product. Add columns in this order:
  `DimProducts[ProductID]`, `DimProducts[ProductName]`, `DimProducts[Category]`,
  `[Units Sold]`, `[Total Revenue]`, `[Total Profit]`, `[Profit Margin %]`.
- **Filters:** Shared context plus `[Total Revenue] > 0`, `[Profit Margin %]`
  is not blank, and `[Profit Margin %] < 0.28`. Use **Number 0.28**, not 28.
  This is an illustrative review threshold for this synthetic portfolio, not a
  real company target or an external retail benchmark. Display that assumption
  in the page footer and table title.
- **Sorting:** Margin ascending, then Revenue descending for equal margins,
  then ProductName ascending for equal values; use multi-column table sorting.
  Include all qualifying products and allow vertical scrolling. Turn totals
  off: this is a review list, while the cards summarize the full selection.
- **Interpretation:** Test the margin of each product's aggregated sales under
  the current filters, not the margin of individual transaction lines. C1's Top
  10 filter does not constrain this list. If nothing qualifies, keep the table
  empty; do not raise the threshold or populate placeholder products.
- **Question:** Which products have the weakest margins, and is their revenue
  large enough to warrant a pricing, cost, or discount review?

### C3 — Monthly revenue by category

- **Type / fields:** Line chart. X-axis: `DimDate[YearMonth]`; Y-axis:
  `[Total Revenue]`; legend: `DimProducts[Category]`. Tooltips:
  `[Total Profit]`, `[Profit Margin %]`, and `[Units Sold]` for that month/category.
- **Filters / sorting:** Shared context; exclude blank Category. Use a categorical
  month axis, sorted YearMonth ascending using YearMonthSort. Keep available
  months within the page date range and preserve missing sales as gaps, not zero.
  Do not apply Top 10 or the low-margin threshold to this visual.
- **Style:** Use the theme's six data colors in a fixed category order across
  pages: Beverages, Groceries, Household, Personal Care, Small Appliances,
  Stationery. Assign each category its corresponding palette color explicitly
  so filtering does not shift the assignments. Keep the legend visible; use
  markers/line styles as well as color.
  Slicers can reduce the number of lines for closer inspection. Axis title:
  **Revenue (LKR)**, or explicitly **Revenue (LKR millions)** if scaled.
- **Question:** Which categories are growing, declining, or showing seasonal
  revenue changes across the available months?

## Useful conditional formatting

Use built-in formatting based on the existing numeric measures; no color or
status measure is needed. Keep numbers visible and avoid whole-row heatmaps.

| Visual / field | Rule | Purpose |
| --- | --- | --- |
| T1 / `[Profit Margin %]` | Background Rules: below `0.25`, navy `#17324D` with white text; from `0.25` inclusive to `0.28` exclusive, soft gray `#E3E9EE` with navy text | Distinguish a more urgent review band within the below-28% list |
| T1 / `[Total Revenue]` | Soft-gray `#E3E9EE` data bars with navy text, minimum 0, automatic maximum, Show bar only off | Show the revenue exposure while retaining readable exact LKR values |
| T1 / `[Total Profit]` | Add a warning icon for values below 0; keep the signed numeric value | Flag losses without relying on color alone |

The 25% urgency band is also a demonstration rule, not a business target. For
margin Rules choose **Number** as the threshold type: `0.25` means 25%, whereas
Power BI's **Percent** option means a percentage of the observed value range.
Configure both background and font rules when using a navy cell so text remains
readable. Leave blank cells unformatted. The synthetic defaults may show no
products in the below-25% band; that does not indicate an error. See Microsoft's
[conditional table formatting guide](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-table-formatting).

## Interactions and manual implementation

Using **Format → Edit interactions**, let each slicer filter all analytical
visuals. Category also filters Product as described above. For chart/table
selections, use **Filter**, not Highlight, on the three cards and the other
charts/table; set interactions to **None** on both slicers. Clicking a category,
product bar, month/category point, or table row then focuses the selected sales
without changing slicer controls. Clearing that selection restores their context.

Product selections in C1 or T1 identify the selected products; T1's margin rule
and C1's Top N rule are local display filters, not new page-wide product cohorts.
To analyze a group consistently, select its products/categories with the slicers.
Use the [visual interaction guide](https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions)
when configuring these settings. No drill-through, new measures, or bookmarks
are required for this page.

Build the page manually after the existing model, measures, and theme are loaded.
As a quick review, confirm that Top 10 affects only C1, the margin threshold
affects only T1, and cards still describe the full slicer selection when nothing
is clicked. Check that changing Category/Product updates both revenue and margin,
and that the month axis runs chronologically across both years. Desktop checks
remain pending. Capture `docs/screenshots/product_performance.png` only after the
actual page is built; no finished screenshot is supplied here.
