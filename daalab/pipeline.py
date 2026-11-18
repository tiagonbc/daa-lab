"""End-to-end run: data -> every strategy -> blend -> JSON for the website.

    python -m daalab.pipeline            (or scripts/run_all.py)
"""
from __future__ import annotations

import importlib
import json
import logging
import math
import pkgutil
import time
import traceback
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import strategies as strat_pkg
from .blend import selection as bl
from .config import CASH, COST_PER_TRADE, RESEARCH_DIR, SITE_DATA
from .data.assets import AssetPanel, validate_proxies
from .data.macro import SERIES as MACRO_SERIES, build_macro
from .data.universe import asset_class, describe
from .engine import metrics as mt
from .engine.core import REGISTRY, run

log = logging.getLogger("daalab")


def _clean(x):
    """JSON-safe rounding (NaN -> null)."""
    if isinstance(x, dict):
        return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if not math.isfinite(float(x)) else round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, pd.Timestamp):
        return x.strftime("%Y-%m-%d")
    return x


def _dump(obj, name):
    path = SITE_DATA / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_clean(obj), separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    return path


def load_strategies():
    for m in pkgutil.iter_modules(strat_pkg.__path__):
        importlib.import_module(f"{strat_pkg.__name__}.{m.name}")
    return REGISTRY


def run_all(blend_cfg: bl.BlendConfig | None = None, sensitivity: bool = True):
    t0 = time.time()
    warnings.filterwarnings("ignore")
    logging.disable(logging.INFO)
    panel = AssetPanel()
    # macro history starts in 1960 so that slow z-scores are fully warmed up before the first trade in 2000
    macro, macro_info = build_macro(pd.date_range("1960-01-31", panel.trade_dates.index[-1], freq="ME"))
    load_strategies()

    results, failures = {}, {}
    for sid, s in REGISTRY.items():
        try:
            results[sid] = run(s, panel, macro)
        except Exception as e:  # keep going; report on the site
            failures[sid] = f"{type(e).__name__}: {e}"
            traceback.print_exc()
    print(f"ran {len(results)} strategies, {len(failures)} failed")

    rf = panel.monthly(CASH).pct_change()
    b6040 = results["bench_6040"].returns
    spy = results["bench_spy"].returns
    R = pd.DataFrame({k: r.returns for k, r in results.items()}).sort_index()
    dates = R.index

    # ---------------------------------------------------------------- strategies
    strategies_out = []
    for sid, res in results.items():
        s = res.strategy
        m = mt.summarize(res.returns, rf, b6040, spy, res.turnover)
        cur = sorted(res.current.items(), key=lambda kv: -kv[1])
        strategies_out.append({
            "id": sid, "name": s.name, "author": s.author, "family": s.family, "year": s.year,
            "source": {"title": s.source_title, "url": s.source_url},
            "allocatesmartly_url": s.allocatesmartly_url,
            "plain_english": s.plain_english, "rules": s.rules, "notes": s.notes,
            "assets": [{"ticker": t, "name": describe(t), "class": asset_class(t)} for t in dict.fromkeys(s.assets + s.optional)],
            "lookback_months": s.lookback_months, "rebalance": s.rebalance, "benchmark": s.benchmark,
            "macro_inputs": s.macro_inputs,
            "metrics": m,
            "current": [{"ticker": t, "weight": w, "class": asset_class(t)} for t, w in cur],
            "signal_date": res.signal_date, "mtd": res.mtd_return,
        })
        W = res.weights.round(4)
        _dump({"dates": [d.strftime("%Y-%m") for d in W.index], "assets": list(W.columns),
               "w": W.values.tolist(), "turnover": res.turnover.round(4).tolist()}, f"weights/{sid}.json")

    # ---------------------------------------------------------------- blend
    cfg = blend_cfg or bl.BlendConfig()
    cand = [k for k, r in results.items() if not r.strategy.benchmark]
    Rc = R[cand]
    wf, selections, comp_w = bl.walk_forward(Rc, rf, cfg)
    is_ret, is_sel = bl.in_sample(Rc, rf, cfg, wf.index[0] - pd.offsets.MonthEnd(1))
    blend_metrics = mt.summarize(wf, rf, b6040, spy)
    last_sel = selections[-1]
    comp_now = pd.Series(1 / len(last_sel.chosen), index=last_sel.chosen)
    alloc = {}
    for sid, w in comp_now.items():
        for t, a in results[sid].current.items():
            alloc[t] = alloc.get(t, 0) + w * a
    by_class = {}
    for t, a in alloc.items():
        by_class[asset_class(t)] = by_class.get(asset_class(t), 0) + a
    # historical blend holdings by asset class (for the stacked area chart)
    cls_hist = {}
    for d, row in comp_w.iterrows():
        acc = {}
        for sid, w in row.items():
            if w <= 0:
                continue
            W = results[sid].weights
            prev = W.loc[:d - pd.offsets.MonthEnd(1)]
            if prev.empty:
                continue
            for t, a in prev.iloc[-1].items():
                if a:
                    acc[asset_class(t)] = acc.get(asset_class(t), 0) + w * a
        cls_hist[d.strftime("%Y-%m")] = acc
    blend_out = {
        "config": cfg.__dict__,
        "returns": {d.strftime("%Y-%m"): r for d, r in wf.items()},
        "in_sample_returns": {d.strftime("%Y-%m"): r for d, r in is_ret.items()},
        "in_sample_pick": is_sel.chosen,
        "metrics": blend_metrics,
        "in_sample_metrics": mt.summarize(is_ret, rf, b6040, spy),
        "selections": [{"date": s.date.strftime("%Y-%m"), "chosen": s.chosen, "n_eligible": len(s.scores),
                        "scores": {k: s.scores[k] for k in list(s.scores)[:20]}, "skipped": s.skipped[:10]}
                       for s in selections],
        "current_components": last_sel.chosen,
        "current_allocation": sorted(([t, w] for t, w in alloc.items()), key=lambda x: -x[1]),
        "current_by_class": by_class,
        "class_history": cls_hist,
        "component_weights": {d.strftime("%Y-%m"): row[row > 0].round(4).to_dict() for d, row in comp_w.iterrows()},
    }
    if sensitivity:
        blend_out["sensitivity"] = bl.sensitivity(Rc, rf, cfg)
    # strategy consensus: average allocation by asset class across every non-benchmark strategy
    cons = {}
    for sid in cand:
        W = results[sid].weights
        for d, row in W.iterrows():
            acc = cons.setdefault(d.strftime("%Y-%m"), {"n": 0})
            acc["n"] += 1
            for t, a in row.items():
                if a:
                    acc[asset_class(t)] = acc.get(asset_class(t), 0) + a
    blend_out["consensus"] = {d: {k: (v / c["n"] if k != "n" else v) for k, v in c.items()} for d, c in sorted(cons.items())}

    # ---------------------------------------------------------------- returns table
    returns_out = {
        "dates": [d.strftime("%Y-%m") for d in dates],
        "cash": [None if pd.isna(v) else v for v in rf.reindex(dates).values],
        "series": {k: [None if pd.isna(v) else round(float(v), 6) for v in R[k].values] for k in R.columns},
    }
    returns_out["series"]["blend"] = [None if pd.isna(v) else round(float(v), 6) for v in wf.reindex(dates).values]

    # ---------------------------------------------------------------- macro dashboard
    macro_cols = ["unemp", "unemp_gap_low12", "payrolls_yoy", "cfnai_ma3", "ism", "indpro_yoy", "real_retail_yoy",
                  "core_cpi_yoy", "core_cpi_3m_ann", "cpi_yoy", "nfci", "baa_spread", "ccc_oas", "curve_10y3m",
                  "real_10y", "y10", "y3m", "vix", "claims_4w_yoy", "m2_yoy"]
    mac = macro.loc["1990-01-31":, [c for c in macro_cols if c in macro]]
    macro_out = {
        "dates": [d.strftime("%Y-%m") for d in mac.index],
        "series": {c: [None if pd.isna(v) else round(float(v), 4) for v in mac[c].values] for c in mac.columns},
        "info": macro_info,
    }
    try:
        from .strategies.macro_factors import site_factors
        fp, labels = site_factors(macro)
        fp = fp.loc["1990-01-31":]
        macro_out["factors"] = {"dates": [d.strftime("%Y-%m") for d in fp.index], "labels": labels,
                                "series": {c: [None if pd.isna(v) else round(float(v), 3) for v in fp[c].values] for c in fp.columns}}
    except ImportError:
        pass

    # ---------------------------------------------------------------- meta
    tickers = sorted({t for r in results.values() for t in r.strategy.assets + r.strategy.optional} | {CASH})
    proxies = validate_proxies(panel, tickers)
    meta = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "data_through": panel.calendar[-1].strftime("%Y-%m-%d"),
        "signal_date": results["bench_6040"].signal_date.strftime("%Y-%m-%d"),
        "partial_month": panel.partial_month,
        "next_rebalance": (panel.calendar[-1] + pd.offsets.BMonthEnd(0)).strftime("%Y-%m-%d"),
        "cost_per_trade": COST_PER_TRADE,
        "n_strategies": len([r for r in results.values() if not r.strategy.benchmark]),
        "failures": failures,
        "glossary": mt.METRIC_GLOSSARY,
        "assets": {t: {**panel.meta.get(t, {}), "name": describe(t), "class": asset_class(t)} for t in tickers if t in panel.meta},
        "proxy_validation": proxies.to_dict(orient="records"),
        "macro_series": {k: {"symbol": v[0], "frequency": v[1], "lag": v[2], "description": v[3]} for k, v in MACRO_SERIES.items()},
        "runtime_s": round(time.time() - t0, 1),
    }

    _dump(strategies_out, "strategies.json")
    _dump(returns_out, "returns.json")
    _dump(blend_out, "blend.json")
    _dump(macro_out, "macro.json")
    _dump(meta, "meta.json")
    lit = RESEARCH_DIR / "literature.json"
    if lit.exists():
        (SITE_DATA / "literature.json").write_text(lit.read_text(encoding="utf-8"), encoding="utf-8")
    review = RESEARCH_DIR / "literature_review.md"
    if review.exists():
        import markdown
        html = markdown.markdown(review.read_text(encoding="utf-8"), extensions=["tables"])
        (SITE_DATA / "literature_review.html").write_text(html, encoding="utf-8")
    print(f"done in {time.time() - t0:.0f}s; blend {blend_metrics['cagr']:.2%} CAGR, Sharpe {blend_metrics['sharpe']:.2f}, "
          f"maxDD {blend_metrics['max_dd']:.1%}; picks {last_sel.chosen}")
    return results, blend_out


if __name__ == "__main__":
    run_all()
