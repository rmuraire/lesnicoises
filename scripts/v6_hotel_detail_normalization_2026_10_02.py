#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas coherence audit — hotel detail normalization.

Runs late in the build, after generated Hotel Take pages exist. It does not
invent hotel facts. It only normalizes the shared envelope of hotel detail
pages: parent link, eyebrow, affiliate CTA wording and language cleanliness.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]

CITY_NAMES = {
    "nice": "Nice",
    "cannes": "Cannes",
    "antibes": "Antibes",
    "menton": "Menton",
    "monaco": "Monaco",
    "eze": "Èze",
    "beaulieu-sur-mer": "Beaulieu-sur-Mer",
    "villefranche-sur-mer": "Villefranche-sur-Mer",
    "saint-jean-cap-ferrat": "Saint-Jean-Cap-Ferrat",
    "saint-tropez": "Saint-Tropez",
}

KNOWN_CITY_LISTS_EN = {
    "nice": "/stay/nice/",
    "cannes": "/en/hotels/cannes/",
    "antibes": "/en/hotels/antibes/",
}
KNOWN_CITY_LISTS_FR = {
    "nice": "/fr/dormir/nice/",
    "cannes": "/hotels/cannes/",
    "antibes": "/hotels/antibes/",
}

def page_lang(text: str) -> str:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', text, re.I)
    return "fr" if m and m.group(1).lower().startswith("fr") else "en"

def hotel_route_parts(path: Path):
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 5 and parts[0] == "en" and parts[1] == "hotels" and parts[-1] == "index.html":
        return "en", parts[2], parts[3]
    if len(parts) >= 4 and parts[0] == "hotels" and parts[-1] == "index.html":
        return "fr", parts[1], parts[2]
    return None

def looks_like_detail(text: str) -> bool:
    signals = (
        'class="hotel-detail"',
        "MAMETAS HOTEL TAKE",
        "THE MAMETAS VERDICT",
        "LE VERDICT MAMETAS",
        "Check rates",
        "Voir les tarifs",
        "Check dates",
    )
    return "<h1" in text.lower() and any(s.lower() in text.lower() for s in signals)

def normalize_affiliate_ctas(text: str, lang: str) -> str:
    def repl(m):
        tag, inner = m.group(1), m.group(2)
        low = tag.lower()
        if "sponsored" not in low:
            return m.group(0)
        href_m = re.search(r'href=["\']([^"\']+)', tag, re.I)
        href = html.unescape(href_m.group(1)) if href_m else ""
        provider = None
        h = href.lower()
        if "booking.com" in h or "kqzyfj.com" in h:
            provider = "Booking.com"
        elif "expedia" in h:
            provider = "Expedia"
        if not provider:
            return m.group(0)
        label = (
            f"Voir les tarifs sur {provider}"
            if lang == "fr"
            else f"Check rates on {provider}"
        )
        return f"<a{tag}>{label}</a>"
    return re.sub(r'<a([^>]+)>(.*?)</a>', repl, text, flags=re.S | re.I)

def normalize_top(text: str, lang: str, city_slug: str) -> str:
    city = CITY_NAMES.get(city_slug, city_slug.replace("-", " ").title())
    if lang == "fr":
        parent = KNOWN_CITY_LISTS_FR.get(city_slug, "/hotels/")
        back = f"← Retour aux hôtels de {city}" if city_slug in KNOWN_CITY_LISTS_FR else "← Retour aux hôtels"
        eyebrow = f"HÔTEL · {city}"
    else:
        parent = KNOWN_CITY_LISTS_EN.get(city_slug, "/en/hotels/")
        back = f"← Back to {city} hotels" if city_slug in KNOWN_CITY_LISTS_EN else "← Back to hotels"
        eyebrow = f"HOTEL · {city}"

    text = re.sub(
        r'<a class="back"[^>]*>.*?</a>',
        f'<a class="mametas-detail-back" href="{parent}">{back}</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<p class="breadcrumbs">.*?</p>',
        f'<a class="mametas-detail-back" href="{parent}">{back}</a>',
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
    text = re.sub(
        r'<p class="eyebrow">.*?</p>',
        f'<p class="eyebrow mametas-detail-eyebrow">{eyebrow}</p>',
        text,
        count=1,
        flags=re.S | re.I,
    )

    # Hotel Take pages sometimes have neither back link nor a standard eyebrow.
    main = re.search(r'<main\b[^>]*>', text, re.I)
    h1 = re.search(r'<h1\b', text, re.I)
    if main and h1 and h1.start() > main.end():
        segment = text[main.end():h1.start()]
        additions = []
        if "mametas-detail-back" not in segment:
            additions.append(f'<a class="mametas-detail-back" href="{parent}">{back}</a>')
        if "mametas-detail-eyebrow" not in segment:
            additions.append(f'<p class="mametas-detail-eyebrow">{eyebrow}</p>')
        if additions:
            text = text[:h1.start()] + "".join(additions) + text[h1.start():]

    # Remove the English-only Hotel Take eyebrow that leaked into FR pages.
    if lang == "fr":
        text = text.replace("MAMETAS HOTEL TAKE ·", "HÔTEL ·")
    return text

def validate(path: Path, text: str, lang: str) -> None:
    name = path.relative_to(ROOT).as_posix()
    if "mametas-detail-back" not in text:
        raise RuntimeError(f"{name}: normalized hotel back link missing")
    if "mametas-detail-eyebrow" not in text:
        raise RuntimeError(f"{name}: normalized hotel eyebrow missing")
    if lang == "fr" and "MAMETAS HOTEL TAKE" in text:
        raise RuntimeError(f"{name}: English Hotel Take eyebrow remains on FR page")
    for m in re.finditer(r'<a([^>]+)>(.*?)</a>', text, re.S | re.I):
        tag = m.group(1).lower()
        if "sponsored" not in tag:
            continue
        href_m = re.search(r'href=["\']([^"\']+)', m.group(1), re.I)
        href = html.unescape(href_m.group(1)) if href_m else ""
        visible = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if "booking.com" in href.lower() or "kqzyfj.com" in href.lower():
            expected = "Voir les tarifs sur Booking.com" if lang == "fr" else "Check rates on Booking.com"
            if visible != expected:
                raise RuntimeError(f"{name}: Booking CTA is not canonical: {visible!r}")
        if "expedia" in href.lower():
            expected = "Voir les tarifs sur Expedia" if lang == "fr" else "Check rates on Expedia"
            if visible != expected:
                raise RuntimeError(f"{name}: Expedia CTA is not canonical: {visible!r}")

def main():
    changed = []
    checked = 0
    for path in sorted(ROOT.rglob("index.html")):
        info = hotel_route_parts(path)
        if not info:
            continue
        route_lang, city_slug, _hotel_slug = info
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not looks_like_detail(text):
            continue
        lang = page_lang(text)
        before = text
        text = normalize_top(text, lang, city_slug)
        text = normalize_affiliate_ctas(text, lang)
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
        validate(path, text, lang)
        checked += 1

    if checked < 10:
        raise RuntimeError(f"Only {checked} hotel detail pages found; expected the materialized hotel catalogue")
    print(f"Hotel detail coherence passed on {checked} pages; changed {len(changed)}.")
    for rel in changed[:80]:
        print("  ", rel)

if __name__ == "__main__":
    main()
