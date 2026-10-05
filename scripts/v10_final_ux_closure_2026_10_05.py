#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final UX closure from Claude's 5 Oct 2026 prescriber audit.

Runs after editorial/content generators. The goal is conservative:
repair layout/accessibility regressions and add semantic hooks for shared CSS,
without redesigning pages that already work.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]

def read(rel):
    p = ROOT / rel
    return p, p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def write_if(rel, fn):
    p, s = read(rel)
    if not s:
        print("skip missing", rel)
        return
    n = fn(s)
    if n != s:
        p.write_text(n, encoding="utf-8")
        print("patched", rel)
    else:
        print("unchanged", rel)

def ensure_body_class(s, cls):
    m = re.search(r'<body([^>]*)>', s, re.I)
    if not m:
        return s
    attrs = m.group(1)
    cm = re.search(r'class=["\']([^"\']*)["\']', attrs, re.I)
    if cm:
        classes = cm.group(1).split()
        if cls in classes:
            return s
        new_classes = " ".join(classes + [cls])
        new_attrs = attrs[:cm.start()] + f'class="{new_classes}"' + attrs[cm.end():]
    else:
        new_attrs = attrs + f' class="{cls}"'
    return s[:m.start()] + '<body' + new_attrs + '>' + s[m.end():]

# Hotel Fit mobile CSS uses an explicit page scope; upstream generators may rewrite the HTML.
for rel in ("en/hotels/finder/index.html", "hotels/finder/index.html"):
    write_if(rel, lambda s: ensure_body_class(s, "hotel-fit-page"))

# The 90-day Expat layer is injected late by v8 and previously landed outside the content wrapper.
def wrap_expat(s):
    if "expat-first-90-days-2026-10-04" not in s:
        return s
    if 'class="wrap ux-relocation-wrap"' in s:
        return s
    pat = re.compile(
        r'(<section\b[^>]*data-layer=["\']expat-first-90-days-2026-10-04["\'][^>]*>[\s\S]*?</section>)',
        re.I,
    )
    n, count = pat.subn(r'<div class="wrap ux-relocation-wrap">\1</div>', s, count=1)
    if count != 1:
        raise RuntimeError("Could not contain Expat first-90-days block")
    return n

for rel in ("en/explore/living-antibes-expat/index.html", "explore/vivre-antibes-expatrie/index.html"):
    write_if(rel, wrap_expat)

# Monaco practical blocks must never span the viewport edge-to-edge.
def contain_monaco_practical(s):
    return re.sub(
        r'class=["\']culture-practical["\']',
        'class="culture-practical ux-contained-practical"',
        s,
        flags=re.I,
    )

for rel in ("en/riviera-guide/monaco/index.html", "riviera-guide/monaco/index.html"):
    write_if(rel, contain_monaco_practical)

# Legacy destination event promos should not visually impersonate the Mametas verdict.
def mark_event_promos(s):
    pat = re.compile(r'<div class="verdict">[\s\S]*?</div>', re.I)
    def repl(m):
        block = m.group(0)
        if re.search(r'COMING|IRONMAN|CARNIVAL|CARNAVAL|MIPIM', block, re.I):
            return block.replace('class="verdict"', 'class="verdict ux-cross-promo"', 1)
        return block
    return pat.sub(repl, s)

for rel in (
    "en/riviera-guide/nice/index.html", "riviera-guide/nice/index.html",
    "en/riviera-guide/cannes/index.html", "riviera-guide/cannes/index.html",
    "en/riviera-guide/eze/index.html", "riviera-guide/eze/index.html",
    "en/riviera-guide/saint-tropez/index.html", "riviera-guide/saint-tropez/index.html",
    "en/riviera-guide/saint-paul-de-vence/index.html", "riviera-guide/saint-paul-de-vence/index.html",
):
    write_if(rel, mark_event_promos)

def strip_tags(value):
    value = re.sub(r'<[^>]+>', ' ', value)
    value = html.unescape(value)
    return re.sub(r'\s+', ' ', value).strip()

# Add semantic labels so responsive CSS can stack intent tables without losing column meaning.
def label_intent_tables(s):
    table_pat = re.compile(
        r'(<table\b[^>]*class=["\'][^"\']*\bintent-table\b[^"\']*["\'][^>]*>[\s\S]*?</table>)',
        re.I,
    )
    def table_repl(tm):
        table = tm.group(1)
        headers = [strip_tags(x) for x in re.findall(r'<th\b[^>]*>([\s\S]*?)</th>', table, re.I)]
        if not headers:
            return table
        def row_repl(rm):
            row = rm.group(0)
            idx = 0
            def cell_repl(cm):
                nonlocal idx
                tag = cm.group(0)
                label = headers[idx] if idx < len(headers) else ""
                idx += 1
                if 'data-label=' in tag.lower() or not label:
                    return tag
                safe = html.escape(label, quote=True)
                return tag[:-1] + f' data-label="{safe}">'
            return re.sub(r'<td\b[^>]*>', cell_repl, row, flags=re.I)
        tbody = re.search(r'<tbody\b[^>]*>[\s\S]*?</tbody>', table, re.I)
        if not tbody:
            return table
        new_tbody = re.sub(r'<tr\b[^>]*>[\s\S]*?</tr>', row_repl, tbody.group(0), flags=re.I)
        return table[:tbody.start()] + new_tbody + table[tbody.end():]
    return table_pat.sub(table_repl, s)

for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git", ".github", "scripts", "docs", "backup"}:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    before = s
    if "intent-table" in s:
        s = label_intent_tables(s)
    if rel.parts and rel.parts[0] == "en":
        # Small legacy-language leak in English source boxes.
        s = s.replace("Site officiel", "Official site").replace("site officiel", "official site")
    if rel.as_posix() in {"index.html", "fr/index.html"}:
        s = s.replace(
            '<link rel="preload" as="image" href="/assets/editorial/mametas-home-hero-2026-09-11.PNG" type="image/png">',
            '<link rel="preload" as="image" href="/assets/editorial/mametas-five-women-hero-960.webp" type="image/webp">'
        )
        old_hero = '<img src="/assets/editorial/mametas-home-hero-2026-09-11.PNG"'
        new_hero = '<img src="/assets/editorial/mametas-five-women-hero-960.webp" fetchpriority="high" decoding="async"'
        if old_hero in s:
            s = s.replace(old_hero, new_hero, 1)
        elif '/assets/editorial/mametas-five-women-hero-960.webp' in s:
            hero = '<img src="/assets/editorial/mametas-five-women-hero-960.webp"'
            i = s.find(hero)
            if i >= 0 and 'fetchpriority="high"' not in s[i:i+260]:
                s = s.replace(hero, hero + ' fetchpriority="high" decoding="async"', 1)
    if s != before:
        p.write_text(s, encoding="utf-8")



# Bring late-generated Hotel Take pages closer to the polished review vocabulary without
# rewriting their facts. This runs after v8, so its added sections are included.
def normalise_late_hotel_detail(s, fr=False):
    s = ensure_body_class(s, "hotel-detail-page")
    replacements = {
        "<h2>Pourquoi le choisir</h2>": "<h2>À qui il convient</h2>",
        "<h2>Le point faible</h2>": "<h2>Mèfi — le compromis</h2>",
    } if fr else {
        "<h2>Why choose it</h2>": "<h2>Who it suits</h2>",
        "<h2>The catch</h2>": "<h2>Mèfi — the catch</h2>",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s

for p in ROOT.rglob("index.html"):
    rel = p.relative_to(ROOT)
    parts = rel.parts
    is_en_hotel = len(parts) >= 5 and parts[0] == "en" and parts[1] == "hotels"
    is_fr_hotel = len(parts) >= 4 and parts[0] == "hotels"
    if not (is_en_hotel or is_fr_hotel):
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "<h1" not in text.lower() or not any(token in text for token in ("affiliate-cta", "hotel-practical-facts", "MAMETAS HOTEL TAKE", "THE MAMETAS VERDICT", "LE VERDICT MAMETAS")):
        continue
    new = normalise_late_hotel_detail(text, is_fr_hotel)
    if new != text:
        p.write_text(new, encoding="utf-8")

# Editorial links should lead shortlist cards; affiliate links are secondary.
def normalise_hotel_choice_actions(s, fr=False):
    card_pat = re.compile(r'<article class="hotel-choice-card">[\s\S]*?</article>', re.I)
    def card_repl(cm):
        card = cm.group(0)
        internal = re.search(r'<h3><a href="(/[^"]+)">', card, re.I)
        if not internal:
            return card
        internal_href = internal.group(1)
        rate = re.search(r'<a class="rate-link" href="([^"]+)"([^>]*)>[\s\S]*?</a>', card, re.I)
        if not rate:
            return card
        rate_href = rate.group(1)
        editorial_label = "Lire notre avis" if fr else "Read our take"
        rates_label = "Voir les tarifs ↗" if fr else "Check rates ↗"
        if rate_href.startswith("http"):
            actions = (
                f'<div class="hotel-card-actions">'
                f'<a class="rate-link editorial-link" href="{internal_href}">{editorial_label}</a>'
                f'<a class="rate-link affiliate-link" href="{rate_href}" rel="sponsored nofollow noopener" target="_blank">{rates_label}</a>'
                f'</div>'
            )
        else:
            actions = f'<div class="hotel-card-actions"><a class="rate-link editorial-link" href="{internal_href}">{editorial_label}</a></div>'
        return card[:rate.start()] + actions + card[rate.end():]
    return card_pat.sub(card_repl, s)

write_if("stay/nice/index.html", lambda s: normalise_hotel_choice_actions(s, False))
write_if("fr/dormir/nice/index.html", lambda s: normalise_hotel_choice_actions(s, True))


# Metadata parity for the Stay hubs: add alternates only when an upstream template omitted them.
def ensure_hreflang(s, fr_url, en_url):
    tags = []
    if f'hreflang="fr" href="{fr_url}"' not in s and f'href="{fr_url}" hreflang="fr"' not in s:
        tags.append(f'<link rel="alternate" hreflang="fr" href="{fr_url}">')
    if f'hreflang="en" href="{en_url}"' not in s and f'href="{en_url}" hreflang="en"' not in s:
        tags.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
    if 'hreflang="x-default"' not in s:
        tags.append(f'<link rel="alternate" hreflang="x-default" href="{en_url}">')
    if tags:
        s = s.replace("</head>", "\n" + "\n".join(tags) + "\n</head>", 1)
    return s

write_if("en/hotels/index.html", lambda s: ensure_hreflang(
    s, "https://www.mametas.com/hotels/", "https://www.mametas.com/en/hotels/"
))
write_if("hotels/index.html", lambda s: ensure_hreflang(
    s, "https://www.mametas.com/hotels/", "https://www.mametas.com/en/hotels/"
))

# Sitemap closure: include every crawlable page whose canonical URL matches its own file route.
# This repairs linked-but-omitted pages without indexing redirects, noindex pages or aliases.
def expected_url(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        route = "/"
    elif rel.endswith("/index.html"):
        route = "/" + rel[:-len("index.html")]
    else:
        return None
    return "https://www.mametas.com" + route

def canonical_of(text):
    m = re.search(
        r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>',
        text,
        re.I,
    )
    return html.unescape(m.group(1)) if m else None

sitemap_path = ROOT / "sitemap.xml"
if sitemap_path.exists():
    xml = sitemap_path.read_text(encoding="utf-8", errors="ignore")
    existing = set(re.findall(r'<loc>(https://www\.mametas\.com/[^<]*)</loc>', xml))
    forbidden_sitemap = {
        "https://www.mametas.com/en/hotels/nice/",
        "https://www.mametas.com/hotels/nice/",
    }
    candidates = []
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {".git", ".github", "scripts", "docs", "backup"}:
            continue
        text_page = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'<meta\b[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', text_page, re.I):
            continue
        expected = expected_url(p)
        canonical = canonical_of(text_page)
        if expected and canonical == expected and canonical not in existing and canonical not in forbidden_sitemap:
            candidates.append(canonical)
    if candidates:
        rows = "".join(
            f'  <url><loc>{url}</loc><lastmod>2026-10-05</lastmod></url>\n'
            for url in sorted(set(candidates))
        )
        xml = xml.replace("</urlset>", rows + "</urlset>", 1)
        sitemap_path.write_text(xml, encoding="utf-8")
        print(f"Sitemap closure added {len(set(candidates))} self-canonical pages.")

# Validation.
for rel in ("en/hotels/finder/index.html", "hotels/finder/index.html"):
    text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
    if "hotel-fit-page" not in text:
        raise RuntimeError(f"{rel}: Hotel Fit page scope missing")

for rel in ("en/explore/living-antibes-expat/index.html", "explore/vivre-antibes-expatrie/index.html"):
    text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
    if "expat-first-90-days-2026-10-04" in text and "ux-relocation-wrap" not in text:
        raise RuntimeError(f"{rel}: Expat block still outside UX wrapper")

for rel in ("en/riviera-guide/monaco/index.html", "riviera-guide/monaco/index.html"):
    text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
    if "culture-practical" in text and "ux-contained-practical" not in text:
        raise RuntimeError(f"{rel}: Monaco practical block still uncontained")

labelled_tables = 0
for p in ROOT.rglob("*.html"):
    s = p.read_text(encoding="utf-8", errors="ignore")
    if "intent-table" in s:
        labelled_tables += s.count('data-label="')
        if '<td' in s and 'data-label="' not in s:
            raise RuntimeError(f"{p.relative_to(ROOT)}: intent table has no mobile labels")

if labelled_tables < 1:
    raise RuntimeError("No responsive intent-table labels were produced")

sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8", errors="ignore")
for required_url in (
    "https://www.mametas.com/en/explore/",
    "https://www.mametas.com/explore/",
    "https://www.mametas.com/en/good-finds/nice-airport-transfer/",
    "https://www.mametas.com/bons-plans/transfert-aeroport-nice/",
):
    if f"<loc>{required_url}</loc>" not in sitemap_text:
        raise RuntimeError(f"Sitemap still missing important crawlable page: {required_url}")

print(f"Final UX HTML closure passed: {labelled_tables} labelled mobile table cells.")
