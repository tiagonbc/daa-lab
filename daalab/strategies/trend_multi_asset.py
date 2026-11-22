"""Multi-asset time-series momentum (Hurst, Ooi & Pedersen 2017; Moskowitz, Ooi & Pedersen 2012), built from ETFs.
Rules follow research/strategies_additions.json. Unlike the long-only allocation strategies in the lab, these can
short an asset and use leverage: cash (BIL) takes 1 - sum(weights), so it is negative when the book is levered."""
from __future__ import annotations

import numpy as np

from ..config import CASH
from ..engine.core import register
from .catalog import meta

LOOKBACKS = (1, 3, 12)
POS_VOL, BOOK_VOL, MAX_SCALE, HALF_LIFE, COV_DAYS = 0.10, 0.10, 4.0, 60, 126

TREND_EQ = ["SPY", "IWM", "EFA", "VNQ"]
TREND_EQ_OPT = ["EEM"]                                   # its pre-ETF proxy is monthly only, so it joins with daily data
TREND_RATES_REAL = ["TLT", "IEF", "LQD", "GLD", "SLV", "DBC"]
TREND_LATE = ["TIP", "HYG", "USO", "UUP"]                # used once their ETFs have 13 months of history


def _trend_book(ctx, core: list[str], optional: list[str]) -> dict:
    U = core + [t for t in optional if t in ctx.available([t], 13)]
    h = ctx.dhist(U, 300)
    r = h.pct_change().iloc[1:]
    vol = r.ewm(halflife=HALF_LIFE, min_periods=120).std().iloc[-1] * np.sqrt(252)
    U = [t for t in U if np.isfinite(vol[t]) and vol[t] > 0 and r[t].iloc[-COV_DAYS:].notna().all()]
    if not U:
        return {CASH: 1.0}
    cash = {n: float(ctx.ret([CASH], n)[CASH]) for n in LOOKBACKS}
    sig = sum(np.sign(ctx.ret(U, n) - cash[n]) for n in LOOKBACKS) / len(LOOKBACKS)
    raw = sig * POS_VOL / vol[U] / len(U)
    if (raw.abs() < 1e-12).all():
        return {CASH: 1.0}
    cov = r[U].iloc[-COV_DAYS:].cov().values * 252
    book_vol = float(np.sqrt(raw.values @ cov @ raw.values))
    scale = min(BOOK_VOL / book_vol, MAX_SCALE) if book_vol > 0 else 0.0
    w = {t: float(v) for t, v in (raw * scale).items() if abs(v) > 1e-6}
    w[CASH] = 1.0 - sum(w.values())
    return w


@register(**meta("hop_trend_multi_asset", assets=TREND_EQ + TREND_RATES_REAL + [CASH], optional=TREND_EQ_OPT + TREND_LATE,
                 needs_daily=True, lookback_months=12))
def hop_trend_multi_asset(ctx):
    return _trend_book(ctx, TREND_EQ + TREND_RATES_REAL, TREND_EQ_OPT + TREND_LATE)


@register(**meta("hop_trend_ex_equity", assets=TREND_RATES_REAL + [CASH], optional=TREND_LATE,
                 needs_daily=True, lookback_months=12))
def hop_trend_ex_equity(ctx):
    return _trend_book(ctx, TREND_RATES_REAL, TREND_LATE)
