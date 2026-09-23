#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXACT_REPLACEMENTS = {
    "index.html": (
        ('href="#plan">Plan</a>', 'href="/plan/five-days-nice-no-car/">Plan</a>'),
        ('href="#places">Places</a>', 'href="/en/riviera-guide/">Places</a>'),
        ('href="#explore">Explore</a>', 'href="/en/explore/">Explore</a>'),
        ('href="#now">Now</a>', 'href="/en/good-finds/">Now</a>'),
        ('/assets/v3.css?v=0.5', '/assets/v3.css?v=0.9'),
        ('<script src="/assets/v3.js"></script>', '<script src="/assets/v3.js?v=0.9"></script>'),
        ('<script src="/assets/v3.js?v=0.6"></script>', '<script src="/assets/v3.js?v=0.9"></script>'),
    ),
    "fr/index.html": (
        ('href="#planifier">Planifier</a>', 'href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a>'),
        ('href="#lieux">Lieux</a>', 'href="/riviera-guide/">Lieux</a>'),
        ('href="#explorer">Explorer</a>', 'href="/explore/">Explorer</a>'),
        ('href="#maintenant">Maintenant</a>', 'href="/bons-plans/">Maintenant</a>'),
        ('/assets/v3.css?v=0.5', '/assets/v3.css?v=0.9'),
        ('<script src="/assets/v3.js"></script>', '<script src="/assets/v3.js?v=0.9"></script>'),
        ('<script src="/assets/v3.js?v=0.6"></script>', '<script src="/assets/v3.js?v=0.9"></script>'),
    ),
    "riviera-guide/index.html": (
        ('family=Inter:wght@400;500;600&amp;display=swap', 'family=Inter:wght@400;500;600;700&amp;display=swap'),
        ('/assets/site.css?v=23.0', '/assets/site.css?v=23.4'),
        ('/assets/site.css?v=23.1', '/assets/site.css?v=23.4'),
    ),
    "bons-plans/index.html": (
        ('family=Inter:wght@400;500;600&amp;display=swap', 'family=Inter:wght@400;500;600;700&amp;display=swap'),
        ('/assets/site.css?v=23.0', '/assets/site.css?v=23.4'),
        ('/assets/site.css?v=23.1', '/assets/site.css?v=23.4'),
    ),
    "en/good-finds/index.html": (
        ('family=Inter:wght@400;500;600&amp;display=swap', 'family=Inter:wght@400;500;600;700&amp;display=swap'),
        ('/assets/site.css?v=23.0', '/assets/site.css?v=23.4'),
        ('/assets/site.css?v=23.1', '/assets/site.css?v=23.4'),
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


GLOBAL_HTML_REPLACEMENTS = (
    ('href="/#plan">Plan</a>', 'href="/plan/five-days-nice-no-car/">Plan</a>'),
    ('href="#plan">Plan</a>', 'href="/plan/five-days-nice-no-car/">Plan</a>'),
    ('href="/#places">Places</a>', 'href="/en/riviera-guide/">Places</a>'),
    ('href="#places">Places</a>', 'href="/en/riviera-guide/">Places</a>'),
    ('href="/stay/nice/">Stay</a>', 'href="/en/hotels/">Stay</a>'),
    ('href="/en/restaurants/">Eat & Do</a>', 'href="/en/explore/">Explore</a>'),
    ('href="/en/restaurants/">Eat &amp; Do</a>', 'href="/en/explore/">Explore</a>'),
    ('href="/#now">Now</a>', 'href="/en/good-finds/">Now</a>'),
    ('href="#now">Now</a>', 'href="/en/good-finds/">Now</a>'),
    ('href="/fr/#planifier">Planifier</a>', 'href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a>'),
    ('href="#planifier">Planifier</a>', 'href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a>'),
    ('href="#lieux">Lieux</a>', 'href="/riviera-guide/">Lieux</a>'),
    ('href="/fr/dormir/nice/">Dormir</a>', 'href="/hotels/">Dormir</a>'),
    ('href="/restaurants/">Manger & faire</a>', 'href="/explore/">Explorer</a>'),
    ('href="/restaurants/">Manger &amp; faire</a>', 'href="/explore/">Explorer</a>'),
    ('href="#maintenant">Maintenant</a>', 'href="/bons-plans/">Maintenant</a>'),
    ('/assets/v3.css?v=0.4', '/assets/v3.css?v=0.6'),
    ('/assets/v3.css?v=0.5', '/assets/v3.css?v=0.6'),
    ('<script src="/assets/v3.js"></script>', '<script src="/assets/v3.js?v=0.9"></script>'),
    ('<script src="/assets/v3.js?v=0.6"></script>', '<script src="/assets/v3.js?v=0.9"></script>'),
    ('/assets/site.css?v=23.0', '/assets/site.css?v=23.4'),
    ('/assets/site.css?v=23.1', '/assets/site.css?v=23.4'),
    ('/assets/site.css?v=23.2', '/assets/site.css?v=23.4'),
    ('<script src="/assets/site.js"></script>', '<script src="/assets/site.js?v=23.2"></script>'),
)


MENU_ENTRY_PAGES = (
    "index.html",
    "fr/index.html",
    "plan/five-days-nice-no-car/index.html",
    "fr/planifier/cinq-jours-nice-sans-voiture/index.html",
    "en/riviera-guide/index.html",
    "riviera-guide/index.html",
    "en/hotels/index.html",
    "hotels/index.html",
    "en/explore/index.html",
    "explore/index.html",
    "en/good-finds/index.html",
    "bons-plans/index.html",
)

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

    for rel in MENU_ENTRY_PAGES:
        html_path = ROOT / rel
        text = html_path.read_text(encoding="utf-8")
        original = text
        for old, new in GLOBAL_HTML_REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            html_path.write_text(text, encoding="utf-8")
            changed.append(rel)

    css = ROOT / "assets/site.css"
    css_text = css.read_text(encoding="utf-8")
    if "\\n" in css_text:
        css_text = css_text.replace("\\n", "\n")
    font_import = '@import url("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap");\\n\\n'
    if not css_text.startswith("@import"):
        css_text = font_import + css_text
    typography_marker = "/* Final typography parity 2026-09-19 */"
    if typography_marker not in css_text:
        css_text += """\n\n/* Final typography parity 2026-09-19 */
.page-hero h1,.article h1,.hotel-detail h1,.culture-detail h1{font-family:var(--serif);font-weight:500;letter-spacing:-.045em;text-transform:none}
.lead,.article .standfirst,.hotel-detail .standfirst,.culture-detail .standfirst{font-family:var(--serif);font-weight:400}
@media(max-width:650px){
  .page-hero h1{font-size:clamp(42px,13vw,62px);line-height:.98}
  .lead{font-size:clamp(20px,6vw,25px);line-height:1.42}
  .article .standfirst,.hotel-detail .standfirst,.culture-detail .standfirst{font-size:22px;line-height:1.45}
}
"""
    css.write_text(css_text, encoding="utf-8")
    if "assets/site.css" not in changed:
        changed.append("assets/site.css")

    # Cache-bust the shared site script everywhere so dialect links and shared fixes are visible immediately.
    for html_path in ROOT.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        original = text
        text = text.replace('/assets/site.js"></script>', '/assets/site.js?v=23.2"></script>')
        text = text.replace('/assets/site.js?v=23.1"></script>', '/assets/site.js?v=23.2"></script>')
        if text != original:
            html_path.write_text(text, encoding="utf-8")
            rel = str(html_path.relative_to(ROOT))
            if rel not in changed:
                changed.append(rel)

    # Cache-bust the legacy stylesheet everywhere so the typography pass is visible immediately.
    for html_path in ROOT.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        original = text
        for old in ("23.0", "23.1", "23.2", "23.3"):
            text = text.replace(f"/assets/site.css?v={old}", "/assets/site.css?v=23.4")
        if text != original:
            html_path.write_text(text, encoding="utf-8")
            rel = str(html_path.relative_to(ROOT))
            if rel not in changed:
                changed.append(rel)

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
            "{label:'Plan',href:'/plan/five-days-nice-no-car/'}",
            "{label:'Planifier',href:'/fr/planifier/cinq-jours-nice-sans-voiture/'}",
        ),
        "assets/v3.js": (
            "if (!menu && header)",
            "data-v3-menu-open",
            "data-menu-bound",
            '{ label: "Plan", href: "/plan/five-days-nice-no-car/" }',
            '{ label: "Places", href: "/en/riviera-guide/" }',
            '{ label: "Stay", href: "/en/hotels/" }',
            '{ label: "Explore", href: "/en/explore/" }',
            '{ label: "Now", href: "/en/good-finds/" }',
            '{ label: "Planifier", href: "/fr/planifier/cinq-jours-nice-sans-voiture/" }',
            '{ label: "Explorer", href: "/explore/" }',
        ),
        "index.html": (
            'href="/plan/five-days-nice-no-car/">Plan</a>',
            'href="/en/riviera-guide/">Places</a>',
            'href="/en/hotels/">Stay</a>',
            'href="/en/explore/">Explore</a>',
            'href="/en/good-finds/">Now</a>',
            '/assets/v3.css?v=0.9',
            '/assets/v3.js?v=0.9',
        ),
        "fr/index.html": (
            'href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a>',
            'href="/riviera-guide/">Lieux</a>',
            'href="/hotels/">Dormir</a>',
            'href="/explore/">Explorer</a>',
            'href="/bons-plans/">Maintenant</a>',
            '/assets/v3.css?v=0.9',
            '/assets/v3.js?v=0.9',
        ),
        "assets/site.css": (
            "@media(max-width:1080px){.primary-nav{display:none}",
            "/* Canonical header parity with V3 navigation */",
            "background:rgba(244,239,228,.96)",
            "padding:14px clamp(20px,4vw,64px)",
            'content:""',
            ".header-inner>.lang-switch span{color:rgba(20,33,61,.4)}",
            ".brand{display:inline-flex;flex-direction:column;flex:0 0 auto;line-height:normal}",
            "line-height:normal",
        ),
        "riviera-guide/index.html": (
            "family=Inter:wght@400;500;600;700&amp;display=swap",
            "/assets/site.css?v=23.4",
        ),
        "bons-plans/index.html": (
            "family=Inter:wght@400;500;600;700&amp;display=swap",
            "/assets/site.css?v=23.4",
        ),
        "en/good-finds/index.html": (
            "family=Inter:wght@400;500;600;700&amp;display=swap",
            "/assets/site.css?v=23.4",
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
    stale_home_links = (
        'href="#plan">Plan</a>',
        'href="#places">Places</a>',
        'href="#explore">Explore</a>',
        'href="#now">Now</a>',
    )
    for needle in stale_home_links:
        if needle in en_home:
            errors.append(f"index.html: stale homepage menu link {needle!r}")
    stale_fr_home_links = (
        'href="#planifier">Planifier</a>',
        'href="#lieux">Lieux</a>',
        'href="#explorer">Explorer</a>',
        'href="#maintenant">Maintenant</a>',
    )
    for needle in stale_fr_home_links:
        if needle in fr_home:
            errors.append(f"fr/index.html: stale homepage menu link {needle!r}")

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
