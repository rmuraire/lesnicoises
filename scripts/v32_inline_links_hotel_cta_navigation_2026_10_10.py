#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final generated-HTML normalization: car-free Hotel Fit and next-decision panels.

Runs LAST, after all V31 and editorial passes. All existing destinations,
booking/affiliate URLs and link text are preserved verbatim.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CAR_PAGES = ("en/hotels/without-a-car/index.html", "hotels/sans-voiture/index.html")
BRIDGE = re.compile(
    r'<div\b[^>]*class=["\'][^"\']*\bsource-box\b[^"\']*\bphase3-hotel-fit\b[^"\']*["\'][^>]*>'
    r'(?P<inner>[\s\S]*?)</div>', re.I)
ANCHOR = re.compile(r'<a\b[^>]*>[\s\S]*?</a>', re.I)
NEXT = re.compile(
    r'<section class="legacy-destination-section">'
    r'(?=\s*<h2\b[^>]*>(?:The next decision|La prochaine décision)</h2>'
    r'\s*<div class="next-decision-list">)',re.I)

def body_class(s, klass):
    match=re.search(r'<body\b[^>]*>',s,re.I)
    if not match: raise RuntimeError("Missing body element")
    tag=match.group()
    if klass in tag:return s
    attr=re.search(r'\bclass=(["\'])(.*?)\1',tag,re.I)
    if attr:
        updated=tag[:attr.end(2)]+" "+klass+tag[attr.end(2):]
    else:
        updated=tag[:-1]+f' class="{klass}">'
    return s[:match.start()]+updated+s[match.end():]

def fix_carfree(s,fr,rel):
    s=body_class(s,"mametas-car-free-guide")
    if 'mametas-hotel-fit-bridge' in s:return s
    def replace(m):
        inner=m.group("inner")
        matches=list(ANCHOR.finditer(inner))
        if len(matches)!=1:
            raise RuntimeError(f"{rel}: expected one Hotel Fit CTA inside old box")
        anchor=matches[0].group()
        href=re.search(r'\bhref=["\']([^"\']+)["\']',anchor,re.I)
        if not href or not href.group(1).startswith("/hotels/finder/") and not href.group(1).startswith("/en/hotels/finder/"):
            raise RuntimeError(f"{rel}: unexpected URL inside Hotel Fit CTA")
        # Keep href, link label, sponsorship properties; move the button beside prose.
        anchor=re.sub(r'class=(["\'])(.*?)\1',
                      lambda q: 'class="'+q.group(2)+' mametas-hotel-fit-action"',anchor,count=1,flags=re.I)
        copy=(
            "Point de chute choisi ? Comparez les hôtels sélectionnés selon le budget, "
            "vos priorités et l’accès aux transports."
            if fr else
            "Base chosen? Compare Mametas-selected hotels by budget, priorities "
            "and transport access."
        )
        return ('<div class="source-box phase3-hotel-fit mametas-hotel-fit-bridge">'
                '<p>'+copy+'</p>'+anchor+'</div>')
    out,n=BRIDGE.subn(replace,s)
    if "phase3-hotel-fit" in s and n!=1:
        raise RuntimeError(f"{rel}: expected exactly one legacy Hotel Fit box; got {n}")
    return out

def main():
    modified=0
    for rel in CAR_PAGES:
        path=ROOT/rel
        if not path.is_file(): raise RuntimeError(f"Missing required car-free page: {rel}")
        old=path.read_text(encoding="utf-8")
        new=fix_carfree(old,not rel.startswith("en/"),rel)
        if old!=new:
            path.write_text(new,encoding="utf-8");modified+=1
        print("Car-free CTA:",rel,"ready",flush=True)
    # All legacy Riviera Guide pages whose final generated structure
    # contains a Next decision list. We only add a class to the section.
    count=0
    for path in sorted([*ROOT.glob("en/riviera-guide/*/index.html"),
                        *ROOT.glob("riviera-guide/*/index.html")]):
        old=path.read_text(encoding="utf-8")
        new,n=NEXT.subn(
            '<section class="legacy-destination-section mametas-next-decision-panel">',
            old)
        if n>1:raise RuntimeError(f"{path}: duplicated Next decision section")
        if new!=old:
            path.write_text(new,encoding="utf-8");count+=1
    css=(ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
    for marker in ("MAMETAS SINGLE-UNDERLINE / CAR-FREE / BOOKING / DECISIONS",
                   ".mametas-hotel-fit-bridge",".mametas-next-decision-panel",
                   ".hotel-choice-card .hotel-choice-copy"):
        if marker not in css: raise RuntimeError(f"Missing final CSS: {marker}")
    print("Car-free/Next decision final markup verified:",modified,count,flush=True)

if __name__=="__main__":
    main()
