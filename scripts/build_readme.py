"""Regenerate README.md from scripts/README.template.md and the website data (docs/data/*.json)."""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://tiagonbc.github.io/daa-lab/"


def pct(v, d=1):
    return "–" if v is None else f"{v * 100:.{d}f}%"


def num(v, d=2):
    return "–" if v is None else f"{v:.{d}f}"


def stats(r, rf):
    """Small re-implementation (mirrors daalab.engine.metrics) on a list of monthly returns."""
    pairs = [(x, f or 0.0) for x, f in zip(r, rf) if x is not None]
    if len(pairs) < 24:
        return None
    R = [p[0] for p in pairs]
    ex = [p[0] - p[1] for p in pairs]
    n = len(R)
    eq, peak, mdd = 1.0, 1.0, 0.0
    for x in R:
        eq *= 1 + x
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    m = sum(ex) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in ex) / (n - 1))
    vol = math.sqrt(sum((x - sum(R) / n) ** 2 for x in R) / (n - 1)) * math.sqrt(12)
    return {"cagr": eq ** (12 / n) - 1, "vol": vol, "sharpe": m * 12 / (sd * math.sqrt(12)), "max_dd": mdd}


def main(site_url=SITE_URL):
    d = ROOT / "docs" / "data"
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    strats = json.loads((d / "strategies.json").read_text(encoding="utf-8"))
    rets = json.loads((d / "returns.json").read_text(encoding="utf-8"))
    blend = json.loads((d / "blend.json").read_text(encoding="utf-8"))
    names = {s["id"]: s["name"] for s in strats}
    dates, cash, S = rets["dates"], rets["cash"], rets["series"]
    b0 = next(i for i, v in enumerate(S["blend"]) if v is not None)

    rows = [("Tiago's DAA Blend (walk-forward)", "blend"), ("60/40 (SPY/IEF)", "bench_6040"),
            ("Global 60/40", "bench_global_6040"), ("OTPP-shaped mix (liquid proxy)", "bench_otpp_mix"), ("S&P 500", "bench_spy")]
    t = ["| Portfolio | CAGR | Volatility | Sharpe | Max drawdown |", "|---|---:|---:|---:|---:|"]
    for label, k in rows:
        m = stats(S[k][b0:], cash[b0:])
        t.append(f"| {label} | {pct(m['cagr'])} | {pct(m['vol'])} | {num(m['sharpe'])} | {pct(m['max_dd'])} |")
    blend_table = f"Period: {dates[b0]} to {dates[-1]}.\n\n" + "\n".join(t)

    i10 = max(0, len(dates) - 120)
    scored = []
    for s in strats:
        if s["benchmark"]:
            continue
        r = S[s["id"]][i10:]
        if sum(v is not None for v in r) < 120:
            continue
        m = stats(r, cash[i10:])
        scored.append((m["sharpe"], s, m))
    scored.sort(key=lambda x: -x[0])
    tt = ["| Strategy | Author | CAGR | Sharpe | Max drawdown |", "|---|---|---:|---:|---:|"]
    for _, s, m in scored[:10]:
        tt.append(f"| {s['name']} | {s['author']} | {pct(m['cagr'])} | {num(m['sharpe'])} | {pct(m['max_dd'])} |")

    try:
        out = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"], cwd=ROOT, capture_output=True, text=True, timeout=120)
        n_tests = re.search(r"(\d+) tests? collected", out.stdout).group(1)
    except Exception:
        n_tests = "the"
    sel = blend["selections"][-1]
    vals = {
        "N_STRATEGIES": str(meta["n_strategies"]), "SITE_URL": site_url, "SIGNAL_DATE": meta["signal_date"],
        "DATA_THROUGH": meta["data_through"], "BLEND_N": str(blend["config"]["n"]), "BLEND_CAP": str(blend["config"]["corr_cap"]),
        "BLEND_TABLE": blend_table, "TOP_TABLE": "\n".join(tt), "SELECTION_DATE": sel["date"],
        "COMPONENTS": ", ".join(names.get(c, c) for c in sel["chosen"]), "N_TESTS": n_tests, "GENERATED_AT": meta["generated_at"],
    }
    text = (ROOT / "scripts" / "README.template.md").read_text(encoding="utf-8")
    for k, v in vals.items():
        text = text.replace("{{" + k + "}}", v)
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print("README.md written")


if __name__ == "__main__":
    main(*sys.argv[1:])
