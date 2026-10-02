#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re,html
ROOT=Path(__file__).resolve().parents[1]
SKIP_TOP={'.git','.github','docs','scripts','data','backup','lesnicoises-v8-no-mercy-update','lesnicoises-v8-no-mercy-update 2'}
errors=[]; checked=0
for p in ROOT.rglob('*.html'):
 rel=p.relative_to(ROOT)
 if rel.parts and rel.parts[0] in SKIP_TOP: continue
 s=p.read_text(encoding='utf-8',errors='ignore')
 m=re.search(r'<html\b[^>]*\blang=["\']([^"\']+)',s,re.I)
 lang='fr' if m and m.group(1).lower().startswith('fr') else 'en'
 for a in re.finditer(r'<a(?P<attrs>[^>]*)>(?P<text>[^<>]{1,120})</a>',s,re.I):
  attrs=a.group('attrs'); txt=html.unescape(a.group('text')).strip()
  hm=re.search(r'\bhref\s*=\s*["\']([^"\']+)',attrs,re.I)
  if not hm or txt in {'FR','EN'}: continue
  href=hm.group(1).lower()
  if 'riviera-fit' in href or 'riviera-chooser' in href or href.endswith('#riviera-fit'):
   checked+=1
   allowed={'Run my profile through Riviera Fit →','Try Riviera Fit →'} if lang=='en' else {'Tester mon profil dans Riviera Fit →','Tester Riviera Fit →'}
   if txt not in allowed: errors.append(f'{rel}: Riviera Fit CTA {txt!r}')
   expected='/en/riviera-fit/' if lang=='en' else '/riviera-fit/'
   if hm.group(1)!=expected: errors.append(f'{rel}: Riviera Fit href {hm.group(1)!r}')
  if '/hotels/finder/' in href:
   checked+=1
   expected='Try Hotel Fit →' if lang=='en' else 'Tester Hotel Fit →'
   if txt!=expected: errors.append(f'{rel}: Hotel Fit CTA {txt!r}')
 if re.search(r'href=["\'](?:/en)?/riviera-chooser/',s,re.I) or re.search(r'href=["\']/#riviera-fit',s,re.I):
  errors.append(f'{rel}: legacy Riviera Fit href remains')
if errors:
 print('V6 CTA validation failed:')
 for e in errors[:100]: print(' -',e)
 raise SystemExit(1)
print('V6 CTA validation passed on',checked,'text CTA links')
