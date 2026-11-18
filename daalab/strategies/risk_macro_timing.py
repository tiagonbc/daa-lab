"""Risk-based portfolios, macro-trend timing and other single-signal strategies
(AllocateSmartly in-house, Livingston, Philosophical Economics, Novell, Quantpedia, Zakamulin,
Pitkajarvi et al., Clare et al.). Rules follow research/strategies_others.json."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

from ..engine.core import register
from .catalog import meta
from .keller_antonacci import add, best, top


# ----------------------------------------------------------------------------- portfolio maths
def _solve(obj, n, cons=(), bounds=None, x0=None):
    x0 = np.full(n, 1 / n) if x0 is None else x0
    res = minimize(obj, x0, method="SLSQP", bounds=bounds or [(0, None)] * n, constraints=list(cons),
                   options={"ftol": 1e-12, "maxiter": 1000})
    return np.clip(res.x, 0, None)


def max_diversification(cov: pd.DataFrame) -> pd.Series:
    S, sig = cov.values, np.sqrt(np.diag(cov.values))
    y = _solve(lambda y: y @ S @ y, len(sig), [{"type": "eq", "fun": lambda y: sig @ y - 1}])
    return pd.Series(y / y.sum(), index=cov.index)


def equal_risk_contribution(cov: pd.DataFrame) -> pd.Series:
    S = cov.values
    n = len(S)
    y = _solve(lambda y: 0.5 * y @ S @ y - np.log(np.maximum(y, 1e-12)).sum() / n, n, bounds=[(1e-8, None)] * n,
               x0=1 / np.sqrt(np.diag(S)))
    return pd.Series(y / y.sum(), index=cov.index)


def max_sharpe(mu: pd.Series, cov: pd.DataFrame, rf: float) -> pd.Series:
    ex = (mu - rf).values
    S = cov.values
    if (ex <= 0).all():   # no asset beats cash: fall back to minimum variance (source silent on this case)
        y = _solve(lambda y: y @ S @ y, len(ex), [{"type": "eq", "fun": lambda y: y.sum() - 1}])
    else:
        y = _solve(lambda y: y @ S @ y, len(ex), [{"type": "eq", "fun": lambda y: ex @ y - 1}])
    return pd.Series(y / y.sum(), index=mu.index)


def min_correlation(rets: pd.DataFrame) -> pd.Series:
    """Varadi's Minimum Correlation Algorithm."""
    C, sig, n = rets.corr().values, rets.std().values, rets.shape[1]
    off = C[~np.eye(n, dtype=bool)]
    A = 1 - norm.cdf(C, off.mean(), off.std())
    np.fill_diagonal(A, 0)
    ranks = pd.Series(A.sum(axis=1) / (n - 1)).rank(ascending=False).values
    v = (ranks / ranks.sum()) @ A
    v = v / v.sum()
    w = (v / sig) / (v / sig).sum()
    return pd.Series(w, index=rets.columns)


US4 = ["SPY", "IEF", "LQD", "VNQ"]


@register(**meta("as_max_diversification", assets=US4, lookback_months=36))
def as_maxdiv(ctx):
    return max_diversification(ctx.mret_hist(US4, 36).cov()).to_dict()


@register(**meta("as_equal_risk_contribution", assets=US4, lookback_months=36))
def as_erc(ctx):
    return equal_risk_contribution(ctx.mret_hist(US4, 36).cov()).to_dict()


@register(**meta("as_max_sharpe", assets=US4, lookback_months=36,
                 notes="Expected return = mean monthly return over each window; cash rate = T-bill return over the same window; "
                       "if no asset beats cash, the minimum-variance portfolio is used."))
def as_maxsharpe(ctx):
    w = 0
    for L in (36, 12):
        h = ctx.mret_hist(US4 + ["BIL"], L)
        w = w + 0.5 * max_sharpe(h[US4].mean(), h[US4].cov(), h["BIL"].mean())
    return w.to_dict()


@register(**meta("as_us_min_correlation", assets=US4, lookback_months=36))
def as_mincorr(ctx):
    return min_correlation(ctx.mret_hist(US4, 36)).to_dict()


# ----------------------------------------------------------------------------- dual momentum variants
@register(**meta("newfound_diversified_dual_momentum", assets=["SPY", "EFA", "AGG"], lookback_months=12))
def newfound_ddm(ctx):
    w = {}
    for L in range(6, 13):
        r = ctx.ret(["SPY", "EFA", "BIL"], L)
        add(w, best(r[["SPY", "EFA"]]) if r["SPY"] > r["BIL"] else "AGG", 1 / 7)
    return w


MAMA = ["SPY", "IWM", "EFA", "EEM", "VNQ", "DBC", "GLD", "TLT"]


@register(**meta("livingston_mama_bear", assets=MAMA, lookback_months=5))
def mama_bear(ctx):
    r = ctx.ret(MAMA + ["BIL"], 5)
    return {k: 1 / 3 for k in top(r, 3)}


PAPA = ["IWF", "IWD", "IWO", "IWN", "EFA", "EEM", "VNQ", "DBC", "GLD", "TLT", "IEF", "LQD", "BNDX"]


@register(**meta("livingston_papa_bear", assets=PAPA, lookback_months=12))
def papa_bear(ctx):
    s = (ctx.ret(PAPA, 3) + ctx.ret(PAPA, 6) + ctx.ret(PAPA, 12)) / 3
    return {k: 1 / 3 for k in top(s, 3)}


# ----------------------------------------------------------------------------- growth-trend timing
def _trend_up(ctx, t="SPY", n=10):
    return ctx.sma_rel([t], n)[t] > 0


@register(**meta("philoeconomics_growth_trend_timing", assets=["SPY"], lookback_months=10,
                 macro_inputs=["real_retail_yoy", "indpro_yoy"],
                 notes="Real retail sales growth = nominal retail sales growth minus CPI inflation (Norgate), a close stand-in for FRED RRSFS."))
def pe_gtt(ctx):
    recession = ctx.mac("real_retail_yoy") < 0 or ctx.mac("indpro_yoy") < 0
    return {"SPY": 1.0} if (not recession or _trend_up(ctx)) else {"BIL": 1.0}


@register(**meta("philoeconomics_gtt_unemployment", assets=["SPY"], lookback_months=10, macro_inputs=["unemp"]))
def pe_gtt_ue(ctx):
    ue = ctx.mac_hist("unemp", 12)
    recession = ue.iloc[-1] > ue.mean()
    return {"SPY": 1.0} if (not recession or _trend_up(ctx)) else {"BIL": 1.0}


@register(**meta("novell_bond_ui1", assets=["HYG", "LQD", "BNDX", "EMB", "IEF", "TLT", "GLD"], lookback_months=1, macro_inputs=["unemp"]))
def novell_ui1(ctx):
    ue = ctx.mac_hist("unemp", 12)
    if ue.iloc[-1] > ue.mean():
        return {"IEF": 0.25, "TLT": 0.25, "GLD": 0.25, "BIL": 0.25}
    return {"HYG": 0.25, "LQD": 0.25, "BNDX": 0.25, "EMB": 0.25}


@register(**meta("novell_tactical_bond", assets=["SHY", "IEF", "TLT", "TIP", "LQD", "HYG"], optional=["BNDX", "EMB"], lookback_months=6))
def novell_tb(ctx):
    U = ["SHY", "IEF", "TLT", "TIP", "LQD", "HYG"] + ctx.available(["BNDX", "EMB"], 6)
    r = ctx.ret(U + ["BIL"], 6)
    w = {}
    for k in top(r[U], 3):
        ok = r[k] > 0 and r[k] > r["BIL"] and k != "SHY"
        add(w, k if ok else "BIL", 1 / 3)
    return w


@register(**meta("quantpedia_trendycmacro", assets=["SPY"], needs_daily=True, lookback_months=11,
                 macro_inputs=["real_retail_yoy", "indpro_yoy", "housing_starts_yoy", "y10", "y3m"]))
def trendycmacro(ctx):
    macro_ok = ctx.mac("real_retail_yoy") > 0 and ctx.mac("indpro_yoy") > 0 and ctx.mac("housing_starts_yoy") > 0
    if macro_ok and ctx.state.get("long"):
        return {"SPY": 1.0}
    h = ctx.dhist(["SPY", "BIL"], 200).pct_change().iloc[1:]
    xs = h["SPY"] - h["BIL"]
    idx = (1 + xs).cumprod()
    med = xs.median()
    rachev = xs[xs > med].mean() / -xs[xs < med].mean()
    go = idx.iloc[-1] > idx.mean() and rachev > 1 and ctx.mac("y10") > ctx.mac("y3m")
    ctx.state["long"] = bool(go)
    return {"SPY": 1.0} if go else {"BIL": 1.0}


@register(**meta("quantpedia_gold_cross_asset_momentum", assets=["GLD", "IEF"], lookback_months=12))
def gold_xmom(ctx):
    r = ctx.ret(["GLD", "IEF"], 12)
    return {"GLD": 1.0} if (r > 0).all() else {"BIL": 1.0}


ZAK_W = np.array([0.0925, 0.0739, 0.0582, 0.0443, 0.0325, 0.0221, 0.0136, 0.0061, 0.0, -0.0046, -0.0082, -0.0107, -0.0125,
                  -0.0136, -0.0139, -0.0143, -0.0139, -0.0132, -0.0125, -0.0118, -0.0107, -0.0096, -0.0089, -0.0079,
                  -0.0068, -0.0057, -0.0050, -0.0043, -0.0032, -0.0025])


@register(**meta("zakamulin_optimal_trend_following", assets=["SPY"], lookback_months=31))
def zakamulin(ctx):
    r = ctx.mret_hist(["SPY"], 30)["SPY"].values[::-1]      # most recent first
    return {"SPY": 1.0} if float(ZAK_W @ r) > 0 else {"BIL": 1.0}


@register(**meta("pitkajarvi_us_cross_asset_momentum", assets=["SPY", "IEF"], lookback_months=12))
def pitkajarvi(ctx):
    r = ctx.ret(["SPY", "IEF", "BIL"], 12)
    xs_s, xs_b = r["SPY"] - r["BIL"], r["IEF"] - r["BIL"]
    if xs_b > 0:
        return {"SPY": 1.0} if xs_s > 0 else {"IEF": 1.0}
    return {"BIL": 1.0}


# ----------------------------------------------------------------------------- risk parity with trend (Clare et al.)
CLARE_US = ["SPY", "IWM", "IEF", "DBC", "VNQ"]


def _rp_trend(ctx, U, mult):
    vol = ctx.mret_hist(U, 12).std()
    raw = pd.Series(mult, index=U) / vol
    rp = raw / raw.sum()
    up = ctx.sma_rel(U, 10) > 0
    w = {}
    for k in U:
        add(w, k if up[k] else "BIL", float(rp[k]))
    return w


@register(**meta("clare_us_risk_parity_trend", assets=CLARE_US, lookback_months=12,
                 notes="Trend is tested on total-return prices rather than cash prices (small difference)."))
def clare_us(ctx):
    return _rp_trend(ctx, CLARE_US, [1.0] * 5)


CLARE_G = ["SPY", "EFA", "EEM", "IEF", "BWX", "DBC", "RWO"]


@register(**meta("clare_global_risk_parity_trend", assets=CLARE_G, lookback_months=12,
                 notes="Trend is tested on total-return prices rather than cash prices (small difference)."))
def clare_global(ctx):
    return _rp_trend(ctx, CLARE_G, [0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0])


# ----------------------------------------------------------------------------- Pragmatic Asset Allocation (tranches)
PAA_RISKY, PAA_DEF = ["ACWI", "QQQ", "EEM"], ["IEF", "GLD", "BIL"]


@register(**meta("quantpedia_pragmatic_aa", assets=PAA_RISKY + ["IEF", "GLD"], lookback_months=14, macro_inputs=["y10", "y3m"],
                 notes="The four tranches are seeded with the same allocation at the start of the backtest."))
def pragmatic_aa(ctx):
    st = ctx.state.setdefault("tranches", {})          # tranche month -> {asset: (weight, held_since)}
    m = ctx.date.month
    lag = 1                                              # trades use data as of the previous month-end

    def up(t):
        return ctx.px([t], lag)[t] > ctx.m[t].iloc[ctx.i - lag - 11:ctx.i - lag + 1].mean()

    def mom(ts):
        return ctx.px(ts, lag) / ctx.px(ts, lag + 12) - 1

    def build():
        alloc, defense = {}, 0.0
        k = ctx.macro.index.get_indexer([ctx.date])[0] - lag
        if ctx.macro["y10"].iloc[k] <= ctx.macro["y3m"].iloc[k]:
            defense = 0.25
        else:
            for t in top(mom(PAA_RISKY), 2):
                if up(t):
                    add(alloc, t, 0.125)
                else:
                    defense += 0.125
        if defense:
            for t in top(mom(PAA_DEF), 2):
                add(alloc, t if (t != "BIL" and up(t)) else "BIL", defense / 2)
        return alloc

    if not st:
        for tm in (1, 4, 7, 10):
            st[tm] = {t: (v, ctx.date) for t, v in build().items()}
    elif m in (1, 4, 7, 10):
        prev = st.get(m, {})
        st[m] = {t: (v, prev[t][1] if t in prev else ctx.date) for t, v in build().items()}
        for tm, tr in st.items():          # stop-loss on the other three tranches
            if tm == m:
                continue
            for t, (v, since) in list(tr.items()):
                if t != "BIL" and not up(t) and (ctx.date - since).days > 365:
                    tr.pop(t)
                    tr["BIL"] = (tr.get("BIL", (0, ctx.date))[0] + v, ctx.date)
    w = {}
    for tr in st.values():
        for t, (v, _) in tr.items():
            add(w, t, v)
    return w
