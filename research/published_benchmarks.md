# Published performance benchmarks for checking the replication

Compiled 2026-11-20. The companion file `published_benchmarks.json` holds 89 records. Each record covers one source, one table or figure, and one period, and gives the exact URL, location, costs, proxies and a confidence label.

The aim is to check a monthly replication (Jan 2000 to Oct 2026) against **published** figures from the strategy authors or other public sources. No AllocateSmartly members content was used.

## How to read the JSON

- **`period.start`** is the first month whose return is included. For example, Keller's "Dec 12 – Dec 22" and TrendXplorer's "31-12-2012..31-12-2022" both become `2013-01`..`2022-12`.
- **`annual_returns`** holds calendar-year returns as decimals. Records that also carry full-sample `stats` keep only the 2000+ years in `annual_returns`; the stats apply to the full `period`.
- **`stats`** values are decimals and `max_dd` is negative. Extra keys appear only when the source names them explicitly:
  - `total_return` is a cumulative, non-annualised return over a short period (BAA Jan–Jun 2022).
  - `sortino` and `pct_time_invested` appear in the Philosophical Economics and ActuallyFinance records.
- **Confidence labels:**
  - `exact`: transcribed from a table, text or data blob.
  - `read-from-chart`: bar heights were pixel-measured, or SVG coordinates were decoded. Every such record states its estimated error and the consistency check that was done.
  - `second-hand`: the figure was quoted by a third party, such as a CXO Advisory reproduction of a paper table or a blog copy of someone else's data.
- **Sharpe definitions differ by source**, so compare Sharpe within a source, not across sources:
  - Keller papers and CXO: excess over T-bills.
  - TrendXplorer: CAGR / vol with rf = 0.
  - Faber: a fixed rf (4%, 5.41% or 6% depending on the version).
- **Costs differ by source:**
  - Keller papers: 0.1% one-way.
  - TrendXplorer: zero.
  - Faber and Antonacci: gross.
  - Philosophical Economics: 0.6% round-trip slip.

## Coverage summary (years 2000–2025)

| strategy_id | Calendar years, exact | Calendar years, read-from-chart | Calendar years, second-hand | # dated-period stat records |
|---|---|---|---|---|
| faber_gtaa5 | 2000–2012 (2013 paper; also the 2009 and 2007 vintages) | – | – | 6 (incl. 2006–2012 and 2006–2016 out-of-sample) |
| faber_gtaa5_buyhold | 2000–2012 | – | – | 5 |
| faber_gtaa_agg3 | 2000–2012 | – | – | 1 (1973–2012) |
| faber_gtaa_agg6 | 2000–2012 | – | – | 1 (1973–2012) |
| gem | **2000–2025** (compounded from Antonacci's monthly table) | – | – | 1 usable (1980–2018) |
| haa_balanced | 2022 | **2000–2022** | – | 9 (2001–22, 2003–22, 2013–22, 2018–22, 2020–22, 2022) |
| haa_simple | 2022 | **2000–2022** | – | 9 |
| baa_g12_balanced | 2022 | – | – | 6 (Jul02–Jun22, Jul12–Jun22, 2003–22, 2013–22, H1-2022) |
| baa_g4_aggressive | – | – | – | 3 (Jul02–Jun22, Jul12–Jun22, H1-2022) |
| daa_g12 | – | – | – | 3 (Jan94–Mar18, Apr08–Mar18 ×2, conflicting) |
| vaa_g4 | – | – | – | 2 (Apr08–Mar18; ~1994–2016, rounded) |
| paa2 | – | 2000–2015 (SHY/IEF variant) | – | 3 (1993–2015; Jul02–Jun22; Jul12–Jun22) |
| philoeconomics_growth_trend_timing | – | 2000–2025 (independent replication) | – | 3, plus exact post-2000 switch dates |
| philoeconomics_gtt_unemployment | 2016–2025 (crude blog) | 2000–2025 (independent replication) | – | 6 |
| browne_permanent_portfolio | **2000–2025** (Lazy Portfolio ETF); 2000–03 (Browne himself); 2021–25 (PortfoliosLab) | – | 2000–2008 (Crawling Road via blog) | 2 |
| portfoliocharts_golden_butterfly | **2000–2025** (Lazy); 2021–25 (PortfoliosLab); 6 years approx. (Optimized Portfolio) | – | – | 2 |
| dalio_all_weather | **2000–2025** (Lazy); 2021–25 (PortfoliosLab); 2008 (Robbins) | – | – | 3 |
| bench_spy | 2000–2025 (Damodaran; Slickcharts) | 2000–2025 (decoded, precision check only) | – | 2 (Keller SPY proxy) |
| bench_ief_rough_ust10y / bench_tbill_3m | 2000–2025 (Damodaran) | – | – | – |

Extra related records that help with debugging:
- `faber_sp500_10m_sma_timing`: Faber's S&P 10-month-SMA sleeve, yearly for 2006–2016.
- `faber_gtaa13`: the base 13-asset model behind the Agg variants.
- `philoeconomics_trend_only_10m_sma`: the trend leg alone, with exact switch dates.
- `bench_6040_spy_ief`: the 60/40 benchmark from the HAA paper.

## Findings by strategy

### 1. Faber GTAA (faber_gtaa5, faber_gtaa5_buyhold, faber_gtaa_agg3, faber_gtaa_agg6)

**Exact yearly returns, 2000–2012.** These come from the 2013 update of *A Quantitative Approach to Tactical Asset Allocation* (SSRN 962461, mirror at mebfaber.com):
- Figure 14 (p.32): timing model and equal-weight buy & hold.
- Figure 20 (p.52): GTAA 13 AGG Top 3 and Top 6.

**Earlier vintages.** The 2009 update (2000–2008, plus monthly returns) and the JWM 2007 paper (2000–2005) are also recorded. They differ from the 2013 figures by up to about 0.6pt a year, and 2008 is +1.59% in the 2009 version vs −0.59% in 2013. Expect the replication to match one vintage only roughly.

**After 2012 there are no author yearly figures.** What exists:
- JPM 2018 "Revisited" paper: 2006–2016 stats for the timing model (4.88% CAGR, 6.55% vol, −9.45% MaxDD) and buy & hold (3.51%).
- Faber's yearly S&P-sleeve timing returns for 2006–2016.
- Concretum Group (2026): an independent update to Mar 2025, 6.05% CAGR. It uses a 200-day SMA variant.

**Proxies (all indices, gross of costs):**
- GTAA-5: S&P 500 TR, MSCI EAFE TR, GFD US 10Y govt TR, GSCI TR, NAREIT TR, with 90-day T-bills as cash.
- Monthly signal and rebalance at the month-end close.

**Caveat for the Agg models.** They rank a **13-asset universe of French-Fama style indices**: LC/SC value, LC/SC momentum, EAFE, EEM, US 10Y, foreign 10Y, US corporates, US 30Y, GSCI, gold, NAREIT. They use the 1/3/6/12-month average return plus a 10-month SMA filter. An ETF-based replication will not match closely.

### 2. Antonacci GEM (gem)

**Exact monthly returns, 1950 to Sep 2026,** are on optimalmomentum.com's GEM page (table image; the Jan-2026 and Oct-2026 versions agree).

**Important:** the printed "GEM Ann" column is the **arithmetic sum of the monthly returns**, not the compounded return. For example, 2013 is printed as 27.7% but compounds to 31.1%. The JSON therefore holds the **compounded** calendar years (preferred record) as well as the printed column, which is flagged "do not compare directly".

I re-checked the compounding for all 26 years.

**Proxies:** S&P 500, MSCI ACWI ex-US (gross), Barclays US Agg, with a T-bill hurdle. Figures are gross of all costs.

The book's 1974–2013 yearly table is not public; only summary stats circulate second-hand.

### 3. Keller family

**HAA Balanced and HAA Simple: best coverage among the Keller strategies.**
- *SSRN 4346906 (v0.98, Mar 2023)*: Fig 6 (Balanced) and Fig 12 (Simple) give R, D, V and SR, after 0.1% one-way costs, for calendar 2022, 2013–2022 and 2003–2022. 2022: Balanced +2.7%, Simple −0.8%.
- *TrendXplorer (co-author Keuning's blog, Feb 2023)*: KPI tables before costs for 2001–22, 2003–22, 2013–22, 2018–22, 2020–22 and 2022. 2022: Balanced +3.67%, Simple −0.38%.
- Its annual-return bar charts (1971–2022) were pixel-measured to get **approximate yearly returns for 2000–2022**. Compounding the chart readings reproduces every KPI-table CAGR within 0.03pp, so the per-year error is about ±0.2pp.
- The paper and the blog differ by about 1pp in 2022. Zero costs explain only part of that, so the data vintage probably differs too.

**BAA Balanced (G12/T6) and BAA Aggressive (G4/T1).**
- *SSRN 4166845 (Jul 2022)*:
  - Figs 3 and 6 give RS (Jul 2002–Jun 2022) and IS2 (Jul 2012–Jun 2022).
  - YTD Jan–Jun 2022 was +6.4% for both. Both were fully defensive then, 33% DBC and 67% BIL.
  - Fig 12 gives Keller's SPY proxy for the same windows, useful as a data check.
- *HAA paper Fig 8*: BAA-Balanced extended to Dec 2022 (2022 +0.6%, 2013–22 7.1%, 2003–22 11.5%). There is no yearly table for BAA anywhere.

**DAA G12 (T6/B2): weak and internally inconsistent.**
- *TrendXplorer table "TC0" (no costs)*: Jan 1994–Mar 2018 R 14.1%, D −8.2%; Apr 2008–Mar 2018 R 11.1%, D −8.2%.
- *The paper's own table for Apr 2008–Mar 2018, reproduced by CXO Advisory*: R 9.9%, D −9.0%.
- The 1.2pp/yr gap is too large to come from costs alone. The SSRN PDF could not be obtained to resolve it (SSRN and ResearchGate return 403; the super.so mirror is 404).

**VAA G4 (T1/B1): weak.**
- *DAA paper via CXO*: Apr 2008–Mar 2018 R 10.5%, D −10.5%.
- *VAA paper OS via CXO's prose (rounded)*: about 16% CAGR, −10% MaxDD, Sharpe 0.92, for roughly Jan 1994–Dec 2016.
- TrendXplorer's VAA post has yearly bars only for the T2/B1 variant, so they were not used. Its full-sample table (Dec 1970–Jun 2017, T1/B1: 20.42%, 12.57% vol, −12.80%) is not in the JSON because it is not comparable.

**PAA2 (Top6, high protection).**
- *Paper OS table via CXO*: 1993–2015 R 10.5%, V 7.9%, D −8.8%, SR 1.00, IEF as safe asset, 0.1% costs.
- *TrendXplorer bars, read from chart*: 2000–2015 yearly returns. Compounding all 45 chart years gives 13.79% vs the published 13.78%. Caveat: this variant uses the best of SHY/IEF and zero costs.
- *BAA paper Fig 1*: a PAA-G12 re-run with BIL/IEF defensive for Jul 2002–Jun 2022 (8.9%) and Jul 2012–Jun 2022 (5.8%).

**Proxy conventions.** All Keller and TrendXplorer figures use ETF total returns, with index history before inception calibrated for ETF fees (PAA paper, Appendix A). Signals are taken at the month-end close and traded at that same close, with full monthly rebalancing.

### 4. Philosophical Economics GTT

**The author never published calendar-year returns.** What exists from the author:
- **Long-sample stats (exact):**
  - GTT with RRSG-or-IPG, Feb 1928–Nov 2015: 11.2% CAGR, 14.5% vol, −47.9% MaxDD.
  - GTT-UE, May 1930–Jan 2016: 10.8%, 14.0%, −51.3%.
  - GTT-UE, 1961–2016: 11.2%, −29.6%.
- **Exact post-2000 switch dates and index levels** for GTT and for the trend-only leg. GTT's exit → re-entry months, as printed: 2001.01→2001.02, 2001.03→2002.03, 2002.04→2002.07, 2002.11→2003.01, 2003.03→2003.04 and 2008.01→2009.07, with no trades from 2009.07 to 2015.11. These are the most useful check for a replication.
- **One near-2000s sub-period (retail-sales-only variant)**, roughly Jul 2002–Oct 2015: 10.6%, −17.3%. The dates were inferred from the chart axis.

**Conventions:** 1-month lag on economic data, revised data, 0.6% round-trip slip, S&P 500 TR vs its 10-month MA, T-bills as cash.

**Independent sources:**
- **ActuallyFinance Recession Timing Dashboard (live, snapshot 2026-11-20).**
  - Exact stats for Aug 1961–Oct 2026: GTT-UE 11.7% / 13.0% / −29.7%; GTT RRSG-or-IPG 11.7% / 12.9% / −30.7%.
  - 2000–2025 yearly returns **decoded from its SVG chart** (about ±0.35pp).
  - It uses real-time vintages where available.
- **CXO Advisory (Nov 2019)**, "Either" = GTT-UE on SPY, Nov 1993–Sep 2019: 12.3% CAGR, −15%. It is gross and assumes **no publication lag**.
- **Schwoerer Substack (Dec 2025)**: yearly GTT-UE returns for 2016–2025. The method is crude (summed partial years, 2025 only to November), but it gives the risk-off months: Jan and Nov 2023, Apr and May 2025.

The brief's date was off: the GTT post is dated 18 Jan 2016 and the unemployment follow-up 21 Feb 2016. No later author updates exist.

### 5. Permanent Portfolio, Golden Butterfly and All Weather

**Portfolio Charts cannot supply nominal yearly returns.** Every figure on the site is real (inflation-adjusted), the yearly bars are drawn client-side, there is no public API or download, and its own AI guide says not to estimate from the bars. Its pages give only 1970–2025 real summary stats, which are not comparable and are not in the JSON. Its definitions are still useful:

| Portfolio | Portfolio Charts allocation | US real summary stats, 1970–2025 |
|---|---|---|
| Permanent Portfolio | USA-LCB 25 / USA-LTT 25 / USA-BIL 25 / GLO-GLD 25 | 5.1% avg real, −19% deepest DD, 7.6% SD |
| Golden Butterfly | USA-LCB 20 / USA-SCV 20 / USA-LTT 20 / USA-STT 20 / GLO-GLD 20 | 6.3% avg real, −18%, 8.3% SD |
| All Seasons | 30 US large-cap blend / 40 LTT / 15 ITT / **8 gold / 7 commodities** | 5.3% avg real, −22%, 8.7% SD |

All three are rebalanced annually. Note that Portfolio Charts splits All Seasons 8/7, not 7.5/7.5.

**Nominal yearly returns used instead:**
- **Lazy Portfolio ETF (exact, 2000–2025, all three).** Monthly nominal returns are embedded in the page. They were compounded to calendar years, cross-checked against the page's own yearly output, and re-checked here from the saved monthly CSVs.
  - Rebalanced every 1 January; no fees or transaction costs.
  - Proxies: PP = VTI/TLT/BIL/GLD; GB = VTI/IJS/TLT/SHY/GLD; AW = VTI/TLT/**IEI (3–7y)**/DBC/GLD.
- **PortfoliosLab (2021–2025 public; real ETFs, net of expense ratios).** Its PP uses SHY as cash. Its GB rebalances **quarterly**. Its AW uses IEF.
- **Harry Browne's own published results (2000–2003).** His portfolio figures are not equal-weight averages of the asset returns, so the weights evidently drifted.
- **Craig Rowland / Crawling Road data via a 2009 blog (2000–2008, second-hand).** It uses 1–2y Treasuries as cash and rebalances annually.
- **Tony Robbins (1984–2013 summary).** 9.72% CAGR, 7.63% SD, 2008 −3.93%, net of fees. This conflicts with Lazy's 2008 figure of +2.38%.

### 6. Data sanity benchmarks

- **S&P 500**
  - *Damodaran histretSP (updated 5 Jan 2026), 2000–2025*: computed annually from index level plus dividends, so it differs slightly from monthly-reinvested TR (2008 −36.55%).
  - *Slickcharts S&P 500 TR, 2000–2025 (2008 −37.00%)*: an aggregator, not S&P DJI, but it matches the commonly cited official figures.
  - *S&P DJI itself*: returned HTTP 403 to automated download.
- **10-year Treasury (Damodaran)**: constant-maturity 10-year returns. Treat it as a rough IEF check only, since IEF has a shorter duration and fees.
- **3-month T-bill (Damodaran)**: the average rate over the year.
- **Keller's SPY proxy (BAA paper Fig 12)**: Jul 2002–Jun 2022 8.9% CAGR, −50.8% MaxDD.
- **60/40 SPY/IEF (HAA paper Fig 16)**: 2022 −14.5%, 2013–22 7.8%, 2003–22 7.4%.

## Could not access or find

- **SSRN direct downloads (Cloudflare 403)** for:
  - DAA 3212862, VAA 3002624, PAA 2759734;
  - Keller LAA, Antonacci 2042750, Faber 962461 (obtained from the mebfaber.com mirror instead).
- **ResearchGate DAA PDF**: 403. The super.so mirror is 404 and the Scribd VAA copy is a JavaScript shell.
- **No published yearly returns for:**
  - Faber GTAA after 2012 (author);
  - BAA, DAA, VAA-G4 (T1/B1) or PAA2 with IEF (author);
  - Philosophical Economics GTT (author);
  - Antonacci's book yearly table (not public).
- **Portfolio Charts nominal yearly returns**: not offered by the site. Robbins's All Seasons yearly table (1984–2013) has no public reproduction.
- **Official S&P DJI factsheets**: 403. PortfoliosLab before 2021 is paywalled.

## Raw evidence (scratchpad, not in the project)

`C:\Users\NORGAT~1\AppData\Local\Temp\claude\C--Users-Norgate-AB--claude-spares-spare-rIIaTa\0010a6b9-599f-434a-9f9f-fedda4ff6f69\scratchpad\`
- `bench_txt\`: layout text of the HAA and BAA papers.
- `bench_dl\web\img*`: TrendXplorer table and chart images.
- `bench_dl\cxo\img`: CXO table images.
- `bench_dl\agentA` (Faber/GEM), `agentB` (GTT), `agentC` (static portfolios, including monthly CSVs).
- `bench_scripts\`: pixel-reading and build scripts.
