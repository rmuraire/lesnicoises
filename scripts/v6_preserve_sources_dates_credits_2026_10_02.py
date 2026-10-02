#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Preserve and normalize source dates + visible photo credits before shell replacement.

This runs before the global shell because several legacy footers contain the only
visible "checked" date on a page. It never invents a date or photo author.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_TOP = {".git", ".github", "docs", "scripts", "data", "backup"}

EN_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
FR_MONTHS = "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"

KNOWN_HERO_CREDITS = {
    "/assets/editorial/monaco-casino-chloe-laurens.jpg": {
        "en": "Photo: Chloé Laurens",
        "fr": "Photo : Chloé Laurens",
    },
    "/assets/editorial/cannes-beach-sophie-kat.jpg": {
        "en": "Photo: Sophie Kat",
        "fr": "Photo : Sophie Kat",
    },
}

# Depositphotos credits are supplied explicitly in the repository metadata.
DEPOSITPHOTO_CREDITS = {}
deposit_meta = ROOT / "data/depositphotos-nice-pratique.json"
if deposit_meta.exists():
    raw = json.loads(deposit_meta.read_text(encoding="utf-8"))
    for item in raw.get("assets", []):
        if item.get("status") != "use" or not item.get("file") or not item.get("credit"):
            continue
        src = "/assets/editorial/depositphotos/nice-pratique/" + item["file"]
        credit = item["credit"]
        DEPOSITPHOTO_CREDITS[src] = {
            "en": f"Photo: {credit}, Depositphotos",
            "fr": f"Photo : {credit}, Depositphotos",
        }

def page_lang(text: str) -> str:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', text, re.I)
    return "fr" if m and m.group(1).lower().startswith("fr") else "en"

def find_checked_date(text: str, lang: str):
    patterns = []
    if lang == "en":
        patterns += [
            rf'\b(\d{{1,2}}\s+(?:{EN_MONTHS})\s+20\d{{2}})\b',
            rf'\b((?:{EN_MONTHS})\s+20\d{{2}})\b',
        ]
    else:
        patterns += [
            rf'\b(\d{{1,2}}\s+(?:{FR_MONTHS})\s+20\d{{2}})\b',
            rf'\b((?:{FR_MONTHS})\s+20\d{{2}})\b',
        ]

    # Prefer the Mametas Checked badge, then article metadata, then footer.
    zones = []
    badge = re.search(r'<a[^>]*class=["\'][^"\']*mametas-checked[^"\']*["\'][^>]*>[\s\S]*?</a>', text, re.I)
    if badge:
        zones.append(badge.group(0))
    meta = re.search(r'<div[^>]*class=["\'][^"\']*article-meta[^"\']*["\'][^>]*>[\s\S]*?</div>', text, re.I)
    if meta:
        zones.append(meta.group(0))
    footer = re.search(r'<footer\b[^>]*>[\s\S]*?</footer>', text, re.I)
    if footer:
        zones.append(footer.group(0))
    zones.append(text[:12000])

    for zone in zones:
        plain = re.sub(r'<[^>]+>', ' ', zone)
        for pattern in patterns:
            m = re.search(pattern, plain, re.I)
            if m:
                return m.group(1)
    return None

def source_heading(lang: str) -> str:
    return "Sources vérifiées" if lang == "fr" else "Sources checked"

def date_label(date: str, lang: str) -> str:
    if lang == "en":
        return f"Checked {date}"
    if re.match(r'^\d{1,2}\s', date):
        return f"Vérifié le {date}"
    return f"Vérifié en {date}"

def normalize_sources(text: str, lang: str) -> str:
    heading = source_heading(lang)

    def repl(m):
        opening, inner, closing = m.group(1), m.group(2), m.group(3)

        # Any historical heading inside a formal sources container becomes the
        # one canonical H2. Dates are kept separately by add_source_date().
        heading_match = re.search(
            r'<h[2-4]\\b[^>]*>[\\s\\S]*?</h[2-4]>',
            inner,
            re.I,
        )
        if heading_match:
            old = heading_match.group(0)
            plain_old = re.sub(r'<[^>]+>', ' ', old)
            if re.search(r'source|sources', plain_old, re.I):
                inner = inner[:heading_match.start()] + f'<h2>{heading}</h2>' + inner[heading_match.end():]
            elif not re.search(rf'<h2>{re.escape(heading)}</h2>', inner, re.I):
                inner = f'<h2>{heading}</h2>' + inner
        else:
            strong = re.search(r'<strong>[^<]*(?:source|sources)[^<]*</strong>', inner, re.I)
            if strong:
                inner = inner[:strong.start()] + f'<h2>{heading}</h2>' + inner[strong.end():]
            else:
                inner = f'<h2>{heading}</h2>' + inner

        return opening + inner + closing

    return re.sub(
        r'(<div\\b[^>]*class=["\\'][^"\\']*sources[^"\\']*["\\'][^>]*>)([\\s\\S]*?)(</div>)',
        repl,
        text,
        flags=re.I,
    )

def add_source_date(text: str, lang: str, date: str | None) -> str:
    if not date or "mametas-source-date" in text:
        return text
    m = re.search(r'<div\b[^>]*class=["\'][^"\']*sources[^"\']*["\'][^>]*>', text, re.I)
    if not m:
        return text
    label = date_label(date, lang)
    insert = f'<p class="mametas-source-date">{label}</p>'
    return text[:m.end()] + insert + text[m.end():]

def normalize_existing_figcaptions(text: str, lang: str) -> str:
    prefix = "Photo : " if lang == "fr" else "Photo: "

    def repl(m):
        inner = m.group(1).strip()
        if not inner:
            return m.group(0)
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        # Keep captions that are genuinely descriptive rather than credits.
        creditish = (
            plain.lower().startswith("photo:"),
            plain.lower().startswith("photo :"),
            "wikimedia" in plain.lower(),
            "depositphotos" in plain.lower(),
            "pexels" in plain.lower(),
            "creator program" in plain.lower(),
            "property photo" in plain.lower(),
            "côte d’azur france" in plain.lower(),
            "cote d'azur france" in plain.lower(),
        )
        if not any(creditish):
            return m.group(0)
        inner = re.sub(r'^\s*Photo\s*:\s*', '', inner, flags=re.I)
        inner = re.sub(r'^\s*Property (?:photo|image)(?:\s+via)?\s+', '', inner, flags=re.I)
        inner = re.sub(r'^\s*via\s+', '', inner, flags=re.I)
        return f"<figcaption>{prefix}{inner}</figcaption>"

    return re.sub(r'<figcaption>([\s\S]*?)</figcaption>', repl, text, flags=re.I)

def add_known_hero_credit(text: str, lang: str) -> str:
    credits = dict(KNOWN_HERO_CREDITS)
    credits.update(DEPOSITPHOTO_CREDITS)

    # The repository explicitly materializes this directory as Renaud's own
    # Nice photo bundle.
    for m in re.finditer(r'<img\b[^>]*src=["\'](/assets/editorial/renaud/nice/[^"\']+)["\'][^>]*>', text, re.I):
        src = m.group(1)
        credits[src] = {
            "en": "Photo: Renaud Muraire",
            "fr": "Photo : Renaud Muraire",
        }

    for src, labels in credits.items():
        if src not in text:
            continue
        # Inspect complete figure blocks and modify only the one that actually
        # contains the credited image. Never let a regex cross figure bounds.
        for m in list(re.finditer(r'<figure\b[^>]*>[\s\S]*?</figure>', text, re.I)):
            figure = m.group(0)
            if src not in figure or "<figcaption" in figure.lower():
                continue
            replacement = figure.replace(
                "</figure>",
                f"<figcaption>{labels[lang]}</figcaption></figure>",
            )
            text = text[:m.start()] + replacement + text[m.end():]
            break
    return text

def main() -> None:
    changed = []
    source_pages = 0
    dated = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "<main" not in text.lower():
            continue
        before = text
        lang = page_lang(text)
        date = find_checked_date(text, lang)
        text = normalize_sources(text, lang)
        if re.search(r'class=["\'][^"\']*sources[^"\']*["\']', text, re.I):
            source_pages += 1
            if date:
                dated += 1
                text = add_source_date(text, lang, date)
        text = normalize_existing_figcaptions(text, lang)
        text = add_known_hero_credit(text, lang)
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel.as_posix())

    print(f"Source/date/photo-credit preservation passed; changed {len(changed)} pages; {dated}/{source_pages} source blocks received a known checked date.")


if __name__ == "__main__":
    main()
