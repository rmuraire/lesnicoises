#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Late family-level normalization for Restaurants, Beaches, Culture and Good Finds.

The goal is structural coherence, not editorial rewriting. Existing facts and
recommendations stay intact.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PRACTICAL_GOOD_FINDS_EN = {
    "nice-airport-transfer", "train-or-bus", "what-to-book", "nice-in-the-rain"
}
PRACTICAL_GOOD_FINDS_FR = {
    "transfert-aeroport-nice", "train-ou-bus", "que-reserver", "nice-quand-il-pleut"
}

def page_lang(text: str) -> str:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', text, re.I)
    return "fr" if m and m.group(1).lower().startswith("fr") else "en"

def text_subject(text: str, fallback: str) -> str:
    for pattern in (
        r'<div class="meta[^"]*">([^<]+)</div>',
        r'<p class="eyebrow[^"]*">([^<]+)</p>',
    ):
        m = re.search(pattern, text, re.I)
        if m:
            raw = re.sub(r'\s+', ' ', m.group(1)).strip()
            parts = re.split(r'\s*[•·]\s*', raw)
            if len(parts) > 1:
                return parts[-1].strip()
    return fallback.replace("-", " ").upper()

def normalize_top(text: str, parent: str, back_label: str, eyebrow: str) -> str:
    text = re.sub(
        r'<a class="(?:back|mametas-detail-back)"[^>]*>.*?</a>',
        f'<a class="mametas-detail-back" href="{parent}">{back_label}</a>',
        text, count=1, flags=re.S | re.I
    )
    text = re.sub(
        r'<div class="meta(?: mametas-detail-eyebrow)?">.*?</div>',
        f'<div class="meta mametas-detail-eyebrow">{eyebrow}</div>',
        text, count=1, flags=re.S | re.I
    )
    text = re.sub(
        r'<p class="eyebrow(?: mametas-detail-eyebrow)?">.*?</p>',
        f'<p class="eyebrow mametas-detail-eyebrow">{eyebrow}</p>',
        text, count=1, flags=re.S | re.I
    )
    return text

def normalize_place_headings(text: str) -> str:
    # Restrict heading-level normalization to .place cards only.
    pattern = re.compile(r'<div class="place"[^>]*>[\s\S]*?</div>(?=(?:\s*<div class="place"|\s*<div class="verdict"|\s*<div class="sources"|\s*<p class="mini-rule"|\s*</div>|\s*</article>))', re.I)
    pos = 0
    parts = []
    for m in pattern.finditer(text):
        parts.append(text[pos:m.start()])
        block = m.group(0)
        block = re.sub(r'<h2([^>]*)>', r'<h3\1>', block, flags=re.I)
        block = re.sub(r'</h2>', '</h3>', block, flags=re.I)
        parts.append(block)
        pos = m.end()
    if not parts:
        return text
    parts.append(text[pos:])
    return ''.join(parts)

def normalize_external_labels(text: str, lang: str) -> str:
    map_label = "Ouvrir la carte ↗" if lang == "fr" else "Open map ↗"
    official_label = "Source officielle ↗" if lang == "fr" else "Official source ↗"
    source_label = "Source ↗"

    def repl(m):
        attrs, inner = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        href_m = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        href = href_m.group(1) if href_m else ""
        if "google.com/maps" in href or "maps.google" in href:
            return f'<a{attrs}>{map_label}</a>'
        low = inner.lower().replace("↗", "").strip()
        if low in {"official source", "official site", "source officielle", "site officiel"}:
            return f'<a{attrs}>{official_label}</a>'
        if low == "source":
            return f'<a{attrs}>{source_label}</a>'
        if inner in {"Michelin Guide", "Michelin"}:
            return f'<a{attrs}>{inner} ↗</a>'
        return m.group(0)

    return re.sub(r'<a([^>]+)>([\s\S]*?)</a>', repl, text, flags=re.I)

def normalize_end_labels(text: str, lang: str) -> str:
    if lang == "en":
        repls = {
            "NEXT DECISION": "THE NEXT DECISION",
            "WHAT NEXT?": "THE NEXT DECISION",
            "WHAT NEXT": "THE NEXT DECISION",
            "NEXT DECISIONS": "THE NEXT DECISION",
            "Checked sources": "Sources checked",
            "Verified sources": "Sources checked",
        }
    else:
        repls = {
            "DÉCISIONS SUIVANTES": "LA PROCHAINE DÉCISION",
            "CONTINUER": "LA PROCHAINE DÉCISION",
            "ET ENSUITE ?": "LA PROCHAINE DÉCISION",
            "Sources consultées": "Sources vérifiées",
        }
    for old, new in repls.items():
        text = text.replace(old, new)
    return text

def normalize_culture_copy(text: str, lang: str) -> str:
    if lang == "en":
        text = text.replace("<h2>Why go</h2>", "<h2>Why we go</h2>")
        text = text.replace("<h2>What to look at</h2>", "<h2>What to actually look at</h2>")
        text = re.sub(r'(<div class="culture-practical"><span>)[^<]+(</span>)', r'\1PRACTICAL\2', text, flags=re.I)
    else:
        text = text.replace("<h2>Pourquoi y aller</h2>", "<h2>Pourquoi on y va</h2>")
        text = re.sub(r'(<div class="culture-practical"><span>)[^<]+(</span>)', r'\1PRATIQUE\2', text, flags=re.I)
        text = text.replace("MAMETAS SAYS", "MAMETAS DIT")
    return text

def normalize_internal_review_links(text: str, lang: str) -> str:
    label = "Lire notre avis complet →" if lang == "fr" else "Read our full review →"

    def repl(m):
        attrs, inner = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        href_m = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        href = href_m.group(1) if href_m else ""
        if not re.match(r'^/(?:en/)?hotels/[^/]+/[^/]+/?$', href):
            return m.group(0)
        low = inner.lower().replace("→", "").strip()
        accepted = {
            "see our full take", "read our full review", "see the hotel",
            "read full review", "full review", "voir notre avis", "lire notre avis complet",
            "voir l’hôtel", "voir l'hotel"
        }
        if low in accepted:
            return f'<a{attrs}>{label}</a>'
        return m.group(0)

    return re.sub(r'<a([^>]+)>([\s\S]*?)</a>', repl, text, flags=re.I)

def family_info(rel: Path, text: str):
    parts = rel.parts
    lang = page_lang(text)

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "restaurants" and parts[-1] == "index.html":
        return lang, "/en/restaurants/", "← Back to restaurants", "RESTAURANTS", parts[-2]
    if len(parts) >= 3 and parts[0] == "restaurants" and parts[-1] == "index.html":
        return lang, "/restaurants/", "← Retour aux restaurants", "RESTAURANTS", parts[-2]

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "beaches" and parts[-1] == "index.html":
        return lang, "/en/beaches/", "← Back to beaches", "BEACHES", parts[-2]
    if len(parts) >= 3 and parts[0] == "plages" and parts[-1] == "index.html":
        return lang, "/plages/", "← Retour aux plages", "PLAGES", parts[-2]

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "culture" and parts[-1] == "index.html":
        return lang, "/en/culture/", "← Back to Art & Culture", "ART & CULTURE", parts[-2]
    if len(parts) >= 3 and parts[0] == "culture" and parts[-1] == "index.html":
        return lang, "/culture/", "← Retour à Art & Culture", "ART & CULTURE", parts[-2]

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "good-finds" and parts[-1] == "index.html" and parts[-2] not in PRACTICAL_GOOD_FINDS_EN:
        return lang, "/en/good-finds/", "← Back to Good Finds", "GOOD FINDS", parts[-2]
    if len(parts) >= 3 and parts[0] == "bons-plans" and parts[-1] == "index.html" and parts[-2] not in PRACTICAL_GOOD_FINDS_FR:
        return lang, "/bons-plans/", "← Retour aux Bons Plans", "BONS PLANS", parts[-2]

    return None

def main() -> None:
    changed = []
    checked = 0

    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8", errors="ignore")
        info = family_info(rel, text)
        if not info:
            # Still normalize local full-review CTA labels site-wide.
            before = text
            text = normalize_internal_review_links(text, page_lang(text))
            if text != before:
                path.write_text(text, encoding="utf-8")
                changed.append(rel.as_posix())
            continue

        lang, parent, back, type_label, slug = info
        before = text
        subject = text_subject(text, slug)
        eyebrow = f"{type_label} · {subject}"

        text = normalize_top(text, parent, back, eyebrow)
        text = normalize_place_headings(text)
        text = normalize_external_labels(text, lang)
        text = normalize_end_labels(text, lang)
        text = normalize_internal_review_links(text, lang)

        if "culture/" in rel.as_posix():
            text = normalize_culture_copy(text, lang)

        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel.as_posix())

        # Detail page guard: a page with a visible H1 should have canonical top.
        if "<h1" in text.lower():
            checked += 1
            if "mametas-detail-back" not in text or "mametas-detail-eyebrow" not in text:
                raise RuntimeError(f"{rel}: family detail top not normalized")

    if checked < 40:
        raise RuntimeError(f"Only {checked} family detail pages normalized; expected full Restaurants/Beaches/Culture/Good Finds set")

    print(f"Family normalization passed on {checked} detail pages; changed {len(set(changed))} files.")


if __name__ == "__main__":
    main()
