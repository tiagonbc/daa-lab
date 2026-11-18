"""Macro-factor allocation, following Macrosynergy's "Wealth management with macro factors" method
(research/macrosynergy_spec.md) with US data available in Norgate + FRED.

The method in plain words:
  1. Turn each economic indicator into a score of how unusual it is versus a NEUTRAL level
     (e.g. inflation minus the 2% target). zn(x) = x / (average absolute size of x so far), capped at +/-3.
  2. Average related scores into themes: growth, labour tightness, inflation pressure, financial ease ...
  3. For each asset, add up the themes that should help it (+) or hurt it (-): e.g. equities like
     growth and easy financial conditions, and dislike inflation pressure and a tight labour market.
  4. Convert asset scores to weights with a softmax: w_i = exp(S_i) / sum_j exp(S_j), cash fixed at S=0.
Every input is lagged for publication delays, and scores only ever use past data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..data import sources as src
from ..data.macro import _monthly_asof
from ..engine.core import NotReady, register
from .catalog import meta
from .keller_antonacci import add

TARGET = 2.0
_CACHE: dict = {}


def zn(x: pd.Series, min_obs: int = 60, cap: float = 3.0) -> pd.Series:
    """Score relative to a zero neutral level, scaled by the expanding mean absolute value (no look-ahead)."""
    mad = x.abs().expanding(min_obs).mean()
    return (x / mad).clip(-cap, cap)


def _theme(parts: dict) -> pd.Series:
    """Weighted average of scores, renormalised over components available at each date; re-scored if >1 part."""
    df = pd.DataFrame({k: v for k, (v, _) in parts.items()})
    w = pd.Series({k: wt for k, (_, wt) in parts.items()})
    num = (df * w).sum(axis=1, min_count=1)
    den = df.notna().mul(w.abs()).sum(axis=1)
    out = num / den.replace(0, np.nan)
    return zn(out) if len(parts) > 1 else out


def _fred_m(series_id, lag, grid):
    try:
        return _monthly_asof(src.fred(series_id), "M", lag, grid)
    except Exception:
        return pd.Series(np.nan, index=grid)


def factor_panel(macro: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    key = (id(macro), len(macro))
    if key in _CACHE:
        return _CACHE[key]
    g = macro.index
    M = macro
    ma3 = lambda s: s.rolling(3).mean()
    trend = M["gdp_yoy"].rolling(60, min_periods=36).median()
    growth_now = M["cfnai_ma3"]
    # Deviation from the original: industrial production is compared with ITS OWN 5-year trend, not trend GDP.
    # US factory output has grown ~1.4pp a year slower than GDP since 1990, so "IP minus GDP trend" sits below zero
    # most of the time and drags the growth score down (negative in 55% of months since 1990).
    xip = ma3(M["indpro_yoy"]) - M["indpro_yoy"].rolling(60, min_periods=36).median()
    xempl = ma3(M["payrolls_yoy"]) - M["payrolls_yoy"].rolling(60, min_periods=36).median()
    du = ma3(M["unemp"]) - ma3(M["unemp"]).shift(12)
    ugap = ma3(M["unemp"]) - M["unemp"].rolling(60, min_periods=36).mean()
    labtight = 0.5 * zn(xempl) - 0.25 * zn(du) - 0.25 * zn(ugap)
    xcpi = pd.concat([M["cpi_yoy"], M["core_cpi_yoy"], M["cpi_6m_ann"], M["core_cpi_6m_ann"]], axis=1).mean(axis=1) - TARGET
    mich = _fred_m("MICH", 1, g)
    xhh = mich - mich.rolling(120, min_periods=60).median()
    xhpi = ma3(M["hpi_yoy"]) - TARGET
    exp1, exp5 = _fred_m("EXPINF1YR", 1, g), _fred_m("EXPINF5YR", 1, g)
    riry = 0.5 * (M["y3m"] - exp1) + 0.5 * (M["y5"] - exp5)
    tp5 = _fred_m("THREEFYTP5", 1, g)
    xmon = M["m2_yoy"] - TARGET - trend
    mfg_lvl = ma3(M["ism"]) - 50
    mfg_chg = ma3(M["ism"]) - ma3(M["ism"]).shift(3)
    isr = _fred_m("MNFCTRIRSA", 2, g)
    inv_chg = ma3(isr) - ma3(isr).shift(3)
    constr_chg = 100 * (ma3(M["housing_starts"]) / ma3(M["housing_starts"]).shift(3) - 1)
    crcarry = 0.5 * zn(M["baa_spread"]) + 0.5 * zn(M["ccc_oas"])

    T = pd.DataFrame(index=g)
    T["PRODGROWTH"] = _theme({"g": (zn(growth_now), .5), "ip": (zn(xip), .5)})
    T["FINEASE"] = _theme({"mon": (zn(xmon), 1 / 3), "rr": (-zn(riry), 1 / 3), "tp": (-zn(tp5), 1 / 3)})
    T["LABT"] = zn(labtight)
    T["INFLPRESS"] = _theme({"cpi": (zn(xcpi), .5), "hh": (zn(xhh), .5)})
    T["CPI"] = zn(xcpi)
    T["HOUSING"] = zn(xhpi)
    T["FIPREMIA"] = _theme({"tp": (zn(tp5), .5), "rr": (zn(riry), .5)})
    T["ECONSTR"] = _theme({"lab": (zn(labtight), 1 / 3), "ip": (zn(xip), 1 / 3), "g": (zn(growth_now), 1 / 3)})
    T["CYCLE"] = _theme({"lvl": (zn(mfg_lvl), 1 / 3), "chg": (zn(mfg_chg), 1 / 3), "inv": (-zn(inv_chg), 1 / 3)})
    T["BUSCONF"] = _theme({"chg": (zn(mfg_chg), .5), "con": (zn(constr_chg), .5)})
    T["INVCYCLE"] = zn(inv_chg)
    T["REALRATES"] = zn(riry)
    T["TERMPREM"] = zn(tp5)
    T["MONGROWTH"] = zn(xmon)
    T["CRCARRY"] = zn(crcarry)

    def comp(signed):
        df = pd.concat([sign * T[k] for k, sign in signed], axis=1)
        return zn(df.mean(axis=1, skipna=True).where(df.notna().sum(axis=1) >= max(2, len(signed) // 2)))

    T["S_EQ"] = comp([("PRODGROWTH", 1), ("FINEASE", 1), ("LABT", -1), ("INFLPRESS", -1), ("CYCLE", 1)])
    T["S_UST"] = comp([("FIPREMIA", 1), ("CPI", -1), ("HOUSING", -1), ("CYCLE", -1)])
    T["S_CR"] = comp([("TERMPREM", 1), ("CPI", -1), ("HOUSING", -1), ("CYCLE", -1), ("CRCARRY", 1), ("ECONSTR", 1),
                      ("INVCYCLE", -1), ("REALRATES", -1)])
    T["S_GLD"] = comp([("BUSCONF", -1), ("MONGROWTH", -1), ("CPI", -1)])
    labels = {"PRODGROWTH": "Growth", "INFLPRESS": "Inflation pressure", "LABT": "Labour tightness",
              "FINEASE": "Financial ease", "CYCLE": "Manufacturing cycle"}
    _CACHE[key] = (T, labels)
    return T, labels


def site_factors(macro: pd.DataFrame):
    T, labels = factor_panel(macro)
    out = T[list(labels)].rename(columns={"PRODGROWTH": "growth", "INFLPRESS": "inflation", "LABT": "labour",
                                          "FINEASE": "financial", "CYCLE": "cycle"})
    return out, {"growth": "Growth", "inflation": "Inflation pressure", "labour": "Labour tightness",
                 "financial": "Financial ease", "cycle": "Manufacturing cycle"}


def _scores(ctx) -> pd.Series:
    T, _ = factor_panel(ctx.macro)
    return T.loc[ctx.date]


MACRO_INPUTS = ["cfnai", "indpro", "payrolls", "unemp", "cpi", "core_cpi", "case_shiller", "m2", "ism", "housing_starts",
                "y3m", "y5", "baa", "ccc_oas", "FRED: MICH, EXPINF1YR, EXPINF5YR, THREEFYTP5, MNFCTRIRSA"]
NOTE = ("Lab replication with US public data. One deliberate change: excess industrial-production growth is measured against "
        "its own 5-year trend rather than trend GDP growth, because US factory output structurally grows slower than GDP and the "
        "original definition biases the US growth score downward. Labour-force growth is proxied by the 60-month median of payroll growth, "
        "building permits by housing starts, and the equity-carry leg of the gold score is omitted (no live earnings data). "
        "ISM data in Norgate stops in Aug 2026 and is carried forward. Signals at quarter-end are traded at the same close "
        "(the original trades one day later).")


@register(**meta("ms_wm_us5_softmax", assets=["SPY", "IEI", "LQD", "GLD"], lookback_months=1, rebalance="Q",
                 family="macro", macro_inputs=MACRO_INPUTS, min_start="1999-12-31", notes=NOTE))
def ms_us5(ctx):
    s = _scores(ctx)
    logits = pd.Series({"SPY": s["S_EQ"], "IEI": s["S_UST"], "LQD": s["S_CR"], "GLD": s["S_GLD"], "BIL": 0.0})
    if logits.isna().any():
        raise NotReady(f"macro scores not available at {ctx.date:%Y-%m}")
    e = np.exp(logits)
    return (e / e.sum()).to_dict()


@register(**meta("ms_wm_balanced_tilt", assets=["SPY", "IEF"], lookback_months=1, rebalance="Q", family="macro",
                 author="Tiago Costa, adapting Brine, Cereda & Sueppel (Macrosynergy, 2026)",
                 macro_inputs=MACRO_INPUTS, min_start="1999-12-31", notes=NOTE))
def ms_tilt(ctx):
    s = _scores(ctx)
    b = pd.Series({"SPY": 0.54, "IEF": 0.36, "BIL": 0.10})
    logits = pd.Series({"SPY": s["S_EQ"], "IEF": s["S_UST"], "BIL": 0.0})
    if logits.isna().any():
        raise NotReady(f"macro scores not available at {ctx.date:%Y-%m}")
    e = b * np.exp(logits)
    return (e / e.sum()).to_dict()


QUAD = {
    (True, False): {"SPY": 0.70, "IEF": 0.30},                              # growth up, inflation down
    (True, True): {"SPY": 0.50, "DBC": 0.20, "TIP": 0.15, "GLD": 0.15},     # reflation
    (False, True): {"SPY": 0.20, "TIP": 0.30, "GLD": 0.25, "BIL": 0.25},    # stagflation
    (False, False): {"SPY": 0.20, "IEF": 0.60, "GLD": 0.20},                # disinflationary slowdown
}


@register(**meta("growth_inflation_quadrants", assets=["SPY", "IEF", "TIP", "DBC", "GLD"], lookback_months=1, family="macro",
                 author="Tiago Costa, after Ilmanen, Maloney & Ross (2014) and Neville et al. (2021)",
                 macro_inputs=MACRO_INPUTS, notes=NOTE))
def quadrants(ctx):
    s = _scores(ctx)
    if pd.isna(s["PRODGROWTH"]) or pd.isna(s["INFLPRESS"]):
        raise NotReady("growth/inflation themes not available yet")
    q = (bool(s["PRODGROWTH"] > 0), bool(s["INFLPRESS"] > 0))
    st = ctx.state
    if "q" not in st:
        st["q"], st["pending"] = q, None
    elif q != st["q"]:
        if st["pending"] == q:                 # new quadrant confirmed at two consecutive month-ends
            st["q"], st["pending"] = q, None
        else:
            st["pending"] = q
    else:
        st["pending"] = None
    return dict(QUAD[st["q"]])


@register(**meta("inflation_surge_overlay", assets=["SPY", "IEF", "TIP", "DBC", "GLD"], lookback_months=10, family="macro",
                 author="Tiago Costa, after Neville, Draaisma, Funnell, Harvey & Van Hemert (2021)",
                 macro_inputs=["cpi_yoy"]))
def inflation_surge(ctx):
    cpi = ctx.mac_hist("cpi_yoy", 7)
    on = ctx.state.get("on", False)
    if not on and cpi.iloc[-1] >= 4.0 and cpi.iloc[-1] > cpi.iloc[0]:
        on = True
    elif on and (cpi.iloc[-1] < 3.0 or cpi.iloc[-1] < cpi.iloc[0]):
        on = False
    ctx.state["on"] = on
    if not on:
        return {"SPY": 0.6, "IEF": 0.4}
    w = {"TIP": 0.4 / 3, "DBC": 0.4 / 3, "GLD": 0.4 / 3}
    add(w, "SPY" if ctx.sma_rel(["SPY"], 10)["SPY"] >= 0 else "BIL", 0.6)
    return w
