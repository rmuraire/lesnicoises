#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Canonical destination decision data. This is the single source used by every
# destination Reality Check so labels and mobility wording cannot drift again.
BASES = {
    "nice": {
        "fr": ("Voiture inutile pour un premier séjour", "€€ à €€€€", "Très solide toute l’année", "Faible"),
        "en": ("No car needed for a first trip", "€€ to €€€€", "Strong year-round", "Low"),
    },
    "cannes": {
        "fr": ("Très simple sans voiture", "€€ à €€€€", "Printemps à début automne", "Faible, sauf grands événements"),
        "en": ("Very easy without a car", "€€ to €€€€", "Spring to early autumn", "Low, except during major events"),
    },
    "antibes": {
        "fr": ("Oui sans voiture en ville. Le Cap demande plus.", "€€ à €€€€", "Mai à septembre pour la plage", "Faible en ville, moyenne sur le Cap"),
        "en": ("Yes without a car in town. The Cap asks for more.", "€€ to €€€€", "May to September for beach time", "Low in town, medium on the Cap"),
    },
    "villefranche": {
        "fr": ("Possible sans voiture, moins fluide que Nice", "€€ à €€€€", "Printemps et automne sont très faciles à aimer", "Moyenne : relief et correspondances"),
        "en": ("Car-free works, less seamlessly than Nice", "€€ to €€€€", "Spring and autumn are particularly easy", "Medium: hills and transfers"),
    },
    "monaco": {
        "fr": ("Sans voiture recommandé", "€€€ à €€€€", "Toute l’année, avec pics lors des grands événements", "Moyenne : relief et budget"),
        "en": ("No car recommended", "€€€ to €€€€", "Year-round, with event-driven spikes", "Medium: hills and spend"),
    },
    "menton": {
        "fr": ("Très bon sans voiture", "€ à €€€", "Très agréable hors plein été", "Faible à moyenne : vous êtes très à l’est"),
        "en": ("Very good without a car", "€ to €€€", "Particularly good outside peak summer", "Low to medium: you are far east"),
    },
    "eze": {
        "fr": ("Bus direct vers le village, ou train + correspondance", "€€ à €€€€", "Toute l’année ; tôt ou tard en haute saison", "Moyenne : Èze-sur-Mer et Èze Village sont distincts"),
        "en": ("Direct bus to the village, or train + connection", "€€ to €€€€", "Year-round; early or late in peak season", "Medium: Èze-sur-Mer and Èze Village are different stops"),
    },
    "sainttropez": {
        "fr": ("Voiture, bateau ou transferts à organiser", "€€€ à €€€€", "Mai à septembre, avec forte pression en été", "Élevée"),
        "en": ("Car, boat or transfers need planning", "€€€ to €€€€", "May to September, with heavy summer pressure", "High"),
    },
    "saintpaul": {
        "fr": ("Voiture très utile. Bus possible.", "€€ à €€€€", "Printemps et automne sont les plus souples", "Moyenne à élevée : accès intérieur"),
        "en": ("A car is very useful. Bus is possible.", "€€ to €€€€", "Spring and autumn are the easiest", "Medium to high: inland access"),
    },
}

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

def block(base: str, lang: str) -> str:
    mobility, budget, season, friction = BASES[base][lang]
    if lang == "fr":
        labels = ("Déplacements", "Budget", "Saison", "Logistique")
        intro = "Ce que cette destination implique vraiment"
        cta = '<a href="/riviera-fit/">Tester mon profil dans Riviera Fit →</a>'
    else:
        labels = ("Getting around", "Budget", "Season", "Logistics")
        intro = "What this destination really implies"
        cta = '<a href="/en/riviera-fit/">Run my profile through Riviera Fit →</a>'
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
    fit = "/riviera-fit/" if lang == "fr" else "/en/riviera-fit/"
    if f'href="{fit}"' not in text:
        raise RuntimeError(f"{rel}: canonical Riviera Fit CTA missing")

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
