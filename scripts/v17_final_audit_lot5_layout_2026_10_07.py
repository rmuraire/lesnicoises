#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit, lot 5: layout/detail finishing.

Conservative implementation of Claude C9-C11, C13, C19 and C20. C12
(remote images) is handled earlier by v15.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

LEGACY=(
 "en/riviera-guide/nice/index.html","riviera-guide/nice/index.html",
 "en/riviera-guide/cannes/index.html","riviera-guide/cannes/index.html",
 "en/riviera-guide/eze/index.html","riviera-guide/eze/index.html",
 "en/riviera-guide/saint-tropez/index.html","riviera-guide/saint-tropez/index.html",
 "en/riviera-guide/saint-paul-de-vence/index.html","riviera-guide/saint-paul-de-vence/index.html",
)
V3=(
 "en/riviera-guide/antibes/index.html","riviera-guide/antibes/index.html",
 "en/riviera-guide/monaco/index.html","riviera-guide/monaco/index.html",
 "en/riviera-guide/menton/index.html","riviera-guide/menton/index.html",
 "en/riviera-guide/villefranche-cap-ferrat/index.html","riviera-guide/villefranche-cap-ferrat/index.html",
)
NEXT_DECISION=(
 "en/riviera-guide/eze/index.html","riviera-guide/eze/index.html",
 "en/riviera-guide/saint-tropez/index.html","riviera-guide/saint-tropez/index.html",
 "en/riviera-guide/saint-paul-de-vence/index.html","riviera-guide/saint-paul-de-vence/index.html",
)

def ensure_body_class(s,cls):
    m=re.search(r'<body([^>]*)>',s,re.I)
    if not m:return s
    attrs=m.group(1)
    cm=re.search(r'class=["\']([^"\']*)["\']',attrs,re.I)
    if cm:
        vals=cm.group(1).split()
        if cls in vals:return s
        attrs=attrs[:cm.start()]+f'class="{" ".join(vals+[cls])}"'+attrs[cm.end():]
    else:
        attrs+=f' class="{cls}"'
    return s[:m.start()]+'<body'+attrs+'>'+s[m.end():]

def add_classes():
    for rels,cls in ((LEGACY,"rg-legacy-final"),(V3,"rg-v3-final")):
        for rel in rels:
            p=ROOT/rel
            if not p.exists():continue
            s=p.read_text(encoding="utf-8",errors="ignore")
            n=ensure_body_class(s,cls)
            if n!=s:
                p.write_text(n,encoding="utf-8"); print("class",cls,rel)

def normalize_next_decision():
    pat=re.compile(
      r'(<h2[^>]*>\s*(?:The next decision|La prochaine décision)\s*</h2>)\s*<p>([\s\S]*?)</p>',
      re.I
    )
    anchor=re.compile(r'<a\b([^>]*)>([\s\S]*?)</a>',re.I)
    for rel in NEXT_DECISION:
        p=ROOT/rel
        if not p.exists():continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        def repl(m):
            links=[]
            for am in anchor.finditer(m.group(2)):
                attrs=am.group(1)
                if 'class=' in attrs:
                    attrs=re.sub(r'class=["\']([^"\']*)["\']',lambda x:f'class="{x.group(1)} link-cta"',attrs,count=1)
                else:
                    attrs+=' class="link-cta"'
                links.append('<a'+attrs+'>'+am.group(2)+'</a>')
            if len(links)<2:return m.group(0)
            return m.group(1)+'<div class="next-decision-list">'+"".join(links)+'</div>'
        s=pat.sub(repl,s,count=1)
        if s!=old:
            p.write_text(s,encoding="utf-8"); print("next decision",rel)

def patch_css():
    p=ROOT/"assets/mametas-shell-v1.css"
    s=p.read_text(encoding="utf-8",errors="ignore")
    token="/* Claude final audit lot 5 — 2026-10-07 */"
    if token in s:return
    s+=r'''

/* Claude final audit lot 5 — 2026-10-07 */

/* C9: editorial heading hierarchy should look like one family. */
.article h2,
.article-body h2,
.intent-detail h2,
.rg-v3-final .article-body h2{
  font-family:var(--mg-serif,var(--serif,Georgia,serif))!important;
}

/* C10: legacy destination pages should not feel typographically older. */
.rg-legacy-final article.article>p,
.rg-legacy-final .route-step p,
.rg-legacy-final p.mini-rule{
  font-size:17px!important;
  line-height:1.65!important;
}
@media(min-width:900px){
  .rg-legacy-final article.article>h1{font-size:58px!important;line-height:1.02!important}
}
@media(max-width:700px){
  .rg-legacy-final article.article>h1{font-size:clamp(40px,11vw,52px)!important}
}

/* C11: keep V3 cover/reality-check spacing compact and aligned. */
.rg-v3-final .article-cover{margin-top:24px!important;margin-bottom:24px!important}
.rg-v3-final .article-aside h2{text-align:left!important}
.rg-v3-final .article-layout{align-items:start!important}

/* C13: next-decision links are actions, not inline prose. */
.next-decision-list{
  display:grid!important;
  grid-template-columns:1fr!important;
  gap:0!important;
  margin:4px 0 28px!important;
}
.next-decision-list .link-cta{
  width:max-content;
  max-width:100%;
  min-height:44px;
  padding:12px 0!important;
  display:inline-flex!important;
  align-items:center!important;
  color:#14213D!important;
  font-size:14px!important;
  font-weight:600!important;
  line-height:1.35!important;
  text-decoration:underline!important;
}

/* C19: comfortable reading measure on wide screens. */
article.article>p,
.article-body>p,
.intent-detail .article-body>p,
.page-hero .lead,
.article-hero .article-deck,
.article .standfirst,
.intent-detail .standfirst{
  max-width:68ch!important;
}

/* C20: small global finishing. */
.consent-settings{
  font-size:12px!important;
  line-height:1.4!important;
  vertical-align:baseline!important;
}
[data-chooser-submit]:disabled,
.chooser-submit:disabled{
  background:#E4E1DA!important;
  border-color:#C8C4BB!important;
  color:#14213D!important;
  opacity:1!important;
}
@media(max-width:600px){
  [data-chooser-submit],
  .chooser-submit{
    white-space:nowrap!important;
    font-size:12px!important;
    letter-spacing:.04em!important;
    padding-left:12px!important;
    padding-right:12px!important;
  }
  .base-grid .base-card-content p,
  .mood-card p,
  .by-mood-card p,
  .explore-mood-card p{
    font-size:14px!important;
    line-height:1.5!important;
  }
  .mood-grid,.by-mood-grid,.explore-mood-grid{grid-template-columns:1fr!important}
  .public-log,.contact-box,.corrections-list,.press-list{
    margin-left:0!important;margin-right:0!important;
    max-width:100%!important;box-sizing:border-box!important;
  }
}

/* Restaurant price strings must not split (€ / €€€). */
.price,.price-level,.restaurant-price{white-space:nowrap!important}
'''
    p.write_text(s,encoding="utf-8"); print("patched CSS lot5")

def validate():
    css=(ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8",errors="ignore")
    for tok in ("Claude final audit lot 5","max-width:68ch",".consent-settings",".next-decision-list"):
        if tok not in css:raise RuntimeError("lot5 CSS missing "+tok)
    for rel in LEGACY:
        p=ROOT/rel
        if p.exists() and "rg-legacy-final" not in p.read_text(encoding="utf-8",errors="ignore"):
            raise RuntimeError("legacy scope missing "+rel)
    for rel in V3:
        p=ROOT/rel
        if p.exists() and "rg-v3-final" not in p.read_text(encoding="utf-8",errors="ignore"):
            raise RuntimeError("V3 scope missing "+rel)
    print("Claude final audit lot 5 validation passed.")

def main():
    add_classes()
    normalize_next_decision()
    patch_css()
    validate()

if __name__=="__main__":
    main()
