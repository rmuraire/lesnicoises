#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final transparency layer for Mametas traveller personas.

Runs late, after all traveller-voice generators and presentation passes.
It does not invent or rewrite traveller experiences. It only:
- removes the restaurant-denigrating Sam block;
- adds a concise methodology disclosure to every traveller-persona component;
- links the disclosure to the full Method page;
- validates that the final public HTML remains transparent.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EN_METHOD = (
    'Editorial persona: a synthesis of real traveller comments, experience feedback '
    'and field observations. <a href="/en/method/">Our method →</a>'
)
FR_METHOD = (
    'Persona éditorial : synthèse de vrais commentaires, retours d’expérience '
    'et constatations de terrain. <a href="/methode/">Notre méthode →</a>'
)

SOLO_EN = (
    'These profiles are editorial personas. They synthesise real traveller comments, '
    'experience feedback and field observations, and do not necessarily correspond '
    'to identifiable individuals. Practical information is checked independently. '
    '<a href="/en/method/">Our method →</a>'
)
SOLO_FR = (
    'Ces profils sont des personas éditoriaux. Ils synthétisent de véritables '
    'commentaires, retours d’expérience et constatations de terrain, et ne '
    'correspondent pas nécessairement à des personnes identifiables. Les informations '
    'pratiques sont vérifiées indépendamment. <a href="/methode/">Notre méthode →</a>'
)

def lang_of(text: str) -> str:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', text, re.I)
    return "fr" if m and m.group(1).lower().startswith("fr") else "en"

def remove_sam(text: str) -> str:
    return re.sub(
        r'<div class="traveller-voice"[^>]*data-layer="traveller-voice-sam-2026-09-30"[^>]*>[\s\S]*?</div>\s*',
        '',
        text,
        count=1,
        flags=re.I,
    )

def ensure_voice_method(text: str, lang: str) -> str:
    method = FR_METHOD if lang == "fr" else EN_METHOD
    pattern = re.compile(
        r'(<div class="traveller-voice"[^>]*>)([\s\S]*?)(</div>)',
        re.I,
    )
    def repl(m):
        block = m.group(0)
        if 'traveller-voice-method' in block:
            return block
        return m.group(1) + m.group(2) + f'<p class="traveller-voice-method">{method}</p>' + m.group(3)
    return pattern.sub(repl, text)

def ensure_home_method(text: str, lang: str) -> str:
    method = FR_METHOD if lang == "fr" else EN_METHOD
    pattern = re.compile(
        r'(<div class="home-hotel-voice"[^>]*>)([\s\S]*?)(</div>)',
        re.I,
    )
    def repl(m):
        block = m.group(0)
        if 'home-hotel-voice-method' in block:
            return block
        return m.group(1) + m.group(2) + f'<p class="home-hotel-voice-method">{method}</p>' + m.group(3)
    return pattern.sub(repl, text)

def ensure_solo_method(text: str, lang: str) -> str:
    method = SOLO_FR if lang == "fr" else SOLO_EN
    start = text.find('data-layer="solo-verbatims-2026-09-30"')
    if start < 0:
        return text
    section_start = text.rfind("<section", 0, start)
    section_end = text.find("</section>", start)
    if section_start < 0 or section_end < 0:
        raise RuntimeError("Solo traveller section bounds not found")
    section = text[section_start:section_end]
    if 'solo-voices-method' in section:
        return text
    note = f'<p class="solo-voices-method">{method}</p>'
    return text[:section_end] + note + text[section_end:]

def patch_pages() -> tuple[int,int,int]:
    voice_count = 0
    solo_count = 0
    home_count = 0

    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {".git",".github","docs","scripts","data","backup"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        before = text
        lang = lang_of(text)

        text = remove_sam(text)
        text = ensure_voice_method(text, lang)
        text = ensure_home_method(text, lang)
        text = ensure_solo_method(text, lang)

        voice_count += text.count('class="traveller-voice"')
        solo_count += text.count('data-layer="solo-verbatims-2026-09-30"')
        home_count += text.count('class="home-hotel-voice"')

        if text != before:
            path.write_text(text, encoding="utf-8")

    return voice_count, solo_count, home_count

def patch_css() -> None:
    path = ROOT / "assets/mametas-shell-v1.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* Traveller persona transparency — 2026-10-02 */"
    if marker in text:
        return
    text += """
%s
.traveller-voice-method,
.home-hotel-voice-method,
.solo-voices-method{
  margin-top:9px!important;
  padding-top:9px;
  border-top:1px solid rgba(20,33,61,.12);
  color:#5f6570!important;
  font-family:var(--mg-sans,Inter,Arial,sans-serif)!important;
  font-size:9.5px!important;
  line-height:1.48!important;
  opacity:.8;
}
.solo-voices-method{
  max-width:820px;
  margin-top:14px!important;
}
.traveller-voice-method a,
.home-hotel-voice-method a,
.solo-voices-method a{
  color:var(--mg-blue,#176f83)!important;
  font-weight:700;
  text-decoration:none;
  border-bottom:1px solid currentColor;
}
""" % marker
    path.write_text(text, encoding="utf-8")

def validate(voice_count: int, solo_count: int, home_count: int) -> None:
    if solo_count < 2:
        raise RuntimeError(f"Expected EN+FR solo persona sections, found {solo_count}")
    if voice_count < 8:
        raise RuntimeError(f"Expected contextual traveller voices, found {voice_count}")
    if home_count < 2:
        raise RuntimeError(f"Expected EN+FR homepage hotel voices, found {home_count}")

    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {".git",".github","docs","scripts","data","backup"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "traveller-voice-sam-2026-09-30" in text or "giant picture menus on Cours Saleya" in text:
            raise RuntimeError(f"{rel}: restaurant-denigrating traveller voice remains")
        if 'class="traveller-voice"' in text and 'traveller-voice-method' not in text:
            raise RuntimeError(f"{rel}: traveller voice missing persona disclosure")
        if 'class="home-hotel-voice"' in text and 'home-hotel-voice-method' not in text:
            raise RuntimeError(f"{rel}: homepage voice missing persona disclosure")
        if 'data-layer="solo-verbatims-2026-09-30"' in text and 'solo-voices-method' not in text:
            raise RuntimeError(f"{rel}: solo voices missing persona disclosure")

    for rel, phrase in (
        ("en/method/index.html", "editorial personas"),
        ("methode/index.html", "personas éditoriaux"),
    ):
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if phrase not in text:
            raise RuntimeError(f"{rel}: traveller-persona methodology missing")

def main() -> None:
    counts = patch_pages()
    patch_css()
    validate(*counts)
    print(
        "Traveller persona transparency passed: "
        f"{counts[0]} contextual voices, {counts[1]} solo sections, {counts[2]} homepage voices."
    )

if __name__ == "__main__":
    main()
