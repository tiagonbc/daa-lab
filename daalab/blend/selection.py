"""Tiago's DAA Blend: the top-N uncorrelated strategies, chosen walk-forward.

The recipe, in plain words:
  1. Every December, look ONLY at the strategy returns known so far.
  2. Score every strategy with at least 5 years of history on two risk-adjusted
     measures (Sharpe ratio and Ulcer Performance Index) over the last 10 years,
     and average the two ranks.
  3. Walk down the ranking. Accept a strategy only if its return correlation with
     every strategy already accepted is below a cap (0.70 by default). Stop at N.
  4. Hold the N strategies in equal weights for the next 12 months.

Because each year's choice only uses past data, the blend's track record is
out-of-sample - the honest way to evaluate a "pick the best" process. The default
settings (N=5, cap=0.70, 10y window) were fixed before looking at results; the
sensitivity grid on the site shows how much the answer depends on them.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from ..engine import metrics as mt


@dataclass
class BlendConfig:
    n: int = 5
    corr_cap: float = 0.70
    window: int = 120          # months used to score and to measure correlation
    min_history: int = 60      # months a strategy needs before it can be picked
    reselect_month: int = 12   # re-select every December
    weighting: str = "equal"   # equal | inverse_vol


@dataclass
class Selection:
    date: pd.Timestamp
    chosen: list[str]
    scores: dict
    skipped: list[dict] = field(default_factory=list)   # [{id, blocked_by, corr}]


def score_strategies(R: pd.DataFrame, rf: pd.Series, asof: pd.Timestamp, cfg: BlendConfig) -> pd.DataFrame:
    hist = R.loc[:asof]
    rows = []
    for c in hist.columns:
        r = hist[c].dropna()
        if len(r) < cfg.min_history:
            continue
        r = r.iloc[-cfg.window:]
        m = mt.summarize(r, rf.reindex(r.index).fillna(0.0))
        rows.append({"id": c, "sharpe": m["sharpe"], "upi": m["upi"], "cagr": m["cagr"], "max_dd": m["max_dd"], "months": len(r)})
    if not rows:
        return pd.DataFrame(columns=["sharpe", "upi", "cagr", "max_dd", "months", "score"])
    df = pd.DataFrame(rows).set_index("id")
    df["score"] = (df["sharpe"].rank(ascending=False) + df["upi"].rank(ascending=False)) / 2
    return df.sort_values("score")


def select(R: pd.DataFrame, rf: pd.Series, asof: pd.Timestamp, cfg: BlendConfig) -> Selection:
    sc = score_strategies(R, rf, asof, cfg)
    window = R.loc[:asof].iloc[-cfg.window:]
    chosen, skipped = [], []
    cap = cfg.corr_cap
    while True:
        chosen, skipped = [], []
        for sid in sc.index:
            if len(chosen) >= cfg.n:
                break
            blocked = None
            for c in chosen:
                pair = window[[sid, c]].dropna()
                rho = pair[sid].corr(pair[c]) if len(pair) >= 24 else 1.0
                if rho > cap:
                    blocked = (c, rho)
                    break
            if blocked:
                skipped.append({"id": sid, "blocked_by": blocked[0], "corr": round(float(blocked[1]), 3)})
            else:
                chosen.append(sid)
        if len(sc) == 0 or len(chosen) >= min(cfg.n, len(sc)) or cap >= 0.99:
            break
        cap += 0.05   # not enough diverse strategies yet: relax the cap a little
    return Selection(date=asof, chosen=chosen, scores=sc.round(4).to_dict(orient="index"), skipped=skipped[:25])


def _weights(R: pd.DataFrame, chosen: list[str], asof: pd.Timestamp, cfg: BlendConfig) -> pd.Series:
    if cfg.weighting == "inverse_vol":
        vol = R.loc[:asof, chosen].iloc[-36:].std()
        w = 1 / vol
        return w / w.sum()
    return pd.Series(1 / len(chosen), index=chosen)


def walk_forward(R: pd.DataFrame, rf: pd.Series, cfg: BlendConfig) -> tuple[pd.Series, list[Selection], pd.DataFrame]:
    """Returns monthly blend returns, the yearly selections, and the component weights in force each month."""
    dates = R.index
    sel_dates = [d for d in dates if d.month == cfg.reselect_month]
    selections, rets, wrows = [], {}, {}
    current = None
    for i, d in enumerate(dates[:-1]):
        if d in sel_dates:
            s = select(R, rf, d, cfg)
            if len(s.chosen) >= min(cfg.n, 3):
                selections.append(s)
                current = _weights(R, s.chosen, d, cfg)
        if current is None:
            continue
        nxt = dates[i + 1]
        r = R.loc[nxt, current.index]
        w = current[r.notna()]
        w = w / w.sum()
        rets[nxt] = float((w * r[w.index]).sum())
        wrows[nxt] = w.to_dict()
    return pd.Series(rets, name="blend"), selections, pd.DataFrame.from_dict(wrows, orient="index").fillna(0.0)


def in_sample(R: pd.DataFrame, rf: pd.Series, cfg: BlendConfig, start: pd.Timestamp) -> tuple[pd.Series, Selection]:
    """Hindsight version: pick once using the WHOLE history. Shown only to measure selection bias."""
    s = select(R, rf, R.index[-1], BlendConfig(**{**cfg.__dict__, "window": 10_000}))
    w = _weights(R, s.chosen, R.index[-1], cfg)
    sub = R.loc[R.index > start, s.chosen]
    out = (sub * w).sum(axis=1, min_count=len(s.chosen)).dropna()
    return out.rename("blend_in_sample"), s


def sensitivity(R: pd.DataFrame, rf: pd.Series, base: BlendConfig, ns=(3, 4, 5, 6, 8, 10), caps=(0.5, 0.6, 0.7, 0.8, 0.9, 1.0)):
    grid = []
    for n in ns:
        for cap in caps:
            cfg = BlendConfig(**{**base.__dict__, "n": n, "corr_cap": cap})
            r, _, _ = walk_forward(R, rf, cfg)
            m = mt.summarize(r, rf)
            grid.append({"n": n, "cap": cap, "cagr": m["cagr"], "sharpe": m["sharpe"], "max_dd": m["max_dd"], "upi": m["upi"]})
    return grid
