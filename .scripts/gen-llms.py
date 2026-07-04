#!/usr/bin/env python3
"""Regenerate llms.txt from note frontmatter.

Deterministic: title and blurb come from config.json, hub order from its
nav, descriptions from each note's frontmatter. Run `task llms` before
publishing from Obsidian. See CLAUDE.md.
"""

import glob
import json
import re
import sys
import urllib.parse
from pathlib import Path

BASE = "https://crbgc-philoserf.flowershow.me"
GOVERNANCE_SITE = "https://crbgc.org"

ROOT = Path(__file__).resolve().parent.parent

# The Flowershow plugin's excludePatterns is the single source of truth for
# what publishes. Its config is gitignored (it holds a token), so fall back
# to a mirror of the list when it is absent; the mirror only needs the
# patterns that can match *.md at the vault root.
PLUGIN_DATA = ROOT / ".obsidian" / "plugins" / "flowershow" / "data.json"
FALLBACK_PATTERNS = (
    r"^CLAUDE\.md$",
    r"^_",
    r"^Drafts/",
    r"^Private/",
    r"Rules of Golf\.md",
)


def exclude_patterns() -> list[re.Pattern]:
    try:
        patterns = json.loads(PLUGIN_DATA.read_text(encoding="utf-8"))[
            "excludePatterns"
        ]
    except (OSError, KeyError, ValueError):
        patterns = FALLBACK_PATTERNS
    return [re.compile(p) for p in patterns]


EXCLUDE = exclude_patterns()


def excluded(path: str) -> bool:
    return any(r.search(path) for r in EXCLUDE)


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    body = m.group(1)
    d = {}
    for key in ("title", "description"):
        km = re.search(rf"^{key}:\s*(.+)$", body, re.M)
        if km:
            d[key] = km.group(1).strip().strip('"').strip("'")
    # tags: either a YAML block (- index) or an inline array ([a, index])
    block = re.search(r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", body, re.M)
    inline = re.search(r"^tags:\s*\[(.*?)\]", body, re.M)
    tags = block.group(1) if block else (inline.group(1) if inline else "")
    d["index"] = bool(re.search(r"(^|[\s,\-])index(\s|,|$)", tags))
    return d


def link(slug: str, note: dict) -> str:
    url = f"{BASE}/{urllib.parse.quote(slug)}"
    desc = note.get("description", "").strip()
    return f"- [{note.get('title', slug)}]({url})" + (f": {desc}" if desc else "")


def main() -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    title = config.get("title", "Notes")
    blurb = config.get("description", "").strip()
    nav_order = [
        link["href"].lstrip("/")
        for link in config.get("nav", {}).get("links", [])
    ]

    notes = {}
    for f in sorted(glob.glob("*.md", root_dir=ROOT)):
        if excluded(f):
            continue
        notes[f[:-3]] = frontmatter(ROOT / f)

    hub_slugs = [s for s in notes if notes[s].get("index")]
    # Hubs in nav order first, then any index notes not in the nav.
    hubs = [s for s in nav_order if s in hub_slugs]
    hubs += sorted(s for s in hub_slugs if s not in hubs)
    rest = sorted(s for s in notes if s not in set(hubs))

    out = [
        f"# {title}",
        "",
        f"> {blurb}",
        "",
        f"A digital garden by Mark Ayers — the informal, editorial companion "
        f"to the Common & Recent Bogey Golf Club governance site at "
        f"{GOVERNANCE_SITE}. Notes are organized around a handful of index "
        f"hubs; each hub links out to its notes. The full note list follows.",
        "",
        "## Topics",
        "",
        *[link(s, notes[s]) for s in hubs],
        "",
        "## All notes",
        "",
        *[link(s, notes[s]) for s in rest],
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"llms.txt: {len(hubs)} hubs, {len(rest)} notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
