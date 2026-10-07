#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit, lot 2: shared components and CTA system.

Order follows Claude: C14 first, then shared rule/fact styles (C1 is completed
by lot 1), buttons, FAQ, large serif text, hotel-card action styling, text
floors, contrast and tap targets. Structural hotel-card content gaps stay for
lot 4, where page-by-page hotel parity is handled.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

def rw(rel, fn):
    p=ROOT/rel
    s=p.read_text(encoding="utf-8",errors="ignore")
    n=fn(s)
    if n!=s:
        p.write_text(n,encoding="utf-8"); print("patched",rel)
    else:
        print("unchanged",rel)

def patch_runtime_duplicates():
    # C14: homepage already has the image-led "Ten reasons..." module after
    # the build. Do not let journey-layer add a second 10-experience section.
    def journey(s):
        marker="data-static-home-experiences"
        if marker in s: return s
        anchor='    if (!home || document.getElementById("riviera-first-trip-edit")) return;'
        if anchor not in s: raise RuntimeError("C14 homepage journey anchor missing")
        repl=anchor+'\n    if (Array.from(document.querySelectorAll("h2")).some(function (h) { return /ten reasons to look up|dix raisons|10 raisons/i.test(h.textContent || ""); })) return; // data-static-home-experiences'
        return s.replace(anchor,repl,1)
    rw("assets/journey-layer.js",journey)

    # practical-layer already guards .practical-decision-layer. Make the
    # intent explicit so future edits do not remove the dedupe.
    def practical(s):
        if "data-practical-dedupe-guard" in s: return s
        old="if(document.querySelector('.practical-decision-layer'))return true;"
        if old not in s: raise RuntimeError("C14 practical guard missing")
        return s.replace(old,"if(document.querySelector('.practical-decision-layer'))return true;/* data-practical-dedupe-guard */",1)
    rw("assets/practical-layer.js",practical)

def plain(html):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html)).strip()

def set_attr(attrs,name,value):
    pat=re.compile(rf'\s{name}=["\'][^"\']*["\']',re.I)
    if pat.search(attrs):
        return pat.sub(f' {name}="{value}"',attrs,1)
    return attrs+f' {name}="{value}"'

def add_classes(attrs,*classes):
    m=re.search(r'\sclass=["\']([^"\']*)["\']',attrs,re.I)
    existing=m.group(1).split() if m else []
    for c in classes:
        if c not in existing: existing.append(c)
    value=" ".join(existing)
    if m:
        return attrs[:m.start()]+f' class="{value}"'+attrs[m.end():]
    return attrs+f' class="{value}"'

def normalize_anchor(m,fr,preserve_riviera=False):
    attrs,inner=m.group(1),m.group(2)
    hm=re.search(r'href=["\']([^"\']+)["\']',attrs,re.I)
    if not hm: return m.group(0)
    href=hm.group(1)
    label=plain(inner)
    low=label.lower()
    href_low=href.lower()
    has_img="<img" in inner.lower()
    cm=re.search(r'\sclass=["\']([^"\']*)["\']',attrs,re.I)
    anchor_classes=set(cm.group(1).split()) if cm else set()
    structural_link=bool(anchor_classes.intersection({
        "practical-link","decision-card","base-card","place-card","stay-card",
        "home-experience-card","home-journey-step","chooser-hotel-card"
    }))

    affiliate=any(x in href_low for x in (
        "booking.com","kqzyfj.com","expedia.","getyourguide.","gyg.me"
    ))
    cta_like=bool(re.search(r'check|rate|date|availability|book|tarif|disponib|réserv|reserv|getyourguide|expedia|booking',low,re.I))

    if affiliate and not has_img and cta_like:
        attrs=add_classes(attrs,"btn","btn--affiliate")
        attrs=set_attr(attrs,"target","_blank")
        attrs=set_attr(attrs,"rel","sponsored nofollow noopener")
        if "getyourguide" in href_low or "gyg.me" in href_low:
            inner="Voir les disponibilités sur GetYourGuide ↗" if fr else "Check availability on GetYourGuide ↗"
        elif "expedia" in href_low:
            inner="Voir les tarifs sur Expedia ↗" if fr else "Check rates on Expedia ↗"
        elif "booking" in href_low or "kqzyfj" in href_low:
            inner="Voir les tarifs sur Booking.com ↗" if fr else "Check rates on Booking.com ↗"
        return f"<a{attrs}>{inner}</a>"

    # Internal Mametas hotel review link.
    if re.match(r'^/(?:en/)?hotels/[^/]+/[^/]+/?$',href):
        review_labels=(
            "read our full review","read full review","our take","read our take",
            "see our full take","see the hotel","voir notre avis complet","notre avis",
            "lire notre avis","voir notre avis","voir l’hôtel","voir l'hotel"
        )
        if any(x in low for x in review_labels):
            attrs=add_classes(attrs,"btn","btn--primary")
            inner="Lire notre avis" if fr else "Read our take"
            return f"<a{attrs}>{inner}</a>"

    # Tool launch labels.
    if (not structural_link) and (not preserve_riviera) and re.match(r'^/(?:en/)?(?:riviera-fit|riviera-chooser)/',href):
        if any(x in low for x in ("riviera fit","riviera chooser","chooser")):
            attrs=add_classes(attrs,"btn","btn--primary")
            inner="Tester Riviera Fit" if fr else "Try Riviera Fit"
            return f"<a{attrs}>{inner}</a>"
    if (not structural_link) and re.match(r'^/(?:en/)?hotels/finder/',href):
        if any(x in low for x in ("hotel fit","matcher","shortlist")):
            attrs=add_classes(attrs,"btn","btn--primary")
            inner="Tester Hotel Fit" if fr else "Try Hotel Fit"
            return f"<a{attrs}>{inner}</a>"

    # External map/source arrows.
    if href.startswith("http") and ("google.com/maps" in href_low or "maps.app.goo.gl" in href_low):
        if "google maps" in low or "open map" in low or "ouvrir la carte" in low:
            attrs=add_classes(attrs,"link-cta")
            inner="Google Maps ↗"
            return f"<a{attrs}>{inner}</a>"

    return m.group(0)

FAQ_PAGES={
 "en/gay-nice/index.html","guide-gay-nice/index.html",
 "en/gay-french-riviera/where-to-stay/index.html","cote-dazur-gay/ou-dormir/index.html",
 "en/gay-french-riviera/beaches-without-a-car/index.html","cote-dazur-gay/plages-sans-voiture/index.html",
}

def convert_open_faq(s):
    # Convert consecutive legacy FAQ .place blocks only when immediately after H2 FAQ.
    hm=re.search(r'<h2[^>]*>\s*FAQ\s*</h2>',s,re.I)
    if not hm: return s
    pos=hm.end()
    items=[]
    cursor=pos
    pat=re.compile(r'\s*<div class=["\']place["\']>\s*<h3>([\s\S]*?)</h3>\s*<p class=["\']why["\']>([\s\S]*?)</p>\s*</div>',re.I)
    while True:
        m=pat.match(s,cursor)
        if not m: break
        q=m.group(1).strip(); a=m.group(2).strip()
        items.append(f'<details class="faq-item"><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>')
        cursor=m.end()
    if not items: return s
    block='<div class="faq-list">'+"".join(items)+'</div>'
    return s[:pos]+block+s[cursor:]

def patch_html_components():
    count=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        fr=bool(re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I))
        preserve_riviera = "/riviera-guide/" in ("/" + rel.as_posix())
        s=re.sub(r'<a\b([^>]*)>([\s\S]*?)</a>',lambda m:normalize_anchor(m,fr,preserve_riviera),s,flags=re.I)
        # B14 exact live headline variants still present in the Oct 7 crawl.
        s=s.replace("Carnival, Ironman, an exhibition closing soon. The Riviera runs on its own calendar.",
                    "Carnival, MIPIM, Ironman. The Riviera has its own calendar.")
        s=s.replace("Carnaval, Ironman, une expo qui ferme bientôt. La Riviera a son propre calendrier.",
                    "Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier.")
        if rel.as_posix() in FAQ_PAGES:
            s=convert_open_faq(s)
        if s!=old:
            p.write_text(s,encoding="utf-8"); count+=1
    print("lot2 HTML components changed",count,"files")

def patch_css():
    rel="assets/mametas-shell-v1.css"
    p=ROOT/rel; s=p.read_text(encoding="utf-8"); old=s
    token="/* Claude final audit lot 2 — shared components — 2026-10-07 */"
    if token not in s:
        s += r'''

/* Claude final audit lot 2 — shared components — 2026-10-07 */
/* One CTA system. Legacy classes inherit the geometry while HTML is migrated. */
.btn,
a.rate-link,
a.hotel-card-cta,
a.hotel-card-take,
a.cta-button,
a.mametas-activity-cta{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:8px!important;
  min-height:44px!important;
  padding:0 20px!important;
  box-sizing:border-box!important;
  border-radius:0!important;
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;
  font-size:12px!important;
  font-weight:700!important;
  line-height:1.2!important;
  letter-spacing:.08em!important;
  text-transform:uppercase!important;
  text-decoration:none!important;
}
.btn--primary{background:#14213D!important;border:1px solid #14213D!important;color:#FFFDF8!important}
.btn--secondary,.btn--affiliate{background:transparent!important;border:1px solid #14213D!important;color:#14213D!important}
a.btn--affiliate{white-space:normal!important}

/* C2: one readable FAQ visual language, including converted legacy gay FAQs. */
.faq-list{margin:18px 0 42px;border-top:1px solid rgba(20,33,61,.16)}
.faq-item{border-bottom:1px solid rgba(20,33,61,.16)}
.faq-item>summary{
  min-height:52px;
  padding:15px 34px 15px 0;
  display:flex;
  align-items:center;
  position:relative;
  cursor:pointer;
  list-style:none;
  color:#14213D;
  font-family:var(--mg-serif,var(--serif,Georgia,serif));
  font-size:18px;
  font-weight:600;
  line-height:1.35;
}
.faq-item>summary::-webkit-details-marker{display:none}
.faq-item>summary::after{content:"+";position:absolute;right:4px;top:50%;transform:translateY(-50%);font-family:Inter,sans-serif;font-size:18px}
.faq-item[open]>summary::after{content:"−"}
.faq-answer{padding:0 0 18px}
.faq-answer p{max-width:68ch!important;margin:0!important;font-family:Inter,sans-serif!important;font-size:16px!important;line-height:1.6!important}

/* C3: oversized serif prose belongs to display headings, not long explanations. */
.verdict-box p,
.decision-first,
.traveller-voice blockquote{
  font-size:20px!important;
  line-height:1.5!important;
}
body.rg-destination .verdict p{font-size:20px!important}
@media(max-width:700px){
  .verdict-box p,.decision-first,.traveller-voice blockquote,
  body.rg-destination .verdict p{font-size:18px!important}
}
body.nice-or-cannes .standfirst,
.nice-or-cannes .standfirst{font-size:20px!important;line-height:1.55!important}

/* C4: shared hotel-card visual grammar. Structural/missing-card content is lot 4. */
.hotel-card img,
.hotel-card-media img,
.hotel-choice-card img,
.hotel-pick-card img{
  width:100%!important;
  aspect-ratio:3/2!important;
  object-fit:cover!important;
}
.hotel-card h3,.hotel-choice-card h3,.hotel-pick-card h3{
  font-family:var(--mg-serif,var(--serif,Georgia,serif))!important;
  font-size:24px!important;
  line-height:1.12!important;
}
.hotel-card-actions{display:flex!important;flex-wrap:wrap!important;gap:8px!important;margin-top:14px!important}
@media(max-width:640px){.hotel-card-actions{display:grid!important;grid-template-columns:1fr!important}.hotel-card-actions .btn{width:100%!important}}

/* C6: readable minimums. */
.hotel-hero-media figcaption,
.culture-hero figcaption,
.article-cover figcaption,
.source-box,.source-box li,.sources,.sources li,
.affiliate-inline,.affiliate-note,
.traveller-voice-method,.home-hotel-voice-method,.solo-voices-method,
.style-nav small,.phase4-budget-grid small{
  font-size:12px!important;
  line-height:1.5!important;
}
.chooser-option,.chooser-answer,.engine-option,.engine-answer,
.chooser-step label,.hotel-fit-page label{
  font-size:14px!important;
}
@media(max-width:600px){
  .mood-card p,.by-mood-card p,.explore-mood-card p{
    font-size:14px!important;
    line-height:1.5!important;
  }
}

/* C7: accessible text accents on pale backgrounds. */
a.place-link{color:#7A5B1B!important}
.article-body .address,
.article-body .kicker,
.article-body .label:not(.verdict .label){
  color:#A3452D;
}

/* C8: mobile tap targets. */
a.place-link,.plan-switcher a,.duration-switcher a,.link-cta{
  display:inline-flex!important;
  align-items:center!important;
  min-height:44px!important;
  box-sizing:border-box!important;
  padding-top:12px!important;
  padding-bottom:12px!important;
}
'''
    p.write_text(s,encoding="utf-8"); print("patched",rel)
    return

def validate():
    journey=(ROOT/"assets/journey-layer.js").read_text(encoding="utf-8",errors="ignore")
    practical=(ROOT/"assets/practical-layer.js").read_text(encoding="utf-8",errors="ignore")
    css=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8",errors="ignore")
    if "data-static-home-experiences" not in journey: raise RuntimeError("C14 home dedupe missing")
    if "data-practical-dedupe-guard" not in practical: raise RuntimeError("C14 practical dedupe guard missing")
    for token in ("faq-item","btn--affiliate","a.place-link",".traveller-voice blockquote"):
        if token not in css: raise RuntimeError("lot2 CSS token missing: "+token)
    for rel in FAQ_PAGES:
        p=ROOT/rel
        if p.exists():
            t=p.read_text(encoding="utf-8",errors="ignore")
            if re.search(r'<h2[^>]*>\s*FAQ\s*</h2>\s*<div class=["\']place["\']>',t,re.I):
                raise RuntimeError("legacy open FAQ survived: "+rel)
    print("Claude final audit lot 2 component validation passed.")

def main():
    patch_runtime_duplicates()
    patch_html_components()
    patch_css()
    validate()

if __name__=="__main__":
    main()
