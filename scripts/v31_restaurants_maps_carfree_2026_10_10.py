#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final scoped presentation normalization: restaurants and car-free hotel guide.

After all editorial generators. Adds body classes for the full restaurant family,
without changing venue names, links, provenance, descriptions or hero image URLs.
Splits inline 'Best for' metadata into two readable lines only when unambiguous.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RESTAURANTS = sorted(
    [*ROOT.glob("en/restaurants/*/index.html"),
     *ROOT.glob("restaurants/*/index.html")]
)
WHY = re.compile(r'<p class="why">(?P<content>[^<]*)</p>', re.I)

def tag_body(s: str, classname: str) -> str:
    m = re.search(r'<body\b[^>]*>', s, flags=re.I)
    if not m:
        raise RuntimeError("Missing <body> in page")
    tag = m.group()
    if classname in tag:
        return s
    attr = re.search(r'\bclass=(["\'])(.*?)\1', tag, flags=re.I)
    if attr:
        new = tag[:attr.start(2)] + attr.group(2) + " " + classname + tag[attr.end(2):]
    else:
        new = tag[:-1] + f' class="{classname}">'
    return s[:m.start()] + new + s[m.end():]

def normalize_restaurant(s: str) -> str:
    s = tag_body(s, "mametas-restaurant-detail")
    def split_why(m: re.Match[str]) -> str:
        content = m.group("content").strip()
        pattern = re.search(r'(?:(?<= · )|^)(Best for:|Choose it for:|Idéal pour :|À choisir pour :|Pour :)\s*',
                            content, flags=re.I)
        if pattern is None:
            return m.group()
        meta = content[:pattern.start()].strip().rstrip("·").strip()
        purpose = content[pattern.start():].strip()
        if meta:
            return ('<div class="mametas-restaurant-brief">'
                    '<p class="mametas-restaurant-tags">' + meta + '</p>'
                    '<p class="mametas-restaurant-best-for">' + purpose + '</p></div>')
        return ('<div class="mametas-restaurant-brief">'
                '<p class="mametas-restaurant-best-for">' + purpose + '</p></div>')
    return WHY.sub(split_why, s)

def main() -> None:
    if len(RESTAURANTS) < 20:
        raise RuntimeError(f"Restaurant family incomplete: {len(RESTAURANTS)}")
    edited = 0
    for f in RESTAURANTS:
        old = f.read_text(encoding="utf-8")
        s = normalize_restaurant(old)
        if 'mametas-restaurant-detail' not in s:
            raise RuntimeError(f"Missing restaurant family body marker: {f}")
        if s.count('href="https://www.google.com/maps') != old.count('href="https://www.google.com/maps'):
            raise RuntimeError(f"Map link count unexpectedly changed: {f}")
        if s.count('class="place"') != old.count('class="place"'):
            raise RuntimeError(f"Restaurant recommendation count changed: {f}")
        if s != old:
            f.write_text(s, encoding="utf-8")
            edited += 1
    car = ROOT / "en/hotels/without-a-car/index.html"
    s = car.read_text(encoding="utf-8")
    t = tag_body(s, "mametas-car-free-guide")
    if t != s:
        car.write_text(t, encoding="utf-8")
        edited += 1
    css = (ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
    for token in ("MAMETAS RESTAURANT / MAP / CAR-FREE RECIPE",
                  ".mametas-restaurant-detail .culture-hero-media",
                  ".mametas-car-free-guide .article .fact"):
        if token not in css:
            raise RuntimeError(f"Missing final CSS: {token}")
    print(f"Scoped restaurant/car-free pages verified: {len(RESTAURANTS)} + 1; edited {edited}")

if __name__ == "__main__":
    main()
