#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASES = {
    "nice": {"path": ROOT / "assets/hotel-finder-nice.json", "structured": True, "station": True, "nocar": True},
    "antibes": {"path": ROOT / "en/hotels/antibes/index.html", "station": True, "nocar": True},
    "cannes": {"path": ROOT / "en/hotels/cannes/index.html", "station": True, "nocar": True},
    "villefranche": {"path": ROOT / "en/hotels/villefranche-sur-mer/index.html", "station": True, "nocar": True},
    "monaco": {"path": ROOT / "en/hotels/monaco/index.html", "station": True, "nocar": True},
    "menton": {"path": ROOT / "en/hotels/menton/index.html", "station": True, "nocar": True},
    "saint-paul": {"path": ROOT / "en/hotels/saint-paul-de-vence/index.html", "station": False, "nocar": False},
    "beaulieu": {"path": ROOT / "en/hotels/beaulieu-sur-mer/index.html", "station": True, "nocar": True},
    "mougins": {"path": ROOT / "en/hotels/mougins/index.html", "station": False, "nocar": False},
    "saint-tropez": {"path": ROOT / "en/hotels/saint-tropez/index.html", "station": False, "nocar": False},
}

PRICE = {"low": 1, "mid": 2, "upper-mid": 3, "high": 4, "very-high": 4}
STYLES = ("practical", "active", "quiet", "chic")
GEOS = ("station", "sea", "oldtown", "quiet")
BUDGETS = ("low", "mid", "upper-mid", "high")


def attrs(raw: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in re.finditer(r'([a-zA-Z0-9_-]+)="([^"]*)"', raw)}


def signals(best: set[str], styles: set[str], base: dict, item: dict | None = None) -> dict[str, bool]:
    item = item or {}
    return {
        "station": bool(item.get("stationFriendly")) or base["station"] or "excursions" in best,
        "nocar": item.get("carFree") is True or item.get("noCarFriendly") is True or base["nocar"] or "car-free" in best,
        "sea": bool(item.get("seaAccess")) or "beach-first" in best,
        "oldtown": bool(item.get("oldTownAccess")) or "old-town" in best,
        "quiet": bool(item.get("quiet")) or "quiet" in best,
        "practical": "practical" in styles or bool(best & {"excursions", "car-free", "value"}),
        "active": "active" in styles or "city-life" in best,
        "chic": "chic" in styles or "hotel-as-trip" in best,
    }


def structured(base: dict) -> list[dict]:
    payload = json.loads(base["path"].read_text(encoding="utf-8"))
    hotels = []
    for item in payload.get("hotels", []):
        fit = item.get("fit") or {}
        best = set(fit.get("bestFor") or [])
        styles = set(item.get("styles") or [])
        hotels.append({
            "name": item.get("name") or item.get("id") or "hotel",
            "price": item.get("priceBand") or "",
            "sig": signals(best, styles, base, item),
        })
    return hotels


def html_inventory(base: dict) -> list[dict]:
    text = base["path"].read_text(encoding="utf-8")
    hotels = []
    card_re = re.compile(r'<article class="hotel-choice-card"([^>]*)>(.*?)</article>', re.S)
    for m in card_re.finditer(text):
        a = attrs(m.group(1))
        body = m.group(2)
        h = re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S)
        name = re.sub(r"<[^>]+>", "", h.group(1)).strip() if h else a.get("data-hotel", "hotel")
        best = set((a.get("data-fit-best") or "").split())
        hotels.append({
            "name": name,
            "price": a.get("data-price-band", ""),
            "sig": signals(best, set(), base),
        })
    return hotels


def qualifies(hotel: dict, style: str | None = None, geo: str | None = None, nocar: bool = False, budget: str | None = None) -> bool:
    sig = hotel["sig"]
    if style and not sig.get(style, False):
        return False
    if geo and not sig.get(geo, False):
        return False
    if nocar and not sig["nocar"]:
        return False
    if budget:
        p = PRICE.get(hotel["price"], 0)
        if not p or p > PRICE[budget]:
            return False
    return True


def report(base_id: str, hotels: list[dict]) -> list[str]:
    n = len(hotels)
    bands = sorted({h["price"] for h in hotels if h["price"]}, key=lambda x: PRICE.get(x, 99))
    lines = [f"{base_id}: {n} hotels | price bands: {', '.join(bands) or 'NONE'}"]
    style_counts = {s: sum(qualifies(h, style=s) for h in hotels) for s in STYLES}
    geo_counts = {g: sum(qualifies(h, geo=g) for h in hotels) for g in GEOS}
    lines.append("  styles: " + ", ".join(f"{k}={v}" for k, v in style_counts.items()))
    lines.append("  geography: " + ", ".join(f"{k}={v}" for k, v in geo_counts.items()))

    # Pair coverage is the useful editorial signal: style x geography,
    # with and without the no-car constraint. Full 4-filter combinations
    # are intentionally allowed to fall back to closest fit.
    missing_pairs = []
    for style, geo in product(STYLES, GEOS):
        exact = sum(qualifies(h, style=style, geo=geo) for h in hotels)
        exact_nocar = sum(qualifies(h, style=style, geo=geo, nocar=True) for h in hotels)
        if exact == 0:
            missing_pairs.append(f"{style}+{geo}")
        elif exact_nocar == 0:
            missing_pairs.append(f"{style}+{geo}+no-car")
    if missing_pairs:
        lines.append("  pair gaps: " + ", ".join(missing_pairs[:12]) + (" …" if len(missing_pairs) > 12 else ""))
    else:
        lines.append("  pair gaps: none")

    low_mid = sum(qualifies(h, budget="mid") for h in hotels)
    if n < 4:
        lines.append("  EDITORIAL PRIORITY: inventory under 4 hotels")
    elif low_mid == 0:
        lines.append("  EDITORIAL PRIORITY: no low/mid-range option")
    elif len([v for v in style_counts.values() if v > 0]) < 3:
        lines.append("  EDITORIAL PRIORITY: narrow style coverage")
    else:
        lines.append("  coverage: acceptable; closest-fit handles over-specific combinations")
    return lines


def main() -> int:
    print("HOTEL FIT COVERAGE AUDIT")
    print("========================")
    zero = []
    for base_id, base in BASES.items():
        if not base["path"].exists():
            print(f"{base_id}: MISSING SOURCE {base['path'].relative_to(ROOT)}")
            zero.append(base_id)
            continue
        hotels = structured(base) if base.get("structured") else html_inventory(base)
        if not hotels:
            zero.append(base_id)
        for line in report(base_id, hotels):
            print(line)
    if zero:
        raise SystemExit("Hotel Fit coverage audit failed: zero inventory for " + ", ".join(zero))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
