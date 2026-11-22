"""Strategy descriptions come from the research catalogs (research/strategies_*.json), so the
plain-English text on the website and the rules in the code are documented in one place."""
from __future__ import annotations

import json
from functools import lru_cache

from ..config import RESEARCH_DIR

FILES = ["strategies_keller_antonacci.json", "strategies_others.json", "macro_strategies.json", "strategies_additions.json"]


@lru_cache(maxsize=None)
def catalog() -> dict:
    out = {}
    for f in FILES:
        p = RESEARCH_DIR / f
        if p.exists():
            for item in json.loads(p.read_text(encoding="utf-8")):
                out[item["id"]] = item
    return out


def meta(spec_id: str, *, id: str | None = None, assets: list[str], **overrides) -> dict:
    """Keyword arguments for @register, filled from the catalog entry `spec_id`."""
    c = catalog().get(spec_id, {})
    src = c.get("source") or {}
    kw = dict(
        id=id or spec_id,
        name=c.get("name", spec_id),
        author=c.get("author", ""),
        family=c.get("family", "other"),
        year=int(src.get("year") or 0),
        source_title=src.get("title", ""),
        source_url=src.get("url", ""),
        allocatesmartly_url=c.get("allocatesmartly_url"),
        plain_english=c.get("plain_english", ""),
        rules=list(c.get("rules", [])),
        notes=c.get("notes", ""),
        assets=assets,
    )
    extra_note = overrides.pop("notes", "")
    kw.update(overrides)
    if extra_note:
        kw["notes"] = (kw["notes"] + " Lab implementation: " + extra_note).strip()
    return kw
