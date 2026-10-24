# Report Interactions

This is the shared interaction specification for **Executive Overview**,
**Product Performance**, and **Regional & Channel**. It replaces the earlier
page-local slicer rules in the page specifications. Keep the existing model,
measures, and standard Desktop visuals; no additional DAX or custom visuals are
needed. All Desktop setup and verification below remain pending.

## Defaults and shared slicers

| Control | Exact field | Synchronization and visibility | Saved default |
| --- | --- | --- | --- |
| Date | `DimDate[Date]` | Sync and show on all three pages; Between slicer | 2025-01-01 through 2026-09-30 inclusive |
| Category | `DimProducts[Category]` | Sync and show on all three pages; dropdown | All categories |
| Region | `DimRegions[RegionName]` | Sync and show on all three pages; dropdown | All regions |
| Channel | `DimChannels[ChannelName]` | Sync and show on all three pages; dropdown | All channels |
| Product | `DimProducts[ProductName]` | Product Performance only; do not sync to other pages | All products |

Keep the first four slicers in the same order and position on every page. Add
the searchable Product dropdown on Product Performance beside or just below
that row. Show every shared slicer: a hidden synchronized control still filters
the page and makes the context harder to understand. Category, Region, Channel,
and Product support multiple selection, Select all, clear, and alphabetical lists.

Retain the page-level Date limits on **every page**, covering only the sales
period above, and keep them locked after authoring. Keep C1's Product Top 10 and
T1's below-28% margin rule as local visual filters on Product Performance. They
are not resettable user choices. Save the report on Executive Overview with
default slicers, no chart selections, and the specified chart sort/drill states.
Use fixed dates rather than a relative-to-today default for this historical data.

### Desktop: configure synchronization

1. Open **View → Sync slicers**. Keep the existing Executive Overview controls
   as the four master slicers. Remove redundant standalone copies of those
   fields from other pages before creating synchronized copies; keep Product.
2. Select the Date slicer. In the Sync slicers pane, check **Sync** and **Visible**
   for all three named pages. Repeat separately for Category, Region, and Channel.
3. Arrange the synchronized controls on each page. If copying/pasting a master
   instead, accept the prompt to sync it; verify the same pane settings afterward.
   Having the same field in two slicers alone does not establish synchronization.
4. Select Product on Product Performance and leave the other pages unchecked
   for Sync and Visible. Keep just one copy of each control per page.
5. Set the shared defaults from the table. Confirm each shared field forms one
   synchronized selection, rather than three independent controls.

The controls use the native [slicer features](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers).
Navigation should retain their selections. A product choice affects only Product
Performance and may still be selected when returning to that page.

## Cross-filtering within a page

Use **Filter**, not Highlight, so cards and charts describe the same selected
sales. Shared slicers filter all cards/charts/tables/matrices on their page.
They do not narrow each other's available lists. On Product Performance,
Category additionally filters the Product list; Product does not filter shared
slicer controls. Clear Product if a changed Category gives an empty intersection.

| Source | Target / behavior |
| --- | --- |
| A chart bar, trend point, or table/matrix value cell | Filter the page's KPI cards and other analytical visuals |
| A regional matrix value cell | Pass both region and category to other analytical visuals |
| A regional small-multiple point | Pass both region and month to other analytical visuals |
| Any chart/table/matrix selection | None on all slicer controls, navigation, and text |
| KPI card | No outgoing filtering |
| Hierarchy drill/expand action | Stay local to that visual; do not apply drill filters to the whole page |

Chart selections are local focus actions and do **not** update synchronized
slicers or carry a product/region selection into another page. Use the shared
slicers for a comparison that must continue across pages. A local chart selection
can remain when returning to its page; clear it or use that page's Reset filters.
Clear a point selection by clicking empty chart space or selecting the point
again. Prefer slicers over combining many Ctrl-click chart selections.

**Desktop steps:** Select each source visual, choose **Format → Edit interactions**,
then choose the Filter or None icon on each target according to the rules above.
Repeat for each slicer and analytical visual on each page; copying visuals is not
proof that their interactions are correct. Exit Edit interactions when done.
See [Microsoft's interaction guide](https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions).

## Page navigation

Use one horizontal **native Page navigator** in the same header location on
each page. Its order and labels must be:

1. Executive Overview
2. Product Performance
3. Regional & Channel

Keep the native page tabs as a fallback. Use navy text on white for inactive
buttons and white text on teal for the selected page; the text and selected
state should identify the location without relying on color alone.

**Desktop steps:** Order and rename the three page tabs first. Select
**Insert → Buttons → Navigator → Page navigator**, format it, then copy it to the
other pages. Exclude hidden and tooltip pages from the navigator. In Desktop
edit mode, **Ctrl+click** a navigator button to follow it. Use a page navigator
rather than data-capturing bookmarks for ordinary navigation, so moving pages
does not restore old filter choices. See the
[page navigator guide](https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators).

## Tooltips: revenue, profit, and orders

Use standard visual tooltips on all bar and line charts. They should show the
hovered category/product/region/channel/month and these existing measures:

| Metric | Measure | Format |
| --- | --- | --- |
| Revenue after discounts | `[Total Revenue]` | Full LKR, 2 decimals |
| Profit after product costs | `[Total Profit]` | Full LKR, 2 decimals |
| Distinct orders | `[Total Orders]` | Whole number, thousands separator |

Existing page-specific tooltip metrics such as margin, AOV, and MoM % may stay,
but keep these three consistent. The tooltip uses the hovered point's context
and active slicers. Order counts remain distinct, even for multi-item orders.
The same order may appear in several category tooltips; those counts cannot be
added to recreate the report total.

**Desktop steps:** Select a chart, enable **Format visual → General → Tooltips**,
and use the default tooltip type. In **Build visual → Tooltips**, add the three
measures as needed; metrics already supplied by the visual need not be duplicated.
Hover a point to check the actual displayed fields and formats. For the category
revenue/profit chart, ensure either series exposes both revenue and profit plus
orders. Native tooltips are documented in the
[visual tooltip guide](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-visual-tooltips).

Cards use their visible labels, and tables/matrices retain native cell tooltips.
Where there is no editable Tooltips field well, do not promise the three-metric
hover or create a tooltip page just to force it. Use adjacent chart tooltips and
cards for the extra metrics; leave the detailed table/matrix fields as specified.

## Reset filters

Place one **Reset filters** button beside the navigator on each page. It resets
the four shared slicers across the report and the **current page's** local data
selections. On Product Performance it also clears Product. It does not clear
stored chart selections on other pages; use their own reset buttons when needed.
It keeps the current page and preserves the fixed date bounds and visual rules.

Create one bookmark per page:

| Page | Bookmark |
| --- | --- |
| Executive Overview | `Reset - Executive Overview` |
| Product Performance | `Reset - Product Performance` |
| Regional & Channel | `Reset - Regional & Channel` |

**Desktop steps:**

1. On each page, set default slicers, clear chart selections, and restore the
   specified sort/drill state. On Product Performance clear Product too.
2. Open **View → Bookmarks**, select **Add**, and give the bookmark its name above.
   Set **Data on**, **All visuals**, **Display off**, and **Current page off**;
   select **Update** after configuring it.
3. Insert **Buttons → Blank**, label it Reset filters, enable **Action**, choose
   **Type → Bookmark**, and select that page's matching bookmark. Do not copy a
   button to another page without changing its bookmark target.
4. **Ctrl+click** to try the button in Desktop. Update bookmarks deliberately
   after changing authored defaults or adding slicers, then save the report.

These settings use [report bookmarks](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks).
They can also restore the captured active-page sort and drill state. If the
button/action is unavailable in the viewing environment, clear each categorical
slicer using its eraser, restore the date range, and clear chart selections
manually. Do not rely on a service-only Reset to default command in Desktop.

## Quick manual check

Choose Western, Online Store, and one category on Executive Overview, then
navigate through both other pages: all four shared controls should retain their
choices. Select a product on Product Performance and confirm it does not filter
the other pages. Hover a chart point for revenue/profit/orders. Reset on that
page and confirm shared defaults and its Product selection are restored without
navigating away. Check that other pages may still need their own local chart
selection cleared. Finally restore defaults, open Executive Overview, and save.

These are manual acceptance steps, not completed verification. No report, PBIX,
PBIP, bookmark, or screenshot is created by this documentation step.
