#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guard the phase-1 global shell after every production materialization."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP_TOP={".git",".github","docs","scripts","data","backup","lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}
errors=[]
checked=0

for p in ROOT.rglob("*.html"):
    rel=p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in SKIP_TOP:
        continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    if "<main" not in s.lower():
        continue
    checked+=1
    name=rel.as_posix()
    tests=[
        (s.count('class="mametas-global-header"')==1,"global header count"),
        (s.count('class="mametas-global-footer"')==1,"global footer count"),
        (s.count('/assets/mametas-shell-v1.css?v=1.0')==1,"shell CSS count"),
        ('>Plan<' in s and '>Places<' in s and '>Stay<' in s and '>Explore<' in s and '>Practical<' in s if re.search(r'<html[^>]+lang=["\']en',s,re.I) else True,"EN canonical nav"),
        ('>Préparer<' in s and '>Destinations<' in s and '>Dormir<' in s and '>Explorer<' in s and '>Pratique<' in s if re.search(r'<html[^>]+lang=["\']fr',s,re.I) else True,"FR canonical nav"),
        ('Eat &amp; Do' not in s and '>Now<' not in s and '>Manger &amp; faire<' not in s and '>Maintenant<' not in s,"legacy nav labels"),
        ('href="/#plan"' not in s and 'href="/#places"' not in s and 'href="/#now"' not in s and 'href="/fr/#lieux"' not in s and 'href="/fr/#maintenant"' not in s,"legacy nav anchors"),
        ('class="site-header"' not in s and 'class="v3-header"' not in s,"legacy header markup"),
    ]
    for ok,label in tests:
        if not ok:
            errors.append(f"{name}: {label}")

if checked < 150:
    errors.append(f"Only {checked} public HTML pages checked; expected a full materialized site")

css=ROOT/"assets/mametas-shell-v1.css"
if not css.exists() or css.stat().st_size < 2000:
    errors.append("assets/mametas-shell-v1.css missing or unexpectedly small")

if errors:
    print("V6 shell validation failed:")
    for e in errors[:120]:
        print(" -",e)
    raise SystemExit(1)

print(f"V6 shell validation passed on {checked} public HTML pages")
