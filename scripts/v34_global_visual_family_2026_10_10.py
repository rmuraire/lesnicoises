#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final visual consistency pass across compiled Mametas page families.

Run only after all editorial materialization, as the last HTML mutation.
Preserves outbound URLs, editorial text and affiliate tracking.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VILLA = "/assets/editorial/villa-ephrussi-trujillo.webp"
PHOTO = ROOT / VILLA.lstrip("/")
MAP = re.compile(r'(?:google\.[^/" ]+/maps|maps\.app\.goo\.gl)', re.I)
A_OPEN = re.compile(r'<a\b[^>]*>', re.I)
ATTR = re.compile(r'\bclass=(["\'])(.*?)\1', re.I | re.S)

def add_body(s, token):
    m = re.search(r'<body\b[^>]*>', s, re.I)
    if not m:
        raise RuntimeError("No body tag")
    tag = m.group()
    if token in tag.split(): return s
    c=ATTR.search(tag)
    if c:
        tag = tag[:c.start(2)] + c.group(2) + " " + token + tag[c.end(2):]
    else:
        tag = tag[:-1] + ' class="' + token + '">'
    return s[:m.start()] + tag + s[m.end():]

def normalize_anchor(m):
    tag=m.group()
    href=re.search(r'\bhref=(["\'])(.*?)\1',tag,re.I | re.S)
    if not href:
        return tag
    url=href.group(2)
    is_map=bool(MAP.search(url))
    is_hotel_fit=('/hotels/finder/' in url) and bool(re.search(
        r'\b(?:btn|button|cta|action|primary|hotel-fit)\b',tag,re.I))
    if not is_map and not is_hotel_fit:
        return tag
    c=ATTR.search(tag)
    classes=c.group(2).split() if c else []
    if is_map:
        classes=[x for x in classes if x not in ("btn","button")]
        classes.append("mametas-map-inline")
    if is_hotel_fit:
        classes.append("mametas-hotel-fit-primary")
    classes=list(dict.fromkeys(classes))
    if c:
        tag=tag[:c.start()]+'class="'+ " ".join(classes)+'"'+tag[c.end():]
    else:
        tag=tag[:-1]+' class="'+ " ".join(classes)+'">'
    if is_map:
        # Avoid leaking legacy button backgrounds into map links when another
        # late stylesheet overrides the canonical class rule.
        inline="display:inline!important;min-height:0!important;padding:0 0 1px!important;border:0!important;border-bottom:1px solid #b9903f!important;background:transparent!important;box-shadow:none!important;"
        old_style=re.search(r'\bstyle="([^"]*)"',tag,re.I|re.S)
        if old_style:
            tag=tag[:old_style.start(1)]+old_style.group(1).rstrip(";")+";"+inline+tag[old_style.end(1):]
        else:
            tag=tag[:-1]+' style="'+inline+'">'
    return tag

def final_stylesheet(s):
    """All generated pages receive the same FINAL CSS, after late rewrites."""
    link='<link rel="stylesheet" href="/assets/mametas-foundation.css?v=1.9">'
    s=re.sub(r'<link\b[^>]*href=["\']/assets/mametas-foundation\.css(?:\?[^"\']*)?["\'][^>]*>\s*','',s,flags=re.I)
    close=re.search(r'</head>',s,re.I)
    if not close:raise RuntimeError("HTML without head close")
    return s[:close.start()]+link+"\n"+s[close.start():]

def apply_villa(s,rel):
    if rel.endswith("/villa-ephrussi/index.html"):
        # Exactly the culture hero photograph, not unrelated interior images.
        fig=re.compile(r'(<figure\b[^>]*class="[^"]*culture-hero-media[^"]*"[^>]*>)([\s\S]*?)(</figure>)',re.I)
        m=fig.search(s)
        if not m:raise RuntimeError("Villa hero missing: "+rel)
        inner=m.group(2)
        inner,n=re.subn(r'(<img\b[^>]*\bsrc=")[^"]+(")',
            lambda a:a.group(1)+VILLA+a.group(2),inner,count=1,flags=re.I)
        if n!=1:raise RuntimeError("Villa hero img missing: "+rel)
        caption='Photo : Jean-Elie Trujillo / Pixabay · sélection Mametas.' if not rel.startswith("en/") else 'Photo: Jean-Elie Trujillo / Pixabay · Mametas selection.'
        inner=re.sub(r'<figcaption>[\s\S]*?</figcaption>','<figcaption>'+caption+'</figcaption>',inner,count=1,flags=re.I)
        s=s[:m.start()]+m.group(1)+inner+m.group(3)+s[m.end():]
        # Only the now-inaccurate credit for the former Commons photograph.
        s=re.sub(r'<li\b[^>]*>[\s\S]*?</li>',
            lambda m:'' if 'File:Villa_Ephrussi_de_Rothschild.jpg' in m.group() else m.group(),
            s,flags=re.I)
        if "Idarvol" in s:
            raise RuntimeError("Old Villa Ephrussi photo attribution still appears in "+rel)
        return s
    if rel in ("culture/index.html","en/culture/index.html"):
        pat=re.compile(r'(<a\b[^>]*href="/(?:en/)?culture/villa-ephrussi/"[^>]*>[\s\S]*?<img\b[^>]*\bsrc=")[^"]+(")',re.I)
        s,n=pat.subn(lambda m:m.group(1)+VILLA+m.group(2),s,count=1)
        if n!=1:raise RuntimeError("Villa culture vignette not found: "+rel)
    return s

def main():
    if not PHOTO.is_file() or PHOTO.stat().st_size < 15000:
        raise RuntimeError("Verified Villa Ephrussi photo is missing")
    from PIL import Image
    with Image.open(PHOTO) as im:
        im.verify()
    links=0
    maps=0
    fit=0
    pages=0
    villa_pages=0
    for path in sorted(ROOT.rglob("*.html")):
        rel=path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/","docs/","scripts/","backup/","node_modules/","lesnicoises-v8-")):
            continue
        s=path.read_text(encoding="utf-8",errors="replace")
        if "<html" not in s.lower() or "</head>" not in s.lower():continue
        old=s
        if re.match(r'^(?:en/)?explore/[^/]+/index.html$',rel):
            s=add_body(s,"mametas-explore-detail")
        if re.match(r'^(?:en/)?solo-female-french-riviera/[^/]+/index.html$',rel) or re.match(
            r'^(?:en/)?voyage-femme-seule-cote-dazur/[^/]+/index.html$',rel):
            s=add_body(s,"mametas-solo-detail")
        if rel in ("en/culture/index.html","culture/index.html",
                   "en/culture/villa-ephrussi/index.html","culture/villa-ephrussi/index.html"):
            s=apply_villa(s,rel)
            villa_pages+=1
        maps+=len(MAP.findall(s))
        s=A_OPEN.sub(normalize_anchor,s)
        s=final_stylesheet(s)
        # A durable check even if some original anchor carried button CSS.
        if rel.endswith("where-to-stay/index.html") and "solo" in rel and "mametas-solo-detail" not in s:
            raise RuntimeError("Solo Female stays family not tagged")
        if s!=old:
            path.write_text(s,encoding="utf-8")
            pages+=1
    if villa_pages!=4:raise RuntimeError(f"Expected 4 Villa detail/index surfaces, got {villa_pages}")
    if pages<30:raise RuntimeError(f"Global visual coverage unexpectedly narrow: {pages}")
    css=(ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
    if "MAMETAS FAMILY PARITY OCT 2026" not in css:
        raise RuntimeError("Global QA stylesheet marker missing")
    print(f"FINAL FAMILY QA: changed {pages} public pages; map URL occurrences {maps}; Villa surfaces {villa_pages}")

if __name__=="__main__":
    main()
