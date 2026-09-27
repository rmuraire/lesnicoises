#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = []

def save(path: Path, text: str, original: str) -> None:
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

def visible_text(html_text: str) -> str:
    text = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', ' ', html_text, flags=re.I)
    text = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', ' ', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', html.unescape(text)).strip()

def rewrite_visible(html_text: str, lang: str, preserve_dialect: bool = False) -> str:
    parts = re.split(r'(<[^>]+>)', html_text)
    out = []
    in_script = False
    in_style = False
    in_anchor = False

    structural_fr = [
        ("Cinq questions. Une base.", "Cinq questions. Un point de chute."),
        ("UNE BASE RECOMMANDÉE", "UN POINT DE CHUTE RECOMMANDÉ"),
        ("Une base recommandée", "Un point de chute recommandé"),
        ("Choisir la base", "Choisir le point de chute"),
        ("Choisir sa base", "Choisir son point de chute"),
        ("Choisissez la bonne base", "Choisissez le bon point de chute"),
        ("Choisissez votre base", "Choisissez votre point de chute"),
        ("Base choisie ?", "Point de chute choisi ?"),
        ("BASE INTENTIONNELLE", "POINT DE CHUTE INTENTIONNEL"),
        ("Meilleure première base", "Meilleur premier point de chute"),
        ("meilleure première base", "meilleur premier point de chute"),
        ("notre meilleure base polyvalente", "notre meilleur point de chute polyvalent"),
        ("notre base par défaut", "notre point de chute par défaut"),
        ("la base polyvalente", "le point de chute polyvalent"),
        ("Base calme à l’est", "Ville calme à l’est"),
        ("Cinq jours, base Nice", "Cinq jours, Nice comme point de chute"),
        ("Dans quelle base dormez-vous ?", "Dans quelle ville dormez-vous ?"),
        ("PAR BASE", "PAR VILLE"),
        ("COMPRENDRE LA BASE", "COMPRENDRE LA VILLE"),
        ("COMMENT LES BASES DIFFÈRENT", "COMMENT LES VILLES DIFFÈRENT"),
        ("LA BASE TIENT TOUJOURS ?", "LA VILLE VOUS CONVIENT TOUJOURS ?"),
        ("Au-delà de votre base", "Au-delà de votre ville"),
        ("AU-DELÀ DE LA BASE", "AU-DELÀ DE LA VILLE"),
        ("Pourquoi cette base", "Pourquoi cette ville"),
        ("Pourquoi pas les autres bases", "Pourquoi pas les autres villes"),
        ("Voir le guide de la base", "Voir le guide de cette ville"),
        ("Trois niveaux. Même base.", "Trois niveaux. Même ville."),
        ("Une fois la base choisie", "Une fois la ville choisie"),
        ("La base est décidée ?", "La ville est décidée ?"),
        ("La base change", "La ville change"),
    ]

    def replace_word_case(text: str, pattern: str, lower: str, title: str, upper: str) -> str:
        def repl(m):
            s = m.group(0)
            if s.isupper():
                return upper
            if s[:1].isupper():
                return title
            return lower
        return re.sub(pattern, repl, text, flags=re.I)

    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if re.match(r'<script\b', low):
                in_script = True
            elif re.match(r'</script\b', low):
                in_script = False
            elif re.match(r'<style\b', low):
                in_style = True
            elif re.match(r'</style\b', low):
                in_style = False
            elif re.match(r'<a\b', low):
                in_anchor = True
            elif re.match(r'</a\b', low):
                in_anchor = False
            out.append(part)
            continue

        if in_script or in_style:
            out.append(part)
            continue

        text = part
        if lang == "fr":
            for old, new in structural_fr:
                text = text.replace(old, new)

            # Standardise the four decision criteria wherever they appear as visible copy.
            text = text.replace("Reality Check", "À savoir")
            text = text.replace("Pression budget", "Budget")
            text = text.replace("Friction", "Logistique")

            # Natural prose: once the canonical concept has been introduced as
            # "point de chute", ordinary sentences simply say ville/villes.
            text = re.sub(r'\bbase\s+Nice\b', 'Nice comme point de chute', text, flags=re.I)
            text = re.sub(r'\bbase\s+Cannes\b', 'Cannes comme point de chute', text, flags=re.I)
            text = re.sub(r'\bbase\s+Antibes\b', 'Antibes comme point de chute', text, flags=re.I)
            text = re.sub(r'\bbase\s+Menton\b', 'Menton comme point de chute', text, flags=re.I)
            text = re.sub(r'\bbase\s+Monaco\b', 'Monaco comme point de chute', text, flags=re.I)
            text = replace_word_case(text, r'\bbases\b', 'villes', 'Villes', 'VILLES')
            text = replace_word_case(text, r'\bbase\b', 'ville', 'Ville', 'VILLE')

            # Dialect never carries functional meaning outside the lexicon.
            if not preserve_dialect:
                text = re.sub(r'\bcagades?\b', lambda m: 'erreurs' if m.group(0).lower().endswith('s') else 'erreur', text, flags=re.I)
                text = re.sub(r'\bDégun\b', 'Personne', text, flags=re.I)
                text = re.sub(r'\bGari\b', '', text, flags=re.I)
            text = re.sub(r'\bpitchoun\b', 'Pichoun', text, flags=re.I)

            if not in_anchor:
                text = re.sub(
                    r'\bPichoun\b',
                    '<a class="dialect-inline" href="/lexique/#pichoun" title="Petit lexique niçois">Pichoun</a>',
                    text
                )
                text = re.sub(
                    r'\bMèfi\b(?!\s*[—-])',
                    '<a class="dialect-inline" href="/lexique/#mefi">Mèfi</a> — attention',
                    text,
                    flags=re.I
                )
        else:
            if not preserve_dialect:
                text = re.sub(r'\bcagades?\b', lambda m: 'mistakes' if m.group(0).lower().endswith('s') else 'mistake', text, flags=re.I)
                text = re.sub(r'\bGari\b', '', text, flags=re.I)
            text = re.sub(r'\bpitchoun\b', 'Pichoun', text, flags=re.I)
            if not in_anchor:
                text = re.sub(
                    r'\bPichoun\b',
                    '<a class="dialect-inline" href="/en/lexicon/#pichoun">Pichoun</a>',
                    text
                )
                text = re.sub(
                    r'\bMèfi\b(?!\s*[—-])',
                    '<a class="dialect-inline" href="/en/lexicon/#mefi">Mèfi</a> — watch out',
                    text,
                    flags=re.I
                )

        out.append(text)

    return "".join(out)

def patch_html() -> None:
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
            text = re.sub(r'>Reality Check<', '>À savoir<', text, flags=re.I)
            text = re.sub(r'>Mobilité<', '>Déplacements<', text)
            text = re.sub(r'>Pression budget<', '>Budget<', text)
            text = re.sub(r'>Friction<', '>Logistique<', text)
            text = text.replace("Ce que cette base implique vraiment", "Ce que ce choix implique vraiment")
            text = text.replace("Ce que ce point de chute implique vraiment", "Ce que ce choix implique vraiment")
        else:
            text = re.sub(r'<a([^>]*?)href="/en/good-finds/"([^>]*)>Now</a>',
                          lambda m: f'<a{m.group(1)}href="/en/practical/"{m.group(2)}>Practical</a>', text)
            text = re.sub(r'>Mobility<', '>Getting around<', text)
            text = re.sub(r'>Budget pressure<', '>Budget<', text)
            text = re.sub(r'>Friction<', '>Logistics<', text)
            text = text.replace("What this base really implies", "What this choice really implies")
            text = text.replace("What this choice really means", "What this choice really implies")

        text = rewrite_visible(
            text,
            "fr" if is_fr else "en",
            preserve_dialect=rel in ("lexique/index.html", "en/lexicon/index.html")
        )

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

        text = re.sub(r'/assets/site\.js(?:\?v=[^"]+)?', '/assets/site.js?v=1.3', text)
        text = re.sub(r'/assets/v3\.js(?:\?v=[^"]+)?', '/assets/v3.js?v=1.2', text)
        text = re.sub(r'/assets/riviera-chooser\.js(?:\?v=[^"]+)?', '/assets/riviera-chooser.js?v=13', text)
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

    # Exhaustive visible-text guard: French pages must no longer require the
    # visitor to understand "base", nor legacy dialect beyond Pichoun / Mèfi.
    for path in ROOT.rglob("*.html"):
        raw = path.read_text(encoding="utf-8")
        is_fr = bool(re.search(r'<html[^>]+lang="fr"', raw, re.I))
        vis = visible_text(raw)
        rel = path.relative_to(ROOT).as_posix()
        if is_fr:
            preserve_dialect = rel == "lexique/index.html"
            for pattern, label in (
                (r'\bbases?\b', "base/bases"),
                (r'\bDégun\b', "Dégun"),
                (r'\bGari\b', "Gari"),
                (r'\bcagades?\b', "cagade"),
            ):
                if preserve_dialect and label in ("Dégun", "Gari", "cagade"):
                    continue
                m = re.search(pattern, vis, re.I)
                if m:
                    context = vis[max(0,m.start()-80):m.end()+120]
                    errors.append(f"{rel}: visible {label}: {context}")
            for raw_pattern, label in (
                (r'>\s*Reality Check\s*<', "Reality Check FR"),
                (r'>\s*Pression budget\s*<', "Pression budget"),
                (r'>\s*Friction\s*<', "Friction label"),
            ):
                if re.search(raw_pattern, raw, re.I):
                    errors.append(f"{rel}: legacy label {label}")
        else:
            if rel == "en/lexicon/index.html":
                continue
            for pattern, label in ((r'\bGari\b',"Gari"),(r'\bcagades?\b',"cagade")):
                m = re.search(pattern, vis, re.I)
                if m:
                    context = vis[max(0,m.start()-80):m.end()+120]
                    errors.append(f"{rel}: visible EN {label}: {context}")

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
        raise SystemExit("Semantic clarity failed:\n- " + "\n- ".join(errors[:80]))
    print("Semantic clarity validation passed: all FR visible base/bases and legacy dialect residues removed")

def main() -> int:
    patch_html()
    validate()
    print(f"Semantic clarity pass changed {len(changed)} HTML file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
