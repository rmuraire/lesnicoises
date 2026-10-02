#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize high-value detail-family page tops from the coherence audit."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "en/good-finds/nice-airport-transfer/index.html": ("/en/practical/", "← Back to Practical", "PRACTICAL · ARRIVAL LOGISTICS"),
    "en/good-finds/train-or-bus/index.html": ("/en/practical/", "← Back to Practical", "PRACTICAL · GETTING AROUND"),
    "en/good-finds/what-to-book/index.html": ("/en/practical/", "← Back to Practical", "PRACTICAL · BOOKINGS"),
    "en/good-finds/nice-in-the-rain/index.html": ("/en/practical/", "← Back to Practical", "PRACTICAL · NICE IN THE RAIN"),
    "en/beaches/nice/index.html": ("/en/beaches/", "← Back to beaches", "BEACHES · NICE"),
    "en/beaches/around-nice/index.html": ("/en/beaches/", "← Back to beaches", "BEACHES · AROUND NICE"),
    "en/beaches/antibes/index.html": ("/en/beaches/", "← Back to beaches", "BEACHES · ANTIBES"),
    "en/beaches/cannes/index.html": ("/en/beaches/", "← Back to beaches", "BEACHES · CANNES"),
}

def normalize_old_article_top(text: str, href: str, back: str, eyebrow: str) -> str:
    text = re.sub(
        r'<a class="back"[^>]*>.*?</a>',
        f'<a class="mametas-detail-back" href="{href}">{back}</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<div class="meta">.*?</div>',
        f'<div class="meta mametas-detail-eyebrow">{eyebrow}</div>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    return text

def normalize_comparison() -> bool:
    path = ROOT / "en/riviera-guide/nice-or-cannes/index.html"
    text = path.read_text(encoding="utf-8")
    before = text
    text = re.sub(
        r'<p class="breadcrumbs">.*?</p>',
        '<a class="mametas-detail-back" href="/en/riviera-guide/">← Back to Places</a>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'<p class="eyebrow">.*?</p>',
        '<p class="eyebrow mametas-detail-eyebrow">FRENCH RIVIERA · NICE OR CANNES</p>',
        text,
        count=1,
        flags=re.S | re.I,
    )
    if text != before:
        path.write_text(text, encoding="utf-8")
        return True
    return False

def main() -> None:
    changed = []
    for rel, (href, back, eyebrow) in TARGETS.items():
        path = ROOT / rel
        if not path.exists():
            raise RuntimeError(f"Expected audit page missing: {rel}")
        text = path.read_text(encoding="utf-8")
        before = text
        text = normalize_old_article_top(text, href, back, eyebrow)
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)
        if "mametas-detail-back" not in text or "mametas-detail-eyebrow" not in text:
            raise RuntimeError(f"{rel}: normalized detail top missing")

    if normalize_comparison():
        changed.append("en/riviera-guide/nice-or-cannes/index.html")

    comp = (ROOT / "en/riviera-guide/nice-or-cannes/index.html").read_text(encoding="utf-8")
    if '<p class="breadcrumbs">' in comp:
        raise RuntimeError("Nice-or-Cannes: breadcrumb generation still present")
    if "FRENCH RIVIERA · NICE OR CANNES" not in comp:
        raise RuntimeError("Nice-or-Cannes: canonical eyebrow missing")

    print(f"Detail-family top normalization passed; changed {len(changed)} pages.")


if __name__ == "__main__":
    main()
