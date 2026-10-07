#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close Claude C9 H1→H3 hierarchy gaps conservatively.

Insert one family-appropriate H2 immediately before the first H3 only when no
H2 occurs between H1 and that H3. This runs after all page-family transforms,
so late materialisation cannot reintroduce the gap.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def label_for(rel,s):
    fr=bool(re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I))
    p="/"+rel.as_posix()
    if "/beaches/" in p or "/plages/" in p or "plages-sans-voiture" in p or "beaches-without-a-car" in p:
        return "Les plages, une par une" if fr else "The beaches, one by one"
    if "/restaurants/" in p:
        return "La sélection" if fr else "The shortlist"
    if "/plan/" in p or "/planifier/" in p:
        return "Le plan" if fr else "The plan"
    if "5-day-itinerary" in p or "itineraire-5-jours" in p:
        return "L’itinéraire" if fr else "The itinerary"
    if "/culture/nice/" in p:
        return "Les musées" if fr else "The museums"
    if "/hotels/" in p:
        return "La sélection" if fr else "The selection"
    if "/explore/" in p:
        return "À savoir" if fr else "What to know"
    return "À retenir" if fr else "What matters"

def patch():
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        h1=re.search(r'</h1>',s,re.I)
        if not h1: continue
        tail=s[h1.end():]
        m=re.search(r'<h([23])\b',tail,re.I)
        if not m or m.group(1)!="3": continue
        pos=h1.end()+m.start()
        label=label_for(rel,s)
        s=s[:pos]+f'<h2 class="family-section-heading">{label}</h2>'+s[pos:]
        p.write_text(s,encoding="utf-8")
        changed+=1
        print("patched hierarchy",rel)
    print("hierarchy pages changed",changed)

def validate():
    bad=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        h1=re.search(r'</h1>',s,re.I)
        if not h1: continue
        m=re.search(r'<h([23])\b',s[h1.end():],re.I)
        if m and m.group(1)=="3": bad.append(rel.as_posix())
    if bad:
        raise RuntimeError("H1→H3 remains: "+", ".join(bad[:50]))
    print("Claude C9 heading hierarchy validation passed.")

if __name__=="__main__":
    patch()
    validate()
