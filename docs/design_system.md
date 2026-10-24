# Retail Sales Analytics — Design System

Use [retail_theme.json](../powerbi/theme/retail_theme.json) for the report's
shared colors, fonts, white visual backgrounds, and light-gray canvas. The aim
is a clear business report that a manager can scan quickly. All displayed data
is synthetic and all money is in Sri Lankan rupees (LKR).

## Page and layout

- Use **16:9**, normally **1280 × 720 px**, on all three planned report pages.
  Select an empty canvas, open **Format page → Canvas settings**, and choose
  **Type → 16:9**. Keep wallpaper plain and the canvas light gray.
- Leave **24 px outer margins**, **16 px between visuals**, and **16 px inside
  cards or visual containers**. Use an 8 px spacing unit for smaller adjustments.
- Use the same reading order on each page: page title and short subtitle, a
  compact slicer row, key figures, then the main charts.
- Keep Date, Region, and Category slicers in consistent positions. Use clear
  labels and dropdowns where lists are long; show the selected date period.
- Executive Overview should use one row of four KPIs and two main chart columns.
  On a 1280 px canvas, four cards can be **296 px wide** each; two chart columns
  can be **608 px wide** each, with the margins and gutters above.
- Use about **4–6 analytical visuals per page**, including KPI cards, plus the
  slicers. Product and regional detail pages can use one wide ranking chart and
  one supporting chart/table instead of adding more tiles.
- Align edges and use equal heights within rows. Avoid overlapping visuals,
  decorative icons, large logos, heavy shadows, and unnecessary borders.

## Typography

Use **Segoe UI** for ordinary text and **Segoe UI Semibold** for headings and key
numbers. Use sentence case, short titles, and consistent measure labels.
Typography sizes below are in points; layout spacing above is in canvas pixels.

| Element | Size | Color / weight |
| --- | --- | --- |
| Page title | 24–28 pt | Navy, Semibold |
| Page subtitle / selected period | 11–12 pt | Slate, regular |
| Chart title | 14 pt | Navy, Semibold |
| Slicer / section heading | 12 pt | Navy, Semibold |
| Axis, legend, table, and data labels | 11–12 pt | Slate, regular |
| KPI value | 28 pt | Navy, Semibold |
| KPI label / comparison note | 11–12 pt | Slate, regular |

The theme supplies shared text defaults. Set page-title text boxes, individual
KPI labels, and any visual-specific sizes manually to follow this table.
Keep labels readable at Fit to page; reduce content before shrinking text.

## Color palette and chart rules

| Role | Hex | Use |
| --- | --- | --- |
| Navy | `#17324D` | Primary text, revenue series, important headings |
| Teal | `#007A75` | Profit series, selected highlights, key accents |
| White | `#FFFFFF` | Chart and KPI surfaces |
| Light gray | `#F3F5F7` | Page canvas |
| Slate | `#52616B` | Secondary text, labels, subtitles |
| Soft gray | `#E3E9EE` | Subtle gridlines and decorative separators |

The ordered data palette is **navy `#17324D`, teal `#007A75`, slate-blue `#536878`,
blue `#326A8C`, muted teal `#3E7974`, gray `#6B7280`**. Use the first two for
most charts. For category comparisons, use one navy bar color and a teal
highlight; reserve the additional colors for charts that need multiple series.

- Use navy for Total Revenue and teal for Total Profit wherever they appear.
  Set series colors manually when necessary: the theme assigns colors by series
  order, not by measure or category name. Keep category assignments consistent
  across pages if categories use separate colors.
- Prefer bars for product/region rankings and lines for monthly trends. Use
  horizontal bars for long product labels, and limit rankings to a readable top 10.
- Use a zero baseline for bar charts, light horizontal gridlines where useful,
  and no chart borders. Avoid 3D charts and large collections of pie slices.
- Keep legends short and add labels, markers, or line styles when series are
  close in color. Do not rely on color alone for categories or performance signs.
- Use navy/slate text on white or light gray; use white text on navy or teal
  when a filled label is necessary. Never use light gray for readable body text.
  Target at least **4.5:1** text/background contrast and **3:1** for essential
  chart marks against their surface. Soft gray separators are decorative only.
- Add concise alt text describing the purpose of each chart and set the keyboard
  tab order to follow the page's reading order. Color checks alone do not verify
  the accessibility of a completed report. See Microsoft's
  [accessibility guidance](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports).

## KPI cards

Use white cards, consistent height around **104–112 px**, 16 px internal padding,
and square or lightly rounded corners (up to 4 px). Keep shadows off. White
surfaces against the light-gray canvas provide enough grouping without outlines.

The Executive Overview uses **Total Revenue**, **Total Profit**, **Total Orders**,
and **Average Order Value**. Place each measure's label above or below its navy
value consistently. Use a small optional comparison note such as
`MoM +4.20%` only when the comparison is defined; display an em dash for a blank
comparison. Keep positive/negative signs visible and explain the comparison
period. Do not turn missing periods into zero growth or introduce a growth target
that does not exist in the data.

## Currency and numbers

Use the formats from [the DAX guide](dax_guide.md). Apply these as model-level
formats so measures remain numeric:

| Value | Format | Example |
| --- | --- | --- |
| LKR money | `"LKR" #,##0.00;-"LKR" #,##0.00` | LKR 1,234.50 |
| Orders / units | `#,##0` | 2,453 |
| Margin / growth | `0.00%` | 28.02% |

Use **Display units → None** for KPI values and tables to show the full LKR
amount. A chart axis may use millions to save space if its title explicitly
states **Revenue (LKR millions)**; keep tooltips at full LKR precision. Preserve
negative signs. Show a blank comparison as blank or an em dash rather than
claiming it is zero. Do not use DAX FORMAT to turn numeric measures into text.

## Import and manual finishing

1. In Power BI Desktop, select **Design → Import theme** and choose
   `powerbi/theme/retail_theme.json`. In versions with the older ribbon, use
   **View → Themes → Browse for themes** instead.
2. After import, set the 16:9 canvas size and arrange visuals using this guide.
   Set card padding, corners, shadows, series assignments, and measure formats
   manually where needed; these are layout rules, not all encoded in the JSON.
3. Existing visual-level formatting can override theme defaults. Review only
   the affected formatting settings before changing them, and save the actual
   report in `powerbi/` after applying the theme.

Microsoft documents [theme imports](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes)
and [custom theme properties](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom).
The JSON is a theme asset, not an implemented dashboard. Desktop import,
rendering, layout, and accessibility verification remain **pending**.
