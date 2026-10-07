#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit, lot 1 (B1-B15), 7 Oct 2026.

Runs after v11. This pass is deliberately conservative: it fixes only the
blockers Claude identified as visibly broken before distribution, and it
fails closed when a known blocker survives.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".github", "scripts", "docs", "backup",
        "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2"}

def read(rel):
    p=ROOT/rel
    return p, p.read_text(encoding="utf-8",errors="ignore")

def write(rel,s,old):
    if s!=old:
        (ROOT/rel).write_text(s,encoding="utf-8")
        print("patched",rel)
    else:
        print("unchanged",rel)

def patch_runtime_layers():
    # B3: never inject a second must-see section when the static V3 list exists.
    rel="assets/editorial-layer.js"
    p,s=read(rel); old=s
    anchor='    var body = document.querySelector(".article-body") || document.querySelector("article.article");\n    if (!body || body.querySelector("[data-mametas-must-see]")) return;'
    repl='    var body = document.querySelector(".article-body") || document.querySelector("article.article");\n    if (document.querySelector(".city-must-list")) return;\n    if (!body || body.querySelector("[data-mametas-must-see]")) return;'
    if "if (document.querySelector(\".city-must-list\")) return;" not in s:
        if anchor not in s: raise RuntimeError("B3 renderMustSee anchor missing")
        s=s.replace(anchor,repl,1)
    write(rel,s,old)

    # B7/C11 precursor: do not inject a second next-decision block if one is already in HTML.
    rel="assets/journey-layer.js"
    p,s=read(rel); old=s
    marker='data-static-next-decision'
    if marker not in s:
        fn=s.find("function renderNextDecision")
        if fn<0: raise RuntimeError("B7 renderNextDecision function missing")
        pos=s.find('var body = article.querySelector(".article-body");',fn)
        if pos<0: raise RuntimeError("B7 body anchor missing")
        end=s.find("\n",pos)
        inject='\n    if (Array.from(body.querySelectorAll(".verdict, .verdict-box")).some(function (node) { return /next decision|prochaine décision/i.test(node.textContent || ""); })) return; // data-static-next-decision'
        # after the following "if (!body) return;" line
        end2=s.find("\n",s.find("if (!body) return;",end))
        s=s[:end2]+inject+s[end2:]
    write(rel,s,old)

def patch_html_blockers():
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        old=s

        # B4: broken regex backreference leaked into Cannes beach headings.
        s=s.replace("<h3\\1>","<h3>").replace("</h3\\1>","</h3>")

        # B10: make expired September information explicitly historical or archived.
        replacements={
          "Until 28 September 2026":"Ended 28 September 2026",
          "until 28 September 2026":"ended 28 September 2026",
          "Until 27 September 2026":"Ended 27 September 2026",
          "until 27 September 2026":"ended 27 September 2026",
          "Until 30 September: 10am-6pm":"Summer hours ended 30 September. Check the official site for current opening hours",
          "Until 30 September: 10 am-6 pm":"Summer hours ended 30 September. Check the official site for current opening hours",
          "Now: Late September":"Archive: September 2026",
          "Updated 24 September 2026. This page changes because September does.":"Archived after September 2026. Keep it for reference; use the Riviera Agenda for current dates.",
          "Carnival, Ironman, an exhibition closing soon.":"Carnival, MIPIM, Ironman. The Riviera has its own calendar.",
          "jusqu’au 28 septembre 2026":"terminée le 28 septembre 2026",
          "jusqu'au 28 septembre 2026":"terminée le 28 septembre 2026",
          "jusqu’au 27 septembre 2026":"terminée le 27 septembre 2026",
          "jusqu'au 27 septembre 2026":"terminée le 27 septembre 2026",
          "Jusqu’au 30 septembre : 10h-18h":"Les horaires d’été se sont terminés le 30 septembre. Vérifiez les horaires actuels sur le site officiel",
          "Jusqu'au 30 septembre : 10h-18h":"Les horaires d’été se sont terminés le 30 septembre. Vérifiez les horaires actuels sur le site officiel",
          "Maintenant : fin septembre":"Archive : septembre 2026",
          "Mis à jour le 24 septembre 2026. Cette page change parce que septembre change.":"Archivée après septembre 2026. Gardez-la comme référence ; utilisez l’Agenda de la Riviera pour les dates actuelles.",
          "Carnaval, Ironman, une expo qui ferme bientôt.":"Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier.",
        }
        for a,b in replacements.items(): s=s.replace(a,b)

        # Seasonal beach wording: do not present 2026 patrol/access dates as current.
        s=s.replace("to 13 September 2026","during the 2026 season, through 13 September")
        s=s.replace("until 30 September 2026","during the 2026 season, through 30 September")
        s=s.replace("from 15 June to 15 September 2026","during the 2026 season, from 15 June to 15 September")
        s=s.replace("jusqu’au 13 septembre 2026","pendant la saison 2026, jusqu’au 13 septembre")
        s=s.replace("jusqu'au 13 septembre 2026","pendant la saison 2026, jusqu’au 13 septembre")
        s=s.replace("jusqu’au 30 septembre 2026","pendant la saison 2026, jusqu’au 30 septembre")
        s=s.replace("jusqu'au 30 septembre 2026","pendant la saison 2026, jusqu’au 30 septembre")
        s=s.replace("du 15 juin au 15 septembre 2026","pendant la saison 2026, du 15 juin au 15 septembre")

        # B11: remove logistics cells whose only value is a placeholder.
        placeholder=r'(?:See official information below\.|Voir les informations officielles ci-dessous\.)'
        patterns=[
          rf'<div[^>]*class=["\'][^"\']*(?:fact|logistics)[^"\']*["\'][^>]*>(?:(?!</div>)[\s\S])*?{placeholder}(?:(?!</div>)[\s\S])*?</div>',
          rf'<li[^>]*>(?:(?!</li>)[\s\S])*?{placeholder}(?:(?!</li>)[\s\S])*?</li>',
          rf'<tr[^>]*>(?:(?!</tr>)[\s\S])*?{placeholder}(?:(?!</tr>)[\s\S])*?</tr>',
        ]
        for pat in patterns:
            s=re.sub(pat,"",s,flags=re.I)

        # If a naked placeholder survived, remove its immediate paragraph/span rather than
        # leaving a false address/access/time statement.
        s=re.sub(rf'<(?:p|span)[^>]*>\s*{placeholder}\s*</(?:p|span)>',"",s,flags=re.I)

        # B14: home agenda headline parity and remove stale exhibition wording wherever it survived.
        s=s.replace("Carnival, IRONMAN, an exhibition closing soon — the Riviera has its own calendar.",
                    "Carnival, MIPIM, Ironman. The Riviera has its own calendar.")
        s=s.replace("Carnaval, IRONMAN, une expo qui ferme bientôt — la Riviera a son propre calendrier.",
                    "Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier.")

        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("lot1 HTML blocker pass changed",changed,"files")

def patch_french_typography():
    """B15/C16 subset: typography on visible French text nodes only."""
    changed=0
    protected_re=re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1>',re.I)
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        if not re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I): continue
        old=s; blocks=[]
        def hold(m):
            key=f"__MAMETAS_LOT1_PROTECTED_{len(blocks)}__"; blocks.append(m.group(0)); return key
        t=protected_re.sub(hold,s)
        parts=re.split(r'(<[^>]+>)',t)
        for i in range(0,len(parts),2):
            x=parts[i]
            # Narrow no-break space before ? ! ; ».
            x=re.sub(r'[ \u00a0\u202f]+([?!;»])', '\u202f\\1', x)
            # Normal no-break space before colon and after «.
            x=re.sub(r'[ \u00a0\u202f]*:', '\u00a0:', x)
            x=re.sub(r'«[ \u00a0\u202f]*', '«\u00a0', x)
            parts[i]=x
        t="".join(parts)
        for i,b in enumerate(blocks): t=t.replace(f"__MAMETAS_LOT1_PROTECTED_{i}__",b)
        if t!=old:
            p.write_text(t,encoding="utf-8"); changed+=1
    print("French typography changed",changed,"files")

def patch_css():
    rel="assets/mametas-shell-v1.css"
    p,s=read(rel); old=s
    token="/* Claude final audit lot 1 — B6 B7 B8 B9 B13 — 2026-10-07 */"
    if token not in s:
        s += r'''

/* Claude final audit lot 1 — B6 B7 B8 B9 B13 — 2026-10-07 */
/* B6: cross-promos on pale cards must never inherit white verdict links. */
body.rg-destination .verdict.ux-cross-promo a{
  color:#14213D!important;
  text-decoration:underline!important;
}

/* B7/B13: global rule/fact primitives outside intent-detail. */
.verdict:not(.ux-cross-promo){
  margin:32px 0!important;
  padding:24px 28px!important;
  background:#14213D!important;
  color:#FFFDF8!important;
}
.verdict:not(.ux-cross-promo) .label{
  display:block!important;
  margin:0 0 10px!important;
  font:700 11px/1.3 Inter,sans-serif!important;
  letter-spacing:.14em!important;
  text-transform:uppercase!important;
  color:#F7C966!important;
}
.verdict:not(.ux-cross-promo) p,
.verdict:not(.ux-cross-promo) p strong,
.verdict:not(.ux-cross-promo) a{
  color:#FFFDF8!important;
}
.verdict:not(.ux-cross-promo) p{
  margin:0 0 10px!important;
  font-family:var(--serif)!important;
  font-size:20px!important;
  line-height:1.45!important;
}
.fact-grid{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:10px!important;
  margin:0 0 36px!important;
}
.fact{
  padding:18px!important;
  border:1px solid rgba(20,33,61,.14)!important;
  background:rgba(255,253,248,.5)!important;
}
.fact b{
  display:block!important;
  margin-bottom:6px!important;
  font:600 11px/1.3 Inter,sans-serif!important;
  letter-spacing:.12em!important;
  text-transform:uppercase!important;
  color:#7A5B1B!important;
}
.fact span{
  display:block!important;
  font-family:var(--serif)!important;
  font-size:20px!important;
  line-height:1.25!important;
  color:#14213D!important;
}

/* Keep the V3 practical catch light: only its label typography is shared. */
body.rg-destination.rg-v3 .practical-decision-layer .label{
  font:700 11px/1.3 Inter,sans-serif!important;
  letter-spacing:.14em!important;
  text-transform:uppercase!important;
  color:#7A5B1B!important;
}

/* B8: legacy verification badge must stay inside the viewport. */
.rg-legacy .mametas-checked{
  max-width:100%!important;
  box-sizing:border-box!important;
}

/* B9: long institutional H1s must wrap at 390px. */
@media (max-width:700px){
  body.about-page h1,
  body[class*="about"] h1,
  .about-hero h1{
    font-size:clamp(34px,9vw,51px)!important;
    overflow-wrap:break-word!important;
    hyphens:auto!important;
  }
  .fact-grid{grid-template-columns:1fr!important}
  .verdict:not(.ux-cross-promo) p{font-size:18px!important}
}
'''
    write(rel,s,old)

def validate():
    # B1
    for rel in ("index.html","fr/index.html"):
        s=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
        if "mametas-home-hero-2026-09-11.PNG" not in s:
            raise RuntimeError(f"B1 hero restore missing in {rel}")

    # B2
    engine=(ROOT/"assets/hotel-engine.js").read_text(encoding="utf-8",errors="ignore")
    if "invalidDetailPaths" not in engine or "hotel-west-end-nice-promenade" not in engine:
        raise RuntimeError("B2/HF1 invalid detail path guard missing")

    # B3
    editorial=(ROOT/"assets/editorial-layer.js").read_text(encoding="utf-8",errors="ignore")
    if 'document.querySelector(".city-must-list")' not in editorial:
        raise RuntimeError("B3 static must-see guard missing")

    # B5 asset exists in build; deployment force-list is checked by workflow separately.
    if not (ROOT/"assets/editorial/iles-de-lerins-bruno-attuyt.webp").exists():
        raise RuntimeError("B5 Lérins asset missing from repo")

    # B6/B8/B9/B13 CSS.
    css=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8",errors="ignore")
    for token in ("verdict.ux-cross-promo a",".rg-legacy .mametas-checked",".fact-grid","Claude final audit lot 1"):
        if token not in css: raise RuntimeError("CSS blocker guard missing: "+token)

    # Rendered HTML blocker sweep.
    bad=[]
    stale=[
      "<h3\\1>","See official information below.","Voir les informations officielles ci-dessous.",
      "an exhibition closing soon","une expo qui ferme bientôt",
      "Now: Late September","Maintenant : fin septembre",
    ]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        for token in stale:
            if token in s: bad.append(f"{rel}: {token}")
    if bad:
        raise RuntimeError("Lot1 blockers survive: "+" | ".join(bad[:20]))

    print("Claude final audit lot 1 validation passed.")

def main():
    patch_runtime_layers()
    patch_html_blockers()
    patch_french_typography()
    patch_css()
    validate()

if __name__=="__main__":
    main()
