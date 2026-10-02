#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CITY_SYSTEM_PATH = ROOT / "data/city-system-v1.json"
CITY_SYSTEM = json.loads(CITY_SYSTEM_PATH.read_text(encoding="utf-8"))
CITY_DATA = CITY_SYSTEM["cities"]

PAGES = {
    "riviera-guide/nice/index.html": ("nice","fr","Nice"),
    "en/riviera-guide/nice/index.html": ("nice","en","Nice"),
    "riviera-guide/cannes/index.html": ("cannes","fr","Cannes"),
    "en/riviera-guide/cannes/index.html": ("cannes","en","Cannes"),
    "riviera-guide/antibes/index.html": ("antibes","fr","Antibes"),
    "en/riviera-guide/antibes/index.html": ("antibes","en","Antibes"),
    "riviera-guide/villefranche-cap-ferrat/index.html": ("villefranche","fr","Villefranche & Cap-Ferrat"),
    "en/riviera-guide/villefranche-cap-ferrat/index.html": ("villefranche","en","Villefranche & Cap-Ferrat"),
    "riviera-guide/monaco/index.html": ("monaco","fr","Monaco"),
    "en/riviera-guide/monaco/index.html": ("monaco","en","Monaco"),
    "riviera-guide/menton/index.html": ("menton","fr","Menton"),
    "en/riviera-guide/menton/index.html": ("menton","en","Menton"),
    "riviera-guide/eze/index.html": ("eze","fr","Èze"),
    "en/riviera-guide/eze/index.html": ("eze","en","Èze"),
    "riviera-guide/saint-tropez/index.html": ("sainttropez","fr","Saint-Tropez"),
    "en/riviera-guide/saint-tropez/index.html": ("sainttropez","en","Saint-Tropez"),
    "riviera-guide/saint-paul-de-vence/index.html": ("saintpaul","fr","Saint-Paul-de-Vence"),
    "en/riviera-guide/saint-paul-de-vence/index.html": ("saintpaul","en","Saint-Paul-de-Vence"),
}

def riviera_fit_route(lang: str) -> str:
    """Use the route that exists at the current build stage.

    This script runs twice in production: once before the canonical Riviera Fit
    migration, and once again in the final coherence stage. The early pass must
    keep the legacy chooser link valid for historical validators; the late pass
    automatically switches to the canonical Riviera Fit route.
    """
    if lang == "fr":
        canonical_file = ROOT / "riviera-fit/index.html"
        return "/riviera-fit/" if canonical_file.exists() else "/riviera-chooser/"
    canonical_file = ROOT / "en/riviera-fit/index.html"
    return "/en/riviera-fit/" if canonical_file.exists() else "/en/riviera-chooser/"


def block(base: str, lang: str) -> str:
    reality = CITY_DATA[base]["reality"][lang]
    mobility = reality["getting_around"]
    budget = reality["budget"]
    season = reality["season"]
    friction = reality["logistics"]
    fit_route = riviera_fit_route(lang)
    if lang == "fr":
        labels = ("Déplacements", "Budget", "Saison", "Logistique")
        intro = "Ce que cette destination implique vraiment"
        cta = f'<a href="{fit_route}">Tester mon profil dans Riviera Fit →</a>'
    else:
        labels = ("Getting around", "Budget", "Season", "Logistics")
        intro = "What this destination really implies"
        cta = f'<a href="{fit_route}">Run my profile through Riviera Fit →</a>'
    values = (mobility, budget, season, friction)
    cells = "".join(
        f'<div><b>{label}</b><span>{value}</span></div>'
        for label, value in zip(labels, values)
    )
    return (
        '<section class="destination-reality" data-destination-reality="true">'
        '<div class="destination-reality-head"><span>REALITY CHECK</span>'
        f'<strong>{intro}</strong></div>'
        f'<div class="destination-reality-grid">{cells}</div>'
        f'<div class="destination-reality-cta">{cta}</div>'
        '</section>'
    )

def normalize_top(text: str, lang: str, town: str) -> str:
    parent = "/riviera-guide/" if lang == "fr" else "/en/riviera-guide/"
    back_label = "← Retour aux destinations" if lang == "fr" else "← Back to Places"
    eyebrow = ("DESTINATIONS" if lang == "fr" else "PLACES") + f" · {town}"

    # Old site.css generation: Back link + meta line.
    text = re.sub(
        r'<a class="back"[^>]*>.*?</a>',
        f'<a class="mametas-detail-back" href="{parent}">{back_label}</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<div class="meta">.*?</div>',
        f'<div class="meta mametas-detail-eyebrow">{eyebrow}</div>',
        text,
        count=1,
        flags=re.S | re.I,
    )

    # V3 generation: breadcrumb + eyebrow.
    text = re.sub(
        r'<p class="breadcrumbs">.*?</p>',
        f'<a class="mametas-detail-back" href="{parent}">{back_label}</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<p class="eyebrow">.*?</p>',
        f'<p class="eyebrow mametas-detail-eyebrow">{eyebrow}</p>',
        text,
        count=1,
        flags=re.S | re.I,
    )

    # Legacy Base / No car / Best for / Checked block. The information now lives
    # in Reality Check + canonical city-card data + Mametas Checked.
    text = re.sub(
        r'<div class="article-meta">.*?</div>',
        '',
        text,
        count=1,
        flags=re.S | re.I,
    )
    return text

def patch(rel: str, base: str, lang: str, town: str) -> bool:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text

    text = normalize_top(text, lang, town)
    text = normalize_destination_tail(text, base, lang, town)
    new = block(base, lang)
    if 'data-destination-reality="true"' in text:
        text = re.sub(
            r'<section class="destination-reality" data-destination-reality="true">.*?</section>',
            new,
            text,
            count=1,
            flags=re.S,
        )
    else:
        badge = re.search(r'<a class="mametas-checked"[^>]*>.*?</a>', text, flags=re.S)
        if not badge:
            raise RuntimeError(f"{rel}: Mametas Checked badge not found")
        text = text[:badge.end()] + new + text[badge.end():]

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False

BASE_HOTEL_FIT = {
    "nice": "nice",
    "villefranche": "villefranche",
    "antibes": "antibes",
    "cannes": "cannes",
    "monaco": "monaco",
    "menton": "menton",
}

def normalize_destination_tail(text: str, base: str, lang: str, town: str) -> str:
    if lang == "en":
        replacements = {
            "<h2>Next decisions</h2>": "<h2>The next decision</h2>",
            "<h2>Your next decision</h2>": "<h2>The next decision</h2>",
            ">YOUR NEXT DECISION<": ">THE NEXT DECISION<",
            "<strong>Continue:</strong>": "<strong>The next decision:</strong>",
        }
    else:
        replacements = {
            "<h2>Décisions suivantes</h2>": "<h2>La prochaine décision</h2>",
            "<h2>Votre prochaine décision</h2>": "<h2>La prochaine décision</h2>",
            ">VOTRE PROCHAINE DÉCISION<": ">LA PROCHAINE DÉCISION<",
            "<strong>Continuer :</strong>": "<strong>La prochaine décision :</strong>",
            "<strong>Continuer:</strong>": "<strong>La prochaine décision :</strong>",
        }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Base destinations get one predictable Hotel Fit bridge. Detours keep their
    # destination-specific hotel wording rather than pretending they are Hotel Fit bases.
    fit_base = BASE_HOTEL_FIT.get(base)
    if fit_base and "destination-hotel-fit-cta" not in text:
        if lang == "en":
            href = f"/en/hotels/finder/?base={fit_base}"
            label = f"Choose a hotel in {town} with Hotel Fit →"
        else:
            href = f"/hotels/finder/?base={fit_base}"
            label = f"Choisir un hôtel à {town} avec Hotel Fit →"
        cta = f'<p class="destination-hotel-fit-cta"><a href="{href}">{label}</a></p>'

        # Put it before the closing decision/source layer, never in a hotel card grid.
        anchors = [
            re.search(r'<h2[^>]*>The next decision</h2>', text, re.I),
            re.search(r'<h2[^>]*>La prochaine décision</h2>', text, re.I),
            re.search(r'<div class="sources"\b', text, re.I),
            re.search(r'<div class="source-box"[^>]*><strong>(?:The next decision|La prochaine décision)', text, re.I),
        ]
        target = next((m for m in anchors if m), None)
        if target:
            text = text[:target.start()] + cta + text[target.start():]
        else:
            article_close = text.lower().rfind("</article>")
            if article_close >= 0:
                text = text[:article_close] + cta + text[article_close:]
    return text


def validate_page(rel: str, lang: str, town: str) -> None:
    text = (ROOT / rel).read_text(encoding="utf-8")
    expected_labels = (
        ("Déplacements", "Budget", "Saison", "Logistique")
        if lang == "fr"
        else ("Getting around", "Budget", "Season", "Logistics")
    )
    for needle in expected_labels:
        if f"<b>{needle}</b>" not in text:
            raise RuntimeError(f"{rel}: missing canonical Reality Check label {needle}")
    if text.count('data-destination-reality="true"') != 1:
        raise RuntimeError(f"{rel}: Reality Check missing or duplicated")
    if "article-meta" in text:
        raise RuntimeError(f"{rel}: legacy article-meta still present")
    if "mametas-detail-back" not in text or "mametas-detail-eyebrow" not in text:
        raise RuntimeError(f"{rel}: canonical detail top missing")
    if town not in text:
        raise RuntimeError(f"{rel}: town marker missing")
    fit = riviera_fit_route(lang)
    if f'href="{fit}"' not in text:
        raise RuntimeError(f"{rel}: Riviera Fit CTA missing for current build stage")
    base = PAGES[rel][0]
    if base in BASE_HOTEL_FIT and "destination-hotel-fit-cta" not in text:
        raise RuntimeError(f"{rel}: canonical Hotel Fit bridge missing")

def main() -> int:
    changed = []
    for rel, (base, lang, town) in PAGES.items():
        if patch(rel, base, lang, town):
            changed.append(rel)
    for rel, (_, lang, town) in PAGES.items():
        validate_page(rel, lang, town)
    print(f"Destination coherence passed; patched {len(changed)} pages.")
    for rel in changed:
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
