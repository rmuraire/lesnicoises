#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas coherence audit — phase 1: one global shell.

Runs late in the production build, after every legacy/materialization layer.
It replaces the many historical headers, mobile menus and footers with one
build-time canonical shell while preserving each page's content and URLs.
"""
from pathlib import Path
from urllib.parse import urlparse
import html
import re

ROOT = Path(__file__).resolve().parents[1]
SHELL_CSS = "/assets/mametas-shell-v1.css?v=1.0"
MARK = 'data-mametas-shell="v1"'
SKIP_TOP = {
    ".git", ".github", "docs", "scripts", "data", "backup",
    "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2",
}

EN_NAV = [
    ("/plan/", "Plan"),
    ("/en/riviera-guide/", "Places"),
    ("/en/hotels/", "Stay"),
    ("/en/explore/", "Explore"),
    ("/en/practical/", "Practical"),
]
FR_NAV = [
    ("/fr/planifier/", "Préparer"),
    ("/riviera-guide/", "Destinations"),
    ("/hotels/", "Dormir"),
    ("/explore/", "Explorer"),
    ("/pratique/", "Pratique"),
]

PAIR_FALLBACKS = {
    "/": ("/fr/", "/"),
    "/fr/": ("/fr/", "/"),
    "/en/": ("/fr/", "/"),
    "/plan/": ("/fr/planifier/", "/plan/"),
    "/fr/planifier/": ("/fr/planifier/", "/plan/"),
    "/plan/three-days-riviera/": ("/fr/planifier/trois-jours-cote-d-azur/", "/plan/three-days-riviera/"),
    "/fr/planifier/trois-jours-cote-d-azur/": ("/fr/planifier/trois-jours-cote-d-azur/", "/plan/three-days-riviera/"),
    "/plan/five-days-nice-no-car/": ("/fr/planifier/cinq-jours-nice-sans-voiture/", "/plan/five-days-nice-no-car/"),
    "/fr/planifier/cinq-jours-nice-sans-voiture/": ("/fr/planifier/cinq-jours-nice-sans-voiture/", "/plan/five-days-nice-no-car/"),
    "/plan/seven-days-riviera/": ("/fr/planifier/sept-jours-cote-d-azur/", "/plan/seven-days-riviera/"),
    "/fr/planifier/sept-jours-cote-d-azur/": ("/fr/planifier/sept-jours-cote-d-azur/", "/plan/seven-days-riviera/"),
    "/plan/car-or-no-car/": ("/fr/planifier/voiture-ou-pas/", "/plan/car-or-no-car/"),
    "/fr/planifier/voiture-ou-pas/": ("/fr/planifier/voiture-ou-pas/", "/plan/car-or-no-car/"),
    "/plan/real-budget/": ("/fr/planifier/budget-reel/", "/plan/real-budget/"),
    "/fr/planifier/budget-reel/": ("/fr/planifier/budget-reel/", "/plan/real-budget/"),
    "/plan/when-to-go/": ("/fr/planifier/quand-partir/", "/plan/when-to-go/"),
    "/fr/planifier/quand-partir/": ("/fr/planifier/quand-partir/", "/plan/when-to-go/"),
    "/en/explore/2-3-hours/": ("/explore/2-3-heures/", "/en/explore/2-3-hours/"),
    "/explore/2-3-heures/": ("/explore/2-3-heures/", "/en/explore/2-3-hours/"),
    "/en/riviera-fit/": ("/riviera-fit/", "/en/riviera-fit/"),
    "/riviera-fit/": ("/riviera-fit/", "/en/riviera-fit/"),
    "/en/riviera-chooser/": ("/riviera-chooser/", "/en/riviera-chooser/"),
    "/riviera-chooser/": ("/riviera-chooser/", "/en/riviera-chooser/"),
    "/stay/nice/": ("/fr/dormir/nice/", "/stay/nice/"),
    "/fr/dormir/nice/": ("/fr/dormir/nice/", "/stay/nice/"),
    "/en/explore/french-riviera-honeymoon/": ("/explore/lune-de-miel-cote-d-azur/", "/en/explore/french-riviera-honeymoon/"),
    "/explore/lune-de-miel-cote-d-azur/": ("/explore/lune-de-miel-cote-d-azur/", "/en/explore/french-riviera-honeymoon/"),
    "/en/explore/french-riviera-babymoon/": ("/explore/babymoon-cote-d-azur/", "/en/explore/french-riviera-babymoon/"),
    "/explore/babymoon-cote-d-azur/": ("/explore/babymoon-cote-d-azur/", "/en/explore/french-riviera-babymoon/"),
    "/en/explore/french-riviera-proposal/": ("/explore/demande-en-mariage-cote-d-azur/", "/en/explore/french-riviera-proposal/"),
    "/explore/demande-en-mariage-cote-d-azur/": ("/explore/demande-en-mariage-cote-d-azur/", "/en/explore/french-riviera-proposal/"),
    "/en/explore/living-antibes-expat/": ("/explore/vivre-antibes-expatrie/", "/en/explore/living-antibes-expat/"),
    "/explore/vivre-antibes-expatrie/": ("/explore/vivre-antibes-expatrie/", "/en/explore/living-antibes-expat/"),
    "/en/explore/retire-french-riviera/": ("/explore/retraite-cote-d-azur/", "/en/explore/retire-french-riviera/"),
    "/explore/retraite-cote-d-azur/": ("/explore/retraite-cote-d-azur/", "/en/explore/retire-french-riviera/"),
    "/en/gay-french-riviera/": ("/cote-dazur-gay/", "/en/gay-french-riviera/"),
    "/cote-dazur-gay/": ("/cote-dazur-gay/", "/en/gay-french-riviera/"),
    "/en/gay-french-riviera/where-to-stay/": ("/cote-dazur-gay/ou-dormir/", "/en/gay-french-riviera/where-to-stay/"),
    "/cote-dazur-gay/ou-dormir/": ("/cote-dazur-gay/ou-dormir/", "/en/gay-french-riviera/where-to-stay/"),
    "/en/gay-french-riviera/beaches-without-a-car/": ("/cote-dazur-gay/plages-sans-voiture/", "/en/gay-french-riviera/beaches-without-a-car/"),
    "/cote-dazur-gay/plages-sans-voiture/": ("/cote-dazur-gay/plages-sans-voiture/", "/en/gay-french-riviera/beaches-without-a-car/"),
    "/en/gay-french-riviera/5-day-itinerary/": ("/cote-dazur-gay/itineraire-5-jours/", "/en/gay-french-riviera/5-day-itinerary/"),
    "/cote-dazur-gay/itineraire-5-jours/": ("/cote-dazur-gay/itineraire-5-jours/", "/en/gay-french-riviera/5-day-itinerary/"),
    "/en/day-trips/": ("/escapades/", "/en/day-trips/"),
    "/escapades/": ("/escapades/", "/en/day-trips/"),
    "/en/day-trips/nice-to-menton-by-train/": ("/escapades/nice-menton-en-train/", "/en/day-trips/nice-to-menton-by-train/"),
    "/escapades/nice-menton-en-train/": ("/escapades/nice-menton-en-train/", "/en/day-trips/nice-to-menton-by-train/"),
    "/en/good-finds/": ("/bons-plans/", "/en/good-finds/"),
    "/bons-plans/": ("/bons-plans/", "/en/good-finds/"),
    "/en/good-finds/nice-airport-transfer/": ("/bons-plans/transfert-aeroport-nice/", "/en/good-finds/nice-airport-transfer/"),
    "/bons-plans/transfert-aeroport-nice/": ("/bons-plans/transfert-aeroport-nice/", "/en/good-finds/nice-airport-transfer/"),
    "/en/good-finds/train-or-bus/": ("/bons-plans/train-ou-bus/", "/en/good-finds/train-or-bus/"),
    "/bons-plans/train-ou-bus/": ("/bons-plans/train-ou-bus/", "/en/good-finds/train-or-bus/"),
    "/en/good-finds/what-to-book/": ("/bons-plans/que-reserver/", "/en/good-finds/what-to-book/"),
    "/bons-plans/que-reserver/": ("/bons-plans/que-reserver/", "/en/good-finds/what-to-book/"),
    "/en/good-finds/nice-in-the-rain/": ("/bons-plans/nice-quand-il-pleut/", "/en/good-finds/nice-in-the-rain/"),
    "/bons-plans/nice-quand-il-pleut/": ("/bons-plans/nice-quand-il-pleut/", "/en/good-finds/nice-in-the-rain/"),
    "/en/good-finds/riviera-mistakes/": ("/bons-plans/erreurs-riviera/", "/en/good-finds/riviera-mistakes/"),
    "/bons-plans/erreurs-riviera/": ("/bons-plans/erreurs-riviera/", "/en/good-finds/riviera-mistakes/"),
    "/en/good-finds/nice-carnival/": ("/bons-plans/carnaval-nice/", "/en/good-finds/nice-carnival/"),
    "/bons-plans/carnaval-nice/": ("/bons-plans/carnaval-nice/", "/en/good-finds/nice-carnival/"),
    "/en/good-finds/ironman-nice/": ("/bons-plans/ironman-nice/", "/en/good-finds/ironman-nice/"),
    "/bons-plans/ironman-nice/": ("/bons-plans/ironman-nice/", "/en/good-finds/ironman-nice/"),
}

def rel_to_route(rel: str) -> str:
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel

def attr(tag: str, name: str):
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*["\']([^"\']+)["\']', tag, re.I)
    return html.unescape(m.group(1)) if m else None

def local_path(url: str):
    if not url:
        return None
    if url.startswith("/"):
        return url
    try:
        p = urlparse(url)
    except Exception:
        return None
    if p.netloc and "mametas.com" not in p.netloc:
        return None
    return p.path or "/"

def alternates(text: str):
    found = {}
    for tag in re.findall(r'<link\b[^>]*>', text, flags=re.I):
        lang = attr(tag, "hreflang")
        href = attr(tag, "href")
        if lang in {"fr", "en"} and href:
            path = local_path(href)
            if path:
                found[lang] = path
    return found

def inferred_pair(route: str):
    if route in PAIR_FALLBACKS:
        return PAIR_FALLBACKS[route]
    if route.startswith("/en/riviera-guide/"):
        return (route.replace("/en/riviera-guide/", "/riviera-guide/", 1), route)
    if route.startswith("/riviera-guide/"):
        return (route, route.replace("/riviera-guide/", "/en/riviera-guide/", 1))
    if route.startswith("/en/hotels/"):
        return (route.replace("/en/hotels/", "/hotels/", 1), route)
    if route.startswith("/hotels/"):
        return (route, route.replace("/hotels/", "/en/hotels/", 1))
    if route.startswith("/en/restaurants/"):
        return (route.replace("/en/restaurants/", "/restaurants/", 1), route)
    if route.startswith("/restaurants/"):
        return (route, route.replace("/restaurants/", "/en/restaurants/", 1))
    if route.startswith("/en/beaches/"):
        slug = route.replace("/en/beaches/", "", 1)
        trans = {"around-nice/":"autour-de-nice/"}.get(slug, slug)
        return ("/plages/" + trans, route)
    if route.startswith("/plages/"):
        slug = route.replace("/plages/", "", 1)
        trans = {"autour-de-nice/":"around-nice/"}.get(slug, slug)
        return (route, "/en/beaches/" + trans)
    if route.startswith("/en/culture/"):
        return (route.replace("/en/culture/", "/culture/", 1), route)
    if route.startswith("/culture/"):
        return (route, route.replace("/culture/", "/en/culture/", 1))
    if route.startswith("/en/practical/"):
        return (route.replace("/en/practical/", "/pratique/", 1), route)
    if route.startswith("/pratique/"):
        return (route, route.replace("/pratique/", "/en/practical/", 1))
    # If no exact translation is declared, fall back to the matching section hub,
    # never to an unrelated page. Exact hreflang metadata always wins above.
    hub_pairs = (
        (("/en/explore/",), "/explore/", "/en/explore/"),
        (("/explore/",), "/explore/", "/en/explore/"),
        (("/en/hotels/",), "/hotels/", "/en/hotels/"),
        (("/hotels/", "/stay/", "/fr/dormir/"), "/hotels/", "/en/hotels/"),
        (("/en/restaurants/",), "/restaurants/", "/en/restaurants/"),
        (("/restaurants/",), "/restaurants/", "/en/restaurants/"),
        (("/en/beaches/",), "/plages/", "/en/beaches/"),
        (("/plages/",), "/plages/", "/en/beaches/"),
        (("/en/culture/",), "/culture/", "/en/culture/"),
        (("/culture/",), "/culture/", "/en/culture/"),
        (("/en/day-trips/",), "/escapades/", "/en/day-trips/"),
        (("/escapades/",), "/escapades/", "/en/day-trips/"),
        (("/en/good-finds/",), "/bons-plans/", "/en/good-finds/"),
        (("/bons-plans/",), "/bons-plans/", "/en/good-finds/"),
        (("/en/practical/",), "/pratique/", "/en/practical/"),
        (("/pratique/",), "/pratique/", "/en/practical/"),
        (("/plan/",), "/fr/planifier/", "/plan/"),
        (("/fr/planifier/",), "/fr/planifier/", "/plan/"),
    )
    for prefixes, fr_hub, en_hub in hub_pairs:
        if route.startswith(prefixes):
            return fr_hub, en_hub
    return ("/fr/", "/")

def language_links(text: str, route: str):
    alts = alternates(text)
    fr, en = inferred_pair(route)
    return alts.get("fr", fr), alts.get("en", en)

def active_index(route: str, lang: str):
    r = route.lower()
    if r in {"/", "/fr/", "/en/"}:
        return None
    if r.startswith(("/plan/", "/fr/planifier/", "/en/riviera-fit/", "/riviera-fit/", "/en/riviera-chooser/", "/riviera-chooser/")):
        return 0
    if "/riviera-guide/" in r:
        return 1
    if r.startswith(("/en/hotels/", "/hotels/", "/stay/", "/fr/dormir/")):
        return 2
    if r.startswith((
        "/en/explore/", "/explore/", "/en/restaurants/", "/restaurants/",
        "/en/beaches/", "/plages/", "/en/culture/", "/culture/",
        "/en/day-trips/", "/escapades/", "/en/gay-", "/cote-dazur-gay/",
        "/guide-gay-nice/", "/en/solo-", "/cote-dazur-femme-solo/",
        "/en/good-finds/", "/bons-plans/"
    )):
        return 3
    if r.startswith(("/en/practical/", "/pratique/")):
        return 4
    return None

def nav_html(items, active):
    links = []
    for i, (href, label) in enumerate(items):
        current = ' aria-current="page"' if active == i else ""
        links.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    return "<ul>" + "".join(links) + "</ul>"

def canonical_header(lang: str, route: str, fr_href: str, en_href: str):
    is_fr = lang == "fr"
    items = FR_NAV if is_fr else EN_NAV
    active = active_index(route, lang)
    nav = nav_html(items, active)
    brand_home = "/fr/" if is_fr else "/"
    aria = "Navigation principale" if is_fr else "Primary navigation"
    language_aria = "Langue" if is_fr else "Language"
    menu = "Menu"
    fr_current = ' aria-current="page"' if is_fr else ""
    en_current = ' aria-current="page"' if not is_fr else ""
    fr_class = " active" if is_fr else ""
    en_class = " active" if not is_fr else ""
    return (
        f'<header class="mametas-global-header" {MARK}>'
        '<div class="mametas-global-header-inner">'
        f'<a class="mametas-global-brand" href="{brand_home}" aria-label="Mametas">'
        '<span class="mametas-global-brand-name">Mametas</span>'
        '<span class="mametas-global-brand-line">They know the Riviera.</span></a>'
        f'<nav class="mametas-global-nav" aria-label="{aria}">{nav}</nav>'
        f'<div class="mametas-global-lang" aria-label="{language_aria}">'
        f'<a class="{"active" if is_fr else ""}" href="{html.escape(fr_href, quote=True)}"{fr_current}>FR</a>'
        '<span>/</span>'
        f'<a class="{"active" if not is_fr else ""}" href="{html.escape(en_href, quote=True)}"{en_current}>EN</a>'
        '</div>'
        '<details class="mametas-global-mobile">'
        f'<summary aria-label="{menu}"><span></span><span></span><span></span></summary>'
        '<div class="mametas-global-mobile-panel">'
        f'<nav aria-label="{aria}">{nav}</nav>'
        '<div class="mametas-global-mobile-lang">'
        f'<a class="{fr_class.strip()}" href="{html.escape(fr_href, quote=True)}"{fr_current}>FR</a><span>/</span>'
        f'<a class="{en_class.strip()}" href="{html.escape(en_href, quote=True)}"{en_current}>EN</a>'
        '</div></div></details>'
        '</div></header>'
    )

def canonical_footer(lang: str):
    is_fr = lang == "fr"
    items = FR_NAV if is_fr else EN_NAV
    nav = "".join(f'<a href="{href}">{label}</a>' for href, label in items)
    if is_fr:
        about = (
            '<a href="/a-propos/">À propos</a>'
            '<a href="/methode/">Méthode & Mametas Checked</a>'
            '<a href="/lexique/">Mini-lexique niçois</a>'
            '<a data-privacy-link="true" href="/fr/confidentialite/">Confidentialité & cookies</a>'
        )
        kicker = "Sélection éditoriale indépendante. Informations pratiques vérifiées."
    else:
        about = (
            '<a href="/en/about/">About</a>'
            '<a href="/en/method/">Method & Mametas Checked</a>'
            '<a href="/en/lexicon/">Niçois mini-lexicon</a>'
            '<a data-privacy-link="true" href="/privacy/">Privacy & cookies</a>'
        )
        kicker = "Independent editorial selection. Practical details checked."
    return (
        f'<footer class="mametas-global-footer" {MARK}>'
        '<div class="mametas-global-footer-inner">'
        '<div class="mametas-global-footer-brand"><span>Mametas</span>'
        '<p>They know the Riviera.</p></div>'
        '<div class="mametas-global-footer-col"><strong>' + ("Navigation" if is_fr else "Navigate") + '</strong>' + nav + '</div>'
        '<div class="mametas-global-footer-col"><strong>Mametas</strong>' + about + '</div>'
        '</div>'
        f'<div class="mametas-global-footer-bottom"><span>{kicker}</span><span>© 2026 Mametas</span></div>'
        '</footer>'
    )

def inject_css(text: str):
    text = re.sub(r'<link[^>]+href=["\']/assets/mametas-shell-v1\.css(?:\?v=[^"\']*)?["\'][^>]*>\s*', '', text, flags=re.I)
    link = f'<link rel="stylesheet" href="{SHELL_CSS}">'
    idx = text.lower().rfind("</head>")
    if idx < 0:
        return text
    return text[:idx] + link + "\n" + text[idx:]

def replace_shell(text: str, header: str, footer: str):
    body = re.search(r'<body\b[^>]*>', text, re.I)
    main = re.search(r'<main\b', text, re.I)
    if not body or not main or main.start() < body.end():
        return text, False

    prefix = text[body.end():main.start()]

    # Preserve real editorial content that old pages may have placed before
    # their header. The coherence pass removes the historical shell, not
    # arbitrary pre-main content.
    skip_pattern = r"<a\b[^>]*class=[\"'][^\"']*skip-link[^\"']*[\"'][^>]*>[\s\S]*?</a>\s*"
    skip = re.findall(skip_pattern, prefix, flags=re.I)
    prefix_without_skip = re.sub(skip_pattern, '', prefix, flags=re.I)
    legacy_header = re.search(r'<header\b', prefix_without_skip, re.I)
    preserved = prefix_without_skip[:legacy_header.start()] if legacy_header else prefix_without_skip
    preserved = preserved.strip()

    clean_prefix = "".join(skip) + header
    if preserved:
        clean_prefix += "\n" + preserved + "\n"
    text = text[:body.end()] + clean_prefix + text[main.start():]

    # Replace the historical footer. Validation below requires a single footer,
    # so legacy + canonical footers can never coexist silently.
    footer_matches = list(re.finditer(r'<footer\b[^>]*>[\s\S]*?</footer>', text, flags=re.I))
    if footer_matches:
        m = footer_matches[-1]
        text = text[:m.start()] + footer + text[m.end():]
    else:
        close_main = text.lower().rfind("</main>")
        if close_main >= 0:
            pos = close_main + len("</main>")
            text = text[:pos] + footer + text[pos:]
        else:
            body_close = text.lower().rfind("</body>")
            if body_close >= 0:
                text = text[:body_close] + footer + text[body_close:]
    return text, True

def page_lang(text: str, rel: str):
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)["\']', text, re.I)
    if m:
        return "fr" if m.group(1).lower().startswith("fr") else "en"
    return "en" if rel.startswith("en/") or rel.startswith("plan/") or rel.startswith("stay/") else "fr"

def public_html():
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP:
            continue
        yield p

def main():
    changed = []
    skipped = []
    for p in public_html():
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8", errors="ignore")
        before = text
        lang = page_lang(text, rel)
        route = rel_to_route(rel)
        fr_href, en_href = language_links(text, route)
        header = canonical_header(lang, route, fr_href, en_href)
        footer = canonical_footer(lang)
        text = inject_css(text)
        text, ok = replace_shell(text, header, footer)
        if not ok:
            skipped.append(rel)
            continue
        if text != before:
            p.write_text(text, encoding="utf-8")
            changed.append(rel)

    if skipped:
        raise SystemExit("Pages without a safe <body>/<main> shell: " + ", ".join(skipped[:20]))

    print(f"Mametas global shell normalized on {len(changed)} HTML files")
    for rel in changed[:120]:
        print("  ", rel)

if __name__ == "__main__":
    main()
