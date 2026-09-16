#!/usr/bin/env python3
"""Cache-bust the repaired Fondation Maeght image on every visible FR/EN entry point."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "culture/index.html",
    "en/culture/index.html",
    "culture/fondation-maeght/index.html",
    "en/culture/fondation-maeght/index.html",
)
ASSET = "fondation-maeght-waterborough.webp"
VERSIONED = ASSET + "?v=20260916b"
PATTERN = re.compile(re.escape(ASSET) + r"(?:\?v=[A-Za-z0-9._-]+)?")

for rel in PAGES:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    new_text, count = PATTERN.subn(VERSIONED, text)
    if count == 0:
        raise RuntimeError(f"Fondation Maeght image reference not found in {rel}")
    path.write_text(new_text, encoding="utf-8")
    print(f"Cache-busted Fondation Maeght image: {rel} ({count} reference(s))")
