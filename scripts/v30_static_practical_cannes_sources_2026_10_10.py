#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the ACTUAL static HTML emitted late in Mametas production.

Legacy static city tips are emitted as <section data-static-editorial=true>
containing three <p class=mini-rule>. The old client-side practical-layer.js
does not render these pages; CSS for .day-grid cannot affect their contents.

Also close the invalid split <div class=sources> on Cannes, preserving URLs.
Runs after v29, before all final validations and the OVH upload.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CITIES = ("nice", "villefranche-cap-ferrat", "antibes", "monaco", "menton")
STATIC_SECTION = re.compile(
    r'<section\b(?=[^>]*\bclass=["\'][^"\']*\bpractical-decision-layer\b)'
    r'(?=[^>]*\bdata-static-editorial=["\']true["\'])'
    r'[^>]*>[\s\S]*?</section>', re.I)
TIP = re.compile(
    r'<p\b[^>]*class=["\']mini-rule["\'][^>]*>\s*'
    r'<strong\b[^>]*>(?P<title>[\s\S]*?)</strong>\s*'
    r'(?P<text>[\s\S]*?)</p>', re.I)
H2 = re.compile(r'<h2\b[^>]*>[\s\S]*?</h2>', re.I)

def normalize_tip_section(source: str, fr: bool, rel: str) -> str:
    def replace(m: re.Match[str]) -> str:
        block = m.group(0)
        if 'data-mametas-practical-v2="true"' in block:
            return block
        matches = list(TIP.finditer(block))
        if len(matches) != 3:
            raise RuntimeError(f"{rel}: expected exactly 3 static tips; found {len(matches)}")
        tip_area = block[matches[0].start():matches[-1].end()]
        if TIP.sub("", tip_area).strip():
            raise RuntimeError(f"{rel}: other content mixed into tip list")
        rows = []
        for match in matches:
            rows.append(
                '<div class="mametas-practical-tip">'
                f'<h3>{match.group("title").strip()}</h3>'
                f'<p>{match.group("text").strip()}</p></div>'
            )
        heading = "Trois décisions pratiques" if fr else "Three practical decisions"
        block, n = H2.subn(f'<h2>{heading}</h2>', block, count=1)
        if n != 1:
            raise RuntimeError(f"{rel}: practical section heading missing")
        new_matches = list(TIP.finditer(block))
        replacement = (
            '<div class="mametas-practical-tip-list" data-mametas-practical-v2="true">'
            + "".join(rows) + '</div>'
        )
        block = (block[:new_matches[0].start()] + replacement
                 + block[new_matches[-1].end():])
        if block.count('class="mametas-practical-tip"') != 3:
            raise RuntimeError(f"{rel}: practical tip count changed")
        return block
    return STATIC_SECTION.sub(replace, source)


BROKEN_CANNES = re.compile(
    r'<section\b[^>]*class=["\']legacy-destination-section["\'][^>]*>\s*'
    r'<h2\b[^>]*>(?:The next decision|La prochaine décision)</h2>\s*'
    r'<div class="sources">\s*<h2>(?:Sources checked|Sources vérifiées)</h2>\s*</section>\s*'
    r'<section\b[^>]*class=["\']legacy-destination-section["\'][^>]*>\s*'
    r'<h2\b[^>]*>(?:Sources checked|Sources vérifiées)</h2>\s*'
    r'(?P<links><ul>[\s\S]*?</ul>)\s*</div>\s*</section>',
    re.I,
)

def normalize_cannes_sources(source: str, fr: bool, rel: str) -> str:
    def repair(m: re.Match[str]) -> str:
        heading = "Sources vérifiées" if fr else "Sources checked"
        links = m.group("links")
        if not links.count("<li"):
            raise RuntimeError(f"{rel}: source links lost in malformed block")
        return (
            '<section class="legacy-destination-section mametas-sources-section">'
            f'<div class="sources"><h2>{heading}</h2>'
            + links + '</div></section>'
        )
    corrected, count = BROKEN_CANNES.subn(repair, source)
    # The known split div in production MUST be repaired, or rejected.
    if re.search(
        r'<div class="sources">\s*<h2>Sources (?:checked|vérifiées)</h2>\s*</section>',
        corrected, re.I,
    ):
        raise RuntimeError(f"{rel}: malformed sources wrapper still present")
    if count > 1:
        raise RuntimeError(f"{rel}: unexpected multiple Cannes wrappers")
    return corrected

def main() -> None:
    transformed = 0
    for city in CITIES:
        for fr in (False, True):
            rel = ("" if fr else "en/") + f"riviera-guide/{city}/index.html"
            file = ROOT / rel
            before = file.read_text(encoding="utf-8")
            after = normalize_tip_section(before, fr, rel)
            if STATIC_SECTION.search(before):
                transformed += 1
                if after.count('data-mametas-practical-v2="true"') != 1:
                    raise RuntimeError(f"{rel}: static tip layout not normalized")
            if after != before:
                file.write_text(after, encoding="utf-8")
            print("Practical family:", rel,
                  "normalized" if after != before else "no static block")
    for fr in (False, True):
        rel = ("" if fr else "en/") + "riviera-guide/cannes/index.html"
        file = ROOT / rel
        old = file.read_text(encoding="utf-8")
        new = normalize_cannes_sources(old, fr, rel)
        if new != old:
            file.write_text(new, encoding="utf-8")
        print("Cannes sources", rel, "repaired" if new != old else "already valid")
    css = (ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
    assert "MAMETAS PRACTICAL STATIC V2" in css
    print("Final static practical pages normalized:", transformed)

if __name__ == "__main__":
    main()
