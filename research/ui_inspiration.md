# UI inspiration from AllocateSmartly's public pages

Scope: only public pages were used: the blog, What We Do, Advanced Features, FAQs, Core Ideas, Pricing, List of Strategies, and the screenshots embedded in public blog posts. No member pages were used. Everything below is described in my own words. No images or text were copied. The goal is a feature and metric checklist for the DAA Lab backtester UI.

---

## 1. Performance metrics they report

**Summary statistics table.** Every strategy review and every Model Portfolio has one. It has two column pairs side by side, and each statistic shows the strategy (or portfolio) next to the benchmark.

| Metric | How they define it / notes for our implementation |
|---|---|
| Annualized Return | Geometric (CAGR), not arithmetic. |
| Annualized Volatility | Annualized standard deviation of monthly returns. |
| Sharpe Ratio | Excess return over cash divided by volatility. |
| Sortino Ratio | Return divided by downside deviation. They describe downside deviation as volatility on losing months only. |
| Max Drawdown (EOM) | Measured on **end-of-month** values, so tests on daily and monthly data are comparable. The month of the trough is shown under the value. |
| Longest Drawdown | Months from the prior all-time high to the next new high. |
| Ulcer Performance Index (UPI, "Martin ratio") | Their favourite risk-adjusted measure. It is return relative to the Ulcer Index, which captures both the depth and the duration of drawdowns. |
| % Profitable Months | Share of months with a positive return. |
| Best Month Return / Worst Month Return | |
| Average Trades per Year | Counts only *trades*, meaning changes in the target allocation. Rebalances back to target are not counted. |
| Annual Turnover | Percentage of the portfolio replaced per year. A better activity measure than trade count when many trades are small. |
| Safe Withdrawal Rate (SWR) | Bengen method. Simulations start on every quarter, with a 30-year retirement and historical inflation. When the data runs out, the sample loops back to the start. The result is the worst sequence. |
| Perpetual Withdrawal Rate (PWR) | The rate that preserves the inflation-adjusted starting capital over the worst sequence. |

**Other statistics they compute or use:**
- **Screener columns:** MTD return, prior-month return, YTD return, plus all of the summary stats above.
- **Composite rankings:**
  - "Risk-adjusted best" is a weighted average of Sharpe, Sortino and UPI.
  - "Lowest drawdown" is a weighted average of Max Drawdown and Ulcer Index.
  - Both are shown over the last 10 years.
- **Keller Ratio:** shown at three risk tolerances (K at 50%, 25% and 10%), computed over 20 years and adjusted for timing luck.
- **Tax efficiency:** the share of historical gains that came from long-term capital gains or dividends versus short-term gains. They also compare FIFO and LIFO lot selection.
- **Exposure to rising interest rates:** a per-strategy estimate.
- **Correlation:** a strategy-to-strategy correlation matrix.
- **Return contribution:** each asset's contribution to annual return. A separate "trading friction" bar shows costs plus slippage as a negative.
- **Alternate-trading-day dispersion:** the spread of results across the 21 normalized trading days.
- **Underperformer flag:** set when recent performance has deteriorated well beyond the strategy's *own* historical norms. Both absolute and benchmark-relative performance count, and so does a long flat stretch, not only a loss.
- **10-year stock-market return forecasts:**
  - Built from several valuation models (CAPE variants, market cap to GDP or GVA, Q ratio, AIAE and others).
  - Shown in two versions: hindsight fit and walk-forward.
  - The average forecast error is reported.

## 2. Chart types

1. **Equity curve (growth of $10,000).**
   - Log scale by default, with a toggle to linear.
   - The strategy line (orange/coral) is drawn against the benchmark line (dark grey).
   - The subtitle states the scaling and the date span.
2. **Drawdown curve.** The benchmark drawdown is a light-grey filled area, and the strategy drawdown is a coloured line over it. Values are end-of-month.
3. **Interactive zoom with rebasing.**
   - Zoom options: preset windows (1, 3, 10 and 20 years), typed YYYY-MM start/end dates, or a mouse-drag selection.
   - Every zoom rebases the curve to $10,000 at the window start.
   - A slider at the bottom then rolls that window length across the whole history, which gives rolling-period comparisons.
4. **Alternate-trading-days chart.**
   - Equity curves for all 21 normalized trading days of the month.
   - Most days are drawn as thin grey lines.
   - The default day (month-end) is highlighted, and sometimes the cross-day average too.
   - It shows timing luck and overfitting risk at a glance.
5. **Performance by day of month traded.** A multi-coloured spaghetti chart on a log scale, one line per trading day.
6. **Historical allocation views (one subpage per strategy):**
   - pie chart of average allocation since inception;
   - average allocation by year, as a stacked chart by asset;
   - the same chart grouped by asset category (US equities, international equities, Treasuries, credit, real estate, commodities, gold, cash);
   - table of recent allocation changes.
7. **Return contribution bar charts:**
   - by asset, sorted from largest to smallest, with trading friction as a separate negative bar;
   - click a bar to drill down to that asset's contribution by year;
   - rolled up by asset category;
   - rolled up as risk-on versus risk-off.
8. **Aggregate TAA allocation.** A 100% stacked area chart of the average month-end allocation across all tracked strategies, by category and over time. It is also shown by individual asset and as risk-on/risk-off, and compared with historical norms.
9. **Cluster analysis.** A radial dendrogram (hierarchical clustering of strategy returns). Branches carry labels such as Classic Tactical, Slow Tactical, Fast Tactical, Primarily Passive, Bonds, RPV and GTT. Hovering shows the strategy names.
10. **Correlation matrix** between strategies. It can be filtered to the strategies of interest.
11. **Valuation and forecast charts:**
    - predicted versus realised 10-year returns as two lines;
    - a scatter plot of the indicator against the subsequent return, with a regression line and a marker for the current reading.
12. **Monthly "recent performance" leaderboard.** A sortable table of every strategy with the month's return and YTD return.
13. **Strategy–asset matrix.** A grid with strategies as rows and asset classes as columns. A dot marks each asset in a strategy's universe.

## 3. Combining strategies into portfolios ("Model Portfolios")

**Building a Model Portfolio:**
- Users combine *strategies*, not assets, with user-set weights. The plan tier sets the limit on the number of portfolios: 3 standard, 15 pro.
- The live view shows the weighted sum of each strategy's current allocation. For example, 50% Strategy A (100% SPY) plus 50% Strategy B (100% cash) shows as 50% SPY and 50% cash.
- Buy & hold assets can be mixed in. Each passive asset is capped at 50%.
- Workflow is a "shopping cart": add strategies while browsing, then commit the portfolio to turn on live tracking and emails.

**Backtesting a Model Portfolio:**
- Weights between strategies are rebalanced at each calendar month-end, with the same cost assumptions as single strategies.
- The backtest starts once strategies covering at least 80% of the weight have data. Until the remaining strategies start, their weight is spread pro rata across the available ones.

**Trading-day options:**
- Each strategy can be set to trade on any normalized day from 1 to 21.
- A strategy can also be **tranched**, meaning split across several days of the month to reduce timing luck.

**Portfolio Optimizer:**
- Searches all strategies (or a user-chosen pool of up to 10) for the best mix of 3, 5 or 10 strategies.
- Objectives include Max Sharpe, Min Variance, Max Diversification, Max Sortino and Max UPI; seven objectives in total.
- Options:
  - shrink the covariance/correlation estimates (an overfitting guard);
  - use only tax-efficient strategies (at least 75% of gains from long-term capital gains or dividends);
  - avoid strategies with high exposure to rising rates.
- It optimises over the common start date of the chosen strategies. It also shows an "alternative" portfolio with a longer history.

**Other combination tools:**
- **Compare tool:** up to 5 strategies, portfolios or benchmarks, aligned to their earliest common date, with side-by-side curves and stats. SWR/PWR always use the full sample.
- **Alternative benchmarks:**
  - the default is 60/40 (60% SPY, 40% IEF, rebalanced monthly);
  - the others are S&P 500, Nasdaq-100, Dow, 10-year Treasuries, ACWI, and a global 60/40 (60% ACWI, 20% BWX, 20% IEF).
  - An ERC portfolio is suggested as a risk-balanced benchmark.
- **Meta Strategy:** a ready-made, walk-forward selection of 10 strategies each month. They describe it as a diversified sample of good strategies rather than an attempt to time strategies.

## 4. Rebalance and "next signal" features

**Intraday signal display:**
- From the 09:30 ET open on a trading day, the platform shows the *expected* new allocation.
- It updates through the day as prices move.
- Backtests assume the final allocation is executed at the 16:00 ET close.

**Email notifications:**
- Can be intraday, end-of-day and/or weekly.
- They fire when a change is likely today.
- The aggregate-allocation report is also available by email.

**Other signal tools:**
- **"Alt. Trading Days: Current Allocation" table:** the current allocation for every trading day of the last month. It shows how sensitive the signal is to day choice.
- **Trades versus rebalances:** only trades (target changes) are signalled. Drift rebalances are left to the user but are included in results.
- **Normalized day of month:** day = round(trading_day / days_in_month × 21). Day 1 is always the first trading day and day 21 is always the last.
  - For month-end indicators traded on another day, the indicator uses the last N values *on that same normalized day*.
  - Example: a 10-month SMA traded on day 15 uses the last ten day-15 closes.
  - Calendar tables that convert normalized days to dates are published each year.

**Execution robustness guidance:**
- A one-day execution delay has had little effect on long-run results.
- Small positions (for example under 5–10%) can be rolled into broader asset classes with little loss.

## 5. Filters and screening

**Strategy Screener:**
- A min/max slider for every statistic, sortable by any column.
- Users pick the number of years to analyse and whether to include alternate trading days.
- Users choose which columns to display.

**Category filters:**
- **Estimated risk:** Conservative, Moderate or Aggressive, based on volatility relative to the 60/40.
- **Strategy type:** Momentum & Trend-Following, Portfolio Optimization, Economic Data, or "Four Seasons" (all-weather style).
- Trade frequency (daily, monthly and so on).
- Best over the last 10 years: highest return, highest risk-adjusted return, or lowest drawdown.
- Crisis performance (for example the GFC).
- Exposure to rising rates.
- Tax efficiency.

**Other screening tools:**
- **Underperformer Watchlist:** a separate list of strategies doing worse than their own history implies.
- **Strategy–asset matrix:** helps pick strategies that trade similar assets, for example to limit turnover or work within a restricted list of ETFs.

## 6. Backtest conventions worth copying (these drive what the UI shows)

**Execution and costs:**
- Trades happen at the close.
- Costs plus slippage are 0.10% per trade (0.20% round trip).
- Dividends are reinvested.
- Uninvested "cash" earns the 3-month T-bill rate. BIL, SHV or GBIL are suggested ETF stand-ins.
- Taxes are not deducted, but tax efficiency is reported.

**Assets and data:**
- Every strategy maps to one representative ETF per asset class: the largest and most liquid, whatever ETF the author used.
- History before each ETF launched is simulated from closely related indices, with that ETF's expense ratio applied.
- Two backtests are often shown:
  - a long one on monthly data, starting earlier;
  - a shorter one on daily data, which enables alternate trading days.
- Indicator inputs use dividend-adjusted prices. Each dividend is treated as unknown until 2 trading days after its ex-date, to avoid look-ahead.
- Macro series are lagged to their publication dates. Vintage (first-reported) data is used where it is available.

**Statistics:** drawdown statistics use end-of-month values.

## 7. Layout and cleanliness principles observed

**Chart and table style:**
- Same visual language everywhere:
  - **Colours:** one accent colour (coral/orange) for the subject, and neutral dark grey or light-grey fill for the benchmark.
  - **Titles:** a clear title, with a one-line subtitle giving the scaling and period.
  - **Gridlines:** sparse horizontal only, no chart junk.
  - **Legend:** below the plot.
- Tables use a dark header bar, zebra-free light rows, right-aligned numbers, and small grey secondary text (for example the date of the max drawdown under its value).
- Stats are always shown *next to a benchmark*, so no number appears without context.

**Defaults and guidance:**
- Log scale is the default for long histories. A short explainer covers when linear is fine.
- The design steers users toward risk-adjusted and long-horizon measures. It warns that windows under about 3 years invite chasing the hot hand, and it defaults to a diversified benchmark rather than the S&P 500.
- Plain-language explanations sit next to advanced tools: a glossary for every statistic, "about this objective" boxes in the optimizer, and hover tooltips on charts.

**Navigation:**
- Progressive disclosure: start from a list of strategies, open the summary backtest, then drill into subpages (historical allocation, return contribution, alternate trading days, tax, withdrawal rates).
- A portfolio-level dashboard manages several Model Portfolios at once.

**Fairness and comparability:**
- All strategies run on the same assets, cost model and dates.
- Compare views align series to a common start date.

## 8. Suggested must-haves for DAA Lab (derived from the above)

1. Per-strategy summary table: CAGR, volatility, Sharpe, Sortino, MaxDD (EOM, with date), longest drawdown, Ulcer Index and UPI, % positive months, best and worst month, trades per year, turnover, SWR and PWR. Each value sits beside the 60/40 (SPY/IEF) benchmark.
2. Charts:
   - log/linear equity curve with rebasing zoom and a rolling-window slider;
   - drawdown overlay;
   - annual returns bars;
   - allocation history (stacked area) and average allocation pie;
   - return contribution by asset, including friction;
   - alternate-trading-day fan chart.
3. Portfolio builder that combines strategies (and optionally B&H assets), with month-end rebalancing between strategies, tranching, the 80% data-availability start rule, and an optimizer (max Sharpe, min variance, max diversification, max UPI) with shrinkage.
4. "Next signal" panel: the current target weights, the weights if today were the rebalance day, the change versus the current holding, and the next scheduled rebalance date (normalized day 21 by default).
5. Screener with min/max filters, category tags (type, risk tier, data needs such as "uses macro data") and a strategy–asset matrix.
