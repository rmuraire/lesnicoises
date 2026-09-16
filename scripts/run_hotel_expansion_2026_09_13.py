#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter

import augment_hotels_2026_09_13 as hotels

_original_update_page_copy = hotels.update_page_copy
HOTEL_CSS = '/assets/hotel-batch.css?v=2.0'


def update_page_copy(text: str, base: str, lang: str) -> str:
    text = _original_update_page_copy(text, base, lang)
    if lang == "en":
        count = hotels.BASES[base]["count"]
        text = re.sub(r"\b\d+ hotels selected\b", f"{count} selected hotels", text)
    return text


def ensure_hotel_css_on_nice_pages() -> None:
    for rel in ("fr/dormir/nice/index.html", "stay/nice/index.html"):
        path = hotels.ROOT / rel
        text = path.read_text(encoding="utf-8")
        if '/assets/hotel-batch.css' in text:
            text = re.sub(r'/assets/hotel-batch\.css\?v=[^"\']+', HOTEL_CSS, text)
        else:
            text = text.replace('</head>', f'<link href="{HOTEL_CSS}" rel="stylesheet"></head>', 1)
        path.write_text(text, encoding="utf-8")
        print(f"Ensured hotel sprite CSS on {rel}")


def validate_without_static_nice() -> None:
    slugs = [h["slug"] for h in hotels.HOTELS]
    urls = [h["url"] for h in hotels.HOTELS]
    if len(set(slugs)) != 44 or len(set(urls)) != 44:
        raise RuntimeError("Hotel batch identifiers or Expedia links are not unique")
    css = (hotels.ROOT / "assets" / "hotel-batch.css").read_text(encoding="utf-8")
    if "/assets/hotels/batch-sprite-2026-09-13.jpg" not in css:
        raise RuntimeError("New batch cards exist but CSS sprite rule is missing")
    all_text = ""
    for cfg in hotels.BASES.values():
        for lang in ("fr", "en"):
            path = hotels.ROOT / cfg[lang]
            text = path.read_text(encoding="utf-8")
            all_text += text
            expected = cfg["count"]
            needle = f"{expected} hôtels sélectionnés" if lang == "fr" else f"{expected} selected hotels"
            if needle not in text:
                raise RuntimeError(f"{path.relative_to(hotels.ROOT)}: expected count marker {needle!r}")
    counts = Counter(re.findall(r'data-hotel="([^"]+)"', all_text))
    nice_slugs = {h["slug"] for h in hotels.HOTELS if h["base"] == "nice"}
    bad = {slug: counts[slug] for slug in slugs if slug not in nice_slugs and counts[slug] != 2}
    if bad:
        raise RuntimeError(f"Each non-Nice hotel must appear once in FR and EN; bad counts: {bad}")
    data = json.loads((hotels.ROOT / "data/hotels/nice.json").read_text(encoding="utf-8"))
    ids = {h["id"] for h in data["hotels"]}
    missing = sorted(nice_slugs - ids)
    if missing or len(data["hotels"]) != 20:
        raise RuntimeError(f"Nice engine inventory invalid; missing={missing}, count={len(data['hotels'])}")
    print("Validated hotel batch; Nice hotels are represented in the 20-hotel engine dataset")


hotels.update_page_copy = update_page_copy

if __name__ == "__main__":
    original_bases = hotels.BASES
    original_validate = hotels.validate
    hotels.BASES = {k: v for k, v in original_bases.items() if k != "nice"}
    hotels.validate = validate_without_static_nice
    try:
        status = hotels.main()
    finally:
        hotels.BASES = original_bases
        hotels.validate = original_validate
    ensure_hotel_css_on_nice_pages()
    raise SystemExit(status)
