#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit, lot 4A: external images, hreflang and low-risk parity fixes.

Runs after lot 3 in production. It deliberately handles only items that are
mechanical and source-preserving:
- localise every Wikimedia image used at runtime;
- add missing hotel-selection hreflang pairs;
- remove/translate a handful of wrong-language fragments called out by Claude;
- remove the empty "En ce moment" heading on Fondation Maeght FR;
- repair the missing Riviera-vs-Amalfi decision card in the FR guide hub when
  the later build has generated the numbered decision-grid version.

No editorial facts are invented here.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import hashlib
import mimetypes
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

WIKI_HOSTS=("commons.wikimedia.org","upload.wikimedia.org")

def is_wiki(url:str)->bool:
    try:
        return urlparse(url).hostname in WIKI_HOSTS
    except Exception:
        return False

def localise_wikimedia():
    outdir=ROOT/"assets"/"editorial"/"culture"/"local"
    outdir.mkdir(parents=True,exist_ok=True)
    url_pat=re.compile(r'https://(?:commons|upload)\.wikimedia\.org/[^"\'<> )]+',re.I)
    seen={}
    changed=0
    downloaded=0

    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        urls=sorted(set(url_pat.findall(s)))
        if not urls: continue
        old=s
        for raw in urls:
            url=raw.replace("&amp;","&")
            if url in seen:
                local=seen[url]
            else:
                fetch_url=url
                if "commons.wikimedia.org/wiki/Special:Redirect/file/" in fetch_url and "?" not in fetch_url:
                    fetch_url += "?width=1600"
                req=Request(fetch_url,headers={"User-Agent":"Mametas/1.0 (editorial image localisation)"})
                with urlopen(req,timeout=45) as resp:
                    data=resp.read()
                    ctype=(resp.headers.get_content_type() or "").lower()
                if not data:
                    raise RuntimeError(f"Empty Wikimedia image: {url}")
                ext={ "image/jpeg":".jpg","image/png":".png","image/webp":".webp" }.get(ctype)
                if not ext:
                    ext=Path(urlparse(fetch_url).path).suffix.lower()
                    if ext not in {".jpg",".jpeg",".png",".webp"}: ext=".jpg"
                digest=hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
                dest=outdir/f"wiki-{digest}{ext}"
                if not dest.exists() or dest.stat().st_size != len(data):
                    dest.write_bytes(data); downloaded+=1
                local="/"+dest.relative_to(ROOT).as_posix()
                seen[url]=local
            s=s.replace(raw,local).replace(raw.replace("&","&amp;"),local)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("Wikimedia localisation:",downloaded,"files downloaded;",changed,"HTML files rewritten")
    return seen

def ensure_hreflang():
    cities=("cannes","antibes","beaulieu-sur-mer","monaco","menton","mougins",
            "saint-tropez","saint-paul-de-vence","villefranche-sur-mer")
    changed=0
    for city in cities:
        pairs=[
          (f"en/hotels/{city}/index.html",f"https://www.mametas.com/en/hotels/{city}/",f"https://www.mametas.com/hotels/{city}/"),
          (f"hotels/{city}/index.html",f"https://www.mametas.com/en/hotels/{city}/",f"https://www.mametas.com/hotels/{city}/"),
        ]
        for rel,en_url,fr_url in pairs:
            p=ROOT/rel
            if not p.exists(): continue
            s=p.read_text(encoding="utf-8",errors="ignore"); old=s
            needed=[
              f'<link rel="alternate" hreflang="en" href="{en_url}">',
              f'<link rel="alternate" hreflang="fr" href="{fr_url}">',
            ]
            insert="\n".join(x for x in needed if x not in s)
            if insert:
                s=s.replace("</head>",insert+"\n</head>",1)
            if s!=old:
                p.write_text(s,encoding="utf-8"); changed+=1
    print("hreflang fixed on",changed,"hotel-selection pages")

def wrong_language_and_small_parity():
    patches={
      "explore/2-3-heures/index.html":[("EXPLORE · 2-3 HOURS","EXPLORER · 2 À 3 HEURES")],
      "hotels/index.html":[("BEST FIT","MEILLEUR CHOIX"),("ALSO CONSIDER","À CONSIDÉRER AUSSI")],
      "en/culture/world-explorations-museum-cannes/index.html":[("Musée des explorations du monde","World Explorations Museum")],
      "en/culture/matisse-rosary-chapel/index.html":[("pour les œuvres de l’artiste","for the artist’s works"),("pour les oeuvres de l’artiste","for the artist’s works")],
    }
    # Beach pages: translate only the explicit French location labels Claude listed.
    en_beach={
      "en/beaches/antibes/index.html":{
        "SORTIE DU VIEIL ANTIBES VERS LE CAP":"LEAVING OLD ANTIBES TOWARDS THE CAP",
        "AU PIED DU CAP D’ANTIBES":"AT THE FOOT OF CAP D’ANTIBES",
        "AU PIED DU CAP D'ANTIBES":"AT THE FOOT OF CAP D’ANTIBES",
        "CÔTÉ OUEST":"WEST SIDE",
      },
      "en/beaches/saint-tropez/index.html":{
        "ENTRÉE DE SAINT-TROPEZ":"ENTRANCE TO SAINT-TROPEZ",
        "VIEILLE VILLE":"OLD TOWN",
        "SOUS LA CITADELLE":"BELOW THE CITADEL",
        "BAIE DES CANOUBIERS":"CANOUBIERS BAY",
        "À L’EST DU VILLAGE":"EAST OF THE VILLAGE",
        "À L'EST DU VILLAGE":"EAST OF THE VILLAGE",
        "BEACHES · SAINT TROPEZ":"BEACHES · SAINT-TROPEZ",
      },
      "en/good-finds/nice-carnival/index.html":{
        "ENTRE MASSÉNA ET LA PROMENADE":"BETWEEN MASSÉNA AND THE PROMENADE",
      }
    }
    for rel,reps in en_beach.items():
        patches.setdefault(rel,[]).extend(reps.items())

    changed=0
    for rel,reps in patches.items():
        p=ROOT/rel
        if not p.exists(): continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        for a,b in reps: s=s.replace(a,b)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1

    # Fondation Maeght FR: remove an empty "En ce moment" heading when it is
    # immediately followed by sources/verification content.
    p=ROOT/"culture/fondation-maeght/index.html"
    if p.exists():
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        s=re.sub(r'<h2[^>]*>\s*En ce moment\s*</h2>\s*(?=(?:<[^>]+>\s*){0,3}(?:Sources|Sources vérifiées|SOURCE|SOURCES))','',s,flags=re.I)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1

    # FR Riviera hub numbered decision grid: if generated upstream, restore
    # the missing 02 card without touching the older non-numbered hub.
    p=ROOT/"riviera-guide/index.html"
    if p.exists():
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        if "decision-grid" in s and "cote-dazur-ou-cote-amalfitaine" not in s:
            m=re.search(r'(<a class="decision-card"[^>]*>\s*<span class="decision-number">01</span>[\s\S]*?</a>)',s,re.I)
            if m:
                card=(
                  '<a class="decision-card" href="/riviera-guide/cote-dazur-ou-cote-amalfitaine/">'
                  '<span class="decision-number">02</span><h3>Côte d’Azur ou côte amalfitaine ?</h3>'
                  '<p>Train contre ferries, art contre falaises, improvisation facile contre carte postale très précise.</p>'
                  '<span class="text-link">Comparer →</span></a>'
                )
                s=s[:m.end()]+card+s[m.end():]
                # Renumber duplicate later cards conservatively.
                seen02=0
                def renum(mm):
                    nonlocal seen02
                    seen02+=1
                    if seen02==1: return mm.group(0)
                    return mm.group(0).replace('>02<','>03<').replace('>03<','>04<',1)
                # no broad renumbering here; existing numbers remain unless exactly missing sequence is obvious.
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1

    print("small parity/language patches changed",changed,"files")

def validate():
    remote=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        if "commons.wikimedia.org" in s or "upload.wikimedia.org" in s:
            remote.append(rel.as_posix())
    if remote:
        raise RuntimeError("Remote Wikimedia images survive: "+", ".join(remote[:30]))

    for city in ("cannes","antibes","beaulieu-sur-mer","monaco","menton","mougins","saint-tropez","saint-paul-de-vence","villefranche-sur-mer"):
        for rel in (f"en/hotels/{city}/index.html",f"hotels/{city}/index.html"):
            p=ROOT/rel
            if not p.exists(): continue
            s=p.read_text(encoding="utf-8",errors="ignore")
            if 'hreflang="en"' not in s or 'hreflang="fr"' not in s:
                raise RuntimeError("Missing hreflang after lot4A: "+rel)

    print("Claude final audit lot 4A validation passed.")

def main():
    localise_wikimedia()
    ensure_hreflang()
    wrong_language_and_small_parity()
    validate()

if __name__=="__main__":
    main()
