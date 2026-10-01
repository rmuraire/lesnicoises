# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]
pairs = [
('en/explore/french-riviera-honeymoon/index.html','/en/explore/french-riviera-honeymoon/','/explore/lune-de-miel-cote-d-azur/'),
('explore/lune-de-miel-cote-d-azur/index.html','/explore/lune-de-miel-cote-d-azur/','/en/explore/french-riviera-honeymoon/'),
('en/explore/french-riviera-babymoon/index.html','/en/explore/french-riviera-babymoon/','/explore/babymoon-cote-d-azur/'),
('explore/babymoon-cote-d-azur/index.html','/explore/babymoon-cote-d-azur/','/en/explore/french-riviera-babymoon/'),
('en/explore/french-riviera-proposal/index.html','/en/explore/french-riviera-proposal/','/explore/demande-en-mariage-cote-d-azur/'),
('explore/demande-en-mariage-cote-d-azur/index.html','/explore/demande-en-mariage-cote-d-azur/','/en/explore/french-riviera-proposal/'),
('en/explore/living-antibes-expat/index.html','/en/explore/living-antibes-expat/','/explore/vivre-antibes-expatrie/'),
('explore/vivre-antibes-expatrie/index.html','/explore/vivre-antibes-expatrie/','/en/explore/living-antibes-expat/'),
('en/explore/retire-french-riviera/index.html','/en/explore/retire-french-riviera/','/explore/retraite-cote-d-azur/'),
('explore/retraite-cote-d-azur/index.html','/explore/retraite-cote-d-azur/','/en/explore/retire-french-riviera/'),
]
errors=[]
for rel, route, alt in pairs:
    p=ROOT/rel
    if not p.exists():
        errors.append(f'missing {rel}'); continue
    s=p.read_text(encoding='utf-8')
    required=[
      '<header class="v3-header">','class="mobile-menu"','class="v3-footer"',
      'Mametas Checked',f'https://www.mametas.com{route}',f'https://www.mametas.com{alt}',
      '<div class="sources">','data-dense-v2="true"','class="intent-table"',
      '"@type":"FAQPage"','class="intent-faq"'
    ]
    for token in required:
        if token not in s: errors.append(f'{rel}: missing {token}')
    if len(re.findall(r'<h1\b',s)) != 1: errors.append(f'{rel}: h1 count')
    if len(re.findall(r'rel="alternate"',s)) != 3: errors.append(f'{rel}: hreflang count')
    title=re.search(r'<title>(.*?)</title>',s,re.S)
    desc=re.search(r'<meta name="description" content="([^"]+)"',s)
    if not title or len(title.group(1))>65: errors.append(f'{rel}: title length')
    if not desc or len(desc.group(1))>160: errors.append(f'{rel}: description length')
    if s.count('target="_blank" rel="nofollow noopener"') < 3: errors.append(f'{rel}: too few checked sources')
    if s.count('data-dense-v2="true"') != 1: errors.append(f'{rel}: dense block count')
    if s.count('class="intent-table"') < 1: errors.append(f'{rel}: no signature table')
    if s.count('<details>') < 6: errors.append(f'{rel}: fewer than 6 FAQ items')
    scripts=re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
    faq_ok=False
    for raw in scripts:
        try:
            obj=json.loads(raw)
            if obj.get('@type')=='FAQPage' and len(obj.get('mainEntity',[]))>=6:
                faq_ok=True
        except Exception:
            pass
    if not faq_ok: errors.append(f'{rel}: invalid FAQPage schema')
    if s.count('<table') != s.count('</table>'): errors.append(f'{rel}: table tags unbalanced')
    if s.count('<details>') != s.count('</details>'): errors.append(f'{rel}: details tags unbalanced')
    if s.count('<ul') != s.count('</ul>'): errors.append(f'{rel}: ul tags unbalanced')
    if '—' in s: errors.append(f'{rel}: em dash outside house style')
    source_match=re.search(r'<div class="sources">([\s\S]*?)</div>',s)
    if source_match:
        hrefs=re.findall(r'href="([^"]+)"',source_match.group(1))
        if len(hrefs) != len(set(hrefs)): errors.append(f'{rel}: duplicate source links')

en=(ROOT/'en/explore/index.html').read_text(encoding='utf-8')
fr=(ROOT/'explore/index.html').read_text(encoding='utf-8')
for route in [p[1] for p in pairs if p[1].startswith('/en/')]:
    if f'href="{route}"' not in en: errors.append(f'EN Explore missing {route}')
for route in [p[1] for p in pairs if not p[1].startswith('/en/')]:
    if f'href="{route}"' not in fr: errors.append(f'FR Explore missing {route}')
if 'TRAVEL YOUR WAY' not in en or 'LIVING ON THE RIVIERA' not in en: errors.append('EN Explore family labels')
if 'VOYAGER À VOTRE FAÇON' not in fr or 'VIVRE SUR LA RIVIERA' not in fr: errors.append('FR Explore family labels')

sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
for _,route,_ in pairs:
    if f'<loc>https://www.mametas.com{route}</loc>' not in sitemap: errors.append(f'sitemap missing {route}')

for rel in ('index.html','fr/index.html'):
    s=(ROOT/rel).read_text(encoding='utf-8')
    if 'home-hotel-voice-daniel-2026-03' not in s: errors.append(f'{rel}: Daniel voice missing')
for rel in ('assets/v3.css','assets/site.css'):
    if 'Homepage Hotel Fit traveller voice — 2026-10-01' not in (ROOT/rel).read_text(encoding='utf-8'):
        errors.append(f'{rel}: Daniel style missing')

if errors:
    print('\n'.join('ERROR '+e for e in errors))
    raise SystemExit(1)
print('V5 intent release validation OK:', len(pairs), 'pages')
