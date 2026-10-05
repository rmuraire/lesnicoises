#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guard the high-intent Nice Carnival 2027 pages against stale ticketing copy."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS={
    "en/good-finds/nice-carnival/index.html":{
        "required":[
            "9–28 February 2027",
            "Vive l’Amour",
            "carnival-ticketing-status-2026-10-05",
            "5 October 2026",
            "explorenicecotedazur.com/en/nice-carnival-2027-vive-lamour/",
            '"dateModified":"2026-10-05"',
        ],
        "forbidden":[
            "Timings, theme, ticketing and detailed route map are not yet published",
            "2027 programme pending",
            "As of 28 September 2026, the City has published the 2027 dates",
        ],
    },
    "bons-plans/carnaval-nice/index.html":{
        "required":[
            "9–28 février 2027",
            "Vive l’Amour",
            "carnival-ticketing-status-2026-10-05",
            "5 octobre 2026",
            "explorenicecotedazur.com/evenement/carnaval-de-nice-2027-vive-lamour/",
            '"dateModified":"2026-10-05"',
        ],
        "forbidden":[
            "Les horaires, le thème, la billetterie et le plan détaillé ne sont pas encore publiés",
            "Programme 2027 à venir",
            "Au 28 septembre 2026, la Ville a publié les dates 2027",
        ],
    },
}
for rel,rules in TARGETS.items():
    p=ROOT/rel
    if not p.exists():
        raise SystemExit(f"Missing Carnival page: {rel}")
    s=p.read_text(encoding="utf-8",errors="ignore")
    for token in rules["required"]:
        if token not in s:
            raise SystemExit(f"{rel}: missing Carnival freshness token: {token}")
    for token in rules["forbidden"]:
        if token in s:
            raise SystemExit(f"{rel}: stale Carnival copy survived: {token}")
print("Carnival 2027 freshness validation passed.")
