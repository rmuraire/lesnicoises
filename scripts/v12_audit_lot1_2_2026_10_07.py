#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit - lots 1 and 2, 7 Oct 2026.

High-confidence structural / visual fixes from Claude's final pre-distribution audit.
Runs late in the build, after v11, so earlier generators cannot reintroduce these defects.
No factual research is invented here: stale practical facts and missing culture logistics
that need source verification are handled separately.
"""
from pathlib import Path
import re, html

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup","lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def read(rel):
    p=ROOT/rel
    return p,p.read_text(encoding="utf-8",errors="ignore")

def write(rel,fn):
    p,s=read(rel)
    n=fn(s)
    if n!=s:
        p.write_text(n,encoding="utf-8")
        print("patched",rel)
    else:
        print("unchanged",rel)

# B3 / C14: never inject a second must-see section when the HTML already has one.
def patch_editorial_layer(s):
    old='''  function renderMustSee(data) {
    var body = document.querySelector(".article-body") || document.querySelector("article.article");
    if (!body || body.querySelector("[data-mametas-must-see]")) return;'''
    new='''  function renderMustSee(data) {
    var body = document.querySelector(".article-body") || document.querySelector("article.article");
    if (document.querySelector(".city-must-list")) return;
    if (!body || body.querySelector("[data-mametas-must-see]")) return;'''
    if old in s:
        s=s.replace(old,new,1)
    elif 'document.querySelector(".city-must-list")' not in s:
        raise RuntimeError("editorial-layer renderMustSee anchor not found")
    return s
write("assets/editorial-layer.js",patch_editorial_layer)

# B3: make the French static must-see list the #indispensables anchor where present.
for rel in (
    "riviera-guide/nice/index.html",
    "riviera-guide/villefranche-cap-ferrat/index.html",
    "riviera-guide/antibes/index.html",
    "riviera-guide/monaco/index.html",
    "riviera-guide/menton/index.html",
):
    def add_anchor(s):
        if 'class="city-must-list"' in s and 'id="indispensables"' not in s:
            s=s.replace('class="city-must-list"','class="city-must-list" id="indispensables"',1)
        return s
    write(rel,add_anchor)

# B4: literal regex backreference leaked into Cannes beach headings.
for rel in ("en/beaches/cannes/index.html","plages/cannes/index.html"):
    write(rel,lambda s:s.replace("<h3\\1>","<h3>").replace("</h3\\1>","</h3>"))

# B5: use the already-proven local Lérins image used by the day-trip page.
for rel in ("en/good-finds/what-to-book/index.html","bons-plans/que-reserver/index.html"):
    write(rel,lambda s:s.replace(
        "/assets/editorial/iles-de-lerins-bruno-attuyt.webp",
        "/assets/editorial/iles-lerins.jpg"
    ))

# B14: one compact agenda module on each homepage; no September 2026 cards.
def homepage_agenda(s,fr=False):
    if fr:
        replacement='''<section class="v3-section now-section" id="maintenant"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">AGENDA DE LA RIVIERA</p><h2>Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier.</h2></div><p>Les grands événements changent les tarifs, la circulation et les disponibilités. Gardez les dates qui comptent avant de réserver.</p></div><div class="now-grid"><a class="now-card" href="/bons-plans/"><time>À venir</time><h3>Voir l’agenda de la Riviera</h3><p>Dates officielles, implications pratiques et liens utiles, mis à jour sans remplir la page pour remplir la page.</p></a></div></div></section>'''
    else:
        replacement='''<section class="v3-section now-section" id="now"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">RIVIERA AGENDA</p><h2>Carnival, MIPIM, Ironman. The Riviera has its own calendar.</h2></div><p>Big events change rates, traffic and availability. Keep the dates that matter in view before you book.</p></div><div class="now-grid"><a class="now-card" href="/en/good-finds/"><time>Coming up</time><h3>Open the Riviera agenda</h3><p>Official dates, practical implications and useful links, kept current without padding the calendar.</p></a></div></div></section>'''
    pat=re.compile(r'<section class="v3-section now-section"[^>]*>[sS]*?</section>',re.I)
    n,count=pat.subn(replacement,s,count=1)
    return n if count else s
write("index.html",lambda s:homepage_agenda(s,False))
write("fr/index.html",lambda s:homepage_agenda(s,True))

# B15/C16: French non-breaking punctuation on visible text nodes only.
# U+202F before ? ! ; » ; U+00A0 before : and after «.
def protect_blocks(s):
    blocks=[]
    pat=re.compile(r'<(script|style)[^>]*>[sS]*?</\1>',re.I)
    def repl(m):
        key=f"__PROTECTED_{len(blocks)}__"
        blocks.append(m.group(0))
        return key
    return pat.sub(repl,s),blocks

def restore(s,blocks):
    for i,b in enumerate(blocks):
        s=s.replace(f"__PROTECTED_{i}__",b)
    return s

def french_text_node(t):
    # Existing spaces (ordinary, NBSP or narrow NBSP) are normalized to the house rule.
    t=re.sub(r'[ \u00a0\u202f]+([?!;»])', '\u202f\\1', t)
    t=re.sub(r'[ \u00a0\u202f]+:', '\u00a0:', t)
    t=re.sub(r'«[ \u00a0\u202f]*', '«\u00a0', t)
    t=t.replace("'","’")
    # English smart quotes leaking into FR visible text.
    t=t.replace("“","«\u00a0").replace("”","\u202f»")
    for a,b in (("coeur","cœur"),("Coeur","Cœur"),("oeuvre","œuvre"),("Oeuvre","Œuvre"),("oeuvres","œuvres"),("Oeuvres","Œuvres"),("oeil","œil"),("Oeil","Œil")):
        t=re.sub(rf'\b{a}\b',b,t)
    return t

def normalize_fr_html(s):
    if not re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I):
        return s
    protected,blocks=protect_blocks(s)
    parts=re.split(r'(<[^>]+>)',protected)
    for i in range(0,len(parts),2):
        parts[i]=french_text_node(parts[i])
    return restore("".join(parts),blocks)

for p in ROOT.rglob("*.html"):
    rel=p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in SKIP: continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    n=normalize_fr_html(s)
    if n!=s:
        p.write_text(n,encoding="utf-8")

# B6 B7 B8 B9 B13 + C1 C3 C6 C7 C8 C20 as one shared CSS layer.
css_path=ROOT/"assets/mametas-shell-v1.css"
css=css_path.read_text(encoding="utf-8")
token="/* Claude final audit lots 1-2 — 2026-10-07 */"
if token not in css:
    css+=r'''

/* Claude final audit lots 1-2 — 2026-10-07 */

/* B6: cross-promo links must remain readable on their light card. */
body.rg-destination .verdict.ux-cross-promo a{
  color:#14213D!important;
  text-decoration:underline!important;
}

/* B7: destination next-decision copy cannot inherit cream-on-cream verdict colours. */
body.rg-destination .verdict:not(.ux-cross-promo) .label,
body.rg-destination .verdict:not(.ux-cross-promo) h2,
body.rg-destination .verdict:not(.ux-cross-promo) strong{
  color:inherit;
}

/* B8 */
.rg-legacy .mametas-checked{
  max-width:100%!important;
  box-sizing:border-box!important;
  white-space:normal!important;
}

/* B9 */
@media(max-width:700px){
  body.about-page h1,
  body.page-about h1,
  .about-hero h1{
    font-size:clamp(34px,9vw,51px)!important;
    overflow-wrap:break-word!important;
    hyphens:auto;
  }
}

/* C1 / B13: one rule-card and facts primitive outside intent-detail. */
.verdict:not(.ux-cross-promo){
  margin:32px 0;
  padding:24px 28px;
  background:#14213D;
  color:#FFFDF8;
}
.verdict:not(.ux-cross-promo) .label{
  display:block;
  margin:0 0 10px;
  font:700 11px/1.3 Inter,sans-serif;
  letter-spacing:.14em;
  text-transform:uppercase;
  color:#F7C966;
}
.verdict:not(.ux-cross-promo) p{
  margin:0 0 12px;
  font-family:var(--serif,"Fraunces",Georgia,serif);
  font-size:20px;
  line-height:1.45;
  color:#FFFDF8;
}
.verdict:not(.ux-cross-promo) p:last-child{margin-bottom:0}
.fact-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:10px;
  margin:0 0 36px;
}
.fact{
  padding:18px;
  border:1px solid rgba(20,33,61,.14);
  background:rgba(255,253,248,.5);
}
.fact b{
  display:block;
  margin-bottom:6px;
  font:600 11px/1.3 Inter,sans-serif;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:#7A5B1B;
}
.fact span{
  display:block;
  font-family:var(--serif,"Fraunces",Georgia,serif);
  font-size:20px;
  line-height:1.25;
  color:#14213D;
}
/* Practical cards in V3 destinations remain light. */
body.rg-destination .culture-practical .verdict,
body.rg-destination .ux-contained-practical .verdict{
  background:#FFFDF8!important;
  color:#14213D!important;
  border:1px solid rgba(122,91,27,.35)!important;
}
body.rg-destination .culture-practical .verdict .label,
body.rg-destination .ux-contained-practical .verdict .label{
  color:#7A5B1B!important;
}
body.rg-destination .culture-practical .verdict p,
body.rg-destination .ux-contained-practical .verdict p{
  color:#14213D!important;
  font-family:Inter,sans-serif!important;
  font-size:16px!important;
}

/* C3: long serif decision copy must not become display typography. */
.verdict-box p,
.decision-first,
.traveller-voice blockquote{
  font-size:20px!important;
  line-height:1.5!important;
}
@media(max-width:700px){
  .fact-grid{grid-template-columns:1fr}
  .verdict:not(.ux-cross-promo) p,
  .verdict-box p,
  .decision-first,
  .traveller-voice blockquote{font-size:18px!important}
}

/* C6: minimum readable sizes. */
.hotel-hero-media figcaption,
.culture-hero figcaption,
.article-visual figcaption{font-size:12px!important;line-height:1.45!important}
.source-box,
.sources,
.sources li,
.source-list,
.source-list li,
.affiliate-note,
.affiliate-disclosure,
.traveller-voice-method,
.home-hotel-voice-method,
.solo-voices-method,
.phase4-budget-grid small,
.style-nav small{font-size:12px!important;line-height:1.5!important}
.chooser-option,
.chooser-option span,
.hotel-engine-choice,
.hotel-engine-choice span,
.engine-base-gate,
.engine-note{font-size:14px!important;line-height:1.45!important}

/* C7 */
.tag,
.eyebrow.terracotta,
.address,
.place-link,
.gold,
.terracotta{color:#7A5B1B}
a.place-link{color:#14213D!important}

/* C8: tactile text links on mobile. */
@media(max-width:700px){
  a.place-link,
  .style-nav a,
  .duration-switch a,
  .plan-duration a,
  .link-cta{
    display:inline-flex;
    align-items:center;
    min-height:44px;
  }
}

/* C20: footer cookie control and disabled Riviera Fit action. */
.v3-footer [data-cookie-settings],
.v3-footer .cookie-choices,
footer [data-cookie-settings],
footer .cookie-choices{
  font-size:12px!important;
  line-height:1.4!important;
}
[data-chooser-submit]:disabled{
  color:#14213D!important;
  background:#E4E1DA!important;
  border-color:#E4E1DA!important;
  opacity:1!important;
}
@media(max-width:700px){
  [data-chooser-submit]{white-space:nowrap!important;font-size:12px!important}
}

/* C19 early safety: keep prose readable on wide screens. */
.article-body>p,
.intent-detail>p,
.content-wrap>p,
.hotel-fit-page p,
.plan-page p{max-width:68ch}
'''
    css_path.write_text(css,encoding="utf-8")
    print("patched assets/mametas-shell-v1.css")

# Basic invariants for this lot.
editorial=(ROOT/"assets/editorial-layer.js").read_text(encoding="utf-8")
if 'document.querySelector(".city-must-list")' not in editorial:
    raise RuntimeError("B3 guard missing")
for rel in ("en/beaches/cannes/index.html","plages/cannes/index.html"):
    s=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
    if "<h3\\1>" in s:
        raise RuntimeError(f"B4 survived: {rel}")
for rel in ("en/good-finds/what-to-book/index.html","bons-plans/que-reserver/index.html"):
    s=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
    if "iles-de-lerins-bruno-attuyt.webp" in s:
        raise RuntimeError(f"B5 survived: {rel}")
for rel in ("index.html","fr/index.html"):
    s=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
    if "september-2026" in s or "septembre-2026" in s:
        raise RuntimeError(f"B14/B10 stale homepage agenda survived: {rel}")

print("Claude final audit lots 1-2 structural pass completed.")
