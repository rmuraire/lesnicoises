#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-10 family QA: Hotel Fit placement + editorial reference/nav semantics.

Late pass (after v27 / v28), scope limited to 18 Riviera Guide city pages.
V3 article-body guides keep their single v27 bridge; older Nice/Cannes guides
get the same one-CTA accommodation contract. No Booking/GYG URLs are edited.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CITIES = ("nice","cannes","antibes","villefranche-cap-ferrat","monaco",
          "menton","eze","saint-paul-de-vence","saint-tropez")
FINDER = re.compile(r'href=["\']/(?:en/)?hotels/finder/(?:\?[^"\']*)?["\']', re.I)
H2 = re.compile(r'<h2\b[^>]*>[\s\S]*?</h2>', re.I)
PROMO_PARAGRAPH = re.compile(r'<p\b[^>]*>[\s\S]*?</p>', re.I)
PROMO_DIV = re.compile(r'<div\b[^>]*class=["\'][^"\']*(?:destination-hotel-fit-cta|destination-hotel-fit-bridge|hotel-fit-cta|editorial-tool-bridge)[^"\']*["\'][^>]*>[\s\S]*?</div>',re.I)
SOURCES = re.compile(r'<div\b[^>]*class=["\']source-box["\'][^>]*>([\s\S]*?)</div>',re.I)
DESTINATION_FIT = re.compile(r'data-mametas-destination-fit=["\']one["\']',re.I)

def label(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip().lower()

def patch_sources(s):
    def classify(m):
        inside=m.group(1)
        low=label(inside)
        if low.startswith(("checked sources", "sources vérifiées", "sources verifiees")):
            # A new class containing "sources" is a formal sources block.
            # The global coherence gate requires an exact h2, not just a
            # <strong> label. Promote the label once and preserve every URL.
            fr_source = low.startswith(("sources vérifiées", "sources verifiees"))
            heading = "Sources vérifiées" if fr_source else "Sources checked"
            links = re.sub(r'^\s*<strong\b[^>]*>[\s\S]*?</strong>\s*', "", inside, count=1, flags=re.I)
            return ('<div class="destination-verified-sources">'
                    f'<h2>{heading}</h2><p>{links.strip()}</p></div>')
        if low.startswith(("continue:", "continuer", "the next decision", "prochaine décision")):
            return '<div class="destination-next-links">'+inside+'</div>'
        return m.group(0)
    return SOURCES.sub(classify,s)

def fix_city(slug, fr):
    rel=("riviera-guide/" if fr else "en/riviera-guide/")+slug+"/index.html"
    file=ROOT/rel
    original=file.read_text(encoding="utf-8")
    s=patch_sources(original)
    # Preserve V3 guides already normalized by v27 (eight EN/FR pages).
    if DESTINATION_FIT.search(s):
        if len(FINDER.findall(s)) != 1:
            raise RuntimeError(f"{rel}: duplicate Hotel Fit links on V3 guide")
    else:
        opening=re.search(r'<article\b[^>]*>',s,re.I)
        if not opening: raise RuntimeError(f"{rel}: article element missing")
        closing=s.find("</article>",opening.end())
        if closing<0: raise RuntimeError(f"{rel}: article closing boundary missing")
        article=s[opening.end():closing]
        present=len(FINDER.findall(article))
        must_add=slug in ("nice","cannes")
        if present or must_add:
            # Remove the previous isolated button and its enclosing tool promo.
            article=PROMO_DIV.sub(lambda m:"" if FINDER.search(m.group(0)) else m.group(0),article)
            article=PROMO_PARAGRAPH.sub(
                lambda m:"" if FINDER.search(m.group(0)) and re.search(r'hotel fit|hotel finder|trouver.*hôtel',m.group(0),re.I) else m.group(0),article)
            if FINDER.search(article):
                # Some late materializers wrap the tool CTA in an otherwise
                # unrecognised <div>/<aside> instead of a paragraph. Remove
                # ONLY its hotel-finder anchor, never sibling editorial links
                # or Booking/GetYourGuide affiliate destinations. We insert
                # precisely one canonical CTA below.
                finder_anchor = re.compile(
                    r"""<a\b(?=[^>]*\bhref=["']/(?:en/)?hotels/finder/(?:\?[^"']*)?["'])[^>]*>[\s\S]*?</a>""",
                    re.I,
                )
                original_count = len(FINDER.findall(article))
                article, removed = finder_anchor.subn("", article)
                if removed != original_count or FINDER.search(article):
                    raise RuntimeError(
                        f"{rel}: unsafe hotel-finder promo cleanup "
                        f"({removed} of {original_count} anchors removed)"
                    )
                # Remove now-empty CTA wrappers only. Do not delete
                # explanatory paragraphs or unrelated editorial content.
                article = re.sub(
                    r'<(?P<tag>p|div|aside)\b[^>]*>\s*</(?P=tag)>',
                    '', article, flags=re.I
                )
            headings=list(H2.finditer(article))
            stay=None
            for h in headings:
                text=label(h.group(0))
                if fr:
                    good=("où dormir" in text or "dormir à cannes" in text or
                          "faut-il dormir" in text or "dormir sur place" in text)
                else:
                    good=("where to stay" in text or "should you stay in cannes" in text or
                          "should you stay overnight" in text)
                if good:
                    stay=h
                    break
            if stay:
                following=next((h for h in headings if h.start()>stay.end()),None)
                point=following.start() if following else len(article)
            else:
                sources=re.search(r'<div\b[^>]*class=["\']sources\b',article,re.I)
                point=sources.start() if sources else len(article)
            url=("/hotels/finder/" if fr else "/en/hotels/finder/")+"?base="+slug
            text=("Comparez les hôtels sélectionnés selon votre budget et vos priorités."
                  if fr else "Compare our selected hotels by budget and what matters most.")
            action="Tester Hotel Fit" if fr else "Try Hotel Fit"
            bridge=('<div class="destination-hotel-fit-single" data-mametas-destination-fit="one">'
                    f'<p>{text}</p><a class="destination-hotel-fit-action" href="{url}">{action}</a></div>\n')
            article=article[:point]+bridge+article[point:]
            if len(FINDER.findall(article))!=1:
                raise RuntimeError(f"{rel}: expected precisely one Hotel Fit CTA")
            s=s[:opening.end()]+article+s[closing:]
    # This is the LAST content pass in production. Older guides and the
    # later source-box normalizer do not always preserve an exact heading.
    # Match the same sources class condition as the global coherence gate,
    # in BOTH languages. Keep all source links and avoid duplicate headings.
    formal_sources = re.search(
        r"""<div\b[^>]*class=["'][^"']*sources[^"']*["'][^>]*>""", s, re.I
    )
    canonical = "Sources vérifiées" if fr else "Sources checked"
    if formal_sources and f"<h2>{canonical}</h2>" not in s:
        start = formal_sources.end()
        next_heading = re.match(r"\s*<h2\b[^>]*>[\s\S]*?</h2>", s[start:], re.I)
        if next_heading:
            s = (s[:start] + f"<h2>{canonical}</h2>" +
                 s[start + next_heading.end():])
        else:
            s = (s[:start] + f"<h2>{canonical}</h2>" + s[start:])
    if formal_sources and f"<h2>{canonical}</h2>" not in s:
        raise RuntimeError(f"{rel}: missing canonical sources heading")
    if s!=original:
        file.write_text(s,encoding="utf-8")
    # Only the 6 destinations with Hotel Fit placement requirements are
    # contractually required to have exactly one link; other destinations
    # retain a CTA only if they already had an explicit Hotel Fit promo.
    if slug in ("nice","cannes","antibes","villefranche-cap-ferrat","monaco","menton"):
        main=s.split("</article>",1)[0]
        count=len(FINDER.findall(main))
        if count!=1:
            raise RuntimeError(f"{rel}: expected one Hotel Fit CTA in article, found {count}")
    print("Guide family checked:",rel)

def main():
    for city in CITIES:
        for fr in (False,True):
            fix_city(city,fr)
    js=(ROOT/"assets/practical-layer.js").read_text(encoding="utf-8")
    for marker in ("Three practical decisions","Trois décisions pratiques"):
        if marker not in js: raise RuntimeError("Practical block heading missing: "+marker)
    css=(ROOT/"assets/mametas-foundation.css").read_text(encoding="utf-8")
    for marker in ("ONE DESTINATION SYSTEM",".destination-next-links",".mametas-activity-inline .mametas-activity-copy"):
        if marker not in css: raise RuntimeError("Family CSS contract missing: "+marker)
    print("ALL 18 RIVIERA GUIDE SUBPAGES CHECKED")

if __name__=="__main__":
    main()
