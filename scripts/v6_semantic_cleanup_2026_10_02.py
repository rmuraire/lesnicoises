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

def normalize_source_block_heading(text: str, lang: str) -> str:
    expected = "Sources vérifiées" if lang == "fr" else "Sources checked"
    pattern = re.compile(
        r'<div\b[^>]*class=["\'][^"\']*sources[^"\']*["\'][^>]*>',
        re.I,
    )
    pos = 0
    while True:
        m = pattern.search(text, pos)
        if not m:
            break
        # Work only near the start of the source block; no need to parse the
        # whole page or alter source content.
        window_end = min(len(text), m.end() + 700)
        window = text[m.end():window_end]

        heading = re.search(r'<h[2-4]\b[^>]*>.*?</h[2-4]>', window, re.S | re.I)
        if heading:
            new_heading = f"<h2>{expected}</h2>"
            abs_start = m.end() + heading.start()
            abs_end = m.end() + heading.end()
            text = text[:abs_start] + new_heading + text[abs_end:]
            pos = abs_start + len(new_heading)
            continue

        strong = re.search(
            r'<strong>\s*(?:Checked sources|Verified sources|Sources checked|Sources verified|Sources vérifiées|Sources consultées|Sources)\s*:?</strong>',
            window,
            re.I,
        )
        if strong:
            new_heading = f"<h2>{expected}</h2>"
            abs_start = m.end() + strong.start()
            abs_end = m.end() + strong.end()
            text = text[:abs_start] + new_heading + text[abs_end:]
            pos = abs_start + len(new_heading)
            continue

        # Formal sources block with no visible heading: add one rather than
        # leaving a generation-specific silent block.
        insert = f"<h2>{expected}</h2>"
        text = text[:m.end()] + insert + text[m.end():]
        pos = m.end() + len(insert)
    return text


def clean_french_labels(text: str) -> str:
    text = text.replace('<span class="day">Mametas rule</span>', '<span class="day">La règle Mametas</span>')
    text = text.replace('<span class="label">MAMETAS RULE</span>', '<span class="label">LA RÈGLE MAMETAS</span>')
    text = text.replace('MAMETAS SAYS', 'RECO MAMETAS')
    text = text.replace('MAMETAS TOOL', 'OUTIL MAMETAS')
    text = text.replace('Faire Riviera Fit →', 'Tester Riviera Fit →')

    # "Base" is the one product term retained by the coherence audit. Normalize
    # the historical "point de chute" variants with their surrounding grammar
    # before applying the safe final catch-all.
    replacements = (
        ('Choisir son point de chute', 'Choisir sa base'),
        ('choisir son point de chute', 'choisir sa base'),
        ('Un bon point de chute', 'Une bonne base'),
        ('un bon point de chute', 'une bonne base'),
        ('Le meilleur point de chute', 'La meilleure base'),
        ('le meilleur point de chute', 'la meilleure base'),
        ('Quel point de chute', 'Quelle base'),
        ('quel point de chute', 'quelle base'),
        ('Un point de chute', 'Une base'),
        ('un point de chute', 'une base'),
        ('Le point de chute', 'La base'),
        ('le point de chute', 'la base'),
        ('Du point de chute', 'De la base'),
        ('du point de chute', 'de la base'),
        ('Au point de chute', 'À la base'),
        ('au point de chute', 'à la base'),
        ('Ce point de chute', 'Cette base'),
        ('ce point de chute', 'cette base'),
        ('Votre point de chute', 'Votre base'),
        ('votre point de chute', 'votre base'),
        ('Notre point de chute', 'Notre base'),
        ('notre point de chute', 'notre base'),
        ('Points de chute', 'Bases'),
        ('points de chute', 'bases'),
        ('POINTS DE CHUTE', 'BASES'),
        ('Point de chute', 'Base'),
        ('point de chute', 'base'),
    )
    for old, new in replacements:
        text = text.replace(old, new)

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
            text = text.replace('href="/#riviera-fit"', 'href="/en/riviera-fit/"')
            text = text.replace("href='/#riviera-fit'", "href='/en/riviera-fit/'")
        else:
            text = clean_french_labels(text)
            text = text.replace('href="/#riviera-fit"', 'href="/riviera-fit/"')
            text = text.replace("href='/#riviera-fit'", "href='/riviera-fit/'")
            text = text.replace('href="/fr/#riviera-fit"', 'href="/riviera-fit/"')
            text = text.replace("href='/fr/#riviera-fit'", "href='/riviera-fit/'")
        text = normalize_source_block_heading(text, lang)
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
