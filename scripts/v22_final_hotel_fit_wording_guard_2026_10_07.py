#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final late-stage Hotel Fit wording guard for Claude audit recipe.

Runs after all content/parity/layout generators so earlier scripts cannot
reintroduce the old dash wording or French "match" anglicism.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"assets/hotel-engine.js"

SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def protect_blocks(s):
    blocks=[]
    pat=re.compile(r'<(script|style)\\b[^>]*>[\\s\\S]*?</\\1>',re.I)
    def repl(m):
        key=f"__MAMETAS_PROTECTED_{len(blocks)}__"
        blocks.append(m.group(0))
        return key
    return pat.sub(repl,s),blocks

def restore_blocks(s,blocks):
    for i,b in enumerate(blocks):
        s=s.replace(f"__MAMETAS_PROTECTED_{i}__",b)
    return s

def final_french_typography():
    """Re-run French spacing after late hotel-depth materialisation."""
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        src=p.read_text(encoding="utf-8",errors="ignore")
        if not re.search(r"<html\\b[^>]*\\blang=[\"']fr",src,re.I): continue
        protected,blocks=protect_blocks(src)
        parts=re.split(r'(<[^>]+>)',protected)
        for i in range(0,len(parts),2):
            t=parts[i]
            entities=[]
            def hold(m):
                key=f"__MAMETAS_ENTITY_{len(entities)}__"
                entities.append(m.group(0)); return key
            t=re.sub(r'&(?:#[0-9]+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);',hold,t)
            t=re.sub(r'[ \\t\\u00a0\\u202f]+(?=[,.])','',t)
            t=re.sub(r'[ \\t\\u00a0\\u202f]*(?=[?!;»])','\\u202f',t)
            t=re.sub(r'[ \\t\\u00a0\\u202f]*(?=:)', '\\u00a0',t)
            t=re.sub(r'«[ \\t\\u00a0\\u202f]*','«\\u00a0',t)
            for ei,entity in enumerate(entities):
                t=t.replace(f"__MAMETAS_ENTITY_{ei}__",entity)
            parts[i]=t
        out=restore_blocks("".join(parts),blocks)
        if out!=src:
            p.write_text(out,encoding="utf-8"); changed+=1
    print("late French typography changed",changed,"HTML files")

def ensure_hotel66_sources():
    pairs=(
      ("en/hotels/nice/hotel-66/index.html",
       '<div class="sources hotel-depth-sources"><p class="mametas-source-date">Checked 7 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://hotel66nice.com/en/" target="_blank" rel="nofollow noopener">Hotel 66 Nice, official site</a></li></ul></div>'),
      ("hotels/nice/hotel-66/index.html",
       '<div class="sources hotel-depth-sources"><p class="mametas-source-date">Vérifié le 7 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://hotel66nice.com/" target="_blank" rel="nofollow noopener">Hotel 66 Nice, site officiel</a></li></ul></div>')
    )
    for rel,block in pairs:
        p=ROOT/rel
        if not p.exists(): continue
        src=p.read_text(encoding="utf-8",errors="ignore")
        if "hotel-depth-sources" in src: continue
        m=re.search(r'<div class=["\\']affiliate-cta["\\']',src,re.I)
        if not m:
            raise RuntimeError("Hotel 66 affiliate anchor missing: "+rel)
        out=src[:m.start()]+block+src[m.start():]
        p.write_text(out,encoding="utf-8")
        print("added Hotel 66 source/date",rel)

def main():
    s=P.read_text(encoding="utf-8",errors="ignore")
    old=s
    replacements={
      "Aucun match exact.":"Aucune correspondance exacte.",
      " - with the trade-offs made explicit.":", with the trade-offs made explicit.",
      " - with the trade-offs":", with the trade-offs",
      " — with the trade-offs made explicit.":", with the trade-offs made explicit.",
      " - avec les critères qu’il faut accepter de relâcher.":", avec les critères qu’il faut accepter de relâcher.",
      " — avec les critères qu’il faut accepter de relâcher.":", avec les critères qu’il faut accepter de relâcher.",
      " — clearly flagged as above budget.":", clearly flagged as above budget.",
      " - clearly flagged as above budget.":", clearly flagged as above budget.",
      " — clairement signalées comme au-dessus du budget.":", clairement signalées comme au-dessus du budget.",
      " - clairement signalées comme au-dessus du budget.":", clairement signalées comme au-dessus du budget.",
    }
    for a,b in replacements.items():
        s=s.replace(a,b)
    if s!=old:
        P.write_text(s,encoding="utf-8")
        print("patched late Hotel Fit wording")
    else:
        print("late Hotel Fit wording already clean")

    ensure_hotel66_sources()
    final_french_typography()

    bad=("Aucun match exact."," - with the trade-offs"," — with the trade-offs",
         " — clearly flagged"," - clearly flagged",
         " - avec les critères"," — avec les critères")
    survive=[x for x in bad if x in s]
    if survive:
        raise RuntimeError("late Hotel Fit wording survives: "+repr(survive))
    for good in ("Aucune correspondance exacte.","invalidDetailPaths"):
        if good not in s:
            raise RuntimeError("required Hotel Fit token missing: "+good)
    print("Late Hotel Fit audit wording guard passed.")

if __name__=="__main__":
    main()
