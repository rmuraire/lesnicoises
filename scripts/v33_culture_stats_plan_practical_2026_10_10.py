#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Late-rendered, scoped HTML QA for Culture, Plan, Stats and Practical.

Idempotent; preserves all editorial paragraphs, official references, image
copyright links (except no-longer-applicable Matisse attribution) and tool
functionality. Run AFTER the V32 pass, before final release tests.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def add_body(s,klass):
    m=re.search(r'<body\b[^>]*>',s,re.I)
    if not m: raise RuntimeError("Missing <body> element")
    old=m.group()
    if klass in old: return s
    cm=re.search(r'\bclass=(["\'])(.*?)\1',old,re.I)
    if cm:
        new=old[:cm.end(2)]+" "+klass+old[cm.end(2):]
    else:
        new=old[:-1]+f' class="{klass}">'
    return s[:m.start()]+new+s[m.end():]

def update_file(rel,transform,required=True):
    p=ROOT/rel
    if not p.is_file():
        if required:raise RuntimeError("Missing generated page: "+rel)
        print("SKIP optional page",rel,flush=True);return False
    old=p.read_text(encoding="utf-8")
    new=transform(old,rel)
    if new!=old:p.write_text(new,encoding="utf-8")
    return new!=old

def stats(s,rel):
    s=add_body(s,"mametas-stats-guide")
    old='<div class="verdict"><span class="label">TRAVELLER?</span>'
    if old in s:
        s=s.replace(old,'<div class="verdict mametas-stats-traveller"><span class="label">TRAVELLER?</span>',1)
    elif 'mametas-stats-traveller' not in s:
        raise RuntimeError("Stats final traveller block unknown")
    # The live HTML has a CTA wrapped between two <br>s. Never strip the link.
    m=re.search(r'<div class="verdict mametas-stats-traveller">([\s\S]*?)</div>',s,re.I)
    if not m:raise RuntimeError("Stats CTA wrapper missing")
    oldblock=m.group()
    newblock=oldblock.replace('<br/>','').replace('<br>','')
    if newblock!=oldblock:s=s.replace(oldblock,newblock,1)
    return s

def plan_fr(s,rel):
    s=add_body(s,"mametas-plan-chooser-single")
    if 'data-riviera-chooser' not in s:raise RuntimeError("Plan page not a Riviera Fit chooser")
    if 'data-chooser-submit' not in s:raise RuntimeError("Functional verdict control missing")
    # Remove only the redundant full-link in the chooser action row; the
    # functional submit button and result section MUST remain.
    pat=re.compile(r'(<div class="chooser-submit-row">[\s\S]*?)'
                   r'(<a\b[^>]*class="[^"]*plan-fit-full-link[^"]*"[^>]*>[\s\S]*?</a>)'
                   r'([\s\S]*?</div>)',re.I)
    s,n=pat.subn(lambda m:m.group(1)+m.group(3),s,count=1)
    if n!=1 and 'plan-fit-full-link' in s:
        raise RuntimeError("Redundant Plan Riviera Fit button wrapper unknown")
    if s.count('data-chooser-submit')!=1:raise RuntimeError("Unexpected Plan submit duplication")
    return s

def article(s,klass):
    return add_body(s,klass)

def culture(s,rel):
    s=add_body(s,"mametas-culture-detail")
    if "matisse-museum/index.html" in rel or "musee-matisse/index.html" in rel:
        target="/assets/editorial/culture-musee-matisse.webp"
        figure=re.compile(r'(<figure class="culture-hero-media">)([\s\S]*?)(</figure>)',re.I)
        m=figure.search(s)
        if not m: raise RuntimeError("Matisse hero figure missing")
        inside=m.group(2)
        inside,n=re.subn(r'(<img\b[^>]*\bsrc=")[^"]+(")',lambda x:x.group(1)+target+x.group(2),inside,count=1,flags=re.I)
        if n!=1:raise RuntimeError("Matisse hero image missing")
        # This is now the card photograph, NOT the former Yair Haklai photo:
        # don't falsely attribute the new photo to the old photographer.
        inside=re.sub(r'<figcaption>[\s\S]*?</figcaption>',
                      '<figcaption>Visuel de la sélection Culture Mametas.</figcaption>' if not rel.startswith("en/") else
                      '<figcaption>Image from the Mametas Culture selection.</figcaption>',
                      inside,count=1)
        s=s[:m.start()]+m.group(1)+inside+m.group(3)+s[m.end():]
        # The old Yair Haklai source credited a different hero. Remove only
        # that stale photo-credit list item, tolerating extra HTML attributes
        # and whitespace introduced by intermediate materialization passes.
        def remove_stale_photo_credit(match):
            item=match.group(0)
            if ("Yair Haklai" in item or
                "File:Mus%C3%A9e_Matisse_de_Nice.jpg" in item):
                return ""
            return item
        s=re.sub(r'<li\b[^>]*>[\s\S]*?</li>',
                 remove_stale_photo_credit,s,flags=re.I)
        if "Yair Haklai" in s:
            raise RuntimeError("Former Matisse photo credit survived hero replacement")
    return s

def main():
    modified=[]
    if update_file("en/french-riviera-tourism-statistics/index.html",stats):modified.append("statistics")
    if update_file("fr/planifier/index.html",plan_fr,required=False):modified.append("Plan FR")
    for rel in ("en/good-finds/nice-airport-transfer/index.html",
                "bons-plans/transfert-aeroport-nice/index.html"):
        if update_file(rel,lambda s,r:article(s,"mametas-arrival-guide"),required=rel.startswith("en/")):
            modified.append(rel)
    for rel in ("en/practical/safety-emergencies/index.html",
                "pratique/securite-urgences/index.html"):
        if update_file(rel,lambda s,r:article(s,"mametas-safety-guide")):
            modified.append(rel)
    paths=sorted([*ROOT.glob("en/culture/*/index.html"),
                  *ROOT.glob("culture/*/index.html")])
    details=0
    for path in paths:
        rel=path.relative_to(ROOT).as_posix()
        source=path.read_text(encoding="utf-8")
        if 'class="culture-detail"' not in source:continue
        if update_file(rel,culture):modified.append(rel)
        details+=1
    if details<20:raise RuntimeError(f"Culture guide family incomplete: {details}")
    # Existing release gate rejects ASCII blanks before French high punctuation
    # in hotels/sans-voiture; fix only visible text nodes, never tags or hrefs.
    car=ROOT/"hotels/sans-voiture/index.html"
    if car.is_file():
        old_car=car.read_text(encoding="utf-8")
        chunks=re.split(r'(<[^>]+>)',old_car)
        for i in range(0,len(chunks),2):
            chunks[i]=re.sub(r' (?=[?!;»:])', '\u202f', chunks[i])
        fixed=''.join(chunks)
        if fixed!=old_car:
            car.write_text(fixed,encoding="utf-8")
            modified.append("French punctuation in car-free")
        assert not any(re.search(r' (?=[?!;»:])',chunk) for chunk in chunks[::2])
    css=(ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
    assert "MAMETAS CULTURE STATS PLAN SAFETY 2026-10-10" in css
    print("Family QA applied:",len(modified),"Culture details",details,flush=True)

if __name__=="__main__":
    main()
