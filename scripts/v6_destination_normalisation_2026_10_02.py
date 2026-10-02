#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[1]
CSS='/assets/mametas-destination-v1.css?v=1.0'

DESTS={
 'nice':('Nice','Nice'),
 'villefranche-cap-ferrat':('Villefranche & Cap-Ferrat','Villefranche & Cap-Ferrat'),
 'antibes':('Antibes','Antibes'),
 'cannes':('Cannes','Cannes'),
 'monaco':('Monaco','Monaco'),
 'menton':('Menton','Menton'),
 'eze':('Èze','Èze'),
 'saint-paul-de-vence':('Saint-Paul-de-Vence','Saint-Paul-de-Vence'),
 'saint-tropez':('Saint-Tropez','Saint-Tropez'),
}

EZE_RC={
 'en':('Bus to the village; the train stops at Èze-sur-Mer','€€ to €€€€','Year-round; busiest in high summer','High: Èze-sur-Mer and Èze Village are not the same stop'),
 'fr':('Bus direct pour le village ; le train s’arrête à Èze-sur-Mer','€€ à €€€€','Toute l’année ; plus tendu en plein été','Élevée : Èze-sur-Mer et Èze Village ne sont pas le même arrêt'),
}

def add_body_class(text):
    m=re.search(r'<body\b([^>]*)>',text,re.I)
    if not m: raise RuntimeError('body missing')
    tag=m.group(0)
    if 'destination-canonical' in tag: return text
    cm=re.search(r'class=["\']([^"\']*)["\']',tag,re.I)
    if cm:
        new=tag[:cm.start(1)]+cm.group(1)+' destination-canonical'+tag[cm.end(1):]
    else:
        new=tag[:-1]+' class="destination-canonical">'
    return text[:m.start()]+new+text[m.end():]

def inject_css(text):
    text=re.sub(r'<link[^>]+href=["\']/assets/mametas-destination-v1\.css(?:\?v=[^"\']*)?["\'][^>]*>\s*','',text,flags=re.I)
    i=text.lower().rfind('</head>')
    if i<0: raise RuntimeError('head close missing')
    return text[:i]+f'<link rel="stylesheet" href="{CSS}">\n'+text[i:]

def rc_block(lang):
    vals=EZE_RC[lang]
    labels=('Getting around','Budget','Season','Logistics') if lang=='en' else ('Déplacements','Budget','Saison','Logistique')
    head=('REALITY CHECK','What this choice really implies') if lang=='en' else ('À SAVOIR','Ce que ce choix implique vraiment')
    href='/en/riviera-fit/' if lang=='en' else '/riviera-fit/'
    cta='Run my profile through Riviera Fit →' if lang=='en' else 'Tester mon profil dans Riviera Fit →'
    cells=''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in zip(labels,vals))
    return f'<section class="destination-reality" data-destination-reality="true"><div class="destination-reality-head"><span>{head[0]}</span><strong>{head[1]}</strong></div><div class="destination-reality-grid">{cells}</div><div class="destination-reality-cta"><a href="{href}">{cta}</a></div></section>'

def normalize_rc(section,lang):
    labels=('Getting around','Budget','Season','Logistics') if lang=='en' else ('Déplacements','Budget','Saison','Logistique')
    head=('REALITY CHECK','What this choice really implies') if lang=='en' else ('À SAVOIR','Ce que ce choix implique vraiment')
    href='/en/riviera-fit/' if lang=='en' else '/riviera-fit/'
    cta='Run my profile through Riviera Fit →' if lang=='en' else 'Tester mon profil dans Riviera Fit →'
    section=re.sub(r'(<div class="destination-reality-head"><span>).*?(</span><strong>).*?(</strong></div>)',lambda m:m.group(1)+head[0]+m.group(2)+head[1]+m.group(3),section,count=1,flags=re.S)
    i=0
    def repl(m):
        nonlocal i
        label=labels[i] if i<len(labels) else m.group(1)
        i+=1
        return '<b>'+label+'</b>'
    section=re.sub(r'<b>.*?</b>',repl,section,flags=re.S)
    section=re.sub(r'<div class="destination-reality-cta">.*?</div>',f'<div class="destination-reality-cta"><a href="{href}">{cta}</a></div>',section,count=1,flags=re.S)
    if lang=='fr':
        section=section.replace('Moyenne à élevée : ville intérieure','Moyenne à élevée : dans les terres').replace('Moyenne à élevée : base intérieure','Moyenne à élevée : dans les terres')
    return section

def canonical_top(text,lang,city):
    back_href='/en/riviera-guide/' if lang=='en' else '/riviera-guide/'
    back_text='← Back to Places' if lang=='en' else '← Retour aux destinations'
    eyebrow=('PLACES · '+city) if lang=='en' else ('DESTINATIONS · '+city)
    text=re.sub(r'<p class="breadcrumbs">.*?</p>',f'<a class="back" href="{back_href}">{back_text}</a>',text,count=1,flags=re.S)
    text=re.sub(r'<a class="back"[^>]*>.*?</a>',f'<a class="back" href="{back_href}">{back_text}</a>',text,count=1,flags=re.S)
    if re.search(r'<div class="meta">.*?</div>',text,re.S):
        text=re.sub(r'<div class="meta">.*?</div>',f'<p class="eyebrow">{eyebrow}</p>',text,count=1,flags=re.S)
    else:
        text=re.sub(r'<p class="eyebrow">.*?</p>',f'<p class="eyebrow">{eyebrow}</p>',text,count=1,flags=re.S)
    text=re.sub(r'<div class="article-meta">.*?</div>','',text,count=1,flags=re.S)
    return text

def patch_page(path,lang,slug,city):
    text=path.read_text(encoding='utf-8')
    text=inject_css(add_body_class(text))
    text=canonical_top(text,lang,city)
    m=re.search(r'<section class="destination-reality" data-destination-reality="true">.*?</section>',text,re.S)
    if m:
        normalized=normalize_rc(m.group(0),lang)
        text=text[:m.start()]+normalized+text[m.end():]
    elif slug=='eze':
        badge=re.search(r'<a class="mametas-checked"[^>]*>.*?</a>',text,re.S)
        if not badge: raise RuntimeError(f'{path}: badge missing')
        block=rc_block(lang)
        text=text[:badge.start()]+block+text[badge.start():]
    else:
        raise RuntimeError(f'{path}: Reality Check missing')

    patt=re.compile(r'(<a class="mametas-checked"[^>]*>.*?</a>)\s*(<section class="destination-reality" data-destination-reality="true">.*?</section>)',re.S)
    text=patt.sub(lambda m:m.group(2)+m.group(1),text,count=1)

    if slug=='eze':
        dp=re.search(r'<div class="destination-practical">(.*?)</div>\s*(?=<div class="fact-grid">)',text,re.S)
        if dp:
            inner=dp.group(1)
            first=re.search(r'<div><b>(.*?)</b><span>(.*?)</span></div>',inner,re.S)
            if first:
                label_text=re.sub(r'<[^>]+>',' ',first.group(1))
                label_text=html.unescape(re.sub(r'\s+',' ',label_text)).strip()
                if not ('important' in label_text.lower() or 'mèfi' in label_text.lower()):
                    first=None
            if first:
                warning=re.sub(r'<[^>]+>',' ',first.group(2))
                warning=html.unescape(re.sub(r'\s+',' ',warning)).strip()
                mefi=f'<div class="destination-mefi"><strong>Mèfi.</strong><p>{html.escape(warning, quote=False)}</p></div>'
                inner=inner[:first.start()]+inner[first.end():]
                replacement='<div class="destination-practical">'+inner+'</div>'
                text=text[:dp.start()]+replacement+text[dp.end():]
                rc=re.search(r'<section class="destination-reality" data-destination-reality="true">.*?</section>',text,re.S)
                if rc and 'class="destination-mefi"' not in text:
                    text=text[:rc.end()]+mefi+text[rc.end():]
    if slug=='eze':
        if lang=='en':
            text=text.replace('<b>A very specific base</b>', '<b>Usually a detour, not a base</b>')
        else:
            text=text.replace('<b>Ville très spécifique</b>', '<b>Plutôt un détour qu’un point de chute</b>')
            text=text.replace('<b>Une ville très spécifique</b>', '<b>Plutôt un détour qu’un point de chute</b>')
            text=text.replace('<b>Un point de chute très spécifique</b>', '<b>Plutôt un détour qu’un point de chute</b>')
    if lang=='en' and slug=='nice':
        text=text.replace('did not wait for you to exist, . Remember','did not wait for you to exist. Remember')
    path.write_text(text,encoding='utf-8')

def main():
    changed=0
    for slug,(en_city,fr_city) in DESTS.items():
        for lang,city,rel in (
            ('en',en_city,f'en/riviera-guide/{slug}/index.html'),
            ('fr',fr_city,f'riviera-guide/{slug}/index.html'),
        ):
            p=ROOT/rel
            if not p.exists(): raise RuntimeError(f'missing {rel}')
            patch_page(p,lang,slug,city); changed+=1
    print('V6 destination normalisation patched',changed,'pages')

if __name__=='__main__':
    main()
