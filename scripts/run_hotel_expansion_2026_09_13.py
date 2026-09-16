#!/usr/bin/env python3
from __future__ import annotations

import re

import augment_hotels_2026_09_13 as hotels

_original_update_page_copy = hotels.update_page_copy
HOTEL_CSS = '/assets/hotel-batch.css?v=2.0'


def update_page_copy(text: str, base: str, lang: str) -> str:
    text = _original_update_page_copy(text, base, lang)
    if lang == "en":
        count = hotels.BASES[base]["count"]
        text = re.sub(r"\b\d+ hotels selected\b", f"{count} selected hotels", text)
    if base == "nice" and lang == "fr":
        text = text.replace("Dix hôtels sélectionnés à Nice", "Vingt hôtels sélectionnés à Nice")
    if base == "nice" and lang == "en":
        text = text.replace("Ten selected Nice hotels", "Twenty selected Nice hotels")
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


hotels.update_page_copy = update_page_copy

if __name__ == "__main__":
    # Nice now has a data-driven decision engine fed by data/hotels/nice.json.
    # The legacy expansion pass expects static hotel grids there, so protect the
    # new chooser while continuing to materialize all other destination hubs.
    original_bases = hotels.BASES
    hotels.BASES = {k: v for k, v in original_bases.items() if k != "nice"}
    try:
        status = hotels.main()
    finally:
        hotels.BASES = original_bases
    ensure_hotel_css_on_nice_pages()
    raise SystemExit(status)
