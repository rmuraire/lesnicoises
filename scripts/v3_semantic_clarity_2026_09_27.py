#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = []

def save(path: Path, text: str, original: str) -> None:
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

def patch_html() -> None:
    fr_replacements = [
        ("Choisir sa base", "Choisir son point de chute"),
        ("Choisissez la base.", "Choisissez votre point de chute."),
        ("Votre base décide", "Votre point de chute décide"),
        ("votre base décide", "votre point de chute décide"),
        ("notre meilleure base polyvalente", "notre meilleur point de chute polyvalent"),
        ("notre base par défaut", "notre point de chute par défaut"),
        ("la base polyvalente", "le point de chute polyvalent"),
        ("une base plus lente", "un point de chute plus lent"),
        ("une base plus douce", "un point de chute plus doux"),
        ("une base centrale", "un point de chute central"),
        ("une base rationnelle", "un point de chute rationnel"),
        ("une base intentionnelle", "un point de chute intentionnel"),
        ("cette base", "ce point de chute"),
        ("même base", "même point de chute"),
        ("votre base", "votre point de chute"),
        ("notre base", "notre point de chute"),
        ("comme base", "comme point de chute"),
        ("de la base", "du point de chute"),
        ("Au-delà de votre base", "Au-delà de votre point de chute"),
        ("quitter sa base", "quitter son point de chute"),
        ("quitter votre base", "quitter votre point de chute"),
        ("Comparer les bases", "Comparer les villes"),
        ("comparez les bases", "comparez les villes"),
        ("Voir toutes les bases", "Comparer toutes les villes"),
        ("bases à comparer", "villes à comparer"),
        ("Choisir une base", "Choisir un point de chute"),
        ("choisir une base", "choisir un point de chute"),
        ("une deuxième base", "un deuxième point de chute"),
        ("une vraie base", "un vrai point de chute"),
    ]

    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        original = text
        is_fr = bool(re.search(r'<html[^>]+lang="fr"', text, re.I))

        if is_fr:
            text = re.sub(r'<a([^>]*?)href="/fr/planifier/"([^>]*)>(?:Planifier|Plan|Préparer)</a>',
                          lambda m: f'<a{m.group(1)}href="/fr/planifier/"{m.group(2)}>Préparer</a>', text)
            text = re.sub(r'<a([^>]*?)href="/riviera-chooser/"([^>]*)>Planifier</a>',
                          lambda m: f'<a{m.group(1)}href="/fr/planifier/"{m.group(2)}>Préparer</a>', text)
            text = re.sub(r'<a([^>]*?)href="/riviera-guide/"([^>]*)>Lieux</a>',
                          lambda m: f'<a{m.group(1)}href="/riviera-guide/"{m.group(2)}>Destinations</a>', text)
            text = re.sub(r'<a([^>]*?)href="/bons-plans/"([^>]*)>Maintenant</a>',
                          lambda m: f'<a{m.group(1)}href="/pratique/"{m.group(2)}>Pratique</a>', text)
            text = text.replace("<h2>Planifier</h2>", "<h2>Préparer</h2>")
            text = text.replace("Right Now", "En ce moment")

            for old, new in fr_replacements:
                text = text.replace(old, new)

            text = text.replace("Faites fonctionner le voyage sans cagade",
                                "Faites fonctionner le voyage sans complications inutiles")
            text = text.replace("Arriver sans cagade", "Arriver sans accroc")
            text = text.replace("Dégun n’a besoin de ça.", "Personne n’a besoin de ça.")
            text = text.replace("Dégun n'a besoin de ça.", "Personne n'a besoin de ça.")
            text = text.replace(", gari.", ".").replace(", gari", "")
            text = re.sub(r'>Reality Check<', '>À savoir<', text, flags=re.I)
            text = re.sub(r'>Mobilité<', '>Déplacements<', text)
            text = re.sub(r'>Pression budget<', '>Budget<', text)
            text = re.sub(r'>Friction<', '>Logistique<', text)
            text = text.replace("Ce que cette base implique vraiment", "Ce que ce choix implique vraiment")
            text = text.replace("Ce que ce point de chute implique vraiment", "Ce que ce choix implique vraiment")
            text = re.sub(r'>(MÈFI|Mèfi)<',
                          r'><a class="dialect-inline" href="/lexique/#mefi">\1</a> — ATTENTION<', text)
        else:
            text = re.sub(r'<a([^>]*?)href="/en/good-finds/"([^>]*)>Now</a>',
                          lambda m: f'<a{m.group(1)}href="/en/practical/"{m.group(2)}>Practical</a>', text)
            text = text.replace("Make the trip work without the cagades",
                                "Make the trip work without avoidable mistakes")
            text = text.replace("Arrive without a cagade", "Arrive smoothly")
            text = text.replace(", gari.", ".").replace(", gari", "")
            text = re.sub(r'>Mobility<', '>Getting around<', text)
            text = re.sub(r'>Budget pressure<', '>Budget<', text)
            text = re.sub(r'>Friction<', '>Logistics<', text)
            text = text.replace("What this base really implies", "What this choice really implies")
            text = text.replace("What this choice really means", "What this choice really implies")
            text = re.sub(r'>(MÈFI|Mèfi)<',
                          r'><a class="dialect-inline" href="/en/lexicon/#mefi">\1</a> — WATCH OUT<', text)

        text = re.sub(r'>(pitchoun)<', '>Pichoun<', text, flags=re.I)

        if rel in ("en/riviera-fit/index.html","en/riviera-chooser/index.html","en/riviera-guide/index.html"):
            if "the town you’ll sleep in each night" not in text:
                note = '<p class="semantic-note"><strong>Base</strong> = the town you’ll sleep in each night. Choose the town before the hotel.</p>'
                text, n = re.subn(r'(<p class="(?:article-deck|lead)">.*?</p>)', r'\1'+note, text, count=1, flags=re.S)
                if not n:
                    text = text.replace("</header>", note+"</header>", 1)

        if rel in ("riviera-fit/index.html","riviera-chooser/index.html","riviera-guide/index.html"):
            if "c’est la ville où vous dormez chaque nuit" not in text:
                note = '<p class="semantic-note">Votre <strong>point de chute</strong>, c’est la ville où vous dormez chaque nuit. Choisissez la ville avant l’hôtel.</p>'
                text, n = re.subn(r'(<p class="(?:article-deck|lead)">.*?</p>)', r'\1'+note, text, count=1, flags=re.S)
                if not n:
                    text = text.replace("</header>", note+"</header>", 1)

        text = re.sub(r'/assets/site\.js(?:\?v=[^"]+)?', '/assets/site.js?v=1.2', text)
        text = re.sub(r'/assets/v3\.js(?:\?v=[^"]+)?', '/assets/v3.js?v=1.1', text)
        text = re.sub(r'/assets/riviera-chooser\.js(?:\?v=[^"]+)?', '/assets/riviera-chooser.js?v=12', text)
        save(path, text, original)

def validate() -> None:
    errors = []
    site = (ROOT/"assets/site.js").read_text(encoding="utf-8")
    v3 = (ROOT/"assets/v3.js").read_text(encoding="utf-8")
    chooser = (ROOT/"assets/riviera-chooser.js").read_text(encoding="utf-8")

    if "{label:'Préparer',href:'/fr/planifier/'}" not in site:
        errors.append("site.js French nav is not Préparer")
    if '{ label: "Préparer", href: "/fr/planifier/" }' not in v3:
        errors.append("v3.js French nav is not Préparer")
    for needle in ("reality:'À savoir'","mobility:'Déplacements'","budget:'Budget'","friction:'Logistique'",
                   "mobility:'Getting around'","friction:'Logistics'"):
        if needle not in chooser:
            errors.append(f"chooser missing {needle}")

    checks = {
        "fr/index.html": ("Préparer", "Destinations"),
        "riviera-guide/index.html": ("point de chute",),
        "en/riviera-guide/index.html": ("the town you’ll sleep in each night",),
        "riviera-fit/index.html": ("point de chute",),
        "en/riviera-fit/index.html": ("the town you’ll sleep in each night",),
    }
    for rel, needles in checks.items():
        p = ROOT/rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel} missing {needle}")

    if errors:
        raise SystemExit("Semantic clarity failed:\n- " + "\n- ".join(errors))
    print("Semantic clarity validation passed")

def main() -> int:
    patch_html()
    validate()
    print(f"Semantic clarity pass changed {len(changed)} HTML file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
