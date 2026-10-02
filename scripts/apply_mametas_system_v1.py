#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile Mametas Presentation System v1 onto the fully generated CSS.

Runs late in the build, after legacy generators. It appends one controlled
presentation layer and applies a few semantic hierarchy fixes that must survive
future rebuilds.
"""
from pathlib import Path
import re
import html

from scripts.materialize_editorial_html import DESTINATIONS

ROOT=Path(__file__).resolve().parents[1]
SYSTEM=ROOT/"assets/mametas-system-v1.css"
START="/* Mametas Presentation System v1 — 2026-10-02"
UNSAFE="/* Editorial rhythm harmonisation — city/detail pages — 2026-10-01 */"

def compile_css(path: Path):
    css=path.read_text(encoding="utf-8",errors="ignore")
    if UNSAFE in css:
        css=css.split(UNSAFE,1)[0].rstrip()+"\n"
    if START in css:
        css=css.split(START,1)[0].rstrip()+"\n"
    system=SYSTEM.read_text(encoding="utf-8").strip()
    path.write_text(css.rstrip()+"\n\n"+system+"\n",encoding="utf-8")
    print("Compiled presentation system:",path.relative_to(ROOT))

def write_if_changed(path: Path, text: str, before: str, label: str):
    if text != before:
        path.write_text(text,encoding="utf-8")
        print(label, path.relative_to(ROOT))

def add_body_class(path: Path, cls: str):
    if not path.exists():
        return
    text=path.read_text(encoding="utf-8",errors="ignore")
    before=text
    m=re.search(r"<body([^>]*)>",text,re.I)
    if not m:
        return
    tag=m.group(0)
    if re.search(rf'\b{re.escape(cls)}\b',tag):
        return
    if 'class="' in tag:
        new=re.sub(r'class="([^"]*)"',lambda mm:f'class="{mm.group(1)} {cls}"',tag,1)
    else:
        new=tag[:-1]+f' class="{cls}">'
    text=text[:m.start()]+new+text[m.end():]
    write_if_changed(path,text,before,"Added body class:")

def patch_copy(path: Path, replacements):
    if not path.exists():
        return
    text=path.read_text(encoding="utf-8",errors="ignore")
    before=text
    for old,new in replacements:
        text=text.replace(old,new)
    write_if_changed(path,text,before,"Updated copy:")

def patch_plan(path: Path, lang: str):
    if not path.exists():
        return
    text=path.read_text(encoding="utf-8",errors="ignore")
    before=text

    # Remove the redundant adoption cue between the hero and the actual first decision.
    text=re.sub(
        r'<aside class="hub-adoption-cue hub-adoption-cue--step1">[\s\S]*?</aside>',
        '',
        text,
        count=1
    )

    if lang=="en":
        replacements=[
            ('<p class="eyebrow">START HERE</p><h2>The decisions that remove options.</h2>',
             '<p class="eyebrow">FIRST DECISION</p><h2>Choose your base.</h2>'),
            ('Plan is not one enormous itinerary. It is where Mametas settles the choices that change everything else.',
             'Riviera Fit asks five questions and makes the call. Prefer to understand the trade-offs first? Compare Places.'),
            ('<h3 id="plan-riviera-fit-title">Five questions. One base.</h3>',
             '<h3 id="plan-riviera-fit-title">Five questions. One recommendation.</h3>'),
            ('Not a list of towns. Answer here: Riviera Fit picks the base, explains why and shows the trade-offs.',
             'Answer here. Riviera Fit picks the base, explains why it wins and shows the trade-offs.')
        ]
    else:
        replacements=[
            ('<p class="eyebrow">COMMENCEZ ICI</p><h2>Les décisions qui enlèvent des options.</h2>',
             '<p class="eyebrow">PREMIÈRE DÉCISION</p><h2>Choisissez votre point de chute.</h2>'),
            ('Plan n’est pas un itinéraire géant. C’est l’endroit où l’on tranche les choix qui changent tout le reste du séjour.',
             'Riviera Fit pose cinq questions et tranche. Vous préférez comprendre les compromis avant ? Comparez les destinations.'),
            ('<h3 id="plan-riviera-fit-title">Cinq questions. Un point de chute.</h3>',
             '<h3 id="plan-riviera-fit-title">Cinq questions. Une recommandation.</h3>'),
            ('Pas une liste de villes. Répondez ici : Riviera Fit choisit la ville, explique pourquoi et vous montre les compromis.',
             'Répondez ici. Riviera Fit choisit la ville, explique pourquoi elle gagne et montre les compromis.')
        ]
    for old,new in replacements:
        text=text.replace(old,new)

    write_if_changed(path,text,before,"Simplified Plan hierarchy:")

def patch_places_hub(path: Path, lang: str):
    if not path.exists():
        return
    text=path.read_text(encoding="utf-8",errors="ignore")
    before=text

    # Mark the specific decision block for a denser treatment.
    phrase="If you are still hesitating" if lang=="en" else "ENCORE EN TRAIN D’HÉSITER ?"
    idx=text.find(phrase)
    if idx>=0:
        section_start=text.rfind("<section",0,idx)
        tag_end=text.find(">",section_start)
        if section_start>=0 and tag_end>section_start:
            tag=text[section_start:tag_end+1]
            if "v3-section" in tag and "hesitation-compact" not in tag:
                if 'class="' in tag:
                    newtag=re.sub(r'class="([^"]*)"',lambda m:f'class="{m.group(1)} hesitation-compact"',tag,1)
                else:
                    newtag=tag[:-1]+' class="hesitation-compact">'
                text=text[:section_start]+newtag+text[tag_end+1:]

    # Correct the EN numbering regression visible in the decision cards.
    if lang=="en":
        text=re.sub(
            r'(<a class="decision-card" href="/plan/"><span class="decision-number">)02(</span><h3>Without a car\?</h3>)',
            r'\g<1>03\g<2>', text, count=1
        )
        text=re.sub(
            r'(<a class="decision-card" href="/plan/five-days-nice-no-car/"><span class="decision-number">)03(</span><h3>Five days\?</h3>)',
            r'\g<1>04\g<2>', text, count=1
        )

    write_if_changed(path,text,before,"Compacted Places hesitation block:")

def canonical_city_must(cfg):
    items=[]
    for i,(title,desc) in enumerate(cfg["must"],1):
        items.append(
            '<div class="city-must-item">'
            f'<span class="city-must-number">{i:02d}</span>'
            '<div class="city-must-copy">'
            f'<h3>{html.escape(title)}</h3>'
            f'<p>{html.escape(desc)}</p>'
            '</div></div>'
        )
    return (
        f'<section id="{html.escape(cfg["must_id"],quote=True)}" '
        'class="city-must-list" data-static-editorial="true">'
        f'<h2>{html.escape(cfg["must_title"])}</h2>'
        f'<p class="city-must-intro">{html.escape(cfg["must_intro"])}</p>'
        '<div class="city-must-items">'+''.join(items)+'</div>'
        '</section>'
    )

def normalize_city_must(path: Path, rel: str):
    if not path.exists() or rel not in DESTINATIONS:
        return
    cfg=DESTINATIONS[rel]
    text=path.read_text(encoding="utf-8",errors="ignore")
    before=text
    must_id=re.escape(cfg["must_id"])
    title=re.escape(cfg["must_title"])

    # Remove the old static version of this one section, leaving supporting
    # practical / next-decision layers untouched.
    text=re.sub(
        rf'<section id="{must_id}"[^>]*>[\s\S]*?</section>',
        '',
        text,
        count=1,
        flags=re.I
    )

    # A few V3 generations created a richer duplicate earlier in the article.
    # Remove only the exact same titled section up to the next H2 / source layer.
    text=re.sub(
        rf'<h2[^>]*>\s*{title}\s*</h2>[\s\S]*?(?=<h2\b|<section class="practical-decision-layer"|<div class="sources"|<!-- MAMETAS_STATIC_DECISIONS_START -->)',
        '',
        text,
        count=1,
        flags=re.I
    )

    block=canonical_city_must(cfg)

    # Prefer the existing static editorial marker so practical layers stay grouped.
    marker='<!-- MAMETAS_STATIC_DECISIONS_START -->'
    if marker in text:
        text=text.replace(marker,marker+'\n'+block,1)
    elif '<div class="sources">' in text:
        text=text.replace('<div class="sources">',block+'\n<div class="sources">',1)
    elif '</article>' in text:
        text=text.replace('</article>',block+'\n</article>',1)
    else:
        raise SystemExit(f"{rel}: no safe insertion point for canonical city component")

    # Guard against duplicate visible titles.
    if text.count(cfg["must_title"]) != 1:
        raise SystemExit(f"{rel}: expected one canonical city title, found {text.count(cfg['must_title'])}")

    write_if_changed(path,text,before,"Normalized city decision component:")


for rel in ("assets/site.css","assets/v3.css"):
    compile_css(ROOT/rel)

# Semantic journey labels.
en_repl=[("STEP 02 · CHOOSE THE HOTEL","AFTER THE BASE · CHOOSE THE HOTEL")]
fr_repl=[("ÉTAPE 02 · CHOISIR L’HÔTEL","APRÈS LA VILLE · CHOISIR L’HÔTEL")]
for rel in ("index.html","en/hotels/index.html"):
    patch_copy(ROOT/rel,en_repl)
for rel in ("fr/index.html","hotels/index.html"):
    patch_copy(ROOT/rel,fr_repl)

# Explicit hierarchy / density fixes.
patch_plan(ROOT/"plan/index.html","en")
patch_plan(ROOT/"fr/planifier/index.html","fr")
patch_places_hub(ROOT/"en/riviera-guide/index.html","en")
patch_places_hub(ROOT/"riviera-guide/index.html","fr")

# Agenda and Riviera Fit escaped the first body-scoped rules.
for rel in ("en/good-finds/index.html","bons-plans/index.html"):
    add_body_class(ROOT/rel,"agenda-hub")
for rel in ("en/riviera-fit/index.html","riviera-fit/index.html","en/riviera-chooser/index.html","riviera-chooser/index.html"):
    add_body_class(ROOT/rel,"riviera-fit-tool")

# Canonical city decision component across all materialized destinations.
for rel in DESTINATIONS:
    normalize_city_must(ROOT/rel,rel)

# Guards.
for rel in ("assets/site.css","assets/v3.css"):
    text=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
    if text.count(START)!=1:
        raise SystemExit(f"{rel}: expected exactly one presentation-system marker")
    if UNSAFE in text:
        raise SystemExit(f"{rel}: unsafe 2026-10-01 city/detail experiment still present")
    for required in ("hesitation-compact",".agenda-hub .page-hero h1",".city-must-list",".city-must-item"):
        if required not in text:
            raise SystemExit(f"{rel}: missing presentation rule {required}")

for rel,bad in (
    ("index.html","STEP 02 · CHOOSE THE HOTEL"),
    ("en/hotels/index.html","STEP 02 · CHOOSE THE HOTEL"),
    ("fr/index.html","ÉTAPE 02 · CHOISIR L’HÔTEL"),
    ("hotels/index.html","ÉTAPE 02 · CHOISIR L’HÔTEL"),
):
    p=ROOT/rel
    if p.exists() and bad in p.read_text(encoding="utf-8",errors="ignore"):
        raise SystemExit(f"{rel}: obsolete step label remains")

for rel,bad in (
    ("plan/index.html","Start with the base. Everything else gets easier."),
    ("fr/planifier/index.html","Commencez par la ville. Le reste devient beaucoup plus simple."),
):
    p=ROOT/rel
    if p.exists() and bad in p.read_text(encoding="utf-8",errors="ignore"):
        raise SystemExit(f"{rel}: redundant Plan adoption cue remains")

print("Mametas Presentation System v1.1 compiled successfully")
