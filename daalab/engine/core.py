"""Backtest engine.

How a strategy runs, in plain words:
  1. At the close of the last trading day of each month the strategy looks ONLY at
     data up to that day and returns target weights, e.g. {"SPY": 0.6, "IEF": 0.4}.
  2. Those weights are held through the following month (they drift with prices).
  3. At the next month-end we trade back to the new targets and pay 0.10% on the
     value traded.
Monthly net returns are what every metric and chart on the site is built from.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

from ..config import CASH, COST_PER_TRADE, EVAL_START

REGISTRY: dict[str, "Strategy"] = {}


class NotReady(Exception):
    """Raised by a strategy whose inputs (e.g. slow macro scores) are not yet available; the start moves later."""


@dataclass
class Strategy:
    id: str
    name: str
    author: str
    family: str                       # momentum-rotation | trend-following | risk-parity | static | macro | valuation | blend
    year: int
    source_title: str
    source_url: str
    assets: list[str]
    fn: Callable
    lookback_months: int = 13
    needs_daily: bool = False
    rebalance: str = "M"              # M monthly, Q quarterly, A annually
    plain_english: str = ""
    rules: list[str] = field(default_factory=list)
    notes: str = ""
    benchmark: bool = False
    allocatesmartly_url: str | None = None
    macro_inputs: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)   # assets used only once their data exists
    min_start: str | None = None                          # earliest rebalance date (e.g. non-price data begins)


def register(**meta):
    def deco(fn):
        s = Strategy(fn=fn, **meta)
        if s.id in REGISTRY:
            raise ValueError(f"duplicate strategy id {s.id}")
        REGISTRY[s.id] = s
        return fn
    return deco


class Context:
    """What a strategy is allowed to see at a rebalance date: data up to `date` only."""

    def __init__(self, monthly: pd.DataFrame, daily: pd.DataFrame | None, macro: pd.DataFrame | None, trade_dates: pd.Series):
        self.m = monthly
        self.d = daily
        self.macro = macro
        self.trade_dates = trade_dates
        self.i = 0
        self.state: dict = {}
        self._mv = monthly.values
        self._cols = {c: k for k, c in enumerate(monthly.columns)}

    # -- time
    @property
    def date(self) -> pd.Timestamp:
        return self.m.index[self.i]

    @property
    def trade_date(self) -> pd.Timestamp:
        return self.trade_dates.get(self.date, self.date)

    # -- monthly helpers (all use month-end total-return levels)
    def px(self, tickers, lag=0) -> pd.Series:
        k = self.i - lag
        if k < 0:   # never let a negative index wrap around to the end of the array (= the future)
            return pd.Series(np.nan, index=tickers)
        return pd.Series(self._mv[k, [self._cols[t] for t in tickers]], index=tickers)

    def ret(self, tickers, n) -> pd.Series:
        """Total return over the last n months."""
        return self.px(tickers) / self.px(tickers, n) - 1

    def ret_skip(self, tickers, n, skip) -> pd.Series:
        """Return from n months ago to `skip` months ago (e.g. 12-1 momentum)."""
        return self.px(tickers, skip) / self.px(tickers, n) - 1

    def mom13612w(self, tickers) -> pd.Series:
        """Keller's fast momentum: 12*r1 + 4*r3 + 2*r6 + 1*r12 (weights favour recent months)."""
        return 12 * self.ret(tickers, 1) + 4 * self.ret(tickers, 3) + 2 * self.ret(tickers, 6) + self.ret(tickers, 12)

    def mom13612u(self, tickers) -> pd.Series:
        """Unweighted average of 1, 3, 6 and 12-month returns."""
        return (self.ret(tickers, 1) + self.ret(tickers, 3) + self.ret(tickers, 6) + self.ret(tickers, 12)) / 4

    def sma(self, tickers, n) -> pd.Series:
        if self.i - n + 1 < 0:
            return pd.Series(np.nan, index=tickers)
        cols = [self._cols[t] for t in tickers]
        return pd.Series(self._mv[self.i - n + 1:self.i + 1, cols].mean(axis=0), index=tickers)

    def sma_rel(self, tickers, n) -> pd.Series:
        """Price relative to its n-month simple moving average, minus 1 (>0 = uptrend)."""
        return self.px(tickers) / self.sma(tickers, n) - 1

    def mret_hist(self, tickers, n) -> pd.DataFrame:
        """Last n monthly returns (rows) up to the current month."""
        lv = self.m[tickers].iloc[max(0, self.i - n):self.i + 1]
        return lv.pct_change().iloc[1:]

    def mvol(self, tickers, n) -> pd.Series:
        return self.mret_hist(tickers, n).std() * np.sqrt(12)

    # -- daily helpers
    def dhist(self, tickers, days) -> pd.DataFrame:
        d = self.d.loc[:self.trade_date, tickers]
        return d.iloc[-(days + 1):]

    def dret(self, tickers, days) -> pd.Series:
        h = self.dhist(tickers, days)
        return h.iloc[-1] / h.iloc[0] - 1

    def dvol(self, tickers, days) -> pd.Series:
        return self.dhist(tickers, days).pct_change().iloc[1:].std() * np.sqrt(252)

    def dcov(self, tickers, days) -> pd.DataFrame:
        return self.dhist(tickers, days).pct_change().iloc[1:].cov() * 252

    def dcorr(self, tickers, days) -> pd.DataFrame:
        return self.dhist(tickers, days).pct_change().iloc[1:].corr()

    def dsma_rel(self, tickers, days) -> pd.Series:
        h = self.dhist(tickers, days - 1)
        return h.iloc[-1] / h.mean() - 1

    def available(self, tickers, months=13) -> list[str]:
        """Tickers with at least `months` of month-end history at the current date."""
        out = []
        for t in tickers:
            k = self._cols[t]
            if self.i - months >= 0 and np.isfinite(self._mv[self.i - months:self.i + 1, k]).all():
                out.append(t)
        return out

    # -- macro (already lagged for publication delays)
    def mac(self, name, lag=0):
        return self.macro[name].iloc[self.macro.index.get_indexer([self.date])[0] - lag]

    def mac_hist(self, name, n) -> pd.Series:
        k = self.macro.index.get_indexer([self.date])[0]
        return self.macro[name].iloc[max(0, k - n + 1):k + 1]


@dataclass
class Result:
    strategy: Strategy
    returns: pd.Series            # monthly net returns, indexed by month-end of the holding month
    weights: pd.DataFrame         # target weights set at each month-end (row t applies to month t+1)
    turnover: pd.Series
    current: dict                 # weights for the month now in progress
    signal_date: pd.Timestamp
    mtd_return: float | None


def _normalize(w: dict) -> dict:
    w = {k: float(v) for k, v in w.items() if abs(v) > 1e-9}
    tot = sum(w.values())
    if not np.isfinite(tot) or abs(tot - 1) > 1e-6:
        raise ValueError(f"weights must sum to 1, got {tot:.6f}: {w}")
    return w


def run(strategy: Strategy, panel, macro: pd.DataFrame | None = None, first_date: str = EVAL_START) -> Result:
    tickers = list(dict.fromkeys(strategy.assets + strategy.optional + [CASH]))
    required = list(dict.fromkeys(strategy.assets + [CASH]))
    M = panel.monthly_frame(tickers)
    D = panel.daily_frame(tickers) if strategy.needs_daily else None
    trade_dates = panel.trade_dates
    grid = trade_dates.index
    M = M.reindex(grid[grid >= M.index[0]])
    partial = panel.partial_month
    R = M.pct_change()

    ctx = Context(M, D, macro, trade_dates)
    lb = strategy.lookback_months
    valid = M[required].notna().all(axis=1).values
    first_ok = None
    min_start = pd.Timestamp(first_date) - pd.offsets.MonthEnd(1)
    if strategy.min_start:
        min_start = max(min_start, pd.Timestamp(strategy.min_start))
    for i in range(lb, len(M)):
        if not valid[i - lb:i + 1].all() or M.index[i] < min_start:
            continue
        if D is not None:
            dd = D.loc[:trade_dates.iloc[i]]
            if len(dd) < 260 or dd[required].iloc[-260:].isna().any().any():
                continue
        first_ok = i
        break
    if first_ok is None:
        raise ValueError(f"{strategy.id}: not enough data")

    last_signal = len(M) - 2 if partial else len(M) - 1
    rets, wrows, tos = {}, {}, {}
    held = None
    rb_months = {"M": set(range(1, 13)), "Q": {3, 6, 9, 12}, "A": {12}}[strategy.rebalance]
    for i in range(first_ok, last_signal + 1):
        ctx.i = i
        dt = M.index[i]
        if held is None or dt.month in rb_months:
            try:
                target = _normalize(strategy.fn(ctx))
            except NotReady:
                if held is None:
                    continue
                raise
            drifted = held or {}
            names = set(target) | set(drifted)
            to = sum(abs(target.get(k, 0) - drifted.get(k, 0)) for k in names)
            if held is None:
                to = sum(abs(v) for v in target.values())
            tos[dt] = to
            wrows[dt] = target
            held = dict(target)
            cost = COST_PER_TRADE * to
        else:
            cost = 0.0
        if i + 1 <= len(M) - 1 and (i + 1 < len(M) - 1 or not partial):
            r_next = R.iloc[i + 1]
            gross = sum(w * r_next[k] for k, w in held.items())
            rets[M.index[i + 1]] = (1 - cost) * (1 + gross) - 1
            # weights drift with prices until the next rebalance
            held = {k: w * (1 + r_next[k]) / (1 + gross) for k, w in held.items()}
        else:
            pending_cost = cost
    current = wrows[M.index[last_signal]] if M.index[last_signal] in wrows else held
    mtd = None
    if partial:
        r_now = R.iloc[-1]
        mtd = float(sum(w * r_now[k] for k, w in current.items()))
    W = pd.DataFrame.from_dict(wrows, orient="index").fillna(0.0)
    return Result(
        strategy=strategy,
        returns=pd.Series(rets, name=strategy.id).astype(float),
        weights=W,
        turnover=pd.Series(tos, name="turnover"),
        current=current,
        signal_date=trade_dates.iloc[last_signal],
        mtd_return=mtd,
    )
