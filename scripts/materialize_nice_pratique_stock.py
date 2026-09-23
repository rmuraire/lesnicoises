#!/usr/bin/env python3
"""Materialize the web-optimized Depositphotos Nice practical bundle when present.

The source ZIP is intentionally versioned as a .zip (excluded from public deployment).
Its contents are extracted into assets/editorial/depositphotos/nice-pratique/ during the
build, so the static deploy sees the WebP files as materialized public outputs.
"""
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "MAMETAS_NICE_PRATIQUE_WEB.zip"
PREFIX = "assets/editorial/depositphotos/nice-pratique/"

def main() -> int:
    if not ARCHIVE.exists():
        print("Nice practical stock archive not present; keeping current fallbacks.")
        return 0

    extracted = 0
    with ZipFile(ARCHIVE) as zf:
        for info in zf.infolist():
            name = info.filename.replace("\\", "/").lstrip("/")
            if info.is_dir() or not name.startswith(PREFIX):
                continue
            target = (ROOT / name).resolve()
            if ROOT.resolve() not in target.parents:
                raise RuntimeError(f"Unsafe archive path: {name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, target.open("wb") as dst:
                dst.write(src.read())
            extracted += 1

    print(f"Materialized {extracted} Nice practical stock asset(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
