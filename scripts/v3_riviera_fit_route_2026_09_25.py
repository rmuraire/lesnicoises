#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRS = (
    ("riviera-chooser/index.html", "riviera-fit/index.html", "fr"),
    ("en/riviera-chooser/index.html", "en/riviera-fit/index.html", "en"),
)

REPLACEMENTS = (
    ("https://www.mametas.com/en/riviera-chooser/", "https://www.mametas.com/en/riviera-fit/"),
    ("https://www.mametas.com/riviera-chooser/", "https://www.mametas.com/riviera-fit/"),
    ("/en/riviera-chooser/", "/en/riviera-fit/"),
    ("/riviera-chooser/", "/riviera-fit/"),
)

def replace_routes(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text

def brand_page(text: str, lang: str) -> str:
    text = replace_routes(text)
    if lang == "fr":
        text = text.replace(
            "<title>Riviera Fit : quelle base choisir sur la Côte d’Azur ? | Mametas</title>",
            "<title>Mametas Riviera Fit : quelle base choisir sur la Côte d’Azur ?</title>",
        )
        text = text.replace('content="Riviera Fit | Mametas"', 'content="Mametas Riviera Fit"')
        text = text.replace("RIVIERA FIT · LE DIAGNOSTIC MAMETAS", "MAMETAS RIVIERA FIT · LA RECO")
        text = text.replace("RIVIERA FIT · LA RECO MAMETAS", "MAMETAS RIVIERA FIT · LA RECO")
    else:
        text = text.replace(
            "<title>Riviera Fit: where should you stay on the French Riviera? | Mametas</title>",
            "<title>Mametas Riviera Fit: where should you stay on the French Riviera?</title>",
        )
        text = text.replace('content="Riviera Fit | Mametas"', 'content="Mametas Riviera Fit"')
        text = text.replace("RIVIERA FIT · THE MAMETAS DIAGNOSIS", "MAMETAS RIVIERA FIT · THE CALL")
        text = text.replace("RIVIERA FIT · THE MAMETAS CALL", "MAMETAS RIVIERA FIT · THE CALL")
    return text

def legacy_page(text: str, lang: str) -> str:
    # The server returns a 301 before this file is served. Keep a complete valid
    # fallback document so repository validators still see one H1, consent and
    # a unique legacy canonical.
    if lang == "fr":
        text = text.replace("RIVIERA FIT · LE DIAGNOSTIC MAMETAS", "MAMETAS RIVIERA FIT · LA RECO")
        text = text.replace("RIVIERA FIT · LA RECO MAMETAS", "MAMETAS RIVIERA FIT · LA RECO")
    else:
        text = text.replace("RIVIERA FIT · THE MAMETAS DIAGNOSIS", "MAMETAS RIVIERA FIT · THE CALL")
        text = text.replace("RIVIERA FIT · THE MAMETAS CALL", "MAMETAS RIVIERA FIT · THE CALL")
    return text

def main() -> int:
    # Build the new canonical pages from the fully materialised chooser pages.
    originals = {}
    for src_rel, dst_rel, lang in PAIRS:
        src = ROOT / src_rel
        if not src.is_file():
            raise RuntimeError(f"Missing source page: {src_rel}")
        original = src.read_text(encoding="utf-8")
        originals[src_rel] = original
        dst = ROOT / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(brand_page(original, lang), encoding="utf-8")

    # Point every generated HTML link at the new canonical route.
    for path in ROOT.rglob("*.html"):
        if any(part.startswith(".") for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        new = replace_routes(text)
        if new != text:
            path.write_text(new, encoding="utf-8")

    # Keep full valid fallback pages behind the server-side 301 rules.
    (ROOT / "riviera-chooser/index.html").write_text(
        legacy_page(originals["riviera-chooser/index.html"], "fr"), encoding="utf-8"
    )
    (ROOT / "en/riviera-chooser/index.html").write_text(
        legacy_page(originals["en/riviera-chooser/index.html"], "en"), encoding="utf-8"
    )

    for rel in ("sitemap.xml", "sitemap-hotels-batch2.xml"):
        path = ROOT / rel
        if path.is_file():
            text = replace_routes(path.read_text(encoding="utf-8"))
            path.write_text(text, encoding="utf-8")

    checks = {
        "riviera-fit/index.html": (
            '<p class="tool-badge">MAMETAS TOOL</p>',
            "RIVIERA FIT · LA RECO",
            'rel="canonical" href="https://www.mametas.com/riviera-fit/"',
            "/en/riviera-fit/",
        ),
        "en/riviera-fit/index.html": (
            '<p class="tool-badge">MAMETAS TOOL</p>',
            "RIVIERA FIT · THE CALL",
            'rel="canonical" href="https://www.mametas.com/en/riviera-fit/"',
            "/riviera-fit/",
        ),
        "riviera-chooser/index.html": (
            'rel="canonical" href="https://www.mametas.com/riviera-chooser/"',
            "<h1>Cinq questions. Une base. Et les compromis avec.</h1>",
        ),
        "en/riviera-chooser/index.html": (
            'rel="canonical" href="https://www.mametas.com/en/riviera-chooser/"',
            "<h1>Five questions. One base. Trade-offs included.</h1>",
        ),
    }
    errors = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")

    ht = (ROOT / ".htaccess").read_text(encoding="utf-8")
    for needle in (
        "RewriteRule ^riviera-chooser/?$ /riviera-fit/ [R=301,L]",
        "RewriteRule ^en/riviera-chooser/?$ /en/riviera-fit/ [R=301,L]",
    ):
        if needle not in ht:
            errors.append(f".htaccess: missing {needle}")

    if errors:
        raise SystemExit("Riviera Fit route migration failed:\n- " + "\n- ".join(errors))
    print("Mametas Riviera Fit canonical route migration passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
