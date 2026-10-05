#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize sibling Plan pages after materialization.

The live audit found that several Plan pages were older generations than the
five-day page. This late pass gives them the same top-of-page system and a hero
image without rewriting itinerary content.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "plan/three-days-riviera/index.html": ("en", "3 DAYS", "/assets/editorial/nice-riviera.jpg", "Nice and the Baie des Anges"),
    "plan/five-days-nice-no-car/index.html": ("en", "5 DAYS", "/assets/editorial/nice-riviera.jpg", "Nice and the Baie des Anges"),
    "plan/seven-days-riviera/index.html": ("en", "7 DAYS", "/assets/editorial/plan-riviera-coast-nice-monaco.jpg", "The Riviera coast between Nice and Monaco"),
    "plan/car-or-no-car/index.html": ("en", "CAR OR NO CAR", "/assets/editorial/riviera-train-hugo.webp", "Regional train on the French Riviera"),
    "plan/real-budget/index.html": ("en", "REAL BUDGET", "/assets/editorial/riviera-beaches-cannes-aerial.webp", "Beach and seafront on the French Riviera"),
    "plan/when-to-go/index.html": ("en", "WHEN TO GO", "/assets/editorial/nice-riviera.jpg", "The French Riviera from Nice"),
    "fr/planifier/trois-jours-cote-d-azur/index.html": ("fr", "3 JOURS", "/assets/editorial/nice-riviera.jpg", "Nice et la baie des Anges"),
    "fr/planifier/cinq-jours-nice-sans-voiture/index.html": ("fr", "5 JOURS", "/assets/editorial/nice-riviera.jpg", "Nice et la baie des Anges"),
    "fr/planifier/sept-jours-cote-d-azur/index.html": ("fr", "7 JOURS", "/assets/editorial/plan-riviera-coast-nice-monaco.jpg", "Le littoral entre Nice et Monaco"),
    "fr/planifier/voiture-ou-pas/index.html": ("fr", "VOITURE OU PAS", "/assets/editorial/riviera-train-hugo.webp", "Un TER sur la Côte d’Azur"),
    "fr/planifier/budget-reel/index.html": ("fr", "BUDGET RÉEL", "/assets/editorial/riviera-beaches-cannes-aerial.webp", "Plage et front de mer sur la Côte d’Azur"),
    "fr/planifier/quand-partir/index.html": ("fr", "QUAND PARTIR", "/assets/editorial/nice-riviera.jpg", "La Côte d’Azur depuis Nice"),
}

def normalize_top(text: str, lang: str, subject: str) -> str:
    parent = "/fr/planifier/" if lang == "fr" else "/plan/"
    back = "← Retour à Préparer" if lang == "fr" else "← Back to Plan"
    eyebrow = f"PLAN · {subject}"

    text = re.sub(
        r'<p class="breadcrumbs">.*?</p>',
        f'<a class="mametas-detail-back" href="{parent}">{back}</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<a class="back"[^>]*>.*?</a>',
        f'<a class="mametas-detail-back" href="{parent}">{back}</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<p class="eyebrow(?: mametas-detail-eyebrow)?">.*?</p>',
        f'<p class="eyebrow mametas-detail-eyebrow">{eyebrow}</p>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<div class="meta(?: mametas-detail-eyebrow)?">.*?</div>',
        f'<div class="meta mametas-detail-eyebrow">{eyebrow}</div>',
        text,
        count=1,
        flags=re.S | re.I,
    )

    # Older pages can lack both a breadcrumb/back link and a usable eyebrow.
    hero = re.search(r'<header\b[^>]*class=["\'][^"\']*article-hero[^"\']*["\'][^>]*>', text, re.I)
    h1 = re.search(r'<h1\b', text, re.I)
    if hero and h1 and hero.end() < h1.start():
        segment = text[hero.end():h1.start()]
        additions = []
        if "mametas-detail-back" not in segment:
            additions.append(f'<a class="mametas-detail-back" href="{parent}">{back}</a>')
        if "mametas-detail-eyebrow" not in segment:
            additions.append(f'<p class="eyebrow mametas-detail-eyebrow">{eyebrow}</p>')
        if additions:
            text = text[:h1.start()] + "".join(additions) + text[h1.start():]
    return text

def add_cover(text: str, src: str, alt: str) -> str:
    if 'class="article-cover"' in text:
        return text
    hero = re.search(
        r'<header\\b[^>]*class=["\\'][^"\\']*article-hero[^"\\']*["\\'][^>]*>[\\s\\S]*?</header>',
        text,
        re.I,
    )
    if not hero:
        return text
    pos = hero.end()
    cover = f'<div class="article-cover mametas-plan-cover"><img src="{src}" alt="{alt}" loading="eager"></div>'
    return text[:pos] + cover + text[pos:]

def main() -> None:
    changed = []
    found = 0
    for rel, (lang, subject, src, alt) in TARGETS.items():
        path = ROOT / rel
        if not path.exists():
            continue
        found += 1
        text = path.read_text(encoding="utf-8")
        before = text
        text = normalize_top(text, lang, subject)
        text = add_cover(text, src, alt)
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)

        if "mametas-detail-back" not in text or "mametas-detail-eyebrow" not in text:
            raise RuntimeError(f"{rel}: Plan top normalization missing")
        if 'class="article-cover' not in text:
            raise RuntimeError(f"{rel}: Plan hero image missing")

    if found < 2:
        raise RuntimeError("Plan normalization could not find even the two source-controlled Plan pages")

    print(f"Plan family normalization passed on {found} pages; changed {len(changed)}.")


if __name__ == "__main__":
    main()
