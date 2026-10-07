#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Late guard for the Claude final-audit recipe.

Runs after all content materialisation so that:
- Hotel Fit wording cannot regress;
- late-created French hotel copy gets correct non-breaking punctuation;
- Hotel 66 has an explicit editorial source/date block.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "assets/hotel-engine.js"
SKIP = {".git",".github","scripts","docs","backup",
        "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def protect_blocks(s):
    blocks=[]
    pat=re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1>', re.I)
    def repl(m):
        key=f"__MAMETAS_PROTECTED_{len(blocks)}__"
        blocks.append(m.group(0))
        return key
    return pat.sub(repl,s),blocks

def restore_blocks(s,blocks):
    for i,b in enumerate(blocks):
        s=s.replace(f"__MAMETAS_PROTECTED_{i}__",b)
    return s

def patch_engine():
    s=ENGINE.read_text(encoding="utf-8",errors="ignore")
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
        ENGINE.write_text(s,encoding="utf-8")
        print("patched late Hotel Fit wording")
    bad=("Aucun match exact."," - with the trade-offs"," — with the trade-offs",
         " — clearly flagged"," - clearly flagged",
         " - avec les critères"," — avec les critères")
    survive=[x for x in bad if x in s]
    if survive:
        raise RuntimeError("late Hotel Fit wording survives: "+repr(survive))
    for good in ("Aucune correspondance exacte.","invalidDetailPaths"):
        if good not in s:
            raise RuntimeError("required Hotel Fit token missing: "+good)

def ensure_hotel66_sources():
    pairs=(
        ("en/hotels/nice/hotel-66/index.html",
         '<div class="sources hotel-depth-sources"><p class="mametas-source-date">Checked 7 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://hotel66nice.com/en/" target="_blank" rel="nofollow noopener">Hotel 66 Nice, official site</a></li></ul></div>'),
        ("hotels/nice/hotel-66/index.html",
         '<div class="sources hotel-depth-sources"><p class="mametas-source-date">Vérifié le 7 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://hotel66nice.com/" target="_blank" rel="nofollow noopener">Hotel 66 Nice, site officiel</a></li></ul></div>')
    )
    for rel,block in pairs:
        p=ROOT/rel
        if not p.exists():
            continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        if "hotel-depth-sources" in s:
            continue
        m=re.search(r"<div class=[\"']affiliate-cta[\"']",s,re.I)
        if not m:
            raise RuntimeError("Hotel 66 affiliate anchor missing: "+rel)
        s=s[:m.start()]+block+s[m.start():]
        p.write_text(s,encoding="utf-8")
        print("added Hotel 66 source/date",rel)

def final_french_typography():
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        src=p.read_text(encoding="utf-8",errors="ignore")
        if not re.search(r"<html\b[^>]*\blang=[\"']fr",src,re.I):
            continue
        protected,blocks=protect_blocks(src)
        parts=re.split(r'(<[^>]+>)',protected)
        for i in range(0,len(parts),2):
            t=parts[i]
            entities=[]
            def hold(m):
                key=f"__MAMETAS_ENTITY_{len(entities)}__"
                entities.append(m.group(0))
                return key
            t=re.sub(r'&(?:#[0-9]+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);',hold,t)
            t=re.sub(r'[ \t\u00a0\u202f]+(?=[,.])','',t)
            t=re.sub(r'[ \t\u00a0\u202f]*(?=[?!;»])','\u202f',t)
            t=re.sub(r'[ \t\u00a0\u202f]*(?=:)', '\u00a0',t)
            t=re.sub(r'«[ \t\u00a0\u202f]*','«\u00a0',t)
            for ei,entity in enumerate(entities):
                t=t.replace(f"__MAMETAS_ENTITY_{ei}__",entity)
            parts[i]=t
        out=restore_blocks("".join(parts),blocks)
        if out!=src:
            p.write_text(out,encoding="utf-8")
            changed+=1
    print("late French typography changed",changed,"HTML files")

def validate_french_spacing():
    bad=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        if not re.search(r"<html\b[^>]*\blang=[\"']fr",s,re.I):
            continue
        protected,_=protect_blocks(s)
        parts=re.split(r'(<[^>]+>)',protected)
        for i in range(0,len(parts),2):
            if re.search(r' (?=[?!;»:])',parts[i]):
                bad.append(rel.as_posix())
                break
    if bad:
        raise RuntimeError("ordinary French high-punctuation spaces survive: "+", ".join(bad[:20]))

def main():
    patch_engine()
    ensure_hotel66_sources()
    final_french_typography()
    validate_french_spacing()
    print("Late final-audit guard passed.")

if __name__=="__main__":
    main()
