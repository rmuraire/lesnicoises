#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile Mametas Presentation System v1 onto the fully generated CSS.

This script must run late in the build, after all legacy/site generation passes.
It never replaces generated CSS with source CSS; it only appends one controlled
system layer and makes two semantic copy fixes on the Stay journey.
"""
from pathlib import Path

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

def patch_copy(path: Path, replacements):
    if not path.exists():
        return
    text=path.read_text(encoding="utf-8",errors="ignore")
    before=text
    for old,new in replacements:
        text=text.replace(old,new)
    if text!=before:
        path.write_text(text,encoding="utf-8")
        print("Updated journey label:",path.relative_to(ROOT))

for rel in ("assets/site.css","assets/v3.css"):
    compile_css(ROOT/rel)

en_repl=[("STEP 02 · CHOOSE THE HOTEL","AFTER THE BASE · CHOOSE THE HOTEL")]
fr_repl=[("ÉTAPE 02 · CHOISIR L’HÔTEL","APRÈS LA VILLE · CHOISIR L’HÔTEL")]
for rel in ("index.html","en/hotels/index.html"):
    patch_copy(ROOT/rel,en_repl)
for rel in ("fr/index.html","hotels/index.html"):
    patch_copy(ROOT/rel,fr_repl)

# Guards.
for rel in ("assets/site.css","assets/v3.css"):
    text=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
    if text.count(START)!=1:
        raise SystemExit(f"{rel}: expected exactly one presentation-system marker")
    if UNSAFE in text:
        raise SystemExit(f"{rel}: unsafe 2026-10-01 city/detail experiment still present")

for rel,bad in (
    ("index.html","STEP 02 · CHOOSE THE HOTEL"),
    ("en/hotels/index.html","STEP 02 · CHOOSE THE HOTEL"),
    ("fr/index.html","ÉTAPE 02 · CHOISIR L’HÔTEL"),
    ("hotels/index.html","ÉTAPE 02 · CHOISIR L’HÔTEL"),
):
    p=ROOT/rel
    if p.exists() and bad in p.read_text(encoding="utf-8",errors="ignore"):
        raise SystemExit(f"{rel}: obsolete step label remains")

print("Mametas Presentation System v1 compiled successfully")
