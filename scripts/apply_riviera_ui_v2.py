#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final Riviera Guide / Riviera Fit delivery layer.

Runs after the existing generators. It does not replace site.css, v3.css or
riviera-chooser.css; it appends one final stylesheet link and stable body
classes so every Riviera page receives the same final presentation layer.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
CSS_HREF="/assets/mametas-riviera-v2.css?v=2.0"

HUBS=("en/riviera-guide/index.html","riviera-guide/index.html")
LEGACY_DESTS=(
    "en/riviera-guide/nice/index.html","riviera-guide/nice/index.html",
    "en/riviera-guide/cannes/index.html","riviera-guide/cannes/index.html",
    "en/riviera-guide/eze/index.html","riviera-guide/eze/index.html",
    "en/riviera-guide/saint-paul-de-vence/index.html","riviera-guide/saint-paul-de-vence/index.html",
    "en/riviera-guide/saint-tropez/index.html","riviera-guide/saint-tropez/index.html",
)
V3_DESTS=(
    "en/riviera-guide/villefranche-cap-ferrat/index.html","riviera-guide/villefranche-cap-ferrat/index.html",
    "en/riviera-guide/antibes/index.html","riviera-guide/antibes/index.html",
    "en/riviera-guide/monaco/index.html","riviera-guide/monaco/index.html",
    "en/riviera-guide/menton/index.html","riviera-guide/menton/index.html",
)
FIT_PAGES=("en/riviera-chooser/index.html","riviera-chooser/index.html")
ALL_TARGETS=HUBS+LEGACY_DESTS+V3_DESTS+FIT_PAGES

def add_body_classes(text: str, classes):
    m=re.search(r"<body([^>]*)>",text,re.I)
    if not m:
        raise SystemExit("Missing body tag")
    tag=m.group(0)
    existing=[]
    cm=re.search(r'class="([^"]*)"',tag,re.I)
    if cm:
        existing=cm.group(1).split()
    for cls in classes:
        if cls not in existing:
            existing.append(cls)
    if cm:
        new=re.sub(r'class="([^"]*)"',f'class="{" ".join(existing)}"',tag,1,flags=re.I)
    else:
        new=tag[:-1]+f' class="{" ".join(existing)}">'
    return text[:m.start()]+new+text[m.end():]

def add_stylesheet(text: str):
    # Remove any earlier version first.
    text=re.sub(
        r'<link[^>]+href="/assets/mametas-riviera-v2\.css(?:\?v=[^"]*)?"[^>]*>\s*',
        '',
        text,
        flags=re.I
    )
    link=f'<link rel="stylesheet" href="{CSS_HREF}">'
    if "</head>" not in text.lower():
        raise SystemExit("Missing head close tag")
    idx=text.lower().rfind("</head>")
    return text[:idx]+link+"\n"+text[idx:]

def patch_hub_numbering(text: str):
    # Stable 01/02/03/04 order in the hesitation block.
    text=text.replace(
        '<a class="decision-card" href="/en/hotels/without-a-car/"><span class="decision-number">02</span>',
        '<a class="decision-card" href="/en/hotels/without-a-car/"><span class="decision-number">03</span>'
    )
    text=text.replace(
        '<a class="decision-card" href="/plan/five-days-nice-no-car/"><span class="decision-number">03</span>',
        '<a class="decision-card" href="/plan/five-days-nice-no-car/"><span class="decision-number">04</span>'
    )
    text=text.replace(
        '<a class="decision-card" href="/hotels/sans-voiture/"><span class="decision-number">02</span>',
        '<a class="decision-card" href="/hotels/sans-voiture/"><span class="decision-number">03</span>'
    )
    text=text.replace(
        '<a class="decision-card" href="/fr/planifier/cinq-jours-nice-sans-voiture/"><span class="decision-number">03</span>',
        '<a class="decision-card" href="/fr/planifier/cinq-jours-nice-sans-voiture/"><span class="decision-number">04</span>'
    )
    return text

def process(rel, classes):
    p=ROOT/rel
    if not p.exists():
        raise SystemExit(f"Missing target {rel}")
    text=p.read_text(encoding="utf-8",errors="ignore")
    before=text
    text=add_stylesheet(text)
    text=add_body_classes(text,classes)
    if rel in HUBS:
        text=patch_hub_numbering(text)
    if text!=before:
        p.write_text(text,encoding="utf-8")
        print("Updated",rel)

for rel in HUBS:
    process(rel,("rg-hub",))
for rel in LEGACY_DESTS:
    process(rel,("rg-destination","rg-legacy"))
for rel in V3_DESTS:
    process(rel,("rg-destination","rg-v3"))
for rel in FIT_PAGES:
    process(rel,("rg-fit",))

# Guards.
for rel in ALL_TARGETS:
    body=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
    if body.count("/assets/mametas-riviera-v2.css?v=2.0")!=1:
        raise SystemExit(f"{rel}: final stylesheet missing/duplicated")
    if rel in HUBS and "rg-hub" not in body:
        raise SystemExit(f"{rel}: hub class missing")
    if rel in LEGACY_DESTS and not all(x in body for x in ("rg-destination","rg-legacy")):
        raise SystemExit(f"{rel}: legacy destination classes missing")
    if rel in V3_DESTS and not all(x in body for x in ("rg-destination","rg-v3")):
        raise SystemExit(f"{rel}: V3 destination classes missing")
    if rel in FIT_PAGES and "rg-fit" not in body:
        raise SystemExit(f"{rel}: Fit class missing")

print("Mametas Riviera UI v2 applied to",len(ALL_TARGETS),"pages")
