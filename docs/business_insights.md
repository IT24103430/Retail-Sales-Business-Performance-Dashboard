# Business Insights — Synthetic Portfolio Data

**All results below come from synthetic portfolio data, not real business results.**
The findings describe the generated Sri Lankan retail scenario; they do not establish real demand or causes.

Coverage: **2025-01-01 through 2026-09-30**, **5,000 order lines**, **2,453 distinct orders**. Money is LKR.

## Calculated metrics

| Metric | Calculated value |
| --- | ---: |
| Gross Revenue | LKR 12,892,276.50 |
| Total Discount | LKR 543,544.21 |
| Total Revenue (after discount) | LKR 12,348,732.29 |
| Total Cost | LKR 8,888,670.77 |
| Total Profit | LKR 3,460,061.52 |
| Profit Margin % | 28.02% |
| Total Orders (distinct OrderID) | 2,453 |
| Units Sold | 11,699 |
| Average Order Value | LKR 5,034.13 |

## Five factual findings

1. **Monthly sales:** 2026-04 had the highest observed monthly net revenue, LKR 962,743.97, with profit of LKR 269,314.11. Its revenue change from 2026-03 was +52.39%.
2. **Strongest category by revenue:** Small Appliances generated LKR 6,009,227.45, 48.66% of total net revenue, and LKR 1,695,048.70 profit; its margin was 28.21%.
3. **Top products by revenue:** Table Fan 16 Inch (P030): LKR 2,882,836.95; Rice Cooker 1.8 L (P029): LKR 1,929,706.25; Electric Kettle 1.7 L (P028): LKR 1,196,684.25. Together these 3 products accounted for 48.66% of total net revenue.
4. **Leading region by revenue:** Western generated LKR 3,593,492.02, 29.10% of net revenue, with 703 distinct orders. Colombo is its representative city label, not an independently measured city market.
5. **Leading channel by revenue:** Physical Store generated LKR 7,660,489.12, 62.03% of net revenue, with 1,507 distinct orders and a 28.10% margin.

## Three recommendations for the fictional scenario

1. **Review product availability:** Prioritize a mock availability and replenishment review for Small Appliances and the revenue-leading products above; inventory and stockout data would be needed to justify purchasing changes.
2. **Investigate margin:** Review unit costs and line discounts in **Beverages**, whose margin is 27.66%, compared with the overall 28.02%; test pricing or discount changes in the fictional scenario.
3. **Evaluate regional and channel plans:** Use Western and Physical Store as starting points for a small fictional assortment or channel experiment, comparing the same calendar months and accounting for regional/channel coverage before extending the plan elsewhere.

## Calculation notes and limits

- Sources: `data/raw/fact_sales.csv` and the four `dim_*.csv` files in the same folder. Products/categories, region labels, and channel labels are looked up using unique dimension keys; customer and region keys are checked.
- GrossSales = Quantity × UnitPrice; NetSales = GrossSales − DiscountAmount; TotalCost = Quantity × UnitCost; LineProfit = NetSales − TotalCost. DiscountAmount is a line total, subtracted once.
- Totals aggregate every validated source line once. Orders use distinct OrderID; margin = total profit ÷ net revenue; AOV = net revenue ÷ distinct orders. Distinct order counts across categories/products are not additive.
- Decimal arithmetic preserves monetary precision; rounding to two decimal places happens only for display. A zero denominator is shown as N/A. Invalid rows or duplicate keys stop generation instead of silently changing totals.
- Leaders use net revenue. Ties use earliest month or alphabetical category/key order; one leader is shown. Top product lists contain up to three products with observed sales.
- Monthly totals use observed order dates. Calendar months with no rows have no observed revenue; the script does not invent zero sales or compare against the last nonblank month. Boundary months may be partial; the supplied dataset ends in September 2026, so 2026 is not a complete sales year.
- Tax, delivery fees, operating expenses, inventory, campaign effects, and real customer information are not modeled. Recommendations are suggestions for a portfolio exercise, not evidence of actual business problems.

Regenerate from the project root with `python3 scripts/generate_insights.py`. This report is calculated from CSVs; it is not evidence of Power BI Desktop execution.
