#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final cleanup after parity additions.

Runs after v17 so late-added FR copy receives the same typography rules as the
rest of the site. Also removes expired September exhibition copy, prevents
hotel title/photo affiliate traps, and removes repeated hotel-selection boilerplate.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKIP={".git",".github","scripts","docs","backup",
      "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

AFFILIATE_HOST_TOKENS=("booking.com","kqzyfj.com","expedia.com","getyourguide")

def protect_blocks(s):
    blocks=[]
    pat=re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1>',re.I)
    def repl(m):
        key=f"__MAMETAS_PROTECTED_{len(blocks)}__"
        blocks.append(m.group(0)); return key
    return pat.sub(repl,s),blocks

def restore_blocks(s,blocks):
    for i,b in enumerate(blocks):
        s=s.replace(f"__MAMETAS_PROTECTED_{i}__",b)
    return s

def typography():
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        protected,blocks=protect_blocks(s)
        fr=bool(re.search(r'<html\b[^>]*\blang=["\']fr',protected,re.I))
        parts=re.split(r'(<[^>]+>)',protected)
        for i in range(0,len(parts),2):
            t=parts[i]
            # Protect HTML entities: French punctuation spacing must not turn
            # "&amp;" into "&amp ;" or otherwise corrupt entity syntax.
            entities=[]
            def hold_entity(m):
                key=f"__MAMETAS_ENTITY_{len(entities)}__"
                entities.append(m.group(0)); return key
            t=re.sub(r'&(?:#[0-9]+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);',hold_entity,t)
            t=re.sub(r'[ \t\u00a0\u202f]+(?=[,.])','',t)
            if fr:
                t=t.replace("'","’")
                t=re.sub(r'[ \t\u00a0\u202f]*(?=[?!;»])','\u202f',t)
                t=re.sub(r'[ \t\u00a0\u202f]*(?=:)', '\u00a0',t)
                t=re.sub(r'«[ \t\u00a0\u202f]*','«\u00a0',t)
                t=t.replace("“","«\u00a0").replace("”","\u202f»")
                for a,b in (("coeur","cœur"),("Coeur","Cœur"),("oeuvre","œuvre"),("Oeuvre","Œuvre"),("oeuvres","œuvres"),("Oeuvres","Œuvres"),("oeil","œil"),("Oeil","Œil")):
                    t=re.sub(rf'\b{a}\b',b,t)
            else:
                t=re.sub(r'[ \t\u00a0\u202f]+(?=:)','',t)
            for ei,entity in enumerate(entities):
                t=t.replace(f"__MAMETAS_ENTITY_{ei}__",entity)
            parts[i]=t
        s=restore_blocks("".join(parts),blocks)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("final typography changed",changed,"HTML files")

def remove_expired_exhibition_copy():
    replacements={
      "bons-plans/nice-quand-il-pleut/index.html":[
        (" En ce moment, l’exposition <em>Henri Matisse - Yves Saint Laurent. Le beau, la mode et le bonheur</em> est annoncée jusqu’au 28 septembre 2026.",""),
        (" Jusqu’au 27 septembre 2026, le musée présente Mathieu Forget.",""),
      ],
      "culture/musee-matisse/index.html":[
        (" Jusqu’au 28 septembre 2026, l’exposition Henri Matisse - Yves Saint Laurent ajoute un dialogue très cohérent avec la mode.",""),
      ],
      "culture/nice/index.html":[
        (" Jusqu’au 28 septembre 2026, exposition Matisse / Yves Saint Laurent.",""),
        (" Jusqu’au 27 septembre 2026, exposition Mathieu Forget.",""),
      ],
    }
    for rel,reps in replacements.items():
        p=ROOT/rel
        if not p.exists(): continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        for a,b in reps: s=s.replace(a,b)
        if s!=old:
            p.write_text(s,encoding="utf-8"); print("expired copy",rel)

def unwrap_affiliate_titles_and_media():
    changed=0
    # Remove affiliate wrappers around media, keeping the image/span itself.
    media_pat=re.compile(
      r'<a\b([^>]*href=["\']([^"\']+)["\'][^>]*)>(\s*(?:<img\b[\s\S]*?>|<span\b[^>]*class=["\'][^"\']*(?:batch-thumb|hotel-choice-media)[^"\']*["\'][\s\S]*?</span>)\s*)</a>',
      re.I
    )
    # Remove affiliate links inside hotel headings.
    title_pat=re.compile(
      r'(<h3\b[^>]*>)\s*<a\b([^>]*href=["\']([^"\']+)["\'][^>]*)>([\s\S]*?)</a>\s*(</h3>)',
      re.I
    )
    # Some showcase cards wrap the entire image/title card in an affiliate
    # anchor. Unwrap those too; the explicit rate button remains the only
    # reservation action.
    card_pat=re.compile(
      r'<a\b([^>]*href=["\']([^"\']+)["\'][^>]*)>([\s\S]*?)</a>',
      re.I
    )
    def affiliate(url): return any(x in url.lower() for x in AFFILIATE_HOST_TOKENS)

    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        def unwrap_media(m):
            if not affiliate(m.group(2)):
                return m.group(0)
            attrs=m.group(1)
            body=m.group(3)
            cm=re.search(r'class=["\']([^"\']*)["\']',attrs,re.I)
            classes=cm.group(1).split() if cm else []
            # Preserve the structural media box even when the reservation link
            # is removed. This keeps every hotel card on the canonical 3:2
            # geometry instead of leaving a sprite/image orphaned in the card.
            if "hotel-choice-media" in classes:
                return '<div class="hotel-choice-media">'+body+'</div>'
            if "hotel-card-media" in classes:
                return '<div class="hotel-card-media">'+body+'</div>'
            return body
        s=media_pat.sub(unwrap_media,s)
        s=title_pat.sub(lambda m:m.group(1)+m.group(4)+m.group(5) if affiliate(m.group(3)) else m.group(0),s)
        def unwrap_card(m):
            body=m.group(3)
            if not affiliate(m.group(2)): return m.group(0)
            if re.search(r'<img\b|<h[1-4]\b|class=["\'][^"\']*(?:hotel-card|hotel-choice|stay-card)',body,re.I):
                return body
            return m.group(0)
        s=card_pat.sub(unwrap_card,s)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("affiliate title/media wrappers removed on",changed,"pages")

def dedupe_boilerplate():
    needles=[
      "Start with this logic, then compare the room and the real rate for your dates. Prices elsewhere have no loyalty to you.",
      "Commencez par cette logique, puis comparez les chambres et le tarif réel à vos dates. Le prix affiché ailleurs n’a aucune loyauté envers vous.",
      "The shortlist is deliberately short. The point is not to recreate Booking with fewer filters",
      "La sélection est volontairement courte. Le but n’est pas de reproduire Booking avec moins de filtres",
      "Do not choose the room in isolation. Put it back into the trip.",
      "Ne choisissez pas seulement la chambre",
      "Move the trip forward instead of climbing back to the menu.",
      "Faites avancer le voyage",
    ]
    changed=0
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore"); old=s
        for needle in needles:
            occurrences=[m for m in re.finditer(re.escape(needle),s)]
            if len(occurrences)<=1: continue
            # Remove whole repeated paragraph after the first when it contains the boilerplate.
            seen=0
            pat=re.compile(r'<p\b[^>]*>[\s\S]*?'+re.escape(needle[:min(48,len(needle))])+r'[\s\S]*?</p>',re.I)
            def repl(m):
                nonlocal seen
                seen+=1
                return m.group(0) if seen==1 else ''
            s=pat.sub(repl,s)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("boilerplate dedupe changed",changed,"pages")

def validate():
    # No late-added French ordinary spacing before high punctuation.
    bad=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP: continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        if not re.search(r'<html\b[^>]*\blang=["\']fr',s,re.I): continue
        s,_=protect_blocks(s)
        parts=re.split(r'(<[^>]+>)',s)
        for i in range(0,len(parts),2):
            if re.search(r' (?=[?!;»:])|[\u00a0\u202f]?(?=,)',parts[i]):
                # commas with no prefix are fine; only literal whitespace is checked below
                if re.search(r'[ \t\u00a0\u202f]+(?=,)',parts[i]) or re.search(r' (?=[?!;»:])',parts[i]):
                    bad.append(rel.as_posix()); break
    if bad: raise RuntimeError("final typography spacing survived: "+", ".join(bad[:20]))

    for rel in ("bons-plans/nice-quand-il-pleut/index.html","culture/musee-matisse/index.html","culture/nice/index.html"):
        p=ROOT/rel
        if p.exists():
            txt=p.read_text(encoding="utf-8",errors="ignore")
            if re.search(r'Jusqu[’\']au (?:27|28) septembre 2026',txt,re.I):
                raise RuntimeError("expired September exhibition survives: "+rel)
    print("Final post-parity cleanup validation passed.")

def main():
    remove_expired_exhibition_copy()
    unwrap_affiliate_titles_and_media()
    dedupe_boilerplate()
    typography()
    validate()

if __name__=="__main__":
    main()
