#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Route every public direct Booking.com reservation URL through Mametas' CJ affiliate wrapper."""
from pathlib import Path
from urllib.parse import quote
import re

ROOT=Path(__file__).resolve().parents[1]
CJ_PREFIX="https://www.kqzyfj.com/click-101875476-15734754?url="
TEXT_SUFFIXES={".html",".json",".xml",".js"}
SKIP_TOP={".git",".github","docs","scripts","data","lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

# Only reservation/deep links are rewritten. Editorial sources such as news.booking.com stay untouched.
BOOKING_RE=re.compile(r'https?://(?:www\.)?booking\.com/(?!content/|articles/|news/|index\.html)([^"\'<>\s]+)',re.I)

def affiliate(url:str)->str:
    if url.startswith(CJ_PREFIX):
        return url
    if url.startswith("http://"):
        url="https://"+url[len("http://"):]
    if url.startswith("https://booking.com/"):
        url="https://www.booking.com/"+url[len("https://booking.com/"):]
    return CJ_PREFIX+quote(url,safe="")

def public_files():
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP:
            continue
        yield p

changed=[]
count=0
for p in public_files():
    s=p.read_text(encoding="utf-8",errors="ignore")
    original=s
    def repl(m):
        global count
        url=m.group(0)
        # Booking newsroom/source links are never commercial booking exits.
        if "news.booking.com" in url:
            return url
        count += 1
        return affiliate(url)
    s=BOOKING_RE.sub(repl,s)
    if s!=original:
        p.write_text(s,encoding="utf-8")
        changed.append(p.relative_to(ROOT).as_posix())

print(f"Booking/CJ enforcement updated {len(changed)} public files and wrapped {count} direct Booking URL occurrence(s).")
for rel in changed:
    print(rel)
