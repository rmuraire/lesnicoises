#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "fr": ROOT / "fr/dormir/nice/index.html",
    "en": ROOT / "stay/nice/index.html",
}

ORDER = {
    "fr": {
        "pratique": [
            "hotel-66", "hotel-64-nice", "hotel-florence-nice", "boutique-hotel-nice-cote-dazur",
            "hotel-byakko-nice", "apollinaire-nice", "hotel-khla-nice",
        ],
        "calme": ["villa-victoria", "hotel-le-grimaldi-by-happyculture", "la-perouse"],
        "vivant": ["hotel-amour-nice", "hotel-aston-la-scala", "hotel-du-couvent", "maison-albar-le-victoria"],
        "chic": [
            "hotel-beau-rivage", "hotel-west-end-nice-promenade", "boscolo-nice-hotel-and-spa",
            "palais-de-la-mediterranee", "anantara-plaza-nice", "le-negresco",
        ],
    },
    "en": {
        "practical": [
            "hotel-66", "hotel-64-nice", "hotel-florence-nice", "boutique-hotel-nice-cote-dazur",
            "hotel-byakko-nice", "apollinaire-nice", "hotel-khla-nice",
        ],
        "quiet": ["villa-victoria", "hotel-le-grimaldi-by-happyculture", "la-perouse"],
        "active": ["hotel-amour-nice", "hotel-aston-la-scala", "hotel-du-couvent", "maison-albar-le-victoria"],
        "chic": [
            "hotel-beau-rivage", "hotel-west-end-nice-promenade", "boscolo-nice-hotel-and-spa",
            "palais-de-la-mediterranee", "anantara-plaza-nice", "le-negresco",
        ],
    },
}


def card_key(card: str) -> str:
    m = re.search(r'data-hotel="([^"]+)"', card)
    if m:
        return m.group(1)
    m = re.search(r'href="/(?:en/)?hotels/nice/([^/]+)/"', card)
    if m:
        return m.group(1)
    return ""


def reorder_section(text: str, section_id: str, wanted: list[str]) -> str:
    marker = f'id="{section_id}"'
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError(f"Missing Nice hotel section: {section_id}")
    section_start = text.rfind("<section", 0, pos)
    section_end = text.find("</section>", pos)
    if section_start < 0 or section_end < 0:
        raise RuntimeError(f"Malformed Nice hotel section: {section_id}")
    grid_start = text.find('<div class="hotel-choice-grid">', pos, section_end)
    if grid_start < 0:
        raise RuntimeError(f"Missing hotel grid in section: {section_id}")
    cards = re.findall(r'<article class="hotel-choice-card".*?</article>', text[grid_start:section_end], flags=re.S)
    by_key = {card_key(card): card for card in cards}
    missing = [k for k in wanted if k not in by_key]
    if missing:
        raise RuntimeError(f"Section {section_id}: expected hotel cards missing: {missing}")
    if len(cards) != len(wanted):
        extra = [card_key(c) for c in cards if card_key(c) not in wanted]
        raise RuntimeError(f"Section {section_id}: unexpected hotel cards: {extra}")
    ordered = "".join(by_key[k] for k in wanted)
    first = text.find(cards[0], grid_start, section_end)
    last = text.find(cards[-1], first, section_end) + len(cards[-1])
    return text[:first] + ordered + text[last:]


def compass(lang: str) -> str:
    if lang == "fr":
        return (
            '<section class="v3-section hotel-chooser hotel-price-compass" id="niveau-budget"><div class="wrap">'
            '<div class="chooser-intro"><div><p class="eyebrow">Le bon niveau de dépense</p>'
            '<h2>Le milieu de gamme n’est plus un trou dans la raquette.</h2></div>'
            '<p>Les prix bougent selon les dates, donc on ne vous invente pas de faux seuils. Mais la logique est claire : dépense intelligente, milieu-haut de gamme avec du caractère, ou hôtel-expérience.</p></div>'
            '<nav class="style-nav">'
            '<a href="#pratique"><span>€€</span><strong>Dépense intelligente</strong><small>Hotel 64 · Florence · Hotel 66 · Byakko</small></a>'
            '<a href="#calme"><span>€€€</span><strong>Le bon milieu-haut</strong><small>Villa Victoria · Le Grimaldi · Hotel Amour · Beau Rivage</small></a>'
            '<a href="#chic"><span>€€€€</span><strong>Monter en gamme exprès</strong><small>La Pérouse · Boscolo · Couvent · Negresco · Anantara</small></a>'
            '</nav><p class="article-meta"><span>Repères relatifs, pas tarifs fixes</span><span>Les prix varient fortement selon les dates</span></p>'
            '</div></section>'
        )
    return (
        '<section class="v3-section hotel-chooser hotel-price-compass" id="budget-level"><div class="wrap">'
        '<div class="chooser-intro"><div><p class="eyebrow">Choose the spend level</p>'
        '<h2>The missing middle is no longer missing.</h2></div>'
        '<p>Rates move too much by date for fake price bands to be useful. The decision is simpler: smart spend, upper-mid with character, or a hotel that is deliberately part of the experience.</p></div>'
        '<nav class="style-nav">'
        '<a href="#practical"><span>€€</span><strong>Smart spend</strong><small>Hotel 64 · Florence · Hotel 66 · Byakko</small></a>'
        '<a href="#quiet"><span>€€€</span><strong>Upper-mid sweet spot</strong><small>Villa Victoria · Le Grimaldi · Hotel Amour · Beau Rivage</small></a>'
        '<a href="#chic"><span>€€€€</span><strong>Splurge deliberately</strong><small>La Pérouse · Boscolo · Couvent · Negresco · Anantara</small></a>'
        '</nav><p class="article-meta"><span>Relative positioning, not fixed rates</span><span>Prices swing heavily by date</span></p>'
        '</div></section>'
    )


def patch_copy(text: str, lang: str) -> str:
    if lang == "fr":
        text = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="20 hôtels sélectionnés à Nice, du bon milieu de gamme au luxe, classés par usage : sans voiture, vivant, calme ou hôtel-expérience.">', text, count=1)
        text = re.sub(r'<p class="article-deck">.*?</p>', '<p class="article-deck">Vingt hôtels, quatre styles de séjour, du choix rationnel au vrai luxe. Commencez par le rôle que doit jouer l’hôtel, puis décidez combien vous voulez y mettre.</p>', text, count=1, flags=re.S)
        text = text.replace('<span>13 septembre 2026</span>', '<span>14 septembre 2026</span>')
        replacements = {
            '<div><span>01 · Pratique</span><h2>Nice est votre base pour rayonner.</h2></div><p>L’accès à la gare et une géographie intelligente battent une vue mer théorique quand vous bougez tous les jours.</p>': '<div><span>01 · Pratique</span><h2>Nice est votre base pour rayonner.</h2></div><p>Sept options, dont plusieurs vraies cartes milieu de gamme : ici la gare, la marche et une géographie intelligente comptent davantage que le prestige du lobby.</p>',
            '<div><span>02 · Calme</span><h2>Vous voulez Nice, mais pas tout Nice dans votre chambre.</h2></div><p>Villa Victoria nous donne enfin une vraie carte centrale calme en dehors de la logique palace.</p>': '<div><span>02 · Calme</span><h2>Vous voulez Nice, mais pas tout Nice dans votre chambre.</h2></div><p>Villa Victoria et Le Grimaldi forment désormais un vrai milieu-haut central et posé ; La Pérouse ajoute la mer quand le budget monte.</p>',
            '<div><span>03 · Vivant</span><h2>Vous voulez la ville en sortant de l’hôtel.</h2></div><p>Vieux-Nice et Masséna restent les meilleurs choix quand les soirées comptent.</p>': '<div><span>03 · Vivant</span><h2>Vous voulez la ville en sortant de l’hôtel.</h2></div><p>Hotel Amour et Aston La Scala rendent enfin cette catégorie moins exclusivement luxe ; le Couvent et Maison Albar restent les choix où l’hôtel pèse davantage dans le budget.</p>',
            '<div><span>04 · Chic & expérience</span><h2>L’hôtel fait partie de la raison du voyage.</h2></div><p>Mer, spa, histoire ou grand confort : ici, on paie aussi pour l’hôtel lui-même. Autant le faire consciemment.</p>': '<div><span>04 · Chic & expérience</span><h2>L’hôtel fait partie de la raison du voyage.</h2></div><p>Beau Rivage et West End permettent d’entrer dans la logique mer sans passer directement au palace ; Boscolo, Anantara, Palais et Negresco assument ensuite clairement la montée en gamme.</p>',
        }
    else:
        text = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="20 selected Nice hotels from smart mid-range to luxury, organised by use: car-free, lively, quiet or hotel-as-experience.">', text, count=1)
        text = re.sub(r'<p class="article-deck">.*?</p>', '<p class="article-deck">Twenty hotels, four trip styles, from rational mid-range choices to real luxury. Decide what the hotel needs to do first, then decide how much you want to spend.</p>', text, count=1, flags=re.S)
        text = text.replace('<span>13 September 2026</span>', '<span>14 September 2026</span>')
        replacements = {
            '<div><span>01 · Practical</span><h2>You are here to use Nice as a base.</h2></div><p>Train access and sensible geography beat a theoretical sea view when you plan to move every day.</p>': '<div><span>01 · Practical</span><h2>You are here to use Nice as a base.</h2></div><p>Seven options now include several genuine mid-range cards: station access, walkability and sensible geography matter more here than lobby prestige.</p>',
            '<div><span>02 · Peaceful</span><h2>You want Nice, but not all of it in your bedroom.</h2></div><p>Villa Victoria finally gives us a central calm card below the palace logic.</p>': '<div><span>02 · Peaceful</span><h2>You want Nice, but not all of it in your bedroom.</h2></div><p>Villa Victoria and Le Grimaldi now create a real calmer upper-mid layer; La Pérouse adds the sea when the budget moves up.</p>',
            '<div><span>03 · Lively</span><h2>You want the city outside the door.</h2></div><p>Old Nice and Masséna remain the strongest choices when evenings matter.</p>': '<div><span>03 · Lively</span><h2>You want the city outside the door.</h2></div><p>Hotel Amour and Aston La Scala stop this category being luxury-only; Hôtel du Couvent and Maison Albar remain the choices where the hotel takes a bigger share of the budget.</p>',
            '<div><span>04 · Chic & experience</span><h2>The hotel is part of the reason.</h2></div><p>Sea, spa, history or serious comfort: here you are paying for the hotel itself too. Better to do it deliberately.</p>': '<div><span>04 · Chic & experience</span><h2>The hotel is part of the reason.</h2></div><p>Beau Rivage and West End let you buy into the seafront logic without jumping straight to palace territory; Boscolo, Anantara, Palais and Negresco then make the upgrade explicit.</p>',
        }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def patch_page(lang: str, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = patch_copy(text, lang)
    if 'hotel-price-compass' not in text:
        marker = '<section class="hotel-style-section"'
        pos = text.find(marker)
        if pos < 0:
            raise RuntimeError(f"Could not locate first hotel section in {path}")
        text = text[:pos] + compass(lang) + text[pos:]
    for section_id, wanted in ORDER[lang].items():
        text = reorder_section(text, section_id, wanted)
    count = len(re.findall(r'<article class="hotel-choice-card"', text))
    if count != 20:
        raise RuntimeError(f"{path.relative_to(ROOT)}: expected 20 hotel cards, found {count}")
    for phrase in (["Hotel 64 Nice", "Hotel Florence Nice", "Hôtel Le Grimaldi by Happyculture", "Hotel Amour Nice", "Hotel Beau Rivage", "Boscolo Nice Hôtel & Spa"] if lang == "fr" else ["Hotel 64 Nice", "Hotel Florence Nice", "Hôtel Le Grimaldi by Happyculture", "Hotel Amour Nice", "Hotel Beau Rivage", "Boscolo Nice Hôtel & Spa"]):
        if phrase not in text:
            raise RuntimeError(f"{path.relative_to(ROOT)}: missing expected Nice hotel {phrase}")
    path.write_text(text, encoding="utf-8")
    print(f"Merchandised {path.relative_to(ROOT)}: 20 hotels, stronger mid/upper-mid ladder")


def main() -> int:
    for lang, path in PAGES.items():
        if not path.is_file():
            raise RuntimeError(f"Missing Nice stay page: {path.relative_to(ROOT)}")
        patch_page(lang, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
