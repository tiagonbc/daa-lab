"""Raw data access: Norgate Data (local, licensed) and free public web sources.

Every pull is cached on disk so the full pipeline can be re-run quickly.
Norgate data stays in data/cache (git-ignored): only derived strategy results
are published.
"""
from __future__ import annotations

import io
import time
import zipfile
from functools import lru_cache

import numpy as np
import pandas as pd
import requests

from ..config import CACHE_DIR, DATA_START, WEB_DIR

MAX_CACHE_AGE_H = 12


def _fresh(path, max_age_h=MAX_CACHE_AGE_H) -> bool:
    return path.exists() and (time.time() - path.stat().st_mtime) < max_age_h * 3600


def _safe(symbol: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in symbol)


# --------------------------------------------------------------------------- Norgate
@lru_cache(maxsize=None)
def norgate_close(symbol: str, total_return: bool = True, start: str = DATA_START) -> pd.Series:
    """Daily close for a Norgate symbol. ETFs/stocks are total-return adjusted
    (dividends reinvested); indices and economic series are returned as-is."""
    path = CACHE_DIR / f"ng_{_safe(symbol)}_{int(total_return)}_{start[:4]}.pkl"
    if _fresh(path):
        return pd.read_pickle(path)
    import norgatedata as nd

    kwargs = dict(
        start_date=start,
        padding_setting=nd.PaddingType.NONE,
        timeseriesformat="pandas-dataframe",
    )
    if total_return:
        kwargs["stock_price_adjustment_setting"] = nd.StockPriceAdjustmentType.TOTALRETURN
    df = nd.price_timeseries(symbol, **kwargs)
    s = df["Close"].astype(float)
    s.index = pd.DatetimeIndex(s.index).normalize()
    s.name = symbol
    s = s[~s.index.duplicated(keep="last")].dropna()
    s.to_pickle(path)
    return s


@lru_cache(maxsize=None)
def norgate_econ(symbol: str) -> pd.Series:
    """Economic series from Norgate. Norgate stamps values by REFERENCE period
    (e.g. October CPI appears on October dates) - publication lags must be
    applied by the caller (see data/macro.py)."""
    return norgate_close(symbol, total_return=False, start="1950-01-01")


# --------------------------------------------------------------------------- Web
def _download(url: str, path, max_age_h=72) -> bytes:
    if _fresh(path, max_age_h):
        return path.read_bytes()
    last = None
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=(15, 120), headers={"User-Agent": "Mozilla/5.0 (daa-lab research)"})
            r.raise_for_status()
            break
        except requests.RequestException as e:   # FRED is occasionally slow - retry
            last = e
            time.sleep(3 * (attempt + 1))
    else:
        if path.exists():
            return path.read_bytes()
        raise last
    path.write_bytes(r.content)
    return r.content


@lru_cache(maxsize=None)
def fred(series_id: str) -> pd.Series:
    """FRED series via the public fredgraph CSV endpoint (no API key)."""
    raw = _download(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}",
        WEB_DIR / f"fred_{series_id}.csv",
    )
    df = pd.read_csv(io.BytesIO(raw))
    df.columns = ["date", "value"]
    s = pd.to_numeric(df["value"], errors="coerce")
    s.index = pd.to_datetime(df["date"])
    return s.dropna().rename(series_id)


@lru_cache(maxsize=None)
def french_market(region_file: str, daily: bool) -> pd.Series:
    """Total market return (Mkt-RF + RF) in USD from the Ken French data library,
    e.g. region_file='Developed_ex_US_3_Factors'. Returns simple returns."""
    suffix = "_Daily_CSV.zip" if daily else "_CSV.zip"
    name = region_file + suffix
    raw = _download(
        f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{name}",
        WEB_DIR / name,
    )
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    rows = []
    started = False
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if not started:
            if len(parts) > 2 and parts[1] == "Mkt-RF":
                started = True
                cols = parts
            continue
        if not parts[0] or not parts[0].isdigit():
            if rows:
                break          # end of the first (monthly/daily) block; annual block follows
            continue
        rows.append(parts)
    df = pd.DataFrame(rows, columns=cols)
    key = df.columns[0]
    fmt = "%Y%m%d" if daily else "%Y%m"
    idx = pd.to_datetime(df[key], format=fmt)
    if not daily:
        idx = idx + pd.offsets.MonthEnd(0)
    mkt = pd.to_numeric(df["Mkt-RF"]) + pd.to_numeric(df["RF"])
    s = pd.Series(mkt.values / 100.0, index=idx, name=region_file)
    return s[s > -0.9999]


@lru_cache(maxsize=None)
def gold_monthly() -> pd.Series:
    """Monthly gold price (USD/oz, monthly average) from the open `datasets/gold-prices`
    repository. Used only as a pre-2004 proxy for GLD (flagged in the site)."""
    raw = _download(
        "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv",
        WEB_DIR / "gold_monthly.csv",
    )
    df = pd.read_csv(io.BytesIO(raw))
    idx = pd.to_datetime(df["Date"], format="%Y-%m") + pd.offsets.MonthEnd(0)
    return pd.Series(df["Price"].astype(float).values, index=idx, name="GOLD")


# --------------------------------------------------------------------------- Synthetic
def bond_tr_from_yield(yield_pct: pd.Series, maturity: float) -> pd.Series:
    """Daily total-return index of a constant-maturity par bond rebuilt each day.

    Each day we 'own' a par bond paying coupon y(t-1) with `maturity` years left,
    reprice it at y(t), and collect one day of carry. This is the standard way
    (e.g. Swinkels 2019) to back-fill bond ETF history from Treasury yields.
    """
    y = (yield_pct / 100.0).dropna()
    y = y[~y.index.duplicated()]
    y_prev = y.shift(1)
    dt = y.index.to_series().diff().dt.days.fillna(1).clip(lower=1) / 365.25
    n = 2 * maturity
    c = y_prev / 2
    r = y / 2
    with np.errstate(divide="ignore", invalid="ignore"):
        price = np.where(r.abs() > 1e-9, c / r * (1 - (1 + r) ** (-n)) + (1 + r) ** (-n), 1.0)
    ret = pd.Series(price, index=y.index) - 1 + y_prev * dt
    ret = ret.iloc[1:].fillna(0.0)
    return (1 + ret).cumprod()


def cash_tr_from_yield(yield_pct: pd.Series) -> pd.Series:
    """Daily total-return index of rolling T-bills from an annualised bill yield."""
    y = (yield_pct / 100.0).dropna()
    y = y[~y.index.duplicated()]
    dt = y.index.to_series().diff().dt.days.fillna(1).clip(lower=1) / 365.25
    ret = (1 + y.shift(1)) ** dt - 1
    return (1 + ret.iloc[1:].fillna(0.0)).cumprod()


@lru_cache(maxsize=None)
def french_portfolio(file_stem: str, column: str, daily: bool = True) -> pd.Series:
    """One portfolio column (e.g. 'BIG HiPRIOR') from a Ken French portfolio file; simple returns."""
    suffix = "_Daily_CSV.zip" if daily else "_CSV.zip"
    name = file_stem + suffix
    raw = _download(f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{name}", WEB_DIR / name)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    header, rows = None, []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if header is None:
            if column in parts:
                header = parts
            continue
        if not parts[0].isdigit():
            if rows:
                break        # first block = value-weighted returns
            continue
        rows.append(parts)
    df = pd.DataFrame(rows, columns=header)
    idx = pd.to_datetime(df.iloc[:, 0], format="%Y%m%d" if daily else "%Y%m")
    s = pd.Series(pd.to_numeric(df[column]).values / 100.0, index=idx, name=column)
    return s[s > -0.9999]


@lru_cache(maxsize=None)
def spf(variable: str) -> pd.DataFrame:
    """Philadelphia Fed Survey of Professional Forecasters, mean responses (e.g. 'RECESS', 'TBOND', 'TBILL').
    Indexed by survey quarter-end date."""
    name = f"mean_{variable.lower()}_level.xlsx"
    raw = _download("https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/"
                    f"data-files/files/{name}", WEB_DIR / name, max_age_h=24 * 7)
    df = pd.read_excel(io.BytesIO(raw))
    df = df.dropna(subset=["YEAR", "QUARTER"])
    df.index = pd.PeriodIndex.from_fields(year=df["YEAR"].astype(int), quarter=df["QUARTER"].astype(int), freq="Q")
    return df.apply(pd.to_numeric, errors="coerce")
