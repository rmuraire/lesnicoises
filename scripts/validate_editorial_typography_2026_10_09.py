#!/usr/bin/env python3
"""Guard against re-introducing the oversized emergency typography rules."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
foundation=(ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
shell=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8")
site=(ROOT/"assets/site.css").read_text(encoding="utf-8")
assert "/* 1) One restrained editorial heading scale." in foundation
headline=foundation.split("/* 1) One restrained editorial heading scale.",1)[1].split("/* 2) Buttons",1)[0]
for sel in (".article h2,",".hotel-detail h2,",".culture-detail h2,",
            ".article h3,",".hotel-card h3,"):
    assert sel not in headline,f"Unexpected emergency title override: {sel}"
for token in (".article h2{font-size:34px", ".hotel-detail h2{font-size:34px",
              ".culture-detail h2{font-size:34px",
              ".article h3{font-size:25px", ".hotel-card h3{font-size:25px"):
    assert token in site,f"Native editorial type size not found: {token}"
rule=shell.split("body.rg-destination.rg-legacy .legacy-destination-section>p,",1)[1].split("}",1)[0]
assert "font-size:16px!important" in rule
assert "line-height:1.68!important" in rule
print("PASS: original article/hotel/culture type scale restored, destinations legible, no extra override")
