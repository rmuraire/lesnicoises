#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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
    "sainttropez": {
        "fr": ("Voiture, bateau ou transferts à organiser", "€€€ à €€€€", "Mai à septembre, avec forte pression en été", "Élevée"),
        "en": ("Car, boat or transfers need planning", "€€€ to €€€€", "May to September, with heavy summer pressure", "High"),
    },
    "saintpaul": {
        "fr": ("Voiture très utile. Bus possible.", "€€ à €€€€", "Printemps et automne sont les plus souples", "Moyenne à élevée : base intérieure"),
        "en": ("A car is very useful. Bus is possible.", "€€ to €€€€", "Spring and autumn are the easiest", "Medium to high: inland base"),
    },
}

PAGES = {
    "riviera-guide/nice/index.html": ("nice","fr"),
    "en/riviera-guide/nice/index.html": ("nice","en"),
    "riviera-guide/cannes/index.html": ("cannes","fr"),
    "en/riviera-guide/cannes/index.html": ("cannes","en"),
    "riviera-guide/antibes/index.html": ("antibes","fr"),
    "en/riviera-guide/antibes/index.html": ("antibes","en"),
    "riviera-guide/villefranche-cap-ferrat/index.html": ("villefranche","fr"),
    "en/riviera-guide/villefranche-cap-ferrat/index.html": ("villefranche","en"),
    "riviera-guide/monaco/index.html": ("monaco","fr"),
    "en/riviera-guide/monaco/index.html": ("monaco","en"),
    "riviera-guide/menton/index.html": ("menton","fr"),
    "en/riviera-guide/menton/index.html": ("menton","en"),
    "riviera-guide/saint-tropez/index.html": ("sainttropez","fr"),
    "en/riviera-guide/saint-tropez/index.html": ("sainttropez","en"),
    "riviera-guide/saint-paul-de-vence/index.html": ("saintpaul","fr"),
    "en/riviera-guide/saint-paul-de-vence/index.html": ("saintpaul","en"),
}

def block(base: str, lang: str) -> str:
    mobility, budget, season, friction = BASES[base][lang]
    if lang == "fr":
        labels = ("Mobilité", "Pression budget", "Saison", "Friction")
        intro = "Ce que cette base implique vraiment"
        cta = '<a href="/riviera-chooser/">Tester mon profil dans Riviera Fit →</a>'
    else:
        labels = ("Mobility", "Budget pressure", "Season", "Friction")
        intro = "What this base really implies"
        cta = '<a href="/en/riviera-chooser/">Run my profile through Riviera Fit →</a>'
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

def patch(rel: str, base: str, lang: str) -> bool:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    new = block(base, lang)
    if 'data-destination-reality="true"' in text:
        text = re.sub(
            r'<section class="destination-reality" data-destination-reality="true">.*?</section>',
            new, text, count=1, flags=re.S
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

def main() -> int:
    changed = []
    for rel, (base, lang) in PAGES.items():
        if patch(rel, base, lang):
            changed.append(rel)
    for rel in PAGES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if text.count('data-destination-reality="true"') != 1:
            raise RuntimeError(f"{rel}: Reality Check missing or duplicated")
        if "Riviera Fit" not in text:
            raise RuntimeError(f"{rel}: Riviera Fit CTA missing")
    print(f"Destination Reality Check passed; patched {len(changed)} pages.")
    for rel in changed:
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
