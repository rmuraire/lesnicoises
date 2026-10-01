#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

SHARE_CSS = '<link rel="stylesheet" href="/assets/share.css?v=1.2">'

def inject_once(text: str, needle: str, before: str) -> str:
    if needle in text:
        return text
    if before not in text:
        raise RuntimeError(f"Cannot inject {needle}: missing {before}")
    return text.replace(before, needle + before, 1)

changed = 0

# Editorial guides load Share universally through consent.js.
# Riviera Fit has its own result-sharing logic inside riviera-chooser.js,
# so it only needs the shared button styling and a fresh chooser asset.
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

print(f"Mametas Share finalised on {changed} Riviera Fit HTML files; editorial Share loads via consent.js")
