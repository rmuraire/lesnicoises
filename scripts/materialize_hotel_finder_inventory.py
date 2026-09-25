#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "hotels" / "nice.json"
FIT_SOURCE = ROOT / "data" / "hotels" / "hotel-fit-v3.json"
OUTPUT = ROOT / "assets" / "hotel-finder-nice.json"


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    fit_source = json.loads(FIT_SOURCE.read_text(encoding="utf-8")) if FIT_SOURCE.is_file() else {}
    fit_hotels = fit_source.get("hotels", {})
    hotels = []
    for item in source.get("hotels", []):
        expedia = (item.get("affiliate") or {}).get("expedia") or {}
        affiliate_url = expedia.get("url", "") if expedia.get("status") == "active" else ""
        raw_image = item.get("image", "") or ""
        image = "" if "batch-sprite" in raw_image else raw_image
        hotels.append({
            "id": item.get("id", ""),
            "name": item.get("name", ""),
            "neighborhood": item.get("neighborhood", ""),
            "priceBand": item.get("priceBand", ""),
            "styles": item.get("styles", []),
            "tripLengths": item.get("tripLengths", []),
            "carFree": bool(item.get("carFree")),
            "stationFriendly": bool(item.get("stationFriendly")),
            "seaAccess": bool(item.get("seaAccess")),
            "oldTownAccess": bool(item.get("oldTownAccess")),
            "quiet": bool(item.get("quiet")),
            "image": image,
            "paths": item.get("paths", {}),
            "affiliate": {"url": affiliate_url} if affiliate_url else {},
            "fit": fit_hotels.get(item.get("id", ""), {}),
        })

    payload = {
        "schemaVersion": 2,
        "base": "nice",
        "fitSchemaVersion": fit_source.get("schemaVersion"),
        "fitTagLabels": fit_source.get("tagLabels", {}),
        "lastEditorialReview": source.get("lastEditorialReview"),
        "priceBandNote": source.get("priceBandNote", {}),
        "hotels": hotels,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Materialized {len(hotels)} Nice hotels to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
