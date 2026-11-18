"""Momentum-rotation strategies by Wouter Keller (& co-authors) and Gary Antonacci.

Rules follow research/strategies_keller_antonacci.json (each entry cites the original paper).
Common building blocks:
  13612W  = 12*r1 + 4*r3 + 2*r6 + r12      (fast, recency-weighted momentum)
  13612U  = (r1 + r3 + r6 + r12) / 4       (unweighted)
  SMA12   = price / average of the last 13 month-end prices - 1
  canary  = assets watched only as an early-warning signal for 'crash protection'
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from ..engine.core import register
from .catalog import meta


# ----------------------------------------------------------------------------- helpers
def top(scores: pd.Series, n: int) -> list[str]:
    """Highest n scores; ties keep the universe order (stable sort)."""
    return list(scores.sort_values(ascending=False, kind="stable").index[:n])


def best(scores: pd.Series) -> str:
    return top(scores, 1)[0]


def add(w: dict, k: str, v: float):
    if v:
        w[k] = w.get(k, 0.0) + v


def ew_corr(ctx, assets, universe, n=12) -> pd.Series:
    """Correlation of each asset's last n monthly returns with an equal-weight portfolio of `universe`."""
    h = ctx.mret_hist(list(dict.fromkeys(assets + universe)), n)
    idx = h[universe].mean(axis=1)
    return h[assets].apply(lambda c: c.corr(idx))


def min_variance(cov: pd.DataFrame) -> pd.Series:
    n = len(cov)
    if n == 1:
        return pd.Series(1.0, index=cov.index)
    S = cov.values
    res = minimize(lambda w: w @ S @ w, np.full(n, 1 / n), method="SLSQP", bounds=[(0, 1)] * n,
                   constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}], options={"ftol": 1e-12, "maxiter": 500})
    w = np.clip(res.x, 0, None)
    return pd.Series(w / w.sum(), index=cov.index)


def max_return_at_vol(mu: pd.Series, cov: pd.DataFrame, target_vol: float, caps: dict) -> pd.Series:
    """Long-only Markowitz: highest expected return with annualised volatility <= target (CAA).
    If even the minimum-variance portfolio is above target, return the minimum-variance portfolio."""
    n = len(mu)
    S = cov.values * 12
    bounds = [(0, caps.get(k, 1.0)) for k in mu.index]
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    x0 = np.array([b[1] for b in bounds]); x0 = x0 / x0.sum()
    mv = minimize(lambda w: w @ S @ w, x0, method="SLSQP", bounds=bounds, constraints=cons, options={"ftol": 1e-12, "maxiter": 500})
    if math.sqrt(max(mv.fun, 0)) >= target_vol:
        w = mv.x
    else:
        cons2 = cons + [{"type": "ineq", "fun": lambda w: target_vol ** 2 - w @ S @ w}]
        res = minimize(lambda w: -(w @ mu.values), mv.x, method="SLSQP", bounds=bounds, constraints=cons2, options={"ftol": 1e-12, "maxiter": 500})
        w = res.x if res.success else mv.x
    w = np.clip(w, 0, None)
    return pd.Series(w / w.sum(), index=mu.index)


# ============================================================================= FAA
FAA_U = ["VTI", "VEA", "VWO", "BND", "GSG", "VNQ", "SHY"]


@register(**meta("faa", assets=FAA_U, needs_daily=True))
def faa(ctx):
    R = ctx.dret(FAA_U, 84)
    V = ctx.dvol(FAA_U, 84)
    cm = ctx.dcorr(FAA_U, 84)
    Cc = (cm.sum() - 1) / (len(FAA_U) - 1)
    loss = R.rank(ascending=False) + 0.5 * V.rank(ascending=True) + 0.5 * Cc.rank(ascending=True)
    picks = list(loss.sort_values(kind="stable").index[:3])
    w = {}
    for p in picks:
        add(w, p if R[p] > 0 else "SHY", 1 / 3)
    return w


# ============================================================================= EAA
EAA_U = ["SPY", "EFA", "EEM", "QQQ", "EWJ", "HYG", "IEF"]


def _eaa(ctx, wR, wC, wV, wS):
    U = EAA_U
    ex = lambda t: (ctx.ret(t, 1) + ctx.ret(t, 3) + ctx.ret(t, 6) + ctx.ret(t, 12)) / 22
    r = ex(U) - ex(["BIL"])["BIL"]
    v = ctx.mret_hist(U, 12).std()
    c = ew_corr(ctx, U, U)
    z = pd.Series(0.0, index=U)
    pos = r > 0
    z[pos] = ((r[pos] ** wR) * ((1 - c[pos]) ** wC) / (v[pos] ** wV)) ** (wS + 1e-6)
    N = len(U)
    cp = (~pos).sum() / N
    top_n = min(1 + math.ceil(math.sqrt(N)), N // 2)
    picks = [k for k in top(z, top_n) if z[k] > 0]
    w = {}
    if picks:
        tot = z[picks].sum()
        for k in picks:
            add(w, k, (1 - cp) * z[k] / tot)
        add(w, "IEF", cp)
    else:
        w = {"IEF": 1.0}
    return w


@register(**meta("eaa_golden_offensive", assets=EAA_U))
def eaa_off(ctx):
    return _eaa(ctx, 1, 0.5, 0, 2)


@register(**meta("eaa_golden_defensive", assets=EAA_U))
def eaa_def(ctx):
    return _eaa(ctx, 1, 1, 0, 0.5)


# ============================================================================= CAA
CAA_U = ["SPY", "QQQ", "EFA", "EEM", "EWJ", "HYG", "IEF", "BIL"]


def _caa(ctx, tv):
    mu = (ctx.ret(CAA_U, 1) + ctx.ret(CAA_U, 3) + ctx.ret(CAA_U, 6) + ctx.ret(CAA_U, 12)) / 22
    cov = ctx.mret_hist(CAA_U, 12).cov()
    caps = {k: 0.25 for k in CAA_U}
    caps.update({"IEF": 1.0, "BIL": 1.0})
    w = max_return_at_vol(mu, cov, tv, caps)
    return {k: v for k, v in w.items() if v > 1e-4} or {"BIL": 1.0}


@register(**meta("caa_offensive", assets=CAA_U))
def caa_off(ctx):
    w = _caa(ctx, 0.10)
    s = sum(w.values())
    return {k: v / s for k, v in w.items()}


@register(**meta("caa_defensive", assets=CAA_U))
def caa_def(ctx):
    w = _caa(ctx, 0.05)
    s = sum(w.values())
    return {k: v / s for k, v in w.items()}


# ============================================================================= PAA
PAA_U = ["SPY", "QQQ", "IWM", "VGK", "EWJ", "EEM", "VNQ", "DBC", "GLD", "HYG", "LQD", "TLT"]
PAA_U_PAPER = ["SPY", "QQQ", "IWM", "VGK", "EWJ", "EEM", "IYR", "GSG", "GLD", "HYG", "LQD", "TLT"]


def _paa(ctx, U, a, protection=("IEF",)):
    N = len(U)
    mom = ctx.sma_rel(U, 13)
    n = int((mom > 0).sum())
    n1 = a * N / 4
    bf = min(1.0, (N - n) / (N - n1))
    prot = protection[0] if len(protection) == 1 else best(ctx.sma_rel(list(protection), 13))
    w = {}
    picks = [k for k in top(mom, 6) if mom[k] > 0]
    if bf < 1 and picks:
        for k in picks:
            add(w, k, (1 - bf) / len(picks))
        add(w, prot, bf)
    else:
        w = {prot: 1.0}
    return w


@register(**meta("paa2", assets=PAA_U + ["IEF"]))
def paa2(ctx):
    return _paa(ctx, PAA_U, 2)


@register(**meta("paa_cpr", assets=PAA_U + ["IEF", "BIL"]))
def paa_cpr(ctx):
    return _paa(ctx, PAA_U, 2, ("IEF", "BIL"))


@register(**meta("paa1", assets=PAA_U_PAPER + ["IEF"]))
def paa1(ctx):
    return _paa(ctx, PAA_U_PAPER, 1)


@register(**meta("paa0", assets=PAA_U_PAPER + ["IEF"]))
def paa0(ctx):
    return _paa(ctx, PAA_U_PAPER, 0)


# ============================================================================= GPM
@register(**meta("gpm", assets=PAA_U + ["IEF", "BIL"]))
def gpm(ctx):
    U = PAA_U
    allx = U + ["IEF", "BIL"]
    r = ctx.mom13612u(allx)
    c = ew_corr(ctx, allx, U)
    z = r * (1 - c.fillna(0))
    n = int((z[U] > 0).sum())
    cp = min(1.0, (12 - n) / 6)
    prot = best(z[["IEF", "BIL"]])
    w = {}
    if cp < 1:
        for k in top(z[U], 3):
            add(w, k, (1 - cp) / 3)
    add(w, prot, cp)
    return w


# ============================================================================= VAA
@register(**meta("vaa_g4", assets=["SPY", "EFA", "EEM", "AGG", "LQD", "IEF", "SHY"]))
def vaa_g4(ctx):
    off, dfn = ["SPY", "EFA", "EEM", "AGG"], ["LQD", "IEF", "SHY"]
    m = ctx.mom13612w(off + dfn)
    return {best(m[off]): 1.0} if (m[off] > 0).all() else {best(m[dfn]): 1.0}


VAA12 = ["SPY", "IWM", "QQQ", "VGK", "EWJ", "VWO", "VNQ", "GSG", "GLD", "TLT", "LQD", "HYG"]
CASH3 = ["SHY", "IEF", "LQD"]


def _breadth_rotation(ctx, risky, cash, T, B, bad_count):
    m = ctx.mom13612w(list(dict.fromkeys(risky + cash)))
    cf = min(1.0, math.floor(bad_count * T / B) / T)
    k = round((1 - cf) * T)
    w = {}
    for a in top(m[risky], k):
        add(w, a, 1 / T)
    add(w, best(m[cash]), cf)
    return w


@register(**meta("vaa_g12", assets=VAA12 + CASH3))
def vaa_g12(ctx):
    b = int((ctx.mom13612w(VAA12) <= 0).sum())
    return _breadth_rotation(ctx, VAA12, CASH3, 2, 4, b)


@register(**meta("vaa_g12_balanced", assets=VAA12 + CASH3))
def vaa_g12_bal(ctx):
    b = int((ctx.mom13612w(VAA12) <= 0).sum())
    return _breadth_rotation(ctx, VAA12, CASH3, 5, 4, b)


# ============================================================================= DAA
CANARY = ["VWO", "BND"]


def _daa(ctx, risky, cash, T, B):
    b = int((ctx.mom13612w(CANARY) < 0).sum())
    return _breadth_rotation(ctx, risky, cash, T, B, b)


DAA12 = ["SPY", "IWM", "QQQ", "VGK", "EWJ", "VWO", "VNQ", "GSG", "GLD", "TLT", "HYG", "LQD"]


@register(**meta("daa_g12", assets=DAA12 + CASH3 + CANARY))
def daa_g12(ctx):
    return _daa(ctx, DAA12, CASH3, 6, 2)


@register(**meta("daa_g6", assets=["SPY", "VEA", "VWO", "LQD", "TLT", "HYG"] + CASH3 + CANARY))
def daa_g6(ctx):
    return _daa(ctx, ["SPY", "VEA", "VWO", "LQD", "TLT", "HYG"], CASH3, 6, 2)


@register(**meta("daa_g4", assets=["SPY", "VEA", "VWO", "BND"] + CASH3))
def daa_g4(ctx):
    return _daa(ctx, ["SPY", "VEA", "VWO", "BND"], CASH3, 2, 1)


CASH_DAA1 = ["SHV", "IEF", "UST"]


@register(**meta("daa1_g4", assets=["SPY", "VEA", "VWO", "BND"] + CASH_DAA1))
def daa1_g4(ctx):
    return _daa(ctx, ["SPY", "VEA", "VWO", "BND"], CASH_DAA1, 4, 1)


@register(**meta("daa1_g12", assets=DAA12 + CASH_DAA1 + CANARY))
def daa1_g12(ctx):
    return _daa(ctx, DAA12, CASH_DAA1, 2, 1)


@register(**meta("daa1_u1", assets=["SPY"] + CASH_DAA1 + CANARY))
def daa1_u1(ctx):
    bad = (ctx.mom13612w(CANARY) < 0).any()
    return {best(ctx.mom13612w(CASH_DAA1)): 1.0} if bad else {"SPY": 1.0}


# ============================================================================= LAA / RAA (use the unemployment rate)
def _gt_bearish(ctx) -> bool:
    """Growth-Trend timing: unemployment above its 12m average AND S&P 500 below its 10m average."""
    ue = ctx.mac_hist("unemp", 12)
    growth_bad = ue.iloc[-1] > ue.mean()
    trend_bad = ctx.sma_rel(["SPY"], 10)["SPY"] < 0
    return bool(growth_bad and trend_bad)


@register(**meta("laa", assets=["IWD", "GLD", "IEF", "QQQ", "SHY", "SPY"], macro_inputs=["unemp"]))
def laa(ctx):
    w = {"IWD": 0.25, "GLD": 0.25, "IEF": 0.25}
    add(w, "SHY" if _gt_bearish(ctx) else "QQQ", 0.25)
    return w


@register(**meta("laa_g4", assets=["IWD", "GLD", "IEF", "SPY", "VEA", "VWO", "SHY"], macro_inputs=["unemp"]))
def laa_g4(ctx):
    w = {"IWD": 0.25, "GLD": 0.25, "IEF": 0.25}
    if _gt_bearish(ctx):
        add(w, "SHY", 0.25)
    else:
        for k, v in {"SPY": 0.5, "VEA": 1 / 3, "VWO": 1 / 6}.items():
            add(w, k, 0.25 * v)
    return w


@register(**meta("raa", assets=["QQQ", "IWN", "GLD", "IEF", "TLT", "EEM", "AGG"], macro_inputs=["unemp"]))
def raa(ctx):
    risk_on = ctx.mac("unemp") <= ctx.mac("unemp", lag=12)   # macro panel already lags UE by 1 month
    if not risk_on:
        risk_on = bool((ctx.mom13612w(["EEM", "AGG"]) > 0).all())
    return {k: 0.2 for k in ["QQQ", "IWN", "GLD", "IEF", "TLT"]} if risk_on else {"IEF": 0.5, "TLT": 0.5}


# ============================================================================= BAA
BAA_CANARY = ["SPY", "VWO", "VEA", "BND"]
BAA_DEF = ["TIP", "DBC", "BIL", "IEF", "TLT", "LQD", "BND"]
BAA12 = ["SPY", "QQQ", "IWM", "VGK", "EWJ", "VWO", "VNQ", "DBC", "GLD", "TLT", "HYG", "LQD"]
BAA4 = ["QQQ", "VWO", "VEA", "BND"]


def _baa(ctx, off, TO):
    if (ctx.mom13612w(BAA_CANARY) > 0).all():
        m = ctx.sma_rel(off, 13)
        return {k: 1 / TO for k in top(m, TO)}
    m = ctx.sma_rel(BAA_DEF, 13)
    w = {}
    for k in top(m, 3):
        add(w, k if m[k] >= m["BIL"] else "BIL", 1 / 3)
    return w


@register(**meta("baa_g12_balanced", assets=BAA12 + BAA_DEF + BAA_CANARY))
def baa_g12(ctx):
    return _baa(ctx, BAA12, 6)


@register(**meta("baa_g4_aggressive", assets=BAA4 + BAA_DEF + BAA_CANARY))
def baa_g4(ctx):
    return _baa(ctx, BAA4, 1)


@register(**meta("baa_g12_t3", assets=BAA12 + BAA_DEF + BAA_CANARY))
def baa_g12_t3(ctx):
    return _baa(ctx, BAA12, 3)


@register(**meta("baa_g4_t2", assets=BAA4 + BAA_DEF + BAA_CANARY))
def baa_g4_t2(ctx):
    return _baa(ctx, BAA4, 2)


# ============================================================================= HAA
def _haa(ctx, off, TO):
    m = ctx.mom13612u(list(dict.fromkeys(off + ["TIP", "BIL", "IEF"])))
    dfn = best(m[["BIL", "IEF"]])
    if m["TIP"] <= 0:
        return {dfn: 1.0}
    w = {}
    for k in top(m[off], TO):
        add(w, k if m[k] > 0 else dfn, 1 / TO)
    return w


HAA8 = ["SPY", "IWM", "VEA", "VWO", "VNQ", "DBC", "IEF", "TLT"]


@register(**meta("haa_balanced", assets=HAA8 + ["TIP", "BIL"]))
def haa_bal(ctx):
    return _haa(ctx, HAA8, 4)


@register(**meta("haa_simple", assets=["SPY", "TIP", "BIL", "IEF"]))
def haa_simple(ctx):
    return _haa(ctx, ["SPY"], 1)


@register(**meta("haa_4", assets=["SPY", "VEA", "VNQ", "IEF", "TIP", "BIL"]))
def haa_4(ctx):
    return _haa(ctx, ["SPY", "VEA", "VNQ", "IEF"], 2)


HAA12 = ["SPY", "QQQ", "IWM", "VGK", "EWJ", "VWO", "VNQ", "DBC", "GLD", "IEF", "TLT", "LQD"]


@register(**meta("haa_12", assets=HAA12 + ["TIP", "BIL"]))
def haa_12(ctx):
    return _haa(ctx, HAA12, 6)


HAA16 = ["SPY", "QQQ", "IWM", "IWD", "VGK", "EWJ", "VWO", "SCZ", "VNQ", "REM", "DBC", "GLD", "IEF", "TLT", "HYG", "LQD"]


@register(**meta("haa_16", assets=HAA16 + ["TIP", "BIL"]))
def haa_16(ctx):
    return _haa(ctx, HAA16, 8)


# ============================================================================= KDA
KDA_U = ["SPY", "VGK", "EWJ", "EEM", "VNQ", "RWX", "IEF", "TLT", "DBC", "GLD"]


@register(**meta("kda", assets=KDA_U + ["AGG", "BIL"], needs_daily=True))
def kda(ctx):
    allx = list(dict.fromkeys(KDA_U + ["AGG", "IEF"]))
    h = ctx.dhist(allx, 252)
    p0 = h.iloc[-1]
    mom = sum(wt * (p0 / h.iloc[-1 - d] - 1) for wt, d in ((12, 21), (4, 63), (2, 126), (1, 252)))
    risky_frac = (mom[["EEM", "AGG"]] > 0).sum() / 2
    picks = [k for k in top(mom[KDA_U], 5) if mom[k] > 0]
    w = {}
    if picks and risky_frac > 0:
        rets = h[picks].pct_change().iloc[1:]
        vol = rets.iloc[-21:].std()
        rho = sum(wt * rets.iloc[-d:].corr() for wt, d in ((12, 21), (4, 63), (2, 126), (1, 252))) / 19
        cov = rho * np.outer(vol, vol)
        mv = min_variance(cov)
        mv = mv[mv >= 0.02]              # AllocateSmartly: drop positions below 2%, re-scale
        mv = mv / mv.sum()
        for k, v in mv.items():
            add(w, k, risky_frac * v)
    else:
        risky_frac = 0.0
    add(w, "IEF" if mom["IEF"] > 0 else "BIL", 1 - risky_frac)
    return w


# ============================================================================= Antonacci
@register(**meta("gem", assets=["SPY", "VEU", "AGG", "BIL"], lookback_months=12))
def gem(ctx):
    r = ctx.ret(["SPY", "VEU", "BIL"], 12)
    if r["SPY"] <= r["BIL"]:
        return {"AGG": 1.0}
    return {best(r[["SPY", "VEU"]]): 1.0}


@register(**meta("gem_simplified", assets=["SPY", "VEU", "AGG", "BIL"], lookback_months=12))
def gem_simple(ctx):
    r = ctx.ret(["SPY", "VEU", "BIL"], 12)
    win = best(r[["SPY", "VEU"]])
    return {win: 1.0} if r[win] > r["BIL"] else {"AGG": 1.0}


CDM = {"equities": ["SPY", "EFA"], "credit": ["LQD", "HYG"], "real_estate": ["VNQ", "REM"], "stress": ["GLD", "TLT"]}


@register(**meta("composite_dual_momentum", assets=[a for v in CDM.values() for a in v] + ["BIL"], lookback_months=12))
def cdm(ctx):
    tick = [a for v in CDM.values() for a in v] + ["BIL"]
    r = ctx.ret(tick, 12)
    w = {}
    for pair in CDM.values():
        win = best(r[pair])
        add(w, win if r[win] > r["BIL"] else "BIL", 0.25)
    return w


@register(**meta("accelerating_dual_momentum", assets=["SPY", "SCZ", "TLT", "TIP"], lookback_months=6))
def adm(ctx):
    s = (ctx.ret(["SPY", "SCZ"], 1) + ctx.ret(["SPY", "SCZ"], 3) + ctx.ret(["SPY", "SCZ"], 6)) / 3
    if s.max() > 0:
        return {best(s): 1.0}
    return {best(ctx.ret(["TLT", "TIP"], 1)): 1.0}


@register(**meta("accelerating_dual_momentum_original", assets=["SPY", "SCZ", "TLT"], lookback_months=6))
def adm_orig(ctx):
    s = ctx.ret(["SPY", "SCZ"], 1) + ctx.ret(["SPY", "SCZ"], 3) + ctx.ret(["SPY", "SCZ"], 6)
    return {"TLT": 1.0} if (s < 0).all() else {best(s): 1.0}
