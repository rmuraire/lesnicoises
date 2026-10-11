#!/usr/bin/env python3
"""Contrôle de l'affiliation Booking (dossier site/).

Chaque lien commercial vers booking.com doit passer par le lien CJ de Mametas.
Seules exceptions : les citations de source placées dans un bloc
<div class="sources ...">, en nofollow, qui renvoient vers la fiche
Booking d'un hôtel pour justifier une information (ce ne sont pas des
liens de réservation). Bloquant.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2] / "site"
CJ = "www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com"
TEXT_SUFFIXES = {".html", ".json", ".xml", ".js"}
BOOKING = re.compile(r'https?://(?:www\.)?booking\.com/[^"\'<>\s]+', re.I)
DIV_TAG = re.compile(r"<(/?)div\b[^>]*>", re.I)
SOURCES_OPEN = re.compile(r'<div\b[^>]*\bclass=["\'][^"\']*\bsources\b', re.I)


def source_blocks(text: str) -> list[tuple[int, int]]:
    """Return the [start, end) ranges of <div class="sources ..."> blocks."""
    ranges = []
    for start in SOURCES_OPEN.finditer(text):
        depth = 0
        for tag in DIV_TAG.finditer(text, start.start()):
            depth += -1 if tag.group(1) else 1
            if depth == 0:
                ranges.append((start.start(), tag.end()))
                break
    return ranges


raw = []
cited = 0
affiliate_count = 0
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
        continue
    rel = p.relative_to(ROOT).as_posix()
    s = p.read_text(encoding="utf-8", errors="ignore")
    affiliate_count += s.count(CJ)
    blocks = source_blocks(s) if p.suffix.lower() == ".html" else []
    for m in BOOKING.finditer(s):
        url = m.group(0)
        if "news.booking.com" in url:
            continue
        if any(a <= m.start() < b for a, b in blocks):
            cited += 1
            continue
        raw.append((rel, url[:220]))

if raw:
    print("LIENS BOOKING NON AFFILIÉS :")
    for rel, url in raw[:100]:
        print(f"- {rel}: {url}")
    sys.exit(1)
if affiliate_count < 100:
    sys.exit(f"Nombre de liens Booking/CJ anormalement bas : {affiliate_count}")
print(
    f"Affiliation Booking conforme : {affiliate_count} liens via CJ, "
    f"0 lien de réservation direct, {cited} citation(s) de source autorisée(s)."
)
