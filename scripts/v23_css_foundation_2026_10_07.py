#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the Mametas canonical CSS foundation last.

The site has two historical visual stacks: assets/site.css and assets/v3.css.
This script makes assets/mametas-foundation.css the single final visual layer
without rewriting hundreds of HTML files. It is intentionally idempotent.

It also audits public HTML coverage so pages that load neither historical
stylesheet are visible in CI instead of silently escaping the design system.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FOUNDATION = ROOT / "assets" / "mametas-foundation.css"
TARGETS = [ROOT / "assets" / "site.css", ROOT / "assets" / "v3.css"]
START = "/* MAMETAS CANONICAL FOUNDATION:BEGIN */"
END = "/* MAMETAS CANONICAL FOUNDATION:END */"

EXCLUDED_TOP = {
    ".git", ".github", "scripts", "docs", "backup", "node_modules",
    "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2",
}


def strip_previous(text: str) -> str:
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), flags=re.S)
    return pattern.sub("", text).rstrip() + "\n"


def apply() -> None:
    if not FOUNDATION.exists():
        raise RuntimeError("Missing assets/mametas-foundation.css")
    foundation = FOUNDATION.read_text(encoding="utf-8").strip()
    if len(foundation) < 3000:
        raise RuntimeError("Canonical foundation CSS is unexpectedly small")

    payload = f"\n{START}\n{foundation}\n{END}\n"
    for target in TARGETS:
        if not target.exists():
            raise RuntimeError(f"Missing CSS target: {target.relative_to(ROOT)}")
        current = target.read_text(encoding="utf-8", errors="ignore")
        target.write_text(strip_previous(current) + payload, encoding="utf-8")
        print("foundation applied", target.relative_to(ROOT))


def public_html():
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in EXCLUDED_TOP:
            continue
        yield p, rel


def audit_html_coverage() -> None:
    covered = 0
    uncovered = []
    empty_images = []
    hotel_cards_without_media = []

    for p, rel in public_html():
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "/assets/site.css" in s or "/assets/v3.css" in s:
            covered += 1
        elif "<html" in s.lower() and "</head>" in s.lower():
            uncovered.append(rel.as_posix())

        for m in re.finditer(r"<img\b[^>]*>", s, flags=re.I):
            tag = m.group(0)
            src = re.search(r"\bsrc=[\"']([^\"']*)[\"']", tag, flags=re.I)
            if not src or not src.group(1).strip():
                empty_images.append(rel.as_posix())
                break

        for m in re.finditer(
            r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>",
            s,
            flags=re.I | re.S,
        ):
            class_match = re.search(
                r"\bclass=[\"']([^\"']*)[\"']",
                m.group("attrs"),
                flags=re.I,
            )
            if not class_match:
                continue
            classes = set(class_match.group(1).split())
            if "hotel-card" not in classes:
                continue
            block = m.group("body")
            # Some legacy CTA buttons unfortunately reuse the "hotel-card" class.
            # Only structured hotel cards (those with a hotel-card-body wrapper)
            # are subject to the media requirement.
            if "hotel-card-body" not in block:
                continue
            if "hotel-card-media" not in block or "<img" not in block.lower():
                compact = re.sub(r"\\s+", " ", block).strip()[:500]
                print("HOTEL CARD WITHOUT MEDIA", rel.as_posix(), m.group("attrs")[:220], compact)
                hotel_cards_without_media.append(rel.as_posix())
                break

    total = covered + len(uncovered)
    print(f"foundation HTML coverage: {covered}/{total} pages load site.css or v3.css")
    if uncovered:
        print("FOUNDATION COVERAGE WARNING: pages with neither canonical host stylesheet:")
        for rel in uncovered[:60]:
            print(" -", rel)
    if empty_images:
        raise RuntimeError("Empty/missing img src on public pages: " + ", ".join(empty_images[:30]))
    if hotel_cards_without_media:
        raise RuntimeError("Canonical hotel-card without media: " + ", ".join(hotel_cards_without_media[:30]))


def validate_css() -> None:
    foundation = FOUNDATION.read_text(encoding="utf-8").strip()
    for target in TARGETS:
        s = target.read_text(encoding="utf-8", errors="ignore")
        if s.count(START) != 1 or s.count(END) != 1:
            raise RuntimeError(f"Foundation marker duplication in {target.name}")
        between = s.split(START, 1)[1].split(END, 1)[0].strip()
        if between != foundation:
            raise RuntimeError(f"Foundation drift in {target.name}")
    print("canonical CSS foundation validation passed")


def main() -> None:
    apply()
    validate_css()
    audit_html_coverage()


if __name__ == "__main__":
    main()
