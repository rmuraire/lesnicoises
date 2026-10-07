#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clear the remaining final-recipe warnings that represent real polish issues.

Runs after post-parity cleanup:
- add a dated official source block to Hotel 66 EN/FR;
- keep only one standard affiliate disclosure per page;
- assert no pill-shaped button radius remains in the shared shell.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def add_hotel66_source(rel,fr):
    p=ROOT/rel
    if not p.exists(): return
    s=p.read_text(encoding="utf-8",errors="ignore"); old=s
    if "hotel66-final-source" not in s:
        heading="Sources vérifiées" if fr else "Sources checked"
        date="Vérifié le 7 octobre 2026" if fr else "Checked 7 October 2026"
        label="Hôtel 66 Nice, site officiel" if fr else "Hotel 66 Nice, official site"
        url="https://hotel66nice.com/fr/" if fr else "https://hotel66nice.com/en/"
        block=f'''<div class="sources hotel66-final-source"><p class="mametas-source-date">{date}</p><h2>{heading}</h2><ul><li><a href="{url}" target="_blank" rel="nofollow noopener">{label}</a></li></ul></div>'''
        m=re.search(r'<div class=["\']hotel-copy["\']>\s*<div class=["\']affiliate-cta',s,re.I)
        if m:
            s=s[:m.start()]+block+s[m.start():]
        else:
            end=s.find("</article>")
            if end>=0: s=s[:end]+block+s[end:]
    if s!=old:
        p.write_text(s,encoding="utf-8"); print("hotel66 source",rel)

def dedupe_standard_disclosures():
    patterns=(
      "Selection stays editorial.",
      "La sélection reste éditoriale.",
    )
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        for phrase in patterns:
            # Keep first paragraph containing the standard disclosure; remove later
            # disclosure paragraphs, not surrounding editorial/booking content.
            para=re.compile(r'<p\b[^>]*>[\s\S]*?'+re.escape(phrase)+r'[\s\S]*?</p>',re.I)
            matches=list(para.finditer(s))
            if len(matches)>1:
                offset=0
                for m in matches[1:]:
                    a=m.start()+offset; b=m.end()+offset
                    s=s[:a]+s[b:]
                    offset-=b-a
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("disclosure pages deduped",changed)

def validate():
    for rel,fr in (("en/hotels/nice/hotel-66/index.html",False),("hotels/nice/hotel-66/index.html",True)):
        p=ROOT/rel
        if not p.exists(): continue
        t=re.sub(r'<[^>]+>',' ',p.read_text(encoding="utf-8",errors="ignore")).lower()
        if "sources" not in t or ("checked 7 october 2026" not in t and "vérifié le 7 octobre 2026" not in t):
            raise RuntimeError("Hotel 66 source/date missing: "+rel)

    multi=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p.read_text(encoding="utf-8",errors="ignore")))
        n=t.count("Selection stays editorial.")+t.count("La sélection reste éditoriale.")
        if n>1: multi.append(rel.as_posix())
    if multi:
        raise RuntimeError("multiple standard disclosures survive: "+", ".join(multi[:20]))

    css=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8",errors="ignore")
    if "border-radius:999px" in css:
        raise RuntimeError("pill-shaped shared-shell button/link radius survived")
    print("Final recipe warning cleanup passed.")

def main():
    add_hotel66_source("en/hotels/nice/hotel-66/index.html",False)
    add_hotel66_source("hotels/nice/hotel-66/index.html",True)
    dedupe_standard_disclosures()
    validate()

if __name__=="__main__":
    main()
