#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
CSS='/assets/mametas-city-card-v1.css?v=1.0'
ORDER_BASE=['nice','villefranche-cap-ferrat','antibes','cannes','monaco','menton']
ORDER_DETOUR=['eze','saint-paul-de-vence','saint-tropez']

DATA={
'nice':{
 'img':'/assets/editorial/depositphotos/nice-pratique/nice-castle-hill-bay.webp','alt':('Nice','Nice'),
 'name':('Nice','Nice'),'tag':('Best first base','Meilleur premier point de chute'),
 'desc':('Trains, restaurants, culture and a real city after dinner.','Trains, restaurants, culture et une vraie ville après dîner.'),
 'mob':('No car needed for a first trip','Pas de voiture nécessaire pour un premier séjour')},
'villefranche-cap-ferrat':{
 'img':'/assets/editorial/villefranche.jpg','alt':('Villefranche-sur-Mer','Villefranche-sur-Mer'),
 'name':('Villefranche & Cap-Ferrat','Villefranche & Cap-Ferrat'),'tag':('Best for beauty','Pour la beauté'),
 'desc':('A spectacular bay, slower pace and Cap-Ferrat on the doorstep.','Une rade spectaculaire, un rythme plus lent et le Cap-Ferrat à portée de main.'),
 'mob':('Car-free works, less seamlessly than Nice','Sans voiture, oui ; moins fluide qu’à Nice')},
'antibes':{
 'img':'/assets/editorial/antibes-gravette.jpg','alt':('Antibes','Antibes'),
 'name':('Antibes','Antibes'),'tag':('Best balance','Meilleur équilibre'),
 'desc':('Old town, sand and useful trains, with the Cap as a second act.','Vieille ville, sable et trains utiles, avec le Cap en deuxième acte.'),
 'mob':('Car-free in town; the Cap asks for more','Sans voiture en ville ; le Cap demande plus')},
'cannes':{
 'img':'/assets/editorial/cannes-suquet-harbour.jpg','alt':('Cannes','Cannes'),
 'name':('Cannes','Cannes'),'tag':('Best for polish','Pour le vernis'),
 'desc':('Compact, sandy and polished, with the hotel often part of the holiday.','Compacte, sableuse et soignée, avec l’hôtel souvent au cœur du séjour.'),
 'mob':('Very easy without a car','Très simple sans voiture')},
'monaco':{
 'img':'/assets/editorial/monaco-harbour.jpg','alt':('Monaco','Monaco'),
 'name':('Monaco','Monaco'),'tag':('Best for spectacle','Pour le spectacle'),
 'desc':('A dramatic city-state where spectacle matters more than value.','Une cité-État spectaculaire où l’effet compte plus que le rapport qualité-prix.'),
 'mob':('No car recommended','Sans voiture recommandé')},
'menton':{
 'img':'/assets/editorial/menton-day.jpg','alt':('Menton','Menton'),
 'name':('Menton','Menton'),'tag':('Best for a slower east','Pour l’est plus calme'),
 'desc':('Softer, slower and almost Italian on the quiet eastern edge.','Plus douce, plus lente, presque italienne, tout à l’est de la côte.'),
 'mob':('Very good without a car','Très bon sans voiture')},
'eze':{
 'img':'/assets/editorial/eze-village.jpg','alt':('Èze','Èze'),
 'name':('Èze','Èze'),'tag':('Best for the panorama','Pour le panorama'),
 'desc':('Hilltop panorama, crowds and logistics: a detour worth planning.','Panorama perché, foule et logistique : un détour qui se prépare.'),
 'mob':('Bus to the village; train to Èze-sur-Mer','Bus pour le village ; train pour Èze-sur-Mer')},
'saint-paul-de-vence':{
 'img':'/assets/editorial/saint-paul-de-vence.jpg','alt':('Saint-Paul-de-Vence','Saint-Paul-de-Vence'),
 'name':('Saint-Paul-de-Vence','Saint-Paul-de-Vence'),'tag':('Best for art inland','Pour l’art dans les terres'),
 'desc':('Art, stone and an inland pause away from the coastal rhythm.','Art, pierre et une pause dans les terres loin du rythme côtier.'),
 'mob':('A car is useful; bus is possible','Voiture utile ; bus possible')},
'saint-tropez':{
 'img':'/assets/editorial/saint-tropez.jpg','alt':('Saint-Tropez','Saint-Tropez'),
 'name':('Saint-Tropez','Saint-Tropez'),'tag':('Only if you really want it','Quand vous le voulez vraiment'),
 'desc':('A deliberate expedition when Saint-Tropez itself is the destination.','Une vraie expédition quand Saint-Tropez est la destination.'),
 'mob':('Car, boat or transfers need planning','Voiture, bateau ou transferts à organiser')},
}

def inject_css(text):
    text=re.sub(r'<link[^>]+href=["\']/assets/mametas-city-card-v1\.css(?:\?v=[^"\']*)?["\'][^>]*>\s*','',text,flags=re.I)
    i=text.lower().rfind('</head>')
    if i<0: raise RuntimeError('head close missing')
    return text[:i]+f'<link rel="stylesheet" href="{CSS}">\n'+text[i:]

def href(lang,key):
    return ('/en/riviera-guide/' if lang=='en' else '/riviera-guide/')+key+'/'

def card(lang,key):
    d=DATA[key]; idx=0 if lang=='en' else 1
    cta='See the guide →' if lang=='en' else 'Voir le guide →'
    return (
      f'<a class="mametas-city-card" data-city-card="{key}" href="{href(lang,key)}">'
      f'<span class="mametas-city-card-media"><img src="{d["img"]}" alt="{d["alt"][idx]}" loading="lazy"></span>'
      f'<span class="mametas-city-card-copy"><small>{d["tag"][idx]}</small><strong>{d["name"][idx]}</strong>'
      f'<span class="mametas-city-card-description">{d["desc"][idx]}</span>'
      f'<span class="mametas-city-card-mobility">{d["mob"][idx]}</span>'
      f'<span class="mametas-city-card-cta">{cta}</span></span></a>'
    )

def replace_place_cards(text,lang):
    for key in DATA:
        h=re.escape(href(lang,key))
        patt=re.compile(r'<a class="place-card" href="'+h+r'">.*?</a>',re.S)
        text,n=patt.subn(card(lang,key),text,count=1)
        if n!=1:
            raise RuntimeError(f'Places card not found exactly once: {lang} {key}')
    return text

def home_base_grid(lang):
    return '<div class="mametas-city-grid mametas-city-grid--bases" id="places">'+''.join(card(lang,k) for k in ORDER_BASE)+'</div>'

def home_detours(lang):
    if lang=='en':
        eyebrow='Beyond your base'; title='Don’t collect the Riviera. Choose it.'
        intro='Once your base is sorted, choose the detour that changes the mood rather than adding another pin.'
    else:
        eyebrow='Au-delà du point de chute'; title='Ne collectionnez pas la Riviera. Choisissez-la.'
        intro='Une fois le point de chute choisi, gardez le détour qui change vraiment l’ambiance au lieu d’ajouter une épingle.'
    return (f'<section class="v3-section home-city-detours" data-home-city-detours="true"><div class="wrap">'
            f'<div class="section-heading"><div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div><p>{intro}</p></div>'
            f'<div class="mametas-city-grid mametas-city-grid--detours">'+''.join(card(lang,k) for k in ORDER_DETOUR)+'</div></div></section>')

def patch_home(path,lang):
    text=inject_css(path.read_text(encoding='utf-8'))
    markers=['<div class="base-grid" id="places">','<div class="base-grid" id="lieux">']
    starts=[text.find(m) for m in markers if text.find(m)>=0]
    start=min(starts) if starts else -1
    end=text.find('<div class="wrap home-section-tail">',start)
    if start<0 or end<0: raise RuntimeError(f'{path}: home base grid markers missing')
    text=text[:start]+home_base_grid(lang)+text[end:]
    if lang=='en':
        marker='<p class="eyebrow">Beyond your base</p>'
        i=text.find(marker)
        if i<0: raise RuntimeError('EN detour section missing')
        sec_start=text.rfind('<section class="v3-section">',0,i)
        sec_end=text.find('</section>',i)
        if sec_start<0 or sec_end<0: raise RuntimeError('EN detour bounds missing')
        text=text[:sec_start]+home_detours(lang)+text[sec_end+10:]
    else:
        if text.find('data-home-city-detours="true"')<0:
            insert=text.find('<section class="v3-section home-experiences"')
            if insert<0: raise RuntimeError('FR home experiences marker missing')
            text=text[:insert]+home_detours(lang)+'\n'+text[insert:]
    path.write_text(text,encoding='utf-8')

def main():
    for lang,rel in [('en','en/riviera-guide/index.html'),('fr','riviera-guide/index.html')]:
        p=ROOT/rel
        t=inject_css(p.read_text(encoding='utf-8'))
        t=replace_place_cards(t,lang)
        p.write_text(t,encoding='utf-8')
    patch_home(ROOT/'index.html','en')
    patch_home(ROOT/'fr/index.html','fr')
    print('V6 city card normalization passed: home + Places EN/FR')

if __name__=='__main__':
    main()
