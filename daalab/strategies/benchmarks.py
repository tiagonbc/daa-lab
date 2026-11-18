"""Reference portfolios every strategy is compared against."""
from ..engine.core import register


@register(
    id="bench_6040", name="60/40 Portfolio (US)", author="Benchmark", family="static", year=1952,
    source_title="Classic balanced portfolio", source_url="https://en.wikipedia.org/wiki/Modern_portfolio_theory",
    assets=["SPY", "IEF"], lookback_months=1, benchmark=True,
    plain_english="60% in US stocks (S&P 500) and 40% in 7-10 year US Treasuries, rebalanced monthly. "
                  "It is the standard yardstick for a balanced investor: any tactical strategy should beat it on risk, return, or both.",
    rules=["Hold 60% SPY and 40% IEF.", "Rebalance back to 60/40 at every month-end."],
)
def bench_6040(ctx):
    return {"SPY": 0.6, "IEF": 0.4}


@register(
    id="bench_spy", name="US Stocks (S&P 500)", author="Benchmark", family="static", year=1957,
    source_title="S&P 500 total return", source_url="https://www.spglobal.com/spdji/en/indices/equity/sp-500/",
    assets=["SPY"], lookback_months=1, benchmark=True,
    plain_english="100% in the S&P 500 with dividends reinvested. Shows what equity-market risk alone delivered.",
    rules=["Hold 100% SPY."],
)
def bench_spy(ctx):
    return {"SPY": 1.0}


@register(
    id="bench_global_6040", name="Global 60/40", author="Benchmark", family="static", year=1990,
    source_title="Global balanced portfolio", source_url="https://www.msci.com/",
    assets=["SPY", "EFA", "EEM", "IEF", "TLT", "AGG"], lookback_months=1, benchmark=True,
    plain_english="A globally diversified balanced mix: 35% US stocks, 18% developed international, 7% emerging markets, "
                  "and 40% US bonds. Closer to what a large pension fund's liquid public-market sleeve looks like.",
    rules=["35% SPY, 18% EFA, 7% EEM, 20% IEF, 20% AGG.", "Rebalance monthly."],
)
def bench_global_6040(ctx):
    return {"SPY": 0.35, "EFA": 0.18, "EEM": 0.07, "IEF": 0.20, "AGG": 0.20}


@register(
    id="bench_otpp_mix", name="OTPP-shaped Reference Mix (liquid proxy)", author="Benchmark", family="static", year=2025,
    source_title="Ontario Teachers' 2025 Annual Report - asset mix, p.32 (illustrative liquid proxy)",
    source_url="https://www.otpp.com/content/dam/otpp/documents/reports/2025-ar/otpp-2025-annual-report-eng.pdf",
    assets=["SPY", "EFA", "EEM", "IEF", "TLT", "DBC", "GLD", "VNQ", "XLU", "LQD"], lookback_months=1, benchmark=True,
    plain_english="An illustrative, liquid stand-in for the shape of OTPP's 2025 asset mix: 43% equity, 23% fixed income, "
                  "20% inflation-sensitive, 23% real assets, 14% credit and 9% absolute return, financed by borrowing "
                  "32% at the T-bill rate (OTPP's 'Funding and other' line). Private assets are proxied with listed ones, "
                  "so this is a teaching device, not a replica of OTPP's portfolio or returns.",
    rules=["Equity 43%: SPY 22%, EFA 14%, EEM 7%.", "Fixed income 23%: IEF 12%, TLT 11%.",
           "Inflation sensitive 20%: commodities (DBC) 10%, gold (GLD) 10%.",
           "Real assets 23%: US REITs (VNQ) 12%, utilities as an infrastructure stand-in (XLU) 11%.",
           "Credit 14%: investment-grade corporates (LQD).", "Absolute return 9%: cash (BIL).",
           "Funding -32%: borrow at the T-bill rate. Net cash = -23%.", "Rebalance monthly."],
    notes="Gross exposure is 132% of capital, matching the leverage implied by the 2025 report. Borrowing is charged at the "
          "T-bill rate with no spread, which flatters the proxy slightly.",
)
def bench_otpp_mix(ctx):
    return {"SPY": 0.22, "EFA": 0.14, "EEM": 0.07, "IEF": 0.12, "TLT": 0.11, "DBC": 0.10, "GLD": 0.10,
            "VNQ": 0.12, "XLU": 0.11, "LQD": 0.14, "BIL": -0.23}
