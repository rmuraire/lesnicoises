#!/usr/bin/env python3
"""Release blocker: protect all 18 FR/EN hotel hub pages from malformed markup.

Checks section structure, actual hotel card count, and cards nested inside
other hotel cards. The text "15 selected hotels" alone is not sufficient.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from augment_hotels_2026_09_13 import BASES

class HotelHubParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.articles=[]
        self.sections=[]
        self.cards=0
        self.cards_per_section=Counter()
        self.section_ids=[]
        self.errors=[]

    def handle_starttag(self, tag, attrs):
        props=dict(attrs)
        classes=set((props.get("class") or "").split())
        if tag=="section":
            section_id=props.get("id") if "hotel-style-section" in classes else None
            self.sections.append(section_id)
            if section_id:
                self.section_ids.append(section_id)
        if tag=="article":
            choice="hotel-choice-card" in classes
            if choice:
                if any(self.articles):
                    self.errors.append("hotel-choice-card nested inside another hotel card")
                self.cards+=1
                section=next((s for s in reversed(self.sections) if s),None)
                self.cards_per_section[section]+=1
            self.articles.append(choice)

    def handle_endtag(self, tag):
        if tag=="article":
            if self.articles: self.articles.pop()
            else: self.errors.append("unexpected </article>")
        if tag=="section":
            if self.sections: self.sections.pop()
            else: self.errors.append("unexpected </section>")

def main():
    errors=[]
    count=0
    for city,meta in BASES.items():
        if city=="nice":
            # Nice uses a separate stay hub component family.
            continue
        for lang in ("fr","en"):
            path=ROOT/meta[lang]
            if not path.is_file():
                errors.append(f"{path}: missing hub file")
                continue
            html=path.read_text(encoding="utf-8")
            parser=HotelHubParser()
            parser.feed(html)
            expected=meta["count"]
            if parser.cards!=expected:
                errors.append(f"{path}: {parser.cards} parsed cards; expected {expected}")
            if len(parser.section_ids)<2:
                errors.append(f"{path}: only {len(parser.section_ids)} sections; expected 2+")
            if len(set(parser.section_ids))!=len(parser.section_ids):
                errors.append(f"{path}: duplicate hotel section IDs")
            for section in parser.section_ids:
                if parser.cards_per_section[section]<1:
                    errors.append(f"{path}: empty section {section}")
            if parser.cards_per_section[None]:
                errors.append(f"{path}: {parser.cards_per_section[None]} cards outside hotel sections")
            for error in parser.errors:
                errors.append(f"{path}: {error}")
            count+=1
            print(f"HUB CHECK {path.relative_to(ROOT)}: {parser.cards}/{expected} cards, "
                  f"{len(parser.section_ids)} sections, no nesting: {not parser.errors}",flush=True)
    if errors:
        for error in errors:
            print("HOTEL STRUCTURE FAIL:",error,flush=True)
        raise SystemExit(f"Hotel hub structural integrity failed: {len(errors)} issues")
    print(f"PASS: {count} FR/EN hotel hubs meet structural contract",flush=True)

if __name__=="__main__":
    main()
