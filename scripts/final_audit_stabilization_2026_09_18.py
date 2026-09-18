#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXACT_REPLACEMENTS = {
    "index.html": (
        ('href="#explore">Explore</a>', 'href="/en/explore/">Explore</a>'),
        ('<script src="/assets/v3.js"></script>', '<script src="/assets/v3.js?v=0.6"></script>'),
    ),
    "fr/index.html": (
        ('href="#explorer">Explorer</a>', 'href="/explore/">Explorer</a>'),
        ('<script src="/assets/v3.js"></script>', '<script src="/assets/v3.js?v=0.6"></script>'),
    ),
    "fr/planifier/cinq-jours-nice-sans-voiture/index.html": (
        ("/fr/dormir/nice/#anime", "/fr/dormir/nice/#vivant"),
        ("/fr/dormir/nice/#paisible", "/fr/dormir/nice/#calme"),
    ),
    "riviera-guide/monaco/index.html": (
        ("/fr/planifier/cinq-jours-nice-sans-voiture/#day-three",
         "/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois"),
    ),
    "riviera-guide/menton/index.html": (
        ("/fr/planifier/cinq-jours-nice-sans-voiture/#day-three",
         "/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois"),
    ),
    "en/day-trips/index.html": (
        ("/en/riviera-guide/nice-or-cannes/",
         "/en/riviera-guide/antibes/#cannes"),
    ),
    "sitemap-hotels-batch2.xml": (
        ("https://www.mametas.com/explorer/",
         "https://www.mametas.com/explore/"),
    ),
}

def patch_file(rel: str, pairs) -> bool:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False

def main() -> int:
    changed = []
    for rel, pairs in EXACT_REPLACEMENTS.items():
        if patch_file(rel, pairs):
            changed.append(rel)

    css = ROOT / "assets/site.css"
    css_text = css.read_text(encoding="utf-8")
    if "\\n" in css_text:
        css.write_text(css_text.replace("\\n", "\n"), encoding="utf-8")
        changed.append("assets/site.css")

    checks = {
        "assets/hotel-engine.js": (
            "id:'mougins'",
            "stationFriendly:false, noCarFriendly:false",
            "if (state.mobility === 'nocar' && !sig.noCar) return false;",
            "dataPath:'/assets/hotel-finder-nice.json?v=2'",
        ),
        "assets/site.js": (
            "if(!mobile&&header)",
            "provider=/expedia",
            "data-menu-bound",
        ),
        "assets/v3.js": (
            "if (!menu && header)",
            "data-v3-menu-open",
            "data-menu-bound",
            '{ label: "Explore", href: "/en/explore/" }',
            '{ label: "Explorer", href: "/explore/" }',
        ),
        "index.html": (
            'href="/en/explore/">Explore</a>',
            '/assets/v3.js?v=0.6',
        ),
        "fr/index.html": (
            'href="/explore/">Explorer</a>',
            '/assets/v3.js?v=0.6',
        ),
        "assets/site.css": (
            "@media(max-width:1080px){.primary-nav{display:none}",
        ),
        "assets/v3.css": (
            ".v3-nav, .v3-header-inner > .lang-switch { display: none; }",
        ),
    }
    errors = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")

    target_checks = {
        "fr/dormir/nice/index.html": ('id="vivant"', 'id="calme"'),
        "fr/planifier/cinq-jours-nice-sans-voiture/index.html": ('id="jour-trois"',),
        "en/riviera-guide/antibes/index.html": ('id="cannes"',),
    }
    for rel, needles in target_checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing target {needle!r}")

    en_home = (ROOT / "index.html").read_text(encoding="utf-8")
    fr_home = (ROOT / "fr/index.html").read_text(encoding="utf-8")
    if 'href="#explore">Explore</a>' in en_home:
        errors.append("index.html: homepage Explore still points to local anchor")
    if 'href="#explorer">Explorer</a>' in fr_home:
        errors.append("fr/index.html: homepage Explorer still points to local anchor")

    sitemap = (ROOT / "sitemap-hotels-batch2.xml").read_text(encoding="utf-8")
    if "https://www.mametas.com/explorer/" in sitemap:
        errors.append("sitemap-hotels-batch2.xml: stale /explorer/ URL remains")

    if errors:
        raise SystemExit("Final audit stabilization failed:\n- " + "\n- ".join(errors))

    print(f"Final audit stabilization passed; patched {len(changed)} generated file(s).")
    for rel in changed:
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
