# Page 01 — Executive Overview

**Purpose:** Help a retail manager understand revenue, profit, order value, and
the main sources of sales for the selected period. **Report page name:**
`Executive Overview`. This is a build specification, not a completed dashboard
or screenshot. Power BI Desktop implementation and verification remain pending.

Use the existing [star schema](data_model.md), [core measures](../powerbi/measures/core_measures.dax),
and [theme](../powerbi/theme/retail_theme.json). Field names below are exact;
bracket-only names such as `[Total Revenue]` refer to existing measures.

## Layout and wireframe

Use a **1600 × 900 px custom canvas (16:9)** for this page's five cards and four
charts. Set Format page → Canvas settings → Type to Custom and enter those
dimensions. This is the roomier 16:9 option within the [design system](design_system.md).
Keep 24 px outer margins, 16 px gutters, white visual surfaces, and a light-gray
canvas. Use the five cards as the only KPI row; do not add gauges or comparison
tiles. Chart panels use two equal columns, about 768 px each.

```text
+--------------------------------------------------------------------------------+
| Retail Sales Analytics | Executive Overview                                     |
| Synthetic Sri Lankan retail sales | All money in LKR                            |
+--------------------------------------------------------------------------------+
| S1 Date: from / to              | S2 Category | S3 Region    | S4 Channel        |
+----------------+----------------+----------------+--------------+----------------+
| K1             | K2             | K3             | K4           | K5             |
| Total Revenue  | Total Profit   | Profit Margin %| Total Orders | Avg Order Value|
+----------------+----------------+----------------+--------------+----------------+
| C1 Monthly revenue                    | C2 Revenue by product category          |
| Line chart                            | Horizontal bars                         |
|                                       |                                         |
+---------------------------------------+-----------------------------------------+
| C3 Revenue by sales channel            | C4 Regions ranked by revenue            |
| Horizontal bars                       | Horizontal bars                         |
|                                       |                                         |
+---------------------------------------+-----------------------------------------+
| Revenue is after discounts | Sales available: 01 Jan 2025 - 30 Sep 2026            |
+--------------------------------------------------------------------------------+
```

Wireframe labels are abbreviated for space; use the full titles specified below.
Allow about 64 px for the header, 72 px for slicers, 112 px for cards, and
256 px for each chart row. Use equal card widths around 298 px. KPI values can
use **24 pt** for this five-card row, with 11–12 pt labels and full LKR values;
keep numbers on one line and adjust within the card before reducing readability.

## Shared page filters and definitions

- Add a **page-level filter** on `DimDate[Date]`: on or after **2025-01-01** and
  on or before **2026-09-30**. This excludes the date table's unused final quarter
  of 2026. Keep this filter when clearing slicers.
- Default state: the entire available sales period, all categories, all regions,
  and all channels. Do not add report-level filters or Top N filters for this page.
- Every card and chart receives the page filter and all four slicers. Additional
  visual filters are stated below. Use dimension labels, not fact IDs, on axes.
- Revenue always means `[Total Revenue]` after discounts; profit means
  `[Total Profit]`. Do not sum unit prices, subtract discounts again, or use
  line count as order count. Margin and AOV are ratios recalculated in context.
- A partial date selection produces partial first/last months; those are not
  full-month comparisons. The default 2026 period is a partial sales year.

## Slicers

| ID / title | Type and exact field | Default / filters | Intended question |
| --- | --- | --- | --- |
| S1 — Date | Date range slicer, Between; `DimDate[Date]`, not Date hierarchy | Inclusive 2025-01-01 to 2026-09-30; constrained by page filter; no relative-to-today selection | Which period should the overview cover? |
| S2 — Category | Dropdown; `DimProducts[Category]` | All; multi-select and Select all enabled; exclude blank labels | Which product categories should be included? |
| S3 — Region | Dropdown; `DimRegions[RegionName]` | All; multi-select and Select all enabled; exclude blank labels | Which customer sales regions should be included? |
| S4 — Channel | Dropdown; `DimChannels[ChannelName]` | All; multi-select and Select all enabled; exclude blank labels | Which sales channels should be included? |

Sort dropdown labels alphabetically and keep the clear-selection icon available.
Each slicer filters all five cards and all four charts. Set its interaction with
the other slicers to **None**, so their available lists/ranges stay stable rather
than cascading. Their selections still combine when filtering analytical visuals.
Keep slicers local to this page until later page specifications define syncing.

## KPI cards

Create five separate **Card** visuals with one measure each. Use the exact
measure name as the visible title/label once; hide any duplicate label. No trend
axis, reference target, visual-level filter, or extra comparison measure is needed.
Each card receives all slicers and chart selections and does not filter other
visuals. Blank results remain blank or display an em dash, never an invented zero.

| ID / title | Exact value measure | Format | Intended question |
| --- | --- | --- | --- |
| K1 — Total Revenue | `[Total Revenue]` | LKR, 2 decimals | How much sales revenue remains after discounts? |
| K2 — Total Profit | `[Total Profit]` | LKR, 2 decimals | How much remains after product costs? |
| K3 — Profit Margin % | `[Profit Margin %]` | `0.00%` | What share of revenue is profit? |
| K4 — Total Orders | `[Total Orders]` | `#,##0` | How many distinct orders contributed to sales? |
| K5 — Average Order Value | `[Average Order Value]` | LKR, 2 decimals | What is the average revenue per distinct order? |

Use navy values with restrained teal accents. Set currency card Display units
to **None** and use `"LKR" #,##0.00;-"LKR" #,##0.00` from the
[DAX guide](dax_guide.md). Total Orders is a distinct count of OrderID even when
an order contains multiple products. Category selections make AOV the selected
category revenue per order containing that category, not the whole basket value.

## Charts

All chart values use existing measures. Tooltips show the category/date label
and the listed measures with full LKR amounts, whole order counts, and percentage
formats. Tooltips are informational; do not create additional measures or pages.

| ID / title | Chart type and exact fields | Filters and sorting | Intended question |
| --- | --- | --- | --- |
| C1 — Monthly revenue | Line chart; X-axis `DimDate[YearMonth]`; Y-axis `[Total Revenue]`; no legend; tooltips `[Total Profit]`, `[Total Orders]`, `[Sales MoM %]` | Shared filters only; categorical axis sorted YearMonth ascending using YearMonthSort; enable Show items with no data within the selected date range; keep missing values as gaps | How does net revenue change from month to month? |
| C2 — Revenue by product category | Clustered horizontal bar chart; Y-axis `DimProducts[Category]`; X-axis `[Total Revenue]`; no legend; tooltips `[Total Profit]`, `[Profit Margin %]`, `[Total Orders]` | Shared filters; Category is not blank and `[Total Revenue]` is not blank; sort revenue descending; include all six categories with matching sales, not Top N | Which product categories contribute the most revenue? |
| C3 — Revenue by sales channel | Clustered horizontal bar chart; Y-axis `DimChannels[ChannelName]`; X-axis `[Total Revenue]`; no legend; tooltips `[Total Profit]`, `[Total Orders]`, `[Average Order Value]` | Shared filters; ChannelName is not blank and `[Total Revenue]` is not blank; sort revenue descending; include all four channels with matching sales | Which channels contribute the most revenue? |
| C4 — Regions ranked by revenue | Clustered horizontal bar chart; Y-axis `DimRegions[RegionName]`; X-axis `[Total Revenue]`; no legend; tooltips `[Total Profit]`, `[Profit Margin %]`, `[Total Orders]` | Shared filters; RegionName is not blank and `[Total Revenue]` is not blank; sort revenue descending; include all nine regions with matching sales; no rank measure required | Which customer regions lead or need attention? |

For C1, use a navy line with markers and a limited number of readable month ticks.
The `[Sales MoM %]` tooltip comes from
[time_measures.dax](../powerbi/measures/time_measures.dax); keep unavailable
comparisons blank. Use complete months when interpreting it as monthly growth.

For C2–C4, use navy bars and a zero baseline. Keep category/region/channel labels
visible and show revenue data labels only where they fit. Channel uses a bar
chart rather than a donut so values are easy to compare without introducing a
percentage-of-total measure. These charts show revenue amounts, not market share.
Region means the customer's assigned region, not a branch or delivery location.

Axis titles must state **Revenue (LKR)**, or **Revenue (LKR millions)** if axis
Display units are Millions. Tooltips retain full precision in either case.

## Interaction settings

Configure **Format → Edit interactions** for each source visual. Use **Filter**
for analytical targets, rather than Highlight, so cards and charts describe the
same selected sales rows. Use **None** for slicer targets and decorative text.

| Source selection | Five KPI cards | Other charts | Four slicers |
| --- | --- | --- | --- |
| S1, S2, S3, or S4 | Filter | Filter all four | None for other slicers |
| C1 month point | Filter | Filter C2, C3, C4 | None |
| C2 category bar | Filter | Filter C1, C3, C4 | None |
| C3 channel bar | Filter | Filter C1, C2, C4 | None |
| C4 region bar | Filter | Filter C1, C2, C3 | None |
| K1–K5 cards | None | None | None |

One click focuses a month/category/channel/region; clearing that chart selection
restores the slicer-defined context. Slicer selections remain visibly unchanged
when a chart point is selected. Use slicers to combine several filters reliably.
No drill-through or cross-page interaction is required for this page.
Microsoft documents [visual interaction settings](https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions)
and [slicer behavior](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers).

## Manual build and quick review

After the queries, model, measures, and theme are applied in Desktop, create the
page, set its date filter, place the four slicers and nine analytical visuals,
then configure the interactions above. Set tab order to header, slicers, KPI
cards, then charts from left to right; provide short alt text for each chart.

For an initial source-based check with slicers at default and no chart selected,
expect Revenue **LKR 12,348,732.29**, Profit **LKR 3,460,061.52**, Margin **28.02%**,
Orders **2,453**, and AOV **LKR 5,034.13**, matching the [data profile](data_profile.md).
Category order counts can overlap, so do not sum them to reproduce Total Orders.
These are expected values, not evidence of Desktop execution.

Leave `docs/screenshots/executive_overview.png` absent until the actual page is
built and captured in Desktop. No screenshot or completed report is created by
this specification.
