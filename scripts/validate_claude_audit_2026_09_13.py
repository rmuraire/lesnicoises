#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
FR_HUBS=["restaurants/index.html","plages/index.html","escapades/index.html","culture/index.html","hotels/sans-voiture/index.html"]
EN_HUBS=["en/restaurants/index.html","en/beaches/index.html","en/day-trips/index.html","en/culture/index.html","en/hotels/without-a-car/index.html"]
CHECKED=FR_HUBS+EN_HUBS+["riviera-guide/nice/index.html","en/riviera-guide/nice/index.html","riviera-guide/monaco/index.html","en/riviera-guide/monaco/index.html","riviera-guide/cannes/index.html","en/riviera-guide/cannes/index.html","riviera-guide/eze/index.html","en/riviera-guide/eze/index.html","plan/five-days-nice-no-car/index.html","fr/planifier/cinq-jours-nice-sans-voiture/index.html","restaurants/nice/index.html","en/restaurants/nice/index.html"]
def txt(p):
 q=ROOT/p
 if not q.is_file():raise AssertionError(f'Missing expected file: {p}')
 return q.read_text(encoding='utf-8')
def has(p,*needles):
 s=txt(p)
 for n in needles:
  if n not in s:raise AssertionError(f'{p}: missing {n!r}')
def target(h):
 if not h.startswith('/') or h.startswith('//'):return None
 path=unquote(urlsplit(h).path)
 if not path or path=='/':return ROOT/'index.html'
 q=ROOT/path.lstrip('/')
 if path.endswith('/'):return q/'index.html'
 return q if q.is_file() else q/'index.html'
def links(p):
 miss=[]
 for h in re.findall(r'href=["\']([^"\']+)["\']',txt(p)):
  q=target(h)
  if q is not None and not q.is_file():miss.append(h)
 if miss:raise AssertionError(f'{p}: broken internal hrefs: {sorted(set(miss))}')
def main():
 for p in FR_HUBS:has(p,'href="/explore/"','Plan du site','data-mobile-nav','name="viewport"')
 for p in EN_HUBS:has(p,'href="/en/explore/"','Site map','data-mobile-nav','name="viewport"')
 for p in ['restaurants/cannes/index.html','en/restaurants/cannes/index.html']:
  n=len(re.findall(r'class="place"',txt(p)))
  if n!=10:raise AssertionError(f'{p}: expected 10 restaurant entries, found {n}')
 has('restaurants/index.html','href="/restaurants/cannes/"','>10 ADRESSES<');has('en/restaurants/index.html','href="/en/restaurants/cannes/"','>10 ADDRESSES<')
 has('riviera-guide/nice/index.html','/bons-plans/nice-quand-il-pleut/','/bons-plans/erreurs-riviera/','FORTE CHALEUR');has('en/riviera-guide/nice/index.html','/en/good-finds/nice-in-the-rain/','/en/good-finds/riviera-mistakes/','VERY HOT DAYS')
 has('plan/five-days-nice-no-car/index.html','/en/good-finds/nice-in-the-rain/','/en/good-finds/riviera-mistakes/','4–8 weeks before','/en/riviera-guide/eze/');has('fr/planifier/cinq-jours-nice-sans-voiture/index.html','/bons-plans/nice-quand-il-pleut/','/bons-plans/erreurs-riviera/','4 à 8 semaines avant','/riviera-guide/eze/')
 has('riviera-guide/monaco/index.html','FORTE CHALEUR');has('en/riviera-guide/monaco/index.html','VERY HOT DAYS')
 for p,comp in [('riviera-guide/cannes/index.html','/riviera-guide/nice-ou-cannes/'),('en/riviera-guide/cannes/index.html','/en/riviera-guide/nice-or-cannes/')]:
  s=txt(p);has(p,comp,'id="suquet"','id="forville"');portion=s[s.find('<h2'):s.find('id="suquet"')]
  if 'cannes-france.com' in portion:raise AssertionError(f'{p}: Cannes priority cards still exit to Cannes Tourisme')
 has('hotels/sans-voiture/index.html','/fr/dormir/nice/#pratique','/hotels/villefranche-sur-mer/','/hotels/cannes/');has('en/hotels/without-a-car/index.html','/stay/nice/#practical','/en/hotels/villefranche-sur-mer/','/en/hotels/cannes/')
 for p in ['restaurants/nice/index.html','en/restaurants/nice/index.html']:
  s=txt(p);has(p,'/assets/editorial/nice-riviera.jpg')
  if 'commons.wikimedia.org' in s or 'upload.wikimedia.org' in s:raise AssertionError(f'{p}: remote Wikimedia visual remains')
 has('riviera-guide/eze/index.html','LE VERDICT MAMETAS','href="https://www.mametas.com/en/riviera-guide/eze/" hreflang="en"','Depuis Nice','Faut-il réserver ?');has('en/riviera-guide/eze/index.html','THE MAMETAS VERDICT','href="https://www.mametas.com/riviera-guide/eze/" hreflang="fr"','From Nice','Do you need to book?')
 for p in CHECKED:
  s=txt(p)
  if 'name="viewport"' not in s:raise AssertionError(f'{p}: missing responsive viewport')
  if 'primary-nav' not in s and 'v3-nav' not in s:raise AssertionError(f'{p}: missing desktop navigation')
  if 'data-mobile-nav' not in s and 'data-v3-menu' not in s:raise AssertionError(f'{p}: missing mobile navigation')
  links(p)
 for p in ['a-propos/index.html','en/about/index.html','plan/five-days-nice-no-car/index.html','fr/planifier/cinq-jours-nice-sans-voiture/index.html']:
  if not (ROOT/p).is_file():raise AssertionError(f'Preservation guardrail failed: {p} missing')
 print('Claude audit 2026-09-13 validation passed: FR/EN, desktop/mobile structure, internal links and audited dead-ends.')
 return 0
if __name__=='__main__':raise SystemExit(main())
