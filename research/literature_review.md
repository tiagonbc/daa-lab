# Dynamic Asset Allocation: A Plain-Language Literature Review

*From the foundations to the current state (2023-2026). Companion to `literature.json`, which holds 90 verified entries with links and one-line summaries. A few extra verified sources cited in the text, but not in the JSON, are listed at the end.*

---

## 1. What is dynamic asset allocation?

Every large investor first has to decide **how much money goes into each kind of asset**: shares, bonds, credit, real estate, infrastructure, private equity, commodities and cash. That decision is called *asset allocation*, and it comes in three flavours.

- **Strategic asset allocation (SAA)** is the long-term mix. A board sets it every few years, using long-run assumptions about return, risk and the fund's liabilities. Think of it as the fund's "home address".
- **Tactical asset allocation (TAA)** is a deliberate, temporary move away from that address. An example is holding a little less equity for six months because shares look expensive or their trend has turned down. TAA tries to *add return*.
- **Dynamic asset allocation (DAA)** is the broader idea that the mix should *respond to changing conditions* in a disciplined way. It includes TAA. It also covers rules that change exposure as markets move (rebalancing, volatility targeting, drawdown control) and keeping the whole fund inside its risk, liquidity and leverage limits.

At a large pension plan, a DAA or total-fund team usually sits between the long-term policy and the asset-class teams. It acts as the fund's steering wheel, using liquid instruments such as futures and swaps to tilt exposures and manage rebalancing.

The question behind all of this is easy to state and hard to answer: **does changing the mix over time leave investors better off, after costs and after allowing for luck?**

---

## 2. The foundations: why the mix might need to move

**Long-horizon investors.** Portfolio theory began as a one-period problem: pick the best mix for the next period (Markowitz, 1952). Samuelson (1969) and Merton (1969) extended it to many periods. If returns cannot be predicted, and the investor's attitude to risk does not change with wealth, the best mix stays *constant* and the horizon does not matter. That is the theoretical case *for* a fixed strategic mix.

Merton (1973) showed what changes when investment opportunities shift over time: investors should also hold "hedging" positions against bad changes in future opportunities. This is the seed of dynamic allocation. **If expected returns or risks change predictably, the best mix should change too.** Campbell and Viceira (2002) turned this into practical advice for long-term investors. Barberis (2000) added a sobering point: once you admit you are *unsure* how predictable returns are, the case for big timing bets shrinks a lot.

**How much does the policy mix matter?** Brinson, Hood and Beebower (1986) studied 91 US pension funds. The policy mix explained about 94% of the *ups and downs* in each fund's quarterly returns, while timing and security selection explained little and on average cost money. This is often misquoted as "asset allocation explains 90% of returns." Ibbotson and Kaplan (2000) showed that the answer depends on the question. Policy explains about 90% of a fund's swings *over time*, about 40% of the *differences between* funds, and roughly 100% of the *average level* of returns.

**Rules for changing the mix.** Practitioners ran systematic tactical models in the 1980s, comparing expected returns on stocks, bonds and cash (Arnott and von Germeten, 1983; Sharpe, 1987). Perold and Sharpe (1988) gave the clearest map of *dynamic strategies* (see also Black and Perold, 1992). Rebalancing to a constant mix *buys losers and sells winners*, so it does well in choppy markets and badly in strong trends. Portfolio insurance does the opposite: it protects in trends but suffers in whipsaws. The lesson runs through everything that follows: **every dynamic rule is a bet on what kind of market comes next.**

---

## 3. Can we forecast returns? Valuation-based timing

**The case for predictability.** Fama and French (1988) found that high dividend yields were followed by higher stock returns, especially over several years. Fama and French (1989) linked expected returns on stocks and bonds to the business cycle: they tend to be high in bad times and low in good times. Campbell and Shiller (1998) showed that the smoothed price-to-earnings ratio (CAPE) forecasts future *price* changes, not earnings growth. Cochrane (2008) gave a strong defence: if returns were unpredictable, dividend growth would have to be predictable, and it is not. Bond returns are predictable too (Cochrane and Piazzesi, 2005). Koijen et al. (2018) showed that *carry*, the return an asset earns if prices do not move, predicts returns in almost every asset class.

**The case against.** Welch and Goyal (2008) delivered the best-known cold shower. Almost none of the popular predictors beat the simple historical average when used *out of sample*, that is, with only the information available at the time. Their update (Goyal, Welch and Zafirov, 2024) adds 29 newer predictors and data through 2021. More than a third lose their in-sample significance, about half of the rest fail out of sample, and only a few hold up.

**Rescue attempts.** Campbell and Thompson (2008) showed that common-sense limits help. Ruling out a negative forecast equity premium, for example, turns weak predictors into small but useful ones. Rapach, Strauss and Zhou (2010) showed that *averaging* many predictors gives steadier out-of-sample gains than any single one. Neely et al. (2014) found that simple trend indicators add information that valuation and macro variables miss.

**The practitioner view.** Asness (2003) criticised the "Fed model", which compares the stock earnings yield with bond yields, for mixing real and nominal quantities. Asness, Ilmanen and Maloney (2017) found that valuation timing alone would have disappointed, because markets can stay expensive for years. Their advice was to "sin a little": make modest tilts, preferably combined with momentum. Ilmanen (2011) offers the fullest practitioner synthesis. Expected returns vary and can be estimated, but the estimates are noisy, so they are best used for **modest tilts and realistic long-run assumptions**.

**Bottom line:** valuation tells you something about the next ten years and very little about the next ten months.

---

## 4. Momentum and trend: the most robust tactical signal

**Two kinds of momentum.** *Cross-sectional momentum* buys recent winners and sells recent losers relative to each other (Jegadeesh and Titman, 1993). *Time-series momentum*, or *trend following*, asks of each asset on its own: has it gone up over the past year? If yes, hold it; if no, step aside or go short.

**Simple rules for allocators.** Faber (2007) made trend following popular: hold each of five asset classes only when its price is above its 10-month moving average, otherwise hold cash. Over a long history this cut drawdowns sharply while keeping equity-like returns. Blitz and van Vliet (2008) combined value and momentum signals across 12 asset classes with good results. Antonacci (2014) combined *absolute* momentum (trend) with *relative* momentum (pick the stronger asset) into "dual momentum."

Keller and co-authors built a family of increasingly defensive rules. Some add volatility and correlation to the momentum ranking (Keller and van Putten, 2012) or feed momentum estimates into a mean-variance optimiser (Keller, Butler and Kipnis, 2015). Others use the *breadth* of momentum, sometimes measured on a separate "canary" set of assets, to decide how much to hold in safe assets (Keller and Keuning, 2016, 2017, 2018). Clare et al. (2016) found that adding a trend filter to risk-parity and momentum portfolios was the key ingredient for better risk-adjusted returns. These are useful templates, but mostly unreviewed working papers tuned with hindsight.

**Academic evidence.** Moskowitz, Ooi and Pedersen (2012) documented time-series momentum in 58 futures markets. A diversified trend strategy earned strong returns and did best in extreme up and down markets. Asness, Moskowitz and Pedersen (2013) found value and momentum premia across many asset classes, and because the two are negatively correlated, combining them works much better than either alone. Hurst, Ooi and Pedersen (2017) showed that trend following across 67 markets was profitable for more than a century. Levine and Pedersen (2016) showed that the many ways of measuring a trend are closely related, so the exact rule matters less than people think. Baltas and Kosowski (2020) showed that how you estimate volatility and correlation strongly affects turnover and risk.

**Crisis alpha and critiques.** Trend strategies often make money in long equity and bond bear markets, because they turn short as the fall continues (Hamill, Rattray and Van Hemert, 2016). They do *not* protect against sudden one-day crashes, and they lose money in choppy markets. Kim, Tse and Wald (2016) argued that much of the profit comes from *volatility scaling* rather than from the trend signal itself. Huang et al. (2020) found little asset-by-asset evidence that past-year returns predict future returns. Goulding, Harvey and Mazzoleni (2023) showed that trend strategies suffer most at *turning points*, when fast and slow signals disagree.

**Bottom line:** trend is the most widely replicated dynamic signal and has real value in long bear markets. But its returns come in bursts, and it can disappoint for years.

---

## 5. Macro regimes: describing the weather versus forecasting it

**Regime models.** Hamilton (1989) introduced the regime-switching model, in which the economy moves between hidden states, such as expansion and recession, that behave differently. Ang and Bekaert (2002) found that in "bear" regimes volatility and correlations rise, yet international diversification still pays. Kritzman, Page and Turkington (2012) built regime indicators for turbulence, inflation and growth, and tilting by regime improved out-of-sample results, mainly by limiting large losses. Newer methods aim for labels that are stable in real time. "Jump" models penalise frequent switching (Nystrup, Madsen and Lindström, 2018; Shu, Yu and Mulvey, 2024). Similarity-based methods look for the past periods most like today (Mulliner et al., 2026).

**How assets behave in different environments.** Ilmanen, Maloney and Ross (2014) found that equities and credit do best when growth surprises upward, and nominal bonds when growth and inflation surprise downward. Rising inflation is hard for both. Style premia such as value, momentum and carry depended far less on the macro backdrop. Neville et al. (2021) studied about a century of US, UK and Japanese data. Unexpected inflation hurt both stocks and nominal bonds, while commodities and trend following protected best. Harvey et al. (2019) found that buying put options protected reliably but at a high cost, Treasuries were not a reliable hedge, and trend following and quality strategies did best in crises. Campbell, Pflueger and Viceira (2020) explained *why* the stock-bond correlation changes: it depends on how inflation moves with the economy and how monetary policy reacts.

**Using macro data directly.** Brooks (2017) showed that "macro momentum" works across asset classes: go long assets whose economic fundamentals are improving and short those deteriorating. Practitioners now build "macro-quantamental" signals from *point-in-time* economic data, meaning only what was known on each date. Macrosynergy's work on J.P. Morgan's JPMaQS dataset is a visible example (Costa and Sueppel, 2025).

**Bottom line:** regimes are easy to describe after the fact and hard to call in real time. Their most reliable use is to *stress-test* the portfolio and see which exposures will suffer together.

---

## 6. Risk-based and volatility-managed allocation

**Risk parity.** A 60/40 portfolio gets roughly 90% of its *risk* from equities. Qian (2005) proposed "risk parity": size each asset class so it contributes equally to total risk, which usually means more bonds, often with leverage. Maillard, Roncalli and Teiletche (2010) formalised the equal-risk-contribution portfolio. Asness, Frazzini and Pedersen (2012) explained why it can work: many investors avoid leverage, so they overpay for risky assets. Bridgewater's "All Weather" is the best-known practitioner version (Podolsky, Johnson and Jennings, 2012). Its weak spot showed in 2022, when stocks and bonds fell together.

**Volatility targeting.** Volatility clusters, which makes it much easier to forecast than returns (Bollerslev et al., 2018). Moreira and Muir (2017) found that cutting exposure when recent volatility is high improved Sharpe ratios for the market and many factors. Harvey et al. (2018) found that targeting volatility helps equities and credit, mainly by trimming the worst outcomes, but does little for bonds or commodities. Barroso and Santa-Clara (2015) showed that it greatly reduces momentum crashes. On the other side, Cederburg et al. (2020) tested 103 equity strategies and found that, implemented realistically, volatility management did not reliably beat the originals. Liu, Tang and Zhou (2019) also argued that the gains are hard to capture in real time.

**Drawdown control.** Grossman and Zhou (1993) derived the best strategy for an investor who must never lose more than a fixed share of peak wealth: hold risky assets in proportion to the cushion above that floor (see also Chekhlov, Uryasev and Zabarankin, 2005). Like portfolio insurance, such rules sell after losses, which can lock in damage if markets bounce back quickly.

**Bottom line:** risk is far more predictable than return, so **managing risk dynamically is the most dependable tool a DAA team has**. But risk-based portfolios carry hidden bets (for example on bonds) that can hurt when the regime changes.

---

## 7. Factors, reference portfolios and the Total Portfolio Approach

**From asset classes to factors.** Asset-class labels can hide similar risks: private equity, listed equity and high-yield credit all depend heavily on economic growth. Page and Taborsky (2011) showed that asset-class correlations jump in crises while factor correlations stay more stable. Ang (2014) argued that a portfolio should be seen as a bundle of factor exposures, such as growth, inflation, rates, liquidity, value and momentum. Idzorek and Kowara (2013) added a caveat: done consistently, factor and asset-class approaches reach the same answer, so the gain is clearer thinking, not magic. Ilmanen et al. (2021) showed that factor premia vary over time but are hard to time.

**How large funds organise this.** Reviews of Norway's sovereign fund (Ang, Goetzmann and Schaefer, 2009; Ang, Brandt and Denison, 2014) argued for seeing returns as factor exposures and for a simple reference point against which to judge active decisions. Several large asset owners now use a **reference portfolio**: a simple, low-cost mix of listed stocks and bonds that represents the risk the board accepts. CPP Investments targets the risk of an 85/15 equity-bond reference portfolio for its base plan (CPP Investments, 2024), and NZ Super Fund publishes an 80/20 one (NZ Super Fund, 2023). Active teams then build a more diversified portfolio with similar total risk.

This is the core of the **Total Portfolio Approach (TPA)**: each decision is judged by its effect on the *whole* fund, not by whether it beats an asset-class benchmark. Bass, Gladstone and Ang (2017) showed how to view all holdings, public and private, through one set of factors. Recent industry reports describe how TPA is spreading (CAIA Association et al., 2024; CAIA Association and Thinking Ahead Institute, 2025). Beath et al. (2021) describe the "Canadian model": in-house management, strong internal teams and large private-asset allocations, with returns and liability hedging that beat global peers over 2004-2018. Andonov, Bauer and Cremers (2017) showed that accounting rules for liability discount rates shape how much risk US public plans take.

**Bottom line:** in a TPA fund, the DAA team turns a factor-and-risk view of the *whole* fund into concrete, liquid adjustments.

---

## 8. Machine learning and modern methods

**Blending views with equilibrium.** Noisy forecasts fed into a mean-variance optimiser give extreme, unstable portfolios. Black and Litterman (1992) start instead from the returns implied by market prices and blend in the investor's views according to confidence (He and Litterman, 1999). It remains a standard way to turn tactical views into sensible tilts. Hierarchical risk parity uses clustering to diversify without a fragile covariance estimate (López de Prado, 2016).

**Machine learning for prediction.** Gu, Kelly and Xiu (2020) showed that tree models and neural networks forecast stock returns better than linear models, largely by capturing interactions between signals. Bianchi, Büchner and Tamoni (2021) found similar gains for bonds, and Kelly and Xiu (2023) review the field. Jensen et al. (2026) showed that ML portfolios that ignore trading costs chase short-lived signals, so costs must be built into the learning. Bybee et al. (2024) used decades of *Wall Street Journal* articles to measure which themes the news focused on, and found this helps explain economic activity and returns.

**The complexity debate.** Kelly, Malamud and Zhou (2024) argued that models with *more* parameters than data points can predict market returns better than small ones: "the virtue of complexity." Nagel (2025) replied that, with short training windows, the complex model behaves like a simple volatility-timed momentum rule. Kelly and Malamud (2025) responded, and the debate is open. For DAA, the practical message is caution: tactical allocation has *few* assets and *short* monthly histories, exactly where flexible models overfit most easily.

**Large language models.** Researchers have tested whether models like ChatGPT can read news and forecast returns (Lopez-Lira and Tang, 2023) or generate economic expectations (Bybee, 2023). A serious concern is **look-ahead bias**: these models were trained on text written after many of the test dates, so they may "remember" what happened (Glasserman and Lin, 2023; Sarkar and Vafa, 2024). Any LLM-based macro signal must be tested on data after the model's training cut-off.

---

## 9. Backtest overfitting: why most backtests flatter

History is short. Try enough variations and you will always find something that looked great in the past by chance.

- **Data snooping.** Sullivan, Timmermann and White (1999) tested thousands of technical trading rules over 100 years of data. Once they allowed for the number of rules tried, the apparent profits largely disappeared (see also White, 2000).
- **Higher hurdles.** Harvey, Liu and Zhu (2016) argued that a new factor should clear a t-statistic of about 3 rather than 2. Harvey and Liu (2015) showed how to "haircut" a backtest Sharpe ratio for the number of trials.
- **Better statistics.** Sharpe ratios are measured with large error (Lo, 2002). The *deflated Sharpe ratio* adjusts for the number of trials and for non-normal returns (Bailey and López de Prado, 2014). The *probability of backtest overfitting* estimates how often the best in-sample strategy underperforms out of sample (Bailey et al., 2017).
- **Decay.** McLean and Pontiff (2016) found that returns to 97 published predictors fell by about a quarter out of sample and by more than half after publication. Suhonen, Lennkh and Perez (2017) found that the median Sharpe ratio of bank "alternative beta" strategies fell from 1.20 in backtests to 0.31 live.
- **Replication debate.** Hou, Xue and Zhang (2020) found that many anomalies fail to replicate. Jensen, Kelly and Pedersen (2023) countered that most factors *do* replicate when grouped into themes and judged sensibly.
- **A protocol.** Arnott, Harvey and Markowitz (2019) proposed a checklist: state the idea first, record every trial, do not tweak after seeing results, use realistic costs, and keep expectations modest.

**Bottom line:** DAA has only a handful of truly independent observations (a few business cycles), so the burden of proof should be high and live expectations well below backtests.

---

## 10. Combining strategies and signals

Each tactical signal is weak on its own, so combining many is central to modern DAA.

- **Forecast combination.** Bates and Granger (1969) showed that combining forecasts usually beats picking the "best" one. Timmermann (2006) found that simple equal weights are hard to beat, because estimated weights are noisy. Rapach, Strauss and Zhou (2010) got clear out-of-sample gains by combining equity-premium forecasts.
- **Naive versus optimised.** DeMiguel, Garlappi and Uppal (2009) found that none of 14 optimised models consistently beat a simple equal-weight (1/N) portfolio out of sample. Tu and Zhou (2011) showed that blending a sophisticated rule with 1/N captures much of the benefit of both.
- **Negative correlation is valuable.** Value and momentum are negatively correlated, so the combination is much smoother than either (Asness, Moskowitz and Pedersen, 2013).
- **Blend signals or portfolios?** Fitzgibbons et al. (2017) favoured merging signals into one score. Ghayur, Heaney and Platt (2018) found the answer depends on the active-risk budget. Dichtl et al. (2019) found that dynamically re-weighting factors adds only modest value after costs.
- **Rebalancing plus trend.** Rattray et al. (2020) showed that mechanical rebalancing keeps buying the falling asset in a trending crisis. Adding a trend sleeve, or delaying rebalancing when trends are negative, reduced drawdowns.

**Bottom line:** a DAA programme should look like a diversified *portfolio of modest signals* (value, trend, carry, macro momentum, risk scaling) with simple, shrunk weights, not like one clever model.

---

## 11. The current state (2023-2026): what changed

**1. The stock-bond correlation flipped.** For about two decades before 2022, bonds usually rose when stocks fell. In 2022 both fell together. Brixton et al. (2023) showed that the correlation depends on whether growth or inflation uncertainty dominates. Moving from -0.5 to +0.5 raises 60/40 volatility by about one-fifth. Molenaar et al. (2024), with data back to 1875, found that a positive correlation has been common and that shifts can be abrupt. The bond hedge can no longer be assumed.

**2. Higher rates changed the opportunity set.** Ilmanen (2022) warned that falling yields had flattered past returns, so future returns were likely to be lower. Since 2022, cash and bonds again pay meaningful yields, which raises the hurdle for risky assets and for leverage.

**3. Trend following earned its keep.** 2022 was widely reported as a very strong year for trend and managed-futures strategies, which rode persistent moves in rates, currencies and commodities. That fits the evidence that trend protects in inflationary periods and long bear markets (Neville et al., 2021; Hurst, Ooi and Pedersen, 2017).

**4. Private assets and "smoothed" risk.** Reported private-asset values are smoothed, which understates volatility and correlation. Stafford (2022) showed that much of private-equity performance can be replicated with cheap, small public stocks plus modest leverage and smoothed accounting. Ilmanen, Chandra and McQuinn (2020) argued that private equity's expected edge over public equity is modest. A TPA fund has to look through the smoothing to the true exposures.

**5. Leverage and liquidity are front of mind.** The September 2022 UK gilt crisis showed how leveraged pension strategies can face sudden collateral calls and forced selling (Pinter, 2023; Pinter, Siriwardane and Walker, 2024). Bank of Canada staff have documented that large Canadian pension funds finance big bond holdings through repo (Plong and Maru, 2024). They also found that pension plans' repo lending moved Canada's overnight funding rate in late 2025 (Fontaine, Tchamova and Maru, 2026).

**6. Prediction is still hard, and ML is debated.** The Goyal, Welch and Zafirov (2024) update confirms that most classic predictors still fail out of sample. The complexity debate continues (Kelly, Malamud and Zhou, 2024; Nagel, 2025), and LLMs face look-ahead bias.

**7. TPA is spreading.** More asset owners use reference portfolios, factor lenses and a central team that manages fund-level risk, leverage and liquidity. The main obstacles are culture and governance rather than technology (CAIA Association and Thinking Ahead Institute, 2025).

---

## 12. What this means for a pension fund's DAA team

1. **Start from the total fund.** Judge every tilt by its effect on total-fund risk, liquidity and leverage.
2. **Manage risk before chasing return.** Volatility and correlation can be forecast; returns barely can. Monitor the stock-bond correlation closely.
3. **Use a diversified set of signals.** Combine trend, value, carry and macro signals with simple, robust weights, and benchmark the blend against equal weights.
4. **Keep tilts modest.** "Sin a little" rather than make big calls.
5. **Pair rebalancing with trend.** Pure rebalancing is a bet on mean reversion; a trend component protects in long sell-offs.
6. **Use regimes to stress-test,** not to bet the fund on calling the next one.
7. **Hold a high bar for evidence.** Write hypotheses down first, count every trial, deflate Sharpe ratios, use realistic costs, and expect live results well below backtests.
8. **Look through private-asset smoothing** to the true exposures when deciding what the liquid portfolio should do.
9. **Plan liquidity and collateral** as carefully as return. Leverage can turn a market move into a funding problem.
10. **Treat ML and LLMs as tools, not oracles.** Small samples and look-ahead bias are real dangers.

---

## Additional verified sources cited in the text (not in `literature.json`)

- Andonov, A., Bauer, R., Cremers, M. (2017). Pension Fund Asset Allocation and Liability Discount Rates. *Review of Financial Studies* 30(8). https://doi.org/10.1093/rfs/hhx020
- Ang, A., Goetzmann, W.N., Schaefer, S.M. (2009). Evaluation of Active Management of the Norwegian Government Pension Fund - Global. Report to the Norwegian Ministry of Finance. https://www.regjeringen.no/en/documents/report-no.-10-2009-2010/id599137/?ch=6
- Arnott, R.D., von Germeten, J.N. (1983). Systematic Asset Allocation. *Financial Analysts Journal* 39(6). https://doi.org/10.2469/faj.v39.n6.31
- Barroso, P., Santa-Clara, P. (2015). Momentum Has Its Moments. *Journal of Financial Economics* 116(1). https://doi.org/10.1016/j.jfineco.2014.11.010
- Bianchi, D., Büchner, M., Tamoni, A. (2021). Bond Risk Premiums with Machine Learning. *Review of Financial Studies* 34(2). https://doi.org/10.1093/rfs/hhaa062
- Black, F., Perold, A.F. (1992). Theory of Constant Proportion Portfolio Insurance. *Journal of Economic Dynamics and Control* 16(3-4). https://doi.org/10.1016/0165-1889(92)90043-E
- Bollerslev, T., Hood, B., Huss, J., Pedersen, L.H. (2018). Risk Everywhere: Modeling and Managing Volatility. *Review of Financial Studies* 31(7). https://doi.org/10.1093/rfs/hhy041
- Bybee, J.L. (2023). The Ghost in the Machine: Generating Beliefs with Large Language Models. Working paper. https://arxiv.org/abs/2305.02823
- Chekhlov, A., Uryasev, S., Zabarankin, M. (2005). Drawdown Measure in Portfolio Optimization. *International Journal of Theoretical and Applied Finance* 8(1). https://doi.org/10.1142/S0219024905002767
- Cochrane, J.H., Piazzesi, M. (2005). Bond Risk Premia. *American Economic Review* 95(1). https://doi.org/10.1257/0002828053828581
- Fama, E.F., French, K.R. (1989). Business Conditions and Expected Returns on Stocks and Bonds. *Journal of Financial Economics* 25(1). https://doi.org/10.1016/0304-405X(89)90095-0
- Glasserman, P., Lin, C. (2023). Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis. arXiv 2309.17322. https://arxiv.org/abs/2309.17322
- Goulding, C.L., Harvey, C.R., Mazzoleni, M.G. (2023). Momentum Turning Points. *Journal of Financial Economics* 149(3). https://doi.org/10.1016/j.jfineco.2023.05.007
- Hamill, C., Rattray, S., Van Hemert, O. (2016). Trend Following: Equity and Bond Crisis Alpha. SSRN 2831926. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2831926
- Harvey, C.R., Liu, Y. (2015). Backtesting. *Journal of Portfolio Management* 42(1). https://doi.org/10.3905/jpm.2015.42.1.013
- He, G., Litterman, R. (1999). The Intuition Behind Black-Litterman Model Portfolios. Goldman Sachs Investment Management Research. https://econbiz.de/Record/the-intuition-behind-black-litterman-model-portfolios-guangliang/10012740844
- Hou, K., Xue, C., Zhang, L. (2020). Replicating Anomalies. *Review of Financial Studies* 33(5). https://doi.org/10.1093/rfs/hhy131
- Ilmanen, A. (2022). *Investing Amid Low Expected Returns: Making the Most When Markets Offer the Least*. Wiley.
- Ilmanen, A., Chandra, S., McQuinn, N. (2020). Demystifying Illiquid Assets: Expected Returns for Private Equity. *Journal of Alternative Investments*. https://www.aqr.com/insights/research/journal-article/demystifying-illiquid-assets-expected-returns-for-private-equity
- Ilmanen, A., Israel, R., Lee, R., Moskowitz, T.J., Thapar, A. (2021). How Do Factor Premia Vary Over Time? A Century of Evidence. *Journal of Investment Management* 19(4). https://papers.ssrn.com/abstract=3400998
- Jegadeesh, N., Titman, S. (1993). Returns to Buying Winners and Selling Losers. *Journal of Finance* 48(1). https://doi.org/10.1111/j.1540-6261.1993.tb04702.x
- Kelly, B., Malamud, S. (2025). Understanding the Virtue of Complexity. SSRN 5346842. https://papers.ssrn.com/abstract=5346842
- Kelly, B., Xiu, D. (2023). Financial Machine Learning. *Foundations and Trends in Finance* 13(3-4). https://doi.org/10.1561/0500000064
- Kim, A.Y., Tse, Y., Wald, J.K. (2016). Time Series Momentum and Volatility Scaling. *Journal of Financial Markets* 30. https://doi.org/10.1016/j.finmar.2016.05.003
- Liu, F., Tang, X., Zhou, G. (2019). Volatility-Managed Portfolio: Does It Really Work? *Journal of Portfolio Management* 46(1). https://doi.org/10.2139/ssrn.3283395
- Lo, A.W. (2002). The Statistics of Sharpe Ratios. *Financial Analysts Journal* 58(4). https://doi.org/10.2469/faj.v58.n4.2453
- López de Prado, M. (2016). Building Diversified Portfolios that Outperform Out of Sample. *Journal of Portfolio Management* 42(4). https://doi.org/10.3905/jpm.2016.42.4.059
- Markowitz, H. (1952). Portfolio Selection. *Journal of Finance* 7(1). https://doi.org/10.1111/j.1540-6261.1952.tb01525.x
- Neely, C.J., Rapach, D.E., Tu, J., Zhou, G. (2014). Forecasting the Equity Risk Premium: The Role of Technical Indicators. *Management Science* 60(7). https://doi.org/10.1287/mnsc.2013.1838
- Nystrup, P., Madsen, H., Lindström, E. (2018). Dynamic Portfolio Optimization across Hidden Market Regimes. *Quantitative Finance* 18(1). https://doi.org/10.1080/14697688.2017.1342857
- Page, S., Taborsky, M.A. (2011). The Myth of Diversification: Risk Factors versus Asset Classes. *Journal of Portfolio Management* 37(4).
- Pinter, G., Siriwardane, E., Walker, D. (2024). Fire sales of safe assets. Bank of England Staff Working Paper No. 1,089. https://www.bankofengland.co.uk/working-paper/2024/fire-sales-of-safe-assets
- Podolsky, P., Johnson, R., Jennings, O. (2012). The All Weather Story. Bridgewater Associates. https://www.bridgewater.com/research-and-insights/the-all-weather-story
- Sharpe, W.F. (1987). Integrated Asset Allocation. *Financial Analysts Journal* 43(5). https://doi.org/10.2469/faj.v43.n5.25
- Shu, Y., Yu, C., Mulvey, J.M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. *Journal of Asset Management* 25(5). https://doi.org/10.1057/s41260-024-00376-x
- White, H. (2000). A Reality Check for Data Snooping. *Econometrica* 68(5). https://doi.org/10.1111/1468-0262.00152
