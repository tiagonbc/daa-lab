/* DAA Lab - shared helpers: formatting, metrics (mirrors daalab/engine/metrics.py), charts. */
'use strict';

const C = {
  red: '#e81132', blue: '#1f5fae', teal: '#00a0a3', amber: '#eda100', plum: '#8c2f5a',
  green: '#2e8b3a', violet: '#6a5acd', pink: '#e87ba4',
  aub: '#240b14', ink2: '#4f4448', muted: '#7e7076', grid: '#eeeaeb', axis: '#d4d1d2', surface: '#ffffff',
};
// validated categorical order (scripts/validate_palette.js, light surface)
const SERIES = [C.blue, C.red, C.teal, C.amber, C.plum, C.green, C.violet, C.pink];
const CLASS_COLORS = { Equity: C.blue, Bonds: C.teal, 'Real assets': C.amber, Cash: C.plum, Other: C.violet };
const CLASS_ORDER = ['Equity', 'Bonds', 'Real assets', 'Cash', 'Other'];
// fixed colour per featured entity (colour follows the entity, never its rank)
const ENTITY = { blend: C.red, bench_6040: C.blue, bench_global_6040: C.teal, bench_spy: C.amber, bench_otpp_mix: C.plum };

/* ------------------------------------------------------------------ format */
const fmt = {
  pct: (v, d = 1) => (v == null || !isFinite(v)) ? '–' : (v * 100).toFixed(d) + '%',
  spct: (v, d = 1) => (v == null || !isFinite(v)) ? '–' : (v > 0 ? '+' : '') + (v * 100).toFixed(d) + '%',
  num: (v, d = 2) => (v == null || !isFinite(v)) ? '–' : v.toFixed(d),
  int: v => (v == null || !isFinite(v)) ? '–' : Math.round(v).toString(),
  ym: s => { if (!s) return '–'; const [y, m] = s.split('-'); return new Date(+y, +m - 1, 1).toLocaleString('en-CA', { month: 'short', year: 'numeric' }); },
  date: s => s ? new Date(s + 'T12:00:00').toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }) : '–',
};
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const signCls = v => v == null ? '' : (v < 0 ? 'neg' : '');

/* ------------------------------------------------------------------ data */
const DATA = {};
async function load(name) {
  if (DATA[name]) return DATA[name];
  const r = await fetch('data/' + name, { cache: 'no-cache' });
  if (!r.ok) throw new Error('missing data/' + name);
  DATA[name] = await r.json();
  return DATA[name];
}

/* ------------------------------------------------------------------ metrics */
function windowIdx(dates, period) {
  // period: 'full' | 'since2008' | '10y' | '5y' | '3y' | {from,to}
  const n = dates.length;
  if (period === 'full' || !period) return [0, n - 1];
  if (period === 'since2008') return [Math.max(0, dates.indexOf('2008-01')), n - 1];
  const yrs = { '20y': 20, '15y': 15, '10y': 10, '5y': 5, '3y': 3, '1y': 1 }[period];
  if (yrs) return [Math.max(0, n - yrs * 12), n - 1];
  return [Math.max(0, dates.indexOf(period.from)), period.to ? dates.indexOf(period.to) : n - 1];
}

function stats(r, rf, bench, dates) {
  const idx = []; for (let i = 0; i < r.length; i++) if (r[i] != null) idx.push(i);
  if (idx.length < 2) return null;
  const R = idx.map(i => r[i]), F = idx.map(i => rf[i] ?? 0);
  const n = R.length;
  let eq = 1, peak = 1, mdd = 0, ss = 0, under = 0, longest = 0;
  const eqs = [], dds = [];
  for (const x of R) { eq *= 1 + x; peak = Math.max(peak, eq); const dd = eq / peak - 1; mdd = Math.min(mdd, dd); ss += dd * dd; dds.push(dd); eqs.push(eq); under = dd < -1e-9 ? under + 1 : 0; longest = Math.max(longest, under); }
  const cagr = Math.pow(eq, 12 / n) - 1;
  const rfeq = F.reduce((a, x) => a * (1 + x), 1); const rfc = Math.pow(rfeq, 12 / n) - 1;
  const mean = a => a.reduce((s, x) => s + x, 0) / a.length;
  const sd = a => { const m = mean(a); return Math.sqrt(a.reduce((s, x) => s + (x - m) ** 2, 0) / (a.length - 1)); };
  const ex = R.map((x, k) => x - F[k]);
  const vol = sd(R) * Math.sqrt(12);
  const sharpe = mean(ex) * 12 / (sd(ex) * Math.sqrt(12));
  const ddev = Math.sqrt(mean(ex.map(x => Math.min(0, x) ** 2))) * Math.sqrt(12);
  const ulcer = Math.sqrt(ss / n);
  const years = {}; const ycount = {};
  idx.forEach((i, k) => { const y = dates[i].slice(0, 4); years[y] = (years[y] ?? 1) * (1 + R[k]); ycount[y] = (ycount[y] ?? 0) + 1; });
  const full = Object.keys(years).filter(y => ycount[y] === 12).map(y => years[y] - 1);
  const out = {
    start: dates[idx[0]], end: dates[idx[n - 1]], months: n, cagr, vol, sharpe,
    sortino: ddev > 0 ? mean(ex) * 12 / ddev : null, max_dd: mdd, ulcer,
    upi: ulcer > 0 ? (cagr - rfc) / ulcer : null, calmar: mdd < 0 ? cagr / -mdd : null,
    worst_year: full.length ? Math.min(...full) : null, best_year: full.length ? Math.max(...full) : null,
    pct_pos: R.filter(x => x > 0).length / n, worst_month: Math.min(...R), longest_dd: longest, current_dd: dds[n - 1],
  };
  if (bench) {
    const a = [], b = [];
    idx.forEach((i, k) => { if (bench[i] != null) { a.push(R[k]); b.push(bench[i]); } });
    if (a.length > 12) {
      const ma = mean(a), mb = mean(b);
      let cov = 0, va = 0, vb = 0; for (let k = 0; k < a.length; k++) { cov += (a[k] - ma) * (b[k] - mb); va += (a[k] - ma) ** 2; vb += (b[k] - mb) ** 2; }
      out.corr = cov / Math.sqrt(va * vb); out.beta = cov / vb;
    }
  }
  return out;
}

function corr(a, b) {
  const x = [], y = []; for (let i = 0; i < a.length; i++) if (a[i] != null && b[i] != null) { x.push(a[i]); y.push(b[i]); }
  if (x.length < 12) return null;
  const mx = x.reduce((s, v) => s + v, 0) / x.length, my = y.reduce((s, v) => s + v, 0) / y.length;
  let c = 0, vx = 0, vy = 0; for (let k = 0; k < x.length; k++) { c += (x[k] - mx) * (y[k] - my); vx += (x[k] - mx) ** 2; vy += (y[k] - my) ** 2; }
  return c / Math.sqrt(vx * vy);
}

function curve(r, i0, i1) { // growth of 100 from i0 (value 100 at the month before the first return)
  const out = new Array(r.length).fill(null); let eq = 100, started = false;
  for (let i = i0; i <= i1; i++) { if (r[i] == null) { if (started) out[i] = null; continue; } if (!started && i > 0) out[i - 1] = 100; started = true; eq *= 1 + r[i]; out[i] = eq; }
  return out;
}
function ddCurve(r, i0, i1) {
  const out = new Array(r.length).fill(null); let eq = 1, pk = 1, started = false;
  for (let i = i0; i <= i1; i++) { if (r[i] == null) continue; if (!started && i > 0) out[i - 1] = 0; started = true; eq *= 1 + r[i]; pk = Math.max(pk, eq); out[i] = eq / pk - 1; }
  return out;
}
function annual(r, dates) {
  const y = {}; r.forEach((x, i) => { if (x == null) return; const k = dates[i].slice(0, 4); y[k] = (y[k] ?? 1) * (1 + x); });
  return Object.fromEntries(Object.entries(y).map(([k, v]) => [k, v - 1]));
}
function combine(seriesList, weights) { // fixed-weight monthly-rebalanced mix of return series
  const n = seriesList[0].length; const out = new Array(n).fill(null);
  for (let i = 0; i < n; i++) {
    let s = 0, w = 0, ok = true;
    seriesList.forEach((r, k) => { if (r[i] == null) ok = false; else { s += weights[k] * r[i]; w += weights[k]; } });
    out[i] = ok && w > 0 ? s / w : null;
  }
  return out;
}

/* ------------------------------------------------------------------ charts */
const CHARTS = [];
function mount(el, option, renderer = 'svg') {
  if (typeof el === 'string') el = document.getElementById(el);
  if (!el || !window.echarts) return null;
  const c = echarts.init(el, null, { renderer });
  c.setOption(option);
  CHARTS.push(c);
  return c;
}
function disposeCharts() { CHARTS.forEach(c => c.dispose()); CHARTS.length = 0; }
window.addEventListener('resize', () => CHARTS.forEach(c => c.resize()));

function base(extra = {}) {
  return Object.assign({
    animation: false,
    textStyle: { fontFamily: 'Montserrat, Arial, sans-serif', color: C.ink2, fontSize: 11.5 },
    grid: { left: 58, right: 20, top: 16, bottom: 30 },
    tooltip: {
      trigger: 'axis', backgroundColor: '#fff', borderColor: C.axis, borderWidth: 1, padding: [8, 10],
      textStyle: { color: C.aub, fontSize: 12, fontFamily: 'Montserrat, Arial, sans-serif' },
      axisPointer: { type: 'line', lineStyle: { color: C.muted, width: 1 } },
    },
  }, extra);
}
const xCat = (dates, extra = {}) => {
  // one label per January, thinned to every 2/5 years on long spans (no repeated years)
  const yrs = dates.length / 12, step = yrs > 24 ? 5 : yrs > 12 ? 2 : 1;
  const show = (i, v) => yrs < 2 ? (i % 3 === 0) : (v.endsWith('-01') && (+v.slice(0, 4)) % step === 0);
  return Object.assign({
    type: 'category', data: dates, boundaryGap: false,
    axisLine: { lineStyle: { color: C.axis } }, axisTick: { show: false },
    axisLabel: { color: C.muted, interval: show, formatter: v => yrs < 2 ? fmt.ym(v) : v.slice(0, 4) },
  }, extra);
};
const yVal = (extra = {}) => Object.assign({
  type: 'value', splitLine: { lineStyle: { color: C.grid } }, axisLine: { show: false },
  axisLabel: { color: C.muted },
}, extra);

function tipRows(params, f) {
  const head = `<div style="font-weight:600;margin-bottom:4px">${fmt.ym(params[0].axisValue)}</div>`;
  const rows = params.filter(p => p.value != null).map(p =>
    `<div style="display:flex;justify-content:space-between;gap:18px"><span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:${p.color};margin-right:6px"></span>${esc(p.seriesName)}</span><b style="font-family:var(--mono)">${f(p.value)}</b></div>`).join('');
  return head + rows;
}

function lineSeries(name, data, color, opt = {}) {
  return Object.assign({ name, type: 'line', data, showSymbol: false, symbolSize: 8, connectNulls: false,
    lineStyle: { width: opt.width ?? 2, color }, itemStyle: { color }, emphasis: { focus: 'series', lineStyle: { width: 2.5 } }, z: opt.z ?? 2 }, opt.extra || {});
}

function growthChart(el, dates, list, i0, i1, { log = true } = {}) {
  const d = dates.slice(i0, i1 + 1);
  const series = list.map(s => lineSeries(s.name, curve(s.r, i0, i1).slice(i0, i1 + 1), s.color, { width: s.width, z: s.z }));
  return mount(el, base({
    xAxis: xCat(d), yAxis: yVal({ type: log ? 'log' : 'value', logBase: 10, scale: true, min: v => Math.max(1, v.min * 0.92), max: v => v.max * 1.05,
      axisLabel: { color: C.muted, formatter: v => '$' + Math.round(v) } }),
    tooltip: { ...base().tooltip, formatter: p => tipRows(p, v => '$' + v.toFixed(0)) },
    series,
  }));
}
function drawdownChart(el, dates, list, i0, i1) {
  const d = dates.slice(i0, i1 + 1);
  const series = list.map((s, k) => lineSeries(s.name, ddCurve(s.r, i0, i1).slice(i0, i1 + 1), s.color,
    { width: s.width ?? 1.5, extra: k === 0 ? { areaStyle: { color: s.color, opacity: 0.10 } } : {} }));
  return mount(el, base({
    xAxis: xCat(d), yAxis: yVal({ max: 0, axisLabel: { color: C.muted, formatter: v => Math.round(v * 100) + '%' } }),
    tooltip: { ...base().tooltip, formatter: p => tipRows(p, v => fmt.pct(v)) },
    series,
  }));
}
function annualBars(el, years, list) {
  return mount(el, base({
    grid: { left: 52, right: 12, top: 16, bottom: 30 },
    xAxis: { type: 'category', data: years, axisLine: { lineStyle: { color: C.axis } }, axisTick: { show: false }, axisLabel: { color: C.muted, hideOverlap: true } },
    yAxis: yVal({ axisLabel: { color: C.muted, formatter: v => Math.round(v * 100) + '%' } }),
    tooltip: { ...base().tooltip, axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(36,11,20,.05)' } }, formatter: p => tipRows(p, v => fmt.spct(v)).replace(/^<div[^>]*>[^<]*<\/div>/, `<div style="font-weight:600;margin-bottom:4px">${p[0].axisValue}</div>`) },
    series: list.map(s => ({ name: s.name, type: 'bar', data: years.map(y => s.values[y] ?? null), barGap: '15%', barMaxWidth: 14,
      itemStyle: { color: s.color, borderRadius: [3, 3, 0, 0] } })),
  }));
}
function stackedClasses(el, dates, byClass, classes) {
  return mount(el, base({
    xAxis: xCat(dates), yAxis: yVal({ min: 0, max: v => (v.max > 1.005 ? Math.ceil(v.max * 10) / 10 : 1), axisLabel: { color: C.muted, formatter: v => Math.round(v * 100) + '%' } }),
    tooltip: { ...base().tooltip, formatter: p => tipRows(p, v => fmt.pct(v, 0)) },
    series: classes.map(c => ({ name: c, type: 'line', stack: 'w', data: byClass[c], showSymbol: false, step: 'end',
      lineStyle: { width: 0 }, areaStyle: { color: CLASS_COLORS[c] || C.violet, opacity: 0.9 }, itemStyle: { color: CLASS_COLORS[c] || C.violet } })),
  }));
}
function divergingColor(v, scale) { // blue (positive) <-> grey <-> red (negative)
  if (v == null) return '#f7f7f7';
  const t = Math.max(-1, Math.min(1, v / scale));
  const lerp = (a, b, u) => Math.round(a + (b - a) * u);
  const mid = [240, 239, 236], pos = [31, 95, 174], neg = [196, 15, 43];
  const to = t >= 0 ? pos : neg, u = Math.pow(Math.abs(t), 0.8);
  return `rgb(${lerp(mid[0], to[0], u)},${lerp(mid[1], to[1], u)},${lerp(mid[2], to[2], u)})`;
}
function textOn(bg) { const m = bg.match(/\d+/g); if (!m) return C.aub; const [r, g, b] = m.map(Number); return (0.299 * r + 0.587 * g + 0.114 * b) < 140 ? '#fff' : C.aub; }

function sparkline(r, i0, i1, w = 110, h = 28, color = C.aub) {
  const c = curve(r, i0, i1).slice(i0, i1 + 1).filter(v => v != null);
  if (c.length < 3) return '';
  const lg = c.map(Math.log); const mn = Math.min(...lg), mx = Math.max(...lg); const step = Math.max(1, Math.floor(c.length / 60));
  const pts = []; for (let k = 0; k < lg.length; k += step) pts.push([k / (lg.length - 1) * w, h - 2 - (lg[k] - mn) / ((mx - mn) || 1) * (h - 4)]);
  pts.push([w, h - 2 - (lg[lg.length - 1] - mn) / ((mx - mn) || 1) * (h - 4)]);
  return `<svg class="spark" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true"><polyline fill="none" stroke="${color}" stroke-width="1.5" points="${pts.map(p => p.map(v => v.toFixed(1)).join(',')).join(' ')}"/></svg>`;
}
function legendHTML(items, box = false) {
  return `<div class="legend">${items.map(i => `<span><i class="${box ? 'box' : ''}" style="background:${i.color}"></i>${esc(i.name)}</span>`).join('')}</div>`;
}
function tip(text) { return text ? `<span class="tip" tabindex="0">i<span class="tiptext">${esc(text)}</span></span>` : ''; }
