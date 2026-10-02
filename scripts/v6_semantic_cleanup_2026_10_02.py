#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small semantic cleanup for audit findings that are safe to standardise globally.

This pass only applies exact, known replacements. It deliberately avoids broad
copy rewriting.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP_TOP = {".git", ".github", "docs", "scripts", "data", "backup"}

EXACT_REPLACEMENTS = {
    "en/french-riviera-tourism-statistics/index.html": {
        'href="/#riviera-fit"': 'href="/en/riviera-fit/"',
        "Use Riviera Fit →": "Try Riviera Fit →",
    },
    "en/riviera-guide/french-riviera-or-amalfi-coast/index.html": {
        'href="/#riviera-fit"': 'href="/en/riviera-fit/"',
        "Use Riviera Fit →": "Try Riviera Fit →",
    },
    "en/riviera-guide/nice/index.html": {
        "choose the right Nice base": "choose the right Nice hotel",
        "Not yet - choose the right Nice hotel →": "Not yet: choose the right Nice hotel →",
        "Already booked - build the trip around it →": "Already booked: build the trip around it →",
    },
}

def page_lang(text: str) -> str:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', text, re.I)
    return "fr" if m and m.group(1).lower().startswith("fr") else "en"

def clean_english_heading_colons(text: str) -> str:
    # Only headings, not body copy or URLs.
    def repl(m):
        inner = re.sub(r'\s+:', ':', m.group(2))
        return m.group(1) + inner + m.group(3)
    return re.sub(r'(<h[1-3]\b[^>]*>)(.*?)(</h[1-3]>)', repl, text, flags=re.S | re.I)

def clean_french_labels(text: str) -> str:
    text = text.replace('<span class="day">Mametas rule</span>', '<span class="day">La règle Mametas</span>')
    text = text.replace('<span class="label">MAMETAS RULE</span>', '<span class="label">LA RÈGLE MAMETAS</span>')
    text = text.replace('MAMETAS SAYS', 'RECO MAMETAS')
    text = text.replace('MAMETAS TOOL', 'OUTIL MAMETAS')

    # "Base" is the product vocabulary used by Riviera Fit. Older generations
    # sometimes called the same decision a "point de chute".
    text = text.replace('Choisir son point de chute', 'Choisir sa base')
    text = text.replace('choisir son point de chute', 'choisir sa base')
    text = text.replace('APRÈS LA VILLE · CHOISIR L’HÔTEL', 'APRÈS LA BASE · CHOISIR L’HÔTEL')
    text = text.replace("APRÈS LA VILLE · CHOISIR L'HÔTEL", "APRÈS LA BASE · CHOISIR L'HÔTEL")
    return text

def main() -> None:
    changed = []

    for rel, replacements in EXACT_REPLACEMENTS.items():
        path = ROOT / rel
        if not path.exists():
            raise RuntimeError(f"Expected audit page missing: {rel}")
        text = path.read_text(encoding="utf-8")
        before = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)

    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        before = text
        lang = page_lang(text)
        if lang == "en":
            text = clean_english_heading_colons(text)
        else:
            text = clean_french_labels(text)
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel.as_posix())

    # Regression guards for the concrete audit findings.
    for rel in (
        "en/french-riviera-tourism-statistics/index.html",
        "en/riviera-guide/french-riviera-or-amalfi-coast/index.html",
    ):
        s = (ROOT / rel).read_text(encoding="utf-8")
        if '/#riviera-fit' in s or 'Use Riviera Fit →' in s:
            raise RuntimeError(f"{rel}: legacy Riviera Fit CTA remains")
        if 'href="/en/riviera-fit/"' not in s or 'Try Riviera Fit →' not in s:
            raise RuntimeError(f"{rel}: canonical Riviera Fit CTA missing")

    nice = (ROOT / "en/riviera-guide/nice/index.html").read_text(encoding="utf-8")
    if "choose the right Nice base" in nice:
        raise RuntimeError("Nice EN: hotel CTA still says base")

    for rel in ("riviera-guide/antibes/index.html", "riviera-guide/monaco/index.html"):
        s = (ROOT / rel).read_text(encoding="utf-8")
        if "Mametas rule" in s:
            raise RuntimeError(f"{rel}: English label remains on French page")

    print(f"Semantic cleanup passed; changed {len(set(changed))} pages.")


if __name__ == "__main__":
    main()
