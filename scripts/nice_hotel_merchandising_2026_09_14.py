#!/usr/bin/env python3
"""Legacy Nice static-grid merchandising pass.

Nice moved to the data-driven hotel decision engine on 2026-09-16. The engine
uses data/hotels/nice.json as its 20-hotel inventory, so reordering static cards
here would both fail and duplicate merchandising logic. Kept as a no-op because
the production workflow still calls this historical step.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    data_path = ROOT / "data/hotels/nice.json"
    if not data_path.is_file():
        raise RuntimeError("Missing Nice hotel engine dataset")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if data.get("coverage", {}).get("published") != 20 or len(data.get("hotels", [])) != 20:
        raise RuntimeError("Nice hotel engine must contain 20 published hotels")
    for rel in ("fr/dormir/nice/index.html", "stay/nice/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "data-hotel-engine" not in text:
            raise RuntimeError(f"{rel}: hotel decision engine marker missing")
    print("Nice merchandising is handled by the 20-hotel decision engine; legacy static-grid pass skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
