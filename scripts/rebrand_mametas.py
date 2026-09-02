#!/usr/bin/env python3
"""Apply the Mametas production identity to the active static HTML catalogue.

Backup snapshots whose directory name starts with ``lesnicoises-v8`` are
deliberately excluded. They are historical material, not deployed pages.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONSENT_SNIPPET = '<script defer src="/assets/consent.js?v=1.0"></script>'

LEGACY_GA_RE = re.compile(
    r'\s*<!-- Google tag \(gtag\.js\) -->\s*'
    r'<script[^>]*src="https://www\.googletagmanager\.com/gtag/js\?id=G-8B7JENJ1MD"[^>]*></script>\s*'
    r'<script>.*?gtag\(\'config\', \'G-8B7JENJ1MD\'\);\s*</script>\s*',
    flags=re.DOTALL,
)

V3_ROUTES = {
    "index.html": ("/", "/", "/fr/", "en_US"),
    "fr/index.html": ("/fr/", "/", "/fr/", "fr_FR"),
    "plan/five-days-nice-no-car/index.html": (
        "/plan/five-days-nice-no-car/",
        "/plan/five-days-nice-no-car/",
        "/fr/planifier/cinq-jours-nice-sans-voiture/",
        "en_US",
    ),
    "fr/planifier/cinq-jours-nice-sans-voiture/index.html": (
        "/fr/planifier/cinq-jours-nice-sans-voiture/",
        "/plan/five-days-nice-no-car/",
        "/fr/planifier/cinq-jours-nice-sans-voiture/",
        "fr_FR",
    ),
    "stay/nice/index.html": ("/stay/nice/", "/stay/nice/", "/fr/dormir/nice/", "en_US"),
    "fr/dormir/nice/index.html": ("/fr/dormir/nice/", "/stay/nice/", "/fr/dormir/nice/", "fr_FR"),
}


def is_active_html(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return not any(part.startswith("lesnicoises-v8") for part in relative.parts)


def nav_items(language: str, relative: Path) -> str:
    path = relative.as_posix()
    if language == "en":
        entries = [
            ("Plan", "/#plan", path.startswith("plan/")),
            ("Places", "/en/riviera-guide/", path.startswith("en/riviera-guide/")),
            ("Stay", "/stay/nice/", path.startswith("stay/") or path.startswith("en/hotels/")),
            (
                "Eat &amp; Do",
                "/en/restaurants/",
                any(path.startswith(prefix) for prefix in ("en/restaurants/", "en/beaches/", "en/culture/", "en/day-trips/")),
            ),
            ("Now", "/en/good-finds/", path.startswith("en/good-finds/")),
        ]
    else:
        entries = [
            ("Planifier", "/fr/#planifier", path.startswith("fr/planifier/")),
            ("Lieux", "/riviera-guide/", path.startswith("riviera-guide/")),
            ("Dormir", "/fr/dormir/nice/", path.startswith("fr/dormir/") or path.startswith("hotels/")),
            (
                "Manger &amp; faire",
                "/restaurants/",
                any(path.startswith(prefix) for prefix in ("restaurants/", "plages/", "culture/", "escapades/")),
            ),
            ("Maintenant", "/bons-plans/", path.startswith("bons-plans/")),
        ]

    items = []
    for label, href, current in entries:
        aria = ' aria-current="page"' if current else ""
        items.append(f'<li><a{aria} href="{href}">{label}</a></li>')
    return "<ul>" + "".join(items) + "</ul>"


def rebrand_legacy_navigation(html: str, language: str, relative: Path) -> str:
    nav = nav_items(language, relative)
    html = re.sub(
        r'<nav class="primary-nav"><ul>.*?</ul></nav>',
        f'<nav class="primary-nav">{nav}</nav>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'(<div class="mobile-nav"[^>]*>.*?<div class="mobile-nav-top">.*?</div>)<ul>.*?</ul>',
        lambda match: match.group(1) + nav,
        html,
        count=1,
        flags=re.DOTALL,
    )
    home = "/" if language == "en" else "/fr/"
    html = re.sub(r'<a class="brand" href="[^"]*">', f'<a class="brand" href="{home}">', html, count=1)
    return html


def production_metadata(html: str, relative: Path) -> str:
    route = V3_ROUTES.get(relative.as_posix())
    if not route:
        if relative.as_posix() == "en/index.html":
            html = re.sub(
                r'<meta content="[^"]+" name="robots"/?>',
                '<meta content="noindex,follow" name="robots"/>',
                html,
                count=1,
            )
        english = re.search(r'<link href="([^"]+)" hreflang="en" rel="alternate"/?>', html)
        if english:
            html = re.sub(
                r'<link href="[^"]+" hreflang="x-default" rel="alternate"/?>',
                f'<link href="{english.group(1)}" hreflang="x-default" rel="alternate"/>',
                html,
            )
        return html

    canonical_path, english_path, french_path, locale = route
    canonical = "https://www.mametas.com" + canonical_path
    english = "https://www.mametas.com" + english_path
    french = "https://www.mametas.com" + french_path
    metadata = (
        f'  <link rel="canonical" href="{canonical}">\n'
        f'  <link rel="alternate" hreflang="en" href="{english}">\n'
        f'  <link rel="alternate" hreflang="fr" href="{french}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{english}">\n'
    )
    if 'rel="canonical"' not in html:
        html = html.replace('  <meta name="robots"', metadata + '  <meta name="robots"', 1)
    html = re.sub(
        r'<meta name="robots" content="[^"]+">',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        html,
        count=1,
    )
    if 'property="og:url"' not in html:
        html = html.replace(
            '  <meta property="og:image"',
            f'  <meta property="og:url" content="{canonical}">\n'
            f'  <meta property="og:site_name" content="Mametas">\n'
            f'  <meta property="og:locale" content="{locale}">\n'
            '  <meta property="og:image"',
            1,
        )
    html = re.sub(
        r'<meta property="og:image" content="[^"]+">',
        '<meta property="og:image" content="https://www.mametas.com/assets/editorial/mametas-five-women-hero.webp">',
        html,
        count=1,
    )
    html = html.replace("V3 private preview · © 2026 Mametas", "© 2026 Mametas")
    html = html.replace("Aperçu privé V3 · © 2026 Mametas", "© 2026 Mametas")
    html = html.replace("/assets/v3.css?v=0.3", "/assets/v3.css?v=0.4")
    html = html.replace(
        "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,500",
        "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500",
    )
    return html


def transform(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    html = path.read_text(encoding="utf-8")
    original = html
    language_match = re.search(r'<html[^>]*lang="([^"]+)"', html, flags=re.IGNORECASE)
    language = "en" if language_match and language_match.group(1).lower().startswith("en") else "fr"

    replacements = [
        ("https://www.lesnicoises.com", "https://www.mametas.com"),
        ("https://lesnicoises.com", "https://www.mametas.com"),
        ("http://www.lesnicoises.com", "https://www.mametas.com"),
        ("http://lesnicoises.com", "https://www.mametas.com"),
        ("www.lesnicoises.com", "www.mametas.com"),
        ("lesnicoises.com", "www.mametas.com"),
        ("/assets/hero-les-nicoises-final.png", "/assets/editorial/mametas-five-women-hero.webp"),
        ("/assets/hero-les-nicoises-fr.png", "/assets/editorial/mametas-five-women-hero.webp"),
        ("/assets/hero-les-nicoises-en.png", "/assets/editorial/mametas-five-women-hero.webp"),
        ("/assets/hero-les-nicoises.jpg", "/assets/editorial/mametas-five-women-hero.webp"),
        ("LE VERDICT DES NIÇOISES", "LE VERDICT DE MAMETAS"),
        ("Le verdict des Niçoises", "Le verdict de Mametas"),
        ("verdict des Niçoises", "verdict de Mametas"),
        ("THE NIÇOISES VERDICT", "THE MAMETAS VERDICT"),
        ("The Niçoises verdict", "The Mametas verdict"),
        ("LES NIÇOISES SAY", "MAMETAS SAYS"),
        ("The Les Niçoises manifesto", "The Mametas manifesto"),
        ("Le manifeste des Niçoises", "Le manifeste de Mametas"),
        ("Le manifeste Mametas : cinq personnages fictifs", "Le manifeste de Mametas : cinq matriarches fictives"),
        ("<span class=\"brand-name\">LES NIÇOISES</span>", "<span class=\"brand-name\">Mametas</span>"),
        ("<span class=\"brand-sub\">RIVIERA INSIDERS</span>", "<span class=\"brand-sub\">They know the Riviera.</span>"),
        ("© 2026 LES NIÇOISES • RIVIERA INSIDERS", "© 2026 Mametas · They know the Riviera."),
        ("Les Niçoises", "Mametas"),
        ("LES NIÇOISES", "MAMETAS"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    # English is now the canonical homepage at the domain root. Keep /en/ only
    # for catalogue pages; homepage and breadcrumb references must not target a
    # URL that will redirect in production.
    html = html.replace('https://www.mametas.com/en/"', 'https://www.mametas.com/"')

    html = production_metadata(html, relative)

    # Analytics is loaded only after an explicit choice. Remove the former
    # eager-loading snippet from every page before adding the shared controller.
    html = LEGACY_GA_RE.sub("\n", html, count=1)

    if 'class="site-header"' in html:
        html = rebrand_legacy_navigation(html, language, relative)
        html = re.sub(r'/assets/site\.css(?:\?v=[^"\']+)?', "/assets/site.css?v=23.0", html)

    if 'rel="icon"' not in html:
        html = html.replace("</head>", '<link href="/favicon.svg" rel="icon" type="image/svg+xml"/></head>', 1)

    if "/assets/consent.js" not in html:
        html = html.replace("</head>", CONSENT_SNIPPET + "</head>", 1)

    if 'data-privacy-link="true"' not in html and "</footer>" in html:
        if language == "en":
            privacy = '<div class="privacy-links"><a data-privacy-link="true" href="/privacy/">Privacy &amp; cookies</a></div>'
        else:
            privacy = '<div class="privacy-links"><a data-privacy-link="true" href="/fr/confidentialite/">Confidentialité &amp; cookies</a></div>'
        html = html.replace("</footer>", privacy + "</footer>", 1)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = [path for path in ROOT.rglob("*.html") if is_active_html(path) and transform(path)]
    sitemap_path = ROOT / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    sitemap = sitemap.replace("https://lesnicoises.com", "https://www.mametas.com")
    sitemap = re.sub(r'\s*<url><loc>https://www\.mametas\.com/en/</loc>.*?</url>', "", sitemap)
    sitemap = sitemap.replace(
        '<url><loc>https://www.mametas.com/</loc><lastmod>2026-08-29</lastmod></url>',
        '<url><loc>https://www.mametas.com/</loc><lastmod>2026-09-02</lastmod></url>',
    )
    additions = [
        "https://www.mametas.com/fr/",
        "https://www.mametas.com/privacy/",
        "https://www.mametas.com/fr/confidentialite/",
        "https://www.mametas.com/plan/five-days-nice-no-car/",
        "https://www.mametas.com/fr/planifier/cinq-jours-nice-sans-voiture/",
        "https://www.mametas.com/stay/nice/",
        "https://www.mametas.com/fr/dormir/nice/",
    ]
    entries = "\n".join(
        f'  <url><loc>{url}</loc><lastmod>2026-09-02</lastmod></url>'
        for url in additions
        if f"<loc>{url}</loc>" not in sitemap
    )
    if entries:
        sitemap = sitemap.replace("</urlset>", entries + "\n</urlset>")
    sitemap_path.write_text(sitemap, encoding="utf-8")
    print(f"Rebranded {len(changed)} active HTML files.")


if __name__ == "__main__":
    main()
