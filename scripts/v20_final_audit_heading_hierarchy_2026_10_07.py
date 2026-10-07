#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close Claude C9 H1→H3 hierarchy gaps without restructuring content.

For the explicit pages reported by the final recipe diagnostic, insert one
family-appropriate H2 immediately before the first H3 only when no H2 occurs
between H1 and that H3. This preserves cards/content and fixes document
hierarchy with minimal visual/editorial change.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

TARGETS={
 "restaurants/index.html":"Où manger",
 "en/restaurants/index.html":"Where to eat",
 "cote-dazur-gay/plages-sans-voiture/index.html":"Les plages, une par une",
 "en/gay-french-riviera/beaches-without-a-car/index.html":"The beaches, one by one",
 "plages/antibes/index.html":"Les plages, une par une",
 "plages/saint-tropez/index.html":"Les plages, une par une",
 "plages/cannes/index.html":"Les plages, une par une",
 "plages/autour-de-nice/index.html":"Les plages, une par une",
 "plages/nice/index.html":"Les plages, une par une",
 "en/beaches/around-nice/index.html":"The beaches, one by one",
 "en/beaches/antibes/index.html":"The beaches, one by one",
 "en/beaches/saint-tropez/index.html":"The beaches, one by one",
 "en/beaches/cannes/index.html":"The beaches, one by one",
 "en/beaches/nice/index.html":"The beaches, one by one",
 "en/restaurants/menton/index.html":"The shortlist",
 "en/restaurants/theoule-sur-mer/index.html":"The shortlist",
 "en/restaurants/saint-tropez/index.html":"The shortlist",
 "en/restaurants/mougins/index.html":"The shortlist",
 "en/restaurants/saint-paul-de-vence/index.html":"The shortlist",
 "en/restaurants/grasse/index.html":"The shortlist",
 "restaurants/menton/index.html":"La sélection",
 "restaurants/theoule-sur-mer/index.html":"La sélection",
 "restaurants/saint-tropez/index.html":"La sélection",
 "restaurants/mougins/index.html":"La sélection",
 "restaurants/saint-paul-de-vence/index.html":"La sélection",
 "restaurants/grasse/index.html":"La sélection",
 "en/culture/nice/index.html":"The museums",
 "culture/nice/index.html":"Les musées",
 "hotels/cannes/index.html":"La sélection",
 "hotels/nice/index.html":"La sélection",
}

def patch():
    changed=0
    for rel,label in TARGETS.items():
        p=ROOT/rel
        if not p.exists():
            print("skip missing",rel); continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        h1=re.search(r'</h1>',s,re.I)
        if not h1:
            print("skip no h1",rel); continue
        tail=s[h1.end():]
        h3=re.search(r'<h3\b',tail,re.I)
        if not h3:
            continue
        h2=re.search(r'<h2\b',tail[:h3.start()],re.I)
        if h2:
            continue
        pos=h1.end()+h3.start()
        s=s[:pos]+f'<h2 class="family-section-heading">{label}</h2>'+s[pos:]
        p.write_text(s,encoding="utf-8")
        changed+=1
        print("patched hierarchy",rel)
    print("hierarchy pages changed",changed)

def validate():
    bad=[]
    for rel in TARGETS:
        p=ROOT/rel
        if not p.exists(): continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        h1=re.search(r'</h1>',s,re.I)
        if not h1: continue
        tail=s[h1.end():]
        m=re.search(r'<h([23])\b',tail,re.I)
        if m and m.group(1)=="3":
            bad.append(rel)
    if bad:
        raise RuntimeError("H1→H3 remains: "+", ".join(bad))
    print("Claude C9 heading hierarchy validation passed.")

if __name__=="__main__":
    patch()
    validate()
