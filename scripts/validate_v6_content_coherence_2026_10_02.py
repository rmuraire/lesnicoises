#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression guard for the Mametas coherence cleanup.

This is intentionally about system-level regressions, not subjective copy.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")

# 1) Canonical city system and homepage classification.
city = json.loads(read("data/city-system-v1.json"))
if city.get("groups", {}).get("base") != ["nice","villefranche","antibes","cannes","monaco","menton"]:
    errors.append("city system: base classification drift")
if city.get("groups", {}).get("detour") != ["eze","saintpaul","sainttropez"]:
    errors.append("city system: detour classification drift")
if len(city.get("cities", {})) != 9:
    errors.append("city system: expected 9 canonical destinations")

for rel in ("index.html", "fr/index.html"):
    s = read(rel)
    if not s:
        errors.append(f"{rel}: missing homepage")
        continue
    for key in city["groups"]["base"] + city["groups"]["detour"]:
        if s.count(f'data-mametas-city="{key}"') != 1:
            errors.append(f"{rel}: city marker {key} missing/duplicated")
    if s.count('data-city-group="base"') != 1 or s.count('data-city-group="detour"') != 1:
        errors.append(f"{rel}: canonical base/detour groups missing")

# 2) Destination pages.
destination_files = [
    ("nice","nice"), ("villefranche-cap-ferrat","villefranche"),
    ("antibes","antibes"), ("cannes","cannes"), ("monaco","monaco"),
    ("menton","menton"), ("eze","eze"), ("saint-paul-de-vence","saintpaul"),
    ("saint-tropez","sainttropez"),
]
for slug, key in destination_files:
    for lang, prefix in (("en","en/"),("fr","")):
        rel = f"{prefix}riviera-guide/{slug}/index.html"
        s = read(rel)
        if not s:
            errors.append(f"{rel}: missing destination page")
            continue
        if s.count('data-destination-reality="canonical"') != 1:
            errors.append(f"{rel}: canonical Reality Check missing/duplicated")
        labels = ("Getting around","Budget","Season","Logistics") if lang=="en" else ("Déplacements","Budget","Saison","Logistique")
        for label in labels:
            if f"<b>{label}</b>" not in s:
                errors.append(f"{rel}: Reality Check label {label} missing")
        if "mametas-detail-back" not in s or "mametas-detail-eyebrow" not in s:
            errors.append(f"{rel}: canonical detail top missing")
        if key in {"nice","villefranche","antibes","cannes","monaco","menton"} and "destination-hotel-fit-cta" not in s:
            errors.append(f"{rel}: Hotel Fit bridge missing")

# 3) Legacy semantic fragments from the audit.
for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git",".github","docs","scripts","data","backup"}:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    lang_m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', s, re.I)
    lang = "fr" if lang_m and lang_m.group(1).lower().startswith("fr") else "en"
    if '/#riviera-fit' in s:
        errors.append(f"{rel}: legacy Riviera Fit home anchor")
    if lang == "fr":
        for bad in ("Mametas rule", "MAMETAS RULE", "MAMETAS SAYS", "MAMETAS HOTEL TAKE"):
            if bad in s:
                errors.append(f"{rel}: English UI label remains on FR page ({bad})")
    else:
        # English heading punctuation only: no French-style space before colon.
        for m in re.finditer(r'<h[1-3]\b[^>]*>(.*?)</h[1-3]>', s, re.S | re.I):
            plain = re.sub(r'<[^>]+>', '', m.group(1))
            if re.search(r'\s+:', plain):
                errors.append(f"{rel}: English heading has space before colon")
                break

# 4) Source headings: canonical when a formal sources block exists.
for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git",".github","docs","scripts","data","backup"}:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r'<div\b[^>]*class=["\'][^"\']*sources[^"\']*["\']', s, re.I):
        continue
    lang_m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', s, re.I)
    fr = bool(lang_m and lang_m.group(1).lower().startswith("fr"))
    expected = "Sources vérifiées" if fr else "Sources checked"
    if f"<h2>{expected}</h2>" not in s:
        errors.append(f"{rel}: non-canonical sources heading")

# 5) Redirected duplicate Nice hotel hubs must stay out of sitemap.
sm = read("sitemap.xml")
for loc in (
    "https://www.mametas.com/en/hotels/nice/",
    "https://www.mametas.com/hotels/nice/",
):
    if f"<loc>{loc}</loc>" in sm:
        errors.append(f"sitemap.xml: redirected hub still indexed ({loc})")

# 6) Hotel detail pages: canonical top, provider CTA and next decision.
hotel_checked = 0
for p in ROOT.rglob("index.html"):
    rel = p.relative_to(ROOT)
    parts = rel.parts
    if not (
        (len(parts)>=5 and parts[0]=="en" and parts[1]=="hotels")
        or (len(parts)>=4 and parts[0]=="hotels")
    ):
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    if not any(x in s for x in ('class="hotel-detail"',"THE MAMETAS VERDICT","LE VERDICT MAMETAS","MAMETAS HOTEL TAKE")):
        continue
    hotel_checked += 1
    if "mametas-detail-back" not in s or "mametas-detail-eyebrow" not in s:
        errors.append(f"{rel}: hotel detail top missing")
    if "hotel-next-decision" not in s:
        errors.append(f"{rel}: hotel next decision missing")
    for m in re.finditer(r'<a([^>]+)>(.*?)</a>', s, re.S | re.I):
        attrs = m.group(1)
        if "sponsored" not in attrs.lower():
            continue
        href_m = re.search(r'href=["\']([^"\']+)', attrs, re.I)
        href = href_m.group(1) if href_m else ""
        label = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        fr = bool(re.search(r'<html[^>]+lang=["\']fr', s, re.I))
        if "expedia" in href.lower():
            expected = "Voir les tarifs sur Expedia" if fr else "Check rates on Expedia"
            if label != expected:
                errors.append(f"{rel}: non-canonical Expedia CTA")
        if "booking.com" in href.lower() or "kqzyfj.com" in href.lower():
            expected = "Voir les tarifs sur Booking.com" if fr else "Check rates on Booking.com"
            if label != expected:
                errors.append(f"{rel}: non-canonical Booking CTA")

if hotel_checked < 10:
    errors.append(f"hotel detail guard only found {hotel_checked} pages")

# 7) Agenda/current-information naming is one system.
agenda_expectations = {
    "index.html": "RIVIERA AGENDA",
    "fr/index.html": "AGENDA DE LA RIVIERA",
    "en/good-finds/index.html": "RIVIERA AGENDA",
    "bons-plans/index.html": "AGENDA DE LA RIVIERA",
}
for rel, expected in agenda_expectations.items():
    page = read(rel)
    if page and expected not in page:
        errors.append(f"{rel}: canonical agenda name missing ({expected})")

# 8) Restaurant cards must not repeat the compact decision metadata in .why.
restaurant_meta_count = 0
for p in ROOT.rglob("index.html"):
    rel = p.relative_to(ROOT)
    rels = rel.as_posix()
    if "/restaurants/" not in f"/{rels}" or rels in {"en/restaurants/index.html", "restaurants/index.html"}:
        continue
    page = p.read_text(encoding="utf-8", errors="ignore")
    restaurant_meta_count += page.count('class="restaurant-meta"')
    for m in re.finditer(r'<p class="why">([\s\S]*?)</p>', page, re.I):
        why = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if re.match(r'^€{1,4}\s*·', why):
            errors.append(f"{rel}: restaurant metadata duplicated inside .why")
            break
if restaurant_meta_count < 20:
    errors.append(f"restaurant component guard found only {restaurant_meta_count} decision metadata rows")

# 9) Culture practical grid fields must not repeat Address inside Hours & price.
culture_grid_count = 0
for p in ROOT.rglob("index.html"):
    rel = p.relative_to(ROOT)
    rels = rel.as_posix()
    if "/culture/" not in f"/{rels}" or rels in {"en/culture/index.html", "culture/index.html", "en/culture/nice/index.html", "culture/nice/index.html"}:
        continue
    page = p.read_text(encoding="utf-8", errors="ignore")
    for grid in re.finditer(r'<div class="culture-logistics-grid">([\s\S]*?)</div>\s*</div>', page, re.I):
        culture_grid_count += 1
        fields = {}
        for cell in re.finditer(r'<div><b>(.*?)</b><span>([\s\S]*?)</span></div>', grid.group(1), re.I):
            label = re.sub(r'<[^>]+>', '', cell.group(1)).strip()
            value = re.sub(r'<[^>]+>', '', cell.group(2)).strip()
            fields[label] = value
        address = fields.get("Address") or fields.get("Adresse") or ""
        hp = fields.get("Hours & price") or fields.get("Horaires & tarif") or ""
        if address and address not in {"See official information below.", "Voir les informations officielles ci-dessous."} and address in hp:
            errors.append(f"{rel}: culture Hours & price repeats Address")
if culture_grid_count < 20:
    errors.append(f"culture component guard found only {culture_grid_count} practical grids")

if errors:
    print("Content coherence validation failed:")
    for e in errors[:160]:
        print(" -", e)
    raise SystemExit(1)

print(f"Content coherence validation passed; {hotel_checked} hotel detail pages guarded.")
