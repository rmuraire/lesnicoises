#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
changed = []

def save(rel: str, text: str, original: str) -> None:
    if text != original:
        (ROOT / rel).write_text(text, encoding="utf-8")
        changed.append(rel)

def patch_gateway(rel: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text

    if lang == "fr":
        old = '<h2>Deux façons d’utiliser ce guide</h2>\n<div class="verdict"><span class="label">APPROFONDIR OU RAYONNER</span><p><a href="/guide-gay-nice/">Vous restez surtout à Nice ? Utilisez le guide gay détaillé de Nice →</a><br/><a href="/cote-dazur-gay/itineraire-5-jours/">Vous parcourez la côte ? Ouvrez l’itinéraire cinq jours →</a></p></div>'
        new = '''<h2>Deux façons d’utiliser ce guide</h2>
<section class="gay-guide-gateway" aria-label="Choisir le bon guide gay Mametas"><a class="gay-guide-gateway-main" href="/guide-gay-nice/"><span class="gay-guide-gateway-kicker">NICE · GUIDE DÉTAILLÉ</span><h3>Vous restez surtout à Nice ? Entrez dans le vrai guide.</h3><p>Bars, clubs, hôtels Nice Rainbow, restaurants, plage, agenda actuel et ressources locales. Une sélection courte, avec les adresses et les liens pratiques.</p><span class="gay-guide-gateway-cta">Ouvrir le guide gay détaillé de Nice →</span></a><a class="gay-guide-gateway-side" href="/cote-dazur-gay/itineraire-5-jours/"><span class="gay-guide-gateway-kicker">CÔTE · 5 JOURS</span><h3>Vous voulez rayonner ?</h3><p>Gardez Nice comme base LGBTQ+ et construisez le reste de la Riviera autour.</p><span class="gay-guide-gateway-cta">Ouvrir l’itinéraire cinq jours →</span></a></section>'''
    else:
        old = '<h2>Two ways to use this guide</h2>\n<div class="verdict"><span class="label">GO DEEP OR GO WIDE</span><p><a href="/en/gay-nice/">Staying mostly in Nice? Use the detailed Gay Nice guide →</a><br/><a href="/en/gay-french-riviera/5-day-itinerary/">Touring the coast? Open the five-day itinerary →</a></p></div>'
        new = '''<h2>Two ways to use this guide</h2>
<section class="gay-guide-gateway" aria-label="Choose the right Mametas gay guide"><a class="gay-guide-gateway-main" href="/en/gay-nice/"><span class="gay-guide-gateway-kicker">NICE · DETAILED GUIDE</span><h3>Mostly staying in Nice? Go deeper.</h3><p>Bars, clubs, Nice Rainbow hotels, restaurants, beach, current calendar and local resources. A short selection, with addresses and practical links.</p><span class="gay-guide-gateway-cta">Open the detailed Gay Nice guide →</span></a><a class="gay-guide-gateway-side" href="/en/gay-french-riviera/5-day-itinerary/"><span class="gay-guide-gateway-kicker">COAST · 5 DAYS</span><h3>Touring the Riviera?</h3><p>Keep Nice as the LGBTQ+ base and build the rest of the coast around it.</p><span class="gay-guide-gateway-cta">Open the five-day itinerary →</span></a></section>'''

    if old not in text:
        raise RuntimeError(f"{rel}: gay guide gateway anchor not found")
    text = text.replace(old, new, 1)
    save(rel, text, original)

MAPS = {
    "Ramdam Bar": "https://www.google.com/maps/search/?api=1&query=Ramdam+Bar+3+rue+Lascaris+Nice",
    "Le Glam": "https://www.google.com/maps/search/?api=1&query=Le+Glam+6+rue+Eugene+Emanuel+Nice",
    "Club Le 6": "https://www.google.com/maps/search/?api=1&query=Club+Le+6+6+rue+Raoul+Bosio+Nice",
    "Le Klubber": "https://www.google.com/maps/search/?api=1&query=Le+Klubber+14+rue+Benoit+Bunico+Nice",
    "Côté Marais": "https://www.google.com/maps/search/?api=1&query=Cote+Marais+4+rue+du+Pontin+Nice",
    "Davisto": "https://www.google.com/maps/search/?api=1&query=Davisto+18+rue+Saint-Philippe+Nice",
    "Sentimi": "https://www.google.com/maps/search/?api=1&query=Sentimi+2+place+Garibaldi+Nice",
    "Centre LGBTQIA+ Côte d’Azur": "https://www.google.com/maps/search/?api=1&query=Centre+LGBTQIA+Cote+d+Azur+Rue+Cathy+Richeux+Nice",
}

def patch_maps(rel: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    map_label = "Google Maps →"

    for name, url in MAPS.items():
        # Find the named place, then enrich its first address block only.
        name_pos = text.find(f"<h3>{name}</h3>")
        if name_pos < 0:
            raise RuntimeError(f"{rel}: {name} not found")
        addr_start = text.find('<div class="address">', name_pos)
        addr_end = text.find('</div>', addr_start)
        if addr_start < 0 or addr_end < 0:
            raise RuntimeError(f"{rel}: address for {name} not found")
        block = text[addr_start:addr_end + 6]
        if 'gay-map-link' in block:
            continue
        replacement = block[:-6] + f' <a class="gay-map-link" href="{url}" target="_blank" rel="nofollow noopener">{map_label}</a></div>'
        text = text[:addr_start] + replacement + text[addr_end + 6:]

    castel = "https://www.google.com/maps/search/?api=1&query=Castel+Plage+Nice"
    if lang == "fr":
        needle = "<p><strong>Castel Plage</strong>, à l’extrémité est de la Promenade sous la Colline du Château,"
        replacement = f'<p><strong>Castel Plage</strong> <a class="gay-map-link" href="{castel}" target="_blank" rel="nofollow noopener">Google Maps →</a>, à l’extrémité est de la Promenade sous la Colline du Château,'
    else:
        needle = "<p><strong>Castel Plage</strong>, at the eastern end of the Promenade beneath Castle Hill,"
        replacement = f'<p><strong>Castel Plage</strong> <a class="gay-map-link" href="{castel}" target="_blank" rel="nofollow noopener">Google Maps →</a>, at the eastern end of the Promenade beneath Castle Hill,'
    if needle in text:
        text = text.replace(needle, replacement, 1)

    text = text.replace('"dateModified":"2026-09-20"', '"dateModified":"2026-09-25"')
    save(rel, text, original)

def add_css() -> None:
    path = ROOT / "assets/site.css"
    text = path.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 Gay Nice practical layer 2026-09-25 */"
    if marker in text:
        return
    text += r'''

/* V3 Gay Nice practical layer 2026-09-25 */
.gay-guide-gateway{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(280px,.65fr);gap:1px;margin:24px 0 42px;background:rgba(255,255,255,.18);border:1px solid #14213d}
.gay-guide-gateway>a{min-height:250px;padding:30px;display:flex;flex-direction:column;background:#14213d;color:#fff;text-decoration:none!important;transition:background 160ms ease,transform 160ms ease}
.gay-guide-gateway>a:hover,.gay-guide-gateway>a:focus-visible{background:#1a2c50;transform:translateY(-2px)}
.gay-guide-gateway-main{border-right:1px solid rgba(255,255,255,.2)}
.gay-guide-gateway-kicker{color:#f7c966;font-size:9px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
.gay-guide-gateway h3{max-width:15ch;margin:36px 0 14px!important;color:#fff!important;font:500 clamp(29px,3.5vw,45px)/1.05 Fraunces,Georgia,serif!important}
.gay-guide-gateway-side h3{font-size:clamp(25px,2.8vw,34px)!important}
.gay-guide-gateway p{max-width:62ch;margin:0 0 22px!important;color:rgba(255,255,255,.72)!important;font-size:13px!important;line-height:1.6!important}
.gay-guide-gateway-cta{margin-top:auto;color:#f7c966;font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.gay-map-link{display:inline-block;margin-left:6px;color:#176f83!important;font-size:10px;font-weight:800;letter-spacing:.04em;text-decoration:underline!important;text-underline-offset:3px}
.address .gay-map-link{white-space:nowrap}
@media(max-width:760px){.gay-guide-gateway{grid-template-columns:1fr}.gay-guide-gateway-main{border-right:0;border-bottom:1px solid rgba(255,255,255,.2)}.gay-guide-gateway>a{min-height:220px;padding:24px}.gay-guide-gateway h3{margin-top:26px!important}}
'''
    save("assets/site.css", text, original)

def validate() -> None:
    errors = []
    gateway_checks = {
        "cote-dazur-gay/index.html": ("gay-guide-gateway", "Ouvrir le guide gay détaillé de Nice", "Ouvrir l’itinéraire cinq jours"),
        "en/gay-french-riviera/index.html": ("gay-guide-gateway", "Open the detailed Gay Nice guide", "Open the five-day itinerary"),
    }
    for rel, needles in gateway_checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")

    for rel in ("guide-gay-nice/index.html", "en/gay-nice/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if text.count('class="gay-map-link"') < 9:
            errors.append(f"{rel}: expected at least 9 Google Maps links")
        for needle in ("Ramdam Bar", "Le Glam", "Club Le 6", "Le Klubber", "Côté Marais", "Davisto", "Sentimi", "Centre LGBTQIA+ Côte d’Azur", "Castel Plage"):
            if needle not in text:
                errors.append(f"{rel}: missing {needle}")

    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    for needle in ("/* V3 Gay Nice practical layer 2026-09-25 */", ".gay-guide-gateway", ".gay-map-link"):
        if needle not in css:
            errors.append(f"assets/site.css: missing {needle}")

    if errors:
        raise SystemExit("V3 Gay Nice practical layer failed:\n- " + "\n- ".join(errors))

def main() -> int:
    patch_gateway("cote-dazur-gay/index.html", "fr")
    patch_gateway("en/gay-french-riviera/index.html", "en")
    patch_maps("guide-gay-nice/index.html", "fr")
    patch_maps("en/gay-nice/index.html", "en")
    add_css()
    validate()
    print(f"V3 Gay Nice practical layer passed; patched {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
