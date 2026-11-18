"""Asset registry: every ticker a strategy can hold, with its back-fill ("proxy") chain.

Strategies are written in terms of the ETFs their authors used (SPY, EFA, TLT ...).
Most of those ETFs only exist from 2002-2007, so before an ETF launched we splice in
the closest available total-return series:

    ETF (Norgate, dividends reinvested)  ->  total-return index  ->  synthetic series

Proxies are only used for dates BEFORE the real ETF existed, and every splice is
validated against the ETF over the period where both exist (see `validate_proxies`).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from . import sources as src


@dataclass(frozen=True)
class Leg:
    kind: str            # etf | index | index_er | index_div | bond | cash | french_d | french_m | gold_m
    symbol: str
    label: str
    params: tuple = field(default_factory=tuple)

    @property
    def monthly_only(self) -> bool:
        return self.kind in ("french_m", "gold_m")


def etf(t):
    return Leg("etf", t, f"{t} ETF (Norgate, total return)")


def idx(sym, label):
    return Leg("index", sym, label)


def bond(yields, maturity, label):
    """Synthetic Treasury from Norgate constant-maturity yields: yields = {symbol: weight}."""
    return Leg("bond", "+".join(yields), label, (("maturity", maturity), ("weights", tuple(yields.items()))))


CASH_LEG = Leg("cash", "%IRX", "13-week T-bill yield (Norgate %IRX), rolled daily")
Y2 = bond({"%2YTCM": 1.0}, 2.0, "Synthetic 2-year Treasury (Norgate 2y CMT yield)")
Y5 = bond({"%5YTCM": 1.0}, 5.0, "Synthetic 5-year Treasury (Norgate 5y CMT yield)")
Y8 = bond({"%5YTCM": 0.33, "%10YTCM": 0.67}, 8.5, "Synthetic 8.5-year Treasury (Norgate 5y/10y CMT yields)")
Y15 = bond({"%10YTCM": 0.5, "%30YTCM": 0.5}, 15.0, "Synthetic 15-year Treasury (Norgate 10y/30y CMT yields)")
GOLD_LEG = Leg("index_er", "$BCOMPR", "Bloomberg Precious Metals sub-index + T-bill collateral return")
Y25 = bond({"%30YTCM": 1.0}, 25.0, "Synthetic 25-year Treasury (Norgate 30y CMT yield)")


# Proxy chains, in priority order. Tickers not listed fall back to the ETF alone.
CHAINS: dict[str, list[Leg]] = {
    # --- US equity
    "SPY": [etf("SPY"), idx("$SPXTR", "S&P 500 Total Return index")],
    "IVV": [etf("IVV"), etf("SPY"), idx("$SPXTR", "S&P 500 Total Return index")],
    "VOO": [etf("VOO"), etf("SPY"), idx("$SPXTR", "S&P 500 Total Return index")],
    "VTI": [etf("VTI"), idx("$RUATR", "Russell 3000 Total Return index")],
    "IWB": [etf("IWB"), idx("$RUITR", "Russell 1000 Total Return index")],
    "IWM": [etf("IWM"), idx("$RUTTR", "Russell 2000 Total Return index")],
    "VB": [etf("VB"), etf("IWM"), idx("$RUTTR", "Russell 2000 Total Return index")],
    "IJR": [etf("IJR"), idx("$SMLTR", "S&P SmallCap 600 Total Return index"), idx("$RUTTR", "Russell 2000 Total Return index")],
    "MDY": [etf("MDY"), idx("$MIDTR", "S&P MidCap 400 Total Return index")],
    "IJH": [etf("IJH"), etf("MDY"), idx("$MIDTR", "S&P MidCap 400 Total Return index")],
    "QQQ": [etf("QQQ"), idx("$NDXTR", "Nasdaq-100 Total Return index"), Leg("index_div", "$NDX", "Nasdaq-100 price index + 0.5%/yr dividends", (("yield", 0.005),))],
    "IWD": [etf("IWD"), idx("$SPCVTR", "S&P 1500 Value Total Return index")],
    "IWF": [etf("IWF"), idx("$SPCGTR", "S&P 1500 Growth Total Return index")],
    "IWN": [etf("IWN"), idx("$SPSVTR", "S&P SmallCap 600 Value Total Return index")],
    "IWO": [etf("IWO"), idx("$SPSGTR", "S&P SmallCap 600 Growth Total Return index")],
    "VTV": [etf("VTV"), etf("IWD"), idx("$SPCVTR", "S&P 1500 Value Total Return index")],
    "VUG": [etf("VUG"), etf("IWF"), idx("$SPCGTR", "S&P 1500 Growth Total Return index")],
    "VBR": [etf("VBR"), etf("IWN"), idx("$SPSVTR", "S&P SmallCap 600 Value Total Return index")],
    # --- International equity
    "MTUM": [etf("MTUM"), Leg("french_p", "6_Portfolios_ME_Prior_12_2|BIG HiPRIOR", "Ken French US big-cap high-momentum portfolio (daily)")],
    "EFV": [etf("EFV"), Leg("french_p", "Developed_ex_US_6_Portfolios_ME_BE-ME|BIG HiBM", "Ken French Developed ex-US big-cap value portfolio (daily)")],
    "RWO": [etf("RWO"), etf("RWX")],
    "EFA": [etf("EFA"), Leg("french_d", "Developed_ex_US_3_Factors", "Ken French Developed ex-US market (USD, daily)")],
    "VEA": [etf("VEA"), etf("EFA"), Leg("french_d", "Developed_ex_US_3_Factors", "Ken French Developed ex-US market (USD, daily)")],
    "IEFA": [etf("IEFA"), etf("EFA"), Leg("french_d", "Developed_ex_US_3_Factors", "Ken French Developed ex-US market (USD, daily)")],
    "VEU": [etf("VEU"), etf("EFA"), Leg("french_d", "Developed_ex_US_3_Factors", "Ken French Developed ex-US market (USD, daily)")],
    "VGK": [etf("VGK"), Leg("french_d", "Europe_3_Factors", "Ken French Europe market (USD, daily)")],
    "EWJ": [etf("EWJ"), Leg("french_d", "Japan_3_Factors", "Ken French Japan market (USD, daily)")],
    "VPL": [etf("VPL"), Leg("french_d", "Asia_Pacific_ex_Japan_3_Factors", "Ken French Asia Pacific ex-Japan market (USD, daily)")],
    "EEM": [etf("EEM"), Leg("french_m", "Emerging_5_Factors", "Ken French Emerging Markets (USD, monthly only)")],
    "VWO": [etf("VWO"), etf("EEM"), Leg("french_m", "Emerging_5_Factors", "Ken French Emerging Markets (USD, monthly only)")],
    "IEMG": [etf("IEMG"), etf("EEM"), Leg("french_m", "Emerging_5_Factors", "Ken French Emerging Markets (USD, monthly only)")],
    # --- Real estate
    "VNQ": [etf("VNQ"), etf("IYR"), Leg("index_div", "$DWRTF", "Dow Jones US Select REIT price index + 6.5%/yr dividends", (("yield", 0.065),))],
    "IYR": [etf("IYR"), Leg("index_div", "$DWRTF", "Dow Jones US Select REIT price index + 6.5%/yr dividends", (("yield", 0.065),))],
    "SCHH": [etf("SCHH"), etf("VNQ"), etf("IYR")],
    # --- US Treasuries (synthetic from constant-maturity yields before the ETFs)
    "BIL": [etf("BIL"), CASH_LEG],
    "SHV": [etf("SHV"), etf("BIL"), CASH_LEG],
    "SGOV": [etf("SGOV"), etf("BIL"), CASH_LEG],
    "SHY": [etf("SHY"), Y2],
    "VGSH": [etf("VGSH"), etf("SHY"), Y2],
    "IEI": [etf("IEI"), Y5],
    "IEF": [etf("IEF"), Y8],
    "VGIT": [etf("VGIT"), etf("IEI"), Y5],
    "GOVT": [etf("GOVT"), etf("IEF"), Y8],
    "TLH": [etf("TLH"), Y15],
    "TLT": [etf("TLT"), Y25],
    "VGLT": [etf("VGLT"), etf("TLT"), Y25],
    "SPTL": [etf("SPTL"), etf("TLT"), Y25],
    "EDV": [etf("EDV"), etf("TLT"), Y25],
    "ZROZ": [etf("ZROZ"), etf("EDV"), etf("TLT"), Y25],
    # --- Other bonds
    "AGG": [etf("AGG"), idx("$USBIG", "FTSE US Broad Investment-Grade Bond TR index")],
    "BND": [etf("BND"), etf("AGG"), idx("$USBIG", "FTSE US Broad Investment-Grade Bond TR index")],
    "LQD": [etf("LQD"), idx("$USBIGCORP", "FTSE US Broad Investment-Grade Corporate Bond TR index")],
    "VCIT": [etf("VCIT"), etf("LQD"), idx("$USBIGCORP", "FTSE US Broad Investment-Grade Corporate Bond TR index")],
    "TIP": [etf("TIP")],
    "SCHP": [etf("SCHP"), etf("TIP")],
    "VTIP": [etf("VTIP"), etf("TIP")],
    "HYG": [etf("HYG")],
    "JNK": [etf("JNK"), etf("HYG")],
    "BWX": [etf("BWX")],
    "BNDX": [etf("BNDX"), etf("BWX")],
    "ACWI": [etf("ACWI"), etf("VT")],
    "EMB": [etf("EMB")],
    "MUB": [etf("MUB")],
    # --- Real assets
    "GLD": [etf("GLD"), GOLD_LEG],
    "IAU": [etf("IAU"), etf("GLD"), GOLD_LEG],
    "SLV": [etf("SLV"), GOLD_LEG],
    "DBC": [etf("DBC"), idx("$BCOMTR", "Bloomberg Commodity Total Return index")],
    "GSG": [etf("GSG"), idx("$BCOMTR", "Bloomberg Commodity Total Return index")],
    "PDBC": [etf("PDBC"), etf("DBC"), idx("$BCOMTR", "Bloomberg Commodity Total Return index")],
    "DJP": [etf("DJP"), idx("$BCOMTR", "Bloomberg Commodity Total Return index")],
}


def chain(ticker: str) -> list[Leg]:
    return CHAINS.get(ticker, [etf(ticker)])


# --------------------------------------------------------------------------- level series
def _leg_daily(leg: Leg) -> pd.Series | None:
    p = dict(leg.params)
    if leg.kind in ("etf", "index"):
        try:
            return src.norgate_close(leg.symbol, total_return=(leg.kind == "etf"))
        except Exception:
            return None
    if leg.kind == "index_er":   # excess-return futures index + collateral (T-bill) return
        px = src.norgate_close(leg.symbol, total_return=False)
        cash = _leg_daily(CASH_LEG).reindex(px.index).ffill()
        r = px.pct_change().fillna(0.0) + cash.pct_change().fillna(0.0)
        return (1 + r).cumprod()
    if leg.kind == "index_div":
        px = src.norgate_close(leg.symbol, total_return=False)
        r = px.pct_change().fillna(0.0) + p["yield"] / 252
        return (1 + r).cumprod()
    if leg.kind == "bond":
        parts = [src.norgate_econ(sym) * w for sym, w in p["weights"]]
        y = pd.concat(parts, axis=1).sum(axis=1, min_count=len(parts)).dropna()
        return src.bond_tr_from_yield(y, p["maturity"])
    if leg.kind == "cash":
        return src.cash_tr_from_yield(src.norgate_econ(leg.symbol))
    if leg.kind == "french_d":
        r = src.french_market(leg.symbol, daily=True)
        return (1 + r).cumprod()
    if leg.kind == "french_p":
        stem, col = leg.symbol.split("|")
        return (1 + src.french_portfolio(stem, col, daily=True)).cumprod()
    return None


def _leg_monthly(leg: Leg) -> pd.Series | None:
    if leg.kind == "french_m":
        return (1 + src.french_market(leg.symbol, daily=False)).cumprod()
    if leg.kind == "gold_m":
        return src.gold_monthly()
    s = _leg_daily(leg)
    return None if s is None else s.resample("ME").last().dropna()


class AssetPanel:
    """Daily and month-end total-return levels for any ticker, built lazily."""

    def __init__(self, calendar: pd.DatetimeIndex | None = None):
        if calendar is None:
            spx = src.norgate_close("$SPXTR", total_return=False)
            spy = src.norgate_close("SPY")
            calendar = spx.index.union(spy.index)
        self.calendar = pd.DatetimeIndex(calendar)
        self.month_ends = pd.DatetimeIndex(self.calendar.to_series().groupby(self.calendar.to_period("M")).max().values)
        # calendar month-end label -> actual last trading day of that month
        self.trade_dates = pd.Series(self.month_ends, index=self.month_ends + pd.offsets.MonthEnd(0))
        last = self.calendar[-1]
        self.partial_month = bool(last < last + pd.offsets.BMonthEnd(0))
        self._daily: dict[str, pd.Series] = {}
        self._monthly: dict[str, pd.Series] = {}
        self.meta: dict[str, dict] = {}

    def _build(self, ticker: str):
        legs = chain(ticker)
        daily_ret = None
        used = []
        for leg in legs:
            if leg.monthly_only:
                continue
            lvl = _leg_daily(leg)
            if lvl is None or lvl.empty:
                continue
            lvl = lvl.reindex(self.calendar.union(lvl.index)).ffill().reindex(self.calendar)
            lvl = lvl[lvl.index >= lvl.first_valid_index()] if lvl.first_valid_index() is not None else lvl.dropna()
            r = lvl.pct_change().iloc[1:]
            if daily_ret is None:
                daily_ret = r
                used.append((leg, r.index[0]))
            else:
                first = daily_ret.first_valid_index()
                add = r[r.index < first]
                if len(add):
                    daily_ret = pd.concat([add, daily_ret[daily_ret.index >= first]])
                    used.append((leg, add.index[0]))
        if daily_ret is None:
            raise KeyError(f"No data for {ticker}")
        daily = (1 + daily_ret.dropna()).cumprod()
        monthly = daily.groupby(daily.index.to_period("M")).last()
        monthly.index = monthly.index.to_timestamp(how="end").normalize()
        # drop the first partial month - its return would be incomplete
        mret = monthly.pct_change().iloc[1:]
        # monthly-only proxies extend further back in time
        for leg in legs:
            if not leg.monthly_only:
                continue
            ml = _leg_monthly(leg)
            if ml is None:
                continue
            mr = ml.pct_change().dropna()
            add = mr[mr.index < mret.index[0]]
            if len(add):
                mret = pd.concat([add, mret])
                used.append((leg, add.index[0]))
        mlevel = (1 + mret).cumprod()
        mlevel = pd.concat([pd.Series([1.0], index=[mret.index[0] - pd.offsets.MonthEnd(1)]), mlevel])
        self._daily[ticker] = daily.rename(ticker)
        self._monthly[ticker] = mlevel.rename(ticker)
        etf_leg = legs[0]
        etf_start = None
        if etf_leg.kind == "etf":
            try:
                etf_start = src.norgate_close(etf_leg.symbol).index[0]
            except Exception:
                pass
        self.meta[ticker] = {
            "ticker": ticker,
            "etf_start": None if etf_start is None else str(etf_start.date()),
            "daily_start": str(daily.index[0].date()),
            "monthly_start": str(mlevel.index[0].date()),
            "splices": [{"from": str(pd.Timestamp(d).date()), "source": l.label} for l, d in sorted(used, key=lambda x: x[1])],
        }

    def daily(self, ticker: str) -> pd.Series:
        if ticker not in self._daily:
            self._build(ticker)
        return self._daily[ticker]

    def monthly(self, ticker: str) -> pd.Series:
        if ticker not in self._monthly:
            self._build(ticker)
        return self._monthly[ticker]

    def monthly_frame(self, tickers) -> pd.DataFrame:
        return pd.concat([self.monthly(t) for t in tickers], axis=1)

    def daily_frame(self, tickers) -> pd.DataFrame:
        return pd.concat([self.daily(t) for t in tickers], axis=1)


def validate_proxies(panel: AssetPanel, tickers) -> pd.DataFrame:
    """Compare each proxy with its ETF over the overlap (monthly returns)."""
    rows = []
    for t in tickers:
        legs = chain(t)
        if len(legs) < 2 or legs[0].kind != "etf":
            continue
        try:
            etf_lvl = src.norgate_close(legs[0].symbol)
        except Exception:
            continue
        em = etf_lvl.resample("ME").last().pct_change().iloc[2:]
        for leg in legs[1:]:
            if leg.kind == "etf":
                continue
            pl = _leg_monthly(leg)
            if pl is None:
                continue
            pm = pl.pct_change()
            both = pd.concat([em, pm], axis=1, join="inner").dropna()
            both = both[both.index <= em.index[-2]]
            if len(both) < 24:
                continue
            a, b = both.iloc[:, 0], both.iloc[:, 1]
            rows.append({
                "ticker": t, "proxy": leg.label, "months": len(both),
                "corr": round(float(a.corr(b)), 3),
                "tracking_error": round(float((a - b).std() * np.sqrt(12)), 4),
                "ann_return_etf": round(float((1 + a).prod() ** (12 / len(a)) - 1), 4),
                "ann_return_proxy": round(float((1 + b).prod() ** (12 / len(b)) - 1), 4),
            })
    return pd.DataFrame(rows)
