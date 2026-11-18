"""Performance metrics, computed from monthly returns.

Each metric has a one-line plain-language definition in METRIC_GLOSSARY, which the
website shows as a tooltip.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

METRIC_GLOSSARY = {
    "cagr": "Annualized return: the constant yearly growth rate that turns the starting value into the ending value.",
    "vol": "Volatility: how much monthly returns swing around their average, scaled to a year. Lower = smoother ride.",
    "sharpe": "Sharpe ratio: return above cash per unit of volatility. Above 0.5 is decent, above 1 is excellent for an allocation strategy.",
    "sortino": "Sortino ratio: like Sharpe, but only penalises downside swings (losses), not upside ones.",
    "max_dd": "Maximum drawdown: the worst peak-to-trough loss an investor would have lived through.",
    "ulcer": "Ulcer Index: measures how deep AND how long drawdowns last. Lower = less pain.",
    "upi": "Ulcer Performance Index (Martin ratio): return above cash divided by the Ulcer Index.",
    "calmar": "Calmar ratio: annualized return divided by the maximum drawdown.",
    "worst_year": "Worst calendar-year return.",
    "best_year": "Best calendar-year return.",
    "pct_pos": "Share of months with a positive return.",
    "worst_month": "Worst single month.",
    "turnover": "Average share of the portfolio traded per year (100% = the whole portfolio replaced once a year).",
    "corr_6040": "Correlation with a 60% US stocks / 40% US bonds portfolio: +1 moves in lockstep, 0 unrelated.",
    "beta_6040": "Beta to 60/40: how much the strategy moves, on average, when 60/40 moves by 1%.",
    "corr_spy": "Correlation with the US stock market (S&P 500).",
    "longest_dd": "Longest stretch (in months) spent below a previous high.",
    "current_dd": "How far the strategy is today below its all-time high.",
    "up_capture": "Up capture vs 60/40: share of 60/40's gains captured in its up months.",
    "down_capture": "Down capture vs 60/40: share of 60/40's losses suffered in its down months (lower is better).",
}


def equity(r: pd.Series) -> pd.Series:
    return (1 + r).cumprod()


def drawdown(r: pd.Series) -> pd.Series:
    eq = equity(r)
    peak = np.maximum.accumulate(np.r_[1.0, eq.values])[1:]
    return pd.Series(eq.values / peak - 1, index=r.index)


def cagr(r: pd.Series) -> float:
    n = len(r)
    return float((1 + r).prod() ** (12 / n) - 1) if n else np.nan


def summarize(r: pd.Series, rf: pd.Series, bench_6040: pd.Series | None = None, spy: pd.Series | None = None,
              turnover: pd.Series | None = None) -> dict:
    r = r.dropna()
    rf = rf.reindex(r.index).fillna(0.0)
    ex = r - rf
    dd = drawdown(r)
    ulcer = float(np.sqrt((dd ** 2).mean()))
    c = cagr(r)
    c_rf = cagr(rf)
    downside = ex.clip(upper=0)
    dd_dev = float(np.sqrt((downside ** 2).mean()) * np.sqrt(12))
    years = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    full_years = years[r.groupby(r.index.year).size() == 12]
    # longest time under water
    under = (dd < -1e-9).astype(int).values
    longest, run_ = 0, 0
    for u in under:
        run_ = run_ + 1 if u else 0
        longest = max(longest, run_)
    out = {
        "start": r.index[0].strftime("%Y-%m"),
        "end": r.index[-1].strftime("%Y-%m"),
        "months": int(len(r)),
        "cagr": c,
        "vol": float(r.std() * np.sqrt(12)),
        "sharpe": float(ex.mean() * 12 / (ex.std() * np.sqrt(12))) if ex.std() > 0 else np.nan,
        "sortino": float(ex.mean() * 12 / dd_dev) if dd_dev > 0 else np.nan,
        "max_dd": float(dd.min()),
        "ulcer": ulcer,
        "upi": float((c - c_rf) / ulcer) if ulcer > 0 else np.nan,
        "calmar": float(c / abs(dd.min())) if dd.min() < 0 else np.nan,
        "worst_year": float(full_years.min()) if len(full_years) else np.nan,
        "best_year": float(full_years.max()) if len(full_years) else np.nan,
        "pct_pos": float((r > 0).mean()),
        "worst_month": float(r.min()),
        "longest_dd": int(longest),
        "current_dd": float(dd.iloc[-1]),
    }
    if turnover is not None and len(turnover):
        yrs = max(len(r) / 12, 1e-9)
        # one-sided: a full switch from asset A to asset B counts as 100% turnover
        out["turnover"] = float(turnover.iloc[1:].sum() / 2 / yrs) if len(turnover) > 1 else 0.0
    for name, b in (("6040", bench_6040), ("spy", spy)):
        if b is None:
            continue
        both = pd.concat([r, b], axis=1, join="inner").dropna()
        if len(both) < 12:
            continue
        a, bb = both.iloc[:, 0], both.iloc[:, 1]
        out[f"corr_{name}"] = float(a.corr(bb))
        if name == "6040":
            out["beta_6040"] = float(a.cov(bb) / bb.var())
            up, dn = bb > 0, bb < 0
            out["up_capture"] = float(a[up].mean() / bb[up].mean()) if up.any() else np.nan
            out["down_capture"] = float(a[dn].mean() / bb[dn].mean()) if dn.any() else np.nan
    return {k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in out.items()}


def annual_returns(r: pd.Series) -> dict:
    g = r.groupby(r.index.year)
    return {int(y): float((1 + x).prod() - 1) for y, x in g}


def rolling_cagr(r: pd.Series, months: int) -> pd.Series:
    return (1 + r).rolling(months).apply(np.prod, raw=True) ** (12 / months) - 1
