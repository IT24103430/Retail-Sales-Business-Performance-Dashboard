# Page 03 — Regional & Channel

Shared slicer synchronization, navigation, tooltip defaults, and Reset filters
follow [report_interactions.md](report_interactions.md). Reserve header space
for the native page navigator and reset button.


**Report page name:** `Regional & Channel`. **Purpose:** Help sales managers
compare customer regions, channel revenue, monthly regional trends, and the
product-category mix within each region.

Use only built-in **Card, Slicer, Clustered bar chart, Line chart with small
multiples, and Matrix** visuals in Power BI Desktop. This design requires no
AppSource visuals, paid visual subscriptions, map services, geocoding, or external
data. Publishing and sharing the finished report are outside this specification.
Reuse the existing [model](data_model.md), [core measures](../powerbi/measures/core_measures.dax),
and [theme/design system](design_system.md); no new measures or columns are needed.

This is a build specification. No page, screenshot, or report has been created
or verified in Desktop for this step.

## Geographic meaning

`FactSales[RegionID]` identifies the customer's assigned region, including online
orders. It joins to `DimRegions[RegionID]`. RegionName is a Sri Lankan province,
while City is one representative city assigned to that region. It is not the
actual transaction city, customer address, store location, or delivery destination.
Do not present a region's entire revenue as independently measured city sales.

| DimRegions[RegionName] | DimRegions[City] |
| --- | --- |
| Western | Colombo |
| Central | Kandy |
| Southern | Galle |
| Northern | Jaffna |
| Eastern | Batticaloa |
| North Western | Kurunegala |
| North Central | Anuradhapura |
| Uva | Badulla |
| Sabaragamuwa | Ratnapura |

Use these existing labels directly; no composite geographic key or mapping file
is needed. A region/city bar hierarchy provides the requested geographic view
without implying location detail the data does not contain.

## Layout

Use a **1600 × 900 px custom 16:9 canvas**, consistent with the other page
specifications. Keep 24 px outer margins, 16 px gutters, white visual backgrounds,
navy headings, and a light-gray canvas. Place three cards above a two-column
visual grid. Allow scrolling in the small multiples and matrix; do not squeeze
nine regions and all matrix columns into unreadably small labels.

```text
+----------------------------------------------------------------------------+
| Retail Sales Analytics | Regional & Channel                                 |
| Synthetic Sri Lankan retail sales | LKR | Cities are representative labels   |
+----------------------------------------------------------------------------+
| S1 Date                    | S2 Category | S3 Region       | S4 Channel      |
+-------------------------+-----------------------+--------------------------+
| K1 Regional revenue     | K2 Regional orders    | K3 Average order value   |
+-------------------------------------+--------------------------------------+
| C1 Revenue by region                | C2 Revenue by channel                |
| Region > representative city bars   | Horizontal bars                      |
+-------------------------------------+--------------------------------------+
| C3 Monthly revenue by region        | M1 Regional revenue by category      |
| Small-multiple line charts          | Region x category matrix             |
+-------------------------------------+--------------------------------------+
| Sales coverage: 01 Jan 2025 - 30 Sep 2026 | Revenue is after discounts         |
+----------------------------------------------------------------------------+
```

## Shared filters and slicers

Set a page-level `DimDate[Date]` filter from **2025-01-01 through 2026-09-30**,
inclusive. All visuals receive this filter; clearing a slicer must not expose
the unused October–December 2026 dates in DimDate. Default to the whole sales
period, all categories, all regions, and all channels, with no chart selection.
Synchronize and show these four slicers on all three pages as defined in the
shared interaction guide; the Product slicer remains local to Product Performance.

| ID / title | Standard slicer and exact field | Behavior / ordering | Business value |
| --- | --- | --- | --- |
| S1 — Date | Between date slicer: `DimDate[Date]`, not its automatic hierarchy | Inclusive range within the page dates; no relative-to-today default | Compare a chosen trading period consistently across regions and channels |
| S2 — Category | Dropdown: `DimProducts[Category]` | All by default; multi-select; Select all and clear enabled; alphabetical; exclude blanks | Inspect where a product category sells well |
| S3 — Region | Dropdown: `DimRegions[RegionName]` | All by default; multi-select; Select all and clear enabled; alphabetical; exclude blanks | Focus on one region or compare a selected group |
| S4 — Channel | Dropdown: `DimChannels[ChannelName]` | All by default; multi-select; Select all and clear enabled; alphabetical; exclude blanks | Compare regional performance within chosen channels |

Each slicer filters all three cards and all four analytical visuals. Set slicer
interactions with the other slicers to **None**, keeping their lists and ranges
stable; their selections still combine on the analytical visuals. Dates and
labels come from dimensions, with single-direction relationships into FactSales.
Do not add region-to-customer relationships or bidirectional filtering.

## KPI cards

Use three separate **Card** visuals, with one existing measure per card. These
titles are display labels only; do not create regional copies of the measures.
Each card receives all shared filters and analytical selections, with no extra
visual filter and no outgoing interaction.

| ID / visible title | Exact value measure | Format | Business question |
| --- | --- | --- | --- |
| K1 — Regional revenue | `[Total Revenue]` | LKR, 2 decimals | How much revenue comes from the selected region or regions? |
| K2 — Regional orders | `[Total Orders]` | Whole number, `#,##0` | How many distinct orders contributed to this regional selection? |
| K3 — Average order value | `[Average Order Value]` | LKR, 2 decimals | How much revenue does each distinct order contribute on average? |

When Region is All, cards show the combined total for all regions, not an
average region. Revenue is after discounts. Orders use distinct OrderID so
multi-item orders count once. AOV is total selected revenue divided by distinct
selected orders, not an average of regional AOVs. With category filtering it
uses selected category revenue per order containing those selected lines.

## C1 — Revenue by region (representative city)

- **Visual / fields:** Clustered horizontal bar chart. Y-axis hierarchy, in
  order: `DimRegions[RegionName]`, `DimRegions[City]`. X-axis: `[Total Revenue]`;
  no legend. Tooltips: `[Total Profit]`, `[Total Orders]`, `[Average Order Value]`.
- **Display:** Expand the hierarchy to show both region and representative city
  labels; turn label concatenation on where needed. Initially show all nine
  regions with sales, not a Top N subset. Each region currently has one city,
  so expanding changes labels without introducing another revenue allocation.
- **Filters / sorting:** Shared filters, RegionName and City not blank, and
  `[Total Revenue]` not blank; revenue descending, highest at the top. Both
  hierarchy levels remain from DimRegions. Region-slicer selections restrict
  the displayed geography normally.
- **Style:** Navy bars, zero baseline, readable labels, LKR axis and tooltips.
  Add the note **City labels represent regions; these are not city-level sales**.
- **Business value:** Identify strong and weak customer regions while retaining
  familiar Sri Lankan city labels for orientation.

## C2 — Revenue by channel

- **Visual / fields:** Clustered horizontal bar chart. Y-axis:
  `DimChannels[ChannelName]`; X-axis: `[Total Revenue]`; no legend.
  Tooltips: `[Total Profit]`, `[Profit Margin %]`, `[Total Orders]`,
  `[Average Order Value]`.
- **Filters / sorting:** Shared filters; ChannelName not blank and
  `[Total Revenue]` not blank. Sort revenue descending. Include all matching
  Physical Store, Online Store, Mobile App, and Telephone Order channels.
- **Style:** Navy bars, zero baseline, full channel names, no market-share
  percentages or unrequested targets. Keep profit teal only when shown as a
  separate series elsewhere; these bars all encode revenue.
- **Business value:** Identify the channels generating revenue within the
  selected geography/category/period, and inspect order value in tooltips.

## C3 — Monthly revenue by region

- **Visual / fields:** Built-in Line chart. X-axis: `DimDate[YearMonth]`;
  Y-axis: `[Total Revenue]`; **Small multiples:** `DimRegions[RegionName]`;
  no legend. Tooltips: `[Total Profit]`, `[Total Orders]`, `[Average Order Value]`.
- **Filters / sorting:** Shared filters and RegionName not blank; no Top N.
  Sort YearMonth ascending using YearMonthSort. Sort the multiple panels by
  RegionName ascending. Keep no-sales month values blank rather than zero.
- **Layout:** Use a **2 × 2 grid**, synchronized axes, and vertical scrolling to
  access all nine regions. A Region slicer selection reduces the panels. Use
  navy lines and small markers, with 11–12 pt region titles; avoid nine overlaid
  lines distinguished only by color. Focus mode can provide a larger view.
- **Interpretation:** All panels use the same revenue scale. A partial date
  selection produces partial first/last months; 2026 is a partial sales year.
  Do not imply that missing months mean zero sales or calculate full-year growth
  from unequal year lengths.
- **Business value:** Compare regional seasonality and changes over time on a
  shared scale while retaining each region's identity. This is a native
  [small-multiples feature](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-small-multiples),
  not a third-party visual.

## M1 — Regional revenue by category

- **Visual / fields:** Built-in **Matrix**. Rows:
  `DimRegions[RegionName]`. Columns: `DimProducts[Category]`. Values:
  `[Total Revenue]` only. Cell grain: one region/category intersection under
  the selected date/channel filters. The matrix provides the detailed revenue
  breakdown without introducing many measure subcolumns.
- **Filters:** Shared filters; RegionName and Category not blank. Keep empty
  intersections blank, not zero. Display all matching regions/categories without
  Top N filtering; enable Show items with no data for row/column labels when
  the selected region/category has no matching sales.
- **Sorting:** Region rows alphabetical ascending, category columns alphabetical
  ascending. Keep this order stable rather than reordering columns by individual
  region values. C1 provides the separate revenue ranking.
- **Totals:** Show each region's total across categories, each category's total
  across regions, and the overall grand total. Revenue is additive; the grand
  total matches K1 under the same filters when no other visual is selected.
  A selection within M1 can filter K1 while the source matrix keeps its context.
- **Formatting:** Full LKR amounts, 2 decimals, Display units None. Use navy text
  and soft-gray `#E3E9EE` data bars within value cells, minimum 0 and automatic
  maximum, with numbers visible. Keep totals bold and unformatted by data bars.
  Preserve frozen row headers, wrap category headers, and permit horizontal or
  vertical scrolling rather than reducing text below 11 pt.
- **Business value:** Find category strengths and gaps within each region and
  distinguish a broad regional sales issue from a product-mix issue. An empty
  cell indicates no matching synthetic sales, not proof of unmet market demand.
  See Microsoft's [matrix guide](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-matrix-visual).

## Titles, formats, and interactions

Use the titles written above. All card and matrix money uses the existing model
format `"LKR" #,##0.00;-"LKR" #,##0.00`; order counts use `#,##0`, and tooltip
margin uses `0.00%`. Charts may scale axes to millions only with an explicit
**Revenue (LKR millions)** axis title; tooltips retain full LKR values. Blank
cards remain blank or display an em dash, without adding zero-filling measures.

Use **Format → Edit interactions** to configure these behaviors:

| Source | Three KPI cards | Other charts / matrix | Four slicers |
| --- | --- | --- | --- |
| Any slicer | Filter | Filter all four | None for other slicers |
| C1 region/city bar | Filter | Filter C2, C3, M1 | None |
| C2 channel bar | Filter | Filter C1, C3, M1 | None |
| C3 region/month point | Filter | Filter C1, C2, M1 | None |
| M1 region/category cell | Filter | Filter C1, C2, C3 | None |
| KPI cards | None | None | None |

Choose **Filter**, not Highlight. A matrix value-cell selection passes both its
region and category; a region row label passes the region. A trend point passes
its month and region. Clear the visual selection to restore the slicer-defined
context. Slicer controls stay unchanged when analytical visuals are selected.
Keep drill actions local to C1 rather than making hierarchy expansion filter
the whole page; use slicers to build explicit combined selections. The settings
follow Microsoft's [visual interaction guide](https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions).

## Manual build and quick review

Create the page in Desktop after loading the existing queries, model, measures,
and theme. Configure the page date filter, four slicers, three cards, two bar
charts, small-multiple line chart, and matrix. Use short alt text and tab order
following the reading order; keep scrolling controls visible.

For a quick review, select one region and one channel and confirm all visuals
use the same subset. With no analytical selection, the matrix grand total
should match Regional revenue, and monthly values for a region should sum to
its selected-period revenue. Cards must keep distinct order counts; do not add
category-level order counts or average separate AOV values to recreate totals.

Build and verify these behaviors manually in Desktop; they have not been tested
here. Capture `docs/screenshots/regional_channel.png` only after the actual page
is implemented. No finished screenshot or report artifact is supplied by this step.
