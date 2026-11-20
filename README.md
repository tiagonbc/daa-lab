# DAA Lab: Dynamic Asset Allocation research platform

**102 published tactical asset allocation strategies, rebuilt from scratch on Norgate data, plus macro-factor models. They are blended walk-forward into one portfolio that is tracked every month.**

An independent demonstration by **Tiago Costa**, prepared for a job application to the Dynamic Asset Allocation team (Total Fund Management) at Ontario Teachers' Pension Plan. It is not affiliated with or endorsed by OTPP, and it is not investment advice.

**Live site:** https://tiagonbc.github.io/daa-lab/ · Signals as of **2026-10-30** · Data through **2026-11-17**

---

## What this is, in plain language

Dynamic (or tactical) asset allocation means changing how much you hold in stocks, bonds, real assets and cash when markets or the economy change. Researchers have published dozens of rule-based ways to do this. This project:

1. **Rebuilds the research.** 102 strategies from the literature: Faber, Antonacci, Keller, Butler, Varadi, Livingston and others, plus macro-factor models that follow Macrosynergy's method. Each one is coded from its original rules, and any ambiguity is documented.
2. **Tests them fairly.** All use the same data (Norgate, dividends reinvested), the same timing (signals and trades at the month-end close) and the same cost (0.10% of value traded). Before ETFs existed, validated index proxies fill the history.
3. **Picks without hindsight.** Every December the blend ranks strategies on Sharpe and Ulcer Performance over the past 10 years. It keeps the top **5** whose returns correlate at most **0.7** with each other, using only data available at that time. The blend's record is therefore out-of-sample.
4. **Thinks like a total fund.** The blend's view is also tested as an *overlay* on a liquid proxy of OTPP's 2025 asset mix, sized to an active-risk (tracking-error) budget.
5. **Tracks it live.** The pipeline reruns after each month-end. Each month's signals are committed to Git before their returns are known, and the commit history is the audit trail.

## Headline results (hypothetical backtest, monthly, after costs)

Period: 2005-01 to 2026-10.

| Portfolio | CAGR | Volatility | Sharpe | Max drawdown |
|---|---:|---:|---:|---:|
| Tiago's DAA Blend (walk-forward) | 10.0% | 7.7% | 1.07 | -8.5% |
| 60/40 (SPY/IEF) | 8.0% | 9.1% | 0.70 | -29.5% |
| Global 60/40 | 6.9% | 9.5% | 0.57 | -33.4% |
| OTPP-shaped mix (liquid proxy) | 8.4% | 12.2% | 0.59 | -39.0% |
| S&P 500 | 10.7% | 14.8% | 0.65 | -50.8% |

Current blend components (2025-12): Hybrid Asset Allocation - Simple (HAA-1, SPY only), Inflation Compass - Original, Macro-support softmax, US-investable 4 risky classes + cash (faithful US replication), Defense First, Inflation-surge defensive overlay on 60/40.

### Replication check: do the backtests match the authors' published results?

Each strategy is coded from its rules and run on the lab's data, then compared with figures published by its authors or independent sources over the same years: **16 close, 3 broadly consistent, 0 differ** out of 19 ([full report](research/replication_check.md)).

| Strategy | Compared | Result | Verdict |
|---|---|---|---|
| Global Tactical Asset Allocation 5 (GTAA 5) | 13 calendar years (2000-2012) | correlation 0.98, average gap 1.4 pts | close |
| Ivy Portfolio (static 5-asset equal weight) | 13 calendar years (2000-2012) | correlation 0.99, average gap 1.6 pts | close |
| Global Tactical Asset Allocation – Aggressive 3 (GTAA Agg 3) | 12 calendar years (2001-2012) | correlation 0.94, average gap 3.5 pts | broadly consistent |
| Global Tactical Asset Allocation – Aggressive 6 (GTAA Agg 6) | 12 calendar years (2001-2012) | correlation 0.78, average gap 5.0 pts | broadly consistent |
| Global Equities Momentum (GEM) - Traditional Dual Momentum (official rules) | 26 calendar years (2000-2025) | correlation 0.98, average gap 1.7 pts | close |
| Hybrid Asset Allocation - Balanced (HAA-8, G8/T4) | 17 calendar years (2006-2022) | correlation 1.00, average gap 0.8 pts | close |
| Hybrid Asset Allocation - Simple (HAA-1, SPY only) | 17 calendar years (2006-2022) | correlation 1.00, average gap 0.6 pts | close |
| Bold Asset Allocation - Balanced (BAA-G12/T6) | 2012-07 to 2022-06 | CAGR 7.7% vs 7.8%, max DD -7.0% vs -7.2% | close |
| Bold Asset Allocation - Aggressive (BAA-G4/T1) | 2012-07 to 2022-06 | CAGR 11.1% vs 10.9%, max DD -8.5% vs -8.7% | close |
| Defensive Asset Allocation - G12 (DAA, T6/B2) | 2008-04 to 2018-03 | CAGR 9.6% vs 9.9%, max DD -8.9% vs -9.0% | close |
| Vigilant Asset Allocation - G4 Aggressive (VAA-G4, T1/B1) | 2008-04 to 2018-03 | CAGR 8.3% vs 10.5%, max DD -16.1% vs -10.5% | broadly consistent |
| Protective Asset Allocation - PAA2 (high protection, Top6, IEF) | 7 calendar years (2009-2015) | correlation 0.92, average gap 1.4 pts | close |
| Growth-Trend Timing (GTT-Original) | 26 calendar years (2000-2025) | correlation 0.94, average gap 2.3 pts | close |
| Growth-Trend Timing - UE Rate | 10 calendar years (2016-2025) | correlation 0.98, average gap 1.8 pts | close |
| Permanent Portfolio | 26 calendar years (2000-2025) | correlation 1.00, average gap 0.4 pts | close |
| Golden Butterfly | 26 calendar years (2000-2025) | correlation 1.00, average gap 0.6 pts | close |
| All-Weather/All-Seasons Portfolio | 26 calendar years (2000-2025) | correlation 0.99, average gap 0.7 pts | close |
| US Stocks (S&P 500) | 26 calendar years (2000-2025) | correlation 1.00, average gap 0.2 pts | close |
| 60/40 Portfolio (US) | 2003-01 to 2022-12 | CAGR 7.4% vs 7.4%, max DD -29.5% vs -29.5% | close |

### Top strategies by Sharpe ratio, last 10 years

| Strategy | Author | CAGR | Sharpe | Max drawdown |
|---|---|---:|---:|---:|
| Inflation Compass - Original | David Varadi (CSS Analytics) | 27.6% | 1.26 | -17.8% |
| Hybrid Asset Allocation - Simple (HAA-1, SPY only) | Wouter J. Keller, Jan Willem Keuning | 15.5% | 1.24 | -9.1% |
| Hybrid Asset Allocation - HAA-12 (G12/T6) | Wouter J. Keller, Jan Willem Keuning | 12.2% | 1.21 | -4.9% |
| Macro-support softmax, US-investable 4 risky classes + cash (faithful US replication) | Replication of Brine, Cereda & Sueppel (2026) with US public data | 10.8% | 1.17 | -7.4% |
| Defense First | Thomas Carlson | 12.6% | 1.16 | -8.0% |
| Hybrid Asset Allocation 60/40 | NLX Finance (variant of Keller & Keuning's HAA-Simple) | 9.5% | 1.10 | -5.2% |
| Inflation Compass - Enhanced | David Varadi (CSS Analytics) | 21.8% | 1.06 | -15.9% |
| Hybrid Asset Allocation - Balanced (HAA-8, G8/T4) | Wouter J. Keller, Jan Willem Keuning | 11.3% | 1.03 | -8.0% |
| Growth/inflation quadrant allocation (illustrative) | Tiago Costa, after Ilmanen, Maloney & Ross (2014) and Neville et al. (2021) | 10.8% | 1.02 | -12.8% |
| Hybrid Asset Allocation - HAA-4 (G4/T2) | Wouter J. Keller, Jan Willem Keuning | 11.4% | 0.95 | -9.0% |

The full library, with rules in plain English, charts and current holdings, is on the website.

## How it is built

```
daalab/
  data/        Norgate + public-web loaders, proxy chains (ETF -> index -> synthetic), macro panel with publication lags
  engine/      monthly backtester (signals at t, returns over t+1, 0.10% costs) and metrics
  strategies/  one module per family; descriptions come from research/strategies_*.json
  blend/       walk-forward top-N uncorrelated selection, sensitivity grid
  pipeline.py  runs everything and writes docs/data/*.json for the website
docs/          static website (GitHub Pages): no build step, ECharts from a CDN
research/      strategy catalogs, Macrosynergy replication spec, literature review
tests/         metrics, look-ahead protection, macro lags, blend selection
```

### Reproduce

```bash
pip install -r requirements.txt     # needs a Norgate Data subscription with the Norgate Data Updater running
python scripts/run_all.py           # about 10 minutes: every strategy, the blend, the website data and this README
python -m pytest                    # 13 tests
python -m http.server 8791 --directory docs
```

## Data and honesty notes

- **Prices:** Norgate Data, total-return adjusted. Raw Norgate data is licensed and is **not** in this repository; only derived strategy results are published.
- **Back-fills before ETFs existed** were validated against each real ETF over their overlap. Most correlations are above 0.95; see the Method page.
- **Macro data** (Norgate Economic database, FRED, Philadelphia Fed SPF) is lagged by its publication delay. Norgate stores revised values, not first releases.
- **Selection bias:** even a walk-forward blend draws on strategies that were published *because* they backtested well. Expect live results to be weaker than the backtest.
- **AI use:** built with an AI coding assistant (Claude Code). Every output was checked: proxies reconciled to ETFs, citations verified at source, rules checked against the papers, and unit tests for look-ahead.

## Contact

Tiago Costa · tiagonbc@gmail.com · [linkedin.com/in/tiagonbc](https://www.linkedin.com/in/tiagonbc)

*Last generated 2026-11-18 18:37 UTC.*
