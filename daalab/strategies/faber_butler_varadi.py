"""Trend-following and risk-based strategies: Meb Faber, Alpha Architect, Adam Butler, David Varadi.

Rules follow research/strategies_others.json; where the source is ambiguous the choice is
documented in each strategy's notes (shown on the website).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from ..engine.core import register
from .catalog import meta
from .keller_antonacci import add, best, min_variance, top


def mom1_3_6_12(ctx, t):
    return (ctx.ret(t, 1) + ctx.ret(t, 3) + ctx.ret(t, 6) + ctx.ret(t, 12)) / 4


# ============================================================================= Faber
IVY = ["SPY", "EFA", "IEF", "VNQ", "DBC"]


@register(**meta("faber_ivy_static", assets=IVY, lookback_months=1, rebalance="A"))
def ivy_static(ctx):
    return {k: 0.2 for k in IVY}


@register(**meta("faber_gtaa5", assets=IVY, lookback_months=10))
def gtaa5(ctx):
    up = ctx.sma_rel(IVY, 10) > 0
    w = {}
    for k in IVY:
        add(w, k if up[k] else "BIL", 0.2)
    return w


GTAA13_W = {"IWD": 0.05, "MTUM": 0.05, "IWN": 0.05, "IWM": 0.05, "EFA": 0.10, "EEM": 0.10, "IEF": 0.05,
            "BWX": 0.05, "LQD": 0.05, "TLT": 0.05, "DBC": 0.10, "GLD": 0.10, "VNQ": 0.20}
GTAA13 = list(GTAA13_W)
GTAA13_CORE = [k for k in GTAA13 if k != "BWX"]


@register(**meta("faber_gtaa13", assets=GTAA13, lookback_months=10))
def gtaa13(ctx):
    up = ctx.sma_rel(GTAA13, 10) > 0
    w = {}
    for k, v in GTAA13_W.items():
        add(w, k if up[k] else "BIL", v)
    return w


def _gtaa_agg(ctx, n):
    U = GTAA13_CORE + ctx.available(["BWX"], 12)
    m = mom1_3_6_12(ctx, U)
    up = ctx.sma_rel(U, 10) > 0
    w = {}
    for k in top(m, n):
        add(w, k if up[k] else "BIL", 1 / n)
    return w


@register(**meta("faber_gtaa_agg3", assets=GTAA13_CORE, optional=["BWX"], lookback_months=12))
def gtaa_agg3(ctx):
    return _gtaa_agg(ctx, 3)


@register(**meta("faber_gtaa_agg6", assets=GTAA13_CORE, optional=["BWX"], lookback_months=12))
def gtaa_agg6(ctx):
    return _gtaa_agg(ctx, 6)


TRINITY_STATIC = {"MTUM": 0.045, "IWD": 0.045, "EFV": 0.0675, "EEM": 0.0225, "LQD": 0.099, "TLT": 0.0675,
                  "BWX": 0.072, "TIP": 0.009, "DBC": 0.025, "GLD": 0.025, "VNQ": 0.0225}


@register(**meta("faber_trinity_lite", assets=list(TRINITY_STATIC), lookback_months=12))
def trinity(ctx):
    ents = ["USEQ", "EFV", "EEM", "LQD", "TLT", "BWX", "TIP", "DBC", "GLD", "VNQ"]
    single = ents[1:]
    m = mom1_3_6_12(ctx, single)
    m["USEQ"] = mom1_3_6_12(ctx, ["MTUM", "IWD"]).mean()
    trend = ctx.sma_rel(single, 10) > 0
    trend["USEQ"] = ctx.sma_rel(["MTUM", "IWD"], 10).mean() > 0
    w = dict(TRINITY_STATIC)
    picks = top(m[ents], 5)
    for e in picks:
        if not trend[e]:
            add(w, "BIL", 0.10)
        elif e == "USEQ":
            add(w, "MTUM", 0.05); add(w, "IWD", 0.05)
        else:
            add(w, e, 0.10)
    if "TIP" not in picks:                # AS 2% minimum-position rule
        w["TLT"] += w.pop("TIP")
    return w


@register(**meta("faber_12m_high_switch", assets=["SPY", "EFA", "VNQ", "GLD", "DBC", "IEF"], lookback_months=12))
def high_switch(ctx):
    U = ["SPY", "EFA", "VNQ", "GLD", "DBC", "IEF"]
    hi = ctx.m[U].iloc[ctx.i - 11:ctx.i + 1].max()
    near = ctx.px(U) >= 0.95 * hi
    w, pool = {}, 0.0
    for k in U[:-1]:
        if near[k]:
            add(w, k, 0.2)
        else:
            pool += 0.2
    add(w, "IEF" if near["IEF"] else "BIL", pool)
    return w


SECTORS = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]


@register(**meta("faber_sector_relative_strength", assets=SECTORS + ["SPY"], lookback_months=12))
def sector_rs(ctx):
    if ctx.sma_rel(["SPY"], 10)["SPY"] < 0:
        return {"BIL": 1.0}
    m = sum(ctx.ret(SECTORS, k) for k in (1, 3, 6, 9, 12)) / 5
    return {k: 1 / 3 for k in top(m, 3)}


@register(**meta("faber_tactical_yield", assets=["IEF", "LQD"], lookback_months=1, macro_inputs=["y10", "y3m", "baa", "aaa"]))
def tactical_yield(ctx):
    k = ctx.macro.index.get_indexer([ctx.date])[0]
    hist = ctx.macro.iloc[:k + 1]
    term = (hist["y10"] - hist["y3m"]).dropna()
    credit = ((hist["baa"] + hist["aaa"]) / 2 - hist["y3m"]).dropna()
    w = {}
    add(w, "IEF" if term.iloc[-1] > term.median() else "BIL", 0.5)
    add(w, "LQD" if credit.iloc[-1] > credit.median() else "BIL", 0.5)
    return w


# ============================================================================= Alpha Architect robust asset allocation
RAA_U = ["IWD", "MTUM", "EFV", "EFA", "VNQ", "DBC", "IEF"]


def _aa_raa(ctx, weights):
    U = list(weights)
    ma = (ctx.sma_rel(U, 12) > 0).astype(float)
    tm = (ctx.ret(U, 12) > ctx.ret(["BIL"], 12)["BIL"]).astype(float)
    w = {}
    for k, v in weights.items():
        e = (ma[k] + tm[k]) / 2
        add(w, k, v * e)
        add(w, "BIL", v * (1 - e))
    return w


@register(**meta("alphaarchitect_raa_balanced", assets=RAA_U, lookback_months=12))
def aa_raa_bal(ctx):
    return _aa_raa(ctx, {"IWD": 0.10, "MTUM": 0.10, "EFV": 0.10, "EFA": 0.10, "VNQ": 0.10, "DBC": 0.10, "IEF": 0.40})


@register(**meta("alphaarchitect_raa_aggressive", assets=RAA_U, lookback_months=12))
def aa_raa_agg(ctx):
    return _aa_raa(ctx, {"IWD": 0.15, "MTUM": 0.15, "EFV": 0.15, "EFA": 0.15, "VNQ": 0.10, "DBC": 0.10, "IEF": 0.20})


# ============================================================================= Butler / ReSolve
AAA_CORE = ["SPY", "VGK", "EWJ", "EEM", "VNQ", "IEF", "TLT", "DBC", "GLD"]


@register(**meta("butler_adaptive_asset_allocation", assets=AAA_CORE, optional=["RWX"], needs_daily=True, lookback_months=7))
def butler_aaa(ctx):
    U = AAA_CORE + [t for t in ["RWX"] if ctx.dhist([t], 130)[t].notna().all()]
    n = len(U) // 2
    m = ctx.dret(U, 126)
    picks = top(m, n)
    h = ctx.dhist(picks, 126).pct_change().iloc[1:]
    vol = h.iloc[-20:].std()
    cov = h.corr() * np.outer(vol, vol)
    w = min_variance(cov)
    w = w[w >= 0.02]
    return (w / w.sum()).to_dict()


@register(**meta("butler_tactical_permanent_portfolio", assets=["SPY", "IEF", "GLD"], needs_daily=True, lookback_months=11))
def butler_tpp(ctx):
    U = ["SPY", "IEF", "GLD"]
    h = ctx.dhist(U, 201).iloc[:-1]          # signals as of the day BEFORE the last trading day
    keep = [k for k in U if h[k].iloc[-1] > h[k].iloc[-200:].mean()]
    if not keep:
        return {"BIL": 1.0}
    r = h[keep].pct_change().iloc[1:]
    iv = 1 / r.iloc[-21:].std()
    w = iv / iv.sum()
    vol = float(np.sqrt(252 * w.values @ r.iloc[-60:].cov().values @ w.values))
    scale = min(1.0, 0.07 / vol) if vol > 0 else 1.0
    out = (w * scale).to_dict()
    add(out, "BIL", 1 - scale)
    return out


# ============================================================================= Varadi
MINCORR_U = ["SPY", "QQQ", "IWM", "EEM", "EFA", "TLT", "VNQ", "GLD"]


@register(**meta("varadi_minimum_correlation", assets=MINCORR_U, needs_daily=True, lookback_months=4))
def mincorr(ctx):
    r = ctx.dhist(MINCORR_U, 60).pct_change().iloc[1:]
    C = r.corr().values
    sig = r.std().values
    n = len(MINCORR_U)
    off = C[~np.eye(n, dtype=bool)]
    A = 1 - norm.cdf(C, off.mean(), off.std())
    np.fill_diagonal(A, 0)
    a = A.sum(axis=1) / (n - 1)
    ranks = pd.Series(a).rank(ascending=False).values      # most correlated (lowest a) -> largest rank
    q = ranks / ranks.sum()
    v = q @ A
    v = v / v.sum()
    w = (v / sig) / (v / sig).sum()
    return dict(zip(MINCORR_U, w))


PC_U = ["SPY", "VNQ", "LQD", "DBC"]


def _channel_states(d: pd.DataFrame) -> pd.DataFrame:
    """Daily percentile-channel score in [-1, 1] for each asset (average of 4 lookbacks, with hysteresis)."""
    out = pd.DataFrame(0.0, index=d.index, columns=d.columns)
    for L in (60, 120, 180, 252):
        up = d.rolling(L).quantile(0.75)
        lo = d.rolling(L).quantile(0.25)
        sig = pd.DataFrame(np.where(d > up, 1.0, np.where(d < lo, -1.0, np.nan)), index=d.index, columns=d.columns)
        out += sig.ffill().fillna(0.0)
    return out / 4


@register(**meta("varadi_percentile_channels", assets=PC_U, needs_daily=True, lookback_months=13))
def pct_channels(ctx):
    if "pc" not in ctx.state:
        ctx.state["pc"] = _channel_states(ctx.d[PC_U])   # each day's state uses only data up to that day
    score = ctx.state["pc"].loc[:ctx.trade_date].iloc[-1]
    vol = ctx.dhist(PC_U, 20).pct_change().iloc[1:].std()
    c = score / vol
    w = c.abs() / c.abs().sum() if c.abs().sum() > 0 else c * 0
    w[score <= 0] = 0
    out = {k: float(v) for k, v in w.items() if v > 0}
    add(out, "BIL", 1 - sum(out.values()))
    return out


POS = {"XLE": 0.5, "XLI": 1 / 6, "XLF": 1 / 6, "XLB": 1 / 6}
NEG = {"XLU": 1 / 3, "XLV": 1 / 3, "XLP": 1 / 3}
INFL_U = list(dict.fromkeys(list(POS) + list(NEG) + ["SPY", "XLK"]))


def _sector_inflation_ratio(ctx, days):
    h = ctx.dhist(list(POS) + list(NEG), days)
    rel = h / h.iloc[0]
    pos = sum(v * rel[k] for k, v in POS.items())
    neg = sum(v * rel[k] for k, v in NEG.items())
    return pos / neg


@register(**meta("varadi_growth_inflation_sector_timing", assets=INFL_U, needs_daily=True, lookback_months=11,
                 notes="Original rules switch on any day the regime changes; here the regime is evaluated at month-end only "
                       "(monthly approximation). The turnover-reduction AllocateSmartly agreed with the author is not public."))
def gi_sector(ctx):
    spy = ctx.dhist(["SPY"], 200)["SPY"]
    growth_up = spy.iloc[-1] > spy.iloc[-200:].mean()
    R = _sector_inflation_ratio(ctx, 200)
    infl_up = R.iloc[-1] > R.median()
    return {("XLE" if infl_up else "XLK") if growth_up else ("XLV" if infl_up else "XLP"): 1.0}


def _compass(ctx, sma_days, be_level, be_days, reg_days):
    spy = ctx.dhist(["SPY"], sma_days)["SPY"]
    growth_up = spy.iloc[-1] > spy.iloc[-sma_days:].mean()
    be = ctx.state["be"].loc[:ctx.trade_date].dropna()
    be_ok = be.iloc[-1] > be_level
    be_mom = be.iloc[-1] > be.iloc[-1 - be_days]
    R = _sector_inflation_ratio(ctx, reg_days).values
    slope = np.polyfit(np.arange(len(R)), R, 1)[0]
    infl = be_ok and (be_mom or slope > 0)
    return growth_up, infl


def _load_be(ctx):
    if "be" not in ctx.state:
        from ..data.sources import fred
        ctx.state["be"] = fred("T5YIE")


@register(**meta("varadi_inflation_compass_original", assets=INFL_U + ["IEF"], needs_daily=True, lookback_months=11,
                 macro_inputs=["T5YIE (FRED)"], min_start="2003-06-30"))
def compass_orig(ctx):
    _load_be(ctx)
    g, i = _compass(ctx, 200, 2.0, 60, 60)
    if g:
        return {"XLE": 1.0} if i else {"XLK": 1.0}
    return {"XLU": 1.0} if i else {"XLP": 0.5, "IEF": 0.5}


@register(**meta("varadi_inflation_compass_enhanced", assets=INFL_U + ["IEF", "QQQ", "DBC"], needs_daily=True, lookback_months=13,
                 macro_inputs=["T5YIE (FRED)"], min_start="2003-06-30"))
def compass_enh(ctx):
    _load_be(ctx)
    spy = ctx.dhist(["SPY"], 252)["SPY"]
    be = ctx.state["be"].loc[:ctx.trade_date].dropna()
    h = ctx.dhist(list(POS) + list(NEG), 80)
    w = {}
    combos = [(s_, lv, bd, rd) for s_ in (100, 150, 200, 252) for lv in (1.8, 2.0, 2.2) for bd in (40, 60, 80) for rd in (40, 60, 80)]
    slopes = {}
    for rd in (40, 60, 80):
        hh = h.iloc[-(rd + 1):]
        rel = hh / hh.iloc[0]
        R = (sum(v * rel[k] for k, v in POS.items()) / sum(v * rel[k] for k, v in NEG.items())).values
        slopes[rd] = np.polyfit(np.arange(len(R)), R, 1)[0]
    for sma_days, lv, bd, rd in combos:
        g = spy.iloc[-1] > spy.iloc[-sma_days:].mean()
        i = be.iloc[-1] > lv and (be.iloc[-1] > be.iloc[-1 - bd] or slopes[rd] > 0)
        alloc = ({"XLE": 1.0} if i else {"QQQ": 1.0}) if g else ({"XLU": 0.5, "DBC": 0.5} if i else {"XLP": 0.5, "IEF": 0.5})
        for k, v in alloc.items():
            add(w, k, v / len(combos))
    return w
