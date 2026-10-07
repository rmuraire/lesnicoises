#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit, lot 3: language and typography.

This pass removes the machine-like punctuation habits Claude identified while
preserving the Mametas vocabulary. It deliberately prefers deleting repetitive
negative contrast over inventing replacement copy.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

PROTECTED_NAMES={
    "Maison Albar - Le Victoria":"__NAME_0__",
    "Henri Matisse - Yves Saint Laurent":"__NAME_1__",
    "Le Louis XV - Alain Ducasse":"__NAME_2__",
}
UNPROTECTED={v:k for k,v in PROTECTED_NAMES.items()}

def protect(s):
    for k,v in PROTECTED_NAMES.items(): s=s.replace(k,v)
    return s

def unprotect(s):
    for k,v in UNPROTECTED.items(): s=s.replace(k,v)
    return s

def html_lang(s):
    return "fr" if re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I) else "en"

def clean_text_node(x,lang,restaurant=False):
    x=protect(x)

    # Long/en dashes used as punctuation become a colon. This keeps the
    # relationship explicit without introducing another repeated tic.
    x=re.sub(r'\s+[—–]\s+', ': ', x)
    # Also catch dashes attached to words, while preserving numeric ranges such as 9–28.
    x=re.sub(r'(?<=[A-Za-zÀ-ÖØ-öø-ÿ])\s*—\s*(?=[A-Za-zÀ-ÖØ-öø-ÿ])', ': ', x)
    x=re.sub(r'(?<=[,.;!?])\s*—\s*(?=[A-Za-zÀ-ÖØ-öø-ÿ])', ' ', x)

    # Short hyphen as punctuation is concentrated in restaurant decision lines.
    if restaurant:
        x=re.sub(r'\s+-\s+', ': ', x)

    # The dominant "X, not Y" / "X, pas Y" pattern: keep the affirmative claim,
    # drop the repetitive negative tail. This is intentionally conservative.
    if lang=="en":
        x=re.sub(r',\s+(?:not|not merely|not just|not only)\s+[^.!?<>]{1,140}(?=[.!?])', '', x, flags=re.I)
    else:
        x=re.sub(r',\s+(?:pas|et non|pas seulement)\s+[^.!?<>]{1,140}(?=[.!?])', '', x, flags=re.I)

    # Exact repeated editorial fragments identified in C17.
    x=x.replace("Do not choose the room in isolation. Put it back into the trip.","")
    x=x.replace("Ne choisissez pas seulement la chambre. Replacez-la dans le voyage.","")
    x=x.replace("Ne choisissez pas la chambre seule. Replacez-la dans le voyage.","")

    # French typography after punctuation changes.
    if lang=="fr":
        x=re.sub(r'[ \u00a0\u202f]+([?!;»])','\u202f\\1',x)
        x=re.sub(r'[ \u00a0\u202f]*:','\u00a0:',x)
        x=re.sub(r'«[ \u00a0\u202f]*','«\u00a0',x)
    else:
        x=re.sub(r'\s+:',':',x)

    x=re.sub(r'[ \t]{2,}',' ',x)
    return unprotect(x)

def process_html(rel,p):
    s=p.read_text(encoding="utf-8",errors="ignore")
    old=s
    lang=html_lang(s)
    restaurant="/restaurants/" in ("/"+rel.as_posix())

    # Protect script/style blocks; dynamic JS is patched separately.
    blocks=[]
    pat=re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1>',re.I)
    def hold(m):
        key=f"__MAMETAS_LANG_BLOCK_{len(blocks)}__"; blocks.append(m.group(0)); return key
    t=pat.sub(hold,s)
    parts=re.split(r'(<[^>]+>)',t)
    for i in range(0,len(parts),2):
        parts[i]=clean_text_node(parts[i],lang,restaurant)
    t="".join(parts)
    for i,b in enumerate(blocks): t=t.replace(f"__MAMETAS_LANG_BLOCK_{i}__",b)

    # C17: keep only one "start with this logic" paragraph per page.
    en_sentence="Start with this logic, then compare the room and the real rate for your dates. Prices elsewhere have no loyalty to you."
    fr_sentence="Commencez par cette logique, puis comparez la chambre et le vrai tarif pour vos dates. Les prix ailleurs n’ont aucune loyauté envers vous."
    for sentence in (en_sentence,fr_sentence):
        first=t.find(sentence)
        if first>=0:
            head=t[:first+len(sentence)]
            tail=t[first+len(sentence):].replace(sentence,"")
            t=head+tail

    # Remove a repeated generic next-step sentence; the links carry the action.
    t=t.replace("Move the trip forward instead of climbing back to the menu.","")
    t=t.replace("Faites avancer le voyage plutôt que de remonter au menu.","")

    if t!=old:
        p.write_text(t,encoding="utf-8")
        return True
    return False

def patch_dynamic_js():
    for rel in ("assets/editorial-layer.js","assets/journey-layer.js","assets/practical-layer.js",
                "assets/hotel-engine.js","assets/riviera-chooser.js"):
        p=ROOT/rel
        if not p.exists(): continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        s=protect(s)
        # Dynamic user-visible strings: remove long punctuation dashes.
        s=s.replace(" — ",": ").replace(" – ",": ")
        # C17 next-decision repeated sentence can disappear entirely.
        s=s.replace("You understand the place. Now move the trip forward instead of climbing back to the menu.","Choose the next part of the trip.")
        s=s.replace("Vous avez compris le lieu. Maintenant, faites avancer le voyage plutôt que de remonter au menu.","Choisissez maintenant la suite du séjour.")
        s=unprotect(s)
        if s!=old:
            p.write_text(s,encoding="utf-8"); print("patched",rel)

def unify_affiliate_disclosures():
    canonical={
      "en":"Affiliate links: Mametas may earn a commission at no extra cost to you. Selection stays editorial.",
      "fr":"Liens affiliés : Mametas peut percevoir une commission, sans coût pour vous. La sélection reste éditoriale.",
    }
    count=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        lang=html_lang(s)
        # Only disclosure elements/classes, never Method prose.
        pat=re.compile(r'<p([^>]*class=["\'][^"\']*(?:affiliate|disclosure)[^"\']*["\'][^>]*)>[\s\S]*?</p>',re.I)
        s=pat.sub(lambda m:f'<p{m.group(1)}>{canonical[lang]}</p>',s)
        if s!=old:
            p.write_text(s,encoding="utf-8"); count+=1
    print("affiliate disclosure normalization changed",count,"files")

def validate():
    bad_dash=[]
    bad_typo=[]
    opposition_pages=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        # Visible text only.
        visible=re.sub(r'<(script|style)\b[^>]*>[\s\S]*?</\1>','',s,flags=re.I)
        text=re.sub(r'<[^>]+>',' ',visible)
        text=unprotect(text)
        # En-dash without spaces is legitimate in ranges/routes (9–28, Nice–Cannes).
        # Flag all em-dashes and only spaced en-dashes as prose punctuation.
        if "—" in text or re.search(r'\s–\s', text):
            bad_dash.append(rel.as_posix())
        if html_lang(s)=="fr":
            m1=re.search(r' (?=[?!;»:])',text)
            if m1:
                a=max(0,m1.start()-70); b=min(len(text),m1.end()+90)
                bad_typo.append(rel.as_posix()+" :: "+re.sub(r'\\s+',' ',text[a:b]))
        # Report residual opposition density; do not fail on isolated deliberate uses.
        if html_lang(s)=="en":
            n=len(re.findall(r',\s+not\b|\bNot\s+[^.!?]{1,80}[.!?]',text,re.I))
        else:
            n=len(re.findall(r',\s+pas\b|\bPas\s+[^.!?]{1,80}[.!?]',text,re.I))
        if n>1: opposition_pages.append((rel.as_posix(),n))

    for rel in ("assets/editorial-layer.js","assets/journey-layer.js","assets/practical-layer.js","assets/hotel-engine.js","assets/riviera-chooser.js"):
        s=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
        if " — " in s or " – " in s:
            bad_dash.append(rel)

    if bad_dash:
        raise RuntimeError("Long punctuation dash survives: "+", ".join(bad_dash[:20]))
    if bad_typo:
        raise RuntimeError("French breakable punctuation spacing survives: "+", ".join(bad_typo[:20]))

    print("Residual pages with >1 explicit opposition:",len(opposition_pages))
    for rel,n in opposition_pages[:30]: print(" opposition",n,rel)
    print("Claude final audit lot 3 language validation passed.")

def main():
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        if process_html(rel,p): changed+=1
    print("language cleanup changed",changed,"HTML files")
    patch_dynamic_js()
    unify_affiliate_disclosures()
    validate()

if __name__=="__main__":
    main()
