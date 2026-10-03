#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas coherence audit — phase 2: destination-page system.

Late build pass. It normalises only the reusable destination-page chrome:
named parent link, eyebrow, Reality Check and Riviera Fit CTA. Editorial H1s,
body sections, hotel selections, sources and images are intentionally left
untouched.
"""
from pathlib import Path
import html
import re

from mametas_coherence_config import (
    DESTINATIONS,
    DESTINATION_BACK,
    REALITY_LABELS,
    RIVIERA_FIT,
)

ROOT = Path(__file__).resolve().parents[1]


def reality_block(slug: str, lang: str) -> str:
    cfg = DESTINATIONS[slug]
    labels = REALITY_LABELS[lang]
    values = cfg["reality"][lang]
    fit_href, fit_label = RIVIERA_FIT[lang]
    title = "What this place really implies" if lang == "en" else "Ce que cette destination implique vraiment"
    cells = "".join(
        f"<div><b>{html.escape(label)}</b><span>{html.escape(value)}</span></div>"
        for label, value in zip(labels, values)
    )
    return (
        '<section class="destination-reality" data-destination-reality="canonical">'
        '<div class="destination-reality-head"><span>REALITY CHECK</span>'
        f"<strong>{html.escape(title)}</strong></div>"
        f'<div class="destination-reality-grid">{cells}</div>'
        f'<div class="destination-reality-cta"><a href="{fit_href}">{html.escape(fit_label)}</a></div>'
        "</section>"
    )


def canonical_back(lang: str) -> str:
    href, label = DESTINATION_BACK[lang]
    return f'<a class="mametas-detail-back" href="{href}">{html.escape(label)}</a>'


def normalise_top(text: str, slug: str, lang: str) -> str:
    name = DESTINATIONS[slug]["name"][lang]
    back = canonical_back(lang)

    # V3-generation pages use breadcrumbs; recent site.css pages use .back.
    text, n = re.subn(
        r'<p class="breadcrumbs">[\s\S]*?</p>',
        back,
        text,
        count=1,
        flags=re.I,
    )
    if n == 0:
        text, n = re.subn(
            r'<a\b[^>]*class=["\'][^"\']*\bback\b[^"\']*["\'][^>]*>[\s\S]*?</a>',
            back,
            text,
            count=1,
            flags=re.I,
        )

    if n == 0:
        # Last-resort insertion without touching body copy.
        m = re.search(r'(<header\b[^>]*class=["\'][^"\']*article-hero[^"\']*["\'][^>]*>\s*<div\b[^>]*class=["\'][^"\']*wrap[^"\']*["\'][^>]*>)', text, re.I)
        if m:
            text = text[:m.end()] + back + text[m.end():]
        else:
            m = re.search(r'<article\b[^>]*>', text, re.I)
            if not m:
                raise RuntimeError(f"{slug}/{lang}: cannot place canonical parent link")
            text = text[:m.end()] + back + text[m.end():]

    eyebrow = ("PLACES" if lang == "en" else "DESTINATIONS") + " · " + name
    if re.search(r'<p\b[^>]*class=["\'][^"\']*\beyebrow\b', text, re.I):
        text = re.sub(
            r'(<p\b[^>]*class=["\'][^"\']*\beyebrow\b[^"\']*["\'][^>]*>)[\s\S]*?(</p>)',
            lambda m: m.group(1) + html.escape(eyebrow) + m.group(2),
            text,
            count=1,
            flags=re.I,
        )
    elif re.search(r'<div\b[^>]*class=["\'][^"\']*\bmeta\b', text, re.I):
        text = re.sub(
            r'(<div\b[^>]*class=["\'][^"\']*\bmeta\b[^"\']*["\'][^>]*>)[\s\S]*?(</div>)',
            lambda m: m.group(1) + html.escape(eyebrow) + m.group(2),
            text,
            count=1,
            flags=re.I,
        )
    else:
        raise RuntimeError(f"{slug}/{lang}: eyebrow/meta marker not found")

    # The old Base / No car / Best for / Checked row duplicates canonical data.
    text = re.sub(r'<div\b[^>]*class=["\'][^"\']*article-meta[^"\']*["\'][^>]*>[\s\S]*?</div>', '', text, count=1, flags=re.I)
    return text


def normalise_reality(text: str, slug: str, lang: str) -> str:
    block = reality_block(slug, lang)

    # Remove any earlier-generation Reality Check first.
    text = re.sub(
        r'<section\b[^>]*class=["\'][^"\']*destination-reality[^"\']*["\'][^>]*>[\s\S]*?</section>',
        '',
        text,
        flags=re.I,
    )

    badge = re.search(r'<a\b[^>]*class=["\'][^"\']*mametas-checked[^"\']*["\'][^>]*>[\s\S]*?</a>', text, flags=re.I)
    if not badge:
        raise RuntimeError(f"{slug}/{lang}: Mametas Checked badge not found")
    return text[:badge.start()] + block + badge.group(0) + text[badge.end():]


def patch(path: Path, slug: str, lang: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="strict")
    before = text
    text = normalise_top(text, slug, lang)
    text = normalise_reality(text, slug, lang)
    if text != before:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = []
    for slug, cfg in DESTINATIONS.items():
        for lang in ("en", "fr"):
            rel = cfg["paths"][lang]
            path = ROOT / rel
            if not path.exists():
                raise RuntimeError(f"Missing destination page: {rel}")
            if patch(path, slug, lang):
                changed.append(rel)

    print(f"Mametas destination system normalised on {len(changed)} pages")
    for rel in changed:
        print("  ", rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
