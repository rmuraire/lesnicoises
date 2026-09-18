#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "nice": ("fr/dormir/nice/index.html", "stay/nice/index.html", 20),
    "antibes": ("hotels/antibes/index.html", "en/hotels/antibes/index.html", 11),
    "cannes": ("hotels/cannes/index.html", "en/hotels/cannes/index.html", 13),
    "villefranche": ("hotels/villefranche-sur-mer/index.html", "en/hotels/villefranche-sur-mer/index.html", 4),
    "monaco": ("hotels/monaco/index.html", "en/hotels/monaco/index.html", 7),
    "menton": ("hotels/menton/index.html", "en/hotels/menton/index.html", 9),
    "saint-paul": ("hotels/saint-paul-de-vence/index.html", "en/hotels/saint-paul-de-vence/index.html", 8),
    "beaulieu": ("hotels/beaulieu-sur-mer/index.html", "en/hotels/beaulieu-sur-mer/index.html", 5),
    "mougins": ("hotels/mougins/index.html", "en/hotels/mougins/index.html", 6),
    "saint-tropez": ("hotels/saint-tropez/index.html", "en/hotels/saint-tropez/index.html", 12),
}
SYMBOL = {"low": "€", "mid": "€€", "upper-mid": "€€€", "high": "€€€€"}
VALID = set(SYMBOL)

# Relative editorial positioning only; never live room rates.
AUGMENTED_BANDS = {
    "ac-hotel-by-marriott-ambassadeur-antibes": "upper-mid", "hotel-josse": "mid",
    "hotel-mademoiselle": "mid", "hotel-le-pre-catelan": "mid", "royal-antibes": "upper-mid",
    "canopy-by-hilton-cannes": "upper-mid", "hotel-barriere-le-gray-d-albion": "upper-mid",
    "jw-marriott-cannes": "high", "mondrian-cannes": "high",
    "okko-hotels-cannes-centre-hotel-and-spa-belle-plage": "mid", "hotel-and-spa-belle-plage": "upper-mid",
    "hotel-le-provencal": "mid", "le-versailles": "upper-mid",
    "columbus-hotel-monte-carlo": "upper-mid", "fairmont-monte-carlo": "high",
    "hotel-novotel-monte-carlo": "mid", "hotel-port-palace": "upper-mid",
    "best-western-hotel-mediterranee-menton": "low", "hotel-riva-art-and-spa": "mid",
    "hotel-vacances-bleues-royal-westminster": "mid", "princess-et-richmond": "upper-mid",
    "hotel-le-hameau": "mid", "les-vergers-de-saint-paul": "mid",
    "hotel-marcellin": "low", "hotels-carlton-beaulieu": "upper-mid",
    "hotel-royal-mougins": "upper-mid", "hotel-les-liserons-de-mougins": "low",
    "la-bastide-de-mougins": "upper-mid", "la-lune-de-mougins": "mid",
    "airelles-chateau-de-la-messardiere": "high", "byblos-saint-tropez": "high",
    "hotel-la-tartane-saint-tropez": "high", "hotel-de-paris-saint-tropez": "high",
    "la-bastide-de-saint-tropez": "high",
}
PORTFOLIO_BANDS = {
    "le-saint-paul": "high", "domaine-du-mas-de-pierre": "high", "toile-blanche": "upper-mid",
    "la-grande-bastide": "upper-mid", "hotel-les-messugues": "mid", "les-bastides-saint-paul": "mid",
    "hotel-comte-de-nice-beaulieu": "mid", "ibis-styles-beaulieu": "low", "hotel-frisia": "mid",
    "grand-hotel-cap-ferrat": "high", "hermitage-monte-carlo": "high", "monte-carlo-bay": "high",
    "hotel-victoria-roquebrune": "upper-mid", "ibis-roquebrune": "low",
    "belles-rives": "high", "juana": "high", "hotel-le-sud": "mid", "hotel-de-letoile-antibes": "low",
    "five-seas-cannes": "high", "verlaine": "upper-mid", "provence-cannes": "upper-mid",
    "le-mas-candille": "high", "villa-sophia": "mid", "kube": "high", "villa-marie": "high",
    "sezz": "high", "la-ponche": "high", "les-palmiers-sainte-maxime": "mid",
    "la-romarine": "mid", "la-ferme-daugustin": "upper-mid",
}

def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", value.lower()).strip()

def nice_bands() -> dict[str, str]:
    data = json.loads((ROOT / "data/hotels/nice.json").read_text(encoding="utf-8"))
    out = {}
    for hotel in data.get("hotels", []):
        slug = hotel.get("slug") or hotel.get("id")
        band = hotel.get("priceBand")
        if band == "very-high":
            band = "high"
        if slug and band in VALID:
            out[slug] = band
    return out

def budget_text_to_band(value: str) -> str | None:
    value = norm(html.unescape(re.sub(r"<[^>]+>", " ", value)))
    if any(x in value for x in ("extreme", "tres haut", "very high", "grand luxe", "palace")):
        return "high"
    if any(x in value for x in ("upper-mid", "upper mid", "milieu / haut", "milieu/haut", "haut de gamme", "high-end", "high end")):
        return "upper-mid"
    if value in {"haut", "high"}:
        return "upper-mid"
    if any(x in value for x in ("milieu de gamme", "mid-range", "mid range", "moyen")):
        return "mid"
    if any(x in value for x in ("budget", "accessible", "raisonnable", "reasonable", "mesure", "value")):
        return "low"
    return None

def slug_from_card(card: str) -> str:
    m = re.search(r'data-hotel="([^"]+)"', card)
    if m:
        return m.group(1)
    for href in re.findall(r'href="([^"]+)"', card):
        path = urlsplit(html.unescape(href)).path
        if path.startswith("/hotels/") or path.startswith("/en/hotels/"):
            bits = [bit for bit in path.split("/") if bit]
            if len(bits) >= 3:
                return bits[-1]
    return ""

def detail_band(card: str) -> str | None:
    for href in re.findall(r'href="([^"]+)"', card):
        path = urlsplit(html.unescape(href)).path
        if not (path.startswith("/hotels/") or path.startswith("/en/hotels/")):
            continue
        target = ROOT / path.lstrip("/")
        if path.endswith("/"):
            target /= "index.html"
        if not target.is_file():
            continue
        text = target.read_text(encoding="utf-8")
        m = re.search(r'<span>\s*Budget\s*</span>\s*<(?:b|strong)>(.*?)</(?:b|strong)>', text, flags=re.I | re.S)
        if m:
            band = budget_text_to_band(m.group(1))
            if band:
                return band
    return None

def annotate_card(card: str, band: str, lang: str) -> str:
    if 'data-price-band=' not in card:
        card = card.replace('<article class="hotel-choice-card"', f'<article class="hotel-choice-card" data-price-band="{band}"', 1)
    if 'class="hotel-price-band"' in card:
        return card
    title = "Positionnement prix relatif — le tarif réel varie selon vos dates" if lang == "fr" else "Relative price positioning — the real rate varies by date"
    badge = f'<span class="hotel-price-band" title="{title}">{SYMBOL[band]}</span>'
    m = re.search(r'(<div class="hotel-choice-tags">.*?)(</div>)', card, flags=re.S)
    if m:
        return card[:m.start()] + m.group(1) + badge + m.group(2) + card[m.end():]
    return card.replace("<h3>", badge + "<h3>", 1)

def annotate_page(path: Path, lang: str, expected: int, bands: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    cards = list(re.finditer(r'<article class="hotel-choice-card".*?</article>', text, flags=re.S))
    if len(cards) != expected:
        raise RuntimeError(f"{path.relative_to(ROOT)}: expected {expected} hotel cards, found {len(cards)}")
    unresolved, rebuilt, cursor = [], [], 0
    for match in cards:
        card = match.group(0)
        slug = slug_from_card(card)
        band = bands.get(slug) or detail_band(card)
        if not band:
            m = re.search(r"<h3[^>]*>(.*?)</h3>", card, flags=re.S)
            title = " ".join(re.sub(r"<[^>]+>", " ", m.group(1) if m else slug).split())
            unresolved.append(f"{slug or '?'} ({title})")
            continue
        rebuilt.append(text[cursor:match.start()])
        rebuilt.append(annotate_card(card, band, lang))
        cursor = match.end()
    if unresolved:
        raise RuntimeError(f"{path.relative_to(ROOT)}: undocumented price band for {unresolved}")
    rebuilt.append(text[cursor:])
    path.write_text("".join(rebuilt), encoding="utf-8")
    print(f"Price bands applied to {path.relative_to(ROOT)}: {expected} hotels")

def finder_budget_block(lang: str) -> str:
    if lang == "fr":
        return '''<fieldset><legend>5 · Quel est votre plafond de budget ?</legend><div class="engine-buttons"><button class="is-active" type="button" aria-pressed="true" data-engine-group="budget" data-engine-choice="any">Peu importe</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="low">€ · Budget relatif</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="mid">€€ · Milieu de gamme</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="upper-mid">€€€ · Milieu-haut</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="high">€€€€ · Luxe / palace</button></div><p class="engine-note">Repères relatifs Mametas, jamais des prix live. Le moteur garde les hôtels à ce niveau ou en dessous ; Booking.com donne ensuite le vrai tarif pour vos dates.</p></fieldset>'''
    return '''<fieldset><legend>5 · What is your maximum spend level?</legend><div class="engine-buttons"><button class="is-active" type="button" aria-pressed="true" data-engine-group="budget" data-engine-choice="any">No preference</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="low">€ · Relative budget</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="mid">€€ · Mid-range</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="upper-mid">€€€ · Upper-mid</button><button type="button" aria-pressed="false" data-engine-group="budget" data-engine-choice="high">€€€€ · Luxury / palace</button></div><p class="engine-note">Mametas relative bands, never live prices. The finder keeps hotels at or below that level; Booking.com then gives the real rate for your dates.</p></fieldset>'''

def patch_finder(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("Quatre décisions. Puis seulement les hôtels.", "Cinq décisions. Puis seulement les hôtels.")
    text = text.replace("Four decisions. Then the hotels.", "Five decisions. Then the hotels.")
    if 'data-engine-group="budget"' not in text:
        marker = '<div class="engine-submit-row">'
        if marker not in text:
            raise RuntimeError(f"{path.relative_to(ROOT)}: finder submit marker missing")
        text = text.replace(marker, finder_budget_block(lang) + marker, 1)
    text = re.sub(r'/assets/hotel-engine\.css\?v=\d+', '/assets/hotel-engine.css?v=6', text)
    text = re.sub(r'/assets/hotel-engine\.js\?v=\d+', '/assets/hotel-engine.js?v=4', text)
    path.write_text(text, encoding="utf-8")
    print(f"Budget criterion added to {path.relative_to(ROOT)}")

def main() -> int:
    bands = {}
    bands.update(PORTFOLIO_BANDS)
    bands.update(AUGMENTED_BANDS)
    bands.update(nice_bands())
    for _, (fr, en, count) in PAGES.items():
        annotate_page(ROOT / fr, "fr", count, bands)
        annotate_page(ROOT / en, "en", count, bands)
    patch_finder(ROOT / "hotels/finder/index.html", "fr")
    patch_finder(ROOT / "en/hotels/finder/index.html", "en")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
