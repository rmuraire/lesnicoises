#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    "index.html",
    "fr/index.html",
    "en/riviera-guide/antibes/index.html",
    "riviera-guide/antibes/index.html",
]
MARKER = "<!-- Mametas automated deployment sync -->"

changed = []
for rel in TARGETS:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        continue
    if "</body>" not in text:
        raise SystemExit(f"Missing </body> in {rel}")
    text = text.replace("</body>", f"{MARKER}\n</body>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

print("Pages marked for deployment:")
for rel in changed:
    print(f"- {rel}")
