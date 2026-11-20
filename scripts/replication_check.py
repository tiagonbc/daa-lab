"""Compare the lab's backtests with figures published by the strategies' authors.

Reads  research/published_benchmarks.json  (published annual returns or period statistics, with sources)
and    docs/data/returns.json              (the lab's monthly returns),
writes docs/data/replication.json          (shown on the Method page)
and    research/replication_check.md       (a readable report).

Verdict per comparison (calendar-year returns):
  close              correlation >= 0.90 and mean absolute difference <= 3 percentage points
  broadly consistent correlation >= 0.75 and mean absolute difference <= 6 points
  differs            anything else - explained in the notes (proxies, rule reading, costs)
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def annual_from_monthly(dates, rets):
    years, counts = {}, {}
    for d, r in zip(dates, rets):
        if r is None:
            continue
        y = d[:4]
        years[y] = years.get(y, 1.0) * (1 + r)
        counts[y] = counts.get(y, 0) + 1
    return {y: v - 1 for y, v in years.items() if counts[y] == 12}


def period_stats(dates, rets, cash, start, end):
    rows = [(r, c or 0.0) for d, r, c in zip(dates, rets, cash) if start <= d <= end and r is not None]
    if len(rows) < 12:
        return None
    R = [r for r, _ in rows]
    ex = [r - c for r, c in rows]
    n = len(R)
    eq, pk, mdd = 1.0, 1.0, 0.0
    for x in R:
        eq *= 1 + x
        pk = max(pk, eq)
        mdd = min(mdd, eq / pk - 1)
    mean = sum(R) / n
    vol = math.sqrt(sum((x - mean) ** 2 for x in R) / (n - 1)) * math.sqrt(12)
    me = sum(ex) / n
    sde = math.sqrt(sum((x - me) ** 2 for x in ex) / (n - 1))
    first = next(d for d, r in zip(dates, rets) if start <= d <= end and r is not None)
    last = [d for d, r in zip(dates, rets) if start <= d <= end and r is not None][-1]
    return {"cagr": eq ** (12 / n) - 1, "vol": vol, "sharpe": me * 12 / (sde * math.sqrt(12)) if sde > 0 else None,
            "max_dd": mdd, "from": first, "to": last, "months": n}


def corr(a, b):
    n = len(a)
    if n < 3:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(va * vb) if va > 0 and vb > 0 else None


def verdict(c, mad):
    if c is None or mad is None:
        return "insufficient overlap"
    if c >= 0.90 and mad <= 0.03:
        return "close"
    if c >= 0.75 and mad <= 0.06:
        return "broadly consistent"
    return "differs"


# Headline source when the authors' own figures disagree (documented in LAB_NOTES).
PREFERRED = {"daa_g12": {"cagr": 0.099}}

# What explains each comparison, from diagnostics run in the lab (shown on the website).
LAB_NOTES = {
    "bench_spy": "Data check: the lab's S&P 500 series against official yearly total returns.",
    "bench_6040": "Matches the 60/40 (SPY/IEF) benchmark in Keller & Keuning (2023) to the decimal.",
    "daa_g12": "The authors' sources disagree: the paper's table (via CXO) gives 9.9% / -9.0% for Mar 2008 - Mar 2018, "
               "the co-author's blog 11.1% / -8.2%. The lab's 9.6% / -8.9% matches the paper.",
    "vaa_g4": "The lab uses AllocateSmartly's ETFs (EFA, EEM, AGG). Rerun on the paper's ETFs (VEA, VWO, BND) the lab gives "
              "10.6% / -10.1% vs the published 10.5% / -10.5%: the gap is entirely the choice of ETF proxies.",
    "faber_gtaa_agg6": "Most of the gap is 2008 (lab -8.0% vs +12.1%) and 2002-03. Faber used index data throughout: foreign "
                       "government bonds before 2008 (BWX starts late 2007 in the lab), the GSCI (lab: Bloomberg Commodity) and a "
                       "small-cap momentum index (lab: Russell 2000, as AllocateSmartly does).",
    "faber_gtaa_agg3": "Same data differences as GTAA Aggressive 6, with a smaller effect because only 3 assets are held.",
    "haa_balanced": "Published yearly returns were read from the co-author's chart (about +/-0.3 points).",
    "haa_simple": "Published yearly returns were read from the co-author's chart (about +/-0.3 points).",
    "paa2": "Published yearly returns were read from the co-author's chart; the lab's PAA2 starts in 2008 (HYG data).",
    "philoeconomics_growth_trend_timing": "Compared with an independent replication (yearly returns read from its chart); the lab "
                                          "uses Norgate retail sales deflated by CPI instead of FRED's real retail sales.",
}


ALIASES = {"faber_gtaa5_buyhold": "faber_ivy_static", "bench_6040_spy_ief": "bench_6040"}
CONF_RANK = {"exact": 0, "read-from-chart": 1, "second-hand": 2}


def period_verdict(o, q):
    dc = abs(o["cagr"] - q["cagr"]) if "cagr" in q else None
    dd = abs(o["max_dd"] - q["max_dd"]) if "max_dd" in q else 0.0
    if dc is None:
        return "compare"
    if dc <= 0.01 and dd <= 0.03:
        return "close"
    if dc <= 0.025 and dd <= 0.06:
        return "broadly consistent"
    return "differs"


def pick_primary(rows):
    """One headline comparison per strategy: yearly returns (most years, best confidence) beat period stats."""
    by = {}
    for k, r in enumerate(rows):
        if r.get("verdict") in ("not in lab", "no usable figures", "insufficient overlap", "partial overlap"):
            continue
        conf = CONF_RANK.get((r.get("confidence") or "second-hand")[:15].split()[0], 2)
        if r.get("method") == "calendar-year returns" and r["n_years"] >= 5:
            key = (0, conf, -r["n_years"])
        elif r.get("method") == "period statistics" and r.get("ours"):
            months = r["ours"]["months"]
            key = (1, conf, -months)
        else:
            continue
        sid = r["strategy_id"]
        pref = PREFERRED.get(sid)
        if pref and r.get("published") and all(abs(r["published"].get(k, 9) - v) < 1e-9 for k, v in pref.items()):
            key = (-1,)
        if sid not in by or key < by[sid][0]:
            by[sid] = (key, k)
    for sid, (_, k) in by.items():
        rows[k]["primary"] = True
    return rows


def main():
    pub_path = ROOT / "research" / "published_benchmarks.json"
    if not pub_path.exists():
        print("no published_benchmarks.json yet")
        return
    published = json.loads(pub_path.read_text(encoding="utf-8"))
    rets = json.loads((ROOT / "docs" / "data" / "returns.json").read_text(encoding="utf-8"))
    names = {s["id"]: s["name"] for s in json.loads((ROOT / "docs" / "data" / "strategies.json").read_text(encoding="utf-8"))}
    dates, cash, series = rets["dates"], rets["cash"], rets["series"]
    out = []
    for p in published:
        sid = ALIASES.get(p.get("strategy_id"), p.get("strategy_id"))
        if sid not in series:
            out.append({**{k: p.get(k) for k in ("source_title", "source_url", "location")}, "strategy_id": sid,
                        "verdict": "not in lab", "notes": p.get("notes", "")})
            continue
        ours_annual = annual_from_monthly(dates, series[sid])
        row = {"strategy_id": sid, "name": names.get(sid, sid), "source_title": p.get("source_title"),
               "source_url": p.get("source_url"), "location": p.get("location"), "confidence": p.get("confidence"),
               "proxies": p.get("proxies"), "costs": p.get("costs"), "source_notes": p.get("notes", "")}
        pa = p.get("annual_returns") or {}
        years = sorted(y for y in pa if y in ours_annual and pa[y] is not None and y >= "2000")
        if years:
            a = [ours_annual[y] for y in years]
            b = [float(pa[y]) for y in years]
            diffs = [x - y for x, y in zip(a, b)]
            c = corr(a, b)
            mad = sum(abs(d) for d in diffs) / len(diffs)
            row.update({"method": "calendar-year returns", "years": f"{years[0]}-{years[-1]}", "n_years": len(years),
                        "corr": c, "mean_abs_diff": mad, "mean_diff": sum(diffs) / len(diffs),
                        "by_year": {y: {"ours": o, "published": q} for y, o, q in zip(years, a, b)},
                        "verdict": verdict(c, mad)})
        elif p.get("stats") and p.get("period"):
            st = p["stats"]
            per = p["period"]
            ours = period_stats(dates, series[sid], cash, per["start"], per["end"])
            if ours:
                full = ours["from"] <= per["start"] or ours["from"][:4] == per["start"][:4]
                row.update({"method": "period statistics", "period": per, "ours": ours, "published": st,
                            "overlap": "full period" if full else f"partial: lab data from {ours['from']}",
                            "verdict": period_verdict(ours, st) if full else "partial overlap"})
            else:
                row.update({"method": "period statistics", "period": per, "verdict": "insufficient overlap"})
        else:
            row["verdict"] = "no usable figures"
        out.append(row)
    out = pick_primary(out)
    for r in out:
        if r.get("primary") and r.get("strategy_id") in LAB_NOTES:
            r["lab_note"] = LAB_NOTES[r["strategy_id"]]
    (ROOT / "docs" / "data" / "replication.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    lines = ["# Replication check: lab backtests vs published figures", "",
             "Generated by `scripts/replication_check.py` from `research/published_benchmarks.json`.", "",
             "| Strategy | Source | Compared | Correlation | Mean abs. diff | Verdict |", "|---|---|---|---:|---:|---|"]
    for r in sorted(out, key=lambda r: (r.get("strategy_id") or "", not r.get("primary"))):
        if r.get("method") == "calendar-year returns":
            c = "–" if r["corr"] is None else f"{r['corr']:.2f}"
            star = " **(headline)**" if r.get("primary") else ""
            lines.append(f"| {r['name']}{star} | {r['source_title']} ({r.get('location') or ''}) | years {r['years']} ({r['n_years']}) | "
                         f"{c} | {r['mean_abs_diff'] * 100:.1f} pp | {r['verdict']} |")
        elif r.get("method") == "period statistics" and r.get("ours"):
            o, q = r["ours"], r["published"]
            comp = ", ".join(f"{k} {o[k] * 100:.1f}% vs {q[k] * 100:.1f}%" if k != "sharpe" else f"Sharpe {o[k]:.2f} vs {q[k]:.2f}"
                             for k in ("cagr", "max_dd", "sharpe") if k in q and o.get(k) is not None)
            star = " **(headline)**" if r.get("primary") else ""
            lines.append(f"| {r['name']}{star} | {r['source_title']} ({r.get('location') or ''}) | {r['period']['start']}–{r['period']['end']}: {comp} | – | – | {r['verdict']} |")
        else:
            lines.append(f"| {r.get('name', r.get('strategy_id'))} | {r.get('source_title')} | – | – | – | {r.get('verdict')} |")
    (ROOT / "research" / "replication_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
