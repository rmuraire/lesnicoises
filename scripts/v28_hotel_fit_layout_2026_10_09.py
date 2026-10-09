#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep Hotel Fit introductory promise and Riviera Fit bridge in their own rows.

Apply after every editorial/CTA pass and before production validation.
This is intentionally scoped to the two Hotel Fit tool pages (EN/FR).
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("en/hotels/finder/index.html", "hotels/finder/index.html")

def normalize_page(rel):
    page = ROOT / rel
    s = page.read_text(encoding="utf-8")
    before = s
    # Detach the editorial disclosure from the two-column section-heading grid.
    # The old right-side paragraph visually floated across from the large H2.
    heading = re.compile(
        r'(?P<open><div class="section-heading">)'
        r'(?P<title><div>[\s\S]*?</h2></div>)'
        r'(?P<note><p>[^<]+</p>)</div>'
        r'(?=\s*<div class="hotel-engine")', re.I
    )
    if 'class="hotel-fit-intro-note"' not in s:
        match = heading.search(s)
        if not match or "Mametas" not in match.group("note"):
            raise RuntimeError(rel + ": Hotel Fit introductory disclosure not located")
        note = match.group("note").replace("<p>", '<p class="hotel-fit-intro-note">', 1)
        repl = ('<div class="section-heading hotel-fit-heading">' + match.group("title") +
                '</div>' + note)
        s = s[:match.start()] + repl + s[match.end():]

    # The prior tool CTA lived inside a paragraph and was automatically turned
    # into a free-standing navy button by another build pass. Make it a clear
    # one-row action beside a short explanation, inside fieldset 1.
    gate = re.compile(
        r'<p\b[^>]*class=["\'][^"\']*\bengine-base-gate\b[^"\']*["\'][^>]*>'
        r'(?P<body>[\s\S]*?)</p>', re.I
    )
    if 'data-hotel-fit-base-bridge="true"' not in s:
        match = gate.search(s)
        if not match:
            # PR coherence jobs start from a smaller, earlier materialization
            # than production and do not always run v3_architecture_phase2.
            # Create the same canonical bridge in that case.
            first_legend = re.search(r'<fieldset>\s*<legend>1\s*·\s*[^<]+</legend>', s)
            if not first_legend:
                raise RuntimeError(rel + ": first Hotel Fit fieldset/legend missing")
            copy = ("Hotel Fit commence quand la géographie est réglée. Vous hésitez encore entre les villes ?"
                    if rel.startswith("hotels/") else
                    "Hotel Fit starts once geography is settled. Still deciding between towns?")
            href = "/riviera-fit/" if rel.startswith("hotels/") else "/en/riviera-fit/"
            label = "Tester Riviera Fit" if rel.startswith("hotels/") else "Try Riviera Fit"
            block = (
                '<div class="engine-base-gate" data-hotel-fit-base-bridge="true">'
                '<p class="engine-base-gate-copy">' + copy + '</p>'
                '<a class="engine-base-gate-cta" href="' + href + '">' + label + '</a>'
                '</div>'
            )
            if rel.startswith("hotels/"):
                block = block.replace(" ?", "\u202f?").replace(" :", "\u202f:")
            s = s[:first_legend.end()] + block + s[first_legend.end():]
        else:
            inner = match.group("body")
            anchor = re.search(r'<a\b[^>]*>[\s\S]*?</a>', inner, re.I)
            if not anchor:
                raise RuntimeError(rel + ": Riviera Fit anchor not found in base gate")
            text = (inner[:anchor.start()] + inner[anchor.end():]).strip()
            if rel.startswith("hotels/"):
                text = re.sub(r' (?=[?!;:»])', "\u202f", text)
            if not text or "Fit" not in text:
                raise RuntimeError(rel + ": base gate explanation missing")
            label = "Tester Riviera Fit" if rel.startswith("hotels/") else "Try Riviera Fit"
            href = "/riviera-fit/" if rel.startswith("hotels/") else "/en/riviera-fit/"
            repl = (
                '<div class="engine-base-gate" data-hotel-fit-base-bridge="true">'
                '<p class="engine-base-gate-copy">' + text + '</p>'
                '<a class="engine-base-gate-cta" href="' + href + '">' + label + '</a>'
                '</div>'
            )
            s = s[:match.start()] + repl + s[match.end():]
    if s.count('class="hotel-fit-intro-note"') != 1:
        raise RuntimeError(rel + ": expected exactly one editorial note")
    if s.count('data-hotel-fit-base-bridge="true"') != 1:
        raise RuntimeError(rel + ": expected exactly one in-flow Riviera Fit bridge")
    # The base selector remains functional and still contains all destinations.
    for group in ("base","style","geography","mobility"):
        if 'data-engine-group="' + group + '"' not in s:
            raise RuntimeError(rel + ": missing Hotel Fit control " + group)
    # Production uses five controls; shortened PR materialization starts with
    # four. Never drop budget when the page actually advertises five.
    if ("Five choices" in s or "Cinq choix" in s or "5 · " in s) and 'data-engine-group="budget"' not in s:
        raise RuntimeError(rel + ": advertised budget control is missing")
    if rel.startswith("en/") and 'href="/en/riviera-fit/"' not in s:
        raise RuntimeError(rel + ": lost English Riviera Fit link")
    if not rel.startswith("en/") and 'href="/riviera-fit/"' not in s:
        raise RuntimeError(rel + ": lost French Riviera Fit link")
    if s != before:
        page.write_text(s, encoding="utf-8")
    print("Hotel Fit header and base-bridge layout validated:",rel)

def main():
    css = (ROOT / "assets/mametas-foundation.css").read_text(encoding="utf-8")
    for token in (".hotel-fit-heading", ".hotel-fit-intro-note", ".engine-base-gate-cta"):
        if token not in css:
            raise RuntimeError("Missing Hotel Fit CSS " + token)
    for rel in PAGES:
        normalize_page(rel)

if __name__ == "__main__":
    main()
