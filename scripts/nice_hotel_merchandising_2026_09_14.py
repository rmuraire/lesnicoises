#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {"fr": ROOT / "fr/dormir/nice/index.html", "en": ROOT / "stay/nice/index.html"}

ORDER = {
    "fr": {
        "pratique": ["hotel-66","hotel-64-nice","hotel-florence-nice","boutique-hotel-nice-cote-dazur","hotel-byakko-nice","apollinaire-nice","hotel-khla-nice"],
        "calme": ["villa-victoria","hotel-le-grimaldi-by-happyculture","la-perouse"],
        "vivant": ["hotel-amour-nice","hotel-aston-la-scala","hotel-du-couvent","maison-albar-le-victoria"],
        "chic": ["hotel-beau-rivage","hotel-west-end-nice-promenade","boscolo-nice-hotel-and-spa","palais-de-la-mediterranee","anantara-plaza-nice","le-negresco"],
    },
    "en": {
        "practical": ["hotel-66","hotel-64-nice","hotel-florence-nice","boutique-hotel-nice-cote-dazur","hotel-byakko-nice","apollinaire-nice","hotel-khla-nice"],
        "quiet": ["villa-victoria","hotel-le-grimaldi-by-happyculture","la-perouse"],
        "active": ["hotel-amour-nice","hotel-aston-la-scala","hotel-du-couvent","maison-albar-le-victoria"],
        "chic": ["hotel-beau-rivage","hotel-west-end-nice-promenade","boscolo-nice-hotel-and-spa","palais-de-la-mediterranee","anantara-plaza-nice","le-negresco"],
    },
}


def card_key(card: str) -> str:
    m = re.search(r'data-hotel="([^"]+)"', card)
    if m:
        return m.group(1)
    m = re.search(r'href="/(?:en/)?hotels/nice/([^/]+)/"', card)
    return m.group(1) if m else ""


def reorder_section(text: str, section_id: str, wanted: list[str]) -> str:
    pos = text.find(f'id="{section_id}"')
    if pos < 0:
        raise RuntimeError(f"Missing Nice hotel section: {section_id}")
    section_end = text.find("</section>", pos)
    grid_start = text.find('<div class="hotel-choice-grid">', pos, section_end)
    if section_end < 0 or grid_start < 0:
        raise RuntimeError(f"Malformed Nice hotel section: {section_id}")
    cards = re.findall(r'<article class="hotel-choice-card".*?</article>', text[grid_start:section_end], flags=re.S)
    by_key = {card_key(card): card for card in cards}
    missing = [key for key in wanted if key not in by_key]
    if missing:
        raise RuntimeError(f"Section {section_id}: expected hotel cards missing: {missing}")
    extras = [card_key(card) for card in cards if card_key(card) not in wanted]
    if extras or len(cards) != len(wanted):
        raise RuntimeError(f"Section {section_id}: unexpected hotel cards: {extras}")
    first = text.find(cards[0], grid_start, section_end)
    last = text.find(cards[-1], first, section_end) + len(cards[-1])
    return text[:first] + "".join(by_key[key] for key in wanted) + text[last:]


def compass(lang: str) -> str:
    if lang == "fr":
        return '<section class="v3-section hotel-chooser hotel-price-compass" id="niveau-budget"><div class="wrap"><div class="chooser-intro"><div><p class="eyebrow">Le bon niveau de dépense</p><h2>Le milieu de gamme n’est plus un trou dans la raquette.</h2></div><p>Les prix bougent selon les dates, donc pas de faux seuils. Choisissez plutôt entre dépense intelligente, milieu-haut avec du caractère et hôtel-expérience.</p></div><nav class="style-nav"><a href="#pratique"><span>€€</span><strong>Dépense intelligente</strong><small>Hotel 64 · Florence · Hotel 66 · Byakko</small></a><a href="#calme"><span>€€€</span><strong>Le bon milieu-haut</strong><small>Villa Victoria · Le Grimaldi · Hotel Amour · Beau Rivage</small></a><a href="#chic"><span>€€€€</span><strong>Monter en gamme exprès</strong><small>La Pérouse · Boscolo · Couvent · Negresco · Anantara</small></a></nav><p class="article-meta"><span>Repères relatifs, pas tarifs fixes</span><span>Les prix varient fortement selon les dates</span></p></div></section>'
    return '<section class="v3-section hotel-chooser hotel-price-compass" id="budget-level"><div class="wrap"><div class="chooser-intro"><div><p class="eyebrow">Choose the spend level</p><h2>The missing middle is no longer missing.</h2></div><p>Rates move too much by date for fake price bands. Choose instead between smart spend, upper-mid with character and a hotel that is deliberately part of the experience.</p></div><nav class="style-nav"><a href="#practical"><span>€€</span><strong>Smart spend</strong><small>Hotel 64 · Florence · Hotel 66 · Byakko</small></a><a href="#quiet"><span>€€€</span><strong>Upper-mid sweet spot</strong><small>Villa Victoria · Le Grimaldi · Hotel Amour · Beau Rivage</small></a><a href="#chic"><span>€€€€</span><strong>Splurge deliberately</strong><small>La Pérouse · Boscolo · Couvent · Negresco · Anantara</small></a></nav><p class="article-meta"><span>Relative positioning, not fixed rates</span><span>Prices swing heavily by date</span></p></div></section>'


def patch_page(lang: str, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    desc = ("20 hôtels sélectionnés à Nice, du bon milieu de gamme au luxe, classés par usage : sans voiture, vivant, calme ou hôtel-expérience." if lang == "fr" else "20 selected Nice hotels from smart mid-range to luxury, organised by use: car-free, lively, quiet or hotel-as-experience.")
    deck = ("Vingt hôtels, quatre styles de séjour, du choix rationnel au vrai luxe. Commencez par le rôle que doit jouer l’hôtel, puis décidez combien vous voulez y mettre." if lang == "fr" else "Twenty hotels, four trip styles, from rational mid-range choices to real luxury. Decide what the hotel needs to do first, then decide how much you want to spend.")
    text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', text, count=1)
    text = re.sub(r'<p class="article-deck">.*?</p>', f'<p class="article-deck">{deck}</p>', text, count=1, flags=re.S)
    text = re.sub(r'<span>(?:\d{1,2} (?:septembre|September) 2026)</span>', '<span>15 septembre 2026</span>' if lang == 'fr' else '<span>15 September 2026</span>', text, count=1)
    if 'hotel-price-compass' not in text:
        pos = text.find('<section class="hotel-style-section"')
        if pos < 0:
            raise RuntimeError(f"Could not locate first hotel section in {path}")
        text = text[:pos] + compass(lang) + text[pos:]
    for section_id, wanted in ORDER[lang].items():
        text = reorder_section(text, section_id, wanted)
    count = len(re.findall(r'<article class="hotel-choice-card"', text))
    if count != 20:
        raise RuntimeError(f"{path.relative_to(ROOT)}: expected 20 hotel cards, found {count}")
    required = ["Hotel 64 Nice","Hotel Florence Nice","Hôtel Le Grimaldi by Happyculture","Hotel Amour Nice","Hotel Beau Rivage","Boscolo Nice Hôtel & Spa"]
    missing = [name for name in required if name not in text]
    if missing:
        raise RuntimeError(f"{path.relative_to(ROOT)}: missing expected hotels {missing}")
    path.write_text(text, encoding="utf-8")
    print(f"Merchandised {path.relative_to(ROOT)}: 20 hotels")


def main() -> int:
    for lang, path in PAGES.items():
        if not path.is_file():
            raise RuntimeError(f"Missing Nice stay page: {path.relative_to(ROOT)}")
        patch_page(lang, path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
