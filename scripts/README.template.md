# DAA Lab: Dynamic Asset Allocation research platform

**{{N_STRATEGIES}} published tactical asset allocation strategies, rebuilt from scratch on Norgate data, plus macro-factor models. They are blended walk-forward into one portfolio that is tracked every month.**

An independent demonstration by **Tiago Costa**, prepared for a job application to the Dynamic Asset Allocation team (Total Fund Management) at Ontario Teachers' Pension Plan. It is not affiliated with or endorsed by OTPP, and it is not investment advice.

**Live site:** {{SITE_URL}} · Signals as of **{{SIGNAL_DATE}}** · Data through **{{DATA_THROUGH}}**

---

## What this is, in plain language

Dynamic (or tactical) asset allocation means changing how much you hold in stocks, bonds, real assets and cash when markets or the economy change. Researchers have published dozens of rule-based ways to do this. This project:

1. **Rebuilds the research.** {{N_STRATEGIES}} strategies from the literature: Faber, Antonacci, Keller, Butler, Varadi, Livingston and others, plus macro-factor models that follow Macrosynergy's method. Each one is coded from its original rules, and any ambiguity is documented.
2. **Tests them fairly.** All use the same data (Norgate, dividends reinvested), the same timing (signals and trades at the month-end close) and the same cost (0.10% of value traded). Before ETFs existed, validated index proxies fill the history.
3. **Picks without hindsight.** Every December the blend ranks strategies on Sharpe and Ulcer Performance over the past 10 years. It keeps the top **{{BLEND_N}}** whose returns correlate at most **{{BLEND_CAP}}** with each other, using only data available at that time. The blend's record is therefore out-of-sample.
4. **Thinks like a total fund.** The blend's view is also tested as an *overlay* on a liquid proxy of OTPP's 2025 asset mix, sized to an active-risk (tracking-error) budget.
5. **Tracks it live.** The pipeline reruns after each month-end. Each month's signals are committed to Git before their returns are known, and the commit history is the audit trail.

## Headline results (hypothetical backtest, monthly, after costs)

{{BLEND_TABLE}}

Current blend components ({{SELECTION_DATE}}): {{COMPONENTS}}.

### Top strategies by Sharpe ratio, last 10 years

{{TOP_TABLE}}

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
python -m pytest                    # {{N_TESTS}} tests
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

*Last generated {{GENERATED_AT}}.*
