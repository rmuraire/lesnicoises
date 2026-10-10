#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install Mametas visual guardrails as the LAST stylesheet on public pages.

The early-October visual baseline already lives in site.css, v3.css and the
global shell. Later component stylesheets may load after those files, so
copying guardrails into site.css/v3.css does not reliably win the cascade.

This pass is intentionally conservative:
- remove any legacy embedded foundation block from site.css/v3.css;
- inject /assets/mametas-foundation.css as the final stylesheet in <head>;
- verify every public HTML page with a head receives it last;
- perform cheap integrity checks before the browser-level smoke test.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FOUNDATION = ROOT / "assets" / "mametas-foundation.css"
FOUNDATION_HREF = "/assets/mametas-foundation.css?v=1.3"
LEGACY_TARGETS = (ROOT / "assets" / "site.css", ROOT / "assets" / "v3.css")
START = "/* MAMETAS CANONICAL FOUNDATION:BEGIN */"
END = "/* MAMETAS CANONICAL FOUNDATION:END */"

EXCLUDED_TOP = {
    ".git", ".github", "scripts", "docs", "backup", "node_modules",
    "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2",
}


def public_html():
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in EXCLUDED_TOP:
            continue
        yield p, rel


def strip_legacy_embedded_foundation() -> None:
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), flags=re.S)
    for target in LEGACY_TARGETS:
        if not target.exists():
            raise RuntimeError(f"Missing CSS target: {target.relative_to(ROOT)}")
        s = target.read_text(encoding="utf-8", errors="ignore")
        cleaned = pattern.sub("", s).rstrip() + "\n"
        if cleaned != s:
            target.write_text(cleaned, encoding="utf-8")
            print("removed legacy embedded foundation", target.relative_to(ROOT))


def inject_last_stylesheet() -> None:
    if not FOUNDATION.exists():
        raise RuntimeError("Missing assets/mametas-foundation.css")
    css = FOUNDATION.read_text(encoding="utf-8", errors="ignore")
    required = (
        ".home-journey-inner",
        ".practical-guide-page .article>.place",
        ".hotel-choice-media",
        ".page-hero h1",
    )
    for token in required:
        if token not in css:
            raise RuntimeError(f"Visual guardrail token missing: {token}")

    link = f'<link rel="stylesheet" href="{FOUNDATION_HREF}">'
    link_pat = re.compile(
        r'<link\b[^>]*href=["\']/assets/mametas-foundation\.css(?:\?v=[^"\']*)?["\'][^>]*>\s*',
        re.I,
    )

    injected = 0
    no_head = []
    for p, rel in public_html():
        s = p.read_text(encoding="utf-8", errors="ignore")
        old = s
        s = link_pat.sub("", s)
        head_idx = s.lower().rfind("</head>")
        if head_idx < 0:
            if "<html" in s.lower():
                no_head.append(rel.as_posix())
            continue
        s = s[:head_idx] + link + "\n" + s[head_idx:]
        if s != old:
            p.write_text(s, encoding="utf-8")
        injected += 1

    print("visual guardrail link installed on", injected, "public HTML pages")
    if no_head:
        raise RuntimeError("Public HTML pages without </head>: " + ", ".join(no_head[:30]))


def audit_html() -> None:
    errors = []
    checked = 0

    for p, rel in public_html():
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "</head>" not in s.lower():
            continue
        checked += 1

        links = re.findall(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\'][^>]*>|'
                           r'<link\b[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']stylesheet["\'][^>]*>',
                           s, flags=re.I)
        hrefs = [a or b for a, b in links]
        if not hrefs or not hrefs[-1].startswith("/assets/mametas-foundation.css"):
            errors.append(rel.as_posix() + " :: visual guardrail is not the final stylesheet")

        for m in re.finditer(r"<img\b[^>]*>", s, flags=re.I):
            tag = m.group(0)
            src = re.search(r"\bsrc=[\"']([^\"']*)[\"']", tag, flags=re.I)
            if not src or not src.group(1).strip():
                errors.append(rel.as_posix() + " :: empty/missing img src")
                break

        # Exact class-token scan avoids confusing hotel-card-body with hotel-card.
        starts = []
        for m in re.finditer(r'<(?:div|article)\b(?P<attrs>[^>]*)>', s, flags=re.I):
            cm = re.search(r'\bclass=["\']([^"\']*)["\']', m.group("attrs"), flags=re.I)
            if cm and ("hotel-card" in cm.group(1).split() or "hotel-choice-card" in cm.group(1).split()):
                starts.append(m.start())
        for i, start in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else min(len(s), start + 5000)
            block = s[start:end]
            if ("hotel-card-body" in block or "hotel-choice-copy" in block):
                has_visual = "<img" in block.lower() or "batch-thumb" in block
                if not has_visual:
                    errors.append(rel.as_posix() + " :: hotel card without visual")
                    break

    print("visual guardrail HTML coverage:", checked, "pages")
    if errors:
        for e in errors[:80]:
            print("FOUNDATION FAIL:", e)
        raise RuntimeError(f"{len(errors)} visual-guardrail integrity failure(s)")


def main() -> None:
    strip_legacy_embedded_foundation()
    inject_last_stylesheet()
    audit_html()
    print("Mametas visual guardrails installed last and validated.")


if __name__ == "__main__":
    main()
