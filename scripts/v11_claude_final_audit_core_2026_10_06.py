#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Core fixes from Claude's 6 Oct 2026 final pre-distribution audit.

Scope deliberately limited to high-confidence, mechanically verifiable defects:
- Riviera Fit RF1-RF3
- Hotel Fit HF1-HF6
- visibly broken punctuation sequences and basic EN/FR punctuation hygiene
- the most repeated Mèfi dash pattern
- shared button primitives for the two decision engines

The broader editorial "opposition tic" rewrite and full-site CTA migration are
kept separate because they require a judgement pass, not a blind regex sweep.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_ROOTS = {
    ".git", ".github", "scripts", "docs", "backup",
    "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2",
}

def write_if(path: Path, new: str, old: str) -> None:
    if new != old:
        path.write_text(new, encoding="utf-8")
        print("patched", path.relative_to(ROOT))
    else:
        print("unchanged", path.relative_to(ROOT))

def patch_riviera_fit() -> None:
    p = ROOT / "assets/riviera-chooser.js"
    s = p.read_text(encoding="utf-8")
    old = s

    # RF1: no-car + ambitious must never claim that "the car or train" does the work.
    s = s.replace(
        "ambitious:'Rythme ambitieux : on élargit la carte sans diluer l’ambiance choisie. Une direction par jour, et la voiture ou le train servent à couvrir davantage de Riviera intelligemment.'",
        "ambitious:'Rythme ambitieux : on élargit la carte sans diluer l’ambiance choisie. Une direction par jour, avec la meilleure liaison disponible, pour couvrir davantage de Riviera intelligemment.'",
    )

    # RF2: French typography.
    s = s.replace("friction:'Moyenne: relief + budget'", "friction:'Moyenne : relief + budget'")

    write_if(p, s, old)

def patch_hotel_fit() -> None:
    p = ROOT / "assets/hotel-engine.js"
    s = p.read_text(encoding="utf-8")
    old = s

    # HF1: these detail routes were 404 in Claude's complete combination test.
    invalid_paths = [
        "/en/hotels/nice/hotel-64-nice/", "/hotels/nice/hotel-64-nice/",
        "/en/hotels/nice/hotel-florence-nice/", "/hotels/nice/hotel-florence-nice/",
        "/en/hotels/nice/hotel-byakko-nice/", "/hotels/nice/hotel-byakko-nice/",
        "/en/hotels/nice/hotel-khla-nice/", "/hotels/nice/hotel-khla-nice/",
        "/en/hotels/nice/hotel-amour-nice/", "/hotels/nice/hotel-amour-nice/",
        "/en/hotels/nice/hotel-aston-la-scala/", "/hotels/nice/hotel-aston-la-scala/",
        "/en/hotels/nice/hotel-west-end-nice-promenade/", "/hotels/nice/hotel-west-end-nice-promenade/",
    ]
    marker = "var invalidDetailPaths = {"
    if marker not in s:
        anchor = "  var unsafeAffiliateIds = { 'apollinaire-nice': true };"
        if anchor not in s:
            raise RuntimeError("Hotel Fit unsafeAffiliateIds anchor missing")
        lines = ",\n".join(f"    {path!r}: true" for path in invalid_paths)
        insertion = anchor + "\n  var invalidDetailPaths = {\n" + lines + "\n  };"
        s = s.replace(anchor, insertion, 1)

    s = s.replace(
        "      if (hotel.detailPath) {\n        actions.push('<a class=\"button hotel-engine-editorial\" href=\"' + esc(hotel.detailPath) + '\">' + labels.details + '</a>');\n      }",
        "      if (hotel.detailPath && !invalidDetailPaths[hotel.detailPath]) {\n        actions.push('<a class=\"btn btn--primary hotel-engine-editorial\" href=\"' + esc(hotel.detailPath) + '\">' + labels.details + '</a>');\n      }",
    )
    s = s.replace(
        "actions.push('<a class=\"button secondary hotel-engine-affiliate\"",
        "actions.push('<a class=\"btn btn--affiliate hotel-engine-affiliate\"",
    )
    s = s.replace(
        "'<button class=\"button secondary hotel-engine-reset\" type=\"button\" data-engine-reset>'",
        "'<button class=\"btn btn--secondary hotel-engine-reset\" type=\"button\" data-engine-reset>'",
    )

    # HF2/HF3/HF4. Some budgetFallback strings are injected earlier in the build.
    s = s.replace(
        "closest:function(n){ return 'Aucun match exact. Voici ' + n + (n > 1 ? ' compromis Mametas les plus proches' : ' compromis Mametas le plus proche') + ' — avec les critères qu’il faut accepter de relâcher.'; }",
        "closest:function(n){ return 'Aucune correspondance exacte. Voici ' + n + (n > 1 ? ' compromis Mametas les plus proches' : ' compromis Mametas le plus proche') + ', avec les critères qu’il faut accepter de relâcher.'; }",
    )
    s = s.replace(
        "closest:function(n){ return 'No exact match. Here ' + (n === 1 ? 'is the closest Mametas compromise' : 'are the ' + n + ' closest Mametas compromises') + ' — with the trade-offs made explicit.'; }",
        "closest:function(n){ return 'No exact match. Here ' + (n === 1 ? 'is the closest Mametas compromise' : 'are the ' + n + ' closest Mametas compromises') + ', with the trade-offs made explicit.'; }",
    )
    s = s.replace(" + symbol + ' — clearly flagged as above budget.'", " + symbol + ', clearly flagged as above budget.'")
    s = s.replace(" + symbol + ' — clairement signalées comme au-dessus du budget.'", " + symbol + ', clairement signalées comme au-dessus du budget.'")
    s = s.replace(" compromises - with the trade-offs made explicit.", " compromises, with the trade-offs made explicit.")
    s = s.replace(" compromis Mametas les plus proches - avec les critères", " compromis Mametas les plus proches, avec les critères")
    s = s.replace(" compromis Mametas le plus proche - avec les critères", " compromis Mametas le plus proche, avec les critères")

    write_if(p, s, old)

def patch_css() -> None:
    p = ROOT / "assets/mametas-shell-v1.css"
    s = p.read_text(encoding="utf-8")
    old = s
    token = "/* Claude final audit core fixes — 2026-10-06 */"
    if token not in s:
        s += r'''

/* Claude final audit core fixes — 2026-10-06 */
.btn{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:8px!important;
  min-height:44px!important;
  padding:0 20px!important;
  box-sizing:border-box!important;
  border:1px solid #14213D!important;
  border-radius:0!important;
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;
  font-size:12px!important;
  font-weight:700!important;
  line-height:1!important;
  letter-spacing:.08em!important;
  text-transform:uppercase!important;
  text-decoration:none!important;
}
.btn--primary{background:#14213D!important;color:#FFFDF8!important}
.btn--secondary,
.btn--affiliate{background:transparent!important;color:#14213D!important}
.btn--affiliate{white-space:normal!important}
.engine-output,
.engine-summary{scroll-margin-top:96px!important}
.engine-base-gate,
.engine-note{font-size:14px!important;line-height:1.5!important}

/* RF3: result copy that carries decisions must stay readable. */
.chooser-result-head>p:not(.eyebrow),
.chooser-alt-grid span,
.chooser-skip p,
.chooser-further-head>p,
.chooser-further-card small,
.chooser-hotels-head>p,
.chooser-hotel-card p{
  font-size:14px!important;
  line-height:1.55!important;
}
'''
    write_if(p, s, old)

def protect_blocks(html: str):
    blocks = []
    pat = re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1>', re.I)
    def repl(m):
        key = f"__MAMETAS_PROTECTED_{len(blocks)}__"
        blocks.append(m.group(0))
        return key
    return pat.sub(repl, html), blocks

def restore_blocks(html: str, blocks):
    for i, block in enumerate(blocks):
        html = html.replace(f"__MAMETAS_PROTECTED_{i}__", block)
    return html

def text_cleanup(text: str, fr: bool) -> str:
    # The 16 broken strings Claude found collapse safely if the missing localism is removed.
    text = text.replace(", ,", ",").replace(", .", ".")
    text = re.sub(r'\s+,', ',', text)

    # Repeated Mèfi construction: preserve voice, remove the machine-like dash.
    text = text.replace("Mèfi — watch out", "Mèfi (watch out)")
    text = text.replace("Mèfi — attention", "Mèfi (attention)")
    text = text.replace("MÈFI — WATCH OUT", "MÈFI · WATCH OUT")
    text = text.replace("MÈFI — ATTENTION", "MÈFI · ATTENTION")
    text = text.replace("Mèfi — the catch", "Mèfi: the catch")
    text = text.replace("Mèfi — le compromis", "Mèfi : le compromis")

    # Apostrophe consistency in rendered copy.
    text = text.replace("'", "’")

    if fr:
        # French colon spacing in visible text only.
        text = re.sub(r'(?<!\s):', '\u00a0:', text)
        text = text.replace("“", "« ").replace("”", " »")
        replacements = {
            "coeur":"cœur", "Coeur":"Cœur", "COEUR":"CŒUR",
            "oeuvre":"œuvre", "Oeuvre":"Œuvre", "OEUVRE":"ŒUVRE",
            "oeuvres":"œuvres", "Oeuvres":"Œuvres", "OEUVRES":"ŒUVRES",
            "oeil":"œil", "Oeil":"Œil", "OEIL":"ŒIL",
        }
        for a,b in replacements.items():
            text = re.sub(rf'\b{a}\b', b, text)
    else:
        text = re.sub(r'\s+:', ':', text)

    return text

def clean_html_visible_text() -> None:
    changed = 0
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_ROOTS:
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        protected, blocks = protect_blocks(s)
        fr = bool(re.search(r'<html\b[^>]*\blang=["\']fr', protected, re.I))

        # Transform only text nodes between tags, never attributes/URLs.
        parts = re.split(r'(<[^>]+>)', protected)
        for i in range(0, len(parts), 2):
            parts[i] = text_cleanup(parts[i], fr)
        n = restore_blocks("".join(parts), blocks)

        if n != s:
            p.write_text(n, encoding="utf-8")
            changed += 1
    print("visible-text cleanup changed", changed, "HTML files")

def validate() -> None:
    chooser = (ROOT/"assets/riviera-chooser.js").read_text(encoding="utf-8")
    engine = (ROOT/"assets/hotel-engine.js").read_text(encoding="utf-8")
    css = (ROOT/"assets/mametas-shell-v1.css").read_text(encoding="utf-8")

    must = [
        ("RF1", "avec la meilleure liaison disponible" in chooser),
        ("RF2", "Moyenne : relief + budget" in chooser),
        ("HF1 denylist", "hotel-west-end-nice-promenade" in engine and "invalidDetailPaths" in engine),
        ("HF4", "Aucune correspondance exacte." in engine),
        ("HF5", "scroll-margin-top:96px" in css),
        ("HF6", ".engine-base-gate" in css and "font-size:14px" in css),
    ]
    failed = [name for name, ok in must if not ok]
    if failed:
        raise RuntimeError("Claude core validation failed: " + ", ".join(failed))

    bad = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_ROOTS:
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        visible, _ = protect_blocks(s)
        if ", ," in visible or ", ." in visible or " ," in visible:
            bad.append(rel.as_posix())
    if bad:
        raise RuntimeError("Broken comma sequences survive: " + ", ".join(bad[:12]))

    print("Claude final audit core validation passed.")

def main() -> None:
    patch_riviera_fit()
    patch_hotel_fit()
    patch_css()
    clean_html_visible_text()
    validate()

if __name__ == "__main__":
    main()
