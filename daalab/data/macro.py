"""US macro panel, aligned to what an investor could actually know at each month-end.

Norgate stamps economic data by the period it DESCRIBES (October CPI sits on October
dates), but October CPI is only published in mid-November. Using it at the end of
October would be look-ahead bias. So every series gets a publication lag:

    value for reference month M  ->  usable from the end of month M + lag

Caveat (stated on the site): Norgate stores the latest *revised* values, not the
first-release vintages, so growth series such as payrolls are slightly cleaner here
than they were in real time. Market-based series (yields, spreads, VIX) have no such issue.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import sources as src

# name: (norgate symbol, frequency, lag, description)
#   frequency M = monthly reference period, Q = quarterly, W = weekly, D = market (daily close)
#   lag is in months for M/Q and in days for W
SERIES = {
    "unemp": ("#UNEMP", "M", 1, "Unemployment rate (%)"),
    "payrolls": ("#NFPAY", "M", 1, "Non-farm payrolls (thousands)"),
    "cpi": ("#CPISA", "M", 1, "Consumer price index, headline"),
    "core_cpi": ("#CPIXSA", "M", 1, "Consumer price index, core (ex food & energy)"),
    "ppi": ("#PPISA", "M", 1, "Producer price index"),
    "indpro": ("#INDSA", "M", 1, "Industrial production index"),
    "retail": ("#RETSA", "M", 1, "Retail & food services sales"),
    "ism": ("#NAPMI", "M", 1, "ISM manufacturing PMI"),
    "cfnai": ("#CFNAI", "M", 1, "Chicago Fed National Activity Index"),
    "housing_starts": ("#HOSSA", "M", 1, "Housing starts"),
    "m2": ("#M2FED", "M", 1, "M2 money stock"),
    "real_pce": ("#PCESA", "Q", 2, "Real personal consumption"),
    "gdp": ("#GDPSA", "Q", 2, "Real GDP"),
    "case_shiller": ("#SPCS20", "M", 2, "S&P/Case-Shiller 20-city home prices"),
    "nfci": ("#NFCI", "W", 7, "Chicago Fed financial conditions (positive = tighter than average)"),
    "nfci_credit": ("#NFCIC", "W", 7, "NFCI credit sub-index"),
    "claims": ("#INJOB", "W", 7, "Initial jobless claims"),
    "y3m": ("%3MTCM", "D", 0, "3-month Treasury yield (%)"),
    "y1": ("%1YTCM", "D", 0, "1-year Treasury yield (%)"),
    "y2": ("%2YTCM", "D", 0, "2-year Treasury yield (%)"),
    "y5": ("%5YTCM", "D", 0, "5-year Treasury yield (%)"),
    "y10": ("%10YTCM", "D", 0, "10-year Treasury yield (%)"),
    "y30": ("%30YTCM", "D", 0, "30-year Treasury yield (%)"),
    "baa": ("%COBAA", "D", 0, "Moody's Baa corporate yield (%)"),
    "aaa": ("%COAAA", "D", 0, "Moody's Aaa corporate yield (%)"),
    "ccc_oas": ("%CCCHYS", "D", 0, "CCC & lower high-yield spread (%)"),
    "vix": ("$VIX", "D", 0, "VIX implied volatility"),
    "copper_gold": ("#CUGC", "D", 0, "Copper / gold price ratio"),
}


def _monthly_asof(s: pd.Series, freq: str, lag: int, grid: pd.DatetimeIndex) -> pd.Series:
    s = s.dropna()
    if freq == "M":
        ref = s.groupby(s.index.to_period("M")).last()
        avail = ref.index.to_timestamp(how="end").normalize() + pd.offsets.MonthEnd(lag)
        out = pd.Series(ref.values, index=avail)
    elif freq == "Q":
        ref = s.groupby(s.index.to_period("Q")).last()
        avail = ref.index.to_timestamp(how="end").normalize() + pd.offsets.MonthEnd(lag)
        out = pd.Series(ref.values, index=avail)
    elif freq == "W":
        shifted = pd.Series(s.values, index=s.index + pd.Timedelta(days=lag))
        out = shifted.groupby(shifted.index.to_period("M")).last()
        out.index = out.index.to_timestamp(how="end").normalize()
    else:  # market data, known at the close
        out = s.groupby(s.index.to_period("M")).last()
        out.index = out.index.to_timestamp(how="end").normalize()
    out = out[~out.index.duplicated(keep="last")].sort_index()
    return out.reindex(grid.union(out.index)).ffill().reindex(grid)


def _last_reference(s: pd.Series, freq: str) -> str:
    d = s.dropna().index[-1]
    return str(d.to_period("Q" if freq == "Q" else "M")) if freq in ("M", "Q") else str(d.date())


def build_macro(grid: pd.DatetimeIndex) -> tuple[pd.DataFrame, dict]:
    raw, info = {}, {}
    for name, (sym, freq, lag, desc) in SERIES.items():
        try:
            s = src.norgate_econ(sym)
        except Exception:
            continue
        raw[name] = _monthly_asof(s, freq, lag, grid)
        info[name] = {"symbol": sym, "frequency": freq, "lag": lag, "description": desc,
                      "latest_reference": _last_reference(s, freq)}
    df = pd.DataFrame(raw, index=grid)

    def yoy(x, n=12):
        return x / x.shift(n) * 100 - 100

    def ann(x, n):
        return ((x / x.shift(n)) ** (12 / n) - 1) * 100

    # ---- derived features (all built only from already-lagged columns)
    df["payrolls_yoy"] = yoy(df["payrolls"])
    df["payrolls_3m_ann"] = ann(df["payrolls"], 3)
    df["cpi_yoy"] = yoy(df["cpi"])
    df["core_cpi_yoy"] = yoy(df["core_cpi"])
    df["core_cpi_3m_ann"] = ann(df["core_cpi"], 3)
    df["core_cpi_6m_ann"] = ann(df["core_cpi"], 6)
    df["cpi_6m_ann"] = ann(df["cpi"], 6)
    df["hpi_yoy"] = yoy(df["case_shiller"])
    df["ppi_yoy"] = yoy(df["ppi"])
    df["indpro_yoy"] = yoy(df["indpro"])
    df["indpro_3m_ann"] = ann(df["indpro"], 3)
    df["retail_yoy"] = yoy(df["retail"])
    df["real_retail_yoy"] = df["retail_yoy"] - df["cpi_yoy"]
    df["m2_yoy"] = yoy(df["m2"])
    df["housing_starts_yoy"] = yoy(df["housing_starts"])
    df["gdp_yoy"] = yoy(df["gdp"])
    df["cfnai_ma3"] = df["cfnai"].rolling(3).mean()
    df["ism_chg3"] = df["ism"] - df["ism"].shift(3)
    df["unemp_ma12"] = df["unemp"].rolling(12).mean()
    df["unemp_gap_low12"] = df["unemp"].rolling(3).mean() - df["unemp"].rolling(12).min()  # Sahm-style
    df["claims_4w_yoy"] = yoy(df["claims"])
    df["curve_10y3m"] = df["y10"] - df["y3m"]
    df["curve_10y2y"] = df["y10"] - df["y2"]
    df["real_10y"] = df["y10"] - df["core_cpi_yoy"]
    df["baa_spread"] = df["baa"] - df["y10"]
    df["y10_chg6"] = df["y10"] - df["y10"].shift(6)
    df["nfci_chg3"] = df["nfci"] - df["nfci"].shift(3)
    return df, info


def expanding_z(x: pd.Series, min_periods: int = 60, clip: float = 3.0) -> pd.Series:
    """Z-score using only the history available at each date (no look-ahead)."""
    mu = x.expanding(min_periods).mean()
    sd = x.expanding(min_periods).std()
    return ((x - mu) / sd).clip(-clip, clip)


def rolling_z(x: pd.Series, window: int = 120, min_periods: int = 60, clip: float = 3.0) -> pd.Series:
    mu = x.rolling(window, min_periods=min_periods).mean()
    sd = x.rolling(window, min_periods=min_periods).std()
    return ((x - mu) / sd).clip(-clip, clip)
