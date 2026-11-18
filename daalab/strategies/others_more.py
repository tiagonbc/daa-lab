"""Remaining published strategies tracked or reviewed by AllocateSmartly: macro/survey timing, channel and
seasonality rules, static 'lazy' portfolios and a few cross-asset signals. Rules follow
research/strategies_others.json; deviations are noted per strategy."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from ..data import sources as src
from ..engine.core import register
from .catalog import meta
from .keller_antonacci import add, best, top


def _mom_avg(ctx, t, ks=(1, 3, 6, 12)):
    return sum(ctx.ret(t, k) for k in ks) / len(ks)


def _monthly_index(ctx, key, symbol):
    """Month-end levels of a Norgate index (price, not total return), cached per run."""
    if key not in ctx.state:
        s = src.norgate_close(symbol, total_return=False)
        m = s.groupby(s.index.to_period("M")).last()
        m.index = m.index.to_timestamp(how="end").normalize()
        ctx.state[key] = m
    return ctx.state[key].loc[:ctx.date]


# ============================================================================= Garg et al.: momentum turning points
GARG = ["SPY", "EFA", "IEF", "BWX", "DBC", "GLD"]


def _garg_states(x: pd.Series, fast: int) -> pd.Series:
    slow = x.rolling(12).mean() >= 0
    fst = x.rolling(fast).mean() >= 0
    st = pd.Series(np.where(slow & fst, "Bu", np.where(slow & ~fst, "Co", np.where(~slow & ~fst, "Be", "Re"))), index=x.index)
    return st.where(x.rolling(12).count() == 12)


def _garg_speeds(x: pd.Series, fast: int):
    st = _garg_states(x, fast)
    nxt = x.shift(-1)
    df = pd.DataFrame({"s": st, "r": nxt}).dropna()
    if len(df) < 60 or df["s"].value_counts().min() < 6 or df["s"].nunique() < 4:
        return 0.5, 0.5
    g = lambda s: df.loc[df["s"] == s, "r"]
    bube = df.loc[df["s"].isin(["Bu", "Be"]), "r"]
    C = (len(g("Bu")) / len(bube)) * g("Bu").mean() / (bube ** 2).mean() - (len(g("Be")) / len(bube)) * g("Be").mean() / (bube ** 2).mean()
    if C <= 0:
        return 0.5, 0.5
    a_co = 0.5 * (1 - (1 / C) * g("Co").mean() / (g("Co") ** 2).mean())
    a_re = 0.5 * (1 + (1 / C) * g("Re").mean() / (g("Re") ** 2).mean())
    return float(np.clip(a_co, 0, 1)), float(np.clip(a_re, 0, 1))


@register(**meta("garg_momentum_turning_points", assets=GARG, lookback_months=12,
                 notes="Speeds are re-estimated every 5 years on each asset's own history available in the lab (from 1988-1991 "
                       "for most assets); with too little history the neutral speed 0.5 is used."))
def garg(ctx):
    ex = ctx.m[GARG + ["BIL"]].iloc[:ctx.i + 1].pct_change()
    ex = ex[GARG].sub(ex["BIL"], axis=0)
    sp = ctx.state.setdefault("speeds", {})
    if "asof" not in ctx.state or (ctx.date - ctx.state["asof"]).days > 5 * 365:
        for t in GARG:
            sp[t] = _garg_speeds(ex[t].dropna().iloc[:-1], 2)
        ctx.state["asof"] = ctx.date
    w = {}
    for t in GARG:
        s = _garg_states(ex[t].dropna(), 2).iloc[-1]
        a_co, a_re = sp[t]
        pos = {"Bu": 1.0, "Be": -1.0, "Co": 1 - 2 * a_co, "Re": 2 * a_re - 1}[s]
        pos = max(0.0, pos)
        if pos * (1 / 6) >= 0.02:
            add(w, t, pos / 6)
    add(w, "BIL", 1 - sum(w.values()))
    return w


# ============================================================================= Baltussen et al.: predicting bond returns
@register(**meta("baltussen_predicting_bond_returns", assets=["IEF", "DBC"], lookback_months=12, macro_inputs=["y10", "y3m"]))
def baltussen(ctx):
    def z(s):
        s = s.dropna().iloc[-120:]
        return (s.iloc[-1] - s.mean()) / s.std() if len(s) >= 60 else np.nan

    hist = ctx.m.iloc[:ctx.i + 1]
    r12 = hist / hist.shift(12) - 1
    k = ctx.macro.index.get_indexer([ctx.date])[0]
    ys = np.clip(z(ctx.macro["y10"].iloc[:k + 1] - ctx.macro["y3m"].iloc[:k + 1]), -1, 1)
    bt = 1.0 if r12["IEF"].iloc[-1] - r12["BIL"].iloc[-1] > 0 else -1.0
    spx = _monthly_index(ctx, "spx", "$SPX")
    eq_x = (spx / spx.shift(12) - 1).reindex(r12.index) - r12["BIL"]
    eq = np.clip(-z(eq_x), -1, 1)
    cm = np.clip(-z(r12["DBC"]), -1, 1)
    sig = [v for v in (ys, bt, eq, cm) if np.isfinite(v)]
    final = (np.mean(sig) + 1) / 2
    return {"IEF": final, "BIL": 1 - final} if final < 1 else {"IEF": 1.0}


# ============================================================================= Survey of Professional Forecasters
@register(**meta("sun_spf_recession_probability", assets=["SPY", "IEF"], lookback_months=1))
def spf_recession(ctx):
    if "spf" not in ctx.state:
        ctx.state["spf"] = (src.spf("RECESS"), src.spf("TBOND"))
    rec, tb = ctx.state["spf"]
    # survey for quarter q is usable from the end of the 2nd month of q
    avail = pd.DatetimeIndex([(p.asfreq("M", "s") + 1).to_timestamp(how="end").normalize() for p in rec.index])
    q = int((avail <= ctx.date).sum()) - 1
    now, prev = rec.iloc[q], rec.iloc[q - 1]
    risk_on = now[["RECESS2", "RECESS3", "RECESS4"]].mean() <= prev[["RECESS3", "RECESS4", "RECESS5"]].mean()
    tq, tp = tb.loc[rec.index[q]], tb.loc[rec.index[q - 1]]
    bond_on = tq[["TBOND3", "TBOND4", "TBOND5"]].mean() <= tp[["TBOND4", "TBOND5", "TBOND6"]].mean()
    dfn = "IEF" if bond_on else "BIL"
    if risk_on:
        w = {"SPY": 0.6}
        add(w, dfn, 0.4)
        return w
    return {dfn: 1.0}


# ============================================================================= Movement Capital composite
@register(**meta("movementcapital_composite", assets=["SPY", "EFA", "IEF", "TIP", "SHV"], lookback_months=15,
                 macro_inputs=["real_retail_yoy", "indpro_yoy", "unemp"]))
def movement(ctx):
    U = ["SPY", "EFA", "SHV"]
    m = sum(ctx.ret(U, k) for k in (3, 6, 9, 12, 15)) / 5
    win = best(m[["SPY", "EFA"]])
    w = {}
    add(w, win if m[win] > m["SHV"] else "IEF", 0.25)
    ue = ctx.mac_hist("unemp", 12)
    signals = int(ctx.mac("real_retail_yoy") < 0) + int(ctx.mac("indpro_yoy") < 0) + int(ue.iloc[-1] > ue.mean())
    if signals < 2:
        add(w, "SPY", 0.125); add(w, "EFA", 0.125)
    else:
        add(w, "IEF", 0.25)
    add(w, "SPY", 0.125); add(w, "EFA", 0.125)
    add(w, "IEF", 0.125); add(w, "TIP", 0.125)
    return w


# ============================================================================= Stoken Active Combined Asset (monthly version)
STOKEN = [("SPY", "IEF", 6, 12), ("GLD", "TLT", 12, 6), ("VNQ", "IEF", 6, 12)]


@register(**meta("stoken_active_combined_asset_monthly", assets=["SPY", "GLD", "VNQ", "IEF", "TLT"], lookback_months=13,
                 notes="Slices are reset to 1/3 every month (the original only rebalances on a signal change or at year-end)."))
def stoken(ctx):
    st = ctx.state.setdefault("risk", {r: True for r, *_ in STOKEN})
    w = {}
    for risk, safe, k_up, k_lo in STOKEN:
        p = ctx.px([risk])[risk]
        prev = ctx.m[risk].iloc[ctx.i - max(k_up, k_lo):ctx.i]
        upper, lower = prev.iloc[-k_up:].max(), prev.iloc[-k_lo:].min()
        if st[risk] and p < lower:
            st[risk] = False
        elif not st[risk] and p > upper:
            st[risk] = True
        add(w, risk if st[risk] else safe, 1 / 3)
    return w


# ============================================================================= J.P. Morgan Efficiente (as replicated by AllocateSmartly)
EFF = ["SPY", "IWM", "EFA", "EEM", "VNQ", "DBC", "GLD", "HYG", "EMB", "LQD", "TLT", "TIP", "BIL"]
EFF_CAP = {"SPY": .2, "IWM": .1, "EFA": .2, "TLT": .2, "LQD": .2, "HYG": .2, "EEM": .2, "EMB": .2, "VNQ": .2, "DBC": .1,
           "GLD": .1, "TIP": .5, "BIL": .5}
EFF_GROUPS = [(["SPY", "IWM", "EFA"], .5), (["TLT", "LQD", "HYG"], .5), (["EEM", "EMB"], .25), (["VNQ", "DBC", "GLD"], .25),
              (["TIP", "BIL"], .5)]


@register(**meta("jpm_efficiente_index", assets=EFF[:-1], needs_daily=True, lookback_months=7))
def efficiente(ctx):
    r = ctx.dhist(EFF, 126).pct_change().iloc[1:]
    mu, S = r.mean().values * 252, r.cov().values * 252
    n = len(EFF)
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}, {"type": "ineq", "fun": lambda w: 0.10 ** 2 - w @ S @ w}]
    for names, cap in EFF_GROUPS:
        idx = [EFF.index(k) for k in names]
        cons.append({"type": "ineq", "fun": lambda w, idx=idx, cap=cap: cap - w[idx].sum()})
    bounds = [(0, EFF_CAP[k]) for k in EFF]
    x0 = np.zeros(n); x0[EFF.index("BIL")] = .5; x0[EFF.index("TIP")] = .5
    res = minimize(lambda w: -(w @ mu), x0, method="SLSQP", bounds=bounds, constraints=cons, options={"ftol": 1e-10, "maxiter": 500})
    w = pd.Series(np.clip(res.x if res.success else x0, 0, None), index=EFF)
    w = w[w >= 0.02]
    return (w / w.sum()).to_dict()


# ============================================================================= Defense First, HAA 60/40, Choi
@register(**meta("carlson_defense_first", assets=["SPY", "TLT", "GLD", "DBC", "UUP"], lookback_months=12))
def defense_first(ctx):
    D = ["TLT", "GLD", "DBC", "UUP"]
    m = _mom_avg(ctx, D + ["BIL"])
    w = {}
    for k, slot in zip(top(m[D], 4), (0.4, 0.3, 0.2, 0.1)):
        add(w, k if m[k] >= m["BIL"] else "SPY", slot)
    return w


@register(**meta("nlx_haa_60_40", assets=["SPY", "IEF", "TIP"], lookback_months=12))
def haa_6040(ctx):
    m = _mom_avg(ctx, ["TIP", "SPY", "IEF", "BIL"])
    if m["TIP"] > 0 and m["SPY"] > 0:
        return {"SPY": 0.6, "IEF": 0.4}
    return {"IEF": 1.0} if m["IEF"] > m["BIL"] else {"BIL": 1.0}


@register(**meta("choi_dividend_growth_allocation", assets=["QQQ", "SCHD", "TLT", "DBC", "TIP"], lookback_months=15,
                 macro_inputs=["y10", "y3m"],
                 notes="S&P 500 dividend yield is derived from Norgate's S&P 500 total-return vs price index (trailing 12 months), lagged one month."))
def choi(ctx):
    tip_ok = ctx.sma_rel(["TIP"], 12)["TIP"] > 0
    spx, tr = _monthly_index(ctx, "spx", "$SPX"), _monthly_index(ctx, "spxtr", "$SPXTR")
    dy = ((tr / tr.shift(12)) / (spx / spx.shift(12)) - 1).iloc[-2]          # previous month (1-month lag)
    k = ctx.macro.index.get_indexer([ctx.date])[0]
    curve = (ctx.macro["y10"] - ctx.macro["y3m"]).iloc[k - 15:k - 6]
    curve_ok = not (curve < -0.5).any()
    if tip_ok and dy >= 0.016 and curve_ok:
        m = _mom_avg(ctx, ["QQQ", "SCHD"], (1, 3, 6, 9, 12))
        return {best(m): 1.0}
    m = ctx.sma_rel(["BIL", "TLT", "DBC"], 6)
    b = best(m)
    return {b: 1.0} if m[b] > 0 else {"BIL": 1.0}


# ============================================================================= switching rules
@register(**meta("glenn_paired_switching", assets=["SPY", "TLT"], lookback_months=3, rebalance="Q"))
def paired(ctx):
    return {best(ctx.ret(["SPY", "TLT"], 3)): 1.0}


QUINT = ["SPY", "QQQ", "EFA", "EEM", "TLT"]


@register(**meta("glenn_quint_switching_filtered", assets=QUINT + ["IEF"], lookback_months=3))
def quint(ctx):
    r = ctx.ret(QUINT, 3)
    return {"IEF": 1.0} if (r < 0).any() else {best(r): 1.0}


VIRAG = ["SPY", "IWM", "XLB", "EFA", "EEM", "VNQ", "IEF", "TLT", "TIP"]


@register(**meta("virag_momentum_based_balancing", assets=VIRAG, lookback_months=3))
def virag(ctx):
    r = ctx.ret(VIRAG, 3)
    r["BIL"] = 0.0
    base = r.sort_values().iloc[1]
    s = (r - base).clip(lower=0)
    if s.sum() <= 0:
        return {"BIL": 1.0}
    return (s / s.sum()).to_dict()


# ============================================================================= calendar strategies
@register(**meta("piard_annual_seasonality", assets=["EWS", "EWZ", "EWG"], lookback_months=1))
def piard(ctx):
    m = (ctx.date + pd.offsets.MonthEnd(1)).month          # the month being held
    w = {}
    if m in (11, 12, 1, 2, 3, 4):
        add(w, "EWS", 0.25); add(w, "EWZ", 0.25)
    else:
        add(w, "BIL", 0.5)
    add(w, "EWG" if m in (10, 11, 12, 3, 4) else "BIL", 0.5)
    return w


@register(**meta("sell_in_may_halloween", assets=["SPY"], lookback_months=1))
def halloween(ctx):
    m = (ctx.date + pd.offsets.MonthEnd(1)).month
    return {"SPY": 1.0} if m in (11, 12, 1, 2, 3, 4) else {"BIL": 1.0}


# ============================================================================= static 'lazy' portfolios
@register(**meta("dalio_all_weather", assets=["SPY", "TLT", "IEF", "GLD", "DBC"], lookback_months=1, rebalance="A"))
def all_weather(ctx):
    return {"SPY": 0.30, "TLT": 0.40, "IEF": 0.15, "GLD": 0.075, "DBC": 0.075}


@register(**meta("browne_permanent_portfolio", assets=["SPY", "TLT", "GLD"], lookback_months=1, rebalance="A"))
def permanent(ctx):
    return {"SPY": 0.25, "TLT": 0.25, "GLD": 0.25, "BIL": 0.25}


@register(**meta("portfoliocharts_golden_butterfly", assets=["SPY", "IWN", "TLT", "SHY", "GLD"], lookback_months=1, rebalance="A"))
def golden_butterfly(ctx):
    return {k: 0.2 for k in ["SPY", "IWN", "TLT", "SHY", "GLD"]}


# ============================================================================= reviewed by AllocateSmartly (not tracked)
def _trend_state_daily(d: pd.Series, n=200, k=5) -> pd.Series:
    """Up/down trend with a 5-day confirmation (flips after k consecutive closes on the other side of the SMA)."""
    above = (d > d.rolling(n).mean()).astype(int)
    runs_up = above.groupby((above != above.shift()).cumsum()).cumcount() + 1
    state = pd.Series(np.nan, index=d.index)
    state[(above == 1) & (runs_up >= k)] = 1.0
    state[(above == 0) & (runs_up >= k)] = 0.0
    return state.ffill().fillna(1.0)


@register(**meta("as_countercyclical_trend", assets=["SPY", "IWN", "GLD", "LQD", "IEF"], needs_daily=True, lookback_months=12,
                 macro_inputs=["baa_spread", "y10", "y1"],
                 notes="Credit spread = Moody's Baa yield minus the 10-year Treasury throughout (FRED's high-yield OAS history is "
                       "no longer public); macro data read at the month-end close rather than 2 days earlier; the daily trend "
                       "overlay is applied at month-ends only."))
def countercyclical(ctx):
    k = ctx.macro.index.get_indexer([ctx.date])[0]
    hist = ctx.macro.iloc[max(0, k - 119):k + 1]
    hy, slope = hist["baa_spread"], hist["y10"] - hist["y1"]
    if hy.iloc[-1] > hy.median():
        port = {"SPY": 0.5, "IWN": 0.4, "GLD": 0.1}
    elif slope.iloc[-1] < slope.median():
        port = {"SPY": 0.5, "IWN": 0.1, "GLD": 0.4}
    else:
        port = {"LQD": 0.5, "IEF": 0.4, "IWN": 0.1}
    if "trend" not in ctx.state:
        ctx.state["trend"] = {t: _trend_state_daily(ctx.d[t].dropna()) for t in ("SPY", "GLD")}
    w = {}
    for t, v in port.items():
        up = t not in ("SPY", "GLD") or ctx.state["trend"][t].loc[:ctx.trade_date].iloc[-1] == 1.0
        add(w, t if up else "IEF", v)
    return w


@register(**meta("jpm_trending_fast_slow", assets=["SPY"], needs_daily=True, lookback_months=12))
def fast_slow(ctx):
    spx = _monthly_index(ctx, "spx", "$SPX")
    vol = np.log(ctx.dhist(["SPY"], 21)["SPY"]).diff().std() * np.sqrt(252)
    mom = spx.iloc[-1] / spx.iloc[-2 if vol >= 0.17 else -13] - 1
    return {"SPY": 1.0} if mom > 0 else {"BIL": 1.0}


@register(**meta("econompic_faber_global_ath", assets=["ACWI", "AGG"], lookback_months=12))
def global_ath(ctx):
    h = ctx.m["ACWI"].iloc[:ctx.i + 1].dropna()
    return {"ACWI": 1.0} if h.iloc[-1] >= h.iloc[:-1].max() else {"AGG": 1.0}


@register(**meta("as_dist_1yr_high", assets=["SPY"], lookback_months=12))
def dist_high(ctx):
    h = ctx.m["SPY"].iloc[ctx.i - 12:ctx.i + 1]
    d = (h.iloc[-1] - h.min()) / (h.max() - h.min())
    return {"SPY": 1.0} if (h.iloc[-1] / h.iloc[0] - 1 > 0 and d >= 0.75) else {"BIL": 1.0}


@register(**meta("bilello_gayed_utilities", assets=["VTI", "XLU"], lookback_months=1,
                 notes="Monthly approximation of the weekly rule: compares the last month's returns at month-end."))
def utilities(ctx):
    r = ctx.ret(["VTI", "XLU"], 1)
    return {"XLU": 1.0} if r["XLU"] > r["VTI"] else {"VTI": 1.0}


COMM = ["DBA", "DBB", "DBE", "DBP"]


def _avg_corr(ctx, days):
    c = ctx.dcorr(COMM, days).values
    return c[~np.eye(len(COMM), dtype=bool)].mean()


@register(**meta("quantpedia_commodity_mom_rev_corr", assets=COMM, needs_daily=True, lookback_months=12,
                 notes="Long/short at +/-25% per ETF with the remaining capital in T-bills."))
def comm_momrev(ctx):
    r = ctx.ret(COMM, 12).sort_values(ascending=False, kind="stable")
    regime_mom = _avg_corr(ctx, 20) > _avg_corr(ctx, 250)
    longs, shorts = (list(r.index[:2]), list(r.index[2:])) if regime_mom else (list(r.index[2:]), list(r.index[:2]))
    w = {k: 0.25 for k in longs}
    w.update({k: -0.25 for k in shorts})
    w["BIL"] = 1.0
    return w


@register(**meta("quantpedia_commodity_frontrun_seasonality", assets=COMM, needs_daily=True, lookback_months=12,
                 notes="Long-only version with the correlation filter (AllocateSmartly's test #3); percentile uses the last 12 monthly returns."))
def comm_season(ctx):
    if _avg_corr(ctx, 20) > _avg_corr(ctx, 250):
        return {"BIL": 1.0}
    h = ctx.mret_hist(COMM, 12)
    w = {}
    for t in COMM:
        x = h[t]
        s = x.iloc[-11]                                  # same calendar month as the month being positioned for, a year ago
        add(w, t if (x <= s).mean() >= 0.5 else "BIL", 0.25)
    return w


COUNTRIES = ["SPY", "EWU", "EWG", "EWQ", "EWI", "EWD", "EWN", "EWP", "EWK", "EWL", "EWC", "EWJ", "EWW", "EWM", "EWA", "EWS",
             "EWY", "EWT", "EWZ", "EWH", "EZA", "FXI", "INDY"]
CORE_C = ["SPY", "EWU", "EWG", "EWQ", "EWI", "EWD", "EWN", "EWP", "EWL", "EWC", "EWJ", "EWW", "EWM", "EWA", "EWS", "EWH"]


@register(**meta("quantpedia_country_frontrun_seasonality", assets=CORE_C, optional=[c for c in COUNTRIES if c not in CORE_C],
                 lookback_months=12))
def country_season(ctx):
    U = CORE_C + ctx.available([c for c in COUNTRIES if c not in CORE_C], 12)
    r = ctx.m[U].iloc[ctx.i - 11:ctx.i - 9]
    score = r.iloc[1] / r.iloc[0] - 1                    # return in month t-10
    wts = np.array([6, 6, 6, 5, 4, 3, 2, 1]) / 33
    return dict(zip(top(score, 8), wts))
