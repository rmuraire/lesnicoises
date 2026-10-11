#!/usr/bin/env python3
"""Normalize the Gay FAQ family to the existing Babymoon intent-faq system."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
GAY_PAGES=(
"cote-dazur-gay/index.html","cote-dazur-gay/ou-dormir/index.html",
"cote-dazur-gay/plages-sans-voiture/index.html","cote-dazur-gay/itineraire-5-jours/index.html",
"guide-gay-nice/index.html","en/gay-french-riviera/index.html",
"en/gay-french-riviera/where-to-stay/index.html",
"en/gay-french-riviera/beaches-without-a-car/index.html",
"en/gay-french-riviera/5-day-itinerary/index.html","en/gay-nice/index.html",
)

def add_body_class(s, token):
    m=re.search(r'<body\b[^>]*>',s,re.I)
    if not m:raise RuntimeError("missing body")
    tag=m.group()
    if token in tag:return s
    c=re.search(r'class="([^"]*)"',tag)
    new=(tag[:c.start(1)]+c.group(1)+' '+token+tag[c.end(1):]) if c else (tag[:-1]+' class="'+token+'">')
    return s[:m.start()]+new+s[m.end():]

def faq_list_end(s,start):
    n=0
    for m in re.finditer(r'</?div\b[^>]*>',s[start:],re.I):
        n+=-1 if m.group().startswith("</") else 1
        if n==0:return start+m.end()
    raise RuntimeError("FAQ div nesting broken")

def normalize(s,rel):
    s=s.replace('<section class="mametas-faq-parity">','<section class="intent-faq">')
    m=re.search(r'<div class="faq-list">',s)
    if m:
        end=faq_list_end(s,m.start())
        content=s[m.end():end-6]
        if content.count('<details')<3 or content.count('</details>')!=content.count('<details'):
            raise RuntimeError(rel+": incomplete FAQ")
        h=re.search(r'<h2[^>]*>\s*FAQ\s*</h2>\s*$',s[:m.start()],re.I)
        if not h:raise RuntimeError(rel+": FAQ heading not attached to list")
        s=s[:h.start()]+'<section class="intent-faq"><h2>FAQ</h2>'+content+'</section>'+s[end:]
    sections=len(re.findall(r'<section\s+class="intent-faq"[^>]*>',s))
    headings=len(re.findall(r'<h2[^>]*>\s*FAQ\s*</h2>',s,re.I))
    if sections>1 or headings>1:raise RuntimeError(rel+": duplicated FAQ")
    if sections:
        if s.count('<details')<3:raise RuntimeError(rel+": FAQ not interactive")
        s=add_body_class(s,'mametas-gay-faq')
    elif headings:
        raise RuntimeError(rel+": unconverted FAQ")
    return s

def run():
    count=0
    for rel in GAY_PAGES:
        p=ROOT/rel
        if not p.is_file():continue
        old=p.read_text(encoding='utf-8')
        new=normalize(old,rel)
        if new!=old:
            p.write_text(new,encoding='utf-8')
            count+=1
    # V4 injected an unrelated sixth CTA into the five-door Solo Female
    # navigation grid. Remove *only that exact tile*, not genuine Hotel Fit
    # links in hotel recommendations, and preserve all five editorial doors.
    solo_tiles={
        'cote-dazur-femme-solo/index.html': (
            '<a class="gay-door btn btn--primary mametas-hotel-fit-primary" href="/hotels/finder/">Tester Hotel Fit</a>'
        ),
        'en/solo-female-french-riviera/index.html': (
            '<a class="gay-door btn btn--primary mametas-hotel-fit-primary" href="/en/hotels/finder/">Try Hotel Fit</a>'
        ),
    }
    for rel,tile in solo_tiles.items():
        path=ROOT/rel
        if not path.is_file():raise RuntimeError(rel+": solo landing missing")
        original=path.read_text(encoding="utf-8")
        existing=original.count(tile)
        if existing>1:raise RuntimeError(rel+": duplicated stray CTA")
        cleaned=original.replace(tile,"",1)
        if cleaned.count('class="gay-door"')!=5:
            raise RuntimeError(rel+": solo decision grid must retain exactly five cards")
        if 'gay-door btn btn--primary mametas-hotel-fit-primary' in cleaned:
            raise RuntimeError(rel+": stray Hotel Fit grid tile survived")
        if cleaned!=original:
            path.write_text(cleaned,encoding="utf-8")
            print("SOLO_GRID_FIXED",rel,"five cards, extra Hotel Fit removed",flush=True)
    print('V36 canonical Babymoon FAQ pages=',count,flush=True)

if __name__=='__main__':run()
