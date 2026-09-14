#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EN_HUBS=["en/restaurants/index.html","en/beaches/index.html","en/day-trips/index.html","en/culture/index.html","en/hotels/without-a-car/index.html"]
for rel in EN_HUBS:
    p=ROOT/rel
    s=p.read_text(encoding="utf-8").replace('href="/en/privacy/"','href="/privacy/"')
    p.write_text(s,encoding="utf-8")
p=ROOT/"hotels/sans-voiture/index.html"
s=p.read_text(encoding="utf-8").replace('href="/hotels/la-perouse/"','href="/fr/dormir/nice/#paisible"')
p.write_text(s,encoding="utf-8")
p=ROOT/"en/hotels/without-a-car/index.html"
s=p.read_text(encoding="utf-8")
if '<h2>Central Cannes</h2>' not in s:
    block='<h2>Central Cannes</h2><p><a class="place-link" href="/en/hotels/cannes/">See Cannes hotels by trip style →</a></p><p>If your trip leans west toward Cannes and Antibes, staying close to Cannes station and the Croisette keeps the city walkable and the coastal railway useful. Choose it because your days point west, not because the red carpet looked persuasive.</p>\n'
    s=s.replace('<div class="note">',block+'<div class="note">',1)
p.write_text(s,encoding="utf-8")

def add_mobile(rel,lang):
    p=ROOT/rel;s=p.read_text(encoding="utf-8")
    if 'data-mobile-nav' in s or 'data-v3-menu' in s:return
    if lang=='fr':
        menu='<div class="mobile-nav" data-mobile-nav=""><div class="mobile-nav-top"><span class="brand-name">Mametas</span><button aria-label="Fermer" class="mobile-nav-close" data-menu-close="">×</button></div><ul><li><a href="/fr/#planifier">Planifier</a></li><li><a href="/riviera-guide/">Lieux</a></li><li><a href="/fr/dormir/nice/">Dormir</a></li><li><a href="/explore/">Explorer</a></li><li><a href="/bons-plans/">Maintenant</a></li></ul></div>'
    else:
        menu='<div class="mobile-nav" data-mobile-nav=""><div class="mobile-nav-top"><span class="brand-name">Mametas</span><button aria-label="Close" class="mobile-nav-close" data-menu-close="">×</button></div><ul><li><a href="/#plan">Plan</a></li><li><a href="/en/riviera-guide/">Places</a></li><li><a href="/stay/nice/">Stay</a></li><li><a href="/en/explore/">Explore</a></li><li><a href="/en/good-finds/">Now</a></li></ul></div>'
    button='<button aria-label="Menu" class="menu-toggle" data-menu-open=""><span></span><span></span><span></span></button>'
    s=s.replace('</div></header>',button+'</div></header>'+menu,1)
    p.write_text(s,encoding="utf-8")
add_mobile('riviera-guide/cannes/index.html','fr')
add_mobile('en/riviera-guide/cannes/index.html','en')
print("Audit hotfix applied: privacy, no-car decisions and Cannes mobile navigation.")
