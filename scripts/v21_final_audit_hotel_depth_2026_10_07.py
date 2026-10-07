#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close Claude C15 hotel-depth gaps without inventing hotel facts.

For the eight short hotel pages, expose the existing editorial logic under the
same headings used by full pages, then add a source/date block. For the six
October-generated pages, ensure a visible Budget fact is present. Runs after
all hotel materialisation/enrichment and before final typography cleanup.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

SHORT={
 "antibes/hotel-la-place": {
   "source_en":"https://www.la-place-hotel.com/en","source_fr":"https://www.la-place-hotel.com/fr",
   "source_label_en":"Hôtel La Place, official site","source_label_fr":"Hôtel La Place, site officiel",
   "budget_en":"Mid-range","budget_fr":"Milieu de gamme",
 },
 "antibes/la-villa-port-antibes": {
   "source_en":"https://www.villa-port-antibes.com/","source_fr":"https://www.villa-port-antibes.com/fr/",
   "source_label_en":"La Villa Port d’Antibes, official site","source_label_fr":"La Villa Port d’Antibes, site officiel",
   "budget_en":"Upper mid-range","budget_fr":"Milieu de gamme supérieur",
 },
 "beaulieu-sur-mer/hotel-le-comte-de-nice": {
   "source_en":"https://www.hotel-comtedenice.com/","source_fr":"https://www.hotel-comtedenice.com/fr/",
   "source_label_en":"Hôtel Le Comte de Nice, official site","source_label_fr":"Hôtel Le Comte de Nice, site officiel",
   "budget_en":"Mid-range","budget_fr":"Milieu de gamme",
 },
 "menton/hotel-de-londres": {
   "source_en":"https://www.hotel-de-londres.com/","source_fr":"https://www.hotel-de-londres.com/fr/",
   "source_label_en":"Hôtel de Londres, official site","source_label_fr":"Hôtel de Londres, site officiel",
   "budget_en":"Mid-range","budget_fr":"Milieu de gamme",
 },
 "menton/hotel-napoleon": {
   "source_en":"https://www.napoleon-menton.com/en/","source_fr":"https://www.napoleon-menton.com/",
   "source_label_en":"Hôtel Napoléon, official site","source_label_fr":"Hôtel Napoléon, site officiel",
   "budget_en":"Upper mid-range","budget_fr":"Milieu de gamme supérieur",
 },
 "nice/boutique-hotel-nice-cote-dazur": {
   "source_en":"https://www.booking.com/hotel/fr/nice-cote-d-39-azur.en-gb.html",
   "source_fr":"https://www.booking.com/hotel/fr/nice-cote-d-39-azur.fr.html",
   "source_label_en":"Booking.com property listing","source_label_fr":"Fiche établissement Booking.com",
   "budget_en":"Mid-range","budget_fr":"Milieu de gamme",
 },
 "nice/villa-victoria": {
   "source_en":"https://villa-victoria.com/en/","source_fr":"https://villa-victoria.com/",
   "source_label_en":"Villa Victoria, official site","source_label_fr":"Villa Victoria, site officiel",
   "budget_en":"Mid-range","budget_fr":"Milieu de gamme",
 },
 "villefranche-sur-mer/welcome-hotel": {
   "source_en":"https://www.welcomehotel.com/en/","source_fr":"https://www.welcomehotel.com/",
   "source_label_en":"Welcome Hotel, official site","source_label_fr":"Welcome Hotel, site officiel",
   "budget_en":"High","budget_fr":"Haut de gamme",
 },
}

NEW_SERIES={
 "nice/hotel-windsor":("Comfort","Confort"),
 "nice/mercure-nice-centre-grimaldi":("Comfort","Confort"),
 "beaulieu-sur-mer/hotel-select":("Practical","Pratique"),
 "beaulieu-sur-mer/hotel-carlton":("Comfort","Confort"),
 "beaulieu-sur-mer/la-reserve-de-beaulieu":("Splurge","Très haut de gamme"),
 "menton/riva-art-spa":("Comfort","Confort"),
}

def visible(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).strip()

def ensure_budget(s,value):
    if re.search(r'>\s*Budget\s*<',s,re.I):
        return s
    # Prefer an existing fact-grid: append one fact before its closing tag.
    m=re.search(r'(<div class=["\'][^"\']*(?:hotel-facts|fact-grid)[^"\']*["\'][^>]*>)([\s\S]*?)(</div>\s*(?:<div class=["\']verdict|<h2))',s,re.I)
    if m:
        block=m.group(1)+m.group(2)+f'<div><span>Budget</span><b>{value}</b></div>'+m.group(3)
        return s[:m.start()]+block+s[m.end():]
    return s

def enrich_short(rel_base,cfg,fr):
    rel=("hotels/" if fr else "en/hotels/")+rel_base+"/index.html"
    p=ROOT/rel
    if not p.exists():
        print("skip missing",rel); return
    s=p.read_text(encoding="utf-8",errors="ignore"); old=s

    # Add semantic headings around the first two editorial paragraphs after the hero.
    # The paragraphs already carry the judgement; this only exposes the structure.
    marker='</figure>'
    pos=s.find(marker)
    if pos>=0:
        tail_start=pos+len(marker)
        tail=s[tail_start:]
        # Locate the first hotel-copy block after the hero.
        m=re.search(r'(<div class=["\']hotel-copy["\']>)([\s\S]*?)(</div>\s*(?:<section class=["\']hotel-gallery|<div class=["\']hotel-copy))',tail,re.I)
        if m:
            body=m.group(2)
            paras=list(re.finditer(r'<p(?:\s[^>]*)?>([\s\S]*?)</p>',body,re.I))
            if paras:
                if not re.search(r'<h2[^>]*>\s*(?:Who it suits|Pour qui)',body,re.I):
                    first=paras[0]
                    label="Pour qui" if fr else "Who it suits"
                    body=body[:first.start()]+f'<h2>{label}</h2>'+body[first.start():]
                # Recompute paragraphs after insertion and place Mèfi before second paragraph.
                paras=list(re.finditer(r'<p(?:\s[^>]*)?>([\s\S]*?)</p>',body,re.I))
                if len(paras)>=2 and "Mèfi" not in body:
                    second=paras[1]
                    label="Mèfi : le compromis" if fr else "Mèfi: the trade-off"
                    body=body[:second.start()]+f'<h2>{label}</h2>'+body[second.start():]
                new=m.group(1)+body+m.group(3)
                tail=tail[:m.start()]+new+tail[m.end():]
                s=s[:tail_start]+tail

    value=cfg["budget_fr" if fr else "budget_en"]
    s=ensure_budget(s,value)

    if "hotel-depth-sources" not in s:
        url=cfg["source_fr" if fr else "source_en"]
        label=cfg["source_label_fr" if fr else "source_label_en"]
        date="Vérifié le 7 octobre 2026" if fr else "Checked 7 October 2026"
        heading="Sources vérifiées" if fr else "Sources checked"
        source=f'''<div class="sources hotel-depth-sources"><p class="mametas-source-date">{date}</p><h2>{heading}</h2><ul><li><a href="{url}" target="_blank" rel="nofollow noopener">{label}</a></li></ul></div>'''
        # Put sources before the booking/affiliate block when possible.
        aff=re.search(r'<div class=["\']hotel-copy["\']>\s*<div class=["\']affiliate-cta',s,re.I)
        if aff:
            s=s[:aff.start()]+source+s[aff.start():]
        else:
            end=s.find("</article>")
            if end>=0: s=s[:end]+source+s[end:]

    if s!=old:
        p.write_text(s,encoding="utf-8"); print("enriched",rel)

def enrich_new_series(rel_base,vals,fr):
    rel=("hotels/" if fr else "en/hotels/")+rel_base+"/index.html"
    p=ROOT/rel
    if not p.exists():
        print("skip missing generated",rel); return
    s=p.read_text(encoding="utf-8",errors="ignore"); old=s
    s=ensure_budget(s,vals[1] if fr else vals[0])
    if s!=old:
        p.write_text(s,encoding="utf-8"); print("budget",rel)

def dedupe_hotel66():
    for rel in ("en/hotels/nice/hotel-66/index.html","hotels/nice/hotel-66/index.html"):
        p=ROOT/rel
        if not p.exists(): continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        # Keep first Mèfi heading; demote any later duplicate heading to a strong label.
        matches=list(re.finditer(r'<h2[^>]*>\s*Mèfi[^<]*</h2>',s,re.I))
        if len(matches)>1:
            offset=0
            for m in matches[1:]:
                a=m.start()+offset; b=m.end()+offset
                txt=re.sub(r'<[^>]+>','',s[a:b]).strip()
                repl=f'<p class="hotel-sub-label"><strong>{txt}</strong></p>'
                s=s[:a]+repl+s[b:]
                offset+=len(repl)-(b-a)
        if s!=old:
            p.write_text(s,encoding="utf-8"); print("deduped",rel)

def validate():
    bad=[]
    for base,cfg in SHORT.items():
        for fr in (False,True):
            rel=("hotels/" if fr else "en/hotels/")+base+"/index.html"
            p=ROOT/rel
            if not p.exists(): continue
            t=visible(p.read_text(encoding="utf-8",errors="ignore")).lower()
            checks=[
              ("who",("pour qui" in t) if fr else ("who it suits" in t)),
              ("mefi","mèfi" in t),
              ("sources",("sources vérifiées" in t) if fr else ("sources checked" in t)),
              ("checked",("vérifié le 7 octobre 2026" in t) if fr else ("checked 7 october 2026" in t)),
              ("budget","budget" in t),
            ]
            missing=[k for k,v in checks if not v]
            if missing: bad.append(f"{rel}: {missing}")
    for base,vals in NEW_SERIES.items():
        for fr in (False,True):
            rel=("hotels/" if fr else "en/hotels/")+base+"/index.html"
            p=ROOT/rel
            if p.exists() and "budget" not in visible(p.read_text(encoding="utf-8",errors="ignore")).lower():
                bad.append(rel+": budget")
    if bad:
        raise RuntimeError("Hotel depth gaps survive: "+" | ".join(bad[:30]))
    print("Claude C15 hotel-depth validation passed.")

def main():
    for base,cfg in SHORT.items():
        enrich_short(base,cfg,False); enrich_short(base,cfg,True)
    for base,vals in NEW_SERIES.items():
        enrich_new_series(base,vals,False); enrich_new_series(base,vals,True)
    dedupe_hotel66()
    validate()

if __name__=="__main__":
    main()
