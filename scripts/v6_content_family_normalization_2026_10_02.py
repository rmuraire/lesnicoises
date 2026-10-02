#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Late family-level normalization for Restaurants, Beaches, Culture and Good Finds.

The pass preserves editorial facts and recommendations. It normalizes the
component grammar around them: page tops, card heading levels, compact decision
metadata, practical blocks, external-link labels and end-of-page vocabulary.
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

def plain(fragment: str) -> str:
    fragment = re.sub(r'<br\s*/?>', ' ', fragment, flags=re.I)
    fragment = re.sub(r'<[^>]+>', ' ', fragment)
    return re.sub(r'\s+', ' ', fragment).strip()

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

    # Some old Culture / Good Finds files are minimal stubs with a bare H1.
    # Give them the same navigation grammar instead of exempting them.
    main = re.search(r'<main\b[^>]*>', text, re.I)
    h1 = re.search(r'<h1\b', text, re.I)
    if main and h1 and main.end() <= h1.start():
        segment = text[main.end():h1.start()]
        additions = []
        if "mametas-detail-back" not in segment:
            additions.append(f'<a class="mametas-detail-back" href="{parent}">{back_label}</a>')
        if "mametas-detail-eyebrow" not in segment:
            additions.append(f'<p class="mametas-detail-eyebrow">{eyebrow}</p>')
        if additions:
            text = text[:h1.start()] + "".join(additions) + text[h1.start():]
    return text

def balanced_div_end(text: str, start: int):
    div_token = re.compile(r'</?div\b[^>]*>', re.I)
    depth = 0
    for token in div_token.finditer(text, start):
        if token.group(0).lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                return token.end()
        else:
            depth += 1
    return None

def transform_balanced_divs(text: str, class_name: str, transform) -> str:
    """Transform complete <div> blocks carrying class_name, including nested divs."""
    search = re.compile(
        rf'<div\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>',
        re.I,
    )
    div_token = re.compile(r'</?div\b[^>]*>', re.I)
    pos = 0
    out = []
    cursor = 0
    while True:
        m = search.search(text, pos)
        if not m:
            break
        depth = 0
        end = None
        for token in div_token.finditer(text, m.start()):
            if token.group(0).lower().startswith("</div"):
                depth -= 1
                if depth == 0:
                    end = token.end()
                    break
            else:
                depth += 1
        if end is None:
            break
        out.append(text[cursor:m.start()])
        out.append(transform(text[m.start():end]))
        cursor = end
        pos = end
    if not out:
        return text
    out.append(text[cursor:])
    return "".join(out)

def normalize_external_labels(text: str, lang: str) -> str:
    map_label = "Ouvrir la carte ↗" if lang == "fr" else "Open map ↗"
    official_label = "Source officielle ↗" if lang == "fr" else "Official source ↗"
    source_label = "Source ↗"

    def repl(m):
        attrs, inner_html = m.group(1), m.group(2)
        inner = plain(inner_html)
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

def restaurant_card(block: str, lang: str) -> str:
    block = re.sub(r'<h2([^>]*)>', r'<h3\1>', block, flags=re.I)
    block = re.sub(r'</h2>', '</h3>', block, flags=re.I)

    address_m = re.search(r'<div class="address">([\s\S]*?)</div>', block, re.I)
    why_m = re.search(r'<p class="why">([\s\S]*?)</p>', block, re.I)
    existing_meta_m = re.search(r'<p class="restaurant-meta">([\s\S]*?)</p>', block, re.I)

    address = plain(address_m.group(1)) if address_m else ""
    why = plain(why_m.group(1)) if why_m else ""
    addr_parts = [x.strip() for x in address.split("·") if x.strip()]
    why_parts = [x.strip() for x in why.split("·") if x.strip()]

    price = ""
    cuisine = ""
    neighbourhood = ""

    if existing_meta_m:
        meta_parts = [x.strip() for x in plain(existing_meta_m.group(1)).split("·") if x.strip()]
        if meta_parts and re.fullmatch(r'€{1,4}', meta_parts[0]):
            price = meta_parts[0]
            cuisine = meta_parts[1] if len(meta_parts) > 1 else ""
            neighbourhood = meta_parts[2] if len(meta_parts) > 2 else ""

    if not price:
        for parts in (addr_parts, why_parts):
            for i, item in enumerate(parts):
                if re.fullmatch(r'€{1,4}', item):
                    price = item
                    if i + 1 < len(parts):
                        cuisine = parts[i + 1]
                    if i + 2 < len(parts):
                        candidate = parts[i + 2]
                        if not candidate.lower().startswith(("best for", "idéal", "choose it for", "choisissez")):
                            neighbourhood = candidate
                    break
            if price:
                break

    if not neighbourhood and len(addr_parts) >= 2:
        tail = addr_parts[-1]
        if not re.fullmatch(r'€{1,4}', tail):
            neighbourhood = tail

    values = [x for x in (price, cuisine, neighbourhood) if x]
    if len(values) >= 2 and not existing_meta_m:
        meta = '<p class="restaurant-meta">' + ' · '.join(values) + '</p>'
        h3 = re.search(r'</h3>', block, re.I)
        if h3:
            block = block[:h3.end()] + meta + block[h3.end():]

    # Older cards sometimes combine the address and decision metadata. Once the
    # decision line exists, keep the address field as an address.
    if address_m and any(re.fullmatch(r'€{1,4}', part) for part in addr_parts):
        first_price = next(i for i, part in enumerate(addr_parts) if re.fullmatch(r'€{1,4}', part))
        clean_address = ' · '.join(addr_parts[:first_price]).strip()
        if clean_address:
            current = re.search(r'<div class="address">[\s\S]*?</div>', block, re.I)
            if current:
                replacement = f'<div class="address">{clean_address}</div>'
                block = block[:current.start()] + replacement + block[current.end():]

    # Nice-generation cards repeat price/cuisine/area inside .why. Preserve only
    # the recommendation clause ("Best for …"), or remove the duplicate line.
    why_current = re.search(r'<p class="why">([\s\S]*?)</p>', block, re.I)
    if why_current:
        why_text = plain(why_current.group(1))
        why_parts_now = [x.strip() for x in why_text.split("·") if x.strip()]
        if why_parts_now and re.fullmatch(r'€{1,4}', why_parts_now[0]):
            keep = next(
                (part for part in why_parts_now if part.lower().startswith(("best for:", "idéal pour", "choose it for:", "choisissez"))),
                "",
            )
            replacement = f'<p class="why">{keep}</p>' if keep else ""
            block = block[:why_current.start()] + replacement + block[why_current.end():]

    return block

def normalize_restaurant_page(text: str, lang: str) -> str:
    text = transform_balanced_divs(text, "place", lambda b: restaurant_card(b, lang))

    if "restaurant-price-legend" not in text:
        # Existing rich legend.
        m = re.search(r'<div class="culture-practical">\s*<span>HOW TO READ THE PRICES</span>([\s\S]*?)</div>', text, re.I)
        if m:
            replacement = '<div class="culture-practical restaurant-price-legend"><span>PRICE GUIDE</span>' + m.group(1) + '</div>'
            text = text[:m.start()] + replacement + text[m.end():]
        else:
            # Existing compact "Price:" rule.
            m = re.search(r'<p class="mini-rule"><strong>Price:</strong>([\s\S]*?)</p>', text, re.I)
            if m:
                replacement = '<div class="culture-practical restaurant-price-legend"><span>PRICE GUIDE</span><p>' + m.group(1).strip() + '</p></div>'
                text = text[:m.start()] + replacement + text[m.end():]
            elif lang == "fr":
                m = re.search(r'<p class="mini-rule"><strong>Prix\s*:</strong>([\s\S]*?)</p>', text, re.I)
                if m:
                    replacement = '<div class="culture-practical restaurant-price-legend"><span>GUIDE DES PRIX</span><p>' + m.group(1).strip() + '</p></div>'
                    text = text[:m.start()] + replacement + text[m.end():]
    return text

def beach_card(block: str, lang: str) -> str:
    block = re.sub(r'<h2([^>]*)>', r'<h3\\1>', block, flags=re.I)
    block = re.sub(r'</h2>', '</h3>', block, flags=re.I)

    facts_start_m = re.search(r'<div class="beach-facts">', block, re.I)
    facts_start = facts_start_m.start() if facts_start_m else None
    facts_end = balanced_div_end(block, facts_start) if facts_start is not None else None
    facts_html = block[facts_start:facts_end] if facts_start is not None and facts_end is not None else ""

    facts = []
    if facts_html:
        for m in re.finditer(r'<div class="beach-fact"><b>(.*?)</b><span>([\\s\\S]*?)</span></div>', facts_html, re.I):
            facts.append([plain(m.group(1)), m.group(2).strip()])

    labels = {x[0].lower(): i for i, x in enumerate(facts)}

    # Derive Access only from transport wording already present on the card.
    if "access" not in labels and "accès" not in labels:
        spot = re.search(r'<p class="spot-logistics">([\\s\\S]*?)</p>', block, re.I)
        if spot:
            raw = re.split(r'<a\\b', spot.group(1), maxsplit=1, flags=re.I)[0]
            access = plain(raw)
            access = re.sub(
                r'^(Find it\\.|Getting there\\.|Access\\.|Accès\\s*:|Y aller\\s*:|Repère\\s*:)',
                '',
                access,
                flags=re.I,
            ).strip()
            if len(access) >= 12:
                facts.append(["Accès" if lang == "fr" else "Access", access])

    # Group existing Cannes lounger/parasol facts into a single 2026-price line.
    price_parts = []
    keep = []
    for label, value in facts:
        if label.lower() in {"lounger", "parasol", "transat"}:
            price_parts.append(f"{label}: {plain(value)}")
        else:
            keep.append([label, value])
    facts = keep
    if price_parts and not any(x[0].lower() in {"2026 prices", "tarifs 2026"} for x in facts):
        facts.append(["Tarifs 2026" if lang == "fr" else "2026 prices", " · ".join(price_parts)])

    if facts:
        preferred = ["type", "access", "accès", "services", "2026 prices", "tarifs 2026"]
        def order(item):
            low = item[0].lower()
            return preferred.index(low) if low in preferred else len(preferred) + facts.index(item)

        ordered = sorted(facts, key=order)
        html = '<div class="beach-facts">' + ''.join(
            f'<div class="beach-fact"><b>{label}</b><span>{value}</span></div>'
            for label, value in ordered
        ) + '</div>'

        if facts_start is not None and facts_end is not None:
            block = block[:facts_start] + html + block[facts_end:]
        else:
            spot = re.search(r'<p class="spot-logistics">', block, re.I)
            if spot:
                block = block[:spot.start()] + html + block[spot.start():]
    return block


def normalize_beach_page(text: str, lang: str) -> str:
    return transform_balanced_divs(text, "place", lambda b: beach_card(b, lang))

def first_external_official_link(text: str):
    for m in re.finditer(r'<a([^>]+)>([\s\S]*?)</a>', text, re.I):
        attrs = m.group(1)
        href_m = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        if not href_m:
            continue
        href = href_m.group(1)
        label = plain(m.group(2)).lower()
        low = href.lower()
        if not href.startswith("http") or "google.com/maps" in low:
            continue
        if any(x in low for x in ("wikimedia.org", "wikipedia.org", "pexels.com", "depositphotos.com", "instagram.com")):
            continue
        if label.startswith("photo"):
            continue
        return href
    return None

def culture_practical_block(block: str, full_text: str, lang: str) -> str:
    if "culture-logistics-grid" in block:
        return block

    content = re.sub(r'^<div[^>]*>|</div>$', '', block, flags=re.I).strip()
    content = re.sub(r'^\s*<span>.*?</span>', '', content, flags=re.S | re.I).strip()
    practical_plain = plain(content)

    segments = re.split(r'<br\s*/?>', content, flags=re.I)
    core_plain = plain(segments[0]) if segments else practical_plain
    access_plain = plain(' '.join(segments[1:])) if len(segments) > 1 else practical_plain

    if lang == "en":
        labels = ("PRACTICAL", "Address", "Getting there", "Time needed", "Hours & price", "Booking")
        missing = "See official information below."
        access_re = r'Getting there\s*:\s*([^|]+?)(?=(?:Open map|Map|Official|$))'
        time_re = r'(?:Allow|Plan for)\s+(?:about\s+)?([0-9]+(?:\s*(?:to|–|-)\s*[0-9]+)?\s*(?:minutes?|hours?))'
        time_sentence_re = r'(?:Allow|Plan for)\s+(?:about\s+)?[0-9]+(?:\s*(?:to|–|-)\s*[0-9]+)?\s*(?:minutes?|hours?)[^.]*\.?'
        checked_re = r'Checked\s+(?:on\s+)?(?:\d{1,2}\s+)?[A-Za-z]+\s+20\d{2}\.?'
    else:
        labels = ("PRATIQUE", "Adresse", "Accès", "Temps à prévoir", "Horaires & tarif", "Réservation")
        missing = "Voir les informations officielles ci-dessous."
        access_re = r'Accès\s*:\s*([^|]+?)(?=(?:Ouvrir la carte|Carte|Horaires|Infos|$))'
        time_re = r'Comptez\s+(?:environ\s+)?([0-9]+(?:\s*(?:à|–|-)\s*[0-9]+)?\s*(?:minutes?|heures?))'
        time_sentence_re = r'Comptez\s+(?:environ\s+)?[0-9]+(?:\s*(?:à|–|-)\s*[0-9]+)?\s*(?:minutes?|heures?)[^.]*\.?'
        checked_re = r'Vérifié(?:e)?\s+(?:le\s+)?(?:\d{1,2}\s+)?[A-Za-zÀ-ÿ]+\s+20\d{2}\.?'

    address = ""
    address_m = re.search(
        r'\b(\d{1,3}\s+(?:rue|avenue|boulevard|quai|promenade|chemin)[^.|]{2,90}|Place\s+[A-ZÀ-ÖØ-Ý][^.|]{2,70})',
        core_plain,
        re.I,
    )
    if address_m:
        address = address_m.group(1).strip(" .")

    access = ""
    m = re.search(access_re, access_plain, re.I)
    if m:
        access = m.group(1).strip(" .")

    duration = ""
    m = re.search(time_re, practical_plain, re.I)
    if m:
        duration = m.group(1).strip()

    # Keep only the remaining opening / price information in this cell. The
    # address, transport and duration have their own fields above.
    hours_price = core_plain
    if address:
        hours_price = hours_price.replace(address, "", 1).strip(" .;·")
    hours_price = re.sub(time_sentence_re, "", hours_price, flags=re.I)
    hours_price = re.sub(checked_re, "", hours_price, flags=re.I)
    hours_price = re.sub(r'\s+', ' ', hours_price).strip(" .;·")
    if not hours_price:
        hours_price = missing

    sources = re.search(r'<div\b[^>]*class=["\'][^"\']*sources[^"\']*["\'][^>]*>[\s\S]*?</div>', full_text, re.I)
    source_html = sources.group(0) if sources else ""
    official_href = first_external_official_link(content) or first_external_official_link(source_html)
    if official_href:
        booking = (
            f'<a href="{official_href}" target="_blank" rel="nofollow noopener">'
            + ("Informations officielles ↗" if lang == "fr" else "Official information ↗")
            + '</a>'
        )
    else:
        booking = missing

    values = (address or missing, access or missing, duration or missing, hours_price, booking)
    grid = ''.join(
        f'<div><b>{label}</b><span>{value}</span></div>'
        for label, value in zip(labels[1:], values)
    )
    return (
        '<div class="culture-logistics" data-culture-logistics="v1">'
        f'<div class="culture-logistics-head"><span>{labels[0]}</span></div>'
        f'<div class="culture-logistics-grid">{grid}</div>'
        '</div>'
    )

def normalize_culture_copy(text: str, lang: str) -> str:
    if lang == "en":
        text = text.replace("<h2>Why go</h2>", "<h2>Why we go</h2>")
        text = text.replace("<h2>What to look at</h2>", "<h2>What to actually look at</h2>")
    else:
        text = text.replace("<h2>Pourquoi y aller</h2>", "<h2>Pourquoi on y va</h2>")
        text = text.replace("MAMETAS SAYS", "RECO MAMETAS")

    original = text
    def repl(m):
        return culture_practical_block(m.group(0), original, lang)
    text = re.sub(r'<div class="culture-practical">[\s\S]*?</div>', repl, text, flags=re.I)
    return text

def normalize_internal_review_links(text: str, lang: str) -> str:
    label = "Lire notre avis complet →" if lang == "fr" else "Read our full review →"

    def repl(m):
        attrs, inner_html = m.group(1), m.group(2)
        inner = plain(inner_html)
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
        return "restaurants", lang, "/en/restaurants/", "← Back to restaurants", "RESTAURANTS", parts[-2]
    if len(parts) >= 3 and parts[0] == "restaurants" and parts[-1] == "index.html":
        return "restaurants", lang, "/restaurants/", "← Retour aux restaurants", "RESTAURANTS", parts[-2]

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "beaches" and parts[-1] == "index.html":
        return "beaches", lang, "/en/beaches/", "← Back to beaches", "BEACHES", parts[-2]
    if len(parts) >= 3 and parts[0] == "plages" and parts[-1] == "index.html":
        return "beaches", lang, "/plages/", "← Retour aux plages", "PLAGES", parts[-2]

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "culture" and parts[-1] == "index.html":
        return "culture", lang, "/en/culture/", "← Back to Art & Culture", "ART & CULTURE", parts[-2]
    if len(parts) >= 3 and parts[0] == "culture" and parts[-1] == "index.html":
        return "culture", lang, "/culture/", "← Retour à Art & Culture", "ART & CULTURE", parts[-2]

    if len(parts) >= 4 and parts[0] == "en" and parts[1] == "good-finds" and parts[-1] == "index.html" and parts[-2] not in PRACTICAL_GOOD_FINDS_EN:
        return "good-finds", lang, "/en/good-finds/", "← Back to Good Finds", "GOOD FINDS", parts[-2]
    if len(parts) >= 3 and parts[0] == "bons-plans" and parts[-1] == "index.html" and parts[-2] not in PRACTICAL_GOOD_FINDS_FR:
        return "good-finds", lang, "/bons-plans/", "← Retour aux Bons Plans", "BONS PLANS", parts[-2]

    return None

def main() -> None:
    changed = []
    checked = 0
    restaurant_meta = 0
    culture_grids = 0

    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8", errors="ignore")
        info = family_info(rel, text)
        if not info:
            before = text
            text = normalize_internal_review_links(text, page_lang(text))
            if text != before:
                path.write_text(text, encoding="utf-8")
                changed.append(rel.as_posix())
            continue

        family, lang, parent, back, type_label, slug = info
        before = text
        subject = text_subject(text, slug)
        eyebrow = f"{type_label} · {subject}"

        text = normalize_top(text, parent, back, eyebrow)
        text = normalize_external_labels(text, lang)
        text = normalize_end_labels(text, lang)
        text = normalize_internal_review_links(text, lang)

        if family == "restaurants":
            text = normalize_restaurant_page(text, lang)
            restaurant_meta += text.count('class="restaurant-meta"')
        elif family == "beaches":
            text = normalize_beach_page(text, lang)
        elif family == "culture":
            text = normalize_culture_copy(text, lang)
            culture_grids += text.count('data-culture-logistics="v1"')

        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel.as_posix())

        if "<h1" in text.lower():
            checked += 1
            if "mametas-detail-back" not in text or "mametas-detail-eyebrow" not in text:
                raise RuntimeError(f"{rel}: family detail top not normalized")

    if checked < 40:
        raise RuntimeError(f"Only {checked} family detail pages normalized; expected full Restaurants/Beaches/Culture/Good Finds set")
    if restaurant_meta < 20:
        raise RuntimeError(f"Only {restaurant_meta} restaurant cards received canonical decision metadata")
    if culture_grids < 20:
        raise RuntimeError(f"Only {culture_grids} culture practical blocks normalized")

    print(
        f"Family normalization passed on {checked} detail pages; "
        f"{restaurant_meta} restaurant cards; {culture_grids} culture practical grids; "
        f"changed {len(set(changed))} files."
    )

if __name__ == "__main__":
    main()
