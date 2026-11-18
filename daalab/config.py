"""Project-wide paths and constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "data" / "cache"      # Norgate pulls (licensed; never committed)
WEB_DIR = ROOT / "data" / "web"          # public web downloads (FRED, Ken French, gold)
DOCS_DIR = ROOT / "docs"                 # GitHub Pages site
SITE_DATA = DOCS_DIR / "data"            # derived results the site reads
RESEARCH_DIR = ROOT / "research"

DATA_START = "1988-01-01"   # earliest date pulled from Norgate
EVAL_START = "2000-01-31"   # first month a strategy may hold positions (if its data allows)
COST_PER_TRADE = 0.001      # 0.10% of traded value, charged on every rebalance
CASH = "BIL"                # ticker used for "cash" everywhere

for _d in (CACHE_DIR, WEB_DIR, SITE_DATA):
    _d.mkdir(parents=True, exist_ok=True)
