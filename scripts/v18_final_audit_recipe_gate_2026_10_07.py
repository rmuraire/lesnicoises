#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static release gate derived from Claude's 24-point final recipe.

This runs after all final-audit transformation scripts. It does not pretend to
replace a real 390/1440 browser pass, but it makes the mechanically testable
parts non-regressive and prints actionable failures.
"""
from pathlib import Path
from urllib.parse import urlparse
import html as htmlmod
import re
import os

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def public_html():
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        yield p,rel

def visible_text(s):
    s=re.sub(r'<(script|style)\b[^>]*>[\s\S]*?</\1>',' ',s,flags=re.I)
    s=re.sub(r'<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',htmlmod.unescape(s)).strip()

errors=[]
warnings=[]
SKIP_MATERIALIZED=os.environ.get("MAMETAS_SKIP_MATERIALIZED")=="1"

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

# 1 homepage hero local and single editorial module.
for rel in ("index.html","fr/index.html"):
    p=ROOT/rel
    if not p.exists(): err("homepage missing "+rel); continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    if "mametas-home-hero-2026-09-11.PNG" not in s:
        err("homepage hero not restored: "+rel)
    if "mametas-five-women-hero-960.webp" in s:
        err("bad hero derivative still referenced: "+rel)

# 2/24 script dedupe guards.
for rel,toks in {
    "assets/editorial-layer.js":('document.querySelector(".city-must-list")',),
    "assets/journey-layer.js":("data-static-next-decision","data-static-home-experiences"),
    "assets/practical-layer.js":("data-practical-dedupe-guard",),
}.items():
    p=ROOT/rel
    if not p.exists(): err("missing shared script "+rel); continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    for tok in toks:
        if tok not in s: err(f"{rel}: missing dedupe guard {tok}")

# 5 Cannes beach leaked regex tokens.
for rel in ("en/beaches/cannes/index.html","plages/cannes/index.html"):
    p=ROOT/rel
    if p.exists() and "\\1" in p.read_text(encoding="utf-8",errors="ignore"):
        err(rel+": leaked regex backreference survives")

# 6/7 Hotel Fit.
engine=(ROOT/"assets/hotel-engine.js").read_text(encoding="utf-8",errors="ignore")
for tok in ("invalidDetailPaths","hotel-west-end-nice-promenade","Aucune correspondance exacte."):
    if tok not in engine: err("Hotel Fit missing token: "+tok)
for bad in ("Aucun match exact."," — clearly flagged"," - with the trade-offs"):
    if bad in engine: err("Hotel Fit stale wording survives: "+bad)

# 8 Riviera Fit no-car ambitious wording.
chooser=(ROOT/"assets/riviera-chooser.js").read_text(encoding="utf-8",errors="ignore")
if "avec la meilleure liaison disponible" not in chooser:
    err("Riviera Fit FR ambitious/no-car wording not fixed")
if "Moyenne: relief + budget" in chooser:
    err("Riviera Fit FR colon spacing stale")

# Global rendered-text checks.
bad_commas=[]
remote_wiki=[]
placeholders=[]
stale_dates=[]
dash_pages=[]
fr_spaces=[]
affiliate_title_photo=[]
h1_h3=[]
repeat_templates=[]
for p,rel in public_html():
    s=p.read_text(encoding="utf-8",errors="ignore")
    txt=visible_text(s)
    rp=rel.as_posix()

    if "commons.wikimedia.org" in s or "upload.wikimedia.org" in s:
        remote_wiki.append(rp)
    # Broken punctuation only inside text nodes. Stripping tags with spaces
    # creates false positives around inline <strong>/<a> boundaries.
    node_source=re.sub(r'<(script|style)\b[^>]*>[\s\S]*?</\1>','',s,flags=re.I)
    nodes=re.split(r'(<[^>]+>)',node_source)
    comma_bad=False
    for ni in range(0,len(nodes),2):
        node=htmlmod.unescape(nodes[ni])
        if ", ," in node or ", ." in node or re.search(r'[ \t\u00a0\u202f]+,',node):
            comma_bad=True; break
    if comma_bad:
        bad_commas.append(rp)
    if "See official information below." in txt or "Voir les informations officielles ci-dessous." in txt:
        placeholders.append(rp)
    if re.search(r'\b(?:until|Until)\s+(?:27|28|30) September 2026\b',txt) or re.search(r'jusqu[’\']au\s+(?:27|28|30) septembre 2026',txt,re.I):
        stale_dates.append(rp)
    if " — " in txt or " – " in txt:
        dash_pages.append(rp)

    # 19 French punctuation spacing: ordinary ASCII space before French high punctuation.
    if re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I):
        # protect tags first and inspect text nodes only
        chunks=re.split(r'(<[^>]+>)',re.sub(r'<(script|style)\b[^>]*>[\s\S]*?</\1>','',s,flags=re.I))
        bad=False
        for i in range(0,len(chunks),2):
            if re.search(r' (?=[?!;»])| (?=:)',chunks[i]):
                bad=True; break
        if bad: fr_spaces.append(rp)

    # 13 affiliate interaction: title/photo must not itself be external reservation link.
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>',s,re.I):
        href=m.group(1).lower()
        body=m.group(2)
        if any(x in href for x in ("booking.com","kqzyfj.com","expedia.com","getyourguide")):
            if re.search(r'<img\b|<h[1-4]\b',body,re.I):
                affiliate_title_photo.append(rp); break

    # C9 diagnostic: first section heading after H1 is H3 before any H2.
    h1=re.search(r'</h1>',s,re.I)
    if h1:
        rest=s[h1.end():]
        m2=re.search(r'<h([23])\b',rest,re.I)
        if m2 and m2.group(1)=="3": h1_h3.append(rp)

    # C17 repeated template phrases: no phrase should repeat twice on one page.
    templ=[
      "Start with this logic, then compare the room and the real rate for your dates.",
      "Commencez par cette logique",
      "The shortlist is deliberately short.",
      "La shortlist est volontairement courte.",
      "Do not choose the room in isolation.",
      "Ne choisissez pas seulement la chambre",
      "Move the trip forward instead of climbing back to the menu.",
      "Faites avancer le voyage",
    ]
    if any(txt.count(t)>1 for t in templ):
        repeat_templates.append(rp)

if bad_commas: err("broken comma spacing/sequences: "+", ".join(bad_commas[:20]))
if remote_wiki and not SKIP_MATERIALIZED: err("remote Wikimedia survives: "+", ".join(remote_wiki[:30]))
elif remote_wiki: warn("remote Wikimedia check deferred to production materialisation")
if placeholders: err("culture logistics placeholders survive: "+", ".join(placeholders[:20]))
if stale_dates: err("past September dates still presented as current: "+", ".join(stale_dates[:20]))
if dash_pages: err("dash punctuation survives on "+str(len(dash_pages))+" pages: "+", ".join(dash_pages[:20]))
if fr_spaces: err("ordinary French spaces before high punctuation on "+str(len(fr_spaces))+" pages: "+", ".join(fr_spaces[:20]))
if affiliate_title_photo: err("hotel name/photo still links directly to reservation partner: "+", ".join(affiliate_title_photo[:30]))
if h1_h3: warn("H1→H3 hierarchy remains on "+str(len(h1_h3))+" pages: "+", ".join(h1_h3[:30]))
if repeat_templates: err("repeated C17 template copy survives: "+", ".join(repeat_templates[:20]))

# 12/14/15/22 CSS contract.
css=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8",errors="ignore")
for tok in (
    ".fact-grid",".verdict:not(.ux-cross-promo)",
    ".btn--affiliate","min-height:44px",
    "#7A5B1B","font-size:12px","font-size:14px",
    "max-width:68ch",".consent-settings",
    "[data-chooser-submit]:disabled",
):
    if tok not in css: err("shared CSS release token missing: "+tok)
if "border-radius:999px" in css:
    warn("pill radius remains somewhere in CSS; verify whether it is a non-button decorative pill")

# 17 hotel selection hreflang (materialised by v15 in production).
cities=("cannes","antibes","beaulieu-sur-mer","monaco","menton","mougins","saint-tropez","saint-paul-de-vence","villefranche-sur-mer")
if not SKIP_MATERIALIZED:
    for city in cities:
        for rel in (f"en/hotels/{city}/index.html",f"hotels/{city}/index.html"):
            p=ROOT/rel
            if not p.exists(): continue
            s=p.read_text(encoding="utf-8",errors="ignore")
            if 'hreflang="en"' not in s or 'hreflang="fr"' not in s:
                err("hreflang missing: "+rel)

# 20 hotel depth diagnostic. Only inspect actual hotel-detail pages.
short_hotels=[]
for p,rel in public_html():
    rp=rel.as_posix()
    if "/hotels/" not in "/"+rp or rp.endswith("/hotels/index.html"): continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    if 'class="hotel-detail' not in s and 'class="hotel-page' not in s: continue
    txt=visible_text(s).lower()
    lang_fr=bool(re.search(r'<html\b[^>]*lang=["\']fr',s,re.I))
    who=("who it suits" in txt) if not lang_fr else ("pour qui" in txt or "à qui il convient" in txt)
    mefi="mèfi" in txt
    sources=("sources" in txt)
    checked=("checked" in txt or "vérifi" in txt)
    budget=("budget" in txt)
    if not all((who,mefi,sources,checked,budget)):
        short_hotels.append((rp,who,mefi,sources,checked,budget))
if short_hotels:
    warn("hotel depth incomplete on "+str(len(short_hotels))+" materialised pages: "+repr(short_hotels[:16]))

# 23 affiliate disclosure diagnostic: more than one standard disclosure on a page.
multi_disclosure=[]
for p,rel in public_html():
    txt=visible_text(p.read_text(encoding="utf-8",errors="ignore"))
    n=txt.count("Selection stays editorial.")+txt.count("La sélection reste éditoriale.")
    if n>1: multi_disclosure.append(rel.as_posix())
if multi_disclosure:
    warn("multiple standard affiliate disclosures: "+", ".join(multi_disclosure[:20]))

print("FINAL RECIPE STATIC GATE")
for w in warnings: print("WARN:",w)
if errors:
    for e in errors: print("FAIL:",e)
    raise SystemExit(f"{len(errors)} final-recipe failure group(s)")
print("PASS: all mechanically enforceable critical recipe checks passed.")
