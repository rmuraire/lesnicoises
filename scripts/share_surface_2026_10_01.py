#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PREFIXES = (
    "en/explore/", "explore/",
    "en/riviera-guide/", "riviera-guide/",
    "en/good-finds/", "bons-plans/",
    "en/culture/", "culture/",
    "en/beaches/", "plages/",
    "en/day-trips/", "escapades/",
    "plan/", "fr/planifier/",
    "en/practical/", "pratique/",
    "en/solo-female-french-riviera/", "cote-dazur-femme-solo/",
    "en/gay-french-riviera/", "cote-dazur-gay/",
    "en/gay-nice/", "guide-gay-nice/",
)

SHARE_CSS = '<link rel="stylesheet" href="/assets/share.css?v=1.0">'
SHARE_JS = '<script defer src="/assets/share.js?v=1.0"></script>'

def is_editorial(rel: str) -> bool:
    return rel.endswith(".html") and any(rel.startswith(prefix) for prefix in PREFIXES)

def inject_once(text: str, needle: str, before: str) -> str:
    if needle in text:
        return text
    if before not in text:
        raise RuntimeError(f"Cannot inject {needle}: missing {before}")
    return text.replace(before, needle + before, 1)

changed = 0
for path in ROOT.rglob("*.html"):
    rel = path.relative_to(ROOT).as_posix()
    if not is_editorial(rel):
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    text = inject_once(text, SHARE_CSS, "</head>")
    text = inject_once(text, SHARE_JS, "</body>")
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed += 1

# Riviera Fit shares a personalised result from riviera-chooser.js, so it only
# needs the shared button styling and cache-busted chooser assets.
for rel in (
    "en/riviera-chooser/index.html", "riviera-chooser/index.html",
    "en/riviera-fit/index.html", "riviera-fit/index.html",
):
    path = ROOT / rel
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    text = inject_once(text, SHARE_CSS, "</head>")
    text = re.sub(r'/assets/riviera-chooser\.js(?:\?v=[^"]+)?', '/assets/riviera-chooser.js?v=14', text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed += 1

print(f"Mametas share surface applied to {changed} HTML files")
