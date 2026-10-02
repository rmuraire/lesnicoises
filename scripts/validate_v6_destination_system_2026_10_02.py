#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate Mametas destination-page coherence after phase 2."""
from pathlib import Path
import re

from mametas_coherence_config import (
    DESTINATIONS,
    DESTINATION_BACK,
    REALITY_LABELS,
    RIVIERA_FIT,
)

ROOT = Path(__file__).resolve().parents[1]
errors = []

bases = [slug for slug, cfg in DESTINATIONS.items() if cfg["group"] == "base"]
detours = [slug for slug, cfg in DESTINATIONS.items() if cfg["group"] == "detour"]
if len(bases) != 6 or len(detours) != 3:
    errors.append(f"canonical destination grouping is {len(bases)} bases / {len(detours)} detours, expected 6/3")

for slug, cfg in DESTINATIONS.items():
    for lang in ("en", "fr"):
        rel = cfg["paths"][lang]
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: missing")
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        name = cfg["name"][lang]
        back_href, back_label = DESTINATION_BACK[lang]
        fit_href, fit_label = RIVIERA_FIT[lang]
        eyebrow = ("PLACES" if lang == "en" else "DESTINATIONS") + " · " + name

        checks = [
            (s.count('data-destination-reality="canonical"') == 1, "canonical Reality Check count"),
            ('class="article-meta"' not in s, "legacy article-meta removed"),
            ('class="breadcrumbs"' not in s, "legacy breadcrumbs removed"),
            (back_href in s and back_label in s, "named parent link"),
            (eyebrow in s, "canonical eyebrow"),
            (fit_href in s and fit_label in s, "canonical Riviera Fit CTA"),
            ('class="mametas-checked"' in s, "Mametas Checked badge preserved"),
        ]
        for label in REALITY_LABELS[lang]:
            checks.append((f"<b>{label}</b>" in s, f"Reality label {label}"))
        if lang == "en":
            for old in ("<b>Mobility</b>", "<b>Budget pressure</b>", "<b>Friction</b>"):
                checks.append((old not in s, f"legacy EN label absent: {old}"))
        else:
            for old in ("<b>Mobilité</b>", "<b>Pression budget</b>", "<b>Friction</b>"):
                checks.append((old not in s, f"legacy FR label absent: {old}"))

        for ok, label in checks:
            if not ok:
                errors.append(f"{rel}: {label}")

# Èze keeps its essential village/station warning; phase 2 must not erase it.
for rel in ("en/riviera-guide/eze/index.html", "riviera-guide/eze/index.html"):
    p = ROOT / rel
    if p.exists():
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "Èze-sur-Mer" not in s or ("village" not in s.lower()):
            errors.append(f"{rel}: Èze village/station warning lost")

# Antibes EN/FR must use the same canonical hero asset.
for rel in ("en/riviera-guide/antibes/index.html", "riviera-guide/antibes/index.html"):
    p = ROOT / rel
    if p.exists() and "/assets/editorial/antibes-gravette.jpg" not in p.read_text(encoding="utf-8", errors="ignore"):
        errors.append(f"{rel}: canonical Antibes hero missing")

if errors:
    print("Destination-system validation failed:")
    for err in errors:
        print(" -", err)
    raise SystemExit(1)

print("Destination-system validation passed on 18 destination pages")
