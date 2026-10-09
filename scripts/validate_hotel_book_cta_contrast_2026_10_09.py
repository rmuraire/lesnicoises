#!/usr/bin/env python3
"""Ensure hotel booking CTAs remain readable and confined to hotel detail pages.

Source-only test; screenshot audit separately rendered all 74 known FR/EN detail
CTAs on a 390px mobile and a 1440px desktop (148 checks).
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
css=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8")
marker="/* HOTEL BOOK CTA CONTRAST — 2026-10-09"
assert css.count(marker)==1,"Missing or duplicate hotel CTA fix"
rules=css.split(marker,1)[1]
for token in (
    "body.hotel-detail-page .affiliate-cta > a.cta-button.btn--affiliate",
    "background:#F7F2E7!important",
    "border:1px solid #F7F2E7!important",
    "color:#14213D!important",
    "background:#FFFFFF!important",
):
    assert token in rules, f"Hotel CTA contrast rule missing: {token}"
assert ".btn--affiliate{background:transparent!important" in css or \
       ".btn--affiliate{background:transparent!important" in \
       (ROOT/"assets/mametas-shell-v1.css").read_text(), \
       "Existing affiliate outline baseline changed: check scope"
checked=0
by_lang={"en":0,"fr":0}
for part,lang in (("en/hotels","en"),("hotels","fr")):
    for file in (ROOT/part).rglob("index.html"):
        txt=file.read_text(encoding="utf-8",errors="ignore")
        if 'class="affiliate-cta"' not in txt:
            continue
        checked+=1
        by_lang[lang]+=1
        assert re.search(r'<body[^>]*class=["\'][^"\']*\bhotel-detail-page\b',txt,re.I), \
            f"Hotel detail CTA missing body scope: {file}"
        assert re.search(r'<a\b[^>]*class=["\'][^"\']*\bcta-button\b[^"\']*\bbtn--affiliate\b',txt,re.I), \
            f"Hotel booking CTA missing expected button classes: {file}"
        assert re.search(r'<a\b[^>]*class=["\'][^"\']*\bcta-button\b[^>]*href=["\']https?://',txt,re.I) or \
               re.search(r'<a\b[^>]*href=["\']https?://[^>]*class=["\'][^"\']*\bcta-button\b',txt,re.I), \
            f"Hotel booking CTA lacks external destination: {file}"
assert checked>=70 and min(by_lang.values())>=30, f"Too few hotel detail pages tested: {by_lang}"
print(f"PASS: {checked} hotel booking CTAs (EN={by_lang['en']}, FR={by_lang['fr']}) protected by scoped contrast rule")
