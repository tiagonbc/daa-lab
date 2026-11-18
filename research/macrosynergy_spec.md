# Replication spec: Macrosynergy "Wealth management with macro factors" (Aug 2026), rebuilt with US public data

*Prepared 2026-11-18. Sources were read from the live post and its companion Jupyter notebook (HTML rendering on macrosynergy.com/academy). The Norgate and FRED facts below were checked against the local Norgate Data Updater and the FRED CSV endpoint on that date. Any item marked **[unverified]** or **[our design]** is either not stated by the source or is a choice made for this replication.*

---

## 1. Summary of the original

| Item | What the post and notebook do |
|---|---|
| Citation | Brine, E., Cereda, F. and Sueppel, R., "Wealth management with macro factors", Macrosynergy research, 22 Aug 2026. Post: https://macrosynergy.com/research/wealth-management-with-macro-factors/ ; notebook: https://macrosynergy.com/academy/notebooks/wealth-management-with-macro-factors/ |
| Question | How should a USD-based real-money investor (no leverage, long horizon) split wealth between cash and 11 risky asset classes when the split is guided by macro factors? |
| Universe | 11 risky classes plus USD cash (details in section 2.1). Returns are USD excess returns over short-term USD rates, built mostly from futures/forwards plus funding. |
| Signals | 35 point-in-time macro factors from JPMaQS. They are scored around a theoretically neutral level, grouped into themes, and the themes are averaged with equal weights per asset class (the post calls this "conceptual parity"). There is no optimisation. The result is one composite "macro support score" per asset class. |
| Weights | SoftMax of the 11 scores, with cash's score fixed at 0 and temperature 1. A positive score puts a class above cash, a negative score puts it below cash, and if every score is negative cash is the largest holding. |
| Rebalancing | Quarterly, using the latest month-end weights, with a 1-day execution lag. No transaction costs and no risk overlay ("naive PnL"). |
| Sample | Jan 2000 to Jul/Aug 2026 (320 traded months in the notebook output). |
| Headline (excess returns over USD cash) | **Macro weights:** 8.9% a year, 9.6% vol, Sharpe 0.92, Sortino 1.31. **Equal weights (1/12 each, cash included):** 4.8% a year, 7.6% vol, Sharpe 0.63, Sortino 0.89. The information ratio of macro minus equal is 0.80, and the rolling 5-year IR stayed positive throughout. Correlation with US equity excess returns is 0.41 for macro and 0.56 for equal. Peak-to-trough drawdown is −36.4% for macro and −33.0% for equal. |
| Headline (total returns, compounded) | 11.05% vs 6.93% a year. Cumulative returns exceed 1,500% for macro and are below 500% for equal (the post calls this "over three times as much"). Notebook IR: 0.81. |
| Predictive test | Panel of 11 classes: quarter-end score against next-quarter excess return. The post says the forward correlation is positive and "exceeds 20%", is highly significant (Macrosynergy panel test), and holds in both half-samples (split at 2013). It is significant for most classes individually. The exception is **industrial metals, which is not significant**. The exact panel coefficient is not printed in the text. |
| Self-declared caveats | Factor choice relies on theory, which brings implicit hindsight bias and also omitted-factor bias. The PnL is gross. A later article will apply sequential ML. |

**Reliance on JPMaQS point-in-time data:** all of it. Every macro factor is a JPMaQS "information state", meaning each date sees only the vintages published by then, so no publication-lag handling is needed in the notebook. Several JPMaQS series have no free equivalent: the "intuitive" GDP nowcasts, survey z-scores (MBCSCORE, CBCSCORE, MBISCORE, HHINFESCORE), the effective inflation target, model-based term premia on swaps, vol-targeted equity carry, LME inventory scores, LASSO fair-value EM spreads, and the FX tradeability blacklists. Returns also come from JPMaQS (futures, FX forwards, CDS indices, GBI-EM/EMBI).

---

## 2. Methodology detail

### 2.1 Asset classes (notebook code IDs)

| Code | Class | Return construction (paraphrased) |
|---|---|---|
| USEQ | US equity | S&P 500 future plus USD short rate |
| DXEQ | DM equity ex US | Equal-weight index futures of AUD, CAD, CHF, EUR, GBP, JPY, SEK, with local rate and FX vs USD |
| EMEQ | EM equity | Equal-weight futures of 12 EMs (China via Hang Seng), with local rate and FX |
| USDU | US Treasuries | Generic **5-year** UST, from the zero curve, rebalanced daily |
| DXDU | DM gov bonds ex US | Equal-weight 5y bonds in AUD, EUR (DE/FR/IT/ES market-value weights), GBP, JPY, NZD, with FX vs USD |
| DXFX | DM FX | Equal-weight long 9 DM currencies vs USD via 1m forwards (blacklist applied) |
| G2CR | DM corporate credit | CDX/iTraxx IG and HY CDS returns plus 5y govt bond return, plus EURUSD for the EU legs |
| EMCR | EM sovereign credit | Equal-weight EMBI country indices |
| EMLC | EM local bonds | Equal-weight GBI-EM country indices in USD (blacklist applied) |
| MTL | Industrial metals | Equal-weight front futures: aluminium, copper, lead, nickel, tin, zinc |
| GLD | Gold | COMEX gold future plus USD deposit rate |
| CASH | USD cash | Libor until 2021, then OIS |

The post reports annualised excess returns for 2000 to Jul 2026: gold 8.9% (highest), EM equity 8.2%, metals 7.8%, DM FX 0.2% (lowest), DM gov bonds 1.4%. Volatility ranged from 4.5% (UST) to 21% (metals).

### 2.2 Factor construction (paraphrasing the notebook)

1. **Raw factors.** Some are excess over a neutral benchmark:
   - XIP = IP %oya 3mma − long-term GDP trend (20-quarter moving median of real GDP %oya).
   - XRPCONS: same construction on real private consumption.
   - XEMPL = employment %oya 3mma − 5-year moving median of workforce growth.
   - XCPIB_PAR = average of {headline, core} × {%oya, 6m/6m saar} CPI − effective inflation target.
   - XHPI = house prices %oya 3mma − inflation target.
   - XINFE = 5y survey, bond-implied and model-implied inflation expectations, each − target.
   - XMONGROWTH = average of narrow and broad money %oya − target − GDP trend.
   - XEQCRR = vol-targeted (10%) real equity carry − 3 (a hurdle equal to a carry Sharpe of 0.3).
   - SPREADIFFRATIO = (EMBIG spread − LASSO fair value) / fair value.

   Others are levels or changes with an implicit neutral of zero: real rates, term premia, survey scores, carry, external balances, terms of trade.
2. **Geographic aggregation before scoring.** "GLB" aggregates are GDP-weighted, or weighted by industry value added for IP and manufacturing surveys. Local baskets are equal-weighted. FX blacklists are applied to FX and duration baskets.
3. **Composite sub-factors:**
   - LABTIGHT (US) = 0.5·z(XEMPL) − 0.25·z(Δ unemployment rate, oya, 3mma) − 0.25·z(unemployment rate 3mma vs its 5-year MA).
   - USDDIR (US) = mean of z(US − global real rates), z(US − global GDP trend), z(US basic balance % GDP).
4. **Scoring (`make_zn_scores`).** This step is applied to every factor, then again to every multi-factor theme, then again to every asset composite.
   - Score = (x − neutral) / MAD, with **neutral = 0**. MAD is the *mean absolute value* of x on an **expanding** window. It is not a standard deviation, and with neutral 0 it is just mean(|x|).
   - The estimates are re-done **monthly** (`est_freq="M"`), need at least **5×261 daily observations** (`min_obs`), and use each series alone (`pan_weight=0`).
   - Scores are **winsorised at ±3**.
   - Package default `iis=True` back-fills the period before the first estimate with that first in-sample estimate. Because the download starts on 2000-01-01, the scaling for roughly 2000–2004 is in-sample. **[inferred from code defaults; mild look-ahead in scale only, not in sign]**
   - Every score also exists in a negated version ("_ZNN").
5. **Themes.** These are linear composites of factor scores, re-scored as above. Weights are renormalised over available components (`complete_xcats=False`). Themes that use US data:

| Theme | Definition (weights) |
|---|---|
| USD_PRODGROWTH | ½ INTRGDPv5Y + ½ XIP |
| USD_FINEASE | ⅓ XMONGROWTH + ⅓ (−RIRY) + ⅓ (−term premium DU05YETP) |
| USD_ECONSTR | ⅓ LABTIGHT + ⅓ XIP + ⅓ INTRGDPv5Y |
| USD_INFLPRESS | ½ XCPIB_PAR + ½ HHINFESCORE |
| USD_FIPREMIA | ½ DU05YETP + ½ RIRY |
| USD_WEAK | ⅓ (−LABTIGHT) + ⅓ (−XRPCONS) + ⅓ (−XCPIB_PAR) |
| USD_LABTIGHTNESS / USD_CPI / USD_HOUSING / USD_REALRATES / USD_TERMPREM / USD_MONGROWTH / USD_EQCARRY / USDDIR | Single factor: LABTIGHT / XCPIB_PAR / XHPI / RIRY / DU05YETP / XMONGROWTH / XEQCRR / USDDIR |
| GLB_CYCLE | ⅕ each: global mfg confidence level, its 3m/3m change, −(inventory survey 3m/3m change), global XIP, global XRPCONS |
| GLB_MFG | ½ mfg confidence level + ½ its change |
| GLB_BUSCONF | ½ Δ mfg confidence + ½ Δ construction confidence |
| GLB_CONSTR | ½ Δ construction confidence + ½ XHPI (EUR, USD average) |
| GLB_REALRATES / GLB_MONGROWTH / GLB_INVCYCLE / GLB_EQCARRY | Global RIRY / XMONGROWTH / Δ inventory survey / XEQCRR |

RIRY is the average of the real short rate (RIR) and the real 5y swap yield.

6. **Asset composites.** Equal-weight average of the signed themes below (+ means the theme as defined, − means negated), then re-scored to give S_a:

| Asset | Themes (sign) |
|---|---|
| USEQ | +USD_PRODGROWTH, +USD_FINEASE, −USD_LABTIGHTNESS, −USD_INFLPRESS, +GLB_CYCLE |
| DXEQ | +DXEQ_DEMAND, −DXEQ_INFL, −DX_TERMPREM, +GLB_CYCLE, −GLB_REALRATES, +DXEQ_TOT, −USDDIR |
| EMEQ | +EMEQ_EXTBAL, +EMEQ_MONEY, +EMEQ_TOT, −EMCR_XSPREAD, −GLB_INVCYCLE, −USDDIR |
| USDU | +USD_FIPREMIA, −USD_CPI, −USD_HOUSING, −GLB_CYCLE |
| DXDU | +DXDU_XBAL, −DXDU_LOCALHEAT, −DXMON, +DX_TERMPREM, −GLB_CYCLE, −USDDIR, +DMFX_RELIP, +DX_FISCAL, +DMFX_CARRY, +USD_WEAK |
| DXFX | +DMFX_RELIP, +DX_FISCAL, +DMFX_CARRY, +USD_WEAK |
| G2CR | +G2_TERMPREM, −USD_CPI, −USD_HOUSING, −GLB_CYCLE, −USDDIR, +DMCR_CARRY, +USD_ECONSTR, −GLB_INVCYCLE, −GLB_REALRATES |
| EMCR | +USD_TERMPREM, +USD_REALRATES, −GLB_CYCLE, +EMCR_NIIP, +EMCR_XSPREAD, +GLB_CONSTR, −GDM_XINFE, −GLB_INVCYCLE |
| EMLC | +EMCR_XSPREAD, +EMCR_NIIP, +EMFX_CARRY, +EMFX_TOT, +EMLC_REERAPPR, −EMLC_INFL, +EMLC_REALRATES, −USD_LABTIGHTNESS, +GLB_MONGROWTH |
| MTL | +GLB_MFG, +MTL_CARRY, +MTL_INVSHORT, −EMCR_XSPREAD, −GLB_REALRATES |
| GLD | −GLB_BUSCONF, −GLB_EQCARRY, −USD_MONGROWTH, −USD_CPI |

*Inconsistency noted:* the notebook's scorecard labels include equity-carry themes for USEQ, DXEQ and EMEQ, but the composites do **not** use them. The post's prose matches the composites.

7. **Weights.** w_i,t = exp(S_i,t) / [Σ_j exp(S_j,t) + exp(0)]. Cash gets exp(0)/(...). The temperature is 1, and there are no caps.
8. **PnL.** NaivePnL with `sig_op="raw"` (position = weight), `rebal_freq="quarterly"`, `rebal_slip=1`, no vol-scaling, no costs. Positions are held at constant notional within each quarter and PnL is not compounded. The total-return run compounds daily. The benchmark is 1/12 in each of the 12 buckets.
9. **Evaluation.** `CategoryRelations` at quarterly frequency (score = last value of the quarter, return = sum over the next quarter), panel test "map", half-sample split at 2013. PnL statistics: return, SD, Sharpe, Sortino, max 21-day, 6-month and peak-to-trough drawdowns, top-5% monthly PnL share, correlation with USEQ, IR vs equal weights, rolling 5-year IR, yearly attribution.

The latest notebook weights are a useful sanity reference, not something to match. On 2026-07-31: USEQ 1.8%, DXEQ 14.4%, EMEQ 19.9%, USDU 6.0%, DXDU 7.1%, DXFX 5.6%, G2CR 3.0%, EMCR 2.1%, EMLC 6.7%, MTL 19.1%, GLD 5.7%, CASH 8.6%.

---

## 3. Data mapping

### 3.1 Norgate "Economic" database: what the symbols are

**Suffix convention.** This is read from the security names returned by the local NDU via `norgatedata.security_name`. No public documentation of it was found on norgatedata.com:

| Suffix | Meaning (from Norgate security names) |
|---|---|
| none | Level |
| 1 | Net change vs previous period |
| 2 | % change vs previous period |
| 3 | % change vs 12 months previous (YoY, also for quarterly series) |
| 4 | Annualised rate (e.g., GDP q/q SAAR %) |

Not every series has every suffix: #CPISA has 2 and 3 only, and #NFCI and #CFNAI have none. There are two labelling quirks:
- **#INDSA2** is labelled "Net Change", but its values are % change. Oct-2026 −0.43 = 103.3954 / 103.8458 − 1.
- **#UNEMP3** ("SAYR") is the % change of the *rate* vs 12 months ago (Sep-2026 −4.55 = 4.2/4.4 − 1), **not** a change in percentage points. Compute pp changes from #UNEMP yourself.

**Dating: by reference period, not release date (verified empirically).** Norgate repeats each observation on **every trading day of its reference period**:
- Oct-2026 CPI (released mid-Nov) sits on the 1–30 Oct bars.
- Q3-2026 GDP sits on every day from 1 Jul to 30 Sep.
- Weekly claims for the week ending Sat 7 Nov sit on the 2–6 Nov bars, although they were released 12 Nov.
- NFCI for the week ending Fri 6 Nov sits on that week's bars.

A naive as-of lookup therefore **looks ahead** by the whole publication lag plus up to one reference period. Norgate's content page also says its updates include revisions and that the whole series is refreshed. The data is **latest-vintage only, with no point-in-time history**. The project's `daalab/data/sources.py::norgate_econ` docstring already says the dating is by reference period, which agrees with this.

**Norgate to FRED equivalence.** Each pair below was checked by matching the latest values on 2026-11-18:

| Norgate | Series | FRED ID | Freq | Norgate start | Typical US release lag (use with caution; prefer ALFRED vintage dates) |
|---|---|---|---|---|---|
| #CPISA / #CPIXSA | CPI-U SA / core CPI SA | CPIAUCSL / CPILFESL | M | 1947 / 1957 | ~10–15 days after month end → usable at end of m+1 |
| #CPIUN / #CPIXUN | CPI NSA / core NSA | CPIAUCNS / CPILFENS | M | 1913 / 1957 | same |
| #CPICH / #CPIXCH | Chained CPI / chained core | SUUR0000SA0 / SUUR0000SA0L1E | M | 1999-12 | same (subject to later revision) |
| #PPISA / #PPIXSA | PPI finished goods SA / ex food & energy | WPSFD49207 / WPSFD4131 | M | 1947 / 1974 | ~mid m+1 |
| #INDSA | Industrial production | INDPRO | M | 1919 | ~15–17th of m+1 |
| #NFPAY | Nonfarm payrolls | PAYEMS | M | 1939 | first Friday of m+1 |
| #UNEMP | Unemployment rate | UNRATE | M | 1948 | first Friday of m+1 |
| (none) | Civilian labour force | CLF16OV | M | – | first Friday of m+1 |
| #INJOB | Initial claims (week ending Sat) | ICSA | W | 1967 | Thursday after week end (+5 days) |
| #GDPSA | **Real** GDP (chained $) | GDPC1 | Q | 1947 | advance ~4 weeks after quarter end; revised at +2 and +3 months and annually |
| #PCESA | **Real** PCE, quarterly | PCECC96 (monthly: DPCERA3M086SBEA from 1959; PCEC96 from 2007) | Q | 1947 | quarterly with GDP; monthly ~end of m+1 |
| #RETSA / #RETXSA | Retail & food services / retail ex food services | RSAFS / RSXFS (real: RRSFS) | M | 1992 | ~mid m+1 |
| #DURSA | Durable goods orders | DGORDER | M | 1992 | ~25th of m+1 |
| #HOSSA / #HOCSA | Housing starts / completions | HOUST / COMPUTSA (permits: PERMIT) | M | 1959 / 1968 | ~17–19th of m+1 |
| #LVSAAT | Light vehicle sales SAAR | ALTSALES | M | 1976 | first days of m+1 |
| #M1FED / #M2FED | M1 / M2 | M1SL / M2SL | M | 1959 | 4th Tuesday of m+1 (H.6) |
| #TCSSA | Construction spending | TTLCONS | M | 1993 | first business day of m+2 |
| #BOPSA | Trade balance (goods & services) | BOPGSTB | M | 1992 | ~5 weeks |
| #CURSA | Current account | IEABC | Q | 1999 | ~11–12 weeks |
| #CO$SA | Corporate profits (named "before tax"; values equal **CPROFIT**, i.e., with IVA & CCAdj) | CPROFIT (ex-adj: A053RC1Q027SBEA) | Q | 1947 | ~2 months |
| #HOMPR | Existing-home median price | HOSMEDUSM052N (**FRED keeps only ~13 months**) | M | 1999 | ~3–4 weeks |
| #SPCS20 | Case-Shiller 20-city **SA** | SPCS20RSA (national: CSUSHPISA, 1987+) | M | 2000 | last Tuesday of m+2 |
| #CFNAI | Chicago Fed National Activity Index | CFNAI (3-mo avg: CFNAIMA3) | M | 1967 | ~3–4 weeks; revised monthly |
| #NFCI, #NFCIC, #NFCIL, #NFCIR | NFCI and its credit, leverage and risk subindices | NFCI, NFCICREDIT, NFCILEVERAGE, NFCIRISK (adjusted: ANFCI) | W (Fri) | 1971 | Wednesday after week end; **whole history re-estimated weekly** |
| #NAPMI | ISM manufacturing PMI | **not on FRED** (removed for licensing; NAPM returns 404). Proxies: Philly Fed GACDFSA066MSFRBPHI (1968+), Empire GACDISA066MSFRBNY (2001+) | M | 1948 | first business day of m+1 (Philly/Empire: within the same month) |
| #US10Y-2Y | 10y − 2y | T10Y2Y | D | 1976 | T+1 |
| %3MTCM %1YTCM %2YTCM %5YTCM %10YTCM %30YTCM | CMT yields | DGS3MO DGS1 DGS2 DGS5 DGS10 DGS30 | D | 1981 / 1962 / 1976 / 1962 / 1962 / 1977 | T+1 |
| %FFYE | Effective fed funds | DFF (monthly FEDFUNDS) | D | 1954 | T+1 |
| %30MTG | 30y mortgage (Freddie Mac) | MORTGAGE30US | W | 1971 | Thursday |
| %COAAA / %COBAA | Moody's Aaa / Baa yields | DAAA / DBAA (Baa − 10y: BAA10Y) | D | 1983 / 1986 | T+1 |
| %CCCHYS | ICE BofA **CCC & lower** HY OAS | BAMLH0A3HYC (**FRED keeps only 3 years**, 2023-11 onward; same for BAMLH0A0HYM2 and BAMLC0A0CM) | D | 1996-12 | T+1 |
| %USPRIME | Prime rate | DPRIME | D | 1955 | – |
| $MOVE | MOVE index | – | D | 2002-11 | T+0 |
| $IDCOT1TR, 3TR, 7TR, 10TR, 20TR, $IDCOTSTR, $IDCOTCTR, $ICET25TR | ICE US Treasury TR (1–3, 3–7, 7–10, 10–20, 20+, 0–1, core, 25+) | – | D | 2004-12-31 (10TR, STR, CTR: 2005-12; 25TR: 2006) | T+0 |
| $USBIG / $USBIGCORP / $SP5IGBIT | FTSE US BIG, BIG corporate, S&P 500 IG corporate TR | – | D | 1994-12-30 | T+0 |

**Staleness and gaps found on 2026-11-18:**
- #NAPMI's last bar is 2026-08-31 (Sep and Oct missing).
- #HOSSA's last bar is Sep, while FRED already has Oct.
- The **Oct-2025 CPI and household-survey data do not exist**. This is the 2025 government shutdown. FRED shows blanks for CPIAUCSL, CPILFESL, UNRATE and CLF16OV. Norgate has **no October-2025 bars** for #CPISA, and its YoY series (#CPISA3, #UNEMP3) end at Sep-2026 because the Oct-2026 YoY cannot be computed. Pipelines must handle that NaN, for example by geometric interpolation of the level for YoY and 6m/6m maths, with a flag.

### 3.2 FRED / ALFRED usage

- **Latest vintage:** `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>`, which is what `daalab.data.sources.fred` uses. In this session plain `curl` to fredgraph hung intermittently, while one IPv4 request and requests from a browser context succeeded. If it hangs, add timeouts and retries.
- **Vintages (point-in-time):** the `fredgraph.csv` vintage parameters were **ignored** in a test on 2026-11-18, and so was `alfredgraph.csv?id=X_YYYYMMDD`. Use the FRED API, which needs a free key:
  - `fred/series/observations?series_id=X&realtime_start=1776-07-04&realtime_end=9999-12-31` returns every vintage. Each observation carries realtime_start and realtime_end, so the as-of value at date t is the one where realtime_start ≤ t < realtime_end. `output_type=4` returns first releases only.
  - `fred/series/vintagedates?series_id=X` returns the **actual release dates**. Use these to model publication lags exactly even if you keep revised values. **[API parameter names from documentation knowledge; not exercised in this session]**
  - Vintage history usually starts years after the data itself, often 1990s–2000s and series-dependent. Check per series before relying on it.
- **Fallback lag rule when vintages are not used:** at month-end decision date t, a monthly series may use reference month m only if m ≤ month(t) − L, where:
  - L = 1 for CPI, PPI, payrolls, unemployment, labour force, IP, ISM, retail sales, housing starts and permits, M2, CFNAI, MICH.
  - L = 2 for monthly real PCE, Case-Shiller, inventories/sales ratios, construction spending.
  - Quarterly GDP is used from the end of the **second** month after quarter end.
  - Weekly NFCI and claims: +5 calendar days after week end.
  - Daily market data: T−1 close.
  - Cleveland Fed EXPINF* for month m is published around mid-m, so it is usable at the end of m. **[release timing from experience; verify with vintagedates]**

### 3.3 Mapping the 35 factors in Annex 1 to US substitutes

✔ = good substitute, ≈ = approximate, ✘ = not replicable with US-only Norgate/FRED data (needs JPMaQS, OECD/IMF or paid data).

| # | JPMaQS factor (ticker) | Used by | US substitute (Norgate / FRED) | Status |
|---|---|---|---|---|
| 1 | Excess GDP growth trend INTRGDPv5Y (US, GLB) | USEQ, G2CR (via ECONSTR) | US: **CFNAI 3-mo avg** (#CFNAI → 3mma; FRED CFNAIMA3), where 0 = trend growth. Alternative: GDPC1 %oya − 20Q moving median of the same (#GDPSA3). GLB: ✘ | ≈ (US), ✘ (GLB) |
| 2 | Relative GDP growth vs US | EMLC/EMFX | – | ✘ |
| 3 | Relative IP growth vs US (6m/6m) | DXFX, DXDU | – | ✘ |
| 4 | Excess IP growth XIP | USEQ, G2CR, GLB_CYCLE | INDPRO %oya 3mma − TREND (#INDSA3 or INDPRO; TREND from GDPC1 / #GDPSA3) | ✔ US / ≈ as GLB |
| 5 | Excess private consumption XRPCONS | USD_WEAK, GLB_CYCLE | DPCERA3M086SBEA %oya 3mma − TREND (monthly), or #PCESA3 quarterly | ✔ US |
| 6 | US relative growth (US − global) | USDDIR | – | ✘ |
| 7 | Excess employment growth XEMPL | LABTIGHT | PAYEMS (#NFPAY3) %oya 3mma − 60-month median of CLF16OV %oya | ✔ |
| 8 | Unemployment rate change (neg.) | LABTIGHT | UNRATE (#UNEMP) 3mma − same 12 months earlier (pp) | ✔ |
| 9 | Unemployment rate vs 5y MA (neg.) | LABTIGHT | UNRATE 3mma − 60-month mean of UNRATE | ✔ |
| 10 | Manufacturing confidence level and 3m/3m change | GLB_CYCLE, GLB_MFG, GLB_BUSCONF | ISM PMI (#NAPMI) − 50 as 3mma, and 3mma(t) − 3mma(t−3). Fallback: Philly Fed GACDFSA066MSFRBPHI (0-neutral diffusion index) | ≈ (US proxy for global) |
| 11 | Inventory survey change (neg.) | GLB_CYCLE, GLB_INVCYCLE | ΔMNFCTRIRSA (manufacturers' inventories/sales), 3mma 3m/3m change; ISRATIO as an alternative | ≈ (hard data, longer lag) |
| 12 | Construction confidence change | GLB_BUSCONF, GLB_CONSTR | PERMIT (or #HOSSA/HOUST) 3mma, % change 3m/3m | ≈ |
| 13 | Excess CPI XCPIB_PAR | USEQ, USDU, G2CR, GLD | Mean of CPIAUCSL and CPILFESL %oya and 6m/6m saar, − 2.0 (#CPISA, #CPIXSA) | ✔ (JPMaQS also jump-adjusts) |
| 14 | Excess inflation expectations XINFE (DM) | EMCR | US only: mean(EXPINF5YR − 2, T5YIE − 2 [2003+]) | ≈ |
| 15 | Household inflation expectations score | USEQ (INFLPRESS) | MICH (UMich 1y) − its trailing 120-month median | ≈ **[our design]** |
| 16 | Excess house price growth XHPI | USDU, G2CR | CSUSHPISA %oya 3mma − 2 (#SPCS203 from 2001 as alternative) | ✔ |
| 17 | Real rates RIRY | USEQ (−), USDU (+), G2CR/MTL/DXEQ (−, as GLB) | ½[(DGS3MO or %3MTCM) − EXPINF1YR] + ½[(DGS5 or %5YTCM) − EXPINF5YR]. Check: DFII5 (2003+) | ✔ US / ≈ GLB |
| 18 | US − global real rates | USDDIR | – | ✘ |
| 19 | 5y term premium DU05YETP | USEQ (−), USDU (+), G2CR (+), EMCR | **THREEFYTP5** (Kim-Wright 5y, 1990+). Alternative: NY Fed ACM ACMTP05 (not on FRED) | ✔ (Treasury rather than swap TP) |
| 20 | Excess equity carry XEQCRR_VT10 − 3 | GLD (−) | ((100/CAPE) − RIR) × 10/σ₆₃d(SPX) − 3, with CAPE from Shiller's free ie_data | ≈ **[our design]** |
| 21 | Excess narrow money | FINEASE, GLD | M1SL %oya − 2 − TREND. **M1 has a definitional break in May 2020** (savings deposits added), so exclude M1 or splice it | ≈ |
| 22 | Excess broad money | FINEASE, GLD | M2SL (#M2FED3) %oya − 2 − TREND | ✔ |
| 23 | Fiscal thrust | DXDU, DXFX, G2CR(EU) | US-only proxy: Δ12m of MTSDS133FMS 12m-sum / nominal GDP | ≈ (not needed for the US core) |
| 24 | External balance ratio | EMEQ | – | ✘ |
| 25 | US basic balance | USDDIR | IEABC / GDP (FDI leg missing) | ≈ (not used) |
| 26 | Trade balance trend | DXEQ, DXDU | – | ✘ |
| 27 | NIIP strength | EMEQ, EMCR, EMLC | – | ✘ |
| 28 | Commodity terms of trade | DXEQ, EMEQ, EMLC | – | ✘ |
| 29 | Macro terms of trade | same | – | ✘ |
| 30 | Openness-adjusted REER appreciation | EMLC | – | ✘ |
| 31 | Real FX forward carry | DXFX, EMLC | – | ✘ |
| 32 | Metals futures carry COCRR | MTL | From Norgate continuous futures, front vs next contract **[not checked]** | ≈ / ✘ |
| 33 | CDS index carry CRCRY | G2CR | Spread level: BAA10Y (or %COBAA − %10YTCM, 1986+) and %CCCHYS (1996+). The full ICE OAS history is only in Norgate | ≈ |
| 34 | LME inventory score (neg.) | MTL | – | ✘ |
| 35 | EMBI spread vs LASSO fair value | EMEQ, EMCR, EMLC, MTL | – | ✘ |

**Conclusion.** A faithful US replication is possible for **USEQ, USDU, GLD and US credit** (most of G2CR). That covers 4 of the 11 risky classes. Their themes use only factors 1, 4, 5, 7–17, 19–22 and 33. The DM ex-US and EM classes cannot be replicated faithfully without non-US macro data. Metals are only partly replicable, and the post found them insignificant anyway.

### 3.4 Investable return series (Norgate)

| Bucket | ETF (Norgate start) | Back-fill before the ETF |
|---|---|---|
| US equity | SPY (1993-01) | $SPXTR (1988) |
| US Treasuries, 5y (faithful) | IEI (2007-01) | $IDCOT3TR (2004-12-31), then a synthetic 5y par bond from %5YTCM/DGS5 (`bond_tr_from_yield`) |
| US Treasuries, 7–10y (user's example) | IEF (2002-07) | $IDCOT7TR (2004-12), then synthetic 10y |
| US IG credit | LQD (2002-07) | $USBIGCORP or $SP5IGBIT (1994-12) |
| US HY (optional) | HYG (2007-04), JNK (2007-12) | none in Norgate before 2007 |
| Gold | GLD (2004-11), IAU (2005-01) | $BCOMPR (precious metals sub-index, 1991, excess return so add cash; includes silver) or the project's `gold_monthly` |
| Cash | BIL (2007-05), SHV (2007-01) | %3MTCM/DGS3MO (`cash_tr_from_yield`), or $IDCOTSTR (2005-12) |
| Optional extensions | TIP (2003-12), DBC (2006-02), DBB (2007-01), EFA (2001-08), EEM (2003-04), EMB (2007-12), BWX (2007-10) | $BCOMTR (1991), $BCOMIN (1991) |

---

## 4. Replication spec (formulas)

### 4.0 Common engine (used by Variants A and B)

**Timeline.** Decisions are made at each month-end business day t, and each series is read as-of t. Without vintages, apply the lag rule in section 3.2. With ALFRED, take the value whose realtime window contains t.

**Transforms** (X is a monthly level, m a reference month):
- `yoy(X)_m = 100·(X_m / X_{m−12} − 1)`
- `ma3(Y)_m = mean(Y_m, Y_{m−1}, Y_{m−2})`
- `saar6(X)_m = 100·[(ΣX_{m..m−5} / ΣX_{m−6..m−11})² − 1]` (6m/6m, annualised)
- `TREND_t` = median of the last 20 published quarterly values of yoy(GDPC1)
- `TARGET = 2.0` (Fed objective). **Parameter:** the original uses JPMaQS's effective target. CPI historically runs about 0.3–0.5 pp above PCE, so test 2.0 and 2.4. **[our parameter]**

**Factors (US).**
| Name | Formula |
|---|---|
| GROWTH_NOW | ma3(CFNAI) |
| XIP | ma3(yoy(INDPRO)) − TREND |
| XRPCONS | ma3(yoy(DPCERA3M086SBEA)) − TREND |
| XEMPL | ma3(yoy(PAYEMS)) − median₆₀ₘ(yoy(CLF16OV)) |
| DU | ma3(UNRATE)_m − ma3(UNRATE)_{m−12} |
| UGAP | ma3(UNRATE)_m − mean₆₀ₘ(UNRATE) |
| LABTIGHT | 0.5·z(XEMPL) − 0.25·z(DU) − 0.25·z(UGAP) |
| XCPI | mean[yoy(CPIAUCSL), yoy(CPILFESL), saar6(CPIAUCSL), saar6(CPILFESL)] − TARGET |
| XHH | MICH − median₁₂₀ₘ(MICH) |
| XHPI | ma3(yoy(CSUSHPISA)) − TARGET |
| RIRY | ½(DGS3MO − EXPINF1YR) + ½(DGS5 − EXPINF5YR), using month-end yields |
| TP5 | THREEFYTP5 (month-end) |
| XMON | yoy(M2SL) − TARGET − TREND (M1 excluded because of the May-2020 break) |
| MFG_LVL | ma3(ISM PMI) − 50 |
| MFG_CHG | ma3(PMI)_m − ma3(PMI)_{m−3} |
| INV_CHG | ma3(MNFCTRIRSA)_m − ma3(MNFCTRIRSA)_{m−3} |
| CONSTR_CHG | 100·(ma3(PERMIT)_m / ma3(PERMIT)_{m−3} − 1) |
| CRCARRY | ½·z(BAA10Y) + ½·z(CCC OAS %CCCHYS). Neutral 0 as in the original, so this theme is **structurally positive** (see caveats) |
| EQCARRY | as in section 3.3 row 20 |

**Score operator** `zn(x)_t = clip(x_t / MAD_t, −3, 3)`:
- `MAD_t = mean_{s ≤ t*}|x_s|` over all month-end observations up to the last re-estimation date t* (monthly, so t* = t).
- Require at least 60 monthly observations, otherwise NaN. Optional flag `iis=True` back-fills with the first estimate, to mimic the notebook.
- Start MAD accumulation at each series' first available date. That is the 1960s–1990s for most inputs, so the strict version still has scores from 2000.

**Themes** (each is re-scored with `zn` if it has more than one component; weights are renormalised over available components):
| Theme | Definition |
|---|---|
| PRODGROWTH | ½ zn(GROWTH_NOW) + ½ zn(XIP) |
| FINEASE | ⅓ zn(XMON) − ⅓ zn(RIRY) − ⅓ zn(TP5). Optional `use_nfci`: add −zn(NFCI) as a 4th leg **[extension, not in the original]** |
| LABT | zn(LABTIGHT) |
| INFLPRESS | ½ zn(XCPI) + ½ zn(XHH) |
| CPI | zn(XCPI) |
| HOUSING | zn(XHPI) |
| FIPREMIA | ½ zn(TP5) + ½ zn(RIRY) |
| ECONSTR | ⅓ zn(LABTIGHT) + ⅓ zn(XIP) + ⅓ zn(GROWTH_NOW) |
| CYCLE (US proxy for GLB_CYCLE) | ⅓ zn(MFG_LVL) + ⅓ zn(MFG_CHG) − ⅓ zn(INV_CHG). Default is survey-only, to avoid double-counting XIP, which already sits in PRODGROWTH. Option `cycle_mode="faithful5"` adds zn(XIP) and zn(XRPCONS) at ⅕ each **[documented deviation]** |
| BUSCONF | ½ zn(MFG_CHG) + ½ zn(CONSTR_CHG) |
| INVCYCLE | zn(INV_CHG) |
| REALRATES | zn(RIRY) |
| TERMPREM | zn(TP5) |
| MONGROWTH | zn(XMON) |
| EQCARRY | zn(EQCARRY) |
| CRCARRY | zn(CRCARRY) |

**Asset composites** (equal-weight mean of the signed themes, then re-scored with `zn`):
- `S_EQ  = zn(mean[+PRODGROWTH, +FINEASE, −LABT, −INFLPRESS, +CYCLE])`. This is the user's growth / financial conditions / labour slack / inflation set.
- `S_UST = zn(mean[+FIPREMIA, −CPI, −HOUSING, −CYCLE])`. This is the real-rate and term-premium set.
- `S_CR  = zn(mean[+TERMPREM, −CPI, −HOUSING, −CYCLE, +CRCARRY, +ECONSTR, −INVCYCLE, −REALRATES])`. This is G2CR without USDDIR, which belonged to the EURUSD leg.
- `S_GLD = zn(mean[−BUSCONF, −EQCARRY, −MONGROWTH, −CPI])`
- `S_CASH = 0`

### 4.1 Variant A: "MS-US5", the faithful softmax on 4 US risky classes plus cash

- **Universe:** SPY, IEI (or IEF), LQD, GLD, BIL (with back-fills from section 3.4).
- **Weights:** `w_i = exp(S_i/τ) / Σ_j exp(S_j/τ)` over i ∈ {EQ, UST, CR, GLD, CASH}, with τ = 1 and no caps (faithful).
- **Rebalance:** compute weights at each quarter-end business day (Mar, Jun, Sep, Dec) and trade at the next day's close (1-day slip).
  - *Faithful PnL:* constant weights within the quarter, r_p = Σ w_i·r_i daily, no compounding (NaivePnL convention).
  - *Implementable PnL:* buy and hold within the quarter, so weights drift.
- **Costs [our assumption]:** 5 bp per side on traded notional. Report gross, 5 bp and 20 bp.
- **Benchmark:** equal weights, 1/5 each (cash included), rebalanced quarterly. Same construction as the post.
- **Sample:** signals from 1995 where data allow, and the headline window 2000-01 to the latest month, to compare with the post.
- **Metrics:**
  - Annualised excess return over cash, SD, Sharpe, Sortino.
  - Max drawdowns (21-day, 6-month, peak-to-trough).
  - IR vs equal weights ((mean daily active / SD) × √252) and rolling 5-year IR.
  - Correlation with SPY, yearly active returns.
  - Pooled panel (4 assets) Pearson and Kendall correlation of quarter-end S_i vs next-quarter excess return, sign accuracy and balanced accuracy, all with a 2013 split.
  - Per-asset predictive regressions.

**Worked example of the weights.** With S = (EQ +1, UST 0, CR −0.5, GLD +0.5, cash 0), the exponentials are (2.718, 1, 0.607, 1.649, 1), summing to 6.974. The weights are 39.0%, 14.3%, 8.7%, 23.6% and 14.3%.

### 4.2 Variant B: "MS-60/40 tilt", a benchmark-anchored softmax (the user's balanced portfolio)

This keeps the post's mechanism but anchors it to a strategic policy.

- **Universe:** SPY, IEF (or IEI), BIL.
- **Policy anchor b:** SPY 0.54, IEF 0.36, cash 0.10. This is a 60/40 on 90% of capital with a 10% cash anchor, so that "cash as the default alternative" survives. A pure 60/40 anchor (b_cash = 0) is allowed as an option, but then cash is never held.
- **Weights:** `w_i = b_i·exp(S_i/τ) / Σ_j b_j·exp(S_j/τ)`. This is identical to a softmax with logits S_i/τ + ln b_i, so equal anchors give back Variant A's formula exactly. S_SPY = S_EQ, S_IEF = S_UST, S_cash = 0, τ = 1.
- **Policy bounds (optional):** SPY in [0.30, 0.80], IEF in [0.10, 0.60], cash in [0, 0.40]. Clip, then send any residual to cash, or take any shortfall from cash, and renormalise. **[our design]** The unbounded version is the faithful default.
- **Rebalance, lag and costs:** as in Variant A. A monthly rebalance is a sensitivity check.
- **Benchmarks:** static 60/40 and static 54/36/10, both rebalanced quarterly.
- **Behaviour (τ = 1, unbounded):**
  - S_EQ = +1, S_UST = 0 gives 76.1 / 18.7 / 5.2.
  - S_EQ = −1, S_UST = −1 gives 46.1 / 30.7 / 23.2.
  - S_EQ = 0, S_UST = +1 gives 33.4 / 60.5 / 6.2.
  - All scores 0 gives 54 / 36 / 10.

---

## 5. Variants from other public research

**C. Growth–inflation quadrant allocation [our design]** (the concept comes from regime-sensitivity research)

- **Signals:** G = sign(PRODGROWTH theme) and I = sign(INFLPRESS theme). Both come from section 4.0 and are point-in-time as above.
- **Quadrant weights, illustrative and not taken from any paper:**

| Regime | Weights |
|---|---|
| G+ / I− | SPY 70, IEF 30 |
| G+ / I+ | SPY 50, DBC 20, TIP 15, GLD 15 |
| G− / I+ | SPY 20, TIP 30, GLD 25, BIL 25 |
| G− / I− | SPY 20, IEF 60, GLD 20 |

- **Rebalance:** monthly, with a 1-month persistence filter (switch only if the new quadrant holds at two consecutive month-ends).
- **Evidence for the sensitivities:**
  - Ilmanen, Maloney & Ross (2014), "Exploring Macroeconomic Sensitivities: How Investments Respond to Different Economic Environments", *Journal of Portfolio Management* 40(3). **[citation from memory; regime definitions not re-verified]**
  - Neville, Draaisma, Funnell, Harvey & Van Hemert (2021), below.

**D. Growth-Trend Timing (GTT)** — Jesse Livermore, *Philosophical Economics*, Jan 2016, https://www.philosophicaleconomics.com/2016/01/gtt/

- **Rule (verified in the post):** at each month-end, look at the growth signals for the *prior* month.
  - If they are all non-recessionary, hold equities for the next month.
  - Otherwise, hold equities only if price is above its 10-month moving average, and hold T-bills if it is below.
- **Preferred signal set:** real retail sales growth and industrial production growth. A recessionary reading (negative growth) from either one switches the trend filter on.
- **Implementation:**
  - Use yoy(RRSFS), or #RETSA deflated by #CPISA, and yoy(INDPRO / #INDSA3).
  - Recession flag = either < 0 at the latest month published by t, which is month t−1.
  - Price: $SPXTR or SPY; out-of-market asset: BIL or %3MTCM.
- **Reported results:**
  - GTT's win rate is about 39%, against about 24% for the plain moving-average strategy.
  - GTT was invested about 87% of the time.
  - The daily 200-day version beat the plain 200-day moving average by about 120 bp a year.
  - The post gives no CAGR or drawdown table for GTT.

**E. Inflation-surge defensive overlay** — evidence from Neville, Draaisma, Funnell, Harvey & Van Hemert (2021), "The Best Strategies for Inflationary Times". Man Institute summary: https://www.man.com/maninstitute/when-inflation-hits ; paper: SSRN 3813202, likely *JPM* 2021 **[journal unverified]**.

- **Paper's definition:** regimes in which year-on-year inflation rises "materially beyond 2%", to 5% or more. There are 8 US regimes since 1926. The regimes are identified **after the fact**.
- **Reported US real annualised returns in those regimes:**
  - Equities −7%, 10y Treasuries −5%, 60/40 −6%.
  - Commodities +14% (vs +1% in normal times).
  - Active trend-following: real CAGR of about 25%.
- **Real-time proxy [our design]:**
  - Surge state turns ON when latest CPI yoy ≥ 4% and is higher than 6 months earlier.
  - It turns OFF when CPI yoy < 3% or has fallen below its value 6 months earlier.
- **Rules:**
  - Base portfolio: 60/40 SPY/IEF.
  - When ON, swap the bond sleeve into ⅓ TIP + ⅓ commodities (DBC, or $BCOMTR plus cash) + ⅓ GLD, and apply a 10-month moving-average filter to the equity sleeve (BIL when below).
  - Monthly rebalance; CPI with a 1-month lag.

---

## 6. Caveats: revisions, look-ahead and fidelity

1. **Norgate macro look-ahead.** Values sit on the reference-period dates, and history is the revised latest vintage. Always shift by the publication lag, or better, the ALFRED release dates. Revisions still leak information, especially for GDP, payrolls, CFNAI (re-estimated monthly) and NFCI (re-estimated weekly). Where vintages exist, use first-release or as-of values, and report results both ways.
2. **Original's in-sample scaling (2000–2004).** This is inferred from `iis=True` and the data starting in 2000. Our strict version does not back-fill. Expect small differences in the early weights.
3. **Neutral = 0 for level factors.** Credit carry and spreads are always positive, so their themes are always ≥ 0, which gives a persistent pro-credit tilt. Real rates and term premia have been positive for most of the history, so they favour Treasuries. This is faithful to the notebook but worth reporting. An alternative is to centre on an expanding median as a sensitivity check.
4. **US proxies for global themes.** These make CYCLE, REALRATES and EQCARRY US-centric and correlated with the US themes. The effective weights differ from the original's.
5. **Substitute series differ from JPMaQS:**
   - Kim-Wright Treasury term premium instead of a swap term premium.
   - The CFNAI is a different growth nowcast from JPMaQS's "intuitive GDP".
   - UMich expectations instead of JPMaQS's household score.
   - Hard inventory ratios instead of survey changes.
   - Building permits instead of a construction survey.
   - A CAPE-based approximation for equity carry.
6. **Data issues:**
   - M1's 2020 break.
   - The Oct-2025 shutdown gap.
   - ISM is missing from FRED and stale in Norgate. Use the Philly Fed fallback.
   - FRED keeps only 3 years of ICE OAS. Use Norgate %CCCHYS, or BAA10Y.
   - FRED keeps only about 13 months of existing-home median price.
7. **Asset mismatch:**
   - The post's UST bucket is 5y, which maps to IEI, not IEF.
   - Its credit bucket is CDS-based, IG and HY, US and EU, with a 5y bond leg. LQD is US IG cash bonds with about 8y duration.
   - Gold is a funded future vs an ETF (expense ratio).
   - Results are **not** expected to match the post's 8.9% vs 4.8%. The universe is smaller and has less dispersion.
8. **Hindsight bias.** The post itself warns that theory-led factor choice embeds hindsight. Avoid tuning τ, the lags or the theme lists on the 2000–2026 sample. Freeze the spec above before the first backtest.
9. **Costs and taxes.** The original is gross. Quarterly softmax turnover can be large around turning points, so always report net results at 5–20 bp.
10. **Small universe.** Only 4 risky assets, so the panel test has much less power than the post's 11-asset panel. Report bootstrap or block-bootstrap confidence intervals.

---

## 7. Sources

- Macrosynergy post (Aug 2026): https://macrosynergy.com/research/wealth-management-with-macro-factors/
- Companion notebook: https://macrosynergy.com/academy/notebooks/wealth-management-with-macro-factors/
- `macrosynergy` package, `make_zn_scores` (develop branch): https://github.com/macrosynergy/macrosynergy/blob/develop/macrosynergy/panel/make_zn_scores.py
- Doeswijk, Lam & Swinkels (cited by the post): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2978509
- Norgate Data content tables (revision footnote): https://norgatedata.com/data-content-tables.php
- Norgate symbol names, dates and values: local NDU via `norgatedata` 1.0.77, queried 2026-11-18
- FRED series pages and fredgraph CSV (IDs and start dates verified 2026-11-18): https://fred.stlouisfed.org/
- Livermore, "Growth and Trend" (GTT): https://www.philosophicaleconomics.com/2016/01/gtt/
- Man Institute, "When inflation hits" (summary of Neville et al. 2021): https://www.man.com/maninstitute/when-inflation-hits
