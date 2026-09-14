#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EN_HUBS=["en/restaurants/index.html","en/beaches/index.html","en/day-trips/index.html","en/culture/index.html","en/hotels/without-a-car/index.html"]
for rel in EN_HUBS:
    p=ROOT/rel
    s=p.read_text(encoding="utf-8").replace('href="/en/privacy/"','href="/privacy/"')
    p.write_text(s,encoding="utf-8")
p=ROOT/"en/hotels/without-a-car/index.html"
s=p.read_text(encoding="utf-8")
if '<h2>Central Cannes</h2>' not in s:
    block='<h2>Central Cannes</h2><p><a class="place-link" href="/en/hotels/cannes/">See Cannes hotels by trip style →</a></p><p>If your trip leans west toward Cannes and Antibes, staying close to Cannes station and the Croisette keeps the city walkable and the coastal railway useful. Choose it because your days point west, not because the red carpet looked persuasive.</p>\n'
    s=s.replace('<div class="note">',block+'<div class="note">',1)
p.write_text(s,encoding="utf-8")
print("Audit hotfix applied: English privacy target and Cannes no-car decision.")
