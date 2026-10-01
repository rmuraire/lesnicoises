#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Blocking audit: every commercial Booking reservation exit on Mametas must use CJ."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
CJ="www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com"
SKIP_TOP={".git",".github","docs","scripts","data","lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}
TEXT_SUFFIXES={".html",".json",".xml",".js"}

raw=[]
affiliate_count=0
for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
        continue
    rel=p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in SKIP_TOP:
        continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    affiliate_count += s.count(CJ)
    for m in re.finditer(r'https?://(?:www\.)?booking\.com/[^"\'<>\s]+',s,re.I):
        url=m.group(0)
        if "news.booking.com" in url:
            continue
        raw.append((rel.as_posix(),url[:220]))

if raw:
    raise SystemExit("NON-AFFILIATE BOOKING LINKS FOUND:\n- "+"\n- ".join(f"{p}: {u}" for p,u in raw[:100]))
if affiliate_count < 100:
    raise SystemExit(f"Affiliate Booking/CJ count unexpectedly low: {affiliate_count}")
print(f"Booking affiliation audit passed: {affiliate_count} CJ/Booking occurrences; 0 raw commercial Booking URLs.")
