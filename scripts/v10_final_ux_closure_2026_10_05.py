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

print(f"Final UX HTML closure passed: {labelled_tables} labelled mobile table cells.")
