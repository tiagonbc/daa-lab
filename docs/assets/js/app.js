/* DAA Lab - pages and router. All numbers come from data/*.json produced by daalab/pipeline.py */
'use strict';

const app = document.getElementById('app');
const UI = { period: 'full', showBench: true, family: 'all', q: '', sort: 'sharpe', asc: false, homeRange: 'full' };
const BENCH_IDS = ['bench_6040', 'bench_global_6040', 'bench_otpp_mix', 'bench_spy'];
const FAMILY_LABEL = { 'momentum-rotation': 'Momentum rotation', 'trend-following': 'Trend following', 'risk-parity': 'Risk-based', static: 'Static', macro: 'Macro', valuation: 'Valuation', other: 'Other', blend: 'Blend' };
const PERIODS = [['full', 'Full history'], ['since2008', 'Since 2008'], ['10y', 'Last 10 years'], ['5y', 'Last 5 years']];

async function core() {
  const [meta, strats, rets, blend] = await Promise.all([load('meta.json'), load('strategies.json'), load('returns.json'), load('blend.json')]);
  const byId = Object.fromEntries(strats.map(s => [s.id, s]));
  return { meta, strats, rets, blend, byId };
}
const nameOf = (byId, id) => id === 'blend' ? "Tiago's DAA Blend" : (byId[id]?.name ?? id);
const firstIdx = r => r.findIndex(v => v != null);

/* ================================================================== OVERVIEW */
async function pageHome() {
  const { meta, strats, rets, blend, byId } = await core();
  const D = rets.dates, S = rets.series;
  const b0 = firstIdx(S.blend), n1 = D.length - 1;
  const mB = stats(S.blend.slice(b0), rets.cash.slice(b0), S.bench_6040.slice(b0), D.slice(b0));
  const m6 = stats(S.bench_6040.slice(b0), rets.cash.slice(b0), S.bench_6040.slice(b0), D.slice(b0));
  const nStrat = strats.filter(s => !s.benchmark).length;
  const comps = blend.current_components;
  const tiles = [
    ['Annualized return', fmt.pct(mB.cagr), fmt.pct(m6.cagr), 'cagr'],
    ['Volatility', fmt.pct(mB.vol), fmt.pct(m6.vol), 'vol'],
    ['Sharpe ratio', fmt.num(mB.sharpe), fmt.num(m6.sharpe), 'sharpe'],
    ['Max drawdown', fmt.pct(mB.max_dd), fmt.pct(m6.max_dd), 'max_dd'],
    ['Ulcer index', fmt.pct(mB.ulcer), fmt.pct(m6.ulcer), 'ulcer'],
    ['Worst year', fmt.pct(mB.worst_year), fmt.pct(m6.worst_year), 'worst_year'],
  ];
  app.innerHTML = `
  <section class="hero">
    <div class="eyebrow">Tiago's demonstration · Dynamic Asset Allocation</div>
    <h1>${nStrat} published tactical allocation strategies, rebuilt from scratch and blended into one portfolio I track every month.</h1>
    <p class="lede">Each strategy shifts money between stocks, bonds, real assets and cash when markets or the economy change. Every December the blend keeps the <b>top ${blend.config.n} strategies that don't move together</b>, judged only on information available at the time. So the ${(mB.months / 12).toFixed(0)}-year record below is out-of-sample: no hindsight.</p>
    <div class="status-row">
      <span class="badge-live">Live tracking</span>
      <span>Signals as of <b>${fmt.date(meta.signal_date)}</b></span>
      <span>Next rebalance <b>${fmt.date(meta.next_rebalance)}</b></span>
      <span>Data through <b>${fmt.date(meta.data_through)}</b></span>
    </div>
  </section>
  <section>
    <div class="kpis">${tiles.map(t => `<div class="kpi"><div class="label">${t[0]} ${tip(meta.glossary[t[3]])}</div><div class="value">${t[1]}</div><div class="cmp">60/40: ${t[2]}</div></div>`).join('')}</div>
    <p class="small muted" style="margin-top:8px">Tiago's DAA Blend vs a 60% US stock / 40% US Treasury portfolio, ${fmt.ym(mB.start)} – ${fmt.ym(mB.end)}, monthly, after 0.10% trading costs.</p>
  </section>
  <section class="card">
    <div class="chart-head">
      <div><h3>Growth of $100</h3><div class="sub" style="margin:0">Log scale: equal vertical distances mean equal percentage gains.</div></div>
      <div class="seg" id="rng">${[['full', 'All'], ['10y', '10Y'], ['5y', '5Y'], ['3y', '3Y']].map(([k, l]) => `<button data-k="${k}" class="${UI.homeRange === k ? 'on' : ''}">${l}</button>`).join('')}</div>
    </div>
    <div id="legend-g"></div>
    <div id="c-growth" class="chart lg"></div>
    <h3 style="margin-top:14px">Drawdowns <span class="muted small">(how far below its previous high each portfolio was)</span></h3>
    <div id="c-dd" class="chart sm"></div>
  </section>
  <section class="grid-2">
    <div class="card">
      <h3>What the blend holds now</h3>
      <div class="sub">Average of the ${comps.length} components' current signals, set at the close on ${fmt.date(meta.signal_date)}.</div>
      ${classBar(blend.current_by_class)}
      <div class="alloc" style="margin-top:14px">${allocRows(blend.current_allocation, meta)}</div>
    </div>
    <div class="card">
      <h3>This year's ${comps.length} components</h3>
      <div class="sub">Chosen in ${fmt.ym(blend.selections.at(-1).date)} from ${blend.selections.at(-1).n_eligible} eligible strategies (5+ years of history).</div>
      <table class="compact"><thead><tr><th>Strategy</th><th>Holding now</th><th class="num">Sharpe</th></tr></thead><tbody>
      ${comps.map(id => { const s = byId[id]; return `<tr class="click" data-href="#/s/${id}"><td><div class="sname">${esc(s.name)}</div><div class="sauth">${esc(s.author)} · ${s.year}</div></td><td>${holdChips(s.current)}</td><td class="num">${fmt.num(s.metrics.sharpe)}</td></tr>`; }).join('')}
      </tbody></table>
      <p style="margin-top:14px"><a class="btn" href="#/blend">How the blend is built →</a></p>
    </div>
  </section>
  <section>
    <div class="section-head"><div><h2>How it works, in four steps</h2><p>Simple rules, applied the same way every month, documented and testable.</p></div></div>
    <div class="steps">
      <div class="step"><h3>Rebuild the research</h3><p>${nStrat} strategies from the tactical-allocation literature (Faber, Antonacci, Keller, Butler and others, plus macro-factor models), coded from their original rules and run on the same data.</p></div>
      <div class="step"><h3>Test fairly</h3><p>Same data (Norgate, dividends reinvested), same timing (trade at the month-end close), same 0.10% trading cost. Before ETFs existed, validated index proxies fill the history.</p></div>
      <div class="step"><h3>Pick without hindsight</h3><p>Each December, rank strategies on Sharpe and Ulcer Performance over the past 10 years. Walk down the list and skip any whose returns correlate above ${blend.config.corr_cap} with one already chosen.</p></div>
      <div class="step"><h3>Track it live</h3><p>The blend holds its ${blend.config.n} picks in equal weights. Every month the pipeline reruns and publishes new signals, and Git commits timestamp each one before its returns are known.</p></div>
    </div>
  </section>
  <section class="grid-3">
    <a class="card flat" href="#/strategies"><h3>Strategy library →</h3><p class="muted small">All ${nStrat} strategies, sortable by any metric, with rules in plain English.</p></a>
    <a class="card flat" href="#/builder"><h3>Build your own mix →</h3><p class="muted small">Combine strategies like a portfolio and see the combined risk and return.</p></a>
    <a class="card flat" href="#/note"><h3>This month's DAA note →</h3><p class="muted small">A one-page, committee-style summary of positioning, macro backdrop and risks.</p></a>
  </section>`;

  const draw = () => {
    disposeCharts();
    const [i0, i1] = UI.homeRange === 'full' ? [b0, n1] : windowIdx(D, UI.homeRange);
    const st = Math.max(i0, b0);
    const list = [
      { name: "Tiago's DAA Blend", r: S.blend, color: ENTITY.blend, width: 2.5, z: 5 },
      { name: '60/40 (US)', r: S.bench_6040, color: ENTITY.bench_6040 },
      { name: 'Global 60/40', r: S.bench_global_6040, color: ENTITY.bench_global_6040 },
      { name: 'S&P 500', r: S.bench_spy, color: ENTITY.bench_spy, width: 1.5 },
    ];
    document.getElementById('legend-g').innerHTML = legendHTML(list);
    growthChart('c-growth', D, list, st, i1);
    drawdownChart('c-dd', D, list, st, i1);
  };
  draw();
  document.getElementById('rng').addEventListener('click', e => { const k = e.target.dataset.k; if (!k) return; UI.homeRange = k; document.querySelectorAll('#rng button').forEach(b => b.classList.toggle('on', b.dataset.k === k)); draw(); });
}

function classBar(byClass) {
  const tot = Object.values(byClass).reduce((a, b) => a + Math.max(0, b), 0) || 1;
  const parts = CLASS_ORDER.filter(c => byClass[c] > 0.0005);
  return `<div class="stackbar" role="img" aria-label="allocation by asset class">${parts.map(c => `<div title="${c} ${fmt.pct(byClass[c])}" style="flex:${byClass[c] / tot};background:${CLASS_COLORS[c]}"></div>`).join('')}</div>
  ${legendHTML(parts.map(c => ({ name: `${c} ${fmt.pct(byClass[c], 0)}`, color: CLASS_COLORS[c] })), true)}`;
}
function allocRows(pairs, meta, limit = 12) {
  const max = Math.max(...pairs.map(p => Math.abs(p[1])), 0.01);
  const shown = pairs.filter(p => Math.abs(p[1]) >= 0.005).slice(0, limit);
  return shown.map(([t, w]) => { const a = meta.assets[t] || {}; const col = CLASS_COLORS[a.class] || C.violet;
    return `<div class="alloc-row"><span class="t">${esc(t)}</span><span class="bar"><b style="width:${Math.abs(w) / max * 100}%;background:${col}"></b></span><span class="v">${fmt.pct(w, 1)}</span><span class="d">${esc(a.name || '')}</span></div>`; }).join('');
}
function holdChips(cur, limit = 4) {
  const items = cur.filter(c => c.weight > 0.005).slice(0, limit);
  return `<div class="chips">${items.map(c => `<span class="chip"><span class="sw" style="background:${CLASS_COLORS[c.class] || C.violet}"></span>${esc(c.ticker)} ${fmt.pct(c.weight, 0)}</span>`).join('')}</div>`;
}

/* ================================================================== THE BLEND */
const EPISODES = [
  ['Dot-com bust', '2000-09', '2002-09'], ['Global financial crisis', '2007-11', '2009-02'], ['2009 rebound', '2009-03', '2009-12'],
  ['Euro debt crisis', '2011-05', '2011-09'], ['2015–16 growth scare', '2015-06', '2016-02'], ['Q4 2018 sell-off', '2018-10', '2018-12'],
  ['COVID crash', '2020-02', '2020-03'], ['2020 rebound', '2020-04', '2020-12'], ['2022 inflation shock', '2022-01', '2022-12'],
  ['2025 tariff shock', '2025-02', '2025-04'],
];
function episodeReturn(r, D, a, b) {
  const i = D.indexOf(a), j = D.indexOf(b); if (i < 0 || j < 0) return null;
  let eq = 1; for (let k = i; k <= j; k++) { if (r[k] == null) return null; eq *= 1 + r[k]; } return eq - 1;
}

async function pageBlend() {
  const { meta, strats, rets, blend, byId } = await core();
  const D = rets.dates, S = rets.series, b0 = firstIdx(S.blend);
  const isR = D.map(d => blend.in_sample_returns[d] ?? null);
  const mWF = stats(S.blend.slice(b0), rets.cash.slice(b0), null, D.slice(b0));
  const mIS = stats(isR.slice(b0), rets.cash.slice(b0), null, D.slice(b0));
  const sens = blend.sensitivity || [];
  const ns = [...new Set(sens.map(x => x.n))], caps = [...new Set(sens.map(x => x.cap))];
  const sels = blend.selections;
  // strategy "consensus": average risky-asset weight across all strategies (from component data)
  app.innerHTML = `
  <section class="hero">
    <div class="eyebrow">The Blend</div>
    <h1>Picking strategies is itself a strategy, so I test it the same way.</h1>
    <p class="lede">Choosing the "best" backtest with hindsight is the most common way to fool yourself in quantitative investing. Here each year's choice uses <b>only data available that December</b>. The page shows every pick, the rules behind it, and how much the result depends on the settings.</p>
  </section>
  <section class="grid-2">
    <div class="card">
      <h3>The selection rule</h3>
      <ol class="rules">
        <li>Eligible: any strategy with at least ${blend.config.min_history / 12} years of track record.</li>
        <li>Score: average rank on <b>Sharpe ratio</b> ${tip(meta.glossary.sharpe)} and <b>Ulcer Performance Index</b> ${tip(meta.glossary.upi)} over the last ${blend.config.window / 12} years.</li>
        <li>Walk down the ranking; accept a strategy only if its monthly-return correlation with every accepted strategy is ≤ <b>${blend.config.corr_cap}</b>.</li>
        <li>Stop at <b>${blend.config.n}</b>. Hold them in equal weights for 12 months, then repeat.</li>
      </ol>
      <p class="small muted">Defaults were fixed before seeing results: N=${blend.config.n}, correlation cap ${blend.config.corr_cap}, ${blend.config.window / 12}-year window.</p>
    </div>
    <div class="card">
      <h3>Hindsight vs honest</h3>
      <div class="sub">Same rule, but "hindsight" ranks strategies using the whole 2000–today history, which no investor had in 2005.</div>
      <table><thead><tr><th></th><th class="num">CAGR</th><th class="num">Sharpe</th><th class="num">Max DD</th><th class="num">UPI</th></tr></thead><tbody>
        <tr><td><b>Walk-forward (honest)</b></td><td class="num">${fmt.pct(mWF.cagr)}</td><td class="num">${fmt.num(mWF.sharpe)}</td><td class="num">${fmt.pct(mWF.max_dd)}</td><td class="num">${fmt.num(mWF.upi)}</td></tr>
        <tr><td>Hindsight pick</td><td class="num">${fmt.pct(mIS.cagr)}</td><td class="num">${fmt.num(mIS.sharpe)}</td><td class="num">${fmt.pct(mIS.max_dd)}</td><td class="num">${fmt.num(mIS.upi)}</td></tr>
      </tbody></table>
      <p class="small" style="margin-top:10px">Hindsight picks: ${blend.in_sample_pick.map(id => `<a href="#/s/${id}">${esc(nameOf(byId, id))}</a>`).join(', ')}.</p>
      <div class="callout small">The gap between the two rows is the <b>selection-bias haircut</b>: how much a backtest flatters you when you pick winners after the fact (Bailey &amp; López de Prado, 2014).</div>
    </div>
  </section>
  <section class="card">
    <div class="chart-head"><h3>Every December's pick</h3><span class="small muted">Red = still in this year's blend</span></div>
    <div class="table-wrap"><table class="compact"><thead><tr><th>Chosen</th><th>Components for the next 12 months</th></tr></thead><tbody>
    ${sels.slice().reverse().map(s => `<tr><td class="mono">${s.date.slice(0, 4)}<div class="sauth">${s.n_eligible} eligible</div></td><td><div class="chips">${s.chosen.map(id => `<a class="chip ${blend.current_components.includes(id) ? 'red' : ''}" href="#/s/${id}">${esc(nameOf(byId, id))}</a>`).join('')}</div></td></tr>`).join('')}
    </tbody></table></div>
  </section>
  <section class="grid-2">
    <div class="card">
      <h3>How much do the settings matter?</h3>
      <div class="sub">Walk-forward Sharpe ratio for every combination of N (rows) and correlation cap (columns). A robust process looks similar across the grid.</div>
      <div class="table-wrap"><table class="heat"><thead><tr><th>N \\ cap</th>${caps.map(c => `<th>${c}</th>`).join('')}</tr></thead><tbody>
      ${ns.map(n => `<tr><th>${n}</th>${caps.map(c => { const x = sens.find(z => z.n === n && z.cap === c); const v = x?.sharpe; const lo = Math.min(...sens.map(z => z.sharpe)), hi = Math.max(...sens.map(z => z.sharpe)); const u = (v - lo) / ((hi - lo) || 1); const bg = `rgba(31,95,174,${0.12 + 0.78 * u})`; const isDef = n === blend.config.n && c === blend.config.corr_cap; return `<td title="CAGR ${fmt.pct(x?.cagr)} · Max DD ${fmt.pct(x?.max_dd)}" style="background:${bg};color:${u > 0.55 ? '#fff' : C.aub};${isDef ? 'outline:2px solid ' + C.red : ''}">${fmt.num(v)}</td>`; }).join('')}</tr>`).join('')}
      </tbody></table></div>
      <p class="small muted" style="margin-top:8px">Red outline = default setting. Hover a cell for CAGR and max drawdown. A cap of 1.0 means "ignore correlation": just the top N.</p>
    </div>
    <div class="card">
      <h3>Stress tests</h3>
      <div class="sub">Cumulative return through past market episodes.</div>
      <div class="table-wrap"><table class="compact"><thead><tr><th>Episode</th><th class="num">Blend</th><th class="num">60/40</th><th class="num">OTPP-shaped</th><th class="num">S&amp;P 500</th></tr></thead><tbody>
      ${EPISODES.map(([n, a, b]) => { const v = [S.blend, S.bench_6040, S.bench_otpp_mix, S.bench_spy].map(r => episodeReturn(r, D, a, b)); return `<tr><td>${n}<div class="sauth">${fmt.ym(a)} – ${fmt.ym(b)}</div></td>${v.map(x => `<td class="num ${signCls(x)}">${fmt.spct(x)}</td>`).join('')}</tr>`; }).join('')}
      </tbody></table></div>
    </div>
  </section>
  <section class="card" id="overlay">
    <div class="section-head" style="margin-bottom:6px"><div><div class="eyebrow">From strategy to total fund</div><h2>Using the blend as a DAA overlay with an active-risk budget</h2>
    <p>A pension fund doesn't swap its whole portfolio into a tactical strategy. It keeps its policy mix and runs <b>tilts</b> on top, sized to an active-risk (tracking-error) budget. Here the blend's view (blend minus a neutral global 60/40) is scaled each month so its expected tracking error matches the budget, then added to a reference portfolio.</p></div></div>
    <div class="toolbar">
      <label class="small">Reference portfolio <select class="input" id="ov-ref"><option value="bench_otpp_mix">OTPP-shaped mix (liquid proxy)</option><option value="bench_global_6040">Global 60/40</option><option value="bench_6040">US 60/40</option></select></label>
      <label class="small">Active-risk budget <input type="range" id="ov-te" min="0.5" max="4" step="0.25" value="1.5"> <b id="ov-te-v" class="mono">1.50%</b></label>
    </div>
    <div class="kpis light" id="ov-kpis"></div>
    <div id="ov-legend" style="margin-top:12px"></div>
    <div id="c-ov" class="chart md"></div>
    <p class="small muted" id="ov-scale"></p>
  </section>
  <section class="card">
    <h3>Blend holdings over time, by asset class</h3>
    <div class="sub">Average of the components' signals each month. A dynamic allocator should visibly change its mix when conditions change.</div>
    ${legendHTML(CLASS_ORDER.slice(0, 4).map(c => ({ name: c, color: CLASS_COLORS[c] })), true)}
    <div id="c-cls" class="chart md"></div>
  </section>
  ${blend.consensus ? `<section class="card">
    <h3>Strategy consensus: what all ${strats.filter(s => !s.benchmark).length} strategies hold, on average</h3>
    <div class="sub">A sentiment gauge for tactical allocators. When most trend and momentum models retreat to bonds and cash at once (2008, 2020, 2022), it usually signals a broad risk-off phase.</div>
    ${legendHTML(CLASS_ORDER.slice(0, 4).map(c => ({ name: c, color: CLASS_COLORS[c] })), true)}
    <div id="c-cons" class="chart md"></div>
  </section>` : ''}
  <section class="card">
    <h3>Calendar-year returns</h3>
    ${legendHTML([{ name: "Tiago's DAA Blend", color: ENTITY.blend }, { name: '60/40 (US)', color: ENTITY.bench_6040 }], true)}
    <div id="c-ann" class="chart md"></div>
  </section>`;

  // class history
  const ch = blend.class_history; const cd = Object.keys(ch);
  const byC = {}; CLASS_ORDER.slice(0, 4).forEach(c => byC[c] = cd.map(d => +(ch[d][c] || 0).toFixed(4)));
  stackedClasses('c-cls', cd, byC, CLASS_ORDER.slice(0, 4));
  if (blend.consensus) {
    const cdates = Object.keys(blend.consensus).filter(d => d >= '2000-01');
    const byK = {}; CLASS_ORDER.slice(0, 4).forEach(c => byK[c] = cdates.map(d => +(Math.max(0, blend.consensus[d][c] || 0)).toFixed(4)));
    stackedClasses('c-cons', cdates, byK, CLASS_ORDER.slice(0, 4));
  }
  const yb = annual(S.blend, D), y6 = annual(S.bench_6040.map((v, i) => i >= b0 ? v : null), D);
  annualBars('c-ann', Object.keys(yb), [{ name: "Tiago's DAA Blend", values: yb, color: ENTITY.blend }, { name: '60/40 (US)', values: y6, color: ENTITY.bench_6040 }]);

  const ovChart = () => {
    const ref = document.getElementById('ov-ref').value, te = +document.getElementById('ov-te').value / 100;
    document.getElementById('ov-te-v').textContent = (te * 100).toFixed(2) + '%';
    const view = S.blend.map((v, i) => v == null || S.bench_global_6040[i] == null ? null : v - S.bench_global_6040[i]);
    const R = S[ref];
    const ov = new Array(D.length).fill(null), act = new Array(D.length).fill(null);
    for (let i = b0 + 36; i < D.length; i++) {
      const hist = view.slice(i - 36, i).filter(v => v != null); if (hist.length < 24 || view[i] == null || R[i] == null) continue;
      const m = hist.reduce((a, b) => a + b, 0) / hist.length; const sd = Math.sqrt(hist.reduce((a, b) => a + (b - m) ** 2, 0) / (hist.length - 1)) * Math.sqrt(12);
      const k = Math.min(1.5, te / sd); act[i] = k * view[i]; ov[i] = R[i] + act[i];
    }
    const i0 = firstIdx(ov), n = D.length;
    const a = act.slice(i0).filter(v => v != null);
    const mean = a.reduce((x, y) => x + y, 0) / a.length; const sd = Math.sqrt(a.reduce((x, y) => x + (y - mean) ** 2, 0) / (a.length - 1)) * Math.sqrt(12);
    const mO = stats(ov.slice(i0), rets.cash.slice(i0), R.slice(i0), D.slice(i0)), mR = stats(R.slice(i0), rets.cash.slice(i0), null, D.slice(i0));
    const ir = mean * 12 / sd, hit = a.filter(v => v > 0).length / a.length, c = corr(act.slice(i0), R.slice(i0));
    const va = mO.cagr - mR.cagr;
    document.getElementById('ov-kpis').innerHTML = [
      ['Value added / yr', fmt.spct(va, 2), 'Annualized return of reference + overlay, minus reference'],
      ['Realized tracking error', fmt.pct(sd, 2), 'Volatility of the overlay\'s active returns'],
      ['Information ratio', fmt.num(ir), 'Active return per unit of active risk; above 0.3 is good for a DAA program'],
      ['Hit rate', fmt.pct(hit, 0), 'Share of months the overlay added value'],
      ['Corr. with reference', fmt.num(c), 'Negative = the overlay tends to help when the reference portfolio is falling'],
      ['Max DD: ref → with overlay', `${fmt.pct(mR.max_dd, 0)} → ${fmt.pct(mO.max_dd, 0)}`, 'Worst peak-to-trough loss before and after the overlay'],
    ].map(t => `<div class="kpi"><div class="label">${t[0]} ${tip(t[2])}</div><div class="value" style="font-size:22px">${t[1]}</div></div>`).join('');
    const cum = []; let e = 1; for (let i = 0; i < n; i++) { if (i < i0 || act[i] == null) { cum.push(null); continue; } e *= 1 + act[i]; cum.push(e - 1); }
    disposeOv(); ovInst = mount('c-ov', base({
      xAxis: xCat(D.slice(i0)), yAxis: yVal({ axisLabel: { color: C.muted, formatter: v => (v * 100).toFixed(0) + '%' } }),
      tooltip: { ...base().tooltip, formatter: p => tipRows(p, v => fmt.spct(v, 2)) },
      series: [lineSeries('Cumulative value added', cum.slice(i0), C.red, { extra: { areaStyle: { color: C.red, opacity: 0.08 } } })],
    }));
    document.getElementById('ov-legend').innerHTML = legendHTML([{ name: 'Cumulative value added by the overlay (% of fund)', color: C.red }]);
    document.getElementById('ov-scale').innerHTML = `For scale: on OTPP's $279.4B of net assets (2025 annual report), every 0.10% of annual value added is about <b>$280M</b> a year. Hypothetical backtest, from ${fmt.ym(D[i0])}; the first 36 months are used to estimate tracking error.`;
  };
  let ovInst = null; const disposeOv = () => { if (ovInst) { ovInst.dispose(); CHARTS.splice(CHARTS.indexOf(ovInst), 1); ovInst = null; } };
  ovChart();
  document.getElementById('ov-ref').addEventListener('change', ovChart);
  document.getElementById('ov-te').addEventListener('input', ovChart);
}

/* ================================================================== STRATEGY LIBRARY */
async function pageStrategies() {
  const { meta, strats, rets, blend } = await core();
  const fams = ['all', ...new Set(strats.filter(s => !s.benchmark).map(s => s.family))];
  app.innerHTML = `
  <section class="hero">
    <div class="eyebrow">Strategy library</div>
    <h1>${strats.filter(s => !s.benchmark).length} tactical strategies on one scoreboard</h1>
    <p class="lede">Same data, same timing, same trading costs. Pick a period: metrics are recalculated in your browser from monthly returns. Click any row for the rules in plain English, charts and current holdings.</p>
  </section>
  <section>
    <div class="toolbar">
      <input type="search" id="q" placeholder="Search name, author, asset…" value="${esc(UI.q)}">
      <div class="seg" id="per">${PERIODS.map(([k, l]) => `<button data-k="${k}" class="${UI.period === k ? 'on' : ''}">${l}</button>`).join('')}</div>
      <select class="input" id="fam">${fams.map(f => `<option value="${f}" ${UI.family === f ? 'selected' : ''}>${f === 'all' ? 'All families' : FAMILY_LABEL[f] || f}</option>`).join('')}</select>
      <label class="check"><input type="checkbox" id="bench" ${UI.showBench ? 'checked' : ''}> Show benchmarks</label>
    </div>
    <div class="card" style="padding:0"><div class="table-wrap" id="tbl"></div></div>
    <p class="small muted" style="margin-top:8px">Red bar = in this year's blend. Strategies only report from the month their data allows. With "Full history", start dates differ, so compare like with like using "Since 2008" or "Last 10 years".</p>
  </section>
  <section class="card">
    <h3>How similar are they? Correlation map</h3>
    <div class="sub">Correlation of monthly returns since 2008, grouped by family. Dark blue = moves together (little diversification), grey = unrelated, red = moves opposite.</div>
    <div id="c-corr" class="chart" style="height:640px"></div>
  </section>`;
  const D = rets.dates;
  const cols = [
    ['name', 'Strategy', false], ['family', 'Family', false], ['start', 'Since', false],
    ['cagr', 'CAGR', true], ['vol', 'Volatility', true], ['sharpe', 'Sharpe', true], ['max_dd', 'Max DD', true],
    ['upi', 'UPI', true], ['worst_year', 'Worst yr', true], ['corr', 'Corr 60/40', true], ['spark', 'Growth', false], ['hold', 'Holding now', false],
  ];
  const gloss = { cagr: 'cagr', vol: 'vol', sharpe: 'sharpe', max_dd: 'max_dd', upi: 'upi', worst_year: 'worst_year', corr: 'corr_6040' };
  const render = () => {
    const [i0, i1] = windowIdx(D, UI.period);
    const q = UI.q.toLowerCase();
    let rows = strats.filter(s => (UI.showBench || !s.benchmark) && (UI.family === 'all' || s.family === UI.family || s.benchmark) &&
      (!q || (s.name + ' ' + s.author + ' ' + s.assets.map(a => a.ticker).join(' ')).toLowerCase().includes(q)))
      .map(s => { const r = rets.series[s.id].slice(i0, i1 + 1); const m = stats(r, rets.cash.slice(i0, i1 + 1), rets.series.bench_6040.slice(i0, i1 + 1), D.slice(i0, i1 + 1)); return { s, m }; })
      .filter(x => x.m);
    if (!q && UI.family === 'all') {
      const r = rets.series.blend.slice(i0, i1 + 1); const m = stats(r, rets.cash.slice(i0, i1 + 1), rets.series.bench_6040.slice(i0, i1 + 1), D.slice(i0, i1 + 1));
      if (m) rows.push({ s: { id: 'blend', name: "Tiago's DAA Blend", author: `Top ${blend.config.n} uncorrelated, walk-forward`, family: 'blend', current: blend.current_allocation.map(([t, w]) => ({ ticker: t, weight: w, class: meta.assets[t]?.class })) }, m, blendRow: true });
    }
    const key = UI.sort, dir = UI.asc ? 1 : -1;
    rows.sort((a, b) => { const va = key === 'name' ? a.s.name : key === 'family' ? a.s.family : key === 'start' ? a.m.start : a.m[key]; const vb = key === 'name' ? b.s.name : key === 'family' ? b.s.family : key === 'start' ? b.m.start : b.m[key];
      if (va == null) return 1; if (vb == null) return -1; return (va > vb ? 1 : va < vb ? -1 : 0) * dir; });
    document.getElementById('tbl').innerHTML = `<table><thead><tr>${cols.map(([k, l, num]) => `<th class="${num ? 'num ' : ''}${['spark', 'hold'].includes(k) ? '' : 'sortable'} ${UI.sort === k ? 'sorted' + (UI.asc ? ' asc' : '') : ''}" data-k="${k}">${l} ${gloss[k] ? tip(meta.glossary[gloss[k]]) : ''}</th>`).join('')}</tr></thead><tbody>
      ${rows.map(({ s, m, blendRow }) => `<tr class="click ${s.benchmark ? 'bench' : ''} ${blend.current_components.includes(s.id) || blendRow ? 'picked' : ''}" data-href="${blendRow ? '#/blend' : '#/s/' + s.id}">
        <td><div class="sname">${esc(s.name)}</div><div class="sauth">${esc(s.author)}${s.year && !blendRow ? ' · ' + s.year : ''}</div></td>
        <td class="small">${esc(FAMILY_LABEL[s.family] || s.family)}</td><td class="mono small">${m.start.slice(0, 4)}</td>
        <td class="num ${signCls(m.cagr)}">${fmt.pct(m.cagr)}</td><td class="num">${fmt.pct(m.vol)}</td><td class="num"><b>${fmt.num(m.sharpe)}</b></td>
        <td class="num neg">${fmt.pct(m.max_dd)}</td><td class="num">${fmt.num(m.upi)}</td><td class="num ${signCls(m.worst_year)}">${fmt.pct(m.worst_year)}</td><td class="num">${fmt.num(m.corr)}</td>
        <td>${sparkline(blendRow ? rets.series.blend : rets.series[s.id], i0, i1, 100, 26, blendRow ? C.red : C.aub)}</td><td>${holdChips(s.current || [], 3)}</td></tr>`).join('')}
    </tbody></table>`;
  };
  render();
  const corrMap = () => {
    const ids = strats.filter(s => !s.benchmark).sort((a, b) => (a.family + a.author).localeCompare(b.family + b.author)).map(s => s.id);
    const [i0] = windowIdx(D, 'since2008');
    const ser = ids.map(id => rets.series[id].slice(i0));
    const data = []; for (let a = 0; a < ids.length; a++) for (let b = 0; b < ids.length; b++) { const v = corr(ser[a], ser[b]); data.push([b, a, v == null ? null : +v.toFixed(2)]); }
    const short = id => { const n = strats.find(s => s.id === id).name; return n.length > 30 ? n.slice(0, 29) + '…' : n; };
    mount('c-corr', base({
      grid: { left: 210, right: 20, top: 10, bottom: 20 }, tooltip: { trigger: 'item', backgroundColor: '#fff', borderColor: C.axis, textStyle: { color: C.aub, fontSize: 12 }, formatter: p => `${esc(strats.find(s => s.id === ids[p.value[1]]).name)}<br>${esc(strats.find(s => s.id === ids[p.value[0]]).name)}<br><b>ρ = ${p.value[2]}</b>` },
      xAxis: { type: 'category', data: ids.map(short), axisLabel: { show: false }, axisTick: { show: false }, axisLine: { show: false } },
      yAxis: { type: 'category', data: ids.map(short), inverse: true, axisLabel: { fontSize: 9.5, color: C.ink2 }, axisTick: { show: false }, axisLine: { show: false } },
      visualMap: { show: false, min: -1, max: 1, inRange: { color: ['#c40f2b', '#f0efec', '#9ec5f4', '#1f5fae', '#0d366b'] } },
      series: [{ type: 'heatmap', data, itemStyle: { borderColor: '#fff', borderWidth: 0.5 } }],
    }), 'canvas');
  };
  corrMap();
  document.getElementById('q').addEventListener('input', e => { UI.q = e.target.value; render(); });
  document.getElementById('fam').addEventListener('change', e => { UI.family = e.target.value; render(); });
  document.getElementById('bench').addEventListener('change', e => { UI.showBench = e.target.checked; render(); });
  document.getElementById('per').addEventListener('click', e => { const k = e.target.dataset.k; if (!k) return; UI.period = k; document.querySelectorAll('#per button').forEach(b => b.classList.toggle('on', b.dataset.k === k)); render(); });
  document.getElementById('tbl').addEventListener('click', e => { const th = e.target.closest('th.sortable'); if (th) { const k = th.dataset.k; UI.asc = UI.sort === k ? !UI.asc : (k === 'name' || k === 'family'); UI.sort = k; render(); } });
}

/* ================================================================== STRATEGY DETAIL */
async function pageStrategy(id) {
  const { meta, strats, rets, blend, byId } = await core();
  const s = byId[id]; if (!s) { app.innerHTML = '<p class="loading">Strategy not found.</p>'; return; }
  const W = await load(`weights/${id}.json`);
  const D = rets.dates, r = rets.series[id], i0 = firstIdx(r), i1 = D.length - 1;
  const m = stats(r.slice(i0), rets.cash.slice(i0), rets.series.bench_6040.slice(i0), D.slice(i0));
  const m6 = stats(rets.series.bench_6040.slice(i0), rets.cash.slice(i0), null, D.slice(i0));
  const inBlend = blend.current_components.includes(id);
  const others = strats.filter(x => x.id !== id && !x.benchmark).map(x => ({ x, c: corr(r, rets.series[x.id]) })).filter(z => z.c != null).sort((a, b) => b.c - a.c);
  const tiles = [['CAGR', fmt.pct(m.cagr), fmt.pct(m6.cagr), 'cagr'], ['Volatility', fmt.pct(m.vol), fmt.pct(m6.vol), 'vol'], ['Sharpe', fmt.num(m.sharpe), fmt.num(m6.sharpe), 'sharpe'],
    ['Max drawdown', fmt.pct(m.max_dd), fmt.pct(m6.max_dd), 'max_dd'], ['UPI', fmt.num(m.upi), fmt.num(m6.upi), 'upi'], ['Corr. 60/40', fmt.num(m.corr), '1.00', 'corr_6040']];
  const splices = s.assets.map(a => meta.assets[a.ticker]).filter(a => a && a.splices && a.splices.length > 1);
  app.innerHTML = `
  <div class="crumbs"><a href="#/strategies">Strategies</a> / ${esc(FAMILY_LABEL[s.family] || s.family)}</div>
  <h1>${esc(s.name)}</h1>
  <div class="meta-row"><span><b>${esc(s.author)}</b> · ${s.year}</span><span>Source: <a href="${esc(s.source.url)}" target="_blank" rel="noopener">${esc(s.source.title)}</a></span>
    ${s.allocatesmartly_url ? `<span><a href="${esc(s.allocatesmartly_url)}" target="_blank" rel="noopener">AllocateSmartly review</a></span>` : ''}
    <span>Rebalance: ${{ M: 'monthly', Q: 'quarterly', A: 'annually' }[s.rebalance]}</span>${inBlend ? '<span class="chip red">In this year\'s blend</span>' : ''}${s.benchmark ? '<span class="chip">Benchmark</span>' : ''}</div>
  <section class="split">
    <div class="card teal"><h3>In plain English</h3><p style="margin-top:6px">${esc(s.plain_english)}</p>
      <h3 style="margin-top:14px">The rules</h3><ol class="rules">${s.rules.map(x => `<li>${esc(x)}</li>`).join('')}</ol>
      ${s.notes ? `<p class="small" style="margin-top:10px"><b>Replication notes:</b> ${esc(s.notes)}</p>` : ''}</div>
    <div class="card"><h3>Holding now</h3><div class="sub">Signal at the close on ${fmt.date(s.signal_date)}${s.mtd != null ? ` · month-to-date ${fmt.spct(s.mtd)}` : ''}</div>
      <div class="alloc">${allocRows(s.current.map(c => [c.ticker, c.weight]), meta)}</div>
      <h3 style="margin-top:18px">Universe</h3><div class="chips" style="margin-top:6px">${s.assets.map(a => `<span class="chip" title="${esc(a.name)}"><span class="sw" style="background:${CLASS_COLORS[a.class] || C.violet}"></span>${esc(a.ticker)}</span>`).join('')}</div></div>
  </section>
  <section><div class="kpis light">${tiles.map(t => `<div class="kpi"><div class="label">${t[0]} ${tip(meta.glossary[t[3]])}</div><div class="value">${t[1]}</div><div class="cmp">60/40: ${t[2]}</div></div>`).join('')}</div>
  <p class="small muted" style="margin-top:6px">${fmt.ym(m.start)} – ${fmt.ym(m.end)} (${(m.months / 12).toFixed(1)} years). Worst year ${fmt.pct(m.worst_year)}, best year ${fmt.pct(m.best_year)}, positive months ${fmt.pct(m.pct_pos, 0)}, longest time under water ${m.longest_dd} months, turnover ${fmt.pct(s.metrics.turnover, 0)} a year.</p></section>
  <section class="card">${legendHTML([{ name: s.name, color: C.red }, { name: '60/40 (US)', color: C.blue }])}<div id="c-g" class="chart"></div><div id="c-d" class="chart sm"></div></section>
  <section class="card"><h3>What it held, month by month</h3><div class="sub">Target weights by asset class at each month-end.</div>${legendHTML(CLASS_ORDER.slice(0, 4).map(c => ({ name: c, color: CLASS_COLORS[c] })), true)}<div id="c-w" class="chart md"></div></section>
  <section class="card"><h3>Monthly returns</h3><div class="sub">Blue = gain, red = loss; darker = bigger. Last column = calendar year.</div><div class="table-wrap">${monthlyHeat(r, D)}</div></section>
  <section class="grid-2">
    <div class="card"><h3>Most similar strategies</h3><table class="compact"><tbody>${others.slice(0, 6).map(z => `<tr class="click" data-href="#/s/${z.x.id}"><td>${esc(z.x.name)}</td><td class="num">${fmt.num(z.c)}</td></tr>`).join('')}</tbody></table></div>
    <div class="card"><h3>Best diversifiers for it</h3><table class="compact"><tbody>${others.slice(-6).reverse().map(z => `<tr class="click" data-href="#/s/${z.x.id}"><td>${esc(z.x.name)}</td><td class="num">${fmt.num(z.c)}</td></tr>`).join('')}</tbody></table></div>
  </section>
  ${splices.length ? `<section class="card grey"><h3>Data notes</h3><p class="small">Before an ETF existed, its history is back-filled with a validated proxy (see <a href="#/method">Method &amp; Data</a>):</p><ul class="small">${splices.map(a => `<li><b>${a.ticker}</b>: ${a.splices.map(sp => `${esc(sp.source)} from ${sp.from.slice(0, 7)}`).join(' → ')}</li>`).join('')}</ul></section>` : ''}`;
  growthChart('c-g', D, [{ name: s.name, r, color: C.red, width: 2.5, z: 5 }, { name: '60/40 (US)', r: rets.series.bench_6040, color: C.blue }], Math.max(0, i0 - 1), i1);
  drawdownChart('c-d', D, [{ name: s.name, r, color: C.red }, { name: '60/40 (US)', r: rets.series.bench_6040, color: C.blue }], Math.max(0, i0 - 1), i1);
  const byC = {}; CLASS_ORDER.slice(0, 4).forEach(c => byC[c] = W.dates.map(() => 0));
  W.w.forEach((row, k) => row.forEach((w, j) => { const cl = meta.assets[W.assets[j]]?.class || 'Other'; if (byC[cl]) byC[cl][k] += w; }));
  stackedClasses('c-w', W.dates, byC, CLASS_ORDER.slice(0, 4));
}
function monthlyHeat(r, D) {
  const rows = {}; r.forEach((v, i) => { if (v == null) return; const [y, mo] = D[i].split('-'); (rows[y] ||= {})[+mo] = v; });
  const yrs = Object.keys(rows).sort().reverse();
  const cell = v => { if (v == null) return '<td></td>'; const bg = divergingColor(v, 0.08); return `<td style="background:${bg};color:${textOn(bg)}">${(v * 100).toFixed(1)}</td>`; };
  return `<table class="heat"><thead><tr><th></th>${['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'].map(x => `<th>${x}</th>`).join('')}<th>Year</th></tr></thead><tbody>
  ${yrs.map(y => { const yr = Object.values(rows[y]).reduce((a, b) => a * (1 + b), 1) - 1; const bg = divergingColor(yr, 0.3); return `<tr><th>${y}</th>${Array.from({ length: 12 }, (_, k) => cell(rows[y][k + 1])).join('')}<td style="background:${bg};color:${textOn(bg)};font-weight:600">${(yr * 100).toFixed(1)}</td></tr>`; }).join('')}</tbody></table>`;
}

/* ================================================================== PORTFOLIO BUILDER */
const BUILD = { sel: null };
async function pageBuilder() {
  const { meta, strats, rets, blend, byId } = await core();
  if (!BUILD.sel) BUILD.sel = Object.fromEntries(blend.current_components.map(id => [id, 1]));
  const list = strats.filter(s => !s.benchmark).sort((a, b) => a.name.localeCompare(b.name));
  app.innerHTML = `
  <section class="hero"><div class="eyebrow">Portfolio builder</div><h1>Combine strategies like building blocks</h1>
  <p class="lede">Pick strategies and weights. The combination rebalances to your weights every month. Diversifying across strategies that think differently usually smooths the ride more than picking the single "best" one.</p></section>
  <section class="split" style="grid-template-columns:minmax(0,1fr) minmax(0,2fr)">
    <div class="card"><div class="toolbar" style="margin-bottom:8px"><button class="btn ghost" id="preset-blend">Load this year's blend</button><button class="btn ghost" id="clear">Clear</button></div>
      <input type="search" class="input" id="bq" placeholder="Filter…" style="width:100%;margin-bottom:8px">
      <div id="blist" style="max-height:640px;overflow:auto"></div></div>
    <div>
      <div class="kpis light" id="bk"></div>
      <div class="card" style="margin-top:16px"><div class="toolbar" style="justify-content:space-between"><div id="bleg"></div><div class="seg" id="bper">${PERIODS.map(([k, l]) => `<button data-k="${k}" class="${UI.period === k ? 'on' : ''}">${l}</button>`).join('')}</div></div><div id="bg" class="chart"></div><div id="bd" class="chart sm"></div></div>
      <div class="grid-2" style="margin-top:16px"><div class="card"><h3>Combined holdings now</h3><div id="balloc" class="alloc" style="margin-top:10px"></div></div><div class="card"><h3>Correlation between your picks</h3><div id="bcorr" class="chart md"></div></div></div>
    </div>
  </section>`;
  const D = rets.dates;
  const drawList = () => {
    const q = (document.getElementById('bq').value || '').toLowerCase();
    document.getElementById('blist').innerHTML = list.filter(s => !q || (s.name + s.author).toLowerCase().includes(q)).map(s => `
      <div class="alloc-row" style="grid-template-columns:22px minmax(0,1fr) 56px;margin-bottom:4px">
        <input type="checkbox" data-id="${s.id}" ${BUILD.sel[s.id] ? 'checked' : ''} aria-label="include ${esc(s.name)}">
        <span><span class="sname small">${esc(s.name)}</span><br><span class="sauth">${esc(s.author)}</span></span>
        <input class="input mono" style="padding:3px 6px;width:56px" type="number" min="0" step="1" data-w="${s.id}" value="${BUILD.sel[s.id] ? Math.round(BUILD.sel[s.id] * 100 / Math.max(1, Object.values(BUILD.sel).reduce((a, b) => a + b, 0))) : ''}" ${BUILD.sel[s.id] ? '' : 'disabled'} aria-label="weight">
      </div>`).join('');
  };
  const compute = () => {
    disposeCharts();
    const ids = Object.keys(BUILD.sel).filter(k => BUILD.sel[k] > 0);
    const bk = document.getElementById('bk');
    if (!ids.length) { bk.innerHTML = '<div class="kpi" style="grid-column:1/-1">Select at least one strategy.</div>'; return; }
    const w = ids.map(k => BUILD.sel[k]); const tot = w.reduce((a, b) => a + b, 0);
    const mix = combine(ids.map(k => rets.series[k]), w);
    const [p0, i1] = windowIdx(D, UI.period); const i0 = Math.max(p0, firstIdx(mix));
    const m = stats(mix.slice(i0, i1 + 1), rets.cash.slice(i0, i1 + 1), rets.series.bench_6040.slice(i0, i1 + 1), D.slice(i0, i1 + 1));
    const m6 = stats(rets.series.bench_6040.slice(i0, i1 + 1), rets.cash.slice(i0, i1 + 1), null, D.slice(i0, i1 + 1));
    bk.innerHTML = [['CAGR', fmt.pct(m.cagr), fmt.pct(m6.cagr)], ['Volatility', fmt.pct(m.vol), fmt.pct(m6.vol)], ['Sharpe', fmt.num(m.sharpe), fmt.num(m6.sharpe)], ['Max drawdown', fmt.pct(m.max_dd), fmt.pct(m6.max_dd)], ['Worst year', fmt.pct(m.worst_year), fmt.pct(m6.worst_year)], ['Corr. 60/40', fmt.num(m.corr), '1.00']]
      .map(t => `<div class="kpi"><div class="label">${t[0]}</div><div class="value" style="font-size:24px">${t[1]}</div><div class="cmp">60/40: ${t[2]}</div></div>`).join('');
    const L = [{ name: 'Your mix', r: mix, color: C.red, width: 2.5, z: 5 }, { name: '60/40 (US)', r: rets.series.bench_6040, color: C.blue }];
    document.getElementById('bleg').innerHTML = legendHTML(L) + `<div class="small muted">${fmt.ym(D[i0])} – ${fmt.ym(D[i1])}</div>`;
    growthChart('bg', D, L, Math.max(0, i0 - 1), i1); drawdownChart('bd', D, L, Math.max(0, i0 - 1), i1);
    const acc = {}; ids.forEach((k, j) => byId[k].current.forEach(c => { acc[c.ticker] = (acc[c.ticker] || 0) + c.weight * w[j] / tot; }));
    document.getElementById('balloc').innerHTML = allocRows(Object.entries(acc).sort((a, b) => b[1] - a[1]), meta, 10);
    const data = []; ids.forEach((a, x) => ids.forEach((b, y) => { const v = corr(rets.series[a].slice(i0, i1 + 1), rets.series[b].slice(i0, i1 + 1)); data.push([x, y, v == null ? null : +v.toFixed(2)]); }));
    const lab = ids.map(k => byId[k].name.length > 22 ? byId[k].name.slice(0, 21) + '…' : byId[k].name);
    mount('bcorr', base({ grid: { left: 130, right: 10, top: 10, bottom: 70 }, tooltip: { trigger: 'item', backgroundColor: '#fff', borderColor: C.axis, textStyle: { color: C.aub }, formatter: p => `${esc(lab[p.value[0]])} · ${esc(lab[p.value[1]])}<br><b>ρ = ${p.value[2]}</b>` },
      xAxis: { type: 'category', data: lab, axisLabel: { rotate: 40, fontSize: 9.5 }, axisTick: { show: false } }, yAxis: { type: 'category', data: lab, axisLabel: { fontSize: 9.5 }, axisTick: { show: false } },
      visualMap: { show: false, min: -1, max: 1, inRange: { color: ['#c40f2b', '#f0efec', '#9ec5f4', '#1f5fae', '#0d366b'] } },
      series: [{ type: 'heatmap', data, label: { show: ids.length <= 8, fontSize: 10, formatter: p => p.value[2]?.toFixed(2) }, itemStyle: { borderColor: '#fff', borderWidth: 2 } }] }));
  };
  drawList(); compute();
  document.getElementById('blist').addEventListener('change', e => {
    const id = e.target.dataset.id, wid = e.target.dataset.w;
    if (id) { if (e.target.checked) BUILD.sel[id] = 1; else delete BUILD.sel[id]; drawList(); compute(); }
    if (wid) { BUILD.sel[wid] = Math.max(0, +e.target.value || 0); compute(); }
  });
  document.getElementById('bq').addEventListener('input', drawList);
  document.getElementById('preset-blend').addEventListener('click', () => { BUILD.sel = Object.fromEntries(blend.current_components.map(id => [id, 1])); drawList(); compute(); });
  document.getElementById('clear').addEventListener('click', () => { BUILD.sel = {}; drawList(); compute(); });
  document.getElementById('bper').addEventListener('click', e => { const k = e.target.dataset.k; if (!k) return; UI.period = k; document.querySelectorAll('#bper button').forEach(b => b.classList.toggle('on', b.dataset.k === k)); compute(); });
}

/* ================================================================== MACRO */
const MACRO_LABEL = {
  unemp: ['Unemployment rate', '%', 'Labour'], unemp_gap_low12: ['Unemployment vs 12-month low (Sahm-style)', 'pp', 'Labour'], payrolls_yoy: ['Payrolls, year over year', '%', 'Labour'],
  claims_4w_yoy: ['Jobless claims, year over year', '%', 'Labour'], cfnai_ma3: ['Chicago Fed activity index (3m avg)', '', 'Growth'], ism: ['ISM manufacturing PMI', '', 'Growth'],
  indpro_yoy: ['Industrial production, y/y', '%', 'Growth'], real_retail_yoy: ['Real retail sales, y/y', '%', 'Growth'], core_cpi_yoy: ['Core CPI inflation, y/y', '%', 'Inflation'],
  core_cpi_3m_ann: ['Core CPI, 3-month annualized', '%', 'Inflation'], cpi_yoy: ['Headline CPI, y/y', '%', 'Inflation'], m2_yoy: ['M2 money supply, y/y', '%', 'Inflation'],
  nfci: ['Financial conditions (NFCI, + = tight)', '', 'Financial'], baa_spread: ['Baa corporate spread over 10y', '%', 'Financial'], ccc_oas: ['CCC high-yield spread', '%', 'Financial'],
  vix: ['VIX implied volatility', '', 'Financial'], curve_10y3m: ['Yield curve: 10y minus 3m', '%', 'Rates'], real_10y: ['Real 10y yield (10y minus core CPI)', '%', 'Rates'],
  y10: ['10-year Treasury yield', '%', 'Rates'], y3m: ['3-month Treasury yield', '%', 'Rates'],
};
async function pageMacro() {
  const [{ meta, strats, rets, byId }, M] = await Promise.all([core(), load('macro.json')]);
  const macroStrats = strats.filter(s => s.family === 'macro');
  const last = k => { const a = M.series[k]; for (let i = a.length - 1; i >= 0; i--) if (a[i] != null) return [a[i], i]; return [null, -1]; };
  const zNow = k => { const a = M.series[k].filter(v => v != null); const [v] = last(k); const m = a.reduce((x, y) => x + y, 0) / a.length; const sd = Math.sqrt(a.reduce((x, y) => x + (y - m) ** 2, 0) / (a.length - 1)); return (v - m) / sd; };
  const keys = Object.keys(MACRO_LABEL).filter(k => M.series[k]);
  const groups = ['Growth', 'Labour', 'Inflation', 'Financial', 'Rates'];
  const F = M.factors;
  app.innerHTML = `
  <section class="hero"><div class="eyebrow">Macro</div><h1>What the economy is saying, and how macro-aware strategies listen</h1>
  <p class="lede">Prices react to the economy. A macro-factor approach (popularised by Macrosynergy's research on wealth management with macro factors) turns economic data into standardised scores (growth, inflation, labour, financial conditions) and tilts a balanced portfolio towards the assets those scores favour. The crucial detail: <b>use data only after it was published</b>. October's CPI is only usable from mid-November.</p></section>
  ${F ? `<section class="grid-2"><div class="card"><h3>Macro factor scores now</h3><div class="sub">Each factor is an average of standardised indicators (z-scores using only past data). 0 = normal; ±1 = unusually strong/weak.</div><div id="c-fac" class="chart md"></div></div>
     <div class="card"><h3>Growth vs inflation: the regime map</h3><div class="sub">Where the US economy sat over the last 36 months (latest = large dot). Each quadrant historically favoured different assets.</div><div id="c-reg" class="chart md"></div></div></section>
     <section class="card"><h3>Factor history</h3>${legendHTML(Object.keys(F.series).map((k, j) => ({ name: F.labels[k], color: SERIES[j] })))}<div id="c-fh" class="chart md"></div></section>` : ''}
  <section>
    <div class="section-head"><div><h2>Indicator dashboard</h2><p>Latest values available at the last month-end, after publication lags. The z-score compares today with the indicator's own history since 1990.</p></div></div>
    <div class="grid-3">${groups.map(g => `<div class="card"><h3>${g}</h3><table class="compact"><tbody>${keys.filter(k => MACRO_LABEL[k][2] === g).map(k => { const [v, i] = last(k); const z = zNow(k); return `<tr><td class="small">${MACRO_LABEL[k][0]}</td><td class="num">${v == null ? '–' : v.toFixed(2)}${MACRO_LABEL[k][1] === '%' ? '%' : ''}</td><td class="num ${z < 0 ? 'neg' : 'pos'}" title="z-score">${z > 0 ? '+' : ''}${z.toFixed(1)}σ</td></tr>`; }).join('')}</tbody></table></div>`).join('')}</div>
  </section>
  <section class="card"><div class="chart-head"><h3>Indicator history</h3><select class="input" id="msel">${keys.map(k => `<option value="${k}">${MACRO_LABEL[k][0]}</option>`).join('')}</select></div><div id="c-m" class="chart md"></div></section>
  ${macroStrats.length ? `<section class="card"><h3>Macro strategies in the lab</h3><table class="compact"><thead><tr><th>Strategy</th><th class="num">CAGR</th><th class="num">Sharpe</th><th class="num">Max DD</th><th>Holding now</th></tr></thead><tbody>${macroStrats.map(s => `<tr class="click" data-href="#/s/${s.id}"><td><div class="sname">${esc(s.name)}</div><div class="sauth">${esc(s.author)}</div></td><td class="num">${fmt.pct(s.metrics.cagr)}</td><td class="num">${fmt.num(s.metrics.sharpe)}</td><td class="num neg">${fmt.pct(s.metrics.max_dd)}</td><td>${holdChips(s.current)}</td></tr>`).join('')}</tbody></table></section>` : ''}
  <section class="card grey"><h3>Data and publication lags</h3><div class="table-wrap"><table class="compact"><thead><tr><th>Series</th><th>Source</th><th>Frequency</th><th>Lag applied</th><th>Latest period in data</th></tr></thead><tbody>
  ${Object.entries(M.info).map(([k, v]) => `<tr><td>${esc(v.description)}</td><td class="mono small">Norgate ${esc(v.symbol)}</td><td>${{ M: 'Monthly', Q: 'Quarterly', W: 'Weekly', D: 'Daily (market)' }[v.frequency]}</td><td>${v.frequency === 'D' ? 'none (market close)' : v.frequency === 'W' ? v.lag + ' days' : v.lag + ' month' + (v.lag > 1 ? 's' : '')}</td><td class="mono small">${esc(v.latest_reference)}</td></tr>`).join('')}
  </tbody></table></div><p class="small muted" style="margin-top:8px">Norgate stores the latest revised values rather than first-release vintages, so growth data such as payrolls is a little cleaner here than it was in real time. Market-based inputs (yields, spreads, VIX) are not revised.</p></section>`;
  const drawM = k => {
    const i = M.series[k].findIndex(v => v != null);
    const old = CHARTS.find(c => c.getDom().id === 'c-m'); if (old) { old.dispose(); CHARTS.splice(CHARTS.indexOf(old), 1); }
    mount('c-m', base({ xAxis: xCat(M.dates.slice(i)), yAxis: yVal({ scale: true }), tooltip: { ...base().tooltip, formatter: p => tipRows(p, v => v.toFixed(2)) }, series: [lineSeries(MACRO_LABEL[k][0], M.series[k].slice(i), C.red)] }));
  };
  drawM(keys[0]); document.getElementById('msel').addEventListener('change', e => drawM(e.target.value));
  if (F) {
    const fk = Object.keys(F.series); const lastF = fk.map(k => { const a = F.series[k]; for (let i = a.length - 1; i >= 0; i--) if (a[i] != null) return a[i]; return null; });
    mount('c-fac', base({ grid: { left: 150, right: 30, top: 10, bottom: 30 }, tooltip: { trigger: 'item', formatter: p => `${p.name}: <b>${p.value.toFixed(2)}</b>` },
      xAxis: yVal({ min: -2.5, max: 2.5 }), yAxis: { type: 'category', data: fk.map(k => F.labels[k]), axisTick: { show: false }, axisLine: { lineStyle: { color: C.axis } } },
      series: [{ type: 'bar', data: lastF.map(v => ({ value: v, itemStyle: { color: v >= 0 ? C.blue : C.red, borderRadius: v >= 0 ? [0, 4, 4, 0] : [4, 0, 0, 4] } })), barMaxWidth: 18, label: { show: true, position: 'right', formatter: p => p.value.toFixed(2), color: C.ink2 } }] }));
    const g = F.series.growth, inf = F.series.inflation; const n = F.dates.length; const pts = [];
    for (let i = n - 36; i < n; i++) if (g[i] != null && inf[i] != null) pts.push([g[i], inf[i], F.dates[i]]);
    mount('c-reg', base({ grid: { left: 50, right: 20, top: 20, bottom: 40 }, tooltip: { trigger: 'item', formatter: p => `${fmt.ym(p.value[2])}<br>Growth ${p.value[0].toFixed(2)} · Inflation ${p.value[1].toFixed(2)}` },
      xAxis: yVal({ name: 'Growth score →', nameLocation: 'middle', nameGap: 26, min: -3, max: 3 }), yAxis: yVal({ name: 'Inflation score →', nameLocation: 'middle', nameGap: 32, min: -3, max: 3 }),
      series: [{ type: 'line', data: pts, showSymbol: true, symbolSize: (v, p) => p.dataIndex === pts.length - 1 ? 14 : 6, lineStyle: { color: C.axis, width: 1 }, itemStyle: { color: C.red },
        markLine: { silent: true, symbol: 'none', lineStyle: { color: C.muted, width: 1, type: 'solid' }, data: [{ xAxis: 0 }, { yAxis: 0 }], label: { show: false } },
        markArea: { silent: true, label: { color: C.muted, fontSize: 11 }, data: [[{ coord: [0, 0], name: 'Reflation / overheating', label: { position: 'insideTopRight' }, itemStyle: { color: 'rgba(237,161,0,.06)' } }, { coord: [3, 3] }], [{ coord: [-3, 0], name: 'Stagflation', label: { position: 'insideTopLeft' }, itemStyle: { color: 'rgba(232,17,50,.05)' } }, { coord: [0, 3] }], [{ coord: [0, -3], name: 'Goldilocks', label: { position: 'insideBottomRight' }, itemStyle: { color: 'rgba(31,95,174,.05)' } }, { coord: [3, 0] }], [{ coord: [-3, -3], name: 'Deflationary slowdown', label: { position: 'insideBottomLeft' }, itemStyle: { color: 'rgba(0,160,163,.05)' } }, { coord: [0, 0] }]] } }] }));
    const i0 = F.dates.findIndex((d, i) => fk.every(k => F.series[k][i] != null));
    mount('c-fh', base({ xAxis: xCat(F.dates.slice(i0)), yAxis: yVal(), tooltip: { ...base().tooltip, formatter: p => tipRows(p, v => v.toFixed(2)) }, series: fk.map((k, j) => lineSeries(F.labels[k], F.series[k].slice(i0), SERIES[j], { width: 1.5 })) }));
  }
}

/* ================================================================== RESEARCH */
const RES = { theme: 'all', q: '' };
async function pageResearch() {
  let lit = []; try { lit = await load('literature.json'); } catch (e) { }
  const { strats } = await core();
  const themes = ['all', ...new Set(lit.map(p => p.theme))];
  let reviewHTML = ''; try { const r = await fetch('data/literature_review.html', { cache: 'no-cache' }); if (r.ok) reviewHTML = await r.text(); } catch (e) { }
  app.innerHTML = `
  <section class="hero"><div class="eyebrow">Research tracker</div><h1>The science of dynamic asset allocation, from 1986 to today</h1>
  <p class="lede">${lit.length} peer-reviewed papers, books and practitioner studies, each verified at the source and summarised in plain language. Red = an idea implemented in this lab.</p></section>
  <section class="split">
    <div>
      <div class="toolbar"><input type="search" id="rq" placeholder="Search title, author, finding…" value="${esc(RES.q)}"><select class="input" id="rt">${themes.map(t => `<option ${RES.theme === t ? 'selected' : ''} value="${esc(t)}">${t === 'all' ? 'All themes' : esc(t)}</option>`).join('')}</select></div>
      <div id="plist"></div>
    </div>
    <div><div class="card teal" style="position:sticky;top:80px"><h3>Reading guide</h3><p class="small" style="margin-top:6px">Start with <b>Foundations</b> (what DAA is), then <b>Momentum &amp; trend</b> and <b>Macro regimes</b> (why tactical signals work), then <b>Robustness &amp; overfitting</b> (why most backtests disappoint). <b>Current state</b> covers what changed after 2022: the stock-bond correlation turning positive, higher rates, and AI.</p>
      ${reviewHTML ? '<p><a class="btn" href="#/review">Read the full review →</a></p>' : ''}<p class="small muted">Strategies in the lab: ${strats.filter(s => !s.benchmark).length}</p></div></div>
  </section>`;
  const draw = () => {
    const q = RES.q.toLowerCase();
    const items = lit.filter(p => (RES.theme === 'all' || p.theme === RES.theme) && (!q || JSON.stringify(p).toLowerCase().includes(q))).sort((a, b) => b.year - a.year);
    let lastY = null;
    document.getElementById('plist').innerHTML = items.map(p => { const yh = p.year !== lastY ? `<div class="year-mark">${p.year}</div>` : ''; lastY = p.year;
      return `${yh}<div class="paper ${p.implemented_in_lab ? 'impl' : ''}"><a class="ttl" href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.title)}</a><div class="by">${esc(p.authors)} · ${esc(p.venue)} · <span class="chip">${esc(p.theme)}</span>${p.implemented_in_lab ? ' <span class="chip red">In the lab</span>' : ''}</div><p>${esc(p.key_finding)}</p><p class="small"><b>Why it matters for DAA:</b> ${esc(p.why_it_matters_for_daa)}</p></div>`; }).join('') || '<p class="muted">No papers match.</p>';
  };
  draw();
  document.getElementById('rq').addEventListener('input', e => { RES.q = e.target.value; draw(); });
  document.getElementById('rt').addEventListener('change', e => { RES.theme = e.target.value; draw(); });
}
async function pageReview() {
  const r = await fetch('data/literature_review.html', { cache: 'no-cache' });
  app.innerHTML = `<div class="crumbs"><a href="#/research">Research</a> / Literature review</div><article class="prose">${r.ok ? await r.text() : '<p>Review not available.</p>'}</article>`;
}

/* ================================================================== MONTHLY NOTE */
async function pageNote() {
  const { meta, strats, rets, blend, byId } = await core();
  let M = null; try { M = await load('macro.json'); } catch (e) { }
  const ch = blend.class_history; const ds = Object.keys(ch); const now = blend.current_by_class, prev = ch[ds.at(-1)] || {};
  const cls = CLASS_ORDER.slice(0, 4);
  const neutral = { Equity: 0.60, Bonds: 0.40, 'Real assets': 0, Cash: 0 };
  const risky = (now.Equity || 0) + (now['Real assets'] || 0);
  const stance = risky > 0.65 ? 'risk-on' : risky > 0.45 ? 'neutral to modestly risk-on' : risky > 0.3 ? 'defensive' : 'strongly defensive';
  const ns = strats.filter(s => !s.benchmark);
  const riskyShare = s => s.current.filter(c => c.class === 'Equity' || c.class === 'Real assets').reduce((a, c) => a + c.weight, 0);
  const breadth = ns.filter(s => riskyShare(s) >= 0.5).length / ns.length;
  const D = rets.dates, S = rets.series, n = D.length;
  const ytdI = D.findIndex(d => d.startsWith(D[n - 1].slice(0, 4)));
  const ytd = r => episodeReturn(r, D, D[ytdI], D[n - 1]);
  const F = M?.factors; const fl = F ? Object.keys(F.series).map(k => [F.labels[k], F.series[k].filter(v => v != null).at(-1)]) : [];
  const fdesc = v => v > 1 ? 'well above normal' : v > 0.3 ? 'above normal' : v < -1 ? 'well below normal' : v < -0.3 ? 'below normal' : 'close to normal';
  const nextMonth = new Date(meta.next_rebalance + 'T12:00:00').toLocaleString('en-CA', { month: 'long', year: 'numeric' });
  app.innerHTML = `
  <div class="memo">
    <div class="memo-head" style="margin-top:28px"><div><div class="eyebrow">DAA monthly note · illustrative</div><h1 style="font-size:30px">Positioning for ${nextMonth}</h1></div>
      <div class="small muted" style="text-align:right">Prepared by Tiago Costa<br>Signals as of ${fmt.date(meta.signal_date)}<br><button class="btn ghost no-print" onclick="window.print()">Print / save PDF</button></div></div>
    <h2>1. Recommendation</h2>
    <p>The blend is <b>${stance}</b>: <b>${fmt.pct(now.Equity || 0, 0)}</b> equity, <b>${fmt.pct(now.Bonds || 0, 0)}</b> bonds, <b>${fmt.pct(now['Real assets'] || 0, 0)}</b> real assets and <b>${fmt.pct(now.Cash || 0, 0)}</b> cash, versus a 60/40 neutral. ${Math.abs((now.Equity || 0) - 0.6) > 0.1 ? `That is a <b>${(now.Equity || 0) > 0.6 ? 'overweight' : 'underweight'}</b> in equities of ${fmt.pct(Math.abs((now.Equity || 0) - 0.6), 0)}.` : 'Equity exposure is close to neutral.'}</p>
    <table class="compact"><thead><tr><th>Asset class</th><th class="num">Blend now</th><th class="num">Last month</th><th class="num">Change</th><th class="num">vs 60/40</th></tr></thead><tbody>
    ${cls.map(c => `<tr><td><span class="chip"><span class="sw" style="background:${CLASS_COLORS[c]}"></span>${c}</span></td><td class="num">${fmt.pct(now[c] || 0)}</td><td class="num">${fmt.pct(prev[c] || 0)}</td><td class="num ${signCls((now[c] || 0) - (prev[c] || 0))}">${fmt.spct((now[c] || 0) - (prev[c] || 0))}</td><td class="num ${signCls((now[c] || 0) - neutral[c])}">${fmt.spct((now[c] || 0) - neutral[c])}</td></tr>`).join('')}
    </tbody></table>
    <h2>2. Why: what the signals say</h2>
    <ul>
      <li><b>Strategy breadth:</b> ${fmt.pct(breadth, 0)} of the ${ns.length} strategies in the lab hold at least half their portfolio in risky assets (equities and real assets). ${breadth > 0.7 ? 'Trend and momentum signals are broadly positive.' : breadth < 0.4 ? 'Most trend and momentum models have moved defensive, which historically happens in drawdowns.' : 'Signals are mixed: a typical sign of a transition.'}</li>
      <li><b>Top holdings across the blend:</b> ${blend.current_allocation.slice(0, 5).map(([t, w]) => `${t} (${meta.assets[t]?.name || ''}) ${fmt.pct(w, 0)}`).join('; ')}.</li>
      ${fl.length ? `<li><b>Macro backdrop:</b> ${fl.map(([l, v]) => `${l.toLowerCase()} is ${fdesc(v)} (${v >= 0 ? '+' : ''}${v.toFixed(1)}σ)`).join('; ')}.</li>` : ''}
      <li><b>Components:</b> ${blend.current_components.map(id => `${byId[id].name} (${byId[id].current.slice(0, 2).map(c => c.ticker + ' ' + fmt.pct(c.weight, 0)).join(', ')})`).join('; ')}.</li>
    </ul>
    <h2>3. Recent performance</h2>
    <table class="compact"><thead><tr><th></th><th class="num">Last month</th><th class="num">Year to date</th><th class="num">Since 2005 (ann.)</th></tr></thead><tbody>
    ${[['blend', "Tiago's DAA Blend"], ['bench_6040', '60/40 (US)'], ['bench_otpp_mix', 'OTPP-shaped mix (proxy)']].map(([k, l]) => { const r = S[k]; const i0 = firstIdx(S.blend); const st = stats(r.slice(i0), rets.cash.slice(i0), null, D.slice(i0)); return `<tr><td>${l}</td><td class="num ${signCls(r[n - 1])}">${fmt.spct(r[n - 1])}</td><td class="num ${signCls(ytd(r))}">${fmt.spct(ytd(r))}</td><td class="num">${fmt.pct(st.cagr)}</td></tr>`; }).join('')}
    </tbody></table>
    <h2>4. Risks and what would change the view</h2>
    <ul>
      <li><b>Whipsaw:</b> trend signals react after a move starts. A sharp V-shaped reversal (as in 2020) costs a defensive allocator part of the rebound.</li>
      <li><b>Stock-bond correlation:</b> since 2022 bonds have not reliably hedged equities. Strategies that rotate into long Treasuries carry inflation risk, so the blend's bond sleeve should be checked against the inflation factor.</li>
      <li><b>Trigger to revisit:</b> a fall in strategy breadth below 40%, or a jump in financial-conditions stress above +1σ, would normally move the blend defensive at the next month-end.</li>
    </ul>
    <h2>5. Implementation</h2>
    <p>Rebalance at the close on ${fmt.date(meta.next_rebalance)}. For a total fund, the same views would be implemented as an <b>overlay</b> with futures and swaps, sized to the DAA active-risk budget (see <a href="#/blend">overlay analysis</a>), rather than by trading the underlying assets.</p>
    <p class="small muted" style="margin-top:24px">Generated automatically from the lab's data on ${esc(meta.generated_at)}. Hypothetical, for demonstration only; not investment advice.</p>
  </div>`;
}

/* ================================================================== METHOD & DATA */
async function pageMethod() {
  const { meta } = await core();
  const pv = meta.proxy_validation || [];
  app.innerHTML = `
  <section class="hero"><div class="eyebrow">Method &amp; data</div><h1>How the lab works, and where it could be wrong</h1>
  <p class="lede">A backtest is only as good as its data and its honesty about limits. This page documents both.</p></section>
  <section class="grid-2">
    <div class="card"><h3>Backtest rules (identical for every strategy)</h3><ul class="small">
      <li><b>Signals</b> use data up to the close of the last trading day of each month, and nothing after.</li>
      <li><b>Trades</b> execute at that same close (the convention in the source papers and on AllocateSmartly). Holdings then drift with prices until the next rebalance.</li>
      <li><b>Costs:</b> ${fmt.pct(meta.cost_per_trade, 2)} of the value traded at every rebalance. No taxes, management fees or slippage beyond that.</li>
      <li><b>Returns</b> are total returns (dividends and interest reinvested), in USD.</li>
      <li><b>Cash</b> earns the 1–3 month T-bill return (BIL, or 13-week T-bill yields before 2007).</li>
      <li><b>Metrics</b> are computed from monthly returns. Sharpe and Sortino use returns in excess of cash.</li></ul></div>
    <div class="card"><h3>Known limitations</h3><ul class="small">
      <li><b>Proxies before ETFs existed.</b> They are validated below. Correlations are mostly above 0.95, but a proxy is not the real fund.</li>
      <li><b>Revised macro data.</b> Norgate stores the latest revised economic values, not first releases. Publication lags are applied, but revisions remain.</li>
      <li><b>Replication ≠ the original.</b> Where a paper is ambiguous, my reading is documented in the strategy's notes. Results can differ from the author's own or AllocateSmartly's.</li>
      <li><b>Selection bias.</b> Even an honest walk-forward is run on a library of strategies that were published <i>because</i> they backtested well. Expect live results to be weaker (McLean &amp; Pontiff, 2016).</li>
      <li><b>US-dollar, US-listed view.</b> A Canadian pension fund would see these returns in CAD, with its own hedging policy.</li></ul></div>
  </section>
  <section class="card"><h3>Proxy validation: does each back-fill track the real ETF?</h3><div class="sub">Monthly returns over the period where both exist. Tracking error = annualised volatility of the difference.</div>
    <div class="table-wrap"><table class="compact"><thead><tr><th>ETF</th><th>Proxy used before launch</th><th class="num">Months</th><th class="num">Correlation</th><th class="num">Tracking error</th><th class="num">ETF ann. return</th><th class="num">Proxy ann. return</th></tr></thead><tbody>
    ${pv.map(p => `<tr><td class="mono">${p.ticker}</td><td class="small">${esc(p.proxy)}</td><td class="num">${p.months}</td><td class="num">${fmt.num(p.corr, 3)}</td><td class="num">${fmt.pct(p.tracking_error, 2)}</td><td class="num">${fmt.pct(p.ann_return_etf)}</td><td class="num">${fmt.pct(p.ann_return_proxy)}</td></tr>`).join('')}
    </tbody></table></div></section>
  <section class="grid-2">
    <div class="card"><h3>Metric glossary</h3><table class="compact"><tbody>${Object.entries(meta.glossary).map(([k, v]) => `<tr><td class="mono small" style="white-space:nowrap">${k}</td><td class="small">${esc(v)}</td></tr>`).join('')}</tbody></table></div>
    <div class="card"><h3>How AI was used, and how its output was checked</h3><p class="small">This lab was built with an AI coding assistant (Claude Code): for code scaffolding, first-pass summaries of papers, and drafting text. Every output was checked:</p><ul class="small">
      <li><b>Data:</b> each proxy reconciled against the real ETF (table above). Benchmarks checked against published index returns.</li>
      <li><b>Rules:</b> each strategy coded from the original paper. Ambiguities are logged in its notes.</li>
      <li><b>Literature:</b> every citation verified at the source (DOI/SSRN/publisher). Unverifiable items were dropped.</li>
      <li><b>Code:</b> unit tests cover the metrics, signals and look-ahead protection (<span class="mono">tests/</span>).</li>
      <li><b>Judgement:</b> the selection rule's settings were fixed before results were seen, and their sensitivity is published.</li></ul></div>
  </section>
  <section class="card grey"><h3>Reproduce it</h3><pre class="mono small" style="white-space:pre-wrap;margin:0">git clone https://github.com/tiagonbc/daa-lab.git && cd daa-lab
pip install -r requirements.txt          # needs a Norgate Data subscription + Norgate Data Updater running
python scripts/run_all.py                # rebuilds every strategy, the blend and docs/data/*.json
python -m pytest                         # tests</pre><p class="small muted" style="margin-top:8px">Generated ${esc(meta.generated_at)} in ${meta.runtime_s}s. ${Object.keys(meta.failures || {}).length ? 'Failed strategies: ' + Object.keys(meta.failures).join(', ') : 'All strategies ran.'}</p></section>`;
}

/* ================================================================== ABOUT */
async function pageAbout() {
  const { meta, strats, blend } = await core();
  app.innerHTML = `
  <section class="hero"><div class="eyebrow">About</div><h1>Why I built this</h1>
  <p class="lede">I built DAA Lab to show, rather than tell, how I would work as an Investment Analyst on OTPP's Dynamic Asset Allocation team: macro and cross-asset research turned into models, tested honestly, and communicated in plain language for decision-makers.</p></section>
  <section class="grid-2">
    <div class="card"><h3>What the role asks for, and where to find it here</h3><table class="compact"><tbody>
      <tr><td class="small">Adjust the asset mix to macro conditions, valuations and risk premia</td><td class="small"><a href="#/macro">Macro factors</a> · <a href="#/blend">The Blend</a></td></tr>
      <tr><td class="small">Cross-asset analysis and scenario assessment</td><td class="small"><a href="#/blend">Stress tests, overlay sizing</a></td></tr>
      <tr><td class="small">Build and maintain quantitative and econometric models</td><td class="small"><a href="#/strategies">${strats.filter(s => !s.benchmark).length} strategies</a>, one shared engine, tests</td></tr>
      <tr><td class="small">Decision-oriented materials for senior forums</td><td class="small"><a href="#/note">Monthly DAA note</a></td></tr>
      <tr><td class="small">Data library, dashboards and monitoring tools</td><td class="small"><a href="#/method">Data pipeline with validation and lags</a></td></tr>
      <tr><td class="small">AI-enabled workflows, with validated outputs</td><td class="small"><a href="#/method">How AI was used and checked</a></td></tr>
      <tr><td class="small">Economics, asset allocation, multi-asset investing</td><td class="small"><a href="#/research">Research tracker</a></td></tr>
    </tbody></table></div>
    <div class="card"><h3>Context: OTPP's total-fund approach</h3><ul class="small">
      <li>OTPP manages <b>$279.4B</b> in net assets (2025) and lists dynamic, top-down asset allocation among its competitive advantages.</li>
      <li>The 2025 mix was 43% equity, 23% fixed income, 20% inflation-sensitive, 23% real assets, 14% credit and 9% absolute return, financed with −32% of funding. The <a href="#/s/bench_otpp_mix">OTPP-shaped proxy</a> in this lab mirrors that shape with liquid ETFs.</li>
      <li>The fund returned 6.7% in 2025 against an 11.7% benchmark, and the report names improving active returns as a 2026 priority. The <a href="#/blend">overlay analysis</a> sizes a tactical program in exactly those terms: value added for a given active-risk budget.</li>
      <li class="muted">Source: Ontario Teachers' 2025 Annual Report. All other figures on this site are hypothetical backtests.</li></ul></div>
  </section>
  <section class="card dark"><div class="grid-2"><div><h2>Tiago Costa</h2><p style="opacity:.85;margin-top:8px">Systematic trader and portfolio engineer. I have run my own systematic long/short book in Canadian, US and Brazilian equities and ETFs since 2017, and built the research, execution and P&amp;L-attribution stack behind it. Earlier, I traded EDP's $2B power-contract portfolio. Electrical engineer; Level I Candidate in the CFA Program. Based in Waterloo, open to Toronto (hybrid).</p></div>
    <div><p style="opacity:.85">Contact</p><p><a style="color:#fff;text-decoration:underline" href="mailto:tiagonbc@gmail.com">tiagonbc@gmail.com</a><br><a style="color:#fff;text-decoration:underline" href="https://www.linkedin.com/in/tiagonbc" target="_blank" rel="noopener">linkedin.com/in/tiagonbc</a></p>
    <p class="small" style="opacity:.7">This is a personal, independent project. It uses OTPP's publicly available annual report for context and borrows its public colour palette for readability. It is not affiliated with or endorsed by Ontario Teachers' Pension Plan.</p></div></div></section>`;
}

/* ================================================================== ROUTER */
const ROUTES = { '': pageHome, blend: pageBlend, strategies: pageStrategies, s: pageStrategy, builder: pageBuilder, macro: pageMacro, research: pageResearch, review: pageReview, note: pageNote, method: pageMethod, about: pageAbout };
async function route() {
  const parts = location.hash.replace(/^#\/?/, '').split('/');
  const fn = ROUTES[parts[0]] || pageHome;
  document.querySelectorAll('#nav a').forEach(a => a.classList.toggle('active', a.dataset.route === (parts[0] || 'home') || (parts[0] === 's' && a.dataset.route === 'strategies') || (parts[0] === 'review' && a.dataset.route === 'research')));
  disposeCharts();
  app.innerHTML = '<div class="loading">Loading…</div>';
  try { await fn(parts[1]); } catch (e) { console.error(e); app.innerHTML = `<div class="loading">Could not load this page (${esc(e.message)}).</div>`; }
  window.scrollTo(0, 0);
  load('meta.json').then(m => { document.getElementById('footer-meta').textContent = `Data through ${fmt.date(m.data_through)} · generated ${m.generated_at}`; }).catch(() => { });
}
app.addEventListener('click', e => { const tr = e.target.closest('[data-href]'); if (tr && !e.target.closest('a,button,input,select')) location.hash = tr.dataset.href; });
window.addEventListener('hashchange', route);
route();
