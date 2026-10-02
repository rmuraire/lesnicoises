#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas city-card coherence pass.

Uses data/city-system-v1.json as the single source of truth for:
- base vs detour classification,
- canonical destination names,
- "best for" tags,
- home-card descriptions,
- routes and imagery.

The pass is intentionally narrow: it normalizes existing city surfaces without
turning hotel or restaurant cards into the same visual component.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/city-system-v1.json").read_text(encoding="utf-8"))
CITIES = DATA["cities"]
GROUPS = DATA["groups"]

HOME_PAGES = {
    "index.html": "en",
    "fr/index.html": "fr",
}
PLACES_PAGES = {
    "en/riviera-guide/index.html": "en",
    "riviera-guide/index.html": "fr",
}


def _replace_balanced_div(text: str, start: int, replacement: str) -> str:
    token_re = re.compile(r"</?div\b[^>]*>", re.I)
    depth = 0
    end = None
    for m in token_re.finditer(text, start):
        token = m.group(0)
        if token.lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                end = m.end()
                break
        else:
            depth += 1
    if end is None:
        raise RuntimeError("Could not find balanced closing </div>")
    return text[:start] + replacement + text[end:]


def _home_card(key: str, lang: str) -> str:
    city = CITIES[key]
    route = city["route"][lang]
    image = city["image"]
    alt = city["alt"][lang]
    tag = city["tag"][lang]
    name = city["name"][lang]
    summary = city["summary"][lang]
    return (
        f'<a class="base-card mametas-city-card" data-mametas-city="{key}" href="{route}">'
        f'<img src="{image}" alt="{alt}" loading="lazy">'
        '<div class="base-card-content">'
        f'<span class="tag">{tag}</span>'
        f'<h3>{name}</h3>'
        f'<p>{summary}</p>'
        '</div></a>'
    )


def _home_grid(keys: list[str], lang: str, group: str, with_id: bool = False) -> str:
    grid_id = ""
    if with_id:
        grid_id = ' id="places"' if lang == "en" else ' id="lieux"'
    cards = "".join(_home_card(key, lang) for key in keys)
    return f'<div class="base-grid mametas-city-grid" data-city-group="{group}"{grid_id}>{cards}</div>'


def _find_grid_for_route(text: str, route: str, start_at: int = 0):
    """Find the nearest grid <div> that encloses a known destination route.

    Historical homepage generators changed ids/classes several times; route
    identity is more stable than presentation markup.
    """
    route_at = text.find(f'href="{route}"', start_at)
    if route_at < 0:
        route_at = text.find(f"href='{route}'", start_at)
    if route_at < 0:
        return None

    candidates = list(re.finditer(
        r'<div\b[^>]*class=["\'][^"\']*grid[^"\']*["\'][^>]*>',
        text[:route_at],
        re.I,
    ))
    for m in reversed(candidates):
        try:
            end_text = _replace_balanced_div(text, m.start(), "__MAMETAS_GRID_SENTINEL__")
        except RuntimeError:
            continue
        sentinel_at = end_text.find("__MAMETAS_GRID_SENTINEL__")
        if sentinel_at < 0:
            continue
        # Recover the original balanced end by comparing suffixes.
        suffix = end_text[sentinel_at + len("__MAMETAS_GRID_SENTINEL__"):]
        end = len(text) - len(suffix)
        if m.start() <= route_at < end:
            return m.start(), end
    return None


def _replace_home_base_grid(text: str, lang: str) -> str:
    route = CITIES["nice"]["route"][lang]
    found = _find_grid_for_route(text, route)
    if not found:
        raise RuntimeError(f"Home {lang}: base city grid not found")
    start, _end = found
    return _replace_balanced_div(
        text,
        start,
        _home_grid(GROUPS["base"], lang, "base", with_id=True),
    )


def _detour_section(lang: str) -> str:
    if lang == "fr":
        eyebrow = "AU-DELÀ DE VOTRE BASE"
        title = "Ne collectionnez pas la Riviera. Choisissez-la."
        intro = (
            "Une fois votre base réglée, gardez les détours qui changent vraiment "
            "l’ambiance du voyage, pas ceux qui ajoutent seulement une épingle."
        )
    else:
        eyebrow = "BEYOND YOUR BASE"
        title = "Do not collect the Riviera. Choose it."
        intro = (
            "Once your base is sorted, keep the detours that genuinely change the "
            "trip, not the ones that merely add another pin."
        )
    return (
        '<section class="v3-section mametas-detour-section"><div class="wrap">'
        '<div class="section-heading"><div>'
        f'<p class="eyebrow">{eyebrow}</p><h2>{title}</h2>'
        f'</div><p>{intro}</p></div>'
        + _home_grid(GROUPS["detour"], lang, "detour", with_id=False)
        + '</div></section>'
    )


def _replace_home_detour_grid(text: str, lang: str) -> str:
    # Saint-Tropez is never in the base group, making it the safest stable
    # route marker for the detour grid.
    route = CITIES["sainttropez"]["route"][lang]
    found = _find_grid_for_route(text, route)
    if found:
        start, _end = found
        return _replace_balanced_div(
            text,
            start,
            _home_grid(GROUPS["detour"], lang, "detour", with_id=False),
        )

    # Some historical FR homepage generations omitted the whole detour section.
    # Recreate it from canonical city data rather than failing or reintroducing
    # a one-off translation patch.
    section = _detour_section(lang)
    target_id = "explorer" if lang == "fr" else "explore"
    marker = re.search(
        rf'<section\b[^>]*\bid=["\']{target_id}["\'][^>]*>',
        text,
        re.I,
    )
    if marker:
        return text[:marker.start()] + section + "\n" + text[marker.start():]

    main_close = text.lower().rfind("</main>")
    if main_close >= 0:
        return text[:main_close] + section + "\n" + text[main_close:]

    raise RuntimeError(f"Home {lang}: no safe insertion point for canonical detours")


def patch_home(path: Path, lang: str) -> bool:
    text = path.read_text(encoding="utf-8")
    before = text
    text = _replace_home_base_grid(text, lang)
    text = _replace_home_detour_grid(text, lang)
    if text != before:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def _find_city_anchor(text: str, route: str):
    pattern = re.compile(
        rf'<a\b[^>]*href=["\']{re.escape(route)}["\'][^>]*>[\s\S]*?</a>',
        re.I,
    )
    for m in pattern.finditer(text):
        if re.search(r'<h3\b', m.group(0), re.I):
            return m
    # Attribute order / formatting fallback.
    pattern = re.compile(r'<a\b[^>]*>[\s\S]*?</a>', re.I)
    for m in pattern.finditer(text):
        block = m.group(0)
        if re.search(rf'href=["\']{re.escape(route)}["\']', block, re.I) and re.search(r'<h3\b', block, re.I):
            return m
    return None


def _normalize_places_card(block: str, key: str, lang: str) -> str:
    city = CITIES[key]
    block = _ensure_data_key(block, key)
    block = re.sub(
        r'<h3>.*?</h3>',
        f'<h3>{city["name"][lang]}</h3>',
        block,
        count=1,
        flags=re.S | re.I,
    )
    tag = city["tag"][lang]

    if re.search(r'<span class=["\'][^"\']*tiny[^"\']*["\']>.*?</span>', block, re.S | re.I):
        block = re.sub(
            r'<span class=["\'][^"\']*tiny[^"\']*["\']>.*?</span>',
            f'<span class="tiny">{tag}</span>',
            block,
            count=1,
            flags=re.S | re.I,
        )
    elif re.search(r'<p[^>]*>\s*<strong>.*?</strong>', block, re.S | re.I):
        block = re.sub(
            r'(<p[^>]*>\s*)<strong>.*?</strong>',
            rf'\1<strong>{tag}.</strong>',
            block,
            count=1,
            flags=re.S | re.I,
        )
    elif re.search(r'<h3\b', block, re.I):
        block = re.sub(
            r'(<h3\b)',
            f'<span class="mametas-city-tag">{tag}</span>\1',
            block,
            count=1,
            flags=re.I,
        )
    return block


def patch_places(path: Path, lang: str) -> bool:
    text = path.read_text(encoding="utf-8")
    before = text
    for key in GROUPS["base"] + GROUPS["detour"]:
        route = CITIES[key]["route"][lang]
        m = _find_city_anchor(text, route)
        if not m:
            raise RuntimeError(f"{path}: city card not found for {key} ({route})")
        block = _normalize_places_card(m.group(0), key, lang)
        text = text[:m.start()] + block + text[m.end():]
    if text != before:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def validate_home(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count('data-city-group="base"') != 1:
        raise RuntimeError(f"{path}: base group missing or duplicated")
    if text.count('data-city-group="detour"') != 1:
        raise RuntimeError(f"{path}: detour group missing or duplicated")
    for key in GROUPS["base"] + GROUPS["detour"]:
        if text.count(f'data-mametas-city="{key}"') != 1:
            raise RuntimeError(f"{path}: city {key} missing or duplicated")
        tag = CITIES[key]["tag"][lang]
        if tag not in text:
            raise RuntimeError(f"{path}: canonical tag missing for {key}: {tag}")
    # Classification regression guards from the coherence audit.
    base_start = text.index('data-city-group="base"')
    detour_start = text.index('data-city-group="detour"')
    if base_start > detour_start:
        raise RuntimeError(f"{path}: base group must precede detours")
    segment_base = text[base_start:detour_start]
    for key in ("monaco", "menton"):
        if f'data-mametas-city="{key}"' not in segment_base:
            raise RuntimeError(f"{path}: {key} must be a base")
    segment_detour = text[detour_start:]
    if 'data-mametas-city="eze"' not in segment_detour:
        raise RuntimeError(f"{path}: Èze must be a detour")


def validate_places(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    for key in GROUPS["base"] + GROUPS["detour"]:
        if text.count(f'data-mametas-city="{key}"') != 1:
            raise RuntimeError(f"{path}: city marker missing or duplicated for {key}")
        tag = CITIES[key]["tag"][lang]
        if tag not in text:
            raise RuntimeError(f"{path}: canonical tag missing for {key}: {tag}")


def main() -> None:
    changed = []
    for rel, lang in HOME_PAGES.items():
        path = ROOT / rel
        if patch_home(path, lang):
            changed.append(rel)
        validate_home(path, lang)

    for rel, lang in PLACES_PAGES.items():
        path = ROOT / rel
        if patch_places(path, lang):
            changed.append(rel)
        validate_places(path, lang)

    print(f"City-card coherence passed; changed {len(changed)} pages.")
    for rel in changed:
        print("  ", rel)


if __name__ == "__main__":
    main()
