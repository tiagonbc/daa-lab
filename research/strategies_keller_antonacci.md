# Keller and Antonacci family: tactical asset allocation strategy catalog

This is the companion to `strategies_keller_antonacci.json`, which has 38 entries. Each JSON entry has the full universe, the signal formula, step-by-step rules, parameters, data needs and the notes on gaps. This file gives you a quick overview, the shared definitions and the caveats.

Compiled 2026-11-18. It covers Wouter J. Keller and his co-authors (Keuning, van Putten, Butler, Kipnis), Ilya Kipnis's KDA, Gary Antonacci, and Accelerating Dual Momentum (Engineered Portfolio, which derives from GEM).

## Shared definitions (used throughout the JSON)

| Term | Definition |
|---|---|
| Rk | Total return over k months, P_t / P_{t-k} - 1, using month-end dividend-adjusted closes |
| **13612W** (fast, weighted) | 12·R1 + 4·R3 + 2·R6 + 1·R12. The papers divide by 4 to get an average annualized return, and Kipnis divides by 19. Scaling changes neither the sign nor the rank. About 40% of the weight falls on the last month. |
| **13612U** (unweighted) | (R1 + R3 + R6 + R12) / 4 |
| **SMA12 momentum** (Keller's "SMA(12)" = SMA13) | P_t / mean(P_t … P_{t-12}) - 1. This uses the 13 most recent month-end prices, including the current one. |
| EAA/CAA return | (R1 + R3 + R6 + R12) / 22. This follows Kipnis's code and AllocateSmartly. |
| Breadth b, B, T | b is the number of "bad" assets, meaning momentum ≤ 0 (some papers say < 0). The cash fraction is CF = min(1, b/B), rounded down to a multiple of 1/T (TrendXplorer's "easy trading" form). The portfolio holds the top round((1-CF)·T) risky assets at 1/T each. |
| PAA bond fraction | BF = min(1, (N - n) / (N - n1)), where n1 = a·N/4, n is the number of assets with positive momentum, and a is the protection factor (0, 1 or 2) |
| Timing | Unless noted, the signal is computed at the close of the last trading day of the month and traded at that same close. Positions are held for one month, and the whole portfolio is rebalanced monthly. |

## Summary table

Universe gives the counts as risky / defensive / canary. "AS" means AllocateSmartly. Confidence is **H** when verified against the paper PDF, **M** when taken from AllocateSmartly's public post plus author-adjacent sources, and **L** when parts are inferred or come only from third-party code.

| id | Strategy | Author(s) | Year | Universe | Signal (short) | Rebalance | AS | Conf. |
|---|---|---|---|---|---|---|---|---|
| faa | Flexible AA | Keller, van Putten | 2012 | 7 (incl. cash SHY) / – / – | 4-month rank blend: R×1 + V×0.5 + C×0.5 (daily vol/corr). Top 3, absolute momentum to cash. | Monthly EOM | Tracked (members) | M/L |
| maa | Modern AA | Keller, van Putten | 2013 | 7 / – / – | 4-month shrunk single-index MVO, positive momentum only | Monthly | No | **L** |
| eaa_golden_offensive | Elastic AA, Golden Offensive | Keller, Butler | 2014 | 7 (cash IEF in universe) | z=(1-c)·r², excess r over T-bills, CP = share of losers to IEF, TopN=3 | Monthly EOM | Tracked (members) | L (universe) |
| eaa_golden_defensive | Elastic AA, Golden Defensive | Keller, Butler | 2014 | 7 | z = sqrt((1-c)·r), otherwise as offensive | Monthly EOM | Tracked (members) | L (universe) |
| caa_offensive | Classical AA, TV 10% | Keller, Butler, Kipnis | 2015 | 6 risky + 2 uncapped (IEF, BIL) | Long-only MVO (CLA), μ = (R1+R3+R6+R12)/22, 12-month covariance, 25% caps | Monthly EOM | Yes | M |
| caa_defensive | Classical AA, TV 5% | Keller, Butler, Kipnis | 2015 | 6 + 2 | As above, with target volatility 5% | Monthly EOM | Yes | M |
| paa2 | Protective AA (PAA2, Top 6, IEF) | Keller, Keuning | 2016 | 12 / 1 / (risky) | SMA12; BF = (12-n)/6 capped at 1; top 6 | Monthly EOM | Yes | M |
| paa_cpr | PAA-CPR (IEF or cash) | Keller, Keuning | 2016 | 12 / 2 / (risky) | As PAA2, with the protection asset being the better of IEF and cash | Monthly EOM | Yes | M |
| paa1 | PAA1 (medium protection) | Keller, Keuning | 2016 | 12 / 1 | BF = (12-n)/9 | Monthly EOM | No | M |
| paa0 | PAA0 (low protection) | Keller, Keuning | 2016 | 12 / 1 | BF = (12-n)/12 | Monthly EOM | No | M |
| gpm | Generalized Protective Momentum | Keuning, Keller | 2016 | 12 / 2 / (risky) | z = 13612U·(1 - corr to EW index); CP = (12-n)/6; top 3 | Monthly EOM | Yes | M |
| vaa_g4 | Vigilant AA G4 (aggressive, T1/B1) | Keller, Keuning | 2017 | 4 / 3 / (risky) | 13612W; any bad asset sends 100% to the best bond | Monthly EOM | Yes | M |
| vaa_g12 | Vigilant AA G12 (paper T2/B4) | Keller, Keuning | 2017 | 12 / 3 / (risky) | 13612W breadth; CF = floor(b·T/B)/T | Monthly EOM | No | M |
| vaa_g12_balanced | Vigilant AA Balanced (AS T5/B4) | Keller, Keuning | 2017 | 12 / 3 | As above with T=5 | Monthly EOM | Yes | M |
| daa_g12 | Defensive AA G12 (T6/B2) | Keller, Keuning | 2018 | 12 / 3 / 2 (VWO, BND) | 13612W canary breadth: 0, 50% or 100% to the best bond | Monthly EOM | Yes (probably this variant) | M |
| daa_g6 | DAA G6 (T6/B2) | Keller, Keuning | 2018 | 6 / 3 / 2 | Same as G12 | Monthly EOM | No | **L** |
| daa_g4 | DAA G4 (T2/B1) | Keller, Keuning | 2018 | 4 / 3 / 2 | Same mechanism, B=1 | Monthly EOM | No | L |
| daa1_g4 | DAA1-G4 aggressive (T4/B1) | Keller, Keuning | 2018 | 4 / 3 (SHV, IEF, UST 2x) / 2 | Same, with a leveraged-Treasury cash option | Monthly EOM | No | L |
| daa1_g12 | DAA1-G12 aggressive (T2/B1) | Keller, Keuning | 2018 | 12 / 3 / 2 | Same | Monthly EOM | No | L |
| daa1_u1 | DAA1-U1 (SPY only) | Keller, Keuning | 2018 | 1 / 3 / 2 | Same | Monthly EOM | No | L |
| laa | Lethargic AA | Keller | 2019 | 75% static (IWD, GLD, IEF) + 25% QQQ↔SHY | Risk-off when UNRATE > its SMA12 and SPX < its SMA10 | Monthly EOM | Yes | M |
| laa_g4 | LAA-G4 (world equity sleeve) | Keller | 2019 | Same with a 3:2:1 SPY/VEA/VWO sleeve | Same | Monthly EOM | No | **L** |
| raa | Resilient AA | Keller | 2020 | 5 / 2 / 2 + UNRATE | Risk-off only when UE(t-1) > UE(t-13) and either canary 13612W ≤ 0 | Monthly EOM | Yes | M |
| baa_g12_balanced | Bold AA Balanced (G12/T6) | Keller | 2022 | 12 / 7 / 4 | Canary 13612W (B=1); SMA12 ranking; top 3 defensive with a BIL floor | Monthly EOM | Yes | **H** |
| baa_g4_aggressive | Bold AA Aggressive (G4/T1) | Keller | 2022 | 4 / 7 / 4 | Same, top 1 offensive | Monthly EOM | Yes | **H** |
| baa_g12_t3 | BAA G12/T3 | Keller | 2022 | 12 / 7 / 4 | Same, top 3 offensive | Monthly EOM | No | H |
| baa_g4_t2 | BAA G4/T2 | Keller | 2022 | 4 / 7 / 4 | Same, top 2 offensive | Monthly EOM | No | H |
| haa_balanced | Hybrid AA Balanced (G8/T4) | Keller, Keuning | 2023 | 8 / 2 / 1 (TIP) | 13612U; TIP canary; top 4 with bad picks swapped for the best of BIL and IEF | Monthly EOM | Yes | **H** |
| haa_simple | Hybrid AA Simple (SPY only) | Keller, Keuning | 2023 | 1 / 2 / 1 | SPY if TIP and SPY are both positive, else the better of IEF and BIL | Monthly EOM | Yes | **H** |
| haa_4 | HAA-4 (G4/T2) | Keller, Keuning | 2023 | 4 / 2 / 1 | Same | Monthly EOM | No | H |
| haa_12 | HAA-12 (G12/T6) | Keller, Keuning | 2023 | 12 / 2 / 1 | Same | Monthly EOM | No | H |
| haa_16 | HAA-16 (G16/T8) | Keller, Keuning | 2023 | 16 / 2 / 1 | Same | Monthly EOM | No | H |
| kda | Kipnis Defensive Adaptive AA | Kipnis | 2019 | 10 / IEF or cash / 2 | 13612W; canary sets 0, 50% or 100% invested; top 5 with positive momentum; min-variance weights (blended correlation) | Monthly EOM | Yes | M |
| gem | Global Equities Momentum (official) | Antonacci | 2014 | 2 / 1 (AGG) / T-bill hurdle | 12-month return: if SPY > T-bills, the better of SPY and ACWI ex-US; otherwise bonds | Monthly EOM | Tracked (members) | M |
| gem_simplified | GEM (flowchart version) | Antonacci | 2014 | 2 / 1 | The better of SPY and ACWI ex-US, held only if it beats T-bills; otherwise bonds | Monthly EOM | No | M |
| composite_dual_momentum | Composite Dual Momentum | Antonacci | 2012 | 4 modules × 2 / cash | 12-month dual momentum in each 25% module, failing module goes to cash | Monthly EOM | Yes | M |
| accelerating_dual_momentum | Accelerating Dual Momentum (AS) | Engineered Portfolio | 2018 | 2 / 2 (TLT, TIP) | Average of R1, R3, R6 for SPY vs SCZ; if neither is positive, the better 1-month of TLT and TIP | Monthly EOM | Yes | M |
| accelerating_dual_momentum_original | ADM (original) | Engineered Portfolio | 2018 | 2 / 1 (TLT) | R1+R3+R6, long Treasuries if both are negative | Monthly | No | M |

## Mapping to AllocateSmartly's tracked list

AllocateSmartly lists 17 Keller-family strategies, 1 by Kipnis, 2 by Antonacci and ADM. They map to the JSON ids as follows:

- BAA Aggressive → `baa_g4_aggressive`
- BAA Balanced → `baa_g12_balanced`
- Resilient AA → `raa`
- Lethargic AA → `laa`
- HAA Balanced → `haa_balanced`
- HAA Simple → `haa_simple`
- Defensive AA → `daa_g12` (the variant is not stated publicly)
- VAA Aggressive → `vaa_g4`
- VAA Balanced → `vaa_g12_balanced`
- CAA Offensive / Defensive → `caa_offensive` / `caa_defensive`
- Generalized Protective Momentum → `gpm`
- PAA → `paa2`
- PAA-CPR → `paa_cpr`
- EAA Offensive / Defensive → `eaa_golden_offensive` / `eaa_golden_defensive`
- Flexible AA → `faa`
- Defensive Adaptive AA → `kda`
- Traditional Dual Momentum → `gem`
- Composite Dual Momentum → `composite_dual_momentum`
- Accelerating Dual Momentum → `accelerating_dual_momentum`

EAA, FAA and Traditional Dual Momentum have no public AllocateSmartly write-up; their rules are members-only. Those entries therefore follow the original sources, and the ETF choices are flagged.

## Notes and caveats

1. **How the rules were verified.** SSRN download pages are behind a Cloudflare bot check, which I did not try to get around. I obtained the full PDFs for HAA, BAA and CAA from public mirrors and read them. For the other strategies I cross-checked the rules against several sources:
   - AllocateSmartly's public posts
   - TrendXplorer, the blog of co-author J.W. Keuning
   - CXO Advisory summaries of the papers
   - TuringTrader's open-source implementations (Keller_DAA/LAA/FAA/CAA, BAA_v2, HAA_v2 and Antonacci_DualMomentumInvesting)
   - Kipnis's own code and posts

   Each JSON `notes` field says which sources an entry relies on and flags any detail that comes from only one source.
2. **Could not be fully specified.**
   - `maa`: only a summary was available, so the weight formula and holding count are unverified.
   - The paper parameters for `daa_g6`, `daa_g4`, `daa1_*` and `laa_g4` come from TuringTrader classes. G6 in particular may not appear in the paper.
   - The universes for the EAA entries are a best reading. They assume the paper's 7-asset index universe equals CAA's 8-asset set minus T-bills.
   - The ETF lists AllocateSmartly uses for FAA, EAA and GEM are not public.
3. **Differences between the papers and AllocateSmartly** (details in each entry):
   - AllocateSmartly executes SHY/BIL trades as the 3-month T-bill rate (cash).
   - It uses EFA/EEM/AGG in place of the papers' VEA/VWO/BND, and VNQ/DBC in place of PAA's IYR/GSG.
   - KDA uses EEM/AGG canaries in place of VWO/BND, and fixed day-count lookbacks.
   - ADM adds a TLT-vs-TIP bond switch.
   - HAA originally sent failing offensive slots to cash; this was later corrected to "the better of IEF and cash".
   - For CAA, AllocateSmartly averages returns as (R1+R3+R6+R12)/22, while TuringTrader weights the lookbacks 1/3/6/12.
4. **Threshold conventions.** The papers alternate between "negative" and "non-positive" momentum as the test for a "bad" asset. The difference rarely matters, but it should be a backtester switch. The same applies to rounding the breadth cash fraction (b/B exactly vs. rounded down to a multiple of 1/T).
5. **Data and look-ahead.**
   - LAA and RAA use revised FRED UNRATE data. To mimic real-time availability, apply a one-month publication lag.
   - Before 1997, TIPS data are simulated; HAA substitutes IEF for TIP before the end of 1973.
   - Keller's papers use index-based ETF proxies from Dec 1969/1970, calibrated for fees (method in the PAA paper's appendix), and assume 0.1% one-way costs.
   - For BIL before its 2007 inception, use a 3-month T-bill total-return series.
6. **Not catalogued (out of scope or unverifiable):**
   - Engineered Portfolio's separate "Engineered Portfolio" strategy, which is not Antonacci's.
   - Antonacci's other book models (Global Balanced Momentum, Dual Momentum Sector Rotation, Parity Portfolio with absolute momentum). AllocateSmartly does not track them, and I could only see them through third-party code, not the book.
   - TrendXplorer's leveraged "DAA on steroids" variants.
   - The VAA and DAA Fama-French test universes (U6, U15).
   - Kipnis's leveraged KDA.
   - Butler et al.'s Adaptive Asset Allocation, which is left to the other agent.
7. **Newer Keller papers.** The newest Keller strategy paper I found is HAA (Feb/Mar 2023). A third-party study from Aug 2026 and BestFolio's catalogue also show nothing newer. However, the SSRN author page (per_id=1935527) blocked automated access, and the shared web-search budget ran out mid-task. A manual check of that page for any 2024-2026 papers is still recommended.
