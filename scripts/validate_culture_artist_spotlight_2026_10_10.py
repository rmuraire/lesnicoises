#!/usr/bin/env python3
"""Non-invasive bilingual Culture artist-spotlight integrity check."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
photo=ROOT/"assets/editorial/renaud-muraire-canterbury-2026.jpg"
css=ROOT/"assets/culture-artist-spotlight.css"
assert photo.exists() and photo.stat().st_size>100_000, "Missing original Canterbury photo"
assert photo.read_bytes()[:3]==b"\xff\xd8\xff", "Culture photo is not valid JPEG"
assert css.exists() and ".culture-artist-spotlight" in css.read_text(encoding="utf8")
for page,copy in [
    ("en/culture/index.html","A Riviera artist to know"),
    ("culture/index.html","Un artiste niçois à découvrir"),
]:
    html=(ROOT/page).read_text(encoding="utf8")
    assert html.count('<aside class="culture-artist-spotlight"')==1, f"{page}: missing or duplicate artist block"
    for needle in [
        copy, "Renaud Muraire", "Canterbury", "Sacred Resonance",
        "renaud-muraire-canterbury-2026.jpg", "assets/culture-artist-spotlight.css",
        "https://www.instagram.com/renaudmuraire/",
        "https://www.renaudmuraire.com/",
    ]:
        assert needle in html, f"{page}: missing {needle}"
print("PASS: two bilingual Culture spotlights, real Canterbury JPEG, stable scoped CSS and Instagram/site links.")
