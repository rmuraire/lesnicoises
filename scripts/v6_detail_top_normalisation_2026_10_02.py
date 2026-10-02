#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

PAGES={
'en/explore/french-riviera-honeymoon/index.html':('/en/explore/','← Back to Explore','FRENCH RIVIERA · HONEYMOON'),
'explore/lune-de-miel-cote-d-azur/index.html':('/explore/','← Retour à Explorer','CÔTE D’AZUR · LUNE DE MIEL'),
'en/explore/french-riviera-babymoon/index.html':('/en/explore/','← Back to Explore','FRENCH RIVIERA · BABYMOON'),
'explore/babymoon-cote-d-azur/index.html':('/explore/','← Retour à Explorer','CÔTE D’AZUR · BABYMOON'),
'en/explore/french-riviera-proposal/index.html':('/en/explore/','← Back to Explore','FRENCH RIVIERA · PROPOSAL'),
'explore/demande-en-mariage-cote-d-azur/index.html':('/explore/','← Retour à Explorer','CÔTE D’AZUR · DEMANDE EN MARIAGE'),
'en/explore/living-antibes-expat/index.html':('/en/explore/','← Back to Explore','FRENCH RIVIERA · EXPAT'),
'explore/vivre-antibes-expatrie/index.html':('/explore/','← Retour à Explorer','CÔTE D’AZUR · EXPATRIATION'),
'en/explore/retire-french-riviera/index.html':('/en/explore/','← Back to Explore','FRENCH RIVIERA · RETIREMENT'),
'explore/retraite-cote-d-azur/index.html':('/explore/','← Retour à Explorer','CÔTE D’AZUR · RETRAITE'),
'en/good-finds/nice-airport-transfer/index.html':('/en/practical/','← Back to Practical','PRACTICAL · AIRPORT'),
'bons-plans/transfert-aeroport-nice/index.html':('/pratique/','← Retour à Pratique','PRATIQUE · AÉROPORT'),
'en/good-finds/train-or-bus/index.html':('/en/practical/','← Back to Practical','PRACTICAL · TRAIN OR BUS'),
'bons-plans/train-ou-bus/index.html':('/pratique/','← Retour à Pratique','PRATIQUE · TRAIN OU BUS'),
'en/good-finds/what-to-book/index.html':('/en/practical/','← Back to Practical','PRACTICAL · WHAT TO BOOK'),
'bons-plans/que-reserver/index.html':('/pratique/','← Retour à Pratique','PRATIQUE · QUE RÉSERVER'),
'en/good-finds/nice-in-the-rain/index.html':('/en/practical/','← Back to Practical','PRACTICAL · RAIN'),
'bons-plans/nice-quand-il-pleut/index.html':('/pratique/','← Retour à Pratique','PRATIQUE · PLUIE'),
'en/beaches/nice/index.html':('/en/beaches/','← Back to beaches','BEACHES · NICE'),
'plages/nice/index.html':('/plages/','← Retour aux plages','PLAGES · NICE'),
'en/beaches/around-nice/index.html':('/en/beaches/','← Back to beaches','BEACHES · AROUND NICE'),
'plages/autour-de-nice/index.html':('/plages/','← Retour aux plages','PLAGES · AUTOUR DE NICE'),
'en/riviera-guide/nice-or-cannes/index.html':('/en/riviera-guide/','← Back to Places','COMPARISON · NICE OR CANNES'),
'riviera-guide/nice-ou-cannes/index.html':('/riviera-guide/','← Retour aux destinations','COMPARATIF · NICE OU CANNES'),
'en/hotels/beaulieu-sur-mer/hotel-select/index.html':('/en/hotels/beaulieu-sur-mer/','← Back to Beaulieu-sur-Mer hotels','HOTEL · BEAULIEU-SUR-MER'),
'hotels/beaulieu-sur-mer/hotel-select/index.html':('/hotels/beaulieu-sur-mer/','← Retour aux hôtels de Beaulieu-sur-Mer','HÔTEL · BEAULIEU-SUR-MER'),
'en/hotels/nice/hotel-windsor/index.html':('/stay/nice/','← Back to Nice hotels','HOTEL · NICE'),
'hotels/nice/hotel-windsor/index.html':('/fr/dormir/nice/','← Retour aux hôtels de Nice','HÔTEL · NICE'),
'en/hotels/beaulieu-sur-mer/la-reserve-de-beaulieu/index.html':('/en/hotels/beaulieu-sur-mer/','← Back to Beaulieu-sur-Mer hotels','HOTEL · BEAULIEU-SUR-MER'),
'hotels/beaulieu-sur-mer/la-reserve-de-beaulieu/index.html':('/hotels/beaulieu-sur-mer/','← Retour aux hôtels de Beaulieu-sur-Mer','HÔTEL · BEAULIEU-SUR-MER'),
'en/hotels/menton/riva-art-spa/index.html':('/en/hotels/menton/','← Back to Menton hotels','HOTEL · MENTON'),
'hotels/menton/riva-art-spa/index.html':('/hotels/menton/','← Retour aux hôtels de Menton','HÔTEL · MENTON'),
'en/hotels/nice/mercure-nice-centre-grimaldi/index.html':('/stay/nice/','← Back to Nice hotels','HOTEL · NICE'),
'hotels/nice/mercure-nice-centre-grimaldi/index.html':('/fr/dormir/nice/','← Retour aux hôtels de Nice','HÔTEL · NICE'),
}

HOTEL_TAKES={p for p in PAGES if '/hotels/' in p and any(x in p for x in ['hotel-select','hotel-windsor','la-reserve-de-beaulieu','riva-art-spa','mercure-nice-centre-grimaldi'])}

def patch_top(text,back_href,back_text,eyebrow):
    if re.search(r'<p class="breadcrumbs">.*?</p>',text,re.S):
        text=re.sub(r'<p class="breadcrumbs">.*?</p>',f'<a class="back" href="{back_href}">{back_text}</a>',text,count=1,flags=re.S)
    elif re.search(r'<a class="back"[^>]*>.*?</a>',text,re.S):
        text=re.sub(r'<a class="back"[^>]*>.*?</a>',f'<a class="back" href="{back_href}">{back_text}</a>',text,count=1,flags=re.S)
    else:
        m=re.search(r'<(?:header class="article-hero"><div class="wrap"|article\b[^>]*>)',text,re.I)
        if not m: raise RuntimeError('cannot place back link')
        text=text[:m.end()]+f'<a class="back" href="{back_href}">{back_text}</a>'+text[m.end():]

    candidates=[
        (r'<div class="meta">.*?</div>',f'<p class="eyebrow">{eyebrow}</p>'),
        (r'<p class="meta">.*?</p>',f'<p class="eyebrow">{eyebrow}</p>'),
        (r'<p class="eyebrow">.*?</p>',f'<p class="eyebrow">{eyebrow}</p>'),
    ]
    for patt,repl in candidates:
        if re.search(patt,text,re.S):
            text=re.sub(patt,repl,text,count=1,flags=re.S); break
    else:
        text,n=re.subn(r'(<h1\b)',f'<p class="eyebrow">{eyebrow}</p>\\1',text,count=1,flags=re.I)
        if n!=1: raise RuntimeError('H1 not found for eyebrow')
    return text

def patch_hotel_take(text,fr):
    if fr:
        text=text.replace('<span class="label">TARIFS</span><h2>Vérifiez vos dates</h2>','<span class="label">RÉSERVER</span><h2>Voir les tarifs ?</h2>')
        text=text.replace('<span class="label">TARIFS</span><h2>Vérifier vos dates</h2>','<span class="label">RÉSERVER</span><h2>Voir les tarifs ?</h2>')
    else:
        text=text.replace('<span class="label">RATES</span><h2>Check your dates</h2>','<span class="label">BOOK</span><h2>Want to check the rates?</h2>')
    return text

def main():
    changed=0
    for rel,(href,label,eyebrow) in PAGES.items():
        p=ROOT/rel
        if not p.exists(): raise RuntimeError(f'missing {rel}')
        s=p.read_text(encoding='utf-8',errors='ignore'); before=s
        s=patch_top(s,href,label,eyebrow)
        if rel in HOTEL_TAKES:
            s=patch_hotel_take(s,not rel.startswith('en/'))
        if s!=before:
            p.write_text(s,encoding='utf-8'); changed+=1
    for rel in ['en/beaches/nice/index.html','en/day-trips/nice-to-menton-by-train/index.html']:
        p=ROOT/rel
        if not p.exists(): continue
        s=p.read_text(encoding='utf-8',errors='ignore'); before=s
        s=s.replace('Nice : the beaches','Nice: the beaches').replace('train : the day trip','train: the day trip').replace('Option 1 :','Option 1:').replace('Option 2 :','Option 2:')
        s=s.replace('secret beach, . It is','secret beach. It is')
        if s!=before: p.write_text(s,encoding='utf-8'); changed+=1
    print('V6 detail-top normalization updated',changed,'files')

if __name__=='__main__': main()
