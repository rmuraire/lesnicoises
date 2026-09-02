#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

replacements = {
    "en/riviera-guide/antibes/index.html": [
        (
            '<h2 id="stay">Where to stay: Mametas still needs more mid-range options</h2>\n<p>Our current shortlist is strong on Cap d’Antibes, with the <a href="/en/hotels/cap-d-antibes/cap-d-antibes-beach-hotel/">Cap d’Antibes Beach Hotel</a> and <a href="/en/hotels/cap-d-antibes/la-villa-cap-d-antibes/">La Villa Cap d’Antibes</a>. What we still lack are defendable options in Antibes itself, especially at more reasonable prices.</p>\n<div class="itinerary-stay-prompt">\n<a href="/en/hotels/cap-d-antibes/cap-d-antibes-beach-hotel/"><span>Cap d’Antibes</span><strong>Cap d’Antibes Beach Hotel</strong><small>When beach, design and the hotel itself are part of the plan.</small></a>\n<a href="/en/hotels/cap-d-antibes/la-villa-cap-d-antibes/"><span>Cap d’Antibes</span><strong>La Villa Cap d’Antibes</strong><small>A quieter alternative, still on the Cap side.</small></a>',
            '<h2 id="stay">Where to stay in Antibes</h2>\n<p>For the old town, restaurants and easy access to the station, start in Antibes itself. Hôtel La Place is the sensible mid-range base; La Villa Port d’Antibes is the more polished option. Choose the Cap when the hotel, gardens and sea are meant to be a bigger part of the stay.</p>\n<div class="itinerary-stay-prompt">\n<a href="/en/hotels/antibes/hotel-la-place/"><span>Antibes</span><strong>Hôtel La Place</strong><small>Compact, central and better aligned with a normal holiday budget.</small></a>\n<a href="/en/hotels/antibes/la-villa-port-antibes/"><span>Antibes</span><strong>La Villa Port d’Antibes & Spa</strong><small>A more polished no-car base near the port, old town and station.</small></a>'
        ),
    ],
    "riviera-guide/antibes/index.html": [
        (
            '<h2 id="dormir">Où dormir : le catalogue Mametas doit encore descendre en gamme</h2>\n<p>Notre sélection actuelle est bonne au Cap d’Antibes, avec le <a href="/hotels/cap-d-antibes/cap-d-antibes-beach-hotel/">Cap d’Antibes Beach Hotel</a> et <a href="/hotels/cap-d-antibes/la-villa-cap-d-antibes/">La Villa Cap d’Antibes</a>. En revanche, il nous manque encore des options solides dans Antibes même, notamment à un niveau de prix plus raisonnable.</p>\n<div class="itinerary-stay-prompt">\n<a href="/hotels/cap-d-antibes/cap-d-antibes-beach-hotel/"><span>Cap d’Antibes</span><strong>Cap d’Antibes Beach Hotel</strong><small>Quand plage, design et hôtel font partie du programme.</small></a>\n<a href="/hotels/cap-d-antibes/la-villa-cap-d-antibes/"><span>Cap d’Antibes</span><strong>La Villa Cap d’Antibes</strong><small>Une option plus discrète, toujours côté Cap.</small></a>',
            '<h2 id="dormir">Où dormir à Antibes</h2>\n<p>Pour la vieille ville, les restaurants et l’accès facile à la gare, commencez par Antibes même. Hôtel La Place est l’option milieu de gamme raisonnable ; La Villa Port d’Antibes est le choix plus soigné. Choisissez plutôt le Cap si l’hôtel, les jardins et la mer doivent prendre davantage de place dans le séjour.</p>\n<div class="itinerary-stay-prompt">\n<a href="/hotels/antibes/hotel-la-place/"><span>Antibes</span><strong>Hôtel La Place</strong><small>Compact, central et plus proche d’un budget de vacances normal.</small></a>\n<a href="/hotels/antibes/la-villa-port-antibes/"><span>Antibes</span><strong>La Villa Port d’Antibes & Spa</strong><small>Une base plus soignée, pratique sans voiture, près du port, de la vieille ville et de la gare.</small></a>'
        ),
    ],
    "index.html": [
        (
            '<div class="stay-intro"><p class="eyebrow">Where to stay</p><h2>A beautiful hotel can still be the wrong hotel.</h2><p>Our cards start with the use case and end with the catch. Rates change; geography and compromises tend to be more reliable.</p><a class="button secondary" href="/stay/nice/">Choose your Nice hotel</a></div>',
            '<div class="stay-intro"><p class="eyebrow">Where to stay in Nice</p><h2>A beautiful hotel can still be the wrong hotel.</h2><p>Nice is our default first-trip base. Our cards start with the use case and end with the catch. Rates change; geography and compromises tend to be more reliable.</p><a class="button secondary" href="/stay/nice/">Choose your Nice hotel</a></div>'
        ),
    ],
    "fr/index.html": [
        (
            '<div class="stay-intro"><p class="eyebrow">Où dormir</p><h2>Un bel hôtel peut rester le mauvais hôtel.</h2><p>Nos cartes commencent par l’usage et se terminent par le compromis. Les prix changent ; la géographie et les inconvénients sont souvent plus fiables.</p><a class="button secondary" href="/fr/dormir/nice/">Choisir son hôtel à Nice</a></div>',
            '<div class="stay-intro"><p class="eyebrow">Où dormir à Nice</p><h2>Un bel hôtel peut rester le mauvais hôtel.</h2><p>Pour un premier séjour, Nice reste notre base par défaut. Nos cartes commencent par l’usage et se terminent par le compromis. Les prix changent ; la géographie et les inconvénients sont souvent plus fiables.</p><a class="button secondary" href="/fr/dormir/nice/">Choisir son hôtel à Nice</a></div>'
        ),
    ],
}

changed = []
for rel, pairs in replacements.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"Expected source block not found in {rel}")
        text = text.replace(old, new, 1)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(rel)

print("Updated:")
for rel in changed:
    print(f"- {rel}")
