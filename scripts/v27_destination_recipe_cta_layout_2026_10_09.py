#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final, family-scoped destination CTA recipe.

Run after all content/CTA generators and before validation/deployment.
A destination gets exactly ONE Hotel Fit entry at the end of its accommodation
section, not inline in editorial prose or repeated in source-boxes.
The eight V3 destination pages share this layout; legacy Places use another
template and are not rewritten here.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ("antibes", "stay", "dormir"),
    ("villefranche-cap-ferrat", "stay", "dormir"),
    ("monaco", "hotel", "hotel"),
    ("menton", "stay", "dormir"),
)
FINDER = re.compile(r'href=["\']/(?:en/)?hotels/finder/(?:\?[^"\']*)?["\']', re.I)
HEADING = re.compile(r'<h2\b[^>]*>[\s\S]*?</h2>', re.I)
LINK = re.compile(r'<a\b[^>]*\bhref=["\']/(?:en/)?hotels/finder/[^"\']*["\'][^>]*>[\s\S]*?</a>', re.I)
PARAGRAPH = re.compile(r'<p\b[^>]*>[\s\S]*?</p>', re.I)
SOURCE_BOX = re.compile(r'<div\b[^>]*class=["\'][^"\']*(?:hotel-fit-cta|destination-hotel-fit-bridge)[^"\']*["\'][^>]*>[\s\S]*?</div>', re.I)
TOOL_DIV = re.compile(r'<div\b[^>]*class=["\'][^"\']*source-box[^"\']*["\'][^>]*>[\s\S]*?</div>', re.I)

def normalize(rel: str, fr: bool, slug: str) -> None:
    path = ROOT / rel
    content = path.read_text(encoding="utf-8")
    body_start = re.search(r'<div\b[^>]*class=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>', content, re.I)
    if not body_start:
        raise RuntimeError(f"{rel}: V3 editorial body missing")
    article_end = content.find("</article>", body_start.end())
    if article_end < 0:
        raise RuntimeError(f"{rel}: article boundary missing")
    before = content[body_start.end():article_end]

    # These blocks were previously injected at different pipeline stages.
    # They are editorial tool promos, not hotel cards, checked source links or
    # any real booking link. Remove only finder-related promos.
    body = SOURCE_BOX.sub(lambda m: "" if FINDER.search(m.group(0)) else m.group(0), before)
    body = TOOL_DIV.sub(lambda m: "" if FINDER.search(m.group(0)) else m.group(0), body)
    body = PARAGRAPH.sub(lambda m: "" if FINDER.search(m.group(0)) else m.group(0), body)
    # Some previous generators left orphan anchors outside p/div. Do not leave
    # a floating call to action behind.
    body = LINK.sub("", body)
    body = re.sub(r'<p\b[^>]*>\s*</p>', "", body, flags=re.I)

    hs = list(HEADING.finditer(body))
    stay = None
    for h in hs:
        title = re.sub(r'<[^>]+>', " ", h.group(0)).lower()
        if slug == "monaco":
            chosen = ("hotels:" in title or "hôtels" in title)
        else:
            chosen = ("where to stay" in title or "où dormir" in title)
        if chosen:
            stay = h
            break
    if stay is None:
        raise RuntimeError(f"{rel}: accommodation section heading missing")
    next_heading = next((h for h in hs if h.start() > stay.end()), None)
    if next_heading is None:
        raise RuntimeError(f"{rel}: no heading after accommodation section")

    url = ("/hotels/finder/" if fr else "/en/hotels/finder/") + f"?base={slug if slug != 'villefranche-cap-ferrat' else 'villefranche'}"
    lead = ("Le bon hôtel dépend de votre budget et de votre façon de voyager."
            if fr else "The right hotel depends on your budget and how you travel.")
    action = "Tester Hotel Fit" if fr else "Try Hotel Fit"
    bridge = (
        '<div class="destination-hotel-fit-single" data-mametas-destination-fit="one">'
        f'<p>{lead}</p><a class="btn btn--primary destination-hotel-fit-action" '
        f'href="{url}">{action}</a></div>\n'
    )
    body = body[:next_heading.start()] + bridge + body[next_heading.start():]
    if len(FINDER.findall(body)) != 1 or body.count('data-mametas-destination-fit="one"') != 1:
        raise RuntimeError(f"{rel}: single Hotel Fit CTA invariant failed")
    content = content[:body_start.end()] + body + content[article_end:]
    if content != path.read_text(encoding="utf-8"):
        path.write_text(content, encoding="utf-8")
    print("Destination Hotel Fit unified:", rel)

def verify_assets() -> None:
    css = (ROOT / "assets/mametas-foundation.css").read_text(encoding="utf-8")
    for token in (".destination-hotel-fit-single", ".practical-decision-layer .day-grid", ".mametas-activity-cta"):
        if token not in css:
            raise RuntimeError(f"Recipe CSS missing: {token}")
    for rel in ("escapades/index.html", "en/day-trips/index.html"):
        html = (ROOT / rel).read_text(encoding="utf-8")
        if "mametas-activity-grid" not in html or "mametas-activity-cta" not in html:
            raise RuntimeError(f"{rel}: curated activity cards or CTAs missing")
    js = (ROOT / "assets/practical-layer.js").read_text(encoding="utf-8")
    for key in ("nice:", "villefranche:", "antibes:", "monaco:", "menton:"):
        if key not in js:
            raise RuntimeError(f"Practical tips family missing: {key}")

def repair_french_punctuation(rel: str) -> None:
    """Replace ordinary spaces before French high punctuation in rendered text.

    This targets only the two known legacy pages flagged by the release gate.
    Keep markup, CSS, inline JS, JSON-LD, URLs and affiliate hrefs intact.
    """
    path = ROOT / rel
    source = path.read_text(encoding="utf-8")
    tokens = re.compile(
        r'(?s)<(?:script|style|textarea|pre|code)\b[^>]*>.*?</(?:script|style|textarea|pre|code)>'
        r'|<[^>]+>|[^<]+',
        flags=re.I,
    )

    def patch(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.startswith("<"):
            return token
        return re.sub(r' (?=[?!;:»])', "\u202f", token)

    fixed = tokens.sub(patch, source)
    if fixed != source:
        path.write_text(fixed, encoding="utf-8")
    # Release gate inspects text nodes rather than source markup.
    nodes = re.split(r'(<[^>]+>)', re.sub(
        r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>',
        '', fixed, flags=re.I,
    ))
    if any(re.search(r' (?=[?!;:»])', node) for node in nodes[::2]):
        raise RuntimeError(f"{rel}: stray ordinary French punctuation space")
    print("French text-node spacing verified:", rel)


def main() -> None:
    for slug, _, _ in PAGES:
        normalize(f"en/riviera-guide/{slug}/index.html", False, slug)
        normalize(f"riviera-guide/{slug}/index.html", True, slug)
    for rel in ("escapades/index.html", "riviera-guide/nice/index.html"):
        repair_french_punctuation(rel)
    verify_assets()
    print("Destination family: 8 pages, one Hotel Fit bridge each; FR/EN activity-card hooks verified.")

if __name__ == "__main__":
    main()
