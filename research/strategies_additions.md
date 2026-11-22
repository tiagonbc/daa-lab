# Strategies added after the AllocateSmartly survey

The machine-readable version is `strategies_additions.json`, which uses the same ids. Code: `daalab/strategies/trend_multi_asset.py`.

These come from a cross-asset diversifier study (Nov 2026) that looked for return sources with little correlation to an equity-timing portfolio. They are the lab's first strategies that can **short** an asset and use **leverage**: cash (BIL) takes `1 - sum(weights)`, so it is negative when the book is levered and above 100% when it is net short.

| id | Name | Universe | Source |
|---|---|---|---|
| `hop_trend_multi_asset` | Multi-Asset Trend Following (1, 3 and 12-month time-series momentum) | SPY, IWM, EFA, EEM, VNQ, TLT, IEF, LQD, TIP, HYG, GLD, SLV, DBC, USO, UUP | Hurst, Ooi & Pedersen (2017), [A Century of Evidence on Trend-Following Investing](https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing), Journal of Portfolio Management |
| `hop_trend_ex_equity` | Multi-Asset Trend Following, ex-equity | TLT, IEF, LQD, TIP, HYG, GLD, SLV, DBC, USO, UUP | same |

## Rules (both)

1. At each month-end close, every asset with 13 months of history votes +1 or -1 on each of its 1, 3 and 12-month total returns versus cash; the signal is the average vote (from -1 to +1).
2. Position = signal x 10% / (asset volatility x N), volatility from an EWMA of daily returns with a 60-day half-life.
3. The book is scaled to 10% expected volatility using the 126-day covariance of daily returns, at most 4x the raw weights.
4. Hold one month.

## Differences from the paper

- 15 (or 10) ETFs instead of 67 futures markets; index proxies before the ETFs where the lab has them. TIP, HYG, USO and UUP join only when their ETFs exist; EEM joins when it has daily data.
- Monthly rebalancing (the paper trades daily); the lab's 0.10% cost on traded value, including the cash leg.
- No fees, no extra borrow fee on short ETF positions, and leverage financed at the T-bill rate. A real account would pay more, so these results are optimistic on financing.
- Builds on Moskowitz, Ooi & Pedersen (2012), [Time Series Momentum](https://doi.org/10.1016/j.jfineco.2011.11.003), Journal of Financial Economics 104(2).
