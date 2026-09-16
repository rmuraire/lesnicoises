#!/usr/bin/env python3
"""Replace known broken/fragile editorial image references before production deploy.

Several small WebP assets in the repository were truncated even though their file names
and HTML references were valid. Prefer known-good local assets when available and use
the verified Wikimedia source directly for Fondation Maeght.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "/assets/editorial/fondation-maeght-waterborough.webp": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/08_Fondation_Maeght.JPG/960px-08_Fondation_Maeght.JPG",
    "/assets/editorial/iles-de-lerins-bruno-attuyt.webp": "/assets/editorial/iles-lerins.jpg",
    "/assets/editorial/musee-matisse-alyona-nagel-pexels.webp": "/assets/editorial/culture-musee-matisse.webp",
    "/assets/editorial/musee-picasso-antibes-clemensfranz.webp": "/assets/editorial/culture-musee-picasso-antibes.webp",
}

LOCAL_TARGETS = [
    "assets/editorial/iles-lerins.jpg",
    "assets/editorial/culture-musee-matisse.webp",
    "assets/editorial/culture-musee-picasso-antibes.webp",
]

for rel in LOCAL_TARGETS:
    path = ROOT / rel
    if not path.is_file() or path.stat().st_size < 20_000:
        raise SystemExit(f"Expected healthy replacement asset missing or suspiciously small: {rel}")

changed_files = 0
replacements_made = 0
for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    original = text
    for bad, good in REPLACEMENTS.items():
        count = text.count(bad)
        if count:
            text = text.replace(bad, good)
            replacements_made += count
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed_files += 1
        print(f"Repaired editorial image refs: {path.relative_to(ROOT)}")

remaining = []
for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    for bad in REPLACEMENTS:
        if bad in text:
            remaining.append(f"{path.relative_to(ROOT)}: {bad}")

if remaining:
    raise SystemExit("Known-bad editorial image references remain:\n" + "\n".join(remaining))

print(f"Editorial image hotfix complete: {replacements_made} refs across {changed_files} HTML files.")
