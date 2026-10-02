#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
DESTS={
 'nice':'Nice','villefranche-cap-ferrat':'Villefranche & Cap-Ferrat','antibes':'Antibes','cannes':'Cannes',
 'monaco':'Monaco','menton':'Menton','eze':'Èze','saint-paul-de-vence':'Saint-Paul-de-Vence','saint-tropez':'Saint-Tropez',
}
errors=[]
for slug,city in DESTS.items():
  for lang,rel in [('en',f'en/riviera-guide/{slug}/index.html'),('fr',f'riviera-guide/{slug}/index.html')]:
    p=ROOT/rel
    if not p.exists(): errors.append(f'{rel}: missing'); continue
    s=p.read_text(encoding='utf-8',errors='ignore')
    body=re.search(r'<body\b[^>]*>',s,re.I)
    back_href='/en/riviera-guide/' if lang=='en' else '/riviera-guide/'
    back_text='← Back to Places' if lang=='en' else '← Retour aux destinations'
    eyebrow=('PLACES · '+city) if lang=='en' else ('DESTINATIONS · '+city)
    labels=['Getting around','Budget','Season','Logistics'] if lang=='en' else ['Déplacements','Budget','Saison','Logistique']
    cta_href='/en/riviera-fit/' if lang=='en' else '/riviera-fit/'
    cta='Run my profile through Riviera Fit →' if lang=='en' else 'Tester mon profil dans Riviera Fit →'
    checks=[
      (body is not None and 'destination-canonical' in body.group(0),'canonical body class'),
      (s.count('/assets/mametas-destination-v1.css?v=1.0')==1,'destination CSS'),
      (s.count(f'<a class="back" href="{back_href}">{back_text}</a>')==1,'canonical back link'),
      (s.count(f'<p class="eyebrow">{eyebrow}</p>')==1,'canonical eyebrow'),
      ('class="breadcrumbs"' not in s,'legacy breadcrumb removed'),
      ('class="article-meta"' not in s,'legacy top facts removed'),
      (s.count('data-destination-reality="true"')==1,'one Reality Check'),
      (s.count('class="mametas-checked"')==1,'one Mametas Checked badge'),
      (s.find('data-destination-reality="true"') < s.find('class="mametas-checked"'),'Reality Check before Checked badge'),
      (f'href="{cta_href}">{cta}</a>' in s,'canonical Riviera Fit CTA'),
      (len(re.findall(r'<h1\b',s))==1,'one H1'),
    ]
    m=re.search(r'<section class="destination-reality" data-destination-reality="true">(.*?)</section>',s,re.S)
    if m:
      got=re.findall(r'<b>(.*?)</b>',m.group(1),re.S)
      checks.append((got==labels,f'Reality Check labels {got!r}'))
      if lang=='en':
        checks.append(('Mobility' not in m.group(1) and 'Budget pressure' not in m.group(1) and '>Friction<' not in m.group(1),'legacy EN labels removed'))
      else:
        checks.append(('Mobilité' not in m.group(1) and 'Pression budget' not in m.group(1) and '>Friction<' not in m.group(1),'legacy FR labels removed'))
    if slug=='eze':
      checks.append((s.count('class="destination-mefi"')==1,'Èze Mèfi'))
    if lang=='fr' and slug=='saint-paul-de-vence':
      checks.append(('ville intérieure' not in s and 'base intérieure' not in s,'Saint-Paul wording'))
    for ok,label in checks:
      if not ok: errors.append(f'{rel}: {label}')

if errors:
  print('V6 destination validation failed:')
  for e in errors: print(' -',e)
  raise SystemExit(1)
print('V6 destination validation passed: 18 pages')
