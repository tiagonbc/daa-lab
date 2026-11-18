# Tactical asset allocation strategies tracked or reviewed by AllocateSmartly (excluding Keller and Antonacci)

Generated 2026-11-18. **88 entries**: 72 strategies or variants on AllocateSmartly's (AS) public tracked list, and 16 strategies AS tested in public blog posts but does not track. The machine-readable version is `strategies_others.json`, which uses the same ids.

## Scope and method

**Coverage:**
- AS's public List of Strategies (allocatesmartly.com/list-of-strategies/, read Nov 2026) names 89 tracked strategies.
- Excluded, because another agent covers them:
  - 17 by Dr. Wouter Keller and his co-authors: BAA ×2, RAA, LAA, HAA ×2, DAA, VAA ×2, CAA ×2, GPM, PAA, PAA-CPR, EAA ×2, FAA;
  - 2 by Gary Antonacci: Traditional and Composite Dual Momentum.
- Included: the remaining **70 tracked strategies**, plus three variants AS tracks under separate names:
  - `stoken_active_combined_asset_monthly` (AS's "Stoken's ACA – Monthly");
  - `as_us_min_correlation` (AS's "US Min Correlation");
  - the GGC "Mid-Month" variant, which is described inside the `link_global_growth_cycle_enhanced` entry.
- Ilya Kipnis's own Defensive Adaptive Asset Allocation and Butler's AAA/TPP are included. Their Keller co-authored CAA is not.

**Sources:**
- All 229 public AS blog posts (from the post sitemap) were downloaded as text and searched.
- Each strategy's AS post, where one exists, was read and checked against the original paper, book or blog where reachable.
- AS's public 2019 strategy–asset matrix and its 2024/25 notice of representative-ETF changes were used for ticker mapping.
- Members-only pages were not accessed.

**Limits:**
- The shared web-search quota ran out partway through.
- SSRN and some publisher sites returned HTTP 403.
- Some checks against original sources therefore could not be completed. These are flagged in `notes` and in the Status column below.

## AS conventions you need in order to match AS results

**Execution and costs:**
- **Timing:** signals are computed at the close of the last trading day of the month and traded at that same close, unless stated otherwise.
- **Alternate trading days:** AS normalises each month to 21 trading days using round(day/days_in_month × 21). Month-end indicators are recomputed on the chosen day.
- **Costs:** 0.10% per trade, covering commission plus slippage. Dividends are reinvested.
- **Cash:** "cash" earns the 3-month T-bill rate. BIL, SHV or GBIL are ETF stand-ins.

**Assets and data:**
- **One ETF per asset class:**
  - Each asset class maps to one representative ETF: SPY, QQQ, IWM, EFA, EEM, VNQ, RWX, RWO, DBC, GLD, IEF, TLT, SHY, AGG, LQD, HYG, TIP, BWX, EMB, BNDX, MTUM, IWD/IWF/IWN/IWO, EFV, SCZ, VGK, EWJ, REM, and the XL* sectors.
  - From early 2025: EFA→IEFA, EEM→IEMG, RWX→VNQI, RWO→REET, IWD→VTV, IWF→VUG, IWN→VBR, IWO→VBK.
  - Commodities DBC→PDBC from about the end of 2022, stitched onto the same series.
- **History before each ETF existed:** index proxies with that ETF's expense ratio applied. AS's monthly backtests often start in the 1970s.
- **Indicator prices:** dividend-adjusted. A dividend is assumed unknown until 2 trading days after its ex-date.
- **Macro data:** lagged to its publication date. ALFRED/first-release vintages are used where available (in use since 2023).

**Benchmark:** 60% SPY and 40% IEF, rebalanced monthly.

**Family labels:** 'risk-parity' here includes AS's whole "Portfolio Optimization" bucket (minimum variance, minimum correlation, max diversification, ERC, max Sharpe).

## Summary table

Status values:
- **full**: rules are specified well enough to implement.
- **partial**: implementable, with flagged assumptions.
- **undisclosed**: proprietary rules or no source found; the entry is a placeholder.

| # | id | Strategy | Author | Family | Rebalance | Universe (risky / defensive / canary / cash) | Non-price data | ETF-only start | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `faber_ivy_static` | Ivy Portfolio (static 5-asset equal weight) | Mebane Faber & Eric Richardson | static | periodic rebalance back to fixed 20% weights… | SPY,EFA,IEF,VNQ,DBC / – / – / – | – | 2006 (DBC Feb-2006; V… | partial |
| 2 | `faber_gtaa5` | Global Tactical Asset Allocation 5 (GTAA 5) | Mebane Faber | trend-following | monthly; signal at the close of the last tra… | SPY,EFA,IEF,VNQ,DBC / – / – / BIL | – | 2007 (BIL May-2007; r… | full |
| 3 | `faber_gtaa13` | Global Tactical Asset Allocation 13 (GTAA 13… | Mebane Faber | trend-following | monthly; signal at the close of the last tra… | IWD,MTUM,IWN,IWM,EFA,EEM,IEF,BWX,LQD,TLT,DBC,GLD,VNQ / – / – / BIL | – | 2013 (MTUM Apr-2013; … | partial |
| 4 | `faber_gtaa_agg3` | Global Tactical Asset Allocation – Aggressiv… | Mebane Faber | momentum-rotation | monthly; signals at the close of the last tr… | IWD,MTUM,IWN,IWM,EFA,EEM,IEF,BWX,LQD,TLT,DBC,GLD,VNQ / – / – / BIL | – | 2013 (MTUM Apr-2013) | full |
| 5 | `faber_gtaa_agg6` | Global Tactical Asset Allocation – Aggressiv… | Mebane Faber | momentum-rotation | monthly; signals at the close of the last tr… | IWD,MTUM,IWN,IWM,EFA,EEM,IEF,BWX,LQD,TLT,DBC,GLD,VNQ / – / – / BIL | – | 2013 (MTUM Apr-2013) | full |
| 6 | `faber_trinity_lite` | The Trinity Portfolio (Lite) | Mebane Faber (Cambria Investment M… | momentum-rotation | monthly; signals at the close of the last tr… | MTUM,IWD,EFV,EEM,LQD,TLT,BWX,TIP,DBC,GLD,VNQ / – / – / BIL | – | 2013 (MTUM Apr-2013; … | full |
| 7 | `faber_12m_high_switch` | 12-Month High Switch [Dynamic Bond] | Mebane Faber | trend-following | monthly; signal at the close of the last tra… | SPY,EFA,VNQ,GLD,DBC / IEF / – / BIL | – | 2007 (BIL May-2007; D… | partial |
| 8 | `faber_sector_relative_strength` | Sector Relative Strength | Mebane Faber | momentum-rotation | monthly; signal at the close of the last tra… | XLB,XLE,XLF,XLI,XLK,XLP,XLU,XLV,XLY / – / SPY / BIL | pre-1999 sector index proxies (e.g. S&P sector indices or Fama-French industry … | 2007 (BIL May-2007; s… | partial |
| 9 | `faber_tactical_yield` | Tactical Yield | Mebane Faber | macro | monthly; signals at the close of the last tr… | – / IEF,LQD / – / BIL | monthly 10-year Treasury yield (e.g. FRED GS10/DGS10 month-end; pre-1953 from l… | 2007 (BIL May-2007; I… | partial |
| 10 | `alphaarchitect_raa_balanced` | Robust Asset Allocation – Balanced (RAA Bala… | Wesley Gray (Alpha Architect), wit… | trend-following | monthly; signals at the close of the last tr… | IWD,MTUM,EFV,EFA,VNQ,DBC / IEF / – / BIL | – | 2013 (MTUM Apr-2013; … | partial |
| 11 | `alphaarchitect_raa_aggressive` | Robust Asset Allocation – Aggressive (RAA Ag… | Wesley Gray (Alpha Architect), wit… | trend-following | monthly; signals at the close of the last tr… | IWD,MTUM,EFV,EFA,VNQ,DBC / IEF / – / BIL | – | 2013 (MTUM Apr-2013) | partial |
| 12 | `butler_adaptive_asset_allocation` | Adaptive Asset Allocation | Adam Butler, Michael Philbrick, Ro… | momentum-rotation | monthly; signal computed and traded at the c… | SPY,VGK,EWJ,EEM,VNQ,RWX,IEF,TLT,DBC,GLD / – / – / – | quadratic-programming solver for long-only min variance | 2007 (RWX launched De… | full |
| 13 | `butler_tactical_permanent_portfolio` | Tactical Permanent Portfolio | Adam Butler (GestaltU / ReSolve As… | trend-following | monthly; all calculations use data as of the… | SPY,IEF,GLD / – / – / cash | 3-month T-bill rate for cash return (AS cash convention) | 2005 (GLD Nov 2004, I… | full |
| 14 | `kipnis_defensive_adaptive_aa` | Defensive Adaptive Asset Allocation (KDA) | Ilya Kipnis (QuantStrat TradeR) | momentum-rotation | monthly; signals and trades at the close of … | SPY,VGK,EWJ,EEM,VNQ,RWX,IEF,TLT,DBC,GLD / IEF / EEM,AGG / cash | 3-month T-bill rate for cash return; QP solver for min variance | 2008 (RWX Dec 2006 pl… | full |
| 15 | `varadi_minimum_correlation` | Minimum Correlation Portfolio | David Varadi (CSS Analytics), with… | risk-parity | monthly, last trading day close (AS default;… | SPY,QQQ,IWM,EEM,EFA,TLT,VNQ,GLD / – / – / – | – | 2005 (GLD Nov 2004, V… | partial |
| 16 | `varadi_percentile_channels` | Percentile Channels | David Varadi (CSS Analytics) | trend-following | monthly; weights computed and traded at the … | SPY,VNQ,LQD,DBC / – / – / cash | 3-month T-bill rate for cash return | 2007 (DBC Feb 2006 pl… | full |
| 17 | `varadi_growth_inflation_sector_timing` | Growth and Inflation Sector Timing | David Varadi (CSS Analytics) | macro | daily check at the close; switch (at that cl… | XLK,XLE,XLV,XLP / – / SPY,XLE,XLI,XLF,XLB,XLU,XLV,XLP / – | – | 1999 (Select Sector S… | partial |
| 18 | `varadi_inflation_compass_original` | Inflation Compass - Original | David Varadi (CSS Analytics) | macro | monthly; signals and trades at the close of … | XLE,XLK,XLU,XLP / IEF / SPY,XLE,XLI,XLF,XLB,XLU,XLV,XLP / – | FRED T5YIE daily (published with ~1 business-day delay; lag accordingly - AS's … | 2003 (T5YIE begins Ja… | partial |
| 19 | `varadi_inflation_compass_enhanced` | Inflation Compass - Enhanced | David Varadi (CSS Analytics) | macro | monthly; last trading day close (as Original) | XLE,QQQ,XLU,PDBC,XLP / IEF / SPY,XLE,XLI,XLF,XLB,XLU,XLV,XLP / – | FRED T5YIE daily (lagged ~1 business day); pre-2003 breakeven proxy (undisclose… | 2006 (DBC Feb 2006 as… | partial |
| 20 | `newfound_diversified_dual_momentum` | Diversified Dual Momentum | Corey Hoffstein (Newfound Research) | momentum-rotation | monthly, last trading day close (AS default,… | SPY,EFA / AGG / – / – | – | 2004 (AGG Sep 2003, E… | partial |
| 21 | `as_max_diversification` | Max Diversification Portfolio (US Max Divers… | AllocateSmartly (N/A developer); t… | risk-parity | monthly; last trading day close | SPY,IEF,LQD,VNQ / – / – / – | QP solver | 2007 (VNQ Sep 2004 pl… | full |
| 22 | `as_equal_risk_contribution` | Equal Risk Contribution Portfolio (US Equal … | AllocateSmartly (N/A developer); t… | risk-parity | monthly; last trading day close | SPY,IEF,LQD,VNQ / – / – / – | ERC solver (e.g. Spinu / log-barrier or iterative) | 2007 (VNQ Sep 2004 pl… | full |
| 23 | `as_max_sharpe` | Max Sharpe Portfolio (US Max Sharpe) | AllocateSmartly (N/A developer); i… | risk-parity | monthly; last trading day close | SPY,IEF,LQD,VNQ / – / – / – | T-bill rate if a non-zero risk-free rate is used; QP solver | 2007 (VNQ Sep 2004 pl… | partial |
| 24 | `as_us_min_correlation` | US Min Correlation | AllocateSmartly (N/A developer); a… | risk-parity | monthly; last trading day close | SPY,IEF,LQD,VNQ / – / – / – | – | 2007 (VNQ Sep 2004 pl… | full |
| 25 | `benchmark_60_40` | 60/40 Benchmark | N/A (AllocateSmartly default bench… | static | monthly, at the close of the last trading da… | SPY / IEF / – / – | – | 2002 (IEF launched Ju… | full |
| 26 | `tresidder_optimumv` | OptimumV | Todd Tresidder (Financial Mentor) | momentum-rotation | monthly, last trading day close (AS default;… | – / – / – / – | unspecified economic-state data (undisclosed; AS would apply its 1-month public… | unknown (universe und… | **undisclosed** |
| 27 | `tresidder_optimum3` | Optimum3 | Todd Tresidder (Financial Mentor) | momentum-rotation | monthly, last trading day close (selection u… | SPY,QQQ,VNQ,REM,IEF,TLT,TIP,VGK,EWJ,SCZ,EEM,RWX,BWX,DBC,GLD / – / – / – | 3-month T-bill series if cash is used for unfilled slots (uncertain) | 2008 approx (SCZ Dec … | **undisclosed** |
| 28 | `tresidder_all_weather_quad_momentum` | All-Weather Quad Momentum (AWQM) | Todd Tresidder (Financial Mentor) | momentum-rotation | monthly (AS default last trading day close) | – / – / – / cash | 3-month T-bill series for cash | unknown (universe und… | **undisclosed** |
| 29 | `livingston_mama_bear` | Mama Bear Portfolio | Brian Livingston (Muscular Portfol… | momentum-rotation | monthly, last trading day close; full rebala… | SPY,IWM,EFA,EEM,VNQ,DBC,GLD,TLT / – / – / cash | – | 2006 (DBC Feb 2006; G… | full |
| 30 | `livingston_papa_bear` | Papa Bear Portfolio | Brian Livingston (Muscular Portfol… | momentum-rotation | monthly, last trading day close; full rebala… | IWF,IWD,IWO,IWN,EFA,EEM,VNQ,DBC,GLD,TLT,IEF,LQD,BNDX / – / – / – | – | 2013 (BNDX Jun 2013);… | full |
| 31 | `philoeconomics_growth_trend_timing` | Growth-Trend Timing (GTT-Original) | Philosophical Economics (pseudonym… | macro | monthly, last trading day close | SPY / – / – / cash | FRED/ALFRED RRSFS (vintages), lagged 1 month; FRED/ALFRED INDPRO (vintages), la… | 1993 (SPY); RRSFS fro… | full |
| 32 | `philoeconomics_gtt_unemployment` | Growth-Trend Timing - UE Rate | Philosophical Economics (pseudonym… | macro | monthly, last trading day close | SPY / – / – / cash | FRED/ALFRED UNRATE with vintages, lagged 1 month; pre-1948 monthly unemployment… | 1993 (SPY) | full |
| 33 | `novell_spy_comp` | SPY-COMP | Paul Novell (Investing for a Livin… | macro | monthly, last trading day close | SPY / IEF / – / – | 6 undisclosed monthly macro series (FRED/ALFRED vintages, lagged 1 month) | 2002 (IEF Jul 2002) | **undisclosed** |
| 34 | `novell_bond_comp` | Bond-COMP | Paul Novell (Investing for a Livin… | macro | monthly, last trading day close; equal-weigh… | HYG,LQD,BNDX,EMB / IEF,TLT,GLD / – / cash | 3-month T-bill series for cash; 6 undisclosed FRED/ALFRED macro series lagged 1… | 2013 (BNDX Jun 2013; … | **undisclosed** |
| 35 | `novell_bond_ui1` | Bond UI1 | Paul Novell (Investing for a Livin… | macro | monthly, last trading day close (AS default;… | HYG,LQD,BNDX,EMB / IEF,TLT,GLD / – / cash | FRED/ALFRED UNRATE vintages lagged 1 month; 3-month T-bill series for cash | 2013 (BNDX Jun 2013) | partial |
| 36 | `novell_tactical_bond` | Tactical Bond Strategy | Paul Novell (Investing for a Livin… | momentum-rotation | monthly, last trading day close; full rebala… | IEF,TLT,TIP,LQD,HYG,BNDX,EMB / – / – / cash | 3-month T-bill series for cash | 2013 (BNDX Jun 2013);… | full |
| 37 | `quantpedia_trendycmacro` | TrendYCMacro | Ďurian and Radovan Vojtko (Quantpe… | macro | monthly; signal and trade at the close of th… | SPY / – / – / BIL | FRED/ALFRED RRSFS (vintage), lagged 1 month; FRED/ALFRED INDPRO (vintage), lagg… | 1994 approx (SPY 1993… | partial |
| 38 | `quantpedia_pragmatic_aa` | Pragmatic Asset Allocation | Radovan Vojtko and Javorská (Quant… | momentum-rotation | 4 annual tranches (25% each) traded at the c… | ACWI,QQQ,EEM / IEF,GLD,BIL / – / cash | month-end 10-year and 3-month Treasury yields (e.g., FRED DGS10, DTB3/DGS3MO; a… | 2009 approx (ACWI 200… | full |
| 39 | `quantpedia_gold_cross_asset_momentum` | Gold Cross-Asset Momentum | Cyril Dujava (Quantpedia) | trend-following | monthly; signal and trade at the close of th… | GLD / – / IEF / cash | 13-week T-bill return for cash | 2005 approx (GLD 2004… | full |
| 40 | `zakamulin_optimal_trend_following` | Optimal Trend Following | Valeriy Zakamulin and Javier Giner | trend-following | monthly; signal and trade at the close of th… | SPY / – / – / cash | 13-week T-bill return for cash | 1996 approx (SPY 1993… | partial |
| 41 | `aspect_risk_managed_momentum` | Risk Managed Momentum (RMM) | Bard Malovany / Aspect Partners | momentum-rotation | monthly; AS assumes execution at the month-e… | DBC / – / – / cash | undisclosed | unknown (at least 200… | **undisclosed** |
| 42 | `pitkajarvi_us_cross_asset_momentum` | US Cross-Asset Momentum | Aleksi Pitkäjärvi, Matti Suominen,… | trend-following | monthly; signal near and trade at the close … | SPY / IEF / – / cash | – | 2003 approx (IEF 2002… | full |
| 43 | `clare_us_risk_parity_trend` | US Risk Parity Trend-Following | Andrew Clare, James Seaton, Peter … | risk-parity | monthly; signal and trade at the close of th… | SPY,IWM,IEF,DBC,VNQ / – / – / cash | 13-week T-bill return for cash | 2007 approx (DBC 2006… | partial |
| 44 | `clare_global_risk_parity_trend` | Global Risk Parity Trend-Following | Andrew Clare, James Seaton, Peter … | risk-parity | monthly; signal and trade at the close of th… | SPY,EFA,EEM,IEF,BWX,DBC,RWO / – / – / cash | 13-week T-bill return for cash | 2009 approx (RWO 2008… | partial |
| 45 | `garg_momentum_turning_points` | Momentum Turning Points | Ashish Garg, Christian L. Goulding… | trend-following | monthly; signal and trade at the close of th… | SPY,EFA,IEF,BWX,DBC,GLD / – / – / cash | 13-week T-bill monthly returns; Ken French market excess returns from 1926-07 (… | 2008 approx (BWX 2007… | partial |
| 46 | `baltussen_predicting_bond_returns` | Predicting Bond Returns | Guido Baltussen, Martin Martens, O… | macro | monthly; signal and trade at the close of th… | IEF / – / S&P 500 price index,DBC / cash | month-end 10-year Treasury yield and 13-week T-bill yield (FRED DGS10/GS10, DTB… | 2007 approx for tradi… | partial |
| 47 | `worldbank_regime_based_saa` | Regime-Based Strategic Asset Allocation | Eric Bouyé and Jérôme Teiletche (W… | static | unknown (likely periodic rebalance to fixed … | – / – / – / – | original paper (portfolio weights and asset-class definitions) | unknown | **undisclosed** |
| 48 | `sun_spf_recession_probability` | SPF Recession Probability (AS reinterpretati… | Yulong Sun (AS-modified) | macro | signals quarterly at the close of the last t… | SPY / IEF / – / cash | Philadelphia Fed SPF Mean_RECESS_Level.xlsx (mean probability of real GNP/GDP d… | 2003 approx (IEF 2002… | full |
| 49 | `engineeredportfolio_accelerating_dual_momentum` | Accelerating Dual Momentum (ADM) | EngineeredPortfolio.com (author no… | momentum-rotation | monthly; signal at the close of the last tra… | SPY,SCZ / TLT,TIP / – / – | – | 2008 (SCZ launched De… | full |
| 50 | `movementcapital_composite` | Composite Strategy | Movement Capital (movement.capital… | trend-following | monthly; signals and trades at the close of … | SPY,EFA / IEF,TIP / SHV / – | FRED/ALFRED RRSFS (real retail and food services sales), INDPRO, UNRATE - vinta… | 2007 (SHV launched Ja… | partial |
| 51 | `stoken_active_combined_asset` | Active Combined Asset (ACA) - Daily | Dick Stoken | trend-following | daily signal check at the close, trade at th… | SPY,GLD,VNQ / IEF,TLT / – / – | – | 2004-11 (GLD; VNQ Sep… | full |
| 52 | `stoken_active_combined_asset_monthly` | Active Combined Asset (ACA) - Monthly | Dick Stoken (month-end conversion … | trend-following | monthly; signals and trades only at the clos… | SPY,GLD,VNQ / IEF,TLT / – / – | – | 2004-11 (GLD; VNQ Sep… | full |
| 53 | `neddavis_three_way_model` | Three Way Model | Ned Davis (Ned Davis Research) | other | unknown (no public AS description); AS inclu… | SPY / TLT,GLD / – / cash | T-bill rate for cash | 2004-11 (GLD) | **undisclosed** |
| 54 | `jpm_efficiente_index` | Efficiente Index | J.P. Morgan | risk-parity | monthly; optimise at the close of the last t… | SPY,IWM,EFA,EEM,VNQ,DBC,GLD,HYG,EMB,LQD / TLT,TIP / – / cash | a constrained quadratic/convex optimiser | 2008 (EMB Dec 2007; H… | full |
| 55 | `carlson_defense_first` | Defense First | Thomas Carlson | momentum-rotation | monthly; signals at the close of the last tr… | SPY / TLT,GLD,PDBC,UUP / BIL / – | pre-ETF: long Treasury TR, gold spot, commodity index TR, US Dollar Index (plus… | 2007 (UUP Feb 2007, B… | full |
| 56 | `nlx_haa_60_40` | Hybrid Asset Allocation 60/40 | NLX Finance (variant of Keller & K… | trend-following | monthly; signals and trades at the close of … | SPY / IEF / TIP / cash | – | 2003-12 (TIP; BIL Jun… | partial |
| 57 | `choi_dividend_growth_allocation` | Dividend & Growth Allocation (DGA) | Paul Choi | macro | monthly; signals and trades at the close of … | QQQ,SCHD / TLT,PDBC / TIP / cash | FRED T10Y3MM from June 2019 onward; before June 2019 AS computes the 10y-3m spr… | 2011-11 (SCHD launche… | full |
| 58 | `glenn_paired_switching` | Paired Switching Strategy | Lewis Glenn (per AllocateSmartly);… | momentum-rotation | quarterly at the last trading day of each ca… | SPY / TLT / – / – | – | 2002-07 (TLT) | partial |
| 59 | `glenn_quint_switching_filtered` | Quint Switching Filtered (QSF) | Lewis Glenn | momentum-rotation | monthly; signals and trades at the close of … | SPY,QQQ,EFA,EEM,TLT / IEF / – / – | – | 2003-04 (EEM) | full |
| 60 | `link_global_growth_cycle` | Global Growth Cycle (GGC) | Grzegorz Link | macro | monthly on the 15th calendar day (or the nex… | SPY / – / – / cash | OECD Composite Leading Indicator by country, monthly, with historical vintages … | 1993 (SPY) | full |
| 61 | `link_global_growth_cycle_enhanced` | Global Growth Cycle Enhanced (GGC Enhanced) | Grzegorz Link | macro | monthly, last trading day close (AS 'Monthly… | SPY,IEFA / AGG / – / cash | OECD CLI by country with vintages, 1-month reporting lag | 2003-09 (AGG; EFA 200… | full |
| 62 | `virag_momentum_based_balancing` | Momentum Based Balancing | Mark Virag | momentum-rotation | monthly; signal and execution at the close o… | SPY,IWM,XLB,EFA,EEM,VNQ,IEF,TLT,TIP / – / – / cash | 3-month T-bill rate (FRED DTB3/TB3MS) for cash return | 2005 (VNQ launched Se… | partial |
| 63 | `elm_eeyd_valuation_only` | Excess Earnings Yield Dynamic - Valuation On… | James White and Victor Haghani (El… | valuation | monthly; signal and execution at the close o… | SPY / TIP / – / – | Shiller monthly CAPE (Shiller online data, ie_data.xls); 10-year TIPS real yiel… | 2004 (TIP launched De… | partial |
| 64 | `elm_eeyd_with_momentum` | Excess Earnings Yield Dynamic with Momentum | James White and Victor Haghani (El… | valuation | monthly; signal and execution at the close o… | SPY / TIP / – / – | Shiller monthly CAPE; 10-year TIPS real yield (FRED DFII10 from 2003; earlier s… | 2004 (TIP launched De… | partial |
| 65 | `vitral_multi_asset_momentum` | Multi-Asset Momentum | Zambrano and Rizzolo (Vitral Advis… | momentum-rotation | unknown (AS default would be monthly, last t… | – / – / – / – | unknown until rules are located | unknown | **undisclosed** |
| 66 | `piard_annual_seasonality` | Annual Seasonality | Fred Piard | other | monthly at the close of the last trading day… | EWS,EWZ,EWG / – / – / cash | 3-month T-bill rate for cash | 2000 (EWZ launched Ju… | full |
| 67 | `sell_in_may_halloween` | Sell in May / Halloween Indicator | N/A (classic anomaly; academic ref… | other | two switches per year at month-end closes: b… | SPY / – / – / cash | 3-month T-bill rate; pre-1993: S&P 500 TR index | 1993 (SPY launched Ja… | full |
| 68 | `rpv_best_value` | Risk Premium Value - Best Value | N/A (AllocateSmartly test; related… | valuation | monthly; signal and execution at the close o… | SPY,LQD,TLT / – / – / cash | long-term Treasury yield (series not stated; e.g. FRED DGS10/DGS20/DGS30) (unce… | 2003 (LQD and TLT lau… | partial |
| 69 | `rpv_weighted` | Risk Premium Value - Weighted | N/A (AllocateSmartly test; related… | valuation | monthly; signal and execution at the close o… | SPY,LQD,TLT / – / – / cash | same yield/earnings series as rpv_best_value (series unspecified by AS); 3-mont… | 2003 (LQD and TLT lau… | partial |
| 70 | `dalio_all_weather` | All-Weather/All-Seasons Portfolio | Ray Dalio (as published by Tony Ro… | static | annually (AS assumption for these four-seaso… | SPY,TLT,IEF,GLD,DBC / – / – / – | – | 2006 (DBC launched Fe… | partial |
| 71 | `browne_permanent_portfolio` | Permanent Portfolio | Harry Browne | static | annually (AS assumption); exact date not sta… | SPY,TLT,GLD / – / – / cash | 3-month T-bill rate for cash | 2005 (GLD launched No… | partial |
| 72 | `portfoliocharts_golden_butterfly` | Golden Butterfly | Tyler (PortfolioCharts.com) | static | annually (AS assumption); exact date not sta… | SPY,IWN,TLT,GLD / SHY / – / – | – | 2005 (GLD Nov 2004; I… | partial |
| | | **— Reviewed in AS blog posts, not tracked —** | | | | | | | |
| 73 | `bilello_gayed_lumber_gold` | Lumber-Gold Strategy (intermarket risk rotat… | Charles Bilello and Michael Gayed | other | weekly; signal computed and traded at the cl… | SPY / IEF / LB1 (generic 1st lumber futures),gold price (series not specified by AS) / – | weekly (from daily) closes of generic front-month lumber futures (Bloomberg LB1… | 2002 (IEF); AS backte… | partial |
| 74 | `smith_bkln` | BKLN 3/12-Day Moving Average Strategy | Cliff Smith | trend-following | daily; evaluated and traded at each day's cl… | BKLN / – / – / cash | T-bill rate for cash return | 2011 (BKLN launched 0… | partial |
| 75 | `as_countercyclical_trend` | Countercyclical Trend Following | Undisclosed (AS withheld the autho… | macro | economic regime set monthly at the last trad… | SPY,IWN,GLD / LQD,IEF / – / – | FRED BAMLH0A0HYM2 (daily, from 12/1996); FRED BAA / DBAA and DGS10 (pre-1997 HY… | 2004 (GLD 11/2004; IW… | partial |
| 76 | `jpm_trending_fast_slow` | Trending Fast and Slow (volatility-switched … | Authors of 'Trending Fast and Slow… | trend-following | monthly, last trading day close | SPY / – / – / cash | T-bill rate for cash | 1993 (SPY); 2007 if B… | partial |
| 77 | `schwartz_yield_rotation` | Yield-Based Asset Class Rotation | Harrison Schwartz | macro | daily; AS base test trades at the close of t… | SPY,GLD / TLT / – / – | FRED T10Y2Y (daily); FRED DFII20 (daily, from 07/2004); FRED DTP30A28 (daily, t… | 2004 (GLD 11/2004; TL… | partial |
| 78 | `econompic_faber_global_ath` | Buy Global Stocks at All-Time Highs (else bo… | Jake Moore (EconomPic) and Meb Fab… | trend-following | monthly, last trading day close | ACWI / AGG / – / – | monthly close of ACWI or global equity index (long history from GFD/MSCI) | 2008 (ACWI 03/2008; A… | full |
| 79 | `lazy_mans_momentum` | Lazy Man's Momentum Strategy (country rotati… | Not verified (SSRN working paper 5… | momentum-rotation | semi-annually, at the close of the last trad… | 22 country equity indices (list per source paper; not given by AS, not verified) / – / – / – | ACWI for benchmark | 1996 (most iShares MS… | partial |
| 80 | `quantpedia_commodity_frontrun_seasonality` | Front-Running Commodity Seasonality (with co… | Cyril Dujava (Quantpedia) | other | monthly, last trading day close | DBA,DBB,DBE,DBP / – / – / cash | monthly returns from the same | 2007 (all four Invesc… | full |
| 81 | `quantpedia_commodity_mom_rev_corr` | Commodity Momentum/Reversal with Intra-Marke… | Margareta Pauchlyova (Quantpedia) | momentum-rotation | monthly, last trading day close | DBA,DBB,DBE,DBP / – / – / – | – | 2007 | full |
| 82 | `quantpedia_country_frontrun_seasonality` | Front-Running Seasonality in Country ETFs | Sona Beluska (Quantpedia) | other | monthly, last trading day close | SPY,EWU,EWG,EWQ,EWI,EWD,EWN,EWP,EWK,EWL,EWC,EWJ,EWW,EWM,EWA,EWS,EWY,EWT,EWZ,EWH,EZA,FXI,INDY /… | – | 2009 (INDY 11/2009; F… | full |
| 83 | `as_dist_1yr_high` | 12-Month Momentum with Distance-to-1-Year-Hi… | Allocate Smartly | trend-following | monthly, last trading day close | SPY / – / – / BIL | monthly dividend-adjusted S&P 500 / SPY closes; 13-week T-bill rate | 1993 (SPY); 2007 with… | partial |
| 84 | `philecon_aiae_timing` | Aggregate Investor Allocation to Equities (A… | Philosophical Economics (Jesse Liv… | valuation | monthly, last trading day close | SPY / – / – / BIL | FRED/ALFRED quarterly Z.1 series: NCBEILQ027S, FBCELLQ027S, FGSDODNS, CMDEBT, B… | 1993 (SPY); 2007 with… | full |
| 85 | `hartley_schwarz_eom_treasury` | End-of-Month / Second-Half-of-Month Treasury… | Jonathan Hartley and Krista Schwar… | other | calendar-based daily timing, close-to-close | TLT / – / – / cash | trading calendar to identify last trading days / normalized days | 2002 (TLT/IEF 07/2002… | partial |
| 86 | `as_sector_ff5_alpha` | Sector Rotation with Fama-French Alphas | Undisclosed (AS withheld the paper… | momentum-rotation | monthly, last trading day close | XLB,XLE,XLF,XLI,XLK,XLP,XLU,XLV,XLY,XLRE / – / – / cash | Ken French data library: Fama/French 5 Factors (2x3), monthly, incl. RF | 1998 (original 9 SPDR… | partial |
| 87 | `bilello_gayed_utilities` | Utilities Beta Rotation (utilities vs market… | Charles Bilello and Michael Gayed … | momentum-rotation | weekly, close of the last trading day of the… | VTI,XLU / – / – / – | optional: Ken French industry and market returns for the original long test | 2001 (VTI 05/2001; XL… | partial |
| 88 | `as_agg_taa_allocation` | Aggregate TAA Allocation as a Trading Signal | Allocate Smartly | other | monthly at month-end close (best after costs… | SPY,VNQ,IEFA,VNQI / IEF,LQD,BWX,GLD,PDBC / – / cash | – | n/a (AS tests from 20… | **undisclosed** |

## Entries that are undisclosed or placeholders (cannot be fully specified)

- `tresidder_optimumv`: Rules undisclosed (proprietary; AS tracks under licence). Only concept known.
- `tresidder_optimum3`: Rules undisclosed; universe of 15 ETFs and broad structure known.
- `tresidder_all_weather_quad_momentum`: Rules undisclosed (proprietary).
- `novell_spy_comp`: Economic indicator set and trend rule are proprietary (members-only on author site).
- `novell_bond_comp`: Economic indicator set is proprietary.
- `aspect_risk_managed_momentum`: Black box; AS withholds rules. Only asset mapping hints known.
- `worldbank_regime_based_saa`: No AS post; original paper not retrievable (SSRN 403, search budget exhausted). Placeholder.
- `neddavis_three_way_model`: No public AS post or original rules found; only the asset set (SPY/TLT/GLD/cash) is known.
- `vitral_multi_asset_momentum`: No AS post; original paper not located (search budget exhausted). Placeholder.
- `as_agg_taa_allocation`: Needs the aggregate allocation of all AS strategies (members-only data) - not replicable stand-alone.

## Entries with flagged assumptions (partial)

- `faber_ivy_static`: Rebalance frequency of AS's static Ivy not stated.
- `faber_gtaa13`: How AS maps the small-cap momentum sleeve is unclear.
- `faber_12m_high_switch`: Original Faber publication not identified; AS rules used.
- `faber_sector_relative_strength`: AS-specific top-N/lookback/filter not public; follows Faber 2010 paper.
- `faber_tactical_yield`: Exact corporate-yield series unverified.
- `alphaarchitect_raa_balanced`: Sleeve weights and signal combination from unverified recollection of the book (40/20/40 eq/real/bonds; 50% MA + 50% TMOM).
- `alphaarchitect_raa_aggressive`: Sleeve weights unverified (60/20/20 assumed).
- `varadi_minimum_correlation`: AS lookback/variant not public (60 trading days assumed).
- `varadi_growth_inflation_sector_timing`: AS turnover-reduction tweak undisclosed; original rules given.
- `varadi_inflation_compass_original`: AS pre-2003 breakeven-inflation proxy undisclosed.
- `varadi_inflation_compass_enhanced`: Ensemble parameter grid not public.
- `newfound_diversified_dual_momentum`: No public rules post; monthly rebalance and T-bill hurdle assumed.
- `as_max_sharpe`: Expected-return estimator and risk-free rate unstated.
- `novell_bond_ui1`: Reconstructed from author posts; AS risk-off basket uncertain.
- `quantpedia_trendycmacro`: AS macro inputs differ slightly from the Quantpedia blog; AS version specified.
- `zakamulin_optimal_trend_following`: 30 lag weights read approximately from a chart.
- `clare_us_risk_parity_trend`: Volatility window frequency (daily vs monthly) not fully pinned down.
- `clare_global_risk_parity_trend`: Volatility window frequency not fully pinned down.
- `garg_momentum_turning_points`: AS flavour (single vs 6-asset), weighting and long-only handling assumed.
- `baltussen_predicting_bond_returns`: z-score window not fully specified.
- `movementcapital_composite`: Macro indicator definitions inferred; original page gone.
- `nlx_haa_60_40`: Original NLX publication not found; AS description used.
- `glenn_paired_switching`: Lookback (3m) and quarterly frequency uncertain.
- `virag_momentum_based_balancing`: Original paper not retrieved; AS rules used.
- `elm_eeyd_valuation_only`: TIPS-yield/CPI series used by AS not named.
- `elm_eeyd_with_momentum`: Momentum overlay documented only by AS.
- `rpv_best_value`: Exact yield/earnings series and averaging window start not named by AS.
- `rpv_weighted`: Exact series not named; weights assumed proportional to positive scores.
- `dalio_all_weather`: Weights are the widely published Robbins version (30/40/15/7.5/7.5); AS rebalance date unstated.
- `browne_permanent_portfolio`: AS rebalance date unstated (annual).
- `portfoliocharts_golden_butterfly`: AS rebalance date unstated (annual).
- `bilello_gayed_lumber_gold`: Original paper not reachable (403); AS rules used.
- `smith_bkln`: Original source not reachable (403); AS rules used.
- `as_countercyclical_trend`: AS withheld the source paper; rules from AS post.
- `jpm_trending_fast_slow`: Source paper behind login; authors not confirmed.
- `schwartz_yield_rotation`: Gold-signal sign inferred.
- `lazy_mans_momentum`: 22-country list and source authors unknown.
- `as_dist_1yr_high`: Source paper not reachable; AS test rules used.
- `hartley_schwarz_eom_treasury`: Original paper not reachable; AS rules used.
- `as_sector_ff5_alpha`: AS withheld the source; rules from AS post.
- `bilello_gayed_utilities`: Source attribution inferred.

## Requested names that are not on AS's list

None of the following appear on AS's public tracked list, and none has a dedicated test among AS's 229 public blog posts. They are **not** included:
- Hedgefundie's Excess Return;
- Bensdorp;
- Logical Invest;
- Scott's Investments "Ivy 10 timing";
- generic lazy or Canadian portfolios;
- "simple mean reversion";
- P/E and yield-curve timing as stand-alone strategies.

Related items that are covered:
- "Quint Switching" is Lewis Glenn's (`glenn_quint_switching_filtered`).
- Yield-curve and valuation inputs appear inside TrendYCMacro, Pragmatic AA, Dividend & Growth, RPV, EEYD and AIAE.
- "The Trend is Our Friend" (Clare et al.) is the source of the two risk-parity trend-following strategies.
- TrendXplorer is JW Keuning's blog, which is in the Keller scope.

## Strategy cards

### 1. Ivy Portfolio (static 5-asset equal weight) (`faber_ivy_static`)

*Mebane Faber & Eric Richardson*, family **static**, AS status **tracked**, spec status **partial**.

- **Source:** The Ivy Portfolio: How to Invest Like the Top Endowments and Avoid Bear Markets (book, Wiley) (2009), https://mebfaber.com/books/
- **AS page:** none (no public AS post)
- **Rebalance:** periodic rebalance back to fixed 20% weights; frequency not stated by AS for Ivy (AS says its buy & hold comparison portfolios such as Golden Butterfly/All-Weather/Permanent are rebalanced annually; monthly also plausible) (uncertain). Trades at the close of the last trading day of the month.
- **Universe:** risky ['SPY', 'EFA', 'IEF', 'VNQ', 'DBC']; defensive []; canary []; cash None
- **Signal:** None (buy & hold). Target w_i = 0.20 for each of the 5 assets at every rebalance.
- **Data needs:** monthly (month-end) dividend-adjusted closes for SPY, EFA/IEFA, IEF, VNQ, DBC/PDBC; long-history index proxies for pre-ETF periods (S&P 500 TR, MSCI EAFE TR, 10y Treasury TR, NAREIT TR, GSCI TR)
- **ETF-only start:** 2006 (DBC Feb-2006; VNQ 2004, IEF 2002, EFA 2001, SPY 1993)
- **In plain English:** A simple endowment-style buy & hold portfolio: one fifth each in US stocks, foreign stocks, Treasuries, real estate and commodities. Nothing is ever timed; the only activity is periodically resetting the five slices back to 20%.
- **Rules:**
  1. Hold 20% each in US large-cap equities (SPY), developed international equities (EFA; IEFA after AS's 2025 ETF change), US 7-10y Treasuries (IEF), US REITs (VNQ) and diversified commodities (DBC; PDBC stitched on from ~Dec 2022).
  2. No timing filter and no cash sleeve: the portfolio is always 100% invested.
  3. At each rebalance date (close of the last trading day of the rebalance month) reset all five weights to exactly 20%; let weights drift between rebalances.
  4. Before an asset has data, AS's convention elsewhere is to split the portfolio evenly among available assets (not stated specifically for Ivy) (uncertain).
- **Notes:** AS has no dedicated public post on its Ivy Portfolio. Evidence it is the static equal-weight version: (1) AS's 2019 public strategy-asset matrix lists Ivy with DBC, EFA, IEF, SPY, VNQ and NO cash column, whereas GTAA 5 has the same five plus Cash; (2) AS lists Ivy among its buy & hold portfolios (All-Weather, Permanent, Golden Butterfly); (3) in AS monthly performance tables, Ivy and GTAA 5 returns nearly coincide in months when GTAA 5 was likely fully invested (e.g. Oct-2017 1.35% vs 1.35%) but diverge sharply when GTAA 5 was partly in cash (e.g. Dec-2018 -4.74% vs -2.76%; Jan-2019 +6.85% vs +0.27%), i.e. Ivy has no trend filter. The book itself also presents the 10-month SMA timing overlay (that tactical version is tracked separately by AS as GTAA 5) and larger Ivy 10/Ivy 20 versions; AS appears to use only the 5-asset version. Rebalance frequency for AS's Ivy is not stated publicly (uncertain). Book ETF tickers not verified (book not accessible); AS conforms to its representative ETFs regardless.

### 2. Global Tactical Asset Allocation 5 (GTAA 5) (`faber_gtaa5`)

*Mebane Faber*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** A Quantitative Approach to Tactical Asset Allocation (Journal of Wealth Management 2007; SSRN working paper 2006, updated Feb 2009 and Feb 2013) (2007), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- **AS page:** none (no public AS post)
- **Rebalance:** monthly; signal at the close of the last trading day of the month, traded at that same close; entire portfolio rebalanced to fixed slices every month even with no signal change
- **Universe:** risky ['SPY', 'EFA', 'IEF', 'VNQ', 'DBC']; defensive []; canary []; cash BIL
- **Signal:** TREND_i = 1 if P_i,t > SMA10_i,t else 0, where P = dividend-adjusted (total return) close on the last trading day of month t and SMA10 = arithmetic mean of the 10 most recent month-end adjusted closes including month t.
- **Data needs:** daily (for month-end) dividend-adjusted closes for SPY, EFA/IEFA, IEF, VNQ, DBC/PDBC, BIL; 3-month T-bill rate/total return for cash before BIL; pre-ETF index proxies back to 1972 (10 months of history before a 1973 start)
- **ETF-only start:** 2007 (BIL May-2007; risky assets all available from DBC Feb-2006)
- **In plain English:** Split the portfolio into five equal slices: US stocks, foreign stocks, Treasuries, real estate and commodities. Each month, keep a slice in its asset only if that asset is above its 10-month average price; otherwise park that slice in T-bills.
- **Rules:**
  1. Assign a fixed 20% slice to each of five assets: SPY (US equities), EFA (intl developed equities; IEFA from 2025), IEF (US 7-10y Treasuries), VNQ (US REITs), DBC (commodities; PDBC stitched on from ~Dec 2022).
  2. At the close on the last trading day of each month compute each asset's 10-month SMA of month-end adjusted closes (current month-end included).
  3. If an asset's month-end close is above its 10-month SMA, hold that asset at 20%; otherwise put that 20% slice in cash (T-bills, BIL).
  4. Slices are independent: an asset's weight never depends on the others, and a failing slice is never redistributed to other assets.
  5. Hold until the last trading day of the following month; rebalance all slices back to 20% monthly regardless of signal changes.
- **Notes:** Verified against Faber 2013 update (buy rule: monthly price > 10-month SMA; sell to cash when below; signals updated only at month-end; total-return series; cash = 90-day T-bills; equal 20% weights; FAQ: rebalanced monthly). AS confirms the 20% slices, 10-month MA, cash, and monthly full rebalance (tax-efficient TAA post) and a 1973 backtest start. Faber's original (and AS's) treatment of 'price' is the total-return/adjusted series. Equality case (close == SMA) unspecified; treat as not above. Faber also tested alternatives (10y bonds as cash, leverage) not used by AS.

### 3. Global Tactical Asset Allocation 13 (GTAA 13 / GTAA Moderate) (`faber_gtaa13`)

*Mebane Faber*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** A Quantitative Approach to Tactical Asset Allocation, February 2013 update (Extension 1: More Asset Classes; 'GTAA Moderate') (2013), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- **AS page:** none (no public AS post)
- **Rebalance:** monthly; signal at the close of the last trading day of the month, traded at that close; all slices reset to target weights monthly
- **Universe:** risky ['IWD', 'MTUM', 'IWN', 'IWM', 'EFA', 'EEM', 'IEF', 'BWX', 'LQD', 'TLT', 'DBC', 'GLD', 'VNQ']; defensive []; canary []; cash BIL
- **Signal:** TREND_i = 1 if P_i,t > SMA10_i,t (10 most recent month-end dividend-adjusted closes incl. current), else 0.
- **Data needs:** month-end dividend-adjusted closes for the 13 ETFs (+ BIL); pre-ETF proxies: factor-style US equity series (value, momentum, small value, small momentum), MSCI EAFE/EM, 10y/30y Treasury, intl govt bond, US corporate bond, GSCI, gold, NAREIT total-return series
- **ETF-only start:** 2013 (MTUM Apr-2013; BWX 2007, BIL 2007, DBC 2006)
- **In plain English:** A 13-slice global portfolio (stocks by style and region, several kinds of bonds, commodities, gold and real estate), each slice with a fixed weight. Every month a slice stays invested only if its asset is above its 10-month average; otherwise that slice sits in T-bills.
- **Rules:**
  1. Fixed target weights (Faber 2013): US large-cap value IWD 5%, US large-cap momentum MTUM 5%, US small-cap value IWN 5%, US small-cap momentum 5% (AS proxy: IWM per its Agg post; see notes), intl developed EFA 10%, emerging EEM 10%, US 10y Treasuries IEF 5%, intl 10y government bonds BWX 5%, US corporate bonds LQD 5%, US 30y Treasuries TLT 5%, commodities DBC 10%, gold GLD 10%, REITs VNQ 20%.
  2. At each month-end close, for each asset: if close > 10-month SMA, hold its full target weight; otherwise move that asset's slice to cash (BIL).
  3. No cross-sectional ranking; slices are independent and never redistributed to other assets.
  4. Hold until the next month-end; rebalance every slice to its target weight monthly.
  5. Apply AS 2025 ETF changes if replicating current AS: IWD->VTV, IWN->VBR, EFA->IEFA, EEM->IEMG; DBC->PDBC (stitched ~Dec 2022).
- **Notes:** Weights and asset list verified from the 2013 SSRN update (table on p.43/49: 5,5,5,5,10,10,5,5,5,5,10,10,20). AS has no public rules post for GTAA 13, but its Agg 3/6 post describes the same 13-asset universe and says the original GTAA 13 controlled how much each asset category could take (consistent with fixed weights). AS's 2019 public matrix shows GTAA 13 holding BWX, DBC, EEM, EFA, GLD, IEF, IWD, IWN, LQD, MTUM, TLT, VNQ + Cash (12 ETFs, no IWM), whereas Agg 3/6 includes IWM as the stand-in for US small-cap momentum. So the mapping of the 5% small-cap-momentum slice in AS's GTAA 13 is unverified (IWM, or folded into another ETF such as MTUM/IWN) (uncertain). The 10-month SMA is assumed to apply per asset as in GTAA 5 (paper describes the extension as the same timing model on more assets). Handling of assets before data exists (AS excludes EEM pre-1989 and BWX pre-mid-2002 in Agg) is not documented for GTAA 13 (uncertain: slice to cash vs redistributed).

### 4. Global Tactical Asset Allocation – Aggressive 3 (GTAA Agg 3) (`faber_gtaa_agg3`)

*Mebane Faber*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** A Quantitative Approach to Tactical Asset Allocation, February 2013 update (Extension 3: GTAA Aggressive); ranking method from 'Relative Strength Strategies for Investing' (2010) (2013), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- **AS page:** https://allocatesmartly.com/aggressive-global-tactical-asset-allocation/
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; full rebalance monthly even without position changes
- **Universe:** risky ['IWD', 'MTUM', 'IWN', 'IWM', 'EFA', 'EEM', 'IEF', 'BWX', 'LQD', 'TLT', 'DBC', 'GLD', 'VNQ']; defensive []; canary []; cash BIL
- **Signal:** MOM_i = (r1 + r3 + r6 + r12)/4 with r_k = P_t/P_{t-k months} - 1 on month-end dividend-adjusted closes (P_t = current month-end close, so r1 includes the latest month). TREND_i = 1 if P_t > SMA10 (10 month-end adjusted closes incl. current).
- **Data needs:** month-end dividend-adjusted closes for the 13 ETFs and BIL (13 months of history needed for r12, 10 for SMA); pre-ETF proxies for each asset class back to ~1980
- **ETF-only start:** 2013 (MTUM Apr-2013)
- **In plain English:** Each month, rank 13 global asset classes by their average return over the last 1, 3, 6 and 12 months and put a third of the portfolio in each of the top three. Any of those three that has fallen below its 10-month average is replaced by T-bills for that third.
- **Rules:**
  1. At the close on the last trading day of the month compute MOM_i (simple average of 1, 3, 6 and 12-month total returns) for each of the 13 assets.
  2. Rank assets by MOM_i descending and select the top 3 (relative momentum). Tie-break not specified (use deterministic order, e.g. higher r12).
  3. Each selected asset gets a fixed 1/3 slice. If a selected asset's close is below its 10-month SMA, its 1/3 slice goes to cash (BIL) instead; the slice is NOT passed to the 4th-ranked asset.
  4. Hold until the last trading day of the next month; rebalance the whole portfolio monthly.
  5. Assets lacking history are excluded from ranking (AS: EEM excluded before 1989, BWX before mid-2002).
  6. AS 2025 ETF changes: IWD->VTV, IWN->VBR, EFA->IEFA, EEM->IEMG; DBC->PDBC (~Dec 2022).
- **Notes:** Rules taken from the AS post and verified against Faber 2013 (top 6 or top 3 of 13 ranked on average of 1/3/6/12-month total returns; only held if above long-term MA, else that portion to cash). AS notes the absolute-momentum filter binds only ~5% of months for Agg 3. AS results are well below the paper's, which AS attributes mainly to Fama-French proxies in the original. Faber's 2010 RS paper used a 1/3/6/9/12 combination for its own tests, but the 2013 paper (and AS) use 1/3/6/12. Tie-breaking unspecified. AS live-trading nuance: signals use the closing auction print; a tiny price difference vs last real-time price once flipped an Agg 6 slice (AS 'when the close is not really the close' post).

### 5. Global Tactical Asset Allocation – Aggressive 6 (GTAA Agg 6) (`faber_gtaa_agg6`)

*Mebane Faber*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** A Quantitative Approach to Tactical Asset Allocation, February 2013 update (Extension 3: GTAA Aggressive) (2013), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- **AS page:** https://allocatesmartly.com/aggressive-global-tactical-asset-allocation/
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; full rebalance monthly
- **Universe:** risky ['IWD', 'MTUM', 'IWN', 'IWM', 'EFA', 'EEM', 'IEF', 'BWX', 'LQD', 'TLT', 'DBC', 'GLD', 'VNQ']; defensive []; canary []; cash BIL
- **Signal:** MOM_i = (r1 + r3 + r6 + r12)/4, r_k = P_t/P_{t-k} - 1 on month-end dividend-adjusted closes (current month-end included). TREND_i = 1 if P_t > SMA10 of month-end adjusted closes (incl. current).
- **Data needs:** month-end dividend-adjusted closes for 13 ETFs + BIL; pre-ETF index proxies back to ~1980
- **ETF-only start:** 2013 (MTUM Apr-2013)
- **In plain English:** Same as the Agg 3 version, but it holds the six strongest of the 13 asset classes, one sixth each. Any of the six that is below its 10-month average is swapped for T-bills.
- **Rules:**
  1. At the month-end close compute MOM_i for the 13 assets.
  2. Select the 6 assets with the highest MOM_i (tie-break unspecified).
  3. Each selected asset gets a fixed 1/6 slice; if it closes below its 10-month SMA its 1/6 goes to cash (BIL), not to the 7th-ranked asset.
  4. Hold until next month-end; rebalance the full portfolio monthly.
  5. Exclude assets without history (AS: EEM before 1989, BWX before mid-2002); same 2025 ETF substitutions as Agg 3.
- **Notes:** Identical to Agg 3 except top_n = 6 and 1/6 slices (AS post). Faber's 2013 paper presents top-6 as the main Aggressive model and top-3 as a variant. AS: trend filter changes allocations in ~20% of months for Agg 6. AS documented a real-time vs official-close discrepancy on 11/30/2021 that moved ~17% from cash to TLT in Agg 6.

### 6. The Trinity Portfolio (Lite) (`faber_trinity_lite`)

*Mebane Faber (Cambria Investment Management)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** The Trinity Portfolio (Cambria white paper; AS links Trinity_WP_122816_A.pdf, dated Dec 2016) (2016), https://www.cambriainvestments.com/wp-content/uploads/2017/01/Trinity_WP_122816_A.pdf
- **AS page:** https://allocatesmartly.com/meb-fabers-trinity-portfolio-lite/
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; whole portfolio (static + dynamic halves) rebalanced monthly
- **Universe:** risky ['MTUM', 'IWD', 'EFV', 'EEM', 'LQD', 'TLT', 'BWX', 'TIP', 'DBC', 'GLD', 'VNQ']; defensive []; canary []; cash BIL
- **Signal:** For each of 10 entities (US equity = MTUM+IWD composite, EFV, EEM, LQD, TLT, BWX, TIP, DBC, GLD, VNQ): MOM = (r1+r3+r6+r12)/4 on month-end dividend-adjusted closes (current month-end included); TREND = 1 if month-end close > SMA of last 10 month-end adjusted closes.
- **Data needs:** month-end dividend-adjusted closes for MTUM, IWD, EFV, EEM, LQD, TLT, BWX, TIP, DBC/PDBC, GLD, VNQ, BIL; pre-ETF proxies back to 1975 (US momentum and value factor series, intl value, EM, corp bonds, long Treasuries, intl govt bonds, TIPS proxy, commodities, gold, REITs)
- **ETF-only start:** 2013 (MTUM Apr-2013; BWX/BIL 2007, DBC 2006, EFV 2005)
- **In plain English:** Half the money sits permanently in a global market-style mix of stocks, bonds, commodities, gold and real estate (with value and momentum tilts). The other half is invested each month in the five strongest of those assets by recent momentum, 10% each, but only if each is above its 10-month average; otherwise that 10% sits in T-bills.
- **Rules:**
  1. Static half (50% of portfolio, % of TOTAL portfolio): MTUM 4.50, IWD 4.50, EFV 6.75, EEM 2.25, LQD 9.90, TLT 6.75, BWX 7.20, TIP 0.90, DBC 2.50, GLD 2.50, VNQ 2.25 (sums to 50%).
  2. Dynamic half (50%): at the month-end close score each of 10 entities by the average of 1, 3, 6 and 12-month total return; MTUM and IWD are treated as ONE US-equity entity (always selected/filtered together).
  3. Select the top 5 entities (top half). Each gets a fixed 10% slice (one fifth of the dynamic half) if its close is above its 10-month SMA; otherwise that 10% goes to cash (BIL). A US-equity selection is split between MTUM and IWD (presumably 5%/5%) (uncertain).
  4. AS 2% minimum-position rule: when TIP is not selected by the dynamic half, its 0.9% static allocation is moved to TLT (so TLT static becomes 7.65%).
  5. Final weight per ETF = static weight + any dynamic slice; hold until the next month-end; rebalance monthly.
  6. Current AS tickers: EEM->IEMG and IWD->VTV after 2025 changes; DBC->PDBC (~Dec 2022).
- **Notes:** Static weights read from the allocation image in the AS post ('Trinity Permanent Allocation'). AS calls it 'Lite' because it replaces the white paper's individual-stock factor exposures (US momentum/value, intl value) with MTUM/IWD/EFV and Faber's sovereign-bond selection with BWX, and expands 10 asset classes to 11 ETFs. Original Cambria white paper could not be retrieved (links 404) so the paper's own weights/versions (e.g., different static/dynamic splits) are unverified. Ambiguities: how the MTUM+IWD composite momentum/SMA is computed (AS offers the math on request only); whether TIP's 0.9% also moves to TLT when TIP is selected but fails its SMA (likely, since the rule is about sub-2% positions) (uncertain); tie-breaks unspecified.

### 7. 12-Month High Switch [Dynamic Bond] (`faber_12m_high_switch`)

*Mebane Faber*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** 12-Month High Switch Model (Meb Faber; AS does not cite the specific publication) (None), https://mebfaber.com/
- **AS page:** https://allocatesmartly.com/meb-fabers-12-month-high-switch/
- **Rebalance:** monthly; signal at the close of the last trading day of the month, traded at that close; rebalance monthly even with no change
- **Universe:** risky ['SPY', 'EFA', 'VNQ', 'GLD', 'DBC']; defensive ['IEF']; canary []; cash BIL
- **Signal:** H12_i,t = max of month-end dividend-adjusted closes over months t-11..t (current estimated close + preceding 11 month-ends). NEAR_HIGH_i = 1 if P_i,t >= 0.95 * H12_i,t (i.e. within 5% of the 12-month high).
- **Data needs:** month-end dividend-adjusted closes for SPY, EFA/IEFA, VNQ, GLD, DBC/PDBC, IEF, BIL; pre-ETF proxies back to ~1969 (S&P 500 TR, EAFE TR, REIT TR, gold, commodity index TR, 10y Treasury TR, T-bills)
- **ETF-only start:** 2007 (BIL May-2007; DBC Feb-2006, GLD Nov-2004)
- **In plain English:** Five assets (US stocks, foreign stocks, real estate, gold, commodities) each get 20% only when they are trading within 5% of their highest month-end price of the past year. Money not used goes to intermediate Treasuries, but only if Treasuries are also near their 12-month high; otherwise it waits in T-bills.
- **Rules:**
  1. At the close on the last trading day of the month compute H12 for SPY, EFA (IEFA from 2025), VNQ, GLD and commodities (DBC, PDBC from ~Dec 2022).
  2. Allocate a fixed 20% to each of these five assets whose month-end close is within 5% of its 12-month high.
  3. Pool the unallocated 20% slices into the defensive sleeve. AS-tracked Dynamic Bond version: put the pool in IEF only if IEF is itself within 5% of its own 12-month high; otherwise put the pool in cash (BIL).
  4. Original (non-tracked) version: unallocated slices always go to IEF.
  5. Hold until the next month-end; rebalance monthly.
  6. Before an asset has sufficient history, split the portfolio evenly among the remaining assets (AS calc note; commodities data from 12/1969, VNQ proxy from 12/1971).
- **Notes:** AS tracks ONLY the Dynamic Bond variant on its platform (stated in AS post). Original Faber publication not identified/verified (AS links mebfaber.com, SSRN 962461 and cambriafunds.com/insights generically). 'Within 5%' interpreted as P >= 0.95*H12; equality and whether the high uses closes only (yes, month-end closes per AS) are as stated by AS. AS lists commodities as PDBC in this 2024 post (DBC stitched to PDBC).

### 8. Sector Relative Strength (`faber_sector_relative_strength`)

*Mebane Faber*, family **momentum-rotation**, AS status **tracked**, spec status **partial**.

- **Source:** Relative Strength Strategies for Investing (Cambria working paper, April 2010) (2010), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1585517
- **AS page:** none (no public AS post)
- **Rebalance:** monthly; signal at the close of the last trading day of the month, traded at that close
- **Universe:** risky ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY']; defensive []; canary ['SPY']; cash BIL
- **Signal:** MOM_i = average of 1, 3, 6, 9 and 12-month total returns on month-end dividend-adjusted closes (Faber 2010 'combination' ranking) (uncertain whether AS uses 1/3/6/9/12 or 1/3/6/12). HEDGE = 1 if S&P 500 (SPY) month-end close < its 10-month SMA (uncertain).
- **Data needs:** month-end dividend-adjusted closes for Select Sector SPDR ETFs, SPY and BIL; pre-1999 sector index proxies (e.g. S&P sector indices or Fama-French industry returns)
- **ETF-only start:** 2007 (BIL May-2007; sector SPDRs Dec-1998)
- **In plain English:** Each month, buy the US stock-market sectors that have risen the most over the past year (blending several look-back periods) and hold them equally. When the overall market is in a downtrend (below its 10-month average) the strategy steps aside into T-bills.
- **Rules:**
  1. At the month-end close rank the US sector ETFs by MOM_i (trailing total-return momentum).
  2. Select the top 3 sectors and weight them equally (1/3 each) (uncertain: paper reports Top 1, Top 2 and Top 3 variants; AS's choice not public).
  3. Dynamic hedge (paper's version): if the S&P 500 closes below its 10-month SMA, move the entire portfolio to cash (T-bills/BIL) (uncertain whether AS uses this market-level filter or a per-sector 10-month SMA filter; the paper says both give similar results).
  4. A sector that drops out of the top N is sold at the monthly rebalance and replaced by the new top-N member.
  5. Hold until the next month-end; rebalance monthly.
- **Notes:** LOW CONFIDENCE ON AS SPECIFICS. AS has no public rules post for this strategy (the AS 'Sector Rotation with Fama-French Alphas' post is an unrelated, rejected strategy). AS's 2019 matrix confirms only that it trades 'US Sectors (Multiple)' plus Cash. Rules above follow Faber's 2010 paper (verified): rank 10 sectors on trailing total returns over 1-12 months or the average of 1/3/6/9/12; hold top 1/2/3 equally; optional dynamic hedge to 100% T-bills when S&P 500 < 10-month SMA (or per sector). AS's exact sector list, lookback combination, number held and filter design are NOT verified. Faber also suggests a sell filter (buy top 3, sell when out of top 5) to cut turnover; not known to be used by AS.

### 9. Tactical Yield (`faber_tactical_yield`)

*Mebane Faber*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** T-Bills and Chill...Most of the Time (Cambria Investments white paper, Feb 2025) (2025), https://www.cambriainvestments.com/wp-content/uploads/2025/02/20250210.TBillsandChillMostoftheTime.Approved.pdf
- **AS page:** https://allocatesmartly.com/meb-fabers-tactical-yield-simple-and-intuitive/
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; rebalanced monthly even with no change
- **Universe:** risky []; defensive ['IEF', 'LQD']; canary []; cash BIL
- **Signal:** TERM_t = Y10_t - Y3M_t; CREDIT_t = YIG_t - Y3M_t (month-end yields). TERM_ON = 1 if TERM_t is in the top half of all observations of TERM up to and including t (expanding window, i.e. TERM_t > expanding median); CREDIT_ON likewise for CREDIT_t.
- **Data needs:** monthly 10-year Treasury yield (e.g. FRED GS10/DGS10 month-end; pre-1953 from long-history sources); monthly 3-month T-bill yield (e.g. FRED TB3MS/DTB3; pre-1934 from long-history sources); monthly investment-grade corporate yield (series not specified; e.g. Moody's Aaa (FRED AAA) or Baa (FRED BAA)) (uncertain); month-end dividend-adjusted closes for IEF, LQD, BIL; long-history 10y Treasury and IG corporate bond total-return proxies from 1930
- **ETF-only start:** 2007 (BIL May-2007; IEF/LQD Jul-2002)
- **In plain English:** Own intermediate Treasuries only when they pay unusually well over T-bills, and own corporate bonds only when their yield over T-bills is unusually high, judged against all past history. Otherwise sit in T-bills.
- **Rules:**
  1. At the close on the last trading day of the month compute the term premium (10-year Treasury yield minus 3-month T-bill yield) and the credit premium (investment-grade corporate bond yield minus 3-month T-bill yield).
  2. Compare each premium with its own full history up to that date (no look-ahead).
  3. If the term premium is in the top half of its history, allocate 50% to IEF; otherwise that 50% stays in cash (BIL).
  4. If the credit premium is in the top half of its history, allocate 50% to LQD; otherwise that 50% stays in cash.
  5. Hold until the next month-end; rebalance monthly.
- **Notes:** Rules from the AS post (2026). Original Cambria PDF link returned 404, so the exact yield series (especially which IG corporate yield), whether yields are month-end or monthly averages, and whether 'top half' is > or >= median could not be verified (uncertain). No publication-lag issue for market yields if month-end daily yields are used; if monthly-average series are used, they are only known after month-end (AS approach not stated). AS notes small early-history discrepancies vs Faber (~1932) due to data sources. AS tested cutoffs 30-70%; 50% is the tracked setting.

### 10. Robust Asset Allocation – Balanced (RAA Balanced) (`alphaarchitect_raa_balanced`)

*Wesley Gray (Alpha Architect), with Jack Vogel and David Foulke*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** DIY Financial Advisor: A Simple Solution to Build and Protect Your Wealth (Wiley); Alpha Architect 'Robust Asset Allocation' blog posts (2015), https://alphaarchitect.com/
- **AS page:** none (no public AS post)
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; slices reset monthly
- **Universe:** risky ['IWD', 'MTUM', 'EFV', 'EFA', 'VNQ', 'DBC']; defensive ['IEF']; canary []; cash BIL
- **Signal:** For each asset i: MA_i = 1 if P_i,t > SMA12_i,t (12 month-end dividend-adjusted closes incl. current) else 0; TMOM_i = 1 if 12-month total return of i > 12-month total return of T-bills else 0. EXPOSURE_i = (MA_i + TMOM_i)/2 in {0, 0.5, 1} (uncertain details).
- **Data needs:** month-end dividend-adjusted closes for IWD, MTUM, EFV, EFA, VNQ, DBC, IEF, BIL (13 months history); 3-month T-bill total return series for TMOM hurdle; pre-ETF proxies for value/momentum US and intl equity, REITs, commodities, 10y Treasuries
- **ETF-only start:** 2013 (MTUM Apr-2013; BIL 2007, DBC 2006, EFV 2005)
- **In plain English:** A diversified mix of US and foreign stocks (tilted to value and momentum), real estate, commodities and a large slice of Treasuries. Each slice is cut in half when one of two simple 12-month trend tests fails and moved fully to T-bills when both fail.
- **Rules:**
  1. Target weights (uncertain, not verified from source): US equity 20% split value IWD 10% / momentum MTUM 10%; international equity 20% split value EFV 10% / EFA 10% (stand-in for intl momentum); US REITs VNQ 10%; commodities DBC 10%; 7-10y Treasuries IEF 40%.
  2. At each month-end compute the two trend rules per asset: price above its 12-month SMA, and 12-month total return above the T-bill return over the same 12 months.
  3. Hold target_weight x 1.0 if both rules are positive, x 0.5 if exactly one is positive, x 0 if neither (uncertain); the de-risked portion goes to cash (BIL).
  4. Trend rules assumed to apply to every sleeve including IEF (uncertain).
  5. Hold until next month-end; rebalance all sleeves monthly.
  6. AS 2025 ETF changes: IWD->VTV, EFA->IEFA; DBC->PDBC (~Dec 2022).
- **Notes:** LOW CONFIDENCE ON WEIGHTS. No AS public rules post exists and alphaarchitect.com returned HTTP 403, so rules are from AS mentions plus unverified recollection of the source. Verified from AS: tracked in Balanced and Aggressive versions; fixed position sizes independent of other assets and no cross-sectional momentum (AS taxes post); uses a 12-month measure, longer than GTAA's 10-month (AS posts); AS 2019 matrix universe = DBC, EFA, EFV, IEF, IWD, MTUM, VNQ + Cash for both versions. NOT verified: exact sleeve weights, the 50/50 MA+TMOM combination, whether IEF is trend-filtered, and how intl momentum maps to EFA. Verify against DIY Financial Advisor (Gray, Vogel, Foulke 2015) before use.

### 11. Robust Asset Allocation – Aggressive (RAA Aggressive) (`alphaarchitect_raa_aggressive`)

*Wesley Gray (Alpha Architect), with Jack Vogel and David Foulke*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** DIY Financial Advisor: A Simple Solution to Build and Protect Your Wealth (Wiley); Alpha Architect 'Robust Asset Allocation' blog posts (2015), https://alphaarchitect.com/
- **AS page:** none (no public AS post)
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; slices reset monthly
- **Universe:** risky ['IWD', 'MTUM', 'EFV', 'EFA', 'VNQ', 'DBC']; defensive ['IEF']; canary []; cash BIL
- **Signal:** Same as RAA Balanced: MA_i = P_t > SMA12; TMOM_i = 12-month total return > 12-month T-bill return; EXPOSURE_i = (MA_i + TMOM_i)/2 (uncertain).
- **Data needs:** month-end dividend-adjusted closes for IWD, MTUM, EFV, EFA, VNQ, DBC, IEF, BIL; 3-month T-bill total return series; pre-ETF proxies as for RAA Balanced
- **ETF-only start:** 2013 (MTUM Apr-2013)
- **In plain English:** The same trend-protected value/momentum asset mix as RAA Balanced, but with more in stocks and less in Treasuries. Each slice is halved or moved to T-bills when its 12-month trend tests fail.
- **Rules:**
  1. Target weights (uncertain, not verified): higher equity/real-asset share and smaller Treasury sleeve than Balanced; best recollection US equity 30% (IWD 15% / MTUM 15%), intl equity 30% (EFV 15% / EFA 15%), VNQ 10%, DBC 10%, IEF 20%.
  2. Apply the same per-sleeve trend rules as Balanced: 100% of target if both 12-month MA and 12-month TMOM are positive, 50% if one, 0% if none; remainder to cash (BIL) (uncertain).
  3. Hold until next month-end; rebalance monthly.
  4. Same AS 2025 ETF substitutions as Balanced.
- **Notes:** LOW CONFIDENCE ON WEIGHTS (see RAA Balanced notes). AS's 2019 matrix shows the Aggressive version uses the same seven ETFs as Balanced including IEF, so it has a nonzero Treasury sleeve; the exact split could not be verified (alphaarchitect.com blocked, no AS public post, web search budget exhausted). Alpha Architect also published an RAA Moderate version that AS does not track. Verify weights and the signal-combination rule against DIY Financial Advisor before relying on this entry.

### 12. Adaptive Asset Allocation (`butler_adaptive_asset_allocation`)

*Adam Butler, Michael Philbrick, Rodrigo Gordillo (GestaltU / ReSolve Asset Management)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Adaptive Asset Allocation: A Primer (2012), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2328254
- **AS page:** https://allocatesmartly.com/adam-butler-gestaltu-adaptive-asset-allocation/
- **Rebalance:** monthly; signal computed and traded at the close of the last trading day of the month; whole portfolio rebalanced every month even if holdings are unchanged
- **Universe:** risky ['SPY', 'VGK', 'EWJ', 'EEM', 'VNQ', 'RWX', 'IEF', 'TLT', 'DBC', 'GLD']; defensive []; canary []; cash None
- **Signal:** MOM_i = P_t / P_{t-126} - 1 on daily dividend-adjusted closes (126 trading days ~ 6 months). Weighted covariance for the selected assets: Sigma = D * C126 * D, where D = diag(sigma_i), sigma_i = std dev of the last 20 daily returns, and C126 = Pearson correlation matrix of the last 126 daily returns.
- **Data needs:** daily dividend-adjusted closes for SPY, VGK, EWJ, EEM, VNQ, RWX, IEF, TLT, DBC, GLD (at least 127 trading days of history); quadratic-programming solver for long-only min variance
- **ETF-only start:** 2007 (RWX launched Dec 2006; DBC Feb 2006; VGK 2005; GLD Nov 2004; plus 126-day lookback)
- **In plain English:** Each month, buy the half of a 10-asset global menu (stocks, REITs, Treasuries, commodities, gold) that has risen the most over the past six months. Instead of splitting money equally, size the positions to make the combined portfolio as low-volatility as possible, using recent volatility and correlation.
- **Rules:**
  1. At the close on the last trading day of the month compute MOM_i for all 10 assets.
  2. Rank by MOM_i and select the top 5 (the top half of the universe). No absolute-momentum filter: the 5 are held even if their momentum is negative; there is no cash.
  3. Before RWX data exist (AS: until mid-1999) the universe is 9 assets and the top 4 are selected (keeps the top-half rule).
  4. Build Sigma = D*C126*D for the selected assets (20-day volatility, 126-day correlation).
  5. Solve the long-only minimum-variance portfolio: minimise w' Sigma w subject to sum(w) = 1 and w_i >= 0.
  6. AS practical filter: any weight below 2% of the portfolio is set to zero and its weight is redistributed proportionally to the remaining positions.
  7. Trade at the same close; hold until the last trading day of the following month.
- **Notes:** AS says complete rules are not stated precisely in the primer; the tested rules were worked out with the authors. CSS Analytics' 2012 replication used ~6-month ROC, top 50% of assets, monthly rebalance and a short (~20-day) volatility lookback, but a reply also mentions a 60-day variance window (conflict unresolved there); AS's 20-day vol / 126-day correlation is the spec to follow. AS post text names EZU for Europe while AS's 2019 asset matrix shows VGK - verify which ETF AS currently uses. The 2% minimum-position rule is an AS addition (negligible effect). Solver/constraints beyond long-only and fully invested are not stated (AS never uses leverage/shorts). No tie-break rule given. AS conforms to standard ETFs and changed EEM->IEMG and RWX->VNQI in 2025. Not verified against the primer PDF itself (SSRN returned 403).

### 13. Tactical Permanent Portfolio (`butler_tactical_permanent_portfolio`)

*Adam Butler (GestaltU / ReSolve Asset Management)*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** Permanent Portfolio Shakedown Part II (GestaltU) (2012), http://www.gestaltu.com/2012/08/permanent-portfolio-shakedown-part-ii.html/
- **AS page:** https://allocatesmartly.com/tactical-permanent-portfolio-gestaltu-investresolve/
- **Rebalance:** monthly; all calculations use data as of the close one trading day BEFORE the last trading day of the month; trades executed at the close of the last trading day; whole portfolio rebalanced monthly
- **Universe:** risky ['SPY', 'IEF', 'GLD']; defensive []; canary []; cash cash
- **Signal:** Evaluated at T-1 (day before the month's last trading day): TREND_i = Close_{T-1} > SMA_200(daily closes ending T-1). sigma_i = std dev of the last 21 daily returns ending T-1. Portfolio vol = sqrt(252 * w' Sigma60 w), Sigma60 = sample covariance of the last 60 daily returns ending T-1 (annualisation by sqrt(252) assumed).
- **Data needs:** daily dividend-adjusted closes for SPY, IEF, GLD (>= 200 trading days); 3-month T-bill rate for cash return (AS cash convention)
- **ETF-only start:** 2005 (GLD Nov 2004, IEF Jul 2002; plus 200-day SMA history)
- **In plain English:** Start from Harry Browne's Permanent Portfolio idea (stocks, Treasuries, gold, cash) but only hold the assets currently in an uptrend, give the calmer assets bigger weights, and move part of the portfolio to cash whenever the expected portfolio volatility would exceed 7% a year.
- **Rules:**
  1. On the trading day before the last trading day of the month (T-1), keep those of SPY, IEF and GLD whose close is above their 200-day simple moving average.
  2. Weight the kept assets by simple inverse volatility: w_i = (1/sigma_i) / sum_j(1/sigma_j), sigma from 21-day daily returns as of T-1.
  3. Compute the annualised volatility of this risk-parity portfolio from the 60-day covariance matrix as of T-1.
  4. If portfolio volatility > 7%, scale all weights by 7%/vol and put the remainder in cash. If <= 7%, keep weights summing to 100% (AS uses no leverage).
  5. If no asset is above its 200-day SMA, hold 100% cash.
  6. Execute at the close of the last trading day of the month (T); hold until the last trading day of the next month.
- **Notes:** The linked GestaltU article only partially specifies a tactical version (it discusses a 10-month MA filter, risk-parity weighting, a 7% (and 5%) volatility target, mostly quarterly rebalancing for the base tests); the precise rules here (200-day SMA, 21-day vol, 60-day covariance, 1-day lag, monthly) come from AS's post and were not verifiable in the original. Annualisation factor (252) and whether the 60-day covariance is sample covariance of simple daily returns are assumptions. Cash is AS's cash (3-month T-bill return). AS shows IEF in this strategy although Browne's buy-and-hold PP that AS tracks uses TLT.

### 14. Defensive Adaptive Asset Allocation (KDA) (`kipnis_defensive_adaptive_aa`)

*Ilya Kipnis (QuantStrat TradeR)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Right Now It's KDA...Asset Allocation (QuantStrat TradeR blog) (2019), https://quantstrattrader.wordpress.com/2019/01/24/right-now-its-kda-asset-allocation/
- **AS page:** https://allocatesmartly.com/ilya-kipnis-defensive-adaptive-asset-allocation/
- **Rebalance:** monthly; signals and trades at the close of the last trading day of the month
- **Universe:** risky ['SPY', 'VGK', 'EWJ', 'EEM', 'VNQ', 'RWX', 'IEF', 'TLT', 'DBC', 'GLD']; defensive ['IEF']; canary ['EEM', 'AGG']; cash cash
- **Signal:** MOM_i = 12*(p0/p21 - 1) + 4*(p0/p63 - 1) + 2*(p0/p126 - 1) + (p0/p252 - 1), p_k = dividend-adjusted close k trading days ago (unnormalised 13612W sum). Covariance for min-var: Sigma = D*C*D with D = diag(std dev of last 21 daily returns) and C = (12*C21 + 4*C63 + 2*C126 + C252)/19, Ck = Pearson correlation of the last k daily returns.
- **Data needs:** daily dividend-adjusted closes for SPY, VGK, EWJ, EEM, VNQ, RWX, IEF, TLT, DBC, GLD, AGG (>= 253 trading days); 3-month T-bill rate for cash return; QP solver for min variance
- **ETF-only start:** 2008 (RWX Dec 2006 plus 252-day lookback; AGG Sep 2003; DBC Feb 2006)
- **In plain English:** Each month, pick up to five of ten global assets with the strongest weighted recent momentum (only those actually rising) and size them for minimum portfolio volatility. Two 'canary' assets (emerging-market stocks and aggregate bonds) decide how much of the portfolio may be at risk; the rest goes to intermediate Treasuries if they are rising, otherwise cash.
- **Rules:**
  1. At the month-end close compute MOM for the 10 investment assets, the canaries EEM and AGG, and IEF.
  2. Canary: if MOM_EEM > 0 and MOM_AGG > 0, risk-on share R = 100%; if exactly one is > 0, R = 50%; if neither, R = 0%.
  3. Investment sleeve: rank the 10 investment assets by MOM, take the top 5, and discard any of them with MOM <= 0.
  4. If 2+ assets remain, weight them by long-only, fully invested minimum variance using the weighted covariance Sigma; if exactly 1 remains it gets the whole sleeve; if none remain the sleeve goes to cash (per Kipnis' code; AS does not state this case).
  5. Multiply sleeve weights by R.
  6. Crash-protection share (1 - R): allocate to IEF if MOM_IEF > 0, otherwise to cash. IEF can also be held in the investment sleeve; weights add.
  7. AS filter: positions below 2% of the portfolio are dropped and reallocated proportionally to the other positions.
  8. Trade at the close; hold until the last trading day of the following month.
- **Notes:** AS conformed Kipnis' VWO/BND canaries to EEM/AGG and replaced month endpoints with fixed day counts (similar but not identical results). Kipnis' backtest assumed cash earns 0 and no costs; AS uses T-bill cash and 0.1%/trade costs. The empty-sleeve case (no qualifying asset) is resolved from Kipnis' R code (weights zero -> cash). A follow-up post 'KDA - Robustness Results' (Feb 2019) exists but was not reviewed. Very high turnover (~7x/yr per AS).

### 15. Minimum Correlation Portfolio (`varadi_minimum_correlation`)

*David Varadi (CSS Analytics), with Michael Kapler, Henry Bee, Corey Rittenhouse*, family **risk-parity**, AS status **tracked**, spec status **partial**.

- **Source:** The Minimum Correlation Algorithm: A Practical Diversification Tool (2012), https://cssanalytics.wordpress.com/2012/09/21/minimum-correlation-algorithm-paper-release/
- **AS page:** none (no public AS post)
- **Rebalance:** monthly, last trading day close (AS default; AS reports ~96 small trades/yr = 8 assets x 12 months)
- **Universe:** risky ['SPY', 'QQQ', 'IWM', 'EEM', 'EFA', 'TLT', 'VNQ', 'GLD']; defensive []; canary []; cash None
- **Signal:** Over a lookback of L daily returns (L = 60 trading days, uncertain): C = Pearson correlation matrix, sigma_i = std dev of daily returns. MinCorr: mu_rho, s_rho = mean and std dev of the N(N-1)/2 off-diagonal correlations; A_ij = 1 - NormCDF(rho_ij; mu_rho, s_rho) for i != j, A_ii = 0; a_i = mean_{j != i} A_ij; rank r_i with the highest a_i (least correlated) = rank 1 and the lowest a_i (most correlated) = rank N; q_i = r_i / sum(r); v_j = sum_i q_i * A_ij; v normalised to sum 1; final w_j = (v_j / sigma_j) / sum_k(v_k / sigma_k).
- **Data needs:** daily dividend-adjusted closes for SPY, QQQ, IWM, EEM, EFA, TLT, VNQ, GLD (>= 61 trading days)
- **ETF-only start:** 2005 (GLD Nov 2004, VNQ Sep 2004, EEM Apr 2003; plus 60-day lookback)
- **In plain English:** Hold all eight major ETFs all the time, but give more money to the assets that are least correlated with the rest and less volatile, so the portfolio is spread across genuinely different return streams. Weights are recalculated each month from recent daily price behaviour.
- **Rules:**
  1. At the month-end close take the last L daily dividend-adjusted returns of the 8 ETFs.
  2. Compute the correlation matrix and each asset's volatility.
  3. Transform correlations into the 'adjusted' matrix A_ij = 1 - NormCDF(rho_ij, mean, sd of all off-diagonal correlations).
  4. Average each row of A (excluding the diagonal), rank the averages so that the most-correlated asset gets the largest rank, and convert ranks to rank weights q = r/sum(r).
  5. Multiply rank weights by A (q' A), normalise to sum to 1, divide by each asset's volatility and renormalise to 100%.
  6. Long-only, always fully invested in all 8 assets; no trend filter, no cash. (Special cases in reference code: 1 asset -> 100%; 2 assets -> inverse volatility.)
  7. Trade at the close and hold until the next month-end.
- **Notes:** No dedicated public AS post; AS's members page slug is 'david-varadis-minimum-correlation-portfolio' (not accessed). Universe taken from AS's public 2019 strategy/asset matrix (EEM, EFA, GLD, IWM, QQQ, SPY, TLT, VNQ), which matches the paper's 8-ETF test universe with IYR->VNQ. Algorithm steps taken from Systematic Investor's SIT R code (co-author Kapler: min.corr), as the paper PDF could not be retrieved. Paper backtest: weekly rebalance, 60-day lookback (SIT defaults). AS lookback, variant and pre-ETF data not public - flagged. AS separately tracks 'US Min Correlation' (SPY/IEF/LQD/VNQ, 36 month-end inputs) - see as_us_min_correlation; do not confuse the two.

### 16. Percentile Channels (`varadi_percentile_channels`)

*David Varadi (CSS Analytics)*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** A Simple Tactical Asset Allocation Portfolio with Percentile Channels (for Dummies) (2015), https://cssanalytics.wordpress.com/2015/02/08/a-simple-tactical-asset-allocation-portfolio-with-percentile-channels-for-dummies/
- **AS page:** https://allocatesmartly.com/david-varadis-percentile-channels/
- **Rebalance:** monthly; weights computed and traded at the close of the last trading day of the month; whole portfolio rebalanced monthly
- **Universe:** risky ['SPY', 'VNQ', 'LQD', 'DBC']; defensive []; canary []; cash cash
- **Signal:** For each asset i and lookback L in {60,120,180,252} trading days: UP = 75th percentile and LO = 25th percentile of the last L daily closes. State S_{i,L}: becomes +1 when Close > UP, becomes -1 when Close < LO, otherwise keeps its previous value (hysteresis, tracked daily). Score_i = (sum over the 4 lookbacks of S_{i,L}) / 4. sigma_i = std dev of the last 20 daily returns.
- **Data needs:** daily dividend-adjusted closes for SPY, VNQ, LQD, DBC (>= 252 trading days); 3-month T-bill rate for cash return
- **ETF-only start:** 2007 (DBC Feb 2006 plus 252-day channel history)
- **In plain English:** Four asset classes are each judged on four time frames: an asset turns 'on' when its price breaks into the top quarter of its recent range and only turns 'off' when it falls into the bottom quarter. Assets that are on more often get more money, scaled down for volatility, and whatever is left over sits in cash.
- **Rules:**
  1. Track the 16 asset/lookback channel states daily (entry above the 75th percentile, exit below the 25th percentile).
  2. At the month-end close compute Score_i = average of the 4 states (values -1, -0.5, 0, 0.5, 1).
  3. Compute C_i = Score_i / sigma_i (20-day volatility).
  4. Compute W_i = |C_i| / sum_j |C_j|, where the denominator includes assets with negative scores.
  5. Set W_i = 0 for assets with negative (or zero) score; the strategy is long-only.
  6. Cash = 1 - sum(W_i).
  7. Trade at the close; hold until the next month-end.
- **Notes:** Weighting formula verified from AS's public worked-example image (20-day volatility, score/vol, abs-sum normalisation including negatives, negatives ignored, cash residual), which matches Kipnis' and Systematic Investor's replications. AS text says channels are calculated at month-end; Systematic Investor and Kipnis' later update track channel crossings daily and sample at month-end - daily state tracking assumed (uncertain whether AS only checks month-end closes). Varadi's original used VTI/ICF and SHY for cash; AS conforms to SPY/VNQ and its standard cash. Percentile interpolation method not stated.

### 17. Growth and Inflation Sector Timing (`varadi_growth_inflation_sector_timing`)

*David Varadi (CSS Analytics)*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** The Growth and Inflation Sector Timing Model (2025), https://cssanalytics.wordpress.com/2025/03/20/the-growth-and-inflation-sector-timing-model/
- **AS page:** https://allocatesmartly.com/david-varadis-growth-and-inflation-sector-timing-a-wildcard-strategy/
- **Rebalance:** daily check at the close; switch (at that close) only when the regime changes; AS version includes an unpublished turnover-reduction modification (< 6 switches/yr on average)
- **Universe:** risky ['XLK', 'XLE', 'XLV', 'XLP']; defensive []; canary ['SPY', 'XLE', 'XLI', 'XLF', 'XLB', 'XLU', 'XLV', 'XLP']; cash None
- **Signal:** GROWTH_UP = SPY_close > SMA_200(SPY daily closes). Sector-Implied Expected Inflation: R_t = POS_t / NEG_t, where POS = total-return index of a basket 50% XLE + 1/6 XLI + 1/6 XLF + 1/6 XLB and NEG = total-return index of 1/3 XLU + 1/3 XLV + 1/3 XLP. INFLATION_UP = R_t > median(R over the last 200 trading days).
- **Data needs:** daily dividend-adjusted closes for SPY, XLK, XLE, XLV, XLP, XLI, XLF, XLB, XLU; pre-1999 S&P 500 sector total-return indices (for history)
- **ETF-only start:** 1999 (Select Sector SPDRs launched Dec 1998; plus 200-day history -> ~Oct 1999)
- **In plain English:** The S&P 500's trend says whether growth is rising, and the relative performance of inflation-sensitive sectors (energy, industrials, financials, materials) versus defensive ones (utilities, health care, staples) says whether inflation expectations are rising. The strategy holds the single sector ETF that has historically done best in the resulting regime.
- **Rules:**
  1. At each daily close compute GROWTH_UP and INFLATION_UP.
  2. Goldilocks (growth up, inflation down): 100% XLK.
  3. Reflation (growth up, inflation up): 100% XLE.
  4. Stagflation (growth down, inflation up): 100% XLV.
  5. Deflation/disinflation (growth down, inflation down): 100% XLP.
  6. Always fully invested in exactly one sector ETF; trade at the close when the regime changes, otherwise hold.
  7. AS-tracked version adds smoothing/turnover reduction agreed with Varadi; the mechanism is not public, so a replication of the original rules will trade more often than AS's version.
- **Notes:** Regime-to-ETF map and basket weights verified from AS's public figures (pie charts 50/17/17/16 and 33/33/34; quadrant: XLE/XLV/XLK/XLP). Varadi's text also remarks that holding Staples in both down-growth regimes would be a simple option, but his explicit choice (and AS's figure) is Health Care for stagflation. Varadi confirmed the ratio uses total-return series; basket construction (daily-rebalanced fixed weights vs buy-and-hold from the start date) and the base date of the ratio are not specified - the 200-day median comparison makes the level irrelevant but the drift method matters slightly. Communication Services excluded for lack of history. Original post gives no explicit execution frequency (daily implied); AS states daily evaluation with turnover reduction (smoothing details undisclosed). Extremely concentrated single-sector strategy.

### 18. Inflation Compass - Original (`varadi_inflation_compass_original`)

*David Varadi (CSS Analytics)*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** The Inflation Compass Model (2026), https://cssanalytics.wordpress.com/2026/07/27/the-inflation-compass-model/
- **AS page:** https://allocatesmartly.com/taming-the-wildcard-david-varadis-inflation-compass/
- **Rebalance:** monthly; signals and trades at the close of the last trading day of the month; hold for the following month
- **Universe:** risky ['XLE', 'XLK', 'XLU', 'XLP']; defensive ['IEF']; canary ['SPY', 'XLE', 'XLI', 'XLF', 'XLB', 'XLU', 'XLV', 'XLP']; cash None
- **Signal:** GROWTH_UP = SPY_close > SMA_200(SPY daily). BE = 5-year breakeven inflation rate (FRED T5YIE, daily). LEVEL_OK = BE_t > 2.0%. BE_MOM = BE_t > BE_{t-60 trading days}. Sector-implied inflation R_t = cumulative growth of (0.5 XLE + 1/6 XLI + 1/6 XLF + 1/6 XLB) / cumulative growth of (1/3 XLU + 1/3 XLV + 1/3 XLP); SECT_MOM = slope of an OLS linear regression of R on time over the last 60 trading days > 0. INFLATION_ON = LEVEL_OK AND (BE_MOM OR SECT_MOM).
- **Data needs:** daily dividend-adjusted closes for SPY, XLE, XLK, XLU, XLP, XLI, XLF, XLB, XLV, IEF; FRED T5YIE daily (published with ~1 business-day delay; lag accordingly - AS's handling not stated); pre-2003 breakeven proxy if backtesting earlier (undisclosed)
- **ETF-only start:** 2003 (T5YIE begins Jan 2003; IEF Jul 2002; sector SPDRs Dec 1998)
- **In plain English:** Like Growth and Inflation Sector Timing, but inflation is read directly from the bond market: inflation counts as 'on' only when 5-year breakeven inflation is above 2% and either the breakeven rate or the inflation-sensitive sectors are trending up. Each month it holds energy, tech, utilities, or a staples/Treasury mix depending on the growth/inflation regime.
- **Rules:**
  1. At the month-end close compute GROWTH_UP and INFLATION_ON.
  2. Growth up + inflation on (reflation): 100% XLE.
  3. Growth up + inflation off (goldilocks): 100% XLK.
  4. Growth down + inflation on (stagflation): 100% XLU.
  5. Growth down + inflation off (disinflationary slowdown): 50% XLP + 50% IEF.
  6. Trade at the close; hold until the next month-end.
- **Notes:** Rules verified against Varadi's post and AS's public regime figure (XLE / XLK / XLU / XLP+IEF). Whether the regression is on the raw or log ratio is not stated; basket rebalancing method not stated. T5YIE starts 2003, yet AS's backtest starts 1990 and AS calls pre-2003 data out-of-sample - AS's pre-2003 inflation-expectation proxy is undisclosed. AS also showed robustness runs replacing T5YIE with 5y inflation swaps (USSWIT5) and Cleveland Fed EXPINF5YR (not part of the tracked rules). Varadi's own tests included a 1-day execution delay sensitivity; AS uses month-end close execution. Highly concentrated strategy.

### 19. Inflation Compass - Enhanced (`varadi_inflation_compass_enhanced`)

*David Varadi (CSS Analytics)*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** The Inflation Compass Model (enhancements proposed by the author to AllocateSmartly) (2026), https://cssanalytics.wordpress.com/2026/07/27/the-inflation-compass-model/
- **AS page:** https://allocatesmartly.com/taming-the-wildcard-david-varadis-inflation-compass/
- **Rebalance:** monthly; last trading day close (as Original)
- **Universe:** risky ['XLE', 'QQQ', 'XLU', 'PDBC', 'XLP']; defensive ['IEF']; canary ['SPY', 'XLE', 'XLI', 'XLF', 'XLB', 'XLU', 'XLV', 'XLP']; cash None
- **Signal:** Same building blocks as the Original (SPY vs SMA_n; T5YIE level > threshold; T5YIE change over k days; slope of k-day regression of the sector-implied inflation ratio), but evaluated over an ensemble of parameter values and averaged. Exact ensemble grid not public (uncertain).
- **Data needs:** daily dividend-adjusted closes for SPY, XLE, QQQ, XLU, PDBC/DBC, XLP, IEF, XLI, XLF, XLB, XLV; FRED T5YIE daily (lagged ~1 business day); pre-2003 breakeven proxy (undisclosed)
- **ETF-only start:** 2006 (DBC Feb 2006 as PDBC proxy; T5YIE Jan 2003; QQQ 1999)
- **In plain English:** The same inflation/growth compass as the Original, but instead of betting on one exact set of settings it averages the signal over many reasonable settings, which usually leaves the portfolio split between a few holdings. It also uses the Nasdaq-100 instead of the tech sector and pairs utilities with commodities in stagflation.
- **Rules:**
  1. For each parameter combination in the ensemble, determine the growth/inflation regime exactly as in the Original.
  2. Map each regime to Enhanced holdings: reflation -> XLE; goldilocks -> QQQ (instead of XLK); stagflation -> 50% XLU + 50% PDBC; disinflation -> 50% XLP + 50% IEF.
  3. Average the resulting allocations across all parameter combinations to get fractional weights (averaging method assumed - uncertain).
  4. Trade at the month-end close; hold for the following month.
- **Notes:** AS describes the Enhanced version only as several author-proposed refinements, chiefly parameter ensembling; specific values not published. The QQQ-for-XLK swap and the 50/50 XLU/PDBC stagflation sleeve come from a reader comment on Varadi's post (Aug 2026) comparing AS's two versions, which Varadi's reply confirmed; other refinements, if any, are unknown. Treat this entry as a best-effort approximation; replication will not match AS exactly.

### 20. Diversified Dual Momentum (`newfound_diversified_dual_momentum`)

*Corey Hoffstein (Newfound Research)*, family **momentum-rotation**, AS status **tracked**, spec status **partial**.

- **Source:** Fragility Case Study: Dual Momentum GEM (2019), https://blog.thinknewfound.com/2019/01/fragility-case-study-dual-momentum-gem/
- **AS page:** https://allocatesmartly.com/asset-allocation-roundup-jan-2019/
- **Rebalance:** monthly, last trading day close (AS default, assumed); Newfound rebalanced the 7-model blend annually
- **Universe:** risky ['SPY', 'EFA']; defensive ['AGG']; canary []; cash None
- **Signal:** For each lookback L in {6,7,8,9,10,11,12} months: R_i(L) = P_t / P_{t-L months} - 1 on month-end dividend-adjusted closes (i = SPY, EFA); hurdle H(L) = T-bill total return over the same L months (BIL / 3-month T-bill).
- **Data needs:** month-end dividend-adjusted closes for SPY, EFA, AGG (>= 12 months); T-bill total return index or BIL
- **ETF-only start:** 2004 (AGG Sep 2003, EFA Aug 2001; plus 12-month lookback; BIL only from 2007 so a T-bill index is needed for the hurdle earlier)
- **In plain English:** Gary Antonacci's Dual Momentum picks US stocks, international stocks, or bonds using one 12-month lookback. This version runs the same rule seven times with lookbacks from 6 to 12 months and splits the money equally, so one unlucky lookback choice matters less.
- **Rules:**
  1. At the month-end close, for each of the 7 lookbacks L = 6..12 months run Antonacci's GEM decision:
  2. Absolute momentum: if R_SPY(L) > H(L), hold whichever of SPY and EFA has the higher R(L) (relative momentum); otherwise hold AGG.
  3. Each of the 7 sub-portfolios is allocated 1/7 of capital; sum the sub-portfolio holdings to get final weights (multiples of 1/7 across SPY, EFA, AGG).
  4. Trade at the close; hold until the next month-end.
- **Notes:** No dedicated public AS post; AS added it to the members area in Jan 2019 and summarised it as GEM split into 7 equal parts with lookbacks of 6-12 months. AS's 2019 asset matrix lists SPY, EFA, AGG (no cash). Newfound's text gives the 6-12 month range, 7 models, equal weighting and an annual rebalance of the blend; the GEM decision tree itself is an image. Unverified: whether AS uses calendar months or 21-day multiples, the exact T-bill hurdle series, and whether AS rebalances sleeves monthly (assumed) rather than annually. AS also tracks a 'Dynamic Bond' variant (AGG must also pass the absolute-momentum rule, else cash) - not specified here.

### 21. Max Diversification Portfolio (US Max Diversification) (`as_max_diversification`)

*AllocateSmartly (N/A developer); technique from Choueifaty & Coignard*, family **risk-parity**, AS status **tracked**, spec status **full**.

- **Source:** Testing Popular Portfolio Optimization Techniques (AllocateSmartly) (2016), https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **AS page:** https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **Rebalance:** monthly; last trading day close
- **Universe:** risky ['SPY', 'IEF', 'LQD', 'VNQ']; defensive []; canary []; cash None
- **Signal:** Inputs from the previous 36 month-end values (monthly returns): sigma_i = std dev of monthly returns, Sigma = sample covariance matrix. Diversification ratio DR(w) = (sum_i w_i sigma_i) / sqrt(w' Sigma w).
- **Data needs:** month-end dividend-adjusted closes for SPY, IEF, LQD, VNQ (>= 37 months); QP solver
- **ETF-only start:** 2007 (VNQ Sep 2004 plus 36 months of month-end data)
- **In plain English:** Holds US stocks, Treasuries, corporate bonds and REITs in the mix that maximises diversification - the ratio of the assets' average stand-alone volatility to the portfolio's actual volatility - using the last three years of monthly data.
- **Rules:**
  1. At the month-end close compute monthly returns from the last 36 month-end dividend-adjusted closes for SPY, IEF, LQD, VNQ.
  2. Maximise DR(w) subject to w_i >= 0 and sum(w) = 1 (no min/max per asset, no cash, no leverage). Equivalent QP: minimise y' Sigma y s.t. sigma' y = 1, y >= 0; then w = y / sum(y).
  3. Trade at the close; hold until next month-end.
- **Notes:** AS tracks this as a generic, unoptimised benchmark-like strategy on the four largest US asset classes. Whether '36 month-end values' means 36 returns (37 prices) or 35 returns is ambiguous. AS observed it tends to ignore LQD. AS's 2019 matrix and later posts label it 'US Max Diversification'; a global extension was mentioned but not found.

### 22. Equal Risk Contribution Portfolio (US Equal Risk Contribution) (`as_equal_risk_contribution`)

*AllocateSmartly (N/A developer); technique from Maillard, Roncalli & Teiletche*, family **risk-parity**, AS status **tracked**, spec status **full**.

- **Source:** Testing Popular Portfolio Optimization Techniques (AllocateSmartly) (2016), https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **AS page:** https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **Rebalance:** monthly; last trading day close
- **Universe:** risky ['SPY', 'IEF', 'LQD', 'VNQ']; defensive []; canary []; cash None
- **Signal:** Sigma = sample covariance of monthly returns from the previous 36 month-end values. Risk contribution RC_i = w_i * (Sigma w)_i.
- **Data needs:** month-end dividend-adjusted closes for SPY, IEF, LQD, VNQ (>= 37 months); ERC solver (e.g. Spinu / log-barrier or iterative)
- **ETF-only start:** 2007 (VNQ Sep 2004 plus 36 months)
- **In plain English:** Splits money across US stocks, Treasuries, corporate bonds and REITs so that each contributes the same amount of risk to the portfolio, accounting for both volatility and correlation, re-estimated monthly from three years of data.
- **Rules:**
  1. At the month-end close estimate Sigma from the last 36 month-end dividend-adjusted closes of SPY, IEF, LQD, VNQ.
  2. Find w with w_i >= 0, sum(w) = 1 such that RC_i is equal for all assets (true ERC using full covariance, not 1/vol).
  3. Trade at the close; hold until next month-end.
- **Notes:** AS stresses this is true ERC (covariance-based) rather than naive inverse-volatility. AS also uses ERC as an alternative benchmark and as half of the Meta Strategy weighting (with Min Correlation) - those are different applications. 36-value ambiguity as in Max Diversification.

### 23. Max Sharpe Portfolio (US Max Sharpe) (`as_max_sharpe`)

*AllocateSmartly (N/A developer); inspired by Keller, Butler & Kipnis 'Momentum and Markowitz: A Golden Combination'*, family **risk-parity**, AS status **tracked**, spec status **partial**.

- **Source:** Testing Popular Portfolio Optimization Techniques (AllocateSmartly) (2016), https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **AS page:** https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **Rebalance:** monthly; last trading day close
- **Universe:** risky ['SPY', 'IEF', 'LQD', 'VNQ']; defensive []; canary []; cash None
- **Signal:** For L in {36, 12} months: mu_L = mean monthly return and Sigma_L = sample covariance over the last L month-end values (assumed); w_MS(L) = argmax (w' mu_L - rf) / sqrt(w' Sigma_L w) s.t. w >= 0, sum(w) = 1. Final w = 0.5 * w_MS(36) + 0.5 * w_MS(12).
- **Data needs:** month-end dividend-adjusted closes for SPY, IEF, LQD, VNQ (>= 37 months); T-bill rate if a non-zero risk-free rate is used; QP solver
- **ETF-only start:** 2007 (VNQ Sep 2004 plus 36 months)
- **In plain English:** Picks the mix of US stocks, Treasuries, corporate bonds and REITs with the best historical return per unit of risk, once using three years of data and once using one year, and averages the two. The one-year half makes it lean toward recent winners, giving it a momentum tilt.
- **Rules:**
  1. At the month-end close compute mu and Sigma for SPY, IEF, LQD, VNQ from the last 36 monthly returns and, separately, from the last 12 monthly returns.
  2. Solve the long-only, fully invested tangency (max Sharpe) portfolio for each window (QP: minimise y' Sigma y s.t. (mu - rf)' y = 1, y >= 0; w = y/sum(y)).
  3. Average the two weight vectors 50/50.
  4. Trade at the close; hold until next month-end.
- **Notes:** Only AS's own description is available. Not stated: expected-return estimator, risk-free rate, behaviour when no asset has excess return > 0 (fallback unknown). Higher turnover and fewer positions than the other optimisers. Labelled 'US Max Sharpe' in later AS posts. | Family set to 'risk-parity' = AS 'Portfolio Optimization' bucket (mean-variance, not strictly risk parity).

### 24. US Min Correlation (`as_us_min_correlation`)

*AllocateSmartly (N/A developer); algorithm by David Varadi*, family **risk-parity**, AS status **tracked**, spec status **full**.

- **Source:** Testing Popular Portfolio Optimization Techniques (AllocateSmartly) (2016), https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **AS page:** https://allocatesmartly.com/testing-popular-portfolio-optimization-techniques/
- **Rebalance:** monthly; last trading day close
- **Universe:** risky ['SPY', 'IEF', 'LQD', 'VNQ']; defensive []; canary []; cash None
- **Signal:** Correlation matrix and volatilities from the previous 36 month-end values (monthly returns); weights from Varadi's Minimum Correlation Algorithm (see varadi_minimum_correlation for the step formula).
- **Data needs:** month-end dividend-adjusted closes for SPY, IEF, LQD, VNQ (>= 37 months)
- **ETF-only start:** 2007 (VNQ Sep 2004 plus 36 months)
- **In plain English:** Holds US stocks, Treasuries, corporate bonds and REITs, overweighting those least correlated with the others and least volatile, based on three years of monthly data.
- **Rules:**
  1. At the month-end close compute monthly returns from the last 36 month-end closes of SPY, IEF, LQD, VNQ.
  2. Apply the Minimum Correlation Algorithm (normalised correlation matrix, rank weights, inverse-volatility scaling) to get long-only weights summing to 100%.
  3. Trade at the close; hold until next month-end.
- **Notes:** Extra entry (not in the assigned list): AS tracks this separately from 'Varadi's Minimum Correlation Portfolio' (it appears as 'US Min Correlation' in AS tables through 2026 and in the 2019 asset matrix with IEF/LQD/SPY/VNQ). Drop if the catalog should only contain the current list-of-strategies names.

### 25. 60/40 Benchmark (`benchmark_60_40`)

*N/A (AllocateSmartly default benchmark)*, family **static**, AS status **tracked**, spec status **full**.

- **Source:** AllocateSmartly FAQ: The 60/40 Benchmark and Other Alternatives (None), https://allocatesmartly.com/faqs/
- **AS page:** https://allocatesmartly.com/faqs/
- **Rebalance:** monthly, at the close of the last trading day of the month
- **Universe:** risky ['SPY']; defensive ['IEF']; canary []; cash None
- **Signal:** None (static weights).
- **Data needs:** dividend-adjusted month-end closes for SPY and IEF; pre-ETF: S&P 500 TR and intermediate Treasury TR indices
- **ETF-only start:** 2002 (IEF launched Jul 2002)
- **In plain English:** AllocateSmartly's yardstick: 60% in the S&P 500 and 40% in intermediate-term US Treasuries, reset to that mix every month.
- **Rules:**
  1. Hold 60% SPY and 40% IEF.
  2. Rebalance back to 60/40 at the close of the last trading day of every month.
- **Notes:** Defined explicitly in AS FAQ (60% SPY, 40% IEF, rebalanced monthly) and confirmed by AS 2019 strategy-asset matrix. Transaction costs apply as in AS backtests.

### 26. OptimumV (`tresidder_optimumv`)

*Todd Tresidder (Financial Mentor)*, family **momentum-rotation**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** OptimumV - proprietary Financial Mentor strategy (rules not publicly disclosed; only available via AllocateSmartly) (2026), https://www.financialmentor.com/
- **AS page:** https://allocatesmartly.com/financial-mentors-optimumv/
- **Rebalance:** monthly, last trading day close (AS default; exact OptimumV timing not disclosed)
- **Universe:** risky []; defensive []; canary []; cash None
- **Signal:** UNDISCLOSED. AS states only that OptimumV shares the core algorithm of Optimum3 (dual momentum pre-selection of roughly the top half of the universe, then a minimum-average-correlation selection of a small high-momentum portfolio) but, unlike Optimum3, tilts the portfolio toward assets suited to the current economic state. The economic-state indicators, tilt mechanism, lookbacks and weights are not public.
- **Data needs:** daily adjusted closes for the (undisclosed) ETF universe, at least DBC/PDBC; unspecified economic-state data (undisclosed; AS would apply its 1-month publication lag and vintage data convention to any monthly macro series)
- **ETF-only start:** unknown (universe undisclosed); AS backtest begins 1987 using index proxies
- **In plain English:** A newer sibling of Optimum3: it still buys a small, diversified set of assets that have strong momentum, but leans toward assets that historically do well in the current economic environment (e.g. commodities when inflationary). The author asked AllocateSmartly not to publish the rules.
- **Rules:**
  1. On the last trading day of each month (assumed AS default), run an Optimum3-style core: keep assets with positive absolute momentum that rank roughly in the top half on relative momentum (see tresidder_optimum3; details undisclosed).
  2. Apply an economic-regime overlay that favours asset classes historically suited to the current macro state (indicators, thresholds and tilt sizes undisclosed).
  3. Form the final portfolio from the tilted selection (number of holdings, weighting and cash handling undisclosed) and hold until the next rebalance.
  4. No faithful replication is possible from public information; any implementation is an approximation.
- **Notes:** AS post (Oct 15 2026) explicitly says Tresidder asked AS not to disclose the OptimumV ruleset; AS knows and independently tested the rules, and warns that any online replication is a guess. Nothing on financialmentor.com (site search for 'optimum'/'allocate smartly') exposes the rules; Financial Mentor's educational series may be paywalled. Family set to momentum-rotation because the core is Optimum3's dual-momentum/min-correlation selection, but the macro tilt means it could also be classed 'macro'. Universe, signals, weights, cash rule and macro inputs all unverifiable. Treat as NOT implementable beyond a rough proxy.

### 27. Optimum3 (`tresidder_optimum3`)

*Todd Tresidder (Financial Mentor)*, family **momentum-rotation**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** Optimum3 - proprietary Financial Mentor strategy (rules shared privately with AllocateSmartly, not public) (2022), https://www.financialmentor.com/
- **AS page:** https://allocatesmartly.com/financial-mentors-optimum3-strategy/
- **Rebalance:** monthly, last trading day close (selection uses daily data)
- **Universe:** risky ['SPY', 'QQQ', 'VNQ', 'REM', 'IEF', 'TLT', 'TIP', 'VGK', 'EWJ', 'SCZ', 'EEM', 'RWX', 'BWX', 'DBC', 'GLD']; defensive []; canary []; cash None
- **Signal:** Partially disclosed. (1) Dual momentum screen: asset momentum must be positive (absolute/time-series) AND the asset must rank in roughly the top half of the 15 assets on momentum (relative/cross-sectional). Momentum formula and lookback UNDISCLOSED (AS's illustrative toy example used 6-month total return and top 6, but AS says this is not how the strategy trades). (2) Diversification selection: from the surviving candidates, pick the 3 assets with the lowest average correlation to the other remaining candidates (described as akin to Varadi's Minimum Correlation Algorithm), using daily return data; correlation window UNDISCLOSED.
- **Data needs:** daily adjusted closes for SPY, QQQ, VNQ, REM, IEF, TLT, TIP, VGK, EWJ, SCZ, EEM, RWX, BWX, DBC, GLD (or daily index proxies pre-inception); 3-month T-bill series if cash is used for unfilled slots (uncertain)
- **ETF-only start:** 2008 approx (SCZ Dec 2007, BWX Oct 2007, REM May 2007)
- **In plain English:** Each month it looks at 15 global asset classes, throws out those that are falling or lagging, and from the best half picks the three that move least alike, so the portfolio is both strong-trending and diversified. The exact formulas are kept private by the author.
- **Rules:**
  1. At the close on the last trading day of the month, compute a momentum score for each of the 15 assets (formula and lookback undisclosed).
  2. Discard assets with non-positive momentum (absolute momentum filter).
  3. Of the remainder, keep roughly the top half of the full 15-asset universe by momentum (exact cut-off undisclosed; 'roughly half' suggests about 7-8 names).
  4. From this candidate list, select the 3 assets with the lowest average correlation to the other remaining candidates, using correlations of daily returns (window undisclosed; whether this is a one-pass ranking or an iterative elimination of the most-correlated asset is undisclosed). Discard all other candidates.
  5. Allocate to the 3 selected assets (weighting undisclosed; equal 1/3 weights are a natural reading of '3-asset portfolio' but uncertain) and hold until the next month-end.
  6. If fewer than 3 assets pass the momentum screen, the treatment (cash, fewer holdings, or bonds) is undisclosed.
- **Notes:** AS (Jan 2022) states it knows the rules and replicated them but is not permitted to disclose them; only the two-stage concept (dual-momentum top-half screen, then 3-asset minimum-correlation selection) and the 15-asset universe are public. AS notes the strategy needs daily data, so its test only starts in 1987, and that it is tax-inefficient because positions rotate for correlation reasons. Financial Mentor's site exposes no public rules (site search returned nothing). All lookbacks, the correlation window, weighting and cash rule are unverified; a replication is an approximation only.

### 28. All-Weather Quad Momentum (AWQM) (`tresidder_all_weather_quad_momentum`)

*Todd Tresidder (Financial Mentor)*, family **momentum-rotation**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** All-Weather Quad Momentum - proprietary Financial Mentor strategy (rules not public) (2021), https://www.financialmentor.com/
- **AS page:** https://allocatesmartly.com/financial-mentors-all-weather-quad-momentum/
- **Rebalance:** monthly (AS default last trading day close)
- **Universe:** risky []; defensive []; canary []; cash cash
- **Signal:** UNDISCLOSED. Publicly: 50% of capital follows a long-term dual-momentum component (momentum measured over roughly the last 10-12 months, conceptually like Antonacci's Traditional Dual Momentum) and 50% follows a short-term dual-momentum component (roughly 1-6 months, conceptually like Accelerating Dual Momentum, which AS implements as the average of 1-, 3- and 6-month total returns), each choosing from a broader 'all-weather' menu than those models.
- **Data needs:** monthly (month-end) adjusted closes for the undisclosed universe (likely US/intl equities, GLD, TIP, TLT, short-term Treasuries); 3-month T-bill series for cash
- **ETF-only start:** unknown (universe undisclosed); AS backtest from 1970 using proxies
- **In plain English:** Half the money chases what has been strongest over the past year and half chases what has been strongest over the past few months, choosing among stocks, gold, inflation-protected bonds, long Treasuries and cash so that some asset fits every economic climate. It often concentrates in just one or two assets, so it can be aggressive.
- **Rules:**
  1. Split the portfolio 50/50 between a long-term and a short-term momentum sleeve; rebalance monthly.
  2. Long-term sleeve: dual momentum (relative + absolute) over ~10-12 months across the all-weather menu (exact lookback, ranking and fallback undisclosed).
  3. Short-term sleeve: dual momentum over ~1-6 months across the same menu (exact formula undisclosed).
  4. The menu spans the four economic regimes: prosperity (equities/risk assets), recession (cash and short-term Treasuries), inflation (gold and TIPS) and deflation (long-term Treasuries); each sleeve tends to hold the single best-suited asset, so the portfolio holds one or two assets at a time (uncertain).
  5. Exact tickers, tie-breaks and the cash/defensive selection logic are undisclosed.
- **Notes:** AS (Jun 2021) states it will not disclose AWQM rules at Financial Mentor's request; it only gives the 50/50 long/short-term momentum split, the conceptual link to Traditional Dual Momentum and Accelerating Dual Momentum, the four-regime asset roles, and that the optimal historical mix would have been ~75% short-term (author deliberately chose 50/50). AS also notes AWQM had the highest rising-USD exposure of its 60+ strategies. 'Quad' presumably refers to the four economic regimes (inference). Tickers, lookbacks, ranking formulas and fallback logic could not be verified; financialmentor.com public pages contain no rules.

### 29. Mama Bear Portfolio (`livingston_mama_bear`)

*Brian Livingston (Muscular Portfolios)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Muscular Portfolios: The Investing Revolution for Superior Returns with Lower Risk (book) / MuscularPortfolios.com Mama Bear page (2018), https://muscularportfolios.com/mama-bear/
- **AS page:** https://allocatesmartly.com/livingstons-muscular-portfolios/
- **Rebalance:** monthly, last trading day close; full rebalance to equal weights every month (AS)
- **Universe:** risky ['SPY', 'IWM', 'EFA', 'EEM', 'VNQ', 'DBC', 'GLD', 'TLT']; defensive []; canary []; cash cash
- **Signal:** MOM_i = P_t / P_{t-5m} - 1 using month-end total-return (dividend-adjusted) closes, i.e. 5-month return ending at the current month-end close; computed for the 8 ETFs plus cash (cash return = 3-month T-bill over the same 5 months, standing in for SHV).
- **Data needs:** month-end adjusted closes for SPY, IWM, EFA, EEM, VNQ, DBC, GLD, TLT; 3-month T-bill total return series for cash (or SHV/BIL)
- **ETF-only start:** 2006 (DBC Feb 2006; GLD Nov 2004)
- **In plain English:** Every month, look at nine broad asset classes (US large and small stocks, foreign and emerging stocks, real estate, commodities, gold, long Treasuries and cash), and put a third of your money into each of the three that rose most over the past five months.
- **Rules:**
  1. At the close on the last trading day of the month, compute the 5-month total return for each of the 9 candidates: SPY, IWM, EFA, EEM, VNQ, DBC, GLD, TLT and cash (SHV in the original; AS replaces SHV with cash).
  2. Rank all 9 by 5-month return and select the top 3 regardless of whether their returns are positive or negative (no absolute-momentum filter).
  3. Allocate 1/3 of the portfolio to each selected asset at the close (if cash ranks in the top 3, that 1/3 is held in cash).
  4. Hold until the last trading day of the following month; rebalance all positions back to 1/3 each month even if holdings do not change.
  5. Tie-breaks are not specified by the author or AS.
- **Notes:** AS mapping of author tickers to AS ETFs inferred by asset class (VONE Russell 1000 -> SPY; VIOO S&P 600 -> IWM). Livingston's website measures 105 trading days using the prior day's closes and trades any consistent day; AS uses month-end and a 5-month lookback, justified because the book backtests used Faber's Idea Farm monthly workbook. AS models SHV as cash. Livingston also suggests trading only when bid-ask spread <1%. AS notes month-end trading has historically been notably better than other days for this model. Backtest start year not given in the AS text. Near-clone of CXO's SACEMS concept.

### 30. Papa Bear Portfolio (`livingston_papa_bear`)

*Brian Livingston (Muscular Portfolios)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Muscular Portfolios: The Investing Revolution for Superior Returns with Lower Risk (book) / MuscularPortfolios.com Papa Bear page (2018), https://muscularportfolios.com/papa-bear/
- **AS page:** https://allocatesmartly.com/livingstons-muscular-portfolios/
- **Rebalance:** monthly, last trading day close; full rebalance to equal weights every month (AS)
- **Universe:** risky ['IWF', 'IWD', 'IWO', 'IWN', 'EFA', 'EEM', 'VNQ', 'DBC', 'GLD', 'TLT', 'IEF', 'LQD', 'BNDX']; defensive []; canary []; cash None
- **Signal:** SCORE_i = (r3 + r6 + r12) / 3 where r_k = P_t / P_{t-k months} - 1 on month-end total-return (dividend-adjusted) closes ending at the current month-end close.
- **Data needs:** month-end adjusted closes for IWF, IWD, IWO, IWN, EFA, EEM, VNQ, DBC, GLD, TLT, IEF, LQD, BNDX (BWX as pre-1988 proxy)
- **ETF-only start:** 2013 (BNDX Jun 2013); ~2007 if BWX (Oct 2007) substitutes for BNDX
- **In plain English:** Every month, score 13 asset classes (US growth and value stocks large and small, foreign and emerging stocks, real estate, commodities, gold, several kinds of bonds) by their average 3-, 6- and 12-month gains, and split the money equally among the top three. It never goes to cash.
- **Rules:**
  1. At the close on the last trading day of the month, compute SCORE = average of the 3-, 6- and 12-month total returns for each of the 13 ETFs.
  2. Select the 3 ETFs with the highest SCORE regardless of sign (no absolute-momentum filter, no cash option).
  3. Allocate 1/3 of the portfolio to each at the close.
  4. Hold until the last trading day of the following month; rebalance to 1/3 each monthly even if holdings are unchanged.
  5. Tie-breaks are not specified.
- **Notes:** Author ETF-to-AS mapping inferred by asset class (e.g., EDV extended-duration Treasuries -> TLT, VCLT long corporate -> LQD); AS end notes list the 13 AS tickers. Livingston's site uses trading-day lookbacks and allows any consistent trading day; AS uses calendar months at month-end (book results were based on Faber's monthly Idea Farm workbook). AS's Papa Bear test is shorter than Mama Bear's; exact start years not stated in text. Considered a near-clone of Faber's GTAA Agg 3 without the absolute-momentum filter.

### 31. Growth-Trend Timing (GTT-Original) (`philoeconomics_growth_trend_timing`)

*Philosophical Economics (pseudonymous blogger 'Jesse Livermore')*, family **macro**, AS status **tracked**, spec status **full**.

- **Source:** Growth and Trend: A Simple, Powerful Technique for Timing the Stock Market (2016), https://www.philosophicaleconomics.com/2016/01/gtt/
- **AS page:** https://allocatesmartly.com/philosophical-economics-growth-trend-timing/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY']; defensive []; canary []; cash cash
- **Signal:** Data month d = previous calendar month (1-month publication lag). RRSFS_YoY = RRSFS_d / RRSFS_{d-12} - 1; INDPRO_YoY = INDPRO_d / INDPRO_{d-12} - 1. RECESSION = (RRSFS_YoY < 0) OR (INDPRO_YoY < 0). TREND_UP = SPY_close_t > SMA_10(month-end closes t-9..t), including the current month-end close.
- **Data needs:** daily or month-end adjusted close for SPY (S&P 500 TR index pre-1993); FRED/ALFRED RRSFS (vintages), lagged 1 month; FRED/ALFRED INDPRO (vintages), lagged 1 month; 3-month T-bill rate (e.g., FRED TB3MS/DTB3) for cash; older retail sales series for pre-1992 stitching
- **ETF-only start:** 1993 (SPY); RRSFS from 1992
- **In plain English:** Stay fully in US stocks whenever both retail sales and industrial production are growing year over year. Only when one of them is shrinking (a recession warning) do you let the classic 10-month moving average decide whether to stay in stocks or move to cash.
- **Rules:**
  1. At the close on the last trading day of month m, read FRED RRSFS (Real Retail and Food Services Sales) and INDPRO (Industrial Production Index) for month m-1 (FRED date m-1/01), using the data vintage available at that date (AS uses vintage/ALFRED data since May 2023).
  2. Compute the year-over-year change of each series for month m-1 versus month m-13.
  3. If both YoY changes are positive: no recession signal; hold 100% SPY regardless of price trend.
  4. If either YoY change is negative: recession signal; check trend. If SPY's month-end close is above its 10-month simple moving average of month-end closes (current month included), hold 100% SPY; otherwise hold 100% cash (3-month T-bills).
  5. Execute at the same close; hold until the last trading day of the following month.
  6. Alternate (non-month-end) trading days in AS use data lagged one further month (m-2).
- **Notes:** PE also tested a daily version with a 200-day MA and other growth signals (real EPS, employment, real personal income, housing starts); PE's preferred combination is retail sales + industrial production, which AS tests. PE compares the S&P 500 total-return index with its 10-month average; AS does not say whether its SMA uses price or dividend-adjusted closes (AS generally uses dividend-adjusted data). AS notes replacing cash with IEF or AGG would have raised returns ~1%/yr (not part of the rules). Vintage data changed 1.7% of historical monthly allocations. Exact behaviour at a YoY of exactly 0 is not specified.

### 32. Growth-Trend Timing - UE Rate (`philoeconomics_gtt_unemployment`)

*Philosophical Economics (pseudonymous blogger 'Jesse Livermore')*, family **macro**, AS status **tracked**, spec status **full**.

- **Source:** In Search of the Perfect Recession Indicator (2016), https://www.philosophicaleconomics.com/2016/02/uetrend/
- **AS page:** https://allocatesmartly.com/philosophical-economics-growth-trend-timing-redux/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY']; defensive []; canary []; cash cash
- **Signal:** Data month d = m-1 (1-month lag). UE_d = UNRATE for month d; UE_SMA12 = mean(UNRATE_{d-11..d}) (12 months ending with month d, inclusive). RECESSION = UE_d > UE_SMA12. TREND_UP = SPY_close_t > SMA_10(month-end closes t-9..t).
- **Data needs:** month-end adjusted close for SPY (S&P 500 TR index pre-1993); FRED/ALFRED UNRATE with vintages, lagged 1 month; pre-1948 monthly unemployment rate series for long backtests; 3-month T-bill rate for cash
- **ETF-only start:** 1993 (SPY)
- **In plain English:** Stay fully in US stocks unless last month's unemployment rate has climbed above its own 12-month average, which tends to happen near recessions. In that case, hold stocks only if the market is above its 10-month moving average; otherwise sit in cash.
- **Rules:**
  1. At the close on the last trading day of month m, take FRED UNRATE (civilian unemployment rate, seasonally adjusted) for months m-12 through m-1, using the vintage available at that date (AS uses ALFRED vintages since May 2023: all 12 values as known at month-end m, including any revisions released by then but none after).
  2. Compute the 12-month average of UNRATE over months m-12..m-1.
  3. If UNRATE for month m-1 is higher than that 12-month average: recession signal; otherwise no recession signal.
  4. No recession signal: hold 100% SPY regardless of price.
  5. Recession signal: hold 100% SPY if SPY's month-end close is above its 10-month SMA of month-end closes (current month included); otherwise hold 100% cash (3-month T-bills).
  6. Execute at the same close; hold until the last trading day of the following month. AS alternate (earlier) trading days use data lagged one extra month.
- **Notes:** PE's original UE post compares the unemployment rate to its trailing 12-month MA and the S&P 500 total-return index to its 10-month MA; PE does not discuss publication lag, AS adds a 1-month lag. AS's 2019 redux tests both GTT variants from 1930 and says they agree ~96% of the time. Vintage data changed 0.9% of historical monthly allocations. AS does not state whether its SPY SMA uses price or dividend-adjusted closes. Equality (UE exactly equal to SMA) treated as no recession per AS wording 'higher than'. This rule is also the timing engine in Keller's Lethargic Asset Allocation and is closely related to Novell's SPY-UI/Bond UI1.

### 33. SPY-COMP (`novell_spy_comp`)

*Paul Novell (Investing for a Living)*, family **macro**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** SPY-COMP (proprietary; Economic Pulse newsletter, Investing for a Living - rules members-only) (2020), https://investingforaliving.us/about-the-economic-pulse-newsletter/
- **AS page:** https://allocatesmartly.com/paul-novells-flagship-strategy-spy-comp/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY']; defensive ['IEF']; canary []; cash None
- **Signal:** PARTIALLY UNDISCLOSED. RECESSION = any one of 6 (undisclosed) monthly economic indicators signals recession, using data for the previous month (1-month lag) and vintage data. If RECESSION, a price trend-following rule on US equities (undisclosed; AS calls it a simple, standard trend rule) decides SPY vs IEF.
- **Data needs:** month-end (and possibly daily) adjusted closes for SPY and IEF with index proxies to 1970; 6 undisclosed monthly macro series (FRED/ALFRED vintages, lagged 1 month)
- **ETF-only start:** 2002 (IEF Jul 2002)
- **In plain English:** Stay fully in US stocks while a dashboard of six economic indicators looks healthy. If any of them flashes a recession warning, let the stock market's price trend decide between staying in stocks or switching entirely to intermediate Treasuries.
- **Rules:**
  1. At the close on the last trading day of month m, evaluate 6 economic indicators using their month m-1 values (1-month publication lag; AS vintage data since May 2023). Indicator identities and thresholds are not disclosed.
  2. If no indicator signals recession: hold 100% SPY regardless of price trend.
  3. If any one indicator signals recession: apply a trend-following test to US equities; if the trend is up hold 100% SPY, otherwise hold 100% IEF (trend rule undisclosed).
  4. Execute at the same close; hold until the next month-end. Portfolio is always 100% in a single asset.
- **Notes:** AS (Apr 2020) chose not to disclose SPY-COMP rules to members; only the structure above is public. Novell's public newsletter page now describes SPY-COMP as using 7 key indicators and mentions an updated SPY-MODCOMP (V2), which differs from AS's description of 6 indicators (the AS-tracked version is the 6-indicator original). Novell's site rule pages are members-only. AS reports ~1 turnover per year and also offers a 'dynamic bond' variant (separate). Indicator list and trend rule cannot be verified; strategy is not exactly replicable from public data.

### 34. Bond-COMP (`novell_bond_comp`)

*Paul Novell (Investing for a Living)*, family **macro**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** Enhancing Returns of TAA Bond Strategies (mentions BOND-COMP; full rules in members-only Economic Pulse newsletter) (2019), https://investingforaliving.us/2019/07/18/enhancing-returns-of-taa-bond-strategies/
- **AS page:** https://allocatesmartly.com/paul-novells-bond-comp-tactical-bond-strategy/
- **Rebalance:** monthly, last trading day close; equal-weight basket rebalanced monthly (AS convention)
- **Universe:** risky ['HYG', 'LQD', 'BNDX', 'EMB']; defensive ['IEF', 'TLT', 'GLD']; canary []; cash cash
- **Signal:** Same regime signal as SPY-COMP: RISK_ON unless any of 6 undisclosed economic indicators (month m-1 data, vintage) signals recession; if recession is signalled, an undisclosed price trend-following rule decides risk-on vs risk-off (presumably the same equity trend test as SPY-COMP - uncertain).
- **Data needs:** month-end adjusted closes for HYG, LQD, BNDX, EMB, IEF, TLT, GLD (+ index proxies to 1970); 3-month T-bill series for cash; 6 undisclosed FRED/ALFRED macro series lagged 1 month; SPY (or other) price series for the trend leg
- **ETF-only start:** 2013 (BNDX Jun 2013; HYG Apr 2007, EMB Dec 2007)
- **In plain English:** Uses SPY-COMP's economic-plus-trend switch, but instead of stocks vs Treasuries it holds an equal mix of credit-type bonds (high yield, corporate, international and emerging market) when conditions look fine, and an equal mix of Treasuries, gold and cash when a recession is signalled and confirmed by price.
- **Rules:**
  1. At the close on the last trading day of month m, compute the SPY-COMP regime signal (6 undisclosed economic indicators lagged 1 month, any-one-triggers, then trend confirmation).
  2. Risk on (no recession signal, or recession signal but trend up): hold 25% each in HYG, LQD, BNDX, EMB.
  3. Risk off (recession signal and trend down): hold 25% each in IEF, TLT, GLD and cash (cash/short-term Treasuries; AS models short-term Treasuries as cash).
  4. Hold until the next month-end; rebalance to equal weights monthly.
- **Notes:** AS describes Bond-COMP as an upgrade of Bond UI1 (UE-rate only) using SPY-COMP's 6-indicator rules. Baskets and equal weighting are stated by AS; the regime signal is a black box. How pre-inception periods for HYG/EMB/BNDX are filled in the 1970 backtest is not stated. Benchmark in AS post is an equal-weight portfolio of the underlying assets. Not exactly replicable from public data.

### 35. Bond UI1 (`novell_bond_ui1`)

*Paul Novell (Investing for a Living)*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** Enhancing Returns of TAA Bond Strategies / Adding Zero Yield Assets to TAA Bond Strategies / Using Economic Indicators to Time the Market (UI indicator) (2019), https://investingforaliving.us/2019/08/06/adding-zero-yield-assets-to-taa-bond-strategies/
- **AS page:** https://allocatesmartly.com/weve-added-three-new-strategies/
- **Rebalance:** monthly, last trading day close (AS default; uncertain)
- **Universe:** risky ['HYG', 'LQD', 'BNDX', 'EMB']; defensive ['IEF', 'TLT', 'GLD']; canary []; cash cash
- **Signal:** Data month d = m-1 (1-month lag, vintage). UI_RISK_OFF = UNRATE_d > SMA_12(UNRATE_{d-11..d}); otherwise risk on. No price-trend confirmation in Novell's 'simple monthly SPY-UI indicator' (uncertain whether AS adds one).
- **Data needs:** month-end adjusted closes for HYG, LQD, BNDX, EMB, IEF, TLT, GLD (+ proxies); FRED/ALFRED UNRATE vintages lagged 1 month; 3-month T-bill series for cash
- **ETF-only start:** 2013 (BNDX Jun 2013)
- **In plain English:** A bond strategy driven only by the unemployment rate: while unemployment is falling relative to its 1-year average it holds a mix of credit-risk bonds; when unemployment turns up it switches to Treasuries, gold and cash.
- **Rules:**
  1. At the close on the last trading day of month m, compare the unemployment rate (UNRATE) for month m-1 with its 12-month simple moving average (vintage data as of that date).
  2. If UNRATE is below (not above) its 12-month SMA: risk on - hold equal weights (25% each) of HYG, LQD, BNDX, EMB.
  3. If UNRATE is above its 12-month SMA: risk off - hold equal weights of the government/hedge basket: IEF, TLT, GLD and cash (Novell's GOVH set is SHY, IEF, TLT, GLD; AS models SHY as cash) - uncertain.
  4. Hold until the next month-end; rebalance to equal weights monthly.
- **Notes:** No dedicated public AS post; AS's Aug 2019 announcement says Bond UI1 uses the US unemployment rate to switch between credit-risk bonds and US government bonds/gold, and AS's vintage-data post lists it. Novell's Jul 2019 post defines UI1 as CRED (HYG, EMB, BNDX, LQD equal weight) vs GOV (SHY, IEF, TLT equal weight) switched by his simple monthly SPY-UI indicator (UNRATE vs 12-month SMA, Part 1 of his 2016 series, no price confirmation); his Aug 2019 post adds GLD (GOVH). AS's 'government bonds/gold' wording suggests the GLD version - exact AS risk-off basket and whether AS applies a trend filter are unverified. Superseded by Bond-COMP; AS flagged it as a candidate for future removal.

### 36. Tactical Bond Strategy (`novell_tactical_bond`)

*Paul Novell (Investing for a Living)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** A Trend Following Bond Portfolio for Any Environment (GTAA Bond 3) (2014), https://investingforaliving.us/2014/12/06/a-trend-following-bond-portfolio-for-any-environment/
- **AS page:** https://allocatesmartly.com/paul-novells-tactical-bond-strategy/
- **Rebalance:** monthly, last trading day close; full rebalance monthly
- **Universe:** risky ['IEF', 'TLT', 'TIP', 'LQD', 'HYG', 'BNDX', 'EMB']; defensive []; canary []; cash cash
- **Signal:** R6_i = P_t / P_{t-6m} - 1 on month-end total-return closes for SHY(=cash), IEF, TLT, TIP, LQD, HYG, BNDX, EMB. Hurdle: R6_BIL = 6-month return of BIL (3-month T-bills). Asset passes if R6_i > 0 AND R6_i > R6_BIL.
- **Data needs:** month-end adjusted closes for SHY, IEF, TLT, TIP, LQD, HYG, BNDX, EMB, BIL (+ BWX and index proxies pre-inception); 3-month T-bill series for cash
- **ETF-only start:** 2013 (BNDX Jun 2013); ~2007-12 using BWX for BNDX (EMB Dec 2007, HYG Apr 2007, BIL May 2007)
- **In plain English:** Each month, pick the three bond types (from short, intermediate and long Treasuries, inflation-protected, corporate, high-yield, international and emerging-market bonds) with the best 6-month returns, and give each a third of the money - but only if it beat both zero and T-bills; otherwise that third goes to cash.
- **Rules:**
  1. At the close on the last trading day of the month, compute the 6-month total return of SHY, IEF, TLT, TIP, LQD, HYG, BNDX and EMB (assets without data at that date are excluded - implied by AS).
  2. Rank and select the top 3 by 6-month return.
  3. For each of the 3: if its 6-month return is positive AND greater than BIL's 6-month return, allocate 1/3 of the portfolio to it; otherwise allocate that 1/3 to cash.
  4. Any 1/3 slot assigned to SHY is held as cash instead (AS convention).
  5. Hold until the last trading day of the following month; rebalance the entire portfolio monthly even if holdings are unchanged. Tie-breaks unspecified.
- **Notes:** Rules are fully stated by AS (Jan 2017). AS adds the BIL hurdle (author used only a positive-return hurdle) and executes at month-end same-day close (author: every 4 weeks, next-day close). Novell's 2014 original 'GTAA Bond 3' had a different/expanded universe (JNK, IGOV, MUB, later EMB) and his 2019 update cites 9 ETFs; the AS 8-asset universe was not reconciled with Novell's current list. AS backtest from 1970 with limited data for several assets; benchmark = equal weight of live assets.

### 37. TrendYCMacro (`quantpedia_trendycmacro`)

*Ďurian and Radovan Vojtko (Quantpedia)*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** Avoid Equity Bear Markets with a Market Timing Strategy (2023), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4397638
- **AS page:** https://allocatesmartly.com/testing-trendycmacro-from-durian-and-vojtko-of-quantpedia/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month; hold until the next month-end
- **Universe:** risky ['SPY']; defensive []; canary []; cash BIL
- **Signal:** Daily excess return XS_d = r_SPY,d - r_BIL,d (adjusted closes). Excess-return index I_d = prod(1+XS). TREND_SMA = I_t > mean(I over last 200 trading days incl. today). RACHEV = mean(XS_d over last 200 days with XS_d > median of those 200) / ( -1 * mean(XS_d over last 200 days with XS_d < median) ); TREND_RR = RACHEV > 1 (Rachev ratio RR(0.5,0.5)). YC = 10y UST yield > 3m UST yield at month-end. MACRO = [YoY(RRSFS) > 0] AND [YoY(INDPRO) > 0] AND [YoY(HOUST) > 0], where YoY uses the observation for the PREVIOUS month: X_{m-1}/X_{m-13} - 1 (1-month publication lag). LONG_m = (LONG_{m-1} AND MACRO_m) OR (TREND_SMA_m AND TREND_RR_m AND YC_m).
- **Data needs:** daily adjusted close SPY (or S&P 500 TR pre-1993); daily BIL / 13-week T-bill return series for excess returns; FRED/ALFRED RRSFS (vintage), lagged 1 month; FRED/ALFRED INDPRO (vintage), lagged 1 month; FRED/ALFRED HOUST (vintage), lagged 1 month; 10-year and 3-month Treasury yields at month-end (e.g., FRED DGS10 and DTB3/DGS3MO; long-history sources pre-1962)
- **ETF-only start:** 1994 approx (SPY 1993-01 plus 200-day warm-up; BIL 2007 but T-bill index can substitute); RRSFS only from 1992
- **In plain English:** Holds the US stock market or cash. It stays invested while the economy (retail sales, industrial production and housing starts) is growing year over year, and otherwise only buys stocks when price trend, a return-asymmetry trend measure, and a non-inverted yield curve all agree.
- **Rules:**
  1. At the close of the last trading day of month m, compute YoY change of RRSFS (real retail & food services sales), INDPRO (industrial production) and HOUST (housing starts) using the data point for month m-1 vs month m-13 (vintage/as-first-available data where possible).
  2. If all three YoY changes are > 0 AND the strategy is currently long SPY, stay 100% SPY (macro strength can only maintain, never initiate, a long position).
  3. Otherwise compute, from daily SPY returns in excess of BIL (T-bill) returns: (a) excess-return index above its 200-day simple average; (b) 200-day Rachev ratio RR(0.5,0.5) > 1; (c) 10-year Treasury yield > 3-month Treasury yield.
  4. If (a), (b) and (c) are all true, go/stay 100% SPY at the close.
  5. If neither the macro-persistence condition nor the full trend+yield-curve condition holds, move 100% to cash (AS: BIL-destined funds are held as cash earning 13-week T-bill return).
  6. Hold until the close of the last trading day of the following month.
- **Notes:** AS replicated using the authors' exact calculations; AS results ~40 bp/yr lower due to 0.1%/trade costs, SPY expense ratio pre-ETF, vintage macro data and non-French data. AS backtest from 1927. Discrepancy with Quantpedia's blog series (Part 3): the blog's final TrendYCMacro uses INDPROD, RSALES and DIVIDEND (Shiller real dividends) for the macro branch, not HOUST; AS (post Sept 2023, from authors' final paper) lists RRSFS, INDPRO, HOUST - follow AS. Quantpedia Part 1 defines Trend as AND of 200-day SMA and RR(0.5,0.5)>1 on market excess returns, monthly decision. Rachev>1 with a median split is practically equivalent to the 200-day mean daily excess return being positive. Whether the 200-day SMA window includes the current day, and exact macro proxies before RRSFS (1992) / HOUST (1959), are not public. Original SSRN PDF could not be accessed (403).

### 38. Pragmatic Asset Allocation (`quantpedia_pragmatic_aa`)

*Radovan Vojtko and Javorská (Quantpedia)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Pragmatic Asset Allocation Model for Semi-Active Investors (2024), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4715415
- **AS page:** https://allocatesmartly.com/pragmatic-asset-allocation-from-vojtko-and-javorska-of-quantpedia/
- **Rebalance:** 4 annual tranches (25% each) traded at the close of the last trading day of Jan, Apr, Jul, Oct (one tranche per date) using signals from the prior month-end (Dec, Mar, Jun, Sep); whole portfolio rebalanced monthly to target weights
- **Universe:** risky ['ACWI', 'QQQ', 'EEM']; defensive ['IEF', 'GLD', 'BIL']; canary []; cash cash
- **Signal:** At signal month-end s (month before trade): MOM12_i = P_s / P_{s-12} - 1 on dividend-adjusted month-end closes; SMA12_i = mean(P_{s-11..s}) (12 month-end closes incl. s); UP_i = P_s > SMA12_i. YC_OK = 10Y UST yield > 3M UST yield at month-end s (AS: actual month-end values).
- **Data needs:** monthly (month-end) adjusted closes ACWI, QQQ, EEM, IEF, GLD, BIL (plus index proxies pre-inception); month-end 10-year and 3-month Treasury yields (e.g., FRED DGS10, DTB3/DGS3MO; authors used GS10, TB3MS); 13-week T-bill return for cash; per-tranche holding start dates to evaluate the >12-month stop-loss condition
- **ETF-only start:** 2009 approx (ACWI 2008-03 plus 12-month lookback)
- **In plain English:** Four overlapping sleeves each rebalance once a year, buying the two strongest of world stocks, Nasdaq-100 and emerging markets if they are in uptrends, or moving to gold/Treasuries/cash when the yield curve is inverted or trends fail. Positions are designed to be held at least a year for tax efficiency, with a quarterly trend check as a safety valve.
- **Rules:**
  1. Split the portfolio into 4 independent tranches of 25%. Tranche k trades only once per year, at the close of the last trading day of its month (1, 4, 7 or 10), using data as of the end of the previous month (12, 3, 6 or 9).
  2. For the trading tranche: if the yield curve is inverted (10Y <= 3M at the signal date), send the whole 25% tranche to the defensive step.
  3. Otherwise rank ACWI, QQQ, EEM by MOM12 descending. For each of the top two only: if UP_i, allocate 12.5% of the total portfolio to it; if not, that 12.5% goes to the defensive step (the 3rd-ranked asset never substitutes).
  4. Defensive step for the amount D sent to defense: rank IEF, GLD, BIL by MOM12 descending; each of the top two receives D/2 if UP_i, otherwise its D/2 goes to cash. BIL allocations are held as cash (AS convention). A tranche can therefore hold up to 3 assets (1 risky + 2 defensive).
  5. Stop-loss on the other three (non-trading) tranches at each tranche date (months 1,4,7,10): for every asset they hold, if the asset's prior month-end close < its SMA12 (as of prior month-end) AND it has been held more than 12 months, sell that slice to cash and keep it in cash until that tranche's next scheduled trade.
  6. Every month-end, rebalance all holdings back to their target fraction of the whole portfolio (simplifying assumption of the authors, matched by AS).
  7. All trades at the close of the last trading day of the month.
- **Notes:** AS also tracks a 'Pragmatic Asset Allocation - Amended' variant (seen in AS correlation table alongside '- Original'): per Quantpedia's follow-up 'A few thoughts on Pragmatic Asset Allocation', the yield-curve risk-off switch is valid for only 12 months; after that, if the curve is still inverted but the moving-average price signal is positive, the YC signal is ignored. Exact AS implementation of the amended version is not public. Unclear details: how tranches are seeded at backtest start (assume staggered start), and whether 'held more than 12 months' counts continuous holding across a tranche's re-selection (AS wording implies yes). Quantpedia says the authors' stop-loss is checked only on quarterly dates and executed at the next tranche date. AS notes 2025 ETF swaps (EEM->IEMG) may apply - verify. Authors' backtest starts 1928; AS starts 1970.

### 39. Gold Cross-Asset Momentum (`quantpedia_gold_cross_asset_momentum`)

*Cyril Dujava (Quantpedia)*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** Cross-Asset Price-Based Regimes for Gold (2025), https://quantpedia.com/cross-asset-price-based-regimes-for-gold/
- **AS page:** https://allocatesmartly.com/gold-cross-asset-momentum/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month
- **Universe:** risky ['GLD']; defensive []; canary ['IEF']; cash cash
- **Signal:** R12_i = TR_t / TR_{t-12} - 1 on dividend-adjusted month-end closes for GLD and IEF; LONG = (R12_GLD > 0) AND (R12_IEF > 0) (strictly positive).
- **Data needs:** monthly adjusted closes GLD and IEF (gold spot and Treasury TR index proxies pre-ETF); 13-week T-bill return for cash
- **ETF-only start:** 2005 approx (GLD 2004-11 plus 12-month lookback)
- **In plain English:** Own gold only when both gold and intermediate Treasuries have risen over the past year; otherwise sit in cash. The idea is that gold does best when falling yields (rising bond prices) and gold's own trend agree.
- **Rules:**
  1. At the close of the last trading day of the month compute 12-month total return of GLD and IEF.
  2. If both are strictly positive, hold 100% GLD; otherwise hold 100% cash (13-week T-bill return).
  3. IEF is a signal only and is never held.
  4. Hold until the close of the following month.
- **Notes:** Quantpedia sample 1969-12 to 2025-09; author tested 1/3/6/12-month windows and all four joint sign states, recommending only the 12-month GLD-up/IEF-up state. Author's cash leg earns Fed Funds; AS uses T-bills (cash). AS backtest from 1970. AS frames it as a small-allocation diversifier or a gold overlay rather than a standalone portfolio.

### 40. Optimal Trend Following (`zakamulin_optimal_trend_following`)

*Valeriy Zakamulin and Javier Giner*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** Optimal Trend Following Rules in Two-State Regime-Switching Models (2022), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4217513
- **AS page:** https://allocatesmartly.com/zakamulins-optimal-trend-following/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month
- **Universe:** risky ['SPY']; defensive []; canary []; cash cash
- **Signal:** IND_t = sum_{k=1..30} w_k * r_{t-k+1}, where r_t is the S&P 500 monthly total return (dividend-adjusted month-end closes) for the month ending at t (k=1 = most recent month). LONG if IND_t > 0. Approximate weights w_k digitized from the authors' chart (label 'NB(4) weights', scale irrelevant): k1 0.0925, k2 0.0739, k3 0.0582, k4 0.0443, k5 0.0325, k6 0.0221, k7 0.0136, k8 0.0061, k9 0.0000, k10 -0.0046, k11 -0.0082, k12 -0.0107, k13 -0.0125, k14 -0.0136, k15 -0.0139, k16 -0.0143, k17 -0.0139, k18 -0.0132, k19 -0.0125, k20 -0.0118, k21 -0.0107, k22 -0.0096, k23 -0.0089, k24 -0.0079, k25 -0.0068, k26 -0.0057, k27 -0.0050, k28 -0.0043, k29 -0.0032, k30 -0.0025.
- **Data needs:** monthly dividend-adjusted closes SPY / S&P 500 TR (>= 30 months history); 13-week T-bill return for cash
- **ETF-only start:** 1996 approx (SPY 1993-01 plus 30-month weight window)
- **In plain English:** A trend signal for the S&P 500 that rewards recent gains (last ~8 months) but treats gains from 10-30 months ago as a sign the bull run may be getting old. Invest when the combined score is positive, otherwise hold cash.
- **Rules:**
  1. At the close of the last trading day of each month, compute the weighted sum of the last 30 monthly total returns of the S&P 500 using the optimal weights (positive for lags 1-8, ~0 at lag 9, negative for lags 10-30).
  2. If the indicator is positive, hold 100% SPY; otherwise hold 100% cash (13-week T-bill return).
  3. Hold until the close of the following month.
- **Notes:** Weights are derived by the authors from a two-state semi-Markov (duration-dependent) regime-switching model calibrated to 1897-2020 US data, maximizing Sharpe ratio; no price optimisation. AS gives only the qualitative shape (bullish <=8m, bearish 10-30m) and the chart; the numbers above are a pixel read of that chart (lag 9 ~0, lag 30 still slightly negative - weights beyond lag 30 assumed zero; uncertain). Whether the authors' rule uses excess or total returns is not confirmed (AS says dividend-adjusted returns). SSRN PDF inaccessible (403); verify weights against the paper before production use.

### 41. Risk Managed Momentum (RMM) (`aspect_risk_managed_momentum`)

*Bard Malovany / Aspect Partners*, family **momentum-rotation**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** Risk Managed Momentum (proprietary model of Aspect Partners; rules undisclosed) (None), https://www.aspect-partners.com/
- **AS page:** https://allocatesmartly.com/aspect-partners-risk-managed-momentum/
- **Rebalance:** monthly; AS assumes execution at the month-end close
- **Universe:** risky ['DBC']; defensive []; canary []; cash cash
- **Signal:** UNDISCLOSED. Publicly known only: momentum measured over multiple long and short lookbacks, heavily weighted to short-term momentum; a crash-protection switch moves the entire portfolio to bonds/cash when risk assets show even mild weakness.
- **Data needs:** undisclosed
- **ETF-only start:** unknown (at least 2006 given DBC)
- **In plain English:** An aggressive, frequently-trading momentum strategy from an advisory firm that rotates among asset classes and quickly retreats fully to bonds/cash when risk assets weaken. Its exact rules are confidential.
- **Rules:**
  1. Not replicable from public information: AS knows the rules but withholds them at Aspect Partners' request.
  2. AS conventions applied: trades at month-end close; DBC used in place of the author's GSG for commodities; any author allocation to SHY is held as cash (13-week T-bill).
  3. Behavioural facts for sanity checks: ~7x annual turnover (most active strategy on AS as of 2020); ~50% of months 100% in bonds/cash; can be 100% in risk assets.
- **Notes:** Black-box strategy: cannot be specified. Aspect Partners' public website (checked) does not describe RMM rules or universe. Only DBC (commodities, replacing GSG) and SHY->cash are known universe members; the rest of the risky and defensive universe is unknown.

### 42. US Cross-Asset Momentum (`pitkajarvi_us_cross_asset_momentum`)

*Aleksi Pitkäjärvi, Matti Suominen, Lauri Vaittinen*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** Cross-asset signals and time series momentum (Journal of Financial Economics) (2020), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2891434
- **AS page:** https://allocatesmartly.com/cross-asset-signals-and-time-series-momentum/
- **Rebalance:** monthly; signal near and trade at the close of the last trading day of the month
- **Universe:** risky ['SPY']; defensive ['IEF']; canary []; cash cash
- **Signal:** XS_SPY = R12(SPY) - R12(BIL); XS_IEF = R12(IEF) - R12(BIL), where R12 = P_t/P_{t-12} - 1 on dividend-adjusted month-end closes (BIL = 3-month T-bill).
- **Data needs:** monthly adjusted closes SPY, IEF; 3-month T-bill total return series
- **ETF-only start:** 2003 approx (IEF 2002-07 plus 12-month lookback; T-bill index for BIL pre-2007)
- **In plain English:** Holds US stocks when both stocks and Treasuries have beaten cash over the past year, holds Treasuries when bonds are up but stocks are down, and otherwise sits in cash. It uses the finding that rising bond prices are good news for stocks while strong stocks are bad news for bonds.
- **Rules:**
  1. At month-end compute 12-month excess returns of SPY and IEF over T-bills.
  2. If XS_SPY > 0 and XS_IEF > 0: hold 100% SPY.
  3. Else if XS_SPY < 0 and XS_IEF > 0: hold 100% IEF.
  4. Otherwise (IEF excess return <= 0): hold 100% cash.
  5. Hold until the close of the following month.
- **Notes:** AS tests a simplified long-only, unlevered, US-only version; the paper trades long/short across many international markets, combining own-asset TSMOM with cross-asset signals (bond past returns positive predictor for equities; equity past returns negative predictor for bonds). Whether excess return is the difference of compounded 12m returns or of summed monthly excess returns is not specified (immaterial for sign in most cases). Treatment of exactly-zero values not specified. Spends ~half of months in cash.

### 43. US Risk Parity Trend-Following (`clare_us_risk_parity_trend`)

*Andrew Clare, James Seaton, Peter N. Smith, Stephen Thomas*, family **risk-parity**, AS status **tracked**, spec status **partial**.

- **Source:** The Trend is Our Friend: Risk Parity, Momentum and Trend Following in Global Asset Allocation (2016), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2126478
- **AS page:** https://allocatesmartly.com/taa-strategy-combining-risk-parity-trend-following/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month; full rebalance every month
- **Universe:** risky ['SPY', 'IWM', 'IEF', 'DBC', 'VNQ']; defensive []; canary []; cash cash
- **Signal:** Simple risk parity (Asness, Frazzini & Pedersen): RPW_i = (1/sigma_i) / sum_j(1/sigma_j), sigma_i = volatility of asset i's returns over the trailing 12 months, computed over all 5 assets regardless of trend. TREND_i = P_i,t > SMA10_i, SMA10 = mean of the last 10 month-end closes including the current one; P is the cash (non-dividend-adjusted) price for SPY, IWM, VNQ.
- **Data needs:** daily and month-end closes (price and adjusted) for SPY, IWM, IEF, DBC, VNQ; 13-week T-bill return for cash
- **ETF-only start:** 2007 approx (DBC 2006-02 plus 12-month volatility window)
- **In plain English:** Gives each of five US asset classes a weight inversely proportional to its volatility, so calm assets like Treasuries get more money. Each asset is held only while it trades above its 10-month average; otherwise its share sits in cash.
- **Rules:**
  1. At the close of the last trading day of each month, compute 12-month volatility for SPY, IWM, IEF, DBC, VNQ and set inverse-volatility weights summing to 100%.
  2. For each asset: if its close is above its 10-month SMA, hold its risk-parity weight; otherwise hold that weight in cash (13-week T-bill).
  3. Hold until the last trading day of the following month; rebalance the whole portfolio monthly even if signals are unchanged.
- **Notes:** AS tested the broad asset-class strategy of Section 3.1 of the paper. Average cash ~30%. AS mentions it would prefer ERC (covariance-aware) to simple RP but tests simple RP. Asness et al. originally estimated vol with a 3-year window of monthly excess returns and scaled to a vol target with leverage; AS uses a 12-month window, unlevered weights summing to 100% (normalisation assumed). Data frequency of the 12-month vol is not stated. AS 2022+ commodity ETF stitch DBC->PDBC per AS conventions. Journal: Journal of Behavioral and Experimental Finance (2016); SSRN version 2012. Paper PDF not accessed (SSRN 403).

### 44. Global Risk Parity Trend-Following (`clare_global_risk_parity_trend`)

*Andrew Clare, James Seaton, Peter N. Smith, Stephen Thomas*, family **risk-parity**, AS status **tracked**, spec status **partial**.

- **Source:** The Trend is Our Friend: Risk Parity, Momentum and Trend Following in Global Asset Allocation (2016), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2126478
- **AS page:** https://allocatesmartly.com/taa-strategy-combining-risk-parity-trend-following/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month; full rebalance every month
- **Universe:** risky ['SPY', 'EFA', 'EEM', 'IEF', 'BWX', 'DBC', 'RWO']; defensive []; canary []; cash cash
- **Signal:** RPW_i = (m_i/sigma_i) / sum_j(m_j/sigma_j), sigma_i = trailing 12-month volatility; m_i = 0.5 for SPY, EFA, IEF, BWX and 1.0 for EEM, DBC, RWO. TREND_i = P_i,t > SMA10_i (10 month-end closes incl. current); cash (non-adjusted) price used for SPY, EFA, EEM, RWO.
- **Data needs:** daily and month-end closes (price and adjusted) for SPY, EFA, EEM, IEF, BWX, DBC, RWO; 13-week T-bill return for cash
- **ETF-only start:** 2009 approx (RWO 2008-05 and BWX 2007-10 plus 12-month volatility window)
- **In plain English:** A global version of the inverse-volatility plus 10-month trend filter idea, using US and international stocks, emerging markets, US and international government bonds, commodities and global REITs. Assets below trend are swapped for cash, keeping the portfolio balanced and low-volatility.
- **Rules:**
  1. At the close of the last trading day of each month, compute 12-month volatility for all 7 assets and inverse-volatility weights, halving the raw weight of SPY, EFA, IEF and BWX (they split one asset-class slot each: US/intl equities and US/intl government bonds), then normalise to 100%.
  2. For each asset: if its close is above its 10-month SMA, hold its weight; otherwise that weight goes to cash (13-week T-bill).
  3. Hold until the last trading day of the following month; rebalance the whole portfolio monthly.
- **Notes:** AS's parenthetical says 'sigma-hat is multiplied by 0.5' but the main text says these assets get half their normal risk-parity weight; implement as half weight (multiplier on 1/sigma). The half allocation also applies to AS's equal-weight benchmark. AS 2025 ticker conventions may replace EFA->IEFA, EEM->IEMG, RWO->REET and DBC->PDBC (from ~2022) - not stated in this 2017 post; verify. Normalisation to 100% and the vol return frequency are assumptions. AS notes alternate-trading-day results suggest the month-end timing may be slightly optimistic.

### 45. Momentum Turning Points (`garg_momentum_turning_points`)

*Ashish Garg, Christian L. Goulding, Campbell R. Harvey, Michele G. Mazzoleni*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** Momentum Turning Points (JFE 2023; SSRN 2019) and Breaking Bad Trends (FAJ 2023) (2023), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3489539
- **AS page:** https://allocatesmartly.com/momentum-turning-points/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month; speed parameters re-estimated every 5 years
- **Universe:** risky ['SPY', 'EFA', 'IEF', 'BWX', 'DBC', 'GLD']; defensive []; canary []; cash cash
- **Signal:** r = monthly dividend-adjusted return minus 13-week T-bill return. SLOW_t = +1 if mean(r_{t-11..t}) >= 0 else -1 (arithmetic average of monthly excess returns). FAST_t = +1 if mean(r over last F months) >= 0 else -1, F = 2 (Portfolio) or 1 (Simple). State: Bull (S+,F+), Correction (S+,F-), Bear (S-,F-), Rebound (S-,F+). Position: Bull +1; Bear -1; Correction (1 - 2*a_Co); Rebound (2*a_Re - 1). Speeds from historical data before the estimation date, with r' = next-month excess return after each state: C = (FREQ[Bu]/FREQ[Bu or Be]) * AVG[r'|Bu]/AVG[r'^2|Bu or Be] - (FREQ[Be]/FREQ[Bu or Be]) * AVG[r'|Be]/AVG[r'^2|Bu or Be]; a_Co = 0.5*(1 - (1/C) * AVG[r'|Co]/AVG[r'^2|Co]); a_Re = 0.5*(1 + (1/C) * AVG[r'|Re]/AVG[r'^2|Re]); clip a to [0,1].
- **Data needs:** monthly adjusted closes SPY, EFA, IEF, BWX, DBC, GLD plus long index histories back to 1958 for estimation; 13-week T-bill monthly returns; Ken French market excess returns from 1926-07 (Simple flavor)
- **ETF-only start:** 2008 approx (BWX 2007-10; estimation requires long pre-ETF index histories)
- **In plain English:** Classifies each asset as in a bull, bear, correction or rebound by comparing its 12-month and 2-month trends. In bulls it is fully invested, in bears it is out, and in corrections/rebounds it takes a partial position whose size is learned from how those states played out historically.
- **Rules:**
  1. For each asset, build monthly excess returns over T-bills from the earliest available data (AS: from 1958-12 for Portfolio where possible; 1926-07 French data for Simple).
  2. Every 5 years, re-estimate a_Co and a_Re per asset from all history up to the prior month (expanding window) using the formulas in 'signal'; clip to [0,1]. (Paper: at least 12 months in each state required; BBT paper re-estimates every 30 months.)
  3. At each month-end classify each asset's state from its 12-month and fast-window average excess returns and compute its position (+1, -1, 1-2a_Co or 2a_Re-1).
  4. Long-only AS adaptation: negative positions are held as cash; positive position p in [0,1] scales the asset's slot.
  5. Portfolio flavor: each of the 6 assets gets an equal slot of 1/6 (paper equal-weights within and across asset classes) times its position; unallocated remainder in cash; any final position below 2% is moved to cash.
  6. Simple flavor: SPY only, fast window = 1 month, slot = 100%.
  7. Hold until next month-end.
- **Notes:** AS tracks one strategy named 'Momentum Turning Points' but describes two flavors (Simple: SPY only; Portfolio: 6 assets, 2-month fast signal); which flavor is the tracked one is not stated publicly (Portfolio assumed as primary). Formulas verified from the JFE paper (Proposition 9, eq. 32-33) and the BBT paper Appendix C. AS's handling of short positions (cash vs other) and the per-asset slot weighting are not stated - long-only, no leverage, flagged as assumptions. AS notes its summary stats use normal compounded returns; only the signals use averaged monthly returns.

### 46. Predicting Bond Returns (`baltussen_predicting_bond_returns`)

*Guido Baltussen, Martin Martens, Olaf Penninga*, family **macro**, AS status **tracked**, spec status **partial**.

- **Source:** Predicting Bond Returns: 70 Years of International Evidence (Financial Analysts Journal) (2022), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3631109
- **AS page:** https://allocatesmartly.com/predicting-us-treasury-returns/
- **Rebalance:** monthly; signal and trade at the close of the last trading day of the month
- **Universe:** risky ['IEF']; defensive []; canary ['S&P 500 price index', 'DBC']; cash cash
- **Signal:** Four signals in [-1,+1]: (1) YS = clip(z(10y yield - 13-week T-bill yield), -1, 1); (2) BT = +1 if R12(IEF) - R12(BIL) > 0 else -1; (3) EQ = clip(-z(R12(S&P 500 price index) - R12(BIL)), -1, 1); (4) CM = clip(-z(R12(DBC)), -1, 1). z(x_t) = (x_t - mean(x over previous 10 years)) / std(x over previous 10 years), using month-end observations. FINAL = (mean(YS, BT, EQ, CM) + 1) / 2 in [0,1].
- **Data needs:** month-end 10-year Treasury yield and 13-week T-bill yield (FRED DGS10/GS10, DTB3/TB3MS); monthly adjusted closes IEF and DBC (index proxies); S&P 500 price index (^GSPC) monthly; 3-month T-bill total return series; >= 10 years of history of each signal for z-scores
- **ETF-only start:** 2007 approx for trading (IEF 2002, DBC 2006-02 + 12m); z-scores need ~10y signal history, so index proxies are required (ETF-only start ~2017)
- **In plain English:** Scales exposure to intermediate Treasuries between 0% and 100% using four votes: a steep yield curve, positive bond trend, weak stocks, and weak commodities are all bullish for bonds. The rest is held in cash.
- **Rules:**
  1. At the close of the last trading day of each month compute the four component signals.
  2. Average them (pre-1970 AS ignores the commodity component and averages the remaining three).
  3. Allocate FINAL (0-100%) to IEF; the remainder sits in cash earning the 3-month T-bill return.
  4. Hold until the end of the following month.
- **Notes:** AS applies the ensemble only to US Treasuries (IEF) rather than the authors' international basket. Whether the 10-year z-score window is rolling (assumed) or expanding with a 10y minimum, and whether it includes the current observation, is not stated by AS (paper not accessed: SSRN 403). Bond trend signal is binary; a zero value is unspecified. AS suggests using it as an overlay to scale treasury exposure of other strategies. The related AS post 'Long-term returns for US Treasury funds are predictable' is a separate yield-vs-10y-return study, not this strategy.

### 47. Regime-Based Strategic Asset Allocation (`worldbank_regime_based_saa`)

*Eric Bouyé and Jérôme Teiletche (World Bank)*, family **static**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** Regime-based strategic asset allocation (exact venue/year not verified) (None), None
- **AS page:** none (no public AS post)
- **Rebalance:** unknown (likely periodic rebalance to fixed weights; AS convention would be month-end) (uncertain)
- **Universe:** risky []; defensive []; canary []; cash None
- **Signal:** UNKNOWN. No AS public post exists; the original paper could not be retrieved (web search budget exhausted, SSRN blocked). AS lists the strategy next to its static benchmark portfolios (All-Weather, Permanent Portfolio, Ivy, Golden Butterfly), suggesting a fixed-weight strategic mix derived from the paper's regime analysis.
- **Data needs:** original paper (portfolio weights and asset-class definitions)
- **ETF-only start:** unknown
- **In plain English:** A long-term (strategic) portfolio designed by World Bank Treasury researchers to hold up across different economic regimes. AllocateSmartly tracks it among its static portfolios, but its exact asset mix could not be confirmed here.
- **Rules:**
  1. Cannot be specified from available sources.
  2. To implement: obtain Bouyé & Teiletche's 'Regime-based strategic asset allocation' (World Bank Treasury authors), extract the recommended portfolio weights, map each asset class to AS-representative ETFs, and rebalance monthly at the last-trading-day close (AS default).
- **Notes:** Only facts confirmed: AS list-of-strategies entry 'Regime-Based Strategic Asset Allocation - Bouyé and Teiletche (World Bank)', placed among static/benchmark portfolios; AS average pairwise correlation 54.3% (Feb 2026 member note). No public AS blog post found (direct slug 404). Do not implement until the paper's weights and AS's ETF mapping are verified.

### 48. SPF Recession Probability (AS reinterpretation, incl. dynamic bond) (`sun_spf_recession_probability`)

*Yulong Sun (AS-modified)*, family **macro**, AS status **tracked**, spec status **full**.

- **Source:** Navigating Economic Downturns: Insights from Survey-Based Recession Indicators (2025), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5198217
- **AS page:** https://allocatesmartly.com/navigating-economic-downturns-with-survey-based-recession-indicators/
- **Rebalance:** signals quarterly at the close of the last trading day of Feb, May, Aug, Nov; portfolio rebalanced to target weights monthly at month-end close
- **Universe:** risky ['SPY']; defensive ['IEF']; canary []; cash cash
- **Signal:** Using Philadelphia Fed SPF mean responses. For survey quarter q: RP_now = mean(RECESS2, RECESS3, RECESS4)_q; RP_prev = mean(RECESS3, RECESS4, RECESS5)_{q-1} (same target quarters). RISK_ON = RP_now <= RP_prev. Rates: Y_now = mean(TBOND3, TBOND4, TBOND5)_q; Y_prev = mean(TBOND4, TBOND5, TBOND6)_{q-1}; BOND_ON = Y_now <= Y_prev (TBILL3..5 vs lagged TBILL4..6 for 1981Q3-1991Q4; before 1981Q3 BOND_ON always true).
- **Data needs:** Philadelphia Fed SPF Mean_RECESS_Level.xlsx (mean probability of real GNP/GDP decline; RECESS1 = survey quarter, RECESS2-5 = next 4 quarters); Philadelphia Fed SPF Mean_TBOND_Level.xlsx (10y Treasury rate, quarterly average; index 3-6 = next 1-4 quarters); Philadelphia Fed SPF Mean_TBILL_Level.xlsx (for 1981Q3-1991Q4); SPF release dates (to check the end-of-2nd-month availability assumption); monthly adjusted closes SPY, IEF; 13-week T-bill returns
- **ETF-only start:** 2003 approx (IEF 2002-07; RECESS data from 1968Q4)
- **In plain English:** Every quarter, checks whether professional forecasters have become more or less worried about a recession than last quarter for the same future quarters. If less worried it holds 60% stocks, otherwise it moves out of stocks; a similar check on expected 10-year yields decides whether the safe part sits in Treasuries or cash.
- **Rules:**
  1. Assume the SPF for quarter q is available by the end of the 2nd month of q (Q1 by end-Feb, Q2 by end-May, Q3 by end-Aug, Q4 by end-Nov).
  2. At the close of the last trading day of months 2, 5, 8, 11 compute RISK_ON and BOND_ON from the latest and previous surveys.
  3. Defensive sleeve = IEF if BOND_ON else cash (13-week T-bill).
  4. If RISK_ON: 60% SPY + 40% defensive sleeve; else 100% defensive sleeve.
  5. Keep the signal for the quarter; rebalance to the target mix at every month-end close.
- **Notes:** This is AS's reinterpretation, not Sun's original: Sun's first version compared RECESS2 vs lagged RECESS3; the revised paper uses RECESS4 vs lagged RECESS5, which AS considers likely overfit; Sun had no rule to exit long-duration bonds. AS averaged horizons 1-3 quarters ahead and added the TBOND rule (its own idea); the AS correlation table labels it 'SPF Recession Probability [Dynamic Bond]'. AS tightened execution to end of month 2 of the quarter. Real-world caveat: SPF release dates vary (Philadelphia Fed page lists the Q1-2026 release in March), so a live implementation should use actual release dates to avoid look-ahead. The 'anxious index' is the RECESS2 field. Sun's paper not accessed (SSRN 403).

### 49. Accelerating Dual Momentum (ADM) (`engineeredportfolio_accelerating_dual_momentum`)

*EngineeredPortfolio.com (author not named on the site)*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Accelerating Dual Momentum Investing (2018), https://engineeredportfolio.com/2018/05/02/accelerating-dual-momentum-investing/
- **AS page:** https://allocatesmartly.com/taa-strategy-accelerating-dual-momentum/
- **Rebalance:** monthly; signal at the close of the last trading day of the month, traded at that same close; hold to next month-end
- **Universe:** risky ['SPY', 'SCZ']; defensive ['TLT', 'TIP']; canary []; cash None
- **Signal:** SCORE_i = (R1_i + R3_i + R6_i)/3 with Rn_i = P_t/P_{t-n months} - 1 on month-end dividend-adjusted (total-return) closes, i in {SPY, SCZ}. Bond selector: R1 (1-month total return) of TLT vs TIP.
- **Data needs:** month-end dividend-adjusted closes for SPY, SCZ, TLT, TIP (daily data if testing alternate trading days); EFA / MSCI EAFE total return as SCZ stand-in before 1990
- **ETF-only start:** 2008 (SCZ launched Dec 2007; TIP 2003, TLT 2002)
- **In plain English:** Each month, compare US large caps with international small caps using an average of their 1-, 3- and 6-month returns and buy the stronger one if its score is positive. If neither equity market is rising, park everything in long Treasuries or TIPS, whichever did better last month. It is very aggressive because it holds one asset at a time.
- **Rules:**
  1. At the last trading day close of the month compute SCORE for SPY and SCZ (equal-weight average of 1-, 3- and 6-month total returns).
  2. If SCORE_SPY > SCORE_SCZ and SCORE_SPY > 0: hold 100% SPY.
  3. Else if SCORE_SCZ > SCORE_SPY and SCORE_SCZ > 0: hold 100% SCZ.
  4. Otherwise (the stronger equity score is <= 0; exact ties not addressed by source): hold 100% of whichever of TLT or TIP has the higher 1-month total return.
  5. Execute at the same close; hold the single position until the last trading day of the next month (the position is 100% of the portfolio every month).
- **Notes:** Verified against the author's article: core version uses VFINX/VINEX with VUSTX as the only fallback; the TLT-vs-TIP 1-month rule is the author's optional variant, which AS chose to include (AS says the baseline sent all defensive trades to long Treasuries). The author says to make the selection 'at the beginning of every month' (i.e., using prior month-end data) and mentions a Quantopian version using fixed day counts instead of calendar months; AS uses month-end calendar returns and trades at the month-end close. Tie-breaking is unspecified. AS flags strong timing luck (end-of-month execution was the best of all alternate trading days). AS also tracks an 'ADM [Dynamic Bond]' variant (from 11/2023) that applies the same absolute-momentum test to the defensive asset and goes to cash if it fails; exact form of that test not published. AS did not use the author's actively managed mutual fund data.

### 50. Composite Strategy (`movementcapital_composite`)

*Movement Capital (movement.capital now redirects to eversightwealth.com)*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** Movement Capital strategy page (Composite Strategy) (2019), https://movement.capital/strategy/
- **AS page:** https://allocatesmartly.com/movement-capitals-composite-strategy-balancing-strategy-and-asset-risk/
- **Rebalance:** monthly; signals and trades at the close of the last trading day of the month; entire portfolio rebalanced to target weights every month
- **Universe:** risky ['SPY', 'EFA']; defensive ['IEF', 'TIP']; canary ['SHV']; cash None
- **Signal:** Trend sleeve: MOM_i = (R3+R6+R9+R12+R15)/5, Rn = P_t/P_{t-n months} - 1 on month-end total-return closes, i in {SPY, EFA, SHV}. Macro sleeve (data as of the previous month, vintage values): sig_RS = YoY change of RRSFS < 0; sig_IP = YoY change of INDPRO < 0; sig_UE = UNRATE_{m-1} > average of UNRATE over the 12 months ending m-1; RECESSION = (sig_RS + sig_IP + sig_UE) >= 2.
- **Data needs:** month-end total-return closes for SPY, EFA, SHV, IEF, TIP; FRED/ALFRED RRSFS (real retail and food services sales), INDPRO, UNRATE - vintage (as available at the time) values, lagged 1 month
- **ETF-only start:** 2007 (SHV launched Jan 2007; TIP Dec 2003)
- **In plain English:** Half of the portfolio is a permanent 50/50 mix of US/international stocks and Treasuries/TIPS. The other half is tactical: one quarter follows stock momentum versus T-bills, and one quarter holds stocks unless at least two of three US economic indicators point to recession, in which case it moves to Treasuries.
- **Rules:**
  1. At the month-end close compute MOM for SPY, EFA and SHV.
  2. Trend-following sleeve (25%): winner = SPY or EFA with the higher MOM. If MOM_winner > MOM_SHV allocate 25% to the winner, else 25% to IEF.
  3. Macroeconomic sleeve (25%): evaluate the three recession indicators using the prior month's (1-month lagged) economic data. If fewer than 2 indicators signal recession allocate 12.5% SPY + 12.5% EFA, otherwise 25% IEF.
  4. Passive stock sleeve (25%): 12.5% SPY + 12.5% EFA, always.
  5. Passive bond sleeve (25%): 12.5% IEF + 12.5% TIP, always (before 1973 the TIP half is held in IEF).
  6. Sum sleeve weights by ticker, trade at the same close, hold to next month-end; rebalance everything to target monthly even if signals are unchanged.
- **Notes:** Simplified AS version agreed with the author. Original: Vanguard funds (VTI, VXUS, VGIT, VTIP), weekly rebalancing with a 30-day position freeze after trades (wash-sale avoidance) and exposures scaled to each client's horizon/risk tolerance; AS uses monthly month-end rebalancing. AS states the macro sleeve uses the same three indicators as Growth-Trend Timing; the exact per-indicator recession tests above are inferred from AS's GTT posts (RRSFS/INDPRO YoY<0, UNRATE above its 12-month average) and are not confirmed by Movement Capital's own page (now offline/redirected). Since May 2023 AS uses vintage economic data for this strategy (3.3% of historical months changed). Tie handling in the SPY/EFA comparison unspecified. Family is a composite (25% dual momentum, 25% macro, 50% static).

### 51. Active Combined Asset (ACA) - Daily (`stoken_active_combined_asset`)

*Dick Stoken*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** Survival of the Fittest for Investors: Using Darwin's Laws of Evolution to Build a Winning Portfolio (book) (2012), https://www.amazon.com/dp/B0076VLJ9W
- **AS page:** https://allocatesmartly.com/stokens-active-combined-asset-strategy/
- **Rebalance:** daily signal check at the close, trade at that close on a signal change; whole portfolio rebalanced to 1/3 per slice on any signal change and on the last trading day of each calendar year
- **Universe:** risky ['SPY', 'GLD', 'VNQ']; defensive ['IEF', 'TLT']; canary []; cash None
- **Signal:** Per slice: UPPER_n(t) = max(close_{t-1}..close_{t-n}), LOWER_n(t) = min(close_{t-1}..close_{t-n}) (previous n trading days, excluding today). SPY/IEF: n_up=126, n_low=252. GLD/TLT: n_up=252, n_low=126. VNQ/IEF: n_up=126, n_low=252. Switch to risk when close_t > UPPER; switch to defensive when close_t < LOWER; otherwise keep current state. SPY channels use the unadjusted (cash) price; VNQ channels use the dividend-adjusted price; GLD pays no dividend.
- **Data needs:** daily closes for SPY (unadjusted for signals, adjusted for returns), GLD, VNQ (dividend-adjusted), IEF and TLT (total return)
- **ETF-only start:** 2004-11 (GLD; VNQ Sep 2004; IEF/TLT Jul 2002)
- **In plain English:** The portfolio is split into three pieces: stocks vs Treasuries, gold vs long Treasuries, and real estate vs Treasuries. Each piece buys the risk asset after a breakout to a new multi-month high and retreats to Treasuries after a breakdown to a multi-month low, with stocks and real estate easier to enter than gold.
- **Rules:**
  1. Split the portfolio into three equal slices (1/3 each): SPY vs IEF, GLD vs TLT, VNQ vs IEF.
  2. Initial state (AS, matching Stoken): all three slices start long their risk asset (SPY, GLD, VNQ) on day 1.
  3. Each trading day at the close, for each slice holding its defensive asset: if the risk asset's close is above its upper channel, switch the slice to the risk asset at that close.
  4. For each slice holding its risk asset: if the risk asset's close is below its lower channel, switch the slice to its defensive asset at that close.
  5. Otherwise leave the slice unchanged (state is persistent between signals).
  6. Whenever any slice changes, and on the last trading day of each calendar year, rebalance the whole portfolio back to 1/3 per slice; otherwise let weights drift.
- **Notes:** Channel table read from the AS post image (20161019.03.png). AS deviations from Stoken: IEF in place of a 5-year Treasury, trading-day lookbacks, daily data only for real estate, and rebalancing on every signal change plus year-end (Stoken: annual only). The strategy trades rarely (under ~3 trades per year). AS separately tracks a month-end version (see stoken_active_combined_asset_monthly) and, from 11/2023, '[Dynamic Bond]' variants of both that apply the channel logic to the defensive asset as well and hold cash if it fails (exact rule not public). Stoken's book is the original source; the book itself was not consulted here.

### 52. Active Combined Asset (ACA) - Monthly (`stoken_active_combined_asset_monthly`)

*Dick Stoken (month-end conversion by AllocateSmartly)*, family **trend-following**, AS status **tracked**, spec status **full**.

- **Source:** Survival of the Fittest for Investors: Using Darwin's Laws of Evolution to Build a Winning Portfolio (book) (2012), https://www.amazon.com/dp/B0076VLJ9W
- **AS page:** https://allocatesmartly.com/stokens-active-combined-asset-strategy/
- **Rebalance:** monthly; signals and trades only at the close of the last trading day of the month; full rebalance to 1/3 per slice on any signal change and at calendar year-end
- **Universe:** risky ['SPY', 'GLD', 'VNQ']; defensive ['IEF', 'TLT']; canary []; cash None
- **Signal:** Same as the daily ACA but using month-end closes: UPPER = max of the previous k month-end closes, LOWER = min of the previous k month-end closes (excluding the current month-end). SPY/IEF: k_up=6, k_low=12. GLD/TLT: k_up=12, k_low=6. VNQ/IEF: k_up=6, k_low=12.
- **Data needs:** month-end closes for SPY, GLD, VNQ, IEF, TLT (index proxies pre-ETF)
- **ETF-only start:** 2004-11 (GLD; VNQ Sep 2004)
- **In plain English:** A once-a-month version of Stoken's three-slice breakout strategy: each slice owns stocks, gold or real estate after a 6- or 12-month high and switches to Treasuries after a 6- or 12-month low.
- **Rules:**
  1. Three 1/3 slices: SPY vs IEF, GLD vs TLT, VNQ vs IEF; start with all slices in their risk asset.
  2. At each month-end close, a slice in defense switches to its risk asset if the risk asset's month-end close exceeds its upper channel; a slice in risk switches to defense if the close is below its lower channel; otherwise unchanged.
  3. Trades execute at the month-end close; on any change, and at the last trading day of the calendar year, rebalance the whole portfolio to 1/3 per slice.
- **Notes:** AS replaced the 252/126 trading-day lookbacks with 12/6 month-end lookbacks and otherwise kept all rules (AS post 'Extended Backtest' section; member announcement 07/2017 says AS tracks it as a separate strategy). AS lists 'Stoken's ACA - Monthly' separately in its strategy-asset matrix and transaction-cost table. Whether the channel excludes the current month-end is inferred from the daily definition ('excluding today'). A '[Dynamic Bond]' variant also exists on AS.

### 53. Three Way Model (`neddavis_three_way_model`)

*Ned Davis (Ned Davis Research)*, family **other**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** Not identified in this session (possibly from Ned Davis's book 'Being Right or Making Money' or NDR research - unverified) (None), None
- **AS page:** none (no public AS post)
- **Rebalance:** unknown (no public AS description); AS includes it among its monthly-tracked strategies
- **Universe:** risky ['SPY']; defensive ['TLT', 'GLD']; canary []; cash cash
- **Signal:** NOT PUBLICLY SPECIFIED. No AllocateSmartly blog post describes the rules, and the original source could not be located (web search budget exhausted). Do not implement without the original source.
- **Data needs:** daily/month-end adjusted closes for SPY, TLT, GLD; T-bill rate for cash; possibly NDR proprietary or non-price indicators (unknown)
- **ETF-only start:** 2004-11 (GLD)
- **In plain English:** A Ned Davis model that, as tracked by AllocateSmartly, moves among US stocks, long-term Treasuries, gold and cash. Its exact rules are not public in any source available here.
- **Rules:**
  1. Rules unknown - the only verifiable facts are listed below.
  2. Holdings are drawn from US stocks (SPY), long-term Treasuries (TLT), gold (GLD) and cash (AS 2019 public strategy-asset matrix).
  3. AS's 2019 transaction-cost study shows ~0.30%/yr drag at 0.10% per trade, i.e. low turnover (roughly 1.5 full portfolio switches per year if positions were all-or-nothing - inference).
- **Notes:** No dedicated AS post exists; the strategy appears only by name ('Davis' Three Way Model') in AS performance tables, the trading-cost table (0.30%/yr) and the 2019 strategy-asset matrix (dots for GLD, SPY, TLT, Cash - read from the matrix image). The original Ned Davis/NDR source was not found: WebSearch quota was exhausted before searching, and no URL was known to fetch. NDR's well-known published models typically combine trend/momentum, sentiment and monetary (interest-rate/Fed) indicators, so non-price inputs are possible but unconfirmed; the name may refer to three asset classes (stocks/bonds/gold) or three indicator groups - unknown. This entry is a placeholder and must be completed from the original source before implementation.

### 54. Efficiente Index (`jpm_efficiente_index`)

*J.P. Morgan*, family **risk-parity**, AS status **tracked**, spec status **full**.

- **Source:** J.P. Morgan Efficiente Index methodology (index brochure/rulebook linked by AS; link now returns 404) (None), https://www.jpmorgan.com/jpmpdf/1320639547153.pdf
- **AS page:** https://allocatesmartly.com/testing-efficiente-index/
- **Rebalance:** monthly; optimise at the close of the last trading day of the month, trade at that close; full rebalance monthly regardless of changes
- **Universe:** risky ['SPY', 'IWM', 'EFA', 'EEM', 'VNQ', 'DBC', 'GLD', 'HYG', 'EMB', 'LQD']; defensive ['TLT', 'TIP']; canary []; cash cash
- **Signal:** Using the trailing 126 trading days (6 months) of daily total returns: mu_i = expected return estimate from that window (e.g. mean daily return annualised; AS does not state the exact estimator), Sigma = sample covariance of daily returns (annualised). Solve max_w w'mu subject to sqrt(w'Sigma w) <= 10% annualised, w_i >= 0, sum(w) = 1 (cash included as an asset), asset caps and group caps.
- **Data needs:** daily dividend-adjusted closes for SPY, IWM, EFA, EEM, VNQ, DBC, GLD, TLT, LQD, HYG, EMB, TIP; daily 3-month T-bill rate for the cash asset; a constrained quadratic/convex optimiser
- **ETF-only start:** 2008 (EMB Dec 2007; HYG Apr 2007; DBC Feb 2006)
- **In plain English:** Every month, a portfolio optimiser picks the mix of 12 asset-class ETFs and cash that would have earned the most over the last six months while keeping volatility under 10%, subject to caps on each asset and each asset group. Because it uses such a short window, it behaves like a momentum strategy that also rewards low volatility and low correlation.
- **Rules:**
  1. At each month-end close collect 126 trading days of daily total returns for the 12 ETFs plus cash (T-bill).
  2. Solve the long-only, unlevered mean-variance problem: maximise expected return subject to annualised realised portfolio volatility <= 10% and the caps below.
  3. Asset caps: SPY 20%, IWM 10%, EFA 20% (group US/developed equities <= 50%); TLT 20%, LQD 20%, HYG 20% (group US bonds <= 50%); EEM 20%, EMB 20% (group emerging markets <= 25%); VNQ 20%, DBC 10%, GLD 10% (group real assets <= 25%); TIP 50%, cash 50% (group TIPS + cash <= 50%).
  4. AS deviation: drop any weight below 2% and redistribute it proportionally across the remaining holdings (AS ignores the original rule that weights are integer multiples of 5%).
  5. Trade at the same close and hold until the next month-end.
- **Notes:** Constraint table transcribed from the AS post image (20180130.04.png). AS says published versions of the index differ slightly and the description is light on detail; AS 'captured the best mix'. Not specified by AS: the exact expected-return estimator, the covariance estimator, and what happens if no portfolio meets the 10% volatility cap (possible because cash is capped at 50%); JPM index documents reportedly handle infeasibility by raising the vol target stepwise - unverified here. The JPM PDF linked by AS now returns 404; the rulebook could not be retrieved. JPM's own ETF-based versions (e.g. the one behind ETF EFFE) may use different ETFs and a different vol target (unverified). Goldman Sachs' Momentum Builder Multi-Asset index is described by AS as nearly identical.

### 55. Defense First (`carlson_defense_first`)

*Thomas Carlson*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Defense First: A Multi-Asset Tactical Model for Adaptive Downside Protection (2025), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5334772
- **AS page:** https://allocatesmartly.com/carlsons-defense-first/
- **Rebalance:** monthly; signals at the close of the last trading day of the month, traded at that close; full rebalance monthly
- **Universe:** risky ['SPY']; defensive ['TLT', 'GLD', 'PDBC', 'UUP']; canary ['BIL']; cash None
- **Signal:** MOM_i = (R1+R3+R6+R12)/4 with Rn = P_t/P_{t-n months} - 1 on month-end dividend-adjusted closes, for i in {TLT, GLD, PDBC, UUP, BIL}. BIL momentum is the hurdle only.
- **Data needs:** month-end dividend-adjusted closes for TLT, GLD, PDBC/DBC, UUP, BIL, SPY; pre-ETF: long Treasury TR, gold spot, commodity index TR, US Dollar Index (plus collateral yield for UUP-like returns), T-bill TR
- **ETF-only start:** 2007 (UUP Feb 2007, BIL May 2007; DBC 2006, PDBC 2014)
- **In plain English:** The strategy ranks four defensive assets (long Treasuries, gold, commodities, US dollar) by recent momentum and gives them 40/30/20/10% of the portfolio. Any defensive asset that is doing worse than T-bills hands its share to US stocks, so stocks are owned mainly when defensive assets are weak.
- **Rules:**
  1. At the month-end close compute MOM for TLT, GLD, PDBC, UUP and BIL.
  2. Rank the four defensive assets by MOM from highest to lowest and assign slot weights 40%, 30%, 20%, 10% by rank.
  3. For each slot: if the asset's MOM < MOM_BIL, give that slot's weight to SPY instead; otherwise hold the asset at the slot weight.
  4. SPY weight = sum of all redirected slots (0%-100%); SPY's own momentum is not checked.
  5. Trade at the same close; hold until the next month-end; rebalance monthly even if unchanged.
- **Notes:** Rules from AS; the SSRN paper returned HTTP 403 and could not be checked directly. Ties in ranking and the case MOM == MOM_BIL are not addressed (AS wording 'less than' implies equality keeps the defensive asset). AS suggests (but did not implement) holding cash instead of UUP because UUP contributed almost nothing after costs, and considering a cap on stock exposure when stock momentum is negative; neither is part of the tracked rules. AS reports that results were benchmark-like after ~1980 with lower drawdowns and low correlation to other TAA strategies.

### 56. Hybrid Asset Allocation 60/40 (`nlx_haa_60_40`)

*NLX Finance (variant of Keller & Keuning's HAA-Simple)*, family **trend-following**, AS status **tracked**, spec status **partial**.

- **Source:** NLX Finance HAA 60/40 variant (original publication not located); base strategy: Keller & Keuning, 'Dual and Canary Momentum with Rising Yields/Inflation: Hybrid Asset Allocation (HAA)' (2024), None
- **AS page:** https://allocatesmartly.com/nlx-finances-hybrid-asset-allocation-60-40/
- **Rebalance:** monthly; signals and trades at the close of the last trading day of the month; rebalanced monthly even without a signal change
- **Universe:** risky ['SPY']; defensive ['IEF']; canary ['TIP']; cash cash
- **Signal:** MOM_i = (R1+R3+R6+R12)/4 (unweighted), Rn = P_t/P_{t-n months} - 1 on month-end dividend-adjusted closes, for TIP, SPY, IEF and BIL (BIL = cash-momentum proxy).
- **Data needs:** month-end dividend-adjusted closes for SPY, TIP, IEF; T-bill total return (BIL or 3-month T-bill) for the cash hurdle and cash return
- **ETF-only start:** 2003-12 (TIP; BIL Jun 2007 only if the ETF is used for the hurdle)
- **In plain English:** When both TIPS and US stocks have positive average momentum, hold a 60/40 mix of stocks and intermediate Treasuries; otherwise hold intermediate Treasuries if they beat T-bills, or cash if not. It is a calmer version of Keller's HAA-Simple, which holds 100% stocks when risk is on.
- **Rules:**
  1. At the month-end close compute MOM for TIP and SPY.
  2. If MOM_TIP > 0 and MOM_SPY > 0 (risk on): hold 60% SPY + 40% IEF.
  3. Otherwise (either is negative): if MOM_IEF > MOM_BIL hold 100% IEF, else 100% cash.
  4. Trade at the same close; hold to next month-end; rebalance to target weights monthly.
- **Notes:** AS gives no rules beyond 'identical to HAA-Simple except 60% SPY / 40% IEF when risk on'; the full rule set above is taken from AS's HAA-Simple post. NLX Finance's own publication could not be located (no link in the AS post; nlxfinance.com does not resolve; web search unavailable). The treatment of exactly-zero momentum is unspecified. AS ran an adversarial test replacing TIPS with IEF before the TIP ETF; results were in line with the original test.

### 57. Dividend & Growth Allocation (DGA) (`choi_dividend_growth_allocation`)

*Paul Choi*, family **macro**, AS status **tracked**, spec status **full**.

- **Source:** Balance Between Growth and Dividend: Dividend & Growth Allocation (2023), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4633601
- **AS page:** https://allocatesmartly.com/chois-dividend-growth-allocation/
- **Rebalance:** monthly; signals and trades at the close of the last trading day of the month; hold to next month-end
- **Universe:** risky ['QQQ', 'SCHD']; defensive ['TLT', 'PDBC']; canary ['TIP']; cash cash
- **Signal:** Risk-on requires all three: (C1) TIP_t > SMA12(TIP month-end closes); (C2) DY_t = D12_{m-1} / SPX_t >= 1.6%, where D12 = trailing-12-month S&P 500 dividends per share as of the previous month (1-month lag) and SPX_t = current S&P 500 price index; (C3) for none of the monthly observations 7 through 15 months before t is the curve inverted, inverted meaning (10y UST yield - 3m UST yield) < -0.50 pp. Risk-on momentum: MOM_i = (R1+R3+R6+R9+R12)/5 on month-end closes. Risk-off momentum: MOM_i = P_t / SMA6(month-end closes) - 1.
- **Data needs:** month-end dividend-adjusted closes for QQQ, SCHD, TIP, TLT, PDBC/DBC, BIL; S&P 500 price index and trailing-12-month dividends per share (quarterly S&P data or Shiller dataset), dividend lagged 1 month; FRED T10Y3MM from June 2019 onward; before June 2019 AS computes the 10y-3m spread from underlying yield series (exact series not stated, e.g. GS10/TB3MS)
- **ETF-only start:** 2011-11 (SCHD launched Oct 2011)
- **In plain English:** The strategy is fully invested in either Nasdaq-100 or high-dividend US stocks, whichever has stronger momentum, but only when TIPS are in an uptrend, the S&P 500 dividend yield is at least 1.6%, and the yield curve has not been deeply inverted 7-15 months earlier. Otherwise it holds the strongest of T-bills, long Treasuries and commodities, or cash if none is trending up.
- **Rules:**
  1. At the month-end close evaluate C1, C2 and C3; risk on only if all three pass.
  2. Risk on: compute MOM (average of 1, 3, 6, 9, 12-month % returns) for QQQ and SCHD; hold 100% of the higher one.
  3. Risk off: compute MOM = close / 6-month SMA of month-end closes - 1 for BIL, TLT and PDBC; if the highest MOM is positive hold 100% of that asset, otherwise hold cash.
  4. Any allocation to BIL is held as cash (AS convention).
  5. Trade at the same close; hold until the last trading day of the next month.
- **Notes:** AS revised its post on 01/10/24 after the author revised the paper on SSRN (01/03/24) to define inversion as the 10y yield at least 0.5% below the 3m yield. AS found the yield-curve rule fragile: FRED's T10Y3MM methodology changed in June 2019, so AS self-computes the spread before that date and uses T10Y3MM afterwards. AS's monthly TIP SMA presumably uses month-end closes (price vs adjusted not stated). AS criticises the fixed 1.6% dividend-yield threshold as fit to post-1990s history and shows an adversarial version (IEF instead of simulated TIPS pre-ETF, no dividend-yield check, from 1970). Tie handling unspecified. SSRN page returned 403, so the paper was not checked directly.

### 58. Paired Switching Strategy (`glenn_paired_switching`)

*Lewis Glenn (per AllocateSmartly); the paired-switching concept was published by A. Maewal & J. R. Bock (2011) - relationship unverified*, family **momentum-rotation**, AS status **tracked**, spec status **partial**.

- **Source:** Paired-Switching for Tactical Portfolio Allocation (Maewal & Bock, SSRN working paper) - attribution of AS's 'Glenn' version unverified (2011), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1917044
- **AS page:** none (no public AS post)
- **Rebalance:** quarterly at the last trading day of each calendar quarter (uncertain - see notes; AS may evaluate monthly)
- **Universe:** risky ['SPY']; defensive ['TLT']; canary []; cash None
- **Signal:** R_i = P_t / P_{t-3 months} - 1 on dividend-adjusted closes for i in {SPY, TLT} (lookback uncertain); hold argmax R_i. Relative momentum only - no absolute filter.
- **Data needs:** month-end dividend-adjusted closes for SPY and TLT (index proxies pre-2002)
- **ETF-only start:** 2002-07 (TLT)
- **In plain English:** Always fully invested in either US stocks or long-term Treasuries, whichever has performed better recently. Because the two usually move in opposite directions, the switch tends to catch whichever is in favour.
- **Rules:**
  1. At each rebalance date compute the trailing (3-month, uncertain) total return of SPY and TLT.
  2. Hold 100% of whichever has the higher return (ties unspecified); never cash.
  3. Hold until the next rebalance date.
- **Notes:** No dedicated public AS post. Confirmed from AS public material: the pair is SPY and TLT (AS 2019 strategy-asset matrix), the strategy uses only relative momentum with no absolute filter (AS 'Dynamic Bond' post, 11/2023), and its trading-cost drag was 0.65%/yr (2019). The lookback (3 months / prior quarter) and quarterly switching come from recollection of the Maewal & Bock paper and could not be verified (SSRN returned 403; web search quota exhausted). Inference: 0.65%/yr at 0.1% per trade implies about 3.25 full switches per year, which would require switching in ~80% of quarters under strict quarterly rebalancing; that is more consistent with a monthly check of a multi-month lookback, so AS's implementation frequency is genuinely uncertain. AS also lists Lewis Glenn as author of Quint Switching Filtered (SSRN 3129098), so 'Glenn' may be a later author of the paired-switching approach rather than the 2011 authors.

### 59. Quint Switching Filtered (QSF) (`glenn_quint_switching_filtered`)

*Lewis Glenn*, family **momentum-rotation**, AS status **tracked**, spec status **full**.

- **Source:** Quint Switching Filtered (Lewis Glenn, SSRN working paper; exact title not verified) (2018), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3129098
- **AS page:** https://allocatesmartly.com/quint-switching-filtered-not-as-simple-as-it-appears-to-be/
- **Rebalance:** monthly; signals and trades at the close of the last trading day of the month
- **Universe:** risky ['SPY', 'QQQ', 'EFA', 'EEM', 'TLT']; defensive ['IEF']; canary []; cash None
- **Signal:** R3_i = P_t / P_{t-3 months} - 1 on month-end total-return closes for i in {SPY, QQQ, EFA, EEM, TLT}.
- **Data needs:** month-end dividend-adjusted closes for SPY, QQQ, EFA, EEM, TLT, IEF (daily if modelling alternate trading days)
- **ETF-only start:** 2003-04 (EEM)
- **In plain English:** Look at five markets (US large caps, Nasdaq-100, developed international, emerging markets and long Treasuries). Only if all five have risen over the past three months, buy the strongest one; otherwise sit entirely in intermediate Treasuries, which happens about three months out of four.
- **Rules:**
  1. At the month-end close compute 3-month total return for SPY, QQQ, EFA, EEM and TLT.
  2. If any of the five has R3 < 0: hold 100% IEF.
  3. If all five have R3 > 0: hold 100% of the asset with the highest R3 (ties unspecified; exactly-zero returns unspecified).
  4. Trade at the same close; hold until the last trading day of the next month.
- **Notes:** Rules from AS; the SSRN paper (abstract 3129098) returned 403 and was not checked directly. 'Filtered' refers to the all-positive requirement; an unfiltered 'Quint Switching' presumably holds the top 3-month performer of the five unconditionally (inferred from the name, unverified). The requested link to Scott's Investments' 'Quint Switching' could not be checked (scottsinvestments.com is now a parked domain; web search unavailable). AS notes TLT acts mainly as a spoiler (held ~2.4% of months), very high exposure to rising rates and extreme timing luck (alternate trading days CAGR 8.5%-14.8%). AS also tracks a '[Dynamic Bond]' variant (from 11/2023) that applies the momentum rule to IEF and goes to cash if it fails (presumably IEF R3 > 0 - exact form not published).

### 60. Global Growth Cycle (GGC) (`link_global_growth_cycle`)

*Grzegorz Link*, family **macro**, AS status **tracked**, spec status **full**.

- **Source:** Global Growth Cycle (grzegorz.link) (2021), https://grzegorz.link/growth
- **AS page:** https://allocatesmartly.com/using-oecd-composite-leading-indicator-data-to-time-the-market/
- **Rebalance:** monthly on the 15th calendar day (or the next trading day) at the close; hold until the next 15th
- **Universe:** risky ['SPY']; defensive []; canary []; cash cash
- **Signal:** DI = (number of countries whose CLI rose month-over-month) / (number of countries with data), using each country's OECD Composite Leading Indicator for the most recent month available (the month ending before the trade month, i.e. CLI_{m-1} vs CLI_{m-2} when trading in month m). Individual countries only; regional aggregates (EA19, G-7, OECD, OECDE, etc.) excluded. Earliest-vintage CLI values. Risk on if DI >= 0.5.
- **Data needs:** OECD Composite Leading Indicator by country, monthly, with historical vintages (OECD vintages unavailable before 2001); daily dividend-adjusted SPY closes; 3-month T-bill rate for cash
- **ETF-only start:** 1993 (SPY)
- **In plain English:** Each month, check what share of countries have a rising OECD leading economic indicator. If at least half are rising, own the S&P 500; otherwise hold cash.
- **Rules:**
  1. On the 15th calendar day of each month (or the first trading day after), compute DI from the previous month's CLI data for all individual countries available at that time.
  2. If DI >= 0.50, hold 100% SPY at the close; otherwise hold 100% cash (3-month T-bill return).
  3. Hold until the 15th of the next month.
- **Notes:** AS's first test (12/2021) replicated the author's revised-data backtest from 1956 (lookahead bias, since each new CLI data point revises the entire history) and then showed a vintage-based test; AS official results use the earliest vintage. Vintaging is imperfect: OECD vintages are missing before 2001 and constituent-country changes before 12/2021 cannot be vintaged (survivorship). The 2023 OECD overhaul cut the CLI to 17 countries; AS's 08/2023 re-test found similar long-run results (agreement ~83% of months). The author's page uses price-only S&P 500 with no costs, cash return or dividends, shifts each DI value 15 days, and presents an alternate version that switches to a 50-day moving-average rule when DI < 0.5 (AS did not replicate it). Exact handling of countries with missing data in a month is not specified.

### 61. Global Growth Cycle Enhanced (GGC Enhanced) (`link_global_growth_cycle_enhanced`)

*Grzegorz Link*, family **macro**, AS status **tracked**, spec status **full**.

- **Source:** Global Growth Cycle enhanced with momentum (grzegorz.link) (2025), https://grzegorz.link/momentum-enhanced
- **AS page:** https://allocatesmartly.com/using-the-oecd-composite-leading-indicator-momentum-to-time-the-market/
- **Rebalance:** monthly, last trading day close (AS 'Monthly' version); AS also tracks a 'Mid-Month' version that trades on the 15th calendar day
- **Universe:** risky ['SPY', 'IEFA']; defensive ['AGG']; canary []; cash cash
- **Signal:** DI as in GGC (share of countries whose OECD CLI rose month-over-month, using the previous month's CLI data - 1-month reporting lag - earliest vintage). Risk on if DI > 0.5 (strict). R12_i = P_t / P_{t-12 months} - 1 on month-end dividend-adjusted closes for SPY, IEFA, AGG, BIL.
- **Data needs:** OECD CLI by country with vintages, 1-month reporting lag; month-end dividend-adjusted closes for SPY, IEFA (EFA pre-2012), AGG, BIL (or 3-month T-bill total return)
- **ETF-only start:** 2003-09 (AGG; EFA 2001; IEFA itself Oct 2012; BIL 2007 only if the ETF is used for the hurdle)
- **In plain English:** The same global leading-indicator test decides between risk on and risk off. When risk is on, it holds whichever of US or international stocks has the better 12-month return; when risk is off, it holds US aggregate bonds if they beat T-bills over 12 months, otherwise cash.
- **Rules:**
  1. At the close on the last trading day of month t, take OECD CLI values for month t-1 (the most recent month, published in the first 1-2 weeks of month t) and month t-2 for every individual country (exclude regional aggregates such as EA19, G-7, OECD, OECDE).
  2. Diffusion Index = share of those countries whose CLI rose month-over-month.
  3. If DI > 0.5 (strictly greater) the strategy is risk on: compare 12-month returns of SPY and IEFA and put 100% in the higher one.
  4. If DI <= 0.5 the strategy is risk off: if AGG's 12-month return exceeds BIL's, put 100% in AGG; otherwise 100% cash (BIL).
  5. Trade at that close and hold until the last trading day of the following month.
  6. Mid-Month variant: on the 15th calendar day (or next trading day) compute the DI from the CLI month just released (the previous month) and apply the same rules; hold until the next 15th.
- **Notes:** Rules and author flowchart from the AS post (12/2025, flowchart image 20251128.06.png). The author's article (fetched) uses VXUS for international stocks and a 12-month lookback in backtests; its text describes the risk-off branch as IEF vs BIL while the flowchart shown by AS says 'Agg Bonds > T-Bills' - AS uses AGG. The > vs >= threshold difference was unintentional by the author; it matters only when an even number of countries can give exactly 0.5 (currently 17 countries). AS did not separately quantify the vintage-data impact for this version. | Additional detail: Author's own version: risk-on SPY vs VXUS, risk-off IEF vs BIL (author says he preferred AGG but his data source lacked it), lookback 12 months (found best by author, who flags possible overfitting); author's page does not clearly state the risk-off lookback or the exact execution day. AS uses AGG vs BIL and SPY vs IEFA. The author notes 39 countries before 2022 and 17 since (odd counts, so > vs >= currently identical). AS vintages each country's data points but cannot vintage historical changes in the country list before 12/2021, so some lookahead remains. Whether 12-month returns are dividend-adjusted is not stated (AS normally uses total return).

### 62. Momentum Based Balancing (`virag_momentum_based_balancing`)

*Mark Virag*, family **momentum-rotation**, AS status **tracked**, spec status **partial**.

- **Source:** Momentum Based Balancing for the Diversified Portfolio (NAAIM Wagner Award paper) (2014), None
- **AS page:** https://allocatesmartly.com/mark-virags-momentum-based-balancing-relative-momentum-taken-to-the-extreme/
- **Rebalance:** monthly; signal and execution at the close of the last trading day of the month; all positions reset to target weights every month
- **Universe:** risky ['SPY', 'IWM', 'XLB', 'EFA', 'EEM', 'VNQ', 'IEF', 'TLT', 'TIP']; defensive []; canary []; cash cash
- **Signal:** R3_i = P_t / P_{t-3m} - 1 on month-end dividend-adjusted closes (AS convention) for the 9 ETFs; R3_cash = 0 by definition (cash is treated as a 10th asset with zero momentum). Baseline B = second-lowest of the 10 R3 values. Score S_i = max(R3_i - B, 0). Weight w_i = S_i / sum_j S_j.
- **Data needs:** month-end dividend-adjusted closes for SPY, IWM, XLB, EFA (IEFA), EEM (IEMG), VNQ, IEF, TLT, TIP; 3-month T-bill rate (FRED DTB3/TB3MS) for cash return; commodity index series to proxy XLB before ~1989 if extending pre-ETF
- **ETF-only start:** 2005 (VNQ launched Sep 2004; TIP Dec 2003; EEM Apr 2003)
- **In plain English:** Each month the strategy looks at how nine stock, real-estate and bond ETFs plus cash did over the last three months. It shifts every return up so the second-worst asset sits at zero, drops the worst, and then allocates money in proportion to each asset's shifted return, so recent winners get the biggest slices.
- **Rules:**
  1. At the close on the last trading day of month t, compute the 3-month total return of SPY, IWM, XLB, EFA, EEM, VNQ, IEF, TLT, TIP; assign cash a 3-month return of exactly 0.
  2. Sort the 10 values and take the second-lowest value as baseline B (B is usually negative).
  3. For every asset (including cash) compute S_i = R3_i - B; any S_i below zero (i.e. the single lowest asset) is set to 0. The second-lowest asset therefore also ends with 0.
  4. Sum all S_i; weight of each asset (including cash) = S_i / sum S.
  5. Edge case not specified by AS: if sum S = 0 (all 10 returns identical) allocate 100% to cash (implementer choice). Ties at the bottom simply produce several zero weights.
  6. Execute all trades at the same close; hold until the last trading day of the next month, then recompute and rebalance to new weights (full monthly rebalance even if ranks unchanged).
  7. Cash portion earns the 3-month T-bill rate (AS 'cash' convention), even though its signal return is fixed at 0.
- **Notes:** AS backtest from 1973. AS describes the paper as a 2014 NAAIM Wagner Award winner; the NAAIM award page lists different 2014 top-3 winners, so the award status could not be confirmed and the paper itself was not retrieved (rules here come from AS's post, which gives a worked numeric example that matches the formula above). Price vs total return for the 3-month return is not stated explicitly; AS generally uses dividend-adjusted data with a 2-day dividend lag. Because rank-proportional weighting concentrates in whichever group (risk-on or bonds) is leading, AS also showed an Optimum-3-style variant, but that is not the tracked version.

### 63. Excess Earnings Yield Dynamic - Valuation Only (`elm_eeyd_valuation_only`)

*James White and Victor Haghani (Elm Wealth)*, family **valuation**, AS status **tracked**, spec status **partial**.

- **Source:** Man Doth Not Invest by Earnings Yield Alone (2022), https://elmwealth.com/man-doth-not-invest-by-earnings-yield-alone/
- **AS page:** https://allocatesmartly.com/excess-earnings-yield-dynamic-valuation-strategy/
- **Rebalance:** monthly; signal and execution at the close of the last trading day of the month; rebalance to target every month even if unchanged
- **Universe:** risky ['SPY']; defensive ['TIP']; canary []; cash None
- **Signal:** EY_t = 1 / CAPE_q where CAPE_q is Shiller's CAPE for the most recent calendar quarter-end month that is at least 3 months before t; RY_t = 10-year TIPS real yield at t (decimal); EEY_t = EY_t - RY_t; w_SPY = clip(EEY_t / (gamma * sigma^2), 0, 1) with gamma = 2 and sigma = 0.18, i.e. w_SPY = clip(EEY_t / 0.0648, 0, 1); w_TIP = 1 - w_SPY.
- **Data needs:** Shiller monthly CAPE (Shiller online data, ie_data.xls); 10-year TIPS real yield: FRED DFII10 (daily, from 2003); 1997-2002 needs another source (e.g. Fed H.15 historical / Gurkaynak-Sack-Wright real curve) (uncertain which AS uses); simulated pre-1997; month-end dividend-adjusted closes for SPY and TIP; pre-ETF: S&P 500 TR index and a simulated TIPS return series
- **ETF-only start:** 2004 (TIP launched Dec 2003)
- **In plain English:** Compares the long-run real return you can expect from US stocks (1/CAPE) with the guaranteed real yield on 10-year TIPS. The bigger the stock advantage, the more goes into stocks, using a textbook formula that scales the advantage by stock risk; the rest sits in TIPS.
- **Rules:**
  1. On the last trading day of month t, look up Shiller CAPE (10-year inflation-adjusted earnings) for the latest quarter-end month (Mar/Jun/Sep/Dec) that is at least 3 months earlier than t (AS's own anti-lookahead lag; e.g. at end-July use March CAPE, at end-September use June CAPE).
  2. Earnings yield EY = 1 / CAPE.
  3. Take the current 10-year TIPS real yield RY (month-end value; decimal).
  4. Excess earnings yield EEY = EY - RY.
  5. Equity weight (Merton rule) = EEY / (2 * 0.18^2); floor at 0%, cap at 100% (no shorting, no leverage).
  6. Remainder (1 - equity weight) goes to TIP. There is no cash/T-bill option.
  7. Execute at the close; hold to the next month-end; rebalance monthly regardless of change.
- **Notes:** AS text renders the denominator as '2 * 0.182'; the superscript was lost: AS footnote says 0.18 is annual stock volatility and Elm's formula is mu/(gamma*sigma^2) with gamma=2 (Elm's worked example 5%/(2*20%^2)=62.5%), so the denominator is 2*0.18^2=0.0648. AS backtest from 1973; AS simulates TIPS returns and real yields pre-1997 and warns these are educated guesses. AS states the authors helped clarify rules. Exact TIPS-yield series and whether month-end or lagged value is used are not stated by AS. Elm's paper did not state rebalance frequency for main backtests (turnover figures assume monthly).

### 64. Excess Earnings Yield Dynamic with Momentum (`elm_eeyd_with_momentum`)

*James White and Victor Haghani (Elm Wealth)*, family **valuation**, AS status **tracked**, spec status **partial**.

- **Source:** Man Doth Not Invest by Earnings Yield Alone (2022), https://elmwealth.com/man-doth-not-invest-by-earnings-yield-alone/
- **AS page:** https://allocatesmartly.com/excess-earnings-yield-dynamic-valuation-strategy/
- **Rebalance:** monthly; signal and execution at the close of the last trading day of the month; rebalance to target every month even if unchanged
- **Universe:** risky ['SPY']; defensive ['TIP']; canary []; cash None
- **Signal:** EEY_t = 1/CAPE_q - RY_t (as in valuation-only). Momentum: for k = 0..11 take SPY dividend-adjusted month-end close P_{t-k} and form D_{t-k} = P_{t-k} / (CPI_{t-k}/CPI_ref) / 1.04^((t-k - ref)/12) (i.e. deflated by CPI and by a constant 4%/yr risk-premium growth path). MOM = +1 if D_t > mean(D_{t-11..t}) else -1. EEY*_t = EEY_t + 0.02*MOM. w_SPY = clip(EEY*_t / (2*0.18^2), 0, 1); w_TIP = 1 - w_SPY.
- **Data needs:** Shiller monthly CAPE; 10-year TIPS real yield (FRED DFII10 from 2003; earlier sources/simulation needed); US CPI (e.g. FRED CPIAUCNS/CPIAUCSL; lag uncertain, suggest 1-month publication lag); month-end dividend-adjusted closes for SPY and TIP
- **ETF-only start:** 2004 (TIP launched Dec 2003)
- **In plain English:** Same stocks-versus-TIPS valuation model, but with a trend tweak: if stocks (after stripping out inflation and a normal 4% yearly gain) are above their 12-month average, the model treats stocks as 2 percentage points more attractive, otherwise 2 points less attractive, before sizing the stock position.
- **Rules:**
  1. Compute EEY exactly as in the valuation-only variant (1/CAPE from latest quarter-end CAPE at least 3 months old, minus 10-year TIPS real yield).
  2. Take the 12 most recent month-end dividend-adjusted closes of SPY (including the current month-end).
  3. Discount each by cumulative inflation (CPI) and by a constant 4% annual risk premium, producing a real, premium-adjusted series of 12 values.
  4. If the latest discounted value exceeds the simple average of the 12 discounted values, add 0.02 to EEY; otherwise subtract 0.02.
  5. Equity weight = adjusted EEY / (2 * 0.18^2), floored at 0 and capped at 1; remainder to TIP.
  6. Execute at the close; hold until next month-end; rebalance monthly.
- **Notes:** Momentum rule details come from AS (who say the authors helped clarify rules); the Elm article treats momentum as an indicator of risk/return but its public text does not spell out lookback or the +/-2% adjustment, so these could only be verified via AS. Exact discounting implementation (reference date, CPI series/lag, monthly compounding 1.04^(1/12)) is not specified; the comparison is scale-invariant so the reference date does not matter. AS backtest from 1973. See valuation-only entry for the 0.18^2 superscript note and TIPS-history caveats.

### 65. Multi-Asset Momentum (`vitral_multi_asset_momentum`)

*Zambrano and Rizzolo (Vitral Advisors)*, family **momentum-rotation**, AS status **tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** not identified (original Zambrano & Rizzolo paper not located) (None), None
- **AS page:** none (no public AS post)
- **Rebalance:** unknown (AS default would be monthly, last trading day close) (uncertain)
- **Universe:** risky []; defensive []; canary []; cash None
- **Signal:** NOT VERIFIED: rules unavailable. Neither AS's public blog/sitemap nor Vitral Advisors' public website/ADV brochure describes the strategy.
- **Data needs:** unknown until rules are located
- **ETF-only start:** unknown
- **In plain English:** A multi-asset momentum strategy from Vitral Advisors, a small New York investment adviser. Its exact rules could not be found in any public source reviewed, so it cannot yet be replicated.
- **Rules:**
  1. Unable to specify: no public AS post exists (strategy only appears in AS's public list of tracked strategies) and the original source could not be located.
  2. Do not implement until the original paper (likely an SSRN working paper by Zambrano and Rizzolo) or AS member description is obtained.
- **Notes:** Searched all downloaded AS posts and AS post sitemap (no post mentions Vitral/Zambrano/Rizzolo; only list-of-strategies). AS site search returned nothing. Vitral Advisors LLC (SEC RIA, CRD 294631, New York) website describes a systematic growth/inflation regime plus trend/momentum approach but no rules; its Form ADV names Carlos Rizzolo as CCO. Web search budget was exhausted before an SSRN/paper search could be run; follow up by searching SSRN for Zambrano & Rizzolo multi-asset momentum. AS's version would presumably follow AS conventions (one representative ETF per asset class, month-end execution), but this is an assumption.

### 66. Annual Seasonality (`piard_annual_seasonality`)

*Fred Piard*, family **other**, AS status **tracked**, spec status **full**.

- **Source:** Quantitative Investing: Strategies to Exploit Stock Market Anomalies for All Investors (Harriman House) (2013), None
- **AS page:** https://allocatesmartly.com/piards-annual-seasonality/
- **Rebalance:** monthly at the close of the last trading day of the month (positions for month m set at the close of the last trading day of month m-1); rebalanced monthly even without a change
- **Universe:** risky ['EWS', 'EWZ', 'EWG']; defensive []; canary []; cash cash
- **Signal:** Purely calendar-based. For holding month m: EWS = 25% and EWZ = 25% if m in {Nov, Dec, Jan, Feb, Mar, Apr}; EWG = 50% if m in {Oct, Nov, Dec, Mar, Apr}; cash = 1 - sum.
- **Data needs:** month-end dividend-adjusted closes for EWS, EWZ, EWG; 3-month T-bill rate for cash; pre-ETF country equity index TR series for Singapore (from 1970), Germany (from 1970), Brazil (from 1988)
- **ETF-only start:** 2000 (EWZ launched Jul 2000; EWS and EWG 1996)
- **In plain English:** Half the portfolio holds Singapore and Brazil stocks only from November to April; the other half holds German stocks only in October-December and March-April. Whenever a sleeve is out of the market it sits in cash.
- **Rules:**
  1. At the close of the last trading day of each month, determine the next calendar month m.
  2. Sleeve A (50%): if m is November through April, hold 25% EWS and 25% EWZ; otherwise that 50% is in cash.
  3. Sleeve B (50%): if m is October, November, December, March or April, hold 50% EWG; otherwise that 50% is in cash.
  4. Resulting monthly targets: Jan/Feb 25 EWS/25 EWZ/50 cash; Mar/Apr 25 EWS/25 EWZ/50 EWG; May-Sep 100 cash; Oct 50 EWG/50 cash; Nov/Dec 25 EWS/25 EWZ/50 EWG.
  5. Rebalance to these targets at every month-end close.
  6. Before 1988 (no Brazil data in AS) allocate the full 50% of sleeve A to EWS.
- **Notes:** AS backtest from 1970. AS combined two separate Piard strategies 50/50 into one tracked strategy. AS shifted execution from Piard's next-month open to the prior month-end close. Piard's book cites classic multi-century annual-seasonality papers (not identified by name in AS text); book not checked directly. Author tickers assumed to match AS (AS does not mention any substitution).

### 67. Sell in May / Halloween Indicator (`sell_in_may_halloween`)

*N/A (classic anomaly; academic reference Bouman & Jacobsen)*, family **other**, AS status **tracked**, spec status **full**.

- **Source:** The Halloween Indicator, 'Sell in May and Go Away': Another Puzzle (Bouman & Jacobsen, American Economic Review 92(5)) (2002), https://www.aeaweb.org/articles?id=10.1257/000282802762024683
- **AS page:** https://allocatesmartly.com/the-ubiquitous-sell-in-may/
- **Rebalance:** two switches per year at month-end closes: buy SPY at the close of the last trading day of October; move to cash at the close of the last trading day of April
- **Universe:** risky ['SPY']; defensive []; canary []; cash cash
- **Signal:** Calendar: for holding month m, w_SPY = 1 if m in {Nov, Dec, Jan, Feb, Mar, Apr} else 0; w_cash = 1 - w_SPY.
- **Data needs:** daily or month-end dividend-adjusted SPY closes; 3-month T-bill rate; pre-1993: S&P 500 TR index
- **ETF-only start:** 1993 (SPY launched Jan 1993)
- **In plain English:** Own the S&P 500 only during the six 'winter' months from November through April and sit in cash from May through October.
- **Rules:**
  1. At the close of the last trading day of October, go 100% SPY.
  2. Hold through November-April.
  3. At the close of the last trading day of April, sell and go 100% cash (3-month T-bill rate).
  4. Hold cash through May-October; repeat annually.
- **Notes:** AS backtest from 1970. AS notes many variants with different switch dates; AS uses simple month-end switching. AS lists author as N/A; the academic citation is supplied here for context only (paper itself not read beyond its listing).

### 68. Risk Premium Value - Best Value (`rpv_best_value`)

*N/A (AllocateSmartly test; related to CXO Advisory's SACEVS)*, family **valuation**, AS status **tracked**, spec status **partial**.

- **Source:** Testing a Risk Premium Value Strategy (AllocateSmartly; no named original author) (2021), https://allocatesmartly.com/testing-a-risk-premium-value-strategy/
- **AS page:** https://allocatesmartly.com/testing-a-risk-premium-value-strategy/
- **Rebalance:** monthly; signal and execution at the close of the last trading day of the month
- **Universe:** risky ['SPY', 'LQD', 'TLT']; defensive []; canary []; cash cash
- **Signal:** RP_TLT = long-term Treasury yield - short-term Treasury yield; RP_LQD = US IG corporate bond yield - long-term Treasury yield; RP_SPY = S&P 500 earnings yield (earnings lagged >= 4 months) - long-term Treasury yield. Z_i,t = (RP_i,t - mean(RP_i, data inception..t)) / sd(RP_i, data inception..t) (expanding window, no lookahead). Positive Z = undervalued.
- **Data needs:** long-term Treasury yield (series not stated; e.g. FRED DGS10/DGS20/DGS30) (uncertain); short-term Treasury yield (series not stated; e.g. FRED DTB3/DGS3MO) (uncertain); US investment-grade corporate yield (series not stated; e.g. Moody's Baa FRED DBAA or Aaa DAAA) (uncertain); S&P 500 earnings yield (earnings type not stated; trailing earnings lagged >= 4 months) (uncertain); dividend-adjusted closes for SPY, LQD, TLT; 3-month T-bill rate for cash
- **ETF-only start:** 2003 (LQD and TLT launched Jul 2002)
- **In plain English:** Measures how generous the extra yield is on long Treasuries (vs short), corporate bonds (vs Treasuries) and stocks (earnings yield vs Treasuries), compared with history. It puts everything into the asset whose premium is most above its historical norm, or into cash if none is above normal.
- **Rules:**
  1. At the close on the last trading day of the month compute the three risk premiums using yield data lagged up to 2 days for reporting delays (AS's daily-data test from 1987).
  2. Normalize each premium as a z-score versus its own mean and standard deviation from the start of the data history through the current date (expanding window).
  3. Pick the asset with the highest z-score.
  4. If that z-score > 0, allocate 100% to that asset's ETF (TLT, LQD or SPY); if it is <= 0, allocate 100% to cash.
  5. Tie-break not specified (implementer choice, e.g. fixed order).
  6. Hold until the next month-end; rebalance monthly.
- **Notes:** AS does not name an original author ('N/A' on its list) and says it is not a SACEVS replication, though annual-return correlation with SACEVS exceeds 98%. Exact yield series, earnings definition, and data inception date for the expanding normalization are not disclosed; z-score computed on daily vs month-end observations is not stated (uncertain). AS notes results depend on the start date chosen for normalization.

### 69. Risk Premium Value - Weighted (`rpv_weighted`)

*N/A (AllocateSmartly test; related to CXO Advisory's SACEVS)*, family **valuation**, AS status **tracked**, spec status **partial**.

- **Source:** Testing a Risk Premium Value Strategy (AllocateSmartly; no named original author) (2021), https://allocatesmartly.com/testing-a-risk-premium-value-strategy/
- **AS page:** https://allocatesmartly.com/testing-a-risk-premium-value-strategy/
- **Rebalance:** monthly; signal and execution at the close of the last trading day of the month; rebalanced monthly
- **Universe:** risky ['SPY', 'LQD', 'TLT']; defensive []; canary []; cash cash
- **Signal:** Same RP and expanding z-score Z_i as RPV Best Value. Weights: w_i = Z_i / sum_{j: Z_j > 0} Z_j for Z_i > 0, else 0; if no Z_i > 0, w_cash = 1.
- **Data needs:** same yield/earnings series as rpv_best_value (series unspecified by AS); dividend-adjusted closes for SPY, LQD, TLT; 3-month T-bill rate for cash
- **ETF-only start:** 2003 (LQD and TLT launched Jul 2002)
- **In plain English:** Same valuation gauges as RPV Best Value, but instead of picking one winner it spreads money across every asset that looks cheap relative to history, giving more to the cheaper ones; if nothing looks cheap it holds cash.
- **Rules:**
  1. Compute the three risk premiums and their expanding-window z-scores exactly as in RPV Best Value.
  2. Keep only assets with z-score > 0.
  3. Allocate to those assets in proportion to their positive z-scores (interpretation of AS's 'proportionally'); weights sum to 100%.
  4. If all z-scores are <= 0, allocate 100% to cash.
  5. Hold until the next month-end; rebalance monthly.
- **Notes:** AS notes the Weighted version still often ends up concentrated (e.g. 100% SPY at time of writing). Proportional-to-z weighting is the natural reading but not explicitly defined. Other caveats as in rpv_best_value.

### 70. All-Weather/All-Seasons Portfolio (`dalio_all_weather`)

*Ray Dalio (as published by Tony Robbins)*, family **static**, AS status **tracked**, spec status **partial**.

- **Source:** MONEY Master the Game (Tony Robbins, interview with Ray Dalio; 'All Seasons' portfolio) (2014), None
- **AS page:** none (no public AS post)
- **Rebalance:** annually (AS assumption for these four-season buy & hold portfolios); exact rebalance date not stated, presumably the close of the last trading day of the year (uncertain)
- **Universe:** risky ['SPY', 'TLT', 'IEF', 'GLD', 'DBC']; defensive []; canary []; cash None
- **Signal:** None (static weights).
- **Data needs:** month-end (or daily for annual rebalance) dividend-adjusted closes for SPY, TLT, IEF, GLD, DBC/PDBC; pre-ETF index proxies: S&P 500 TR, long and intermediate Treasury TR, gold spot, commodity TR index
- **ETF-only start:** 2006 (DBC launched Feb 2006; GLD Nov 2004)
- **In plain English:** A fixed mix designed to hold up in growth, recession, inflation and deflation: 30% US stocks, 55% Treasuries (mostly long-term), and 15% split between gold and commodities, rebalanced once a year.
- **Rules:**
  1. Hold 30% SPY, 40% TLT, 15% IEF, 7.5% GLD, 7.5% DBC at all times.
  2. Let weights drift; once a year reset to target weights at the close (AS: annual rebalance).
  3. No signals or trades other than the annual rebalance.
- **Notes:** No dedicated AS post. AS (Golden Butterfly post, 2016) says it tracks the version published in Robbins' 'Money: Master the Game' and assumes annual rebalancing; AS's 2019 strategy-asset matrix confirms the ETF set SPY, TLT, IEF, GLD, DBC. Weights 30/40/15/7.5/7.5 are the widely reported Robbins version (not printed in AS public text); PortfolioCharts' 'All Seasons' rounds gold/commodities to 8/7. Whether AS still rebalances annually (vs monthly) today and on which date is not verified.

### 71. Permanent Portfolio (`browne_permanent_portfolio`)

*Harry Browne*, family **static**, AS status **tracked**, spec status **partial**.

- **Source:** Fail-Safe Investing: Lifelong Financial Security in 30 Minutes (concept dates to Browne's early-1980s writings) (1999), None
- **AS page:** none (no public AS post)
- **Rebalance:** annually (AS assumption); exact date not stated, presumably close of last trading day of the year (uncertain)
- **Universe:** risky ['SPY', 'TLT', 'GLD']; defensive []; canary []; cash cash
- **Signal:** None (static weights).
- **Data needs:** dividend-adjusted closes for SPY, TLT, GLD; 3-month T-bill rate for cash; pre-ETF: S&P 500 TR, long Treasury TR, gold spot
- **ETF-only start:** 2005 (GLD launched Nov 2004)
- **In plain English:** Splits money equally four ways: US stocks for prosperity, long-term Treasuries for deflation, gold for inflation and cash for recession, then rebalances once a year.
- **Rules:**
  1. Hold 25% SPY, 25% TLT, 25% GLD, 25% cash.
  2. Rebalance to equal 25% weights once a year at the close.
  3. Cash earns the 3-month T-bill rate (AS tracks the cash version, not SHY).
- **Notes:** No dedicated AS post. AS Golden Butterfly post states the tracked Permanent Portfolio uses cash as the short-duration sleeve and annual rebalancing; AS 2019 strategy-asset matrix lists GLD, SPY, TLT, Cash. Browne's original band-rebalancing rule differs from AS's annual schedule (from memory; not verified here).

### 72. Golden Butterfly (`portfoliocharts_golden_butterfly`)

*Tyler (PortfolioCharts.com)*, family **static**, AS status **tracked**, spec status **partial**.

- **Source:** Golden Butterfly Portfolio (PortfolioCharts.com) (2016), https://portfoliocharts.com/portfolios/golden-butterfly-portfolio/
- **AS page:** https://allocatesmartly.com/portfoliocharts-golden-butterfly/
- **Rebalance:** annually (AS assumption); exact date not stated, presumably close of last trading day of the year (uncertain)
- **Universe:** risky ['SPY', 'IWN', 'TLT', 'GLD']; defensive ['SHY']; canary []; cash None
- **Signal:** None (static weights).
- **Data needs:** dividend-adjusted closes for SPY, IWN/VBR, TLT, SHY, GLD; pre-ETF: S&P 500 TR, small-cap value index (small-cap index before 1979), long and short Treasury TR, gold spot
- **ETF-only start:** 2005 (GLD Nov 2004; IWN Jul 2000; SHY/TLT Jul 2002)
- **In plain English:** Five equal 20% slices: US large stocks, US small value stocks, long-term Treasuries, short-term Treasuries and gold. It leans toward growth by doubling the stock exposure versus the Permanent Portfolio and is rebalanced once a year.
- **Rules:**
  1. Hold 20% each of SPY, IWN (US small cap value; VBR from 2025), TLT, SHY, GLD.
  2. Rebalance to equal 20% weights once a year at the close.
  3. AS uses SHY (not cash) for the short-term Treasury sleeve, as the author intended.
- **Notes:** PortfolioCharts page confirms the five 20% sleeves (large cap blend, small cap value, long-term Treasuries, short-term Treasuries, gold) but does not state a rebalance rule; annual rebalancing is AS's assumption. AS backtest from 1970.

### 73. Lumber-Gold Strategy (intermarket risk rotation) (`bilello_gayed_lumber_gold`)

*Charles Bilello and Michael Gayed*, family **other**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** An Intermarket Approach to Tactical Risk Rotation: Using the Signaling Power of Lumber and Gold (2015), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2604248
- **AS page:** https://allocatesmartly.com/the-lumber-gold-strategy/
- **Rebalance:** weekly; signal computed and traded at the close of the last trading day of each week
- **Universe:** risky ['SPY']; defensive ['IEF']; canary ['LB1 (generic 1st lumber futures)', 'gold price (series not specified by AS)']; cash None
- **Signal:** R13_X = P_X(t) / P_X(t - 13 weeks) - 1 using last-trading-day-of-week closes; RISK_ON = R13_lumber > R13_gold. Lumber = generic front-month lumber futures (Bloomberg LB1 COMB Comdty).
- **Data needs:** weekly (from daily) closes of generic front-month lumber futures (Bloomberg LB1 COMB Comdty or equivalent continuous series); weekly gold price (spot or GLD; AS does not say which); daily adjusted close SPY, IEF
- **ETF-only start:** 2002 (IEF); AS backtest from 1987 with proxies
- **In plain English:** Lumber prices tend to rise when the economy is heating up, while gold tends to rise when investors are nervous. Each week, if lumber has beaten gold over the last quarter the strategy owns US stocks; otherwise it owns intermediate Treasuries.
- **Rules:**
  1. At the close on the last trading day of each week, compute the 13-week return of lumber (generic 1st futures, LB1) and of gold.
  2. If lumber's 13-week return is greater than gold's, hold 100% SPY from that close.
  3. Otherwise (including a tie) hold 100% IEF from that close.
  4. Hold until the close of the last trading day of the following week, then repeat.
  5. Optional AS variant: run the same rule on another fixed weekday, comparing that day to the same weekday 13 weeks earlier (AS found Monday weakest, differences small).
- **Notes:** Original SSRN paper could not be retrieved (HTTP 403); rules taken from AS. AS does not state which gold series is used for the signal (spot gold or GLD both plausible) - uncertain. Generic LB1 is an unadjusted front-month price series, so roll gaps affect the 13-week return; also CME's original random-length lumber contract was replaced by a new lumber contract around 2022-23, so a continuous series must be spliced (our observation, verify). Turnover ~7x/yr; AS estimates ~1.5%/yr cost drag at 0.1%/trade. AS observed lumber's 13-week return alone gives similar results (lumber ~3x more volatile than gold). Won the 2015 NAAIM Wagner Award.

### 74. BKLN 3/12-Day Moving Average Strategy (`smith_bkln`)

*Cliff Smith*, family **trend-following**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Unique Application Of Moving Day Average To High Yield Bond ETFs (Seeking Alpha) (2014), https://seekingalpha.com/article/1939751-unique-application-of-moving-day-average-to-high-yield-bond-etfs
- **AS page:** https://allocatesmartly.com/cliff-smiths-bkln-strategy/
- **Rebalance:** daily; evaluated and traded at each day's close
- **Universe:** risky ['BKLN']; defensive []; canary []; cash cash
- **Signal:** SMA3_t = mean of the last 3 daily closes including today's close; SMA12_t = mean of the last 12 daily closes including today's close; LONG = SMA3_t > SMA12_t
- **Data needs:** daily close (and adjusted close for returns) of BKLN; S&P/LSTA Leveraged Loan 100 index daily level for 2007-2011 extension; T-bill rate for cash return
- **ETF-only start:** 2011 (BKLN launched 03/2011); AS extended to 2007 with index data
- **In plain English:** A very fast trend filter on a senior (leveraged) loan fund. When the 3-day average price is above the 12-day average it owns the fund, otherwise it sits in cash.
- **Rules:**
  1. Each trading day, using today's closing price, compute the 3-day and 12-day moving averages of BKLN.
  2. If the 3-day MA ends the day above the 12-day MA, hold 100% BKLN at the close.
  3. Otherwise hold 100% cash at the close.
  4. Repeat every trading day.
- **Notes:** Original Seeking Alpha article blocked (HTTP 403); rules from AS, cross-checked with a third-party write-up which uses the same 3/12-day cross on BKLN (that write-up holds SHY when out - not from AS; AS uses cash). AS's headline chart excludes trading costs; at AS's standard 0.1%/trade the strategy was roughly flat for ~11 years, so execution cost is decisive. AS suggests pre-computing the crossing price and using MOC/LOC orders. Publication year 2014 inferred from AS saying 10+ years before 2025 (uncertain).

### 75. Countercyclical Trend Following (`as_countercyclical_trend`)

*Undisclosed (AS withheld the authors' names)*, family **macro**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Undisclosed paper (title withheld by AS; AS could not confirm rules with the authors) (None), None
- **AS page:** https://allocatesmartly.com/countercyclical-trend-following/
- **Rebalance:** economic regime set monthly at the last trading day close; SPY/GLD trend overlay checked daily at the close (trades can occur any day)
- **Universe:** risky ['SPY', 'IWN', 'GLD']; defensive ['LQD', 'IEF']; canary []; cash None
- **Signal:** HY = ICE BofA US High Yield OAS (FRED BAMLH0A0HYM2), before 12/1996 Moody's Baa yield minus 10y CMT (BAA - DGS10); SLOPE = 10y CMT - 1y CMT (DGS10 - DGS1). Each read with a 2-trading-day lag and compared to its own trailing 10-year median. TREND_i for SPY and GLD: becomes UP after 5 consecutive closes above the 200-day SMA, DOWN after 5 consecutive closes below; otherwise unchanged.
- **Data needs:** FRED BAMLH0A0HYM2 (daily, from 12/1996); FRED BAA / DBAA and DGS10 (pre-1997 HY proxy); FRED DGS10 and DGS1 (daily); daily adjusted close SPY, IWN (IWM pre-1990), GLD, LQD, IEF
- **ETF-only start:** 2004 (GLD 11/2004; IWN 2000, LQD/IEF 2002); AS backtest from 1980
- **In plain English:** Uses credit spreads and the yield curve to decide whether the economy looks stressed, inflationary or slowing, buying more risk when spreads are wide (a contrarian view). Stock and gold positions are also protected by a 200-day trend filter that moves them into Treasuries during downtrends.
- **Rules:**
  1. At the close on the last trading day of each month, take the HY spread and the 10y-1y slope as of 2 trading days earlier and compare each to its median over the trailing 10 years.
  2. If HY spread > its 10-year median: regime = Growth (contrarian; ignore the slope). Portfolio: 50% SPY, 40% IWN, 10% GLD.
  3. Else if slope < its 10-year median: regime = Inflation. Portfolio: 50% SPY, 10% IWN, 40% GLD.
  4. Else (HY spread below median and slope above median): regime = Slowdown. Portfolio: 50% LQD, 40% IEF, 10% IWN.
  5. Rebalance to the regime portfolio at that close; the regime holds until the next month-end close.
  6. Trend overlay, maintained every day regardless of regime: an asset's state flips to downtrend after 5 consecutive closes below its 200-day SMA and to uptrend after 5 consecutive closes above it.
  7. Whenever SPY or GLD is in downtrend, its portfolio sleeve is held in IEF instead; when it returns to uptrend the sleeve moves back. These switches are executed at the close on the day the trend state changes, including mid-month.
  8. Pre-1990, replace IWN with IWM (US small caps) per AS.
- **Notes:** AS stated it could not confirm the exact rules with the authors and captured 'the spirit' of the strategy; original paper unidentified. Not specified: whether the 10-year medians use daily or month-end observations (uncertain), tie handling at the median, and whether the regime portfolio drifts intra-month (assume no rebalance except on trend switches). AS chose monthly regime updates (daily updating was worse after costs). Authors likely used Ken French small-value data, which AS considers unrealistically strong. AS's historical-proxy indices for GLD/LQD/IEF before ETF inception are not listed in the post (AS normally uses underlying indices).

### 76. Trending Fast and Slow (volatility-switched momentum) (`jpm_trending_fast_slow`)

*Authors of 'Trending Fast and Slow' (Journal of Portfolio Management, 2022) - names not verified*, family **trend-following**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Trending Fast and Slow (The Journal of Portfolio Management 48(3), p.103) (2022), https://jpm.pm-research.com/content/48/3/103
- **AS page:** https://allocatesmartly.com/trending-fast-and-slow/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY']; defensive []; canary []; cash cash
- **Signal:** VOL_t = stdev of daily log returns ln(P_d/P_{d-1}) of the S&P 500 price index over the last 21 trading days x sqrt(252). If VOL_t >= 0.17: MOM = P_t / P_{t-1m} - 1, else MOM = P_t / P_{t-12m} - 1 (S&P 500 price index, month-end closes). LONG = MOM > 0.
- **Data needs:** daily S&P 500 price index (^GSPC); daily adjusted close SPY (or S&P 500 TR); T-bill rate for cash
- **ETF-only start:** 1993 (SPY); 2007 if BIL used as cash
- **In plain English:** Looks at how volatile the stock market was over the past month. In calm markets it follows the 12-month trend; in turbulent markets (above 17% annualized volatility) it follows only the last month's move, and it is either fully in stocks or in cash.
- **Rules:**
  1. At the close on the last trading day of the month compute the annualized 21-day volatility of the S&P 500 price index.
  2. If volatility >= 17%, use the 1-month price change; otherwise use the 12-month price change.
  3. If that change is positive, hold 100% SPY at the close; otherwise hold cash.
  4. Hold until the last trading day of the following month.
- **Notes:** Paper not accessible (paywall/redirect) and authors could not be confirmed. AS's volatility definition (21-day log-return stdev x sqrt 252) is AS's own choice since the authors did not specify it; AS matched the authors' results closely. The 17% cutoff came from the authors' decision-tree analysis (~top quintile of observations). Original is long/short; AS long/cash. AS does not plan to track it.

### 77. Yield-Based Asset Class Rotation (`schwartz_yield_rotation`)

*Harrison Schwartz*, family **macro**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Simple Rules-Based Asset Rotation Strategy (Seeking Alpha) (2019), https://seekingalpha.com/article/4283733-simple-rules-based-asset-rotation-strategy
- **AS page:** https://allocatesmartly.com/testing-a-yield-based-asset-class-rotation-strategy/
- **Rebalance:** daily; AS base test trades at the close of the same day as the yield data (not realistic), AS practical variant uses smoothed, lagged data
- **Universe:** risky ['SPY', 'GLD']; defensive ['TLT']; canary []; cash None
- **Signal:** S_SPY = T10Y2Y (10y minus 2y CMT); S_TLT = DFII20 (20-year TIPS yield); S_GLD = T10YIE - T10Y2Y (10y breakeven inflation minus the 10y-2y spread; sign convention inferred, uncertain). Hold argmax(S_SPY, S_TLT, S_GLD).
- **Data needs:** FRED T10Y2Y (daily); FRED DFII20 (daily, from 07/2004); FRED DTP30A28 (daily, to extend DFII20 pre-2004); FRED T10YIE (daily, from 01/2003); daily adjusted close SPY, TLT, GLD
- **ETF-only start:** 2004 (GLD 11/2004; TLT 07/2002)
- **In plain English:** Compares three bond-market readings - the steepness of the yield curve, the long-term real interest rate, and how inflation expectations compare to the curve - and owns stocks, long Treasuries or gold depending on which reading is highest.
- **Rules:**
  1. Each day, read the three series: 10y-2y Treasury spread (-> SPY), 20-year TIPS real yield (-> TLT), and 10y breakeven inflation minus the 10y-2y spread (-> GLD).
  2. Hold 100% of the asset whose series is highest.
  3. AS base test: execute at the close of the same day as the data.
  4. AS practical variant: smooth each series with a 5-day simple moving average and use the value from 3 trading days earlier, then pick the highest (cut trades from ~4/yr to ~1.6/yr; AS says the parameters were arbitrary and other reasonable values were similar).
- **Notes:** Original Seeking Alpha article blocked (HTTP 403). The gold series direction is not explicit in AS text; AS links a FRED graph listing T10YIE first and T10Y2Y second, and T10YIE - T10Y2Y is consistent with the reported trade history (Treasuries ~1998-2003, equities next, gold from ~2018 to early 2020) - treat as likely but unverified. T10YIE begins 2003; AS does not say how the breakeven was obtained for 1998-2002 (uncertain). AS declined to track: the record is dominated by three long trades (73% of the test).

### 78. Buy Global Stocks at All-Time Highs (else bonds) (`econompic_faber_global_ath`)

*Jake Moore (EconomPic) and Meb Faber*, family **trend-following**, AS status **reviewed_not_tracked**, spec status **full**.

- **Source:** Is Buying Stocks at an All-Time High a Good Idea? (2019), https://mebfaber.com/2019/11/04/is-buying-stocks-at-an-all-time-high-a-good-idea/
- **AS page:** https://allocatesmartly.com/buying-global-stocks-at-all-time-highs/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['ACWI']; defensive ['AGG']; canary []; cash None
- **Signal:** ATH_t = P_ACWI(t) >= max over all prior month-end closes P_ACWI(s), s < t (month-end data only)
- **Data needs:** monthly close of ACWI or global equity index (long history from GFD/MSCI); monthly adjusted close AGG or US aggregate bond index
- **ETF-only start:** 2008 (ACWI 03/2008; AGG 09/2003); AS backtest from 1926
- **In plain English:** Owns global stocks only in months when they have just closed at a record high; the rest of the time it owns US bonds. It holds stocks less than 30% of the time.
- **Rules:**
  1. At the close on the last trading day of the month, check whether ACWI's month-end close is a new all-time high versus all previous month-end closes.
  2. If yes, hold 100% ACWI from that close; otherwise hold 100% AGG.
  3. Hold until the last trading day of the following month.
- **Notes:** Faber's post describes the rule generically (stocks at all-time high -> stocks next month, else government bonds); AS chose ACWI and AGG. Whether the all-time high is measured on price or total return is not stated (AS normally uses dividend-adjusted data; uncertain). Tie (equal to prior high) treated as a high here - not specified. AS used this as an illustration that new highs are not a reason to avoid stocks; results depend heavily on bond returns.

### 79. Lazy Man's Momentum Strategy (country rotation) (`lazy_mans_momentum`)

*Not verified (SSRN working paper 5644131)*, family **momentum-rotation**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Lazy Man's Momentum Strategy (SSRN 5644131; exact title/authors not verified) (2025), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5644131
- **AS page:** https://allocatesmartly.com/challenging-the-lazy-mans-momentum-strategy/
- **Rebalance:** semi-annually, at the close of the last trading day of June and December
- **Universe:** risky ['22 country equity indices (list per source paper; not given by AS, not verified)']; defensive []; canary []; cash None
- **Signal:** MOM6_i = P_i(t) / P_i(t-6m) - 1 on month-end closes (total return presumed)
- **Data needs:** monthly total-return series for the 22 country indices (MSCI) or iShares country ETFs; ACWI for benchmark
- **ETF-only start:** 1996 (most iShares MSCI country ETFs launched 03/1996) - depends on the unverified country list
- **In plain English:** Twice a year it buys the half of 22 national stock markets that rose the most over the previous six months, in equal amounts. AS found the momentum selection has added nothing versus picking the losers since about 2000; most of the long-run edge came from equal weighting.
- **Rules:**
  1. At the end of June and December, rank the 22 country indices by 6-month return.
  2. Hold the 11 highest-ranked countries in equal weight (1/11 each), regardless of whether their returns are positive.
  3. Hold for six months until the next rebalance.
  4. Optional (AS robustness check): split into 6 tranches rebalanced semi-annually in different month pairs (Dec/Jun, Jan/Jul, ...); AS found essentially identical results.
- **Notes:** Source paper not retrievable (SSRN 403) - authors, country list and return convention unverified. AS will not add it: relative performance vs the inverse (bottom-11) strategy has been flat since mid-2000. AS floated, but did not test, an absolute-momentum variant (send negative-momentum slots to cash).

### 80. Front-Running Commodity Seasonality (with correlation filter) (`quantpedia_commodity_frontrun_seasonality`)

*Cyril Dujava (Quantpedia)*, family **other**, AS status **reviewed_not_tracked**, spec status **full**.

- **Source:** Trader's Guide to Front-Running Commodity Seasonality (2024), https://quantpedia.com/traders-guide-to-front-running-commodity-seasonality/
- **AS page:** https://allocatesmartly.com/front-running-commodity-seasonality/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['DBA', 'DBB', 'DBE', 'DBP']; defensive []; canary []; cash cash
- **Signal:** For month t (positioning for t+1): s = t-10 (the same calendar month as t+1, one year earlier; author's 'X-11'). PCT_i = percentile rank of r_i(s) within ETF i's own monthly returns from s through t (AS: 'all months since'; Quantpedia: the last 12 monthly returns). SIDE_i = +1 if PCT_i >= 50th percentile else -1. Correlation filter: C_S = average pairwise correlation of daily returns of the 4 ETFs over the last 20 trading days, C_L = same over the last 250 trading days; RISK_OFF = C_S > C_L.
- **Data needs:** daily adjusted close DBA, DBB, DBE, DBP (or DB/Bloomberg/GSCI sector index proxies); monthly returns from the same
- **ETF-only start:** 2007 (all four Invesco DB sector ETFs launched 01/2007)
- **In plain English:** Bets that commodity seasonal patterns get traded a month early: each month it goes long or short four commodity sector funds depending on whether their return in the corresponding month a year earlier was strong or weak. A filter moves to cash when the four commodities start moving too much in lockstep.
- **Rules:**
  1. At each month-end, for each ETF take its return in the month 11 months before the month being positioned for (e.g. at end-December use the previous February).
  2. Rank that return against the ETF's own monthly returns since then; at or above the median -> long, below -> short.
  3. Base version: +/-25% of capital in each ETF (net exposure between -100% and +100%).
  4. Risk-parity variant: size each position inversely to its trailing 36-month volatility (scaling to 100% gross assumed - uncertain).
  5. Correlation-filter variant: if the 20-day average pairwise correlation exceeds the 250-day average, hold 100% cash for the month.
  6. Long-only variant (AS Test #3, includes the correlation filter): short signals become cash (each ETF slot 25%).
  7. Hold all positions until the next month-end.
- **Notes:** AS post lists 'DBC: Energy' - a typo for DBE (later text says DBE). Proof of concept: AS ignored transaction and shorting costs. AS found results concentrated in 2000-2010 and flat otherwise; the correlation filter improved Sharpe. Quantpedia's article gives the 20/250-day windows only in its companion momentum article; exact averaging formula (pairwise mean) not stated - uncertain. Risk-parity sizing formula not stated by AS. Long-short base is the author's design; the long-only variant is AS's.

### 81. Commodity Momentum/Reversal with Intra-Market Correlation (`quantpedia_commodity_mom_rev_corr`)

*Margareta Pauchlyova (Quantpedia)*, family **momentum-rotation**, AS status **reviewed_not_tracked**, spec status **full**.

- **Source:** How to Improve Commodity Momentum Using Intra-Market Correlation (2024), https://quantpedia.com/how-to-improve-commodity-momentum-using-intra-market-correlation/
- **AS page:** https://allocatesmartly.com/front-running-commodity-seasonality/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['DBA', 'DBB', 'DBE', 'DBP']; defensive []; canary []; cash None
- **Signal:** MOM12_i = P_i(t) / P_i(t-12m) - 1 (adjusted closes); C_S = average pairwise correlation of daily returns over the last 20 trading days; C_L = same over the last 250 trading days.
- **Data needs:** daily adjusted close DBA, DBB, DBE, DBP (or index proxies)
- **ETF-only start:** 2007
- **In plain English:** A long/short commodity sector strategy that follows momentum when the four sectors are moving together more than usual and bets on reversal when they are moving apart.
- **Rules:**
  1. At each month-end compute the 12-month return of each of the four ETFs and the short- and long-window average correlations.
  2. If C_S > C_L (momentum regime): long the 2 ETFs with the highest 12-month return and short the 2 with the lowest.
  3. If C_S < C_L (reversal regime, per Quantpedia): long the 2 ETFs with the lowest 12-month return and short the 2 with the highest.
  4. Equal weights (assume +/-25% each, 100% gross - uncertain); hold for one month.
- **Notes:** AS's wording of the reversal branch appears garbled (it repeats the momentum positions); Quantpedia's article states the reversal regime goes long the 2 worst and short the 2 best, which is used here. Tie (C_S = C_L) unspecified. AS found it worked only over the author's original sample and failed in earlier years; no costs included. Long/short only.

### 82. Front-Running Seasonality in Country ETFs (`quantpedia_country_frontrun_seasonality`)

*Sona Beluska (Quantpedia)*, family **other**, AS status **reviewed_not_tracked**, spec status **full**.

- **Source:** Front Running in Country ETFs, or How to Spot and Leverage Seasonality (2025), https://quantpedia.com/front-running-in-country-etfs-or-how-to-spot-and-leverage-seasonality/
- **AS page:** https://allocatesmartly.com/front-running-seasonality-in-country-etfs-an-extended-test/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY', 'EWU', 'EWG', 'EWQ', 'EWI', 'EWD', 'EWN', 'EWP', 'EWK', 'EWL', 'EWC', 'EWJ', 'EWW', 'EWM', 'EWA', 'EWS', 'EWY', 'EWT', 'EWZ', 'EWH', 'EZA', 'FXI', 'INDY']; defensive []; canary []; cash None
- **Signal:** SCORE_i = r_i(t-10): the ETF's return in the calendar month that is 11 months before the month being positioned for (at end of March, use May of the previous year); rank cross-sectionally, descending.
- **Data needs:** monthly total-return series for the 23 ETFs or their MSCI country index proxies
- **ETF-only start:** 2009 (INDY 11/2009; FXI 2004, EZA 2003, most EWx 1996)
- **In plain English:** Assumes investors anticipate each country's seasonal pattern a month early. Each month it buys the 8 country funds that did best, a year ago, in the month that is now one month ahead, with larger weights for the top ranks.
- **Rules:**
  1. At the close on the last trading day of month t, rank all available country ETFs by their return in month t-10.
  2. Select the top 8 and weight them: ranks 1-3 18.18% each, rank 4 15.15%, rank 5 12.12%, rank 6 9.09%, rank 7 6.06%, rank 8 3.03% (i.e. 6,6,6,5,4,3,2,1 /33).
  3. Hold until the last trading day of the following month and repeat.
  4. ETFs enter the universe only once data exist (Quantpedia added EZA, FXI, INDY after their launches).
- **Notes:** Quantpedia's final portfolio averages six sub-portfolios (top 3, 4, ..., 8); AS translated this into the rank weights above (AS assumption, matched their overlap closely). If each sub-portfolio were equal-weighted internally, weights would be the 'alt' set (our computation). AS results exclude transaction costs and AS declined to track (not consistently effective since 1971, esp. late 1990s). Without the front-running month (same month last year) results were worse.

### 83. 12-Month Momentum with Distance-to-1-Year-High Filter (`as_dist_1yr_high`)

*Allocate Smartly*, family **trend-following**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** A Key New Momentum Measure to Consider: Distance from 1-Year High (2023), https://allocatesmartly.com/a-key-new-momentum-measure-to-consider-distance-from-1-year-high/
- **AS page:** https://allocatesmartly.com/a-key-new-momentum-measure-to-consider-distance-from-1-year-high/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY']; defensive []; canary []; cash BIL
- **Signal:** MOM12 = P_t / P_{t-12m} - 1 (dividend-adjusted month-end closes); D = (P_t - min(P_{t-12..t})) / (max(P_{t-12..t}) - min(P_{t-12..t})) over 13 month-end closes including the current one; LONG = MOM12 > 0 AND D >= 0.75
- **Data needs:** monthly dividend-adjusted S&P 500 / SPY closes; 13-week T-bill rate
- **ETF-only start:** 1993 (SPY); 2007 with BIL
- **In plain English:** A classic rule that owns stocks when they are up over the past year, with an extra check: the market must also be in the top quarter of its 1-year price range. If it has risen over the year but fallen well off its high, it waits in cash.
- **Rules:**
  1. At the close on the last trading day of the month compute the S&P 500's 12-month dividend-adjusted price change.
  2. Compute D, the position of the current close within the range of the last 13 month-end closes (0 = 1-year low, 1 = 1-year high).
  3. If the 12-month change is positive and D >= 0.75, hold 100% SPY; otherwise hold T-bills.
  4. Hold until the next month-end.
- **Notes:** AS's own proof of concept (no transaction costs), inspired by Alpha Architect's coverage of an SSRN paper (abstract 2900073, title not verified) on distance from the 52-week high and momentum crashes; AS changed it to a long-only, monthly, no-skip-month index strategy. Boundary (>= vs > 0.75) not stated; AS's bucket table groups 75% with the stronger bucket. Whether D uses the same dividend-adjusted series is not stated (presumed). Revised strategy reduced drawdowns but underperformed the baseline for ~20 years from the early 1990s.

### 84. Aggregate Investor Allocation to Equities (AIAE) Timing (`philecon_aiae_timing`)

*Philosophical Economics (Jesse Livermore, pseudonym) - indicator; Allocate Smartly - trading rule*, family **valuation**, AS status **reviewed_not_tracked**, spec status **full**.

- **Source:** The Single Greatest Predictor of Future Stock Market Returns (2013), https://www.philosophicaleconomics.com/2013/12/the-single-greatest-predictor-of-future-stock-market-returns/
- **AS page:** https://allocatesmartly.com/our-take-on-the-single-greatest-predictor-of-future-stock-market-returns/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['SPY']; defensive []; canary []; cash BIL
- **Signal:** AIAE = E / (E + D), E = market value of corporate equities (FRED NCBEILQ027S + FBCELLQ027S), D = liabilities of real-economy borrowers (FGSDODNS + CMDEBT + BCNSDODNS + DODFFSWCMI + SLGSDODNS), all in the same units. FORECAST_t = a_t + b_t * AIAE_latest from an expanding-window OLS of subsequent 10-year annualized S&P 500 total return on AIAE, using only observations whose 10-year outcome is known at t; LONG = adjusted FORECAST_t > current T-bill yield.
- **Data needs:** FRED/ALFRED quarterly Z.1 series: NCBEILQ027S, FBCELLQ027S, FGSDODNS, CMDEBT, BCNSDODNS, DODFFSWCMI, SLGSDODNS (first-release vintages; check unit differences - millions vs billions); Z.1 release dates; monthly S&P 500 TR / SPY; 3-month T-bill yield (FRED TB3MS/DTB3)
- **ETF-only start:** 1993 (SPY); 2007 with BIL
- **In plain English:** Measures what share of investors' total holdings is in stocks; when that share is high, future 10-year returns have tended to be low. The rule owns stocks when the indicator's forecast return beats T-bills and holds T-bills otherwise.
- **Rules:**
  1. At the close on the last trading day of each month, take the latest published AIAE value (quarterly Federal Reserve Z.1 data; first-release vintage; may be up to ~5 months old).
  2. Fit an OLS regression of subsequent 10-year annualized S&P 500 (dividend-adjusted) return on AIAE using all observations from inception (12/1951) whose 10-year forward return is complete by today (walk-forward, no lookahead).
  3. Forecast the next-10-year annualized return from the latest AIAE.
  4. Adjust the forecast for the S&P 500's move since the AIAE observation date (AS follows Micaletti; exact adjustment formula not given).
  5. If the adjusted forecast exceeds the T-bill yield, hold 100% SPY; otherwise hold T-bills. Hold until next month-end.
- **Notes:** Trading rule is AS's own simple illustration (long ~87% of the time); AS says it barely improved risk-adjusted returns and failed to avoid 2008. FRED series codes come from Portfolio Optimizer's 2023 replication (the original 2013 post defines the ratio conceptually: stocks / (stocks + liabilities of households, nonfinancial corporates, state/local and federal government, rest of world)). AS says it used monthly data in the regression though Z.1 is quarterly - how monthly AIAE values were formed (forward-fill or market-adjusted) is not stated (uncertain). The market-move adjustment method is not specified. AS also mentions but did not publish versions based on Micaletti ('Towards a Better Fed Model') and Asness et al. ('Market Timing: Sin a Little').

### 85. End-of-Month / Second-Half-of-Month Treasury ETF Seasonality (`hartley_schwarz_eom_treasury`)

*Jonathan Hartley and Krista Schwarz (paper); ETF application by Allocate Smartly*, family **other**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Predictable End-of-Month Treasury Returns (2019), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3440417
- **AS page:** https://allocatesmartly.com/predictable-end-of-month-treasury-etf-returns/
- **Rebalance:** calendar-based daily timing, close-to-close
- **Universe:** risky ['TLT']; defensive []; canary []; cash cash
- **Signal:** Variant A (EOM3): in TLT for the returns of the last 3 trading days of each month. Variant B (second half): normalize each month to 21 trading days (day 1 = first, day 21 = last); in TLT for the returns of normalized days 11-21, out on days 1-10.
- **Data needs:** daily adjusted close TLT (and IEF/SHY optional) or index proxies; trading calendar to identify last trading days / normalized days
- **ETF-only start:** 2002 (TLT/IEF 07/2002); AS data from 1999
- **In plain English:** Long-term Treasury funds have tended to rise in the final days, and more broadly the second half, of each month. This calendar rule holds TLT only during those windows.
- **Rules:**
  1. Variant A: buy TLT at the close of the 4th-to-last trading day of the month; sell at the close of the last trading day; otherwise out of the market.
  2. Variant B: buy TLT at the close of normalized trading day 10; sell at the close of the last trading day (day 21); otherwise out of the market.
  3. The same rules can be applied to IEF or SHY (effect shrinks with duration).
- **Notes:** AS analysis is an observation, not a recommended standalone strategy; no transaction costs. Since ~2014 the positive bias shifted from day EOM-1 to EOM-2. AS's day-normalization method (mapping months to 21 days) is described only by reference to its FAQ - reproduce approximately (uncertain). Paper abstract (Sharpe ~1 for last-few-days long) verified via Capital Spectator summary; SSRN page itself blocked.

### 86. Sector Rotation with Fama-French Alphas (`as_sector_ff5_alpha`)

*Undisclosed (AS withheld the paper; rules are AS's modified version)*, family **momentum-rotation**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** Undisclosed paper (title withheld by AS) (None), None
- **AS page:** https://allocatesmartly.com/sector-rotation-fama-french-alphas/
- **Rebalance:** monthly, last trading day close
- **Universe:** risky ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY', 'XLRE']; defensive []; canary []; cash cash
- **Signal:** For each sector i: OLS over 36 month-end observations ending at month t-2 of (R_i - RF) = alpha_i + b1(Mkt-RF) + b2 SMB + b3 HML + b4 RMW + b5 CMA + e, using Fama-French 5-factor monthly data; SELECT if alpha_i > 0.
- **Data needs:** monthly adjusted closes of the sector SPDRs (or S&P 500 sector TR indices); Ken French data library: Fama/French 5 Factors (2x3), monthly, incl. RF
- **ETF-only start:** 1998 (original 9 SPDRs 12/1998; XLRE 10/2015)
- **In plain English:** Each month it estimates how much of each sector's recent 3-year performance cannot be explained by standard market factors, and holds equal amounts of every sector with a positive unexplained return.
- **Rules:**
  1. At the close on the last trading day of the month, for each sector ETF regress its monthly excess returns on the five Fama-French factors over the 36 months ending two months ago (skip the two most recent months for data-release delay).
  2. Select all sectors with a positive intercept (alpha).
  3. Equal-weight the selected sectors; hold until the next month-end.
  4. If no sector has positive alpha: not specified (cash assumed - uncertain).
- **Notes:** AS withheld the source paper and tested 'similar in spirit' rules; the 2-month skip is AS's change for real-world data delays. The exact 10 sectors are not listed: '10 S&P Sector SPDR ETFs' in 11/2017 likely means the nine originals plus XLRE (XLC launched 2018) - uncertain. AS concluded factor alphas have little predictive power for sectors and did not track it.

### 87. Utilities Beta Rotation (utilities vs market relative strength) (`bilello_gayed_utilities`)

*Charles Bilello and Michael Gayed (identification ours; AS withheld the paper title)*, family **momentum-rotation**, AS status **reviewed_not_tracked**, spec status **partial**.

- **Source:** An Intermarket Approach to Beta Rotation: The Strategy, Signal and Power of Utilities (2014 Charles H. Dow Award; identification not confirmed by AS) (2014), None
- **AS page:** https://allocatesmartly.com/beware-strategies-that-fall-down-on-good-data/
- **Rebalance:** weekly, close of the last trading day of the week
- **Universe:** risky ['VTI', 'XLU']; defensive []; canary []; cash None
- **Signal:** R4_X = P_X(t) / P_X(t - 4 weeks) - 1 on weekly closes; HOLD XLU if R4_XLU > R4_VTI else VTI
- **Data needs:** daily/weekly adjusted close XLU, VTI (or SPTRUTIL, RU30INTR/CRSPTMT); optional: Ken French industry and market returns for the original long test
- **ETF-only start:** 2001 (VTI 05/2001; XLU 12/1998); AS test from 10/1989 with index data
- **In plain English:** Each week it owns utility stocks if they have outperformed the overall market over the past four weeks (a sign of defensive positioning), otherwise it owns the whole market.
- **Rules:**
  1. At the close of each week compute the 4-week return of utilities (XLU) and of the total market (VTI).
  2. If utilities' 4-week return is greater, hold 100% XLU for the next week; otherwise hold 100% VTI.
  3. Repeat weekly.
- **Notes:** AS used this as a cautionary example: strong on Ken French data from 1926 but roughly market-like on tradeable index/ETF data since 1989, and would underperform after costs. AS test excluded transaction costs. Paper identity inferred from AS's description (Dow Award winner, 4-week utilities vs market) - not confirmed; source URL not retrieved.

### 88. Aggregate TAA Allocation as a Trading Signal (`as_agg_taa_allocation`)

*Allocate Smartly*, family **other**, AS status **reviewed_not_tracked**, spec status **undisclosed_or_placeholder**.

- **Source:** The Wisdom of 100 Strategies: Using Aggregate TAA Allocation as a Trading Signal (2026), https://allocatesmartly.com/the-wisdom-of-100-strategies-using-aggregate-taa-allocation-as-a-trading-signal/
- **AS page:** https://allocatesmartly.com/the-wisdom-of-100-strategies-using-aggregate-taa-allocation-as-a-trading-signal/
- **Rebalance:** monthly at month-end close (best after costs); AS also tested semi-monthly (normalized days 10 and 21), weekly (days 5/10/15/21) and daily, each with same-day or next-day (1-day lag) execution
- **Universe:** risky ['SPY', 'VNQ', 'IEFA', 'VNQI']; defensive ['IEF', 'LQD', 'BWX', 'GLD', 'PDBC']; canary []; cash cash
- **Signal:** AGG_a(t) = average across all strategies tracked by AS of each strategy's current weight in asset a (AS 'Aggregate Allocation Report'; strategy weighting presumably equal - uncertain).
- **Data needs:** daily allocations of every AS-tracked strategy (members-only on AS); can be approximated by running all tracked strategies in this catalog and averaging; daily adjusted closes for all category proxies
- **ETF-only start:** n/a (AS tests from 2000)
- **In plain English:** Averages what all the tactical strategies AllocateSmartly follows are currently holding and simply copies that average portfolio. It acts like one very diversified tactical portfolio.
- **Rules:**
  1. On each rebalance date, compute the aggregate allocation across all tracked TAA strategies (by individual ticker).
  2. Granularity options: (a) hold the aggregate weights by ticker; (b) roll up positions < 2% into generic asset classes; (c) map to categories: US equities SPY, US real estate VNQ, US gov bonds IEF, US non-gov bonds LQD, intl equities IEFA, intl real estate VNQI, intl bonds BWX, precious metals GLD, commodities PDBC, cash; currency/market-neutral categories held as cash; (d) risk on/off: equities + real estate + high-yield bonds -> SPY, everything else -> IEF (cash separate).
  3. Trade the resulting weights at the close (same day) or at the next day's close (realistic, since the report is generated overnight).
  4. Hold until the next rebalance date.
- **Notes:** NOT directly replicable: requires AS members-only aggregate data. Approximation requires implementing the full set of AS tracked strategies (which changed over time: 50+ in 2020, 100+ in 2026) and averaging; AS's averaging method (equal weight per strategy, handling of alternate trading days) is not stated. Earlier 2020 post (https://allocatesmartly.com/using-aggregate-taa-allocation-as-a-tool-for-timing-the-market/) tested the same idea with EFA/RWX/DBC proxies, without costs.

