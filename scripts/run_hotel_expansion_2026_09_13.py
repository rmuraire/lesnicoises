#!/usr/bin/env python3
from __future__ import annotations

import re

import augment_hotels_2026_09_13 as hotels

_original_update_page_copy = hotels.update_page_copy


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


hotels.update_page_copy = update_page_copy

if __name__ == "__main__":
    raise SystemExit(hotels.main())
