#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAIN_HUBS = (
    "index.html", "fr/index.html",
    "riviera-guide/index.html", "en/riviera-guide/index.html",
    "fr/dormir/nice/index.html", "stay/nice/index.html",
    "explore/index.html", "en/explore/index.html",
    "bons-plans/index.html", "en/good-finds/index.html",
)

FR_FOOTER = '''<footer class="v3-footer"><div class="wrap"><div class="footer-grid"><div class="footer-brand"><span class="v3-brand-name">Mametas</span><p>They know the Riviera. Les lieux sont réels. Les cinq matriarches sont fictives. Le point de vue, lui, est bien vivant.</p></div><div class="footer-col"><h2>Naviguer</h2><a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a><a href="/riviera-guide/">Lieux</a><a href="/fr/dormir/nice/">Dormir</a><a href="/explore/">Explorer</a><a href="/bons-plans/">Maintenant</a></div><div class="footer-col"><h2>Mametas</h2><a href="/a-propos/">À propos de Mametas</a><a href="/methode/">Méthode & Mametas Checked</a><a href="/lexique/">Petit lexique niçois</a><a href="/fr/confidentialite/">Confidentialité & cookies</a></div></div><div class="footer-bottom"><span>Sélection éditoriale indépendante. Certains liens peuvent être affiliés.</span><span>© 2026 Mametas</span></div></div></footer>'''

EN_FOOTER = '''<footer class="v3-footer"><div class="wrap"><div class="footer-grid"><div class="footer-brand"><span class="v3-brand-name">Mametas</span><p>They know the Riviera. The places are real. The five matriarchs are fictional. The point of view is very much alive.</p></div><div class="footer-col"><h2>Navigate</h2><a href="/plan/five-days-nice-no-car/">Plan</a><a href="/en/riviera-guide/">Places</a><a href="/stay/nice/">Stay</a><a href="/en/explore/">Explore</a><a href="/en/good-finds/">Now</a></div><div class="footer-col"><h2>Mametas</h2><a href="/en/about/">About Mametas</a><a href="/en/method/">Method & Mametas Checked</a><a href="/en/lexicon/">Niçois mini-lexicon</a><a href="/privacy/">Privacy & cookies</a></div></div><div class="footer-bottom"><span>Independent editorial selection. Some links may be affiliate links.</span><span>© 2026 Mametas</span></div></div></footer>'''

FR_ABOUT_MAIN = '''<main><section class="page-hero"><div class="wrap"><p class="eyebrow">À PROPOS DE MAMETAS</p><h1>La Riviera, avec une voix qui connaît le chemin.</h1><p class="lead">On connaît tous quelqu’un comme elles : une mère, une tante, une grand-mère qui sait où déjeuner, quelle route prendre et, surtout, où ne pas perdre son temps.</p></div></section><section class="section"><div class="wrap"><div class="about-story-grid"><div class="about-story-media"><img src="/assets/editorial/mametas-home-hero-2026-09-11.PNG" alt="Les cinq matriarches fictives de Mametas sur le bord de mer niçois" loading="eager"></div><div class="about-story-copy"><h2>Pourquoi Mametas existe</h2><p>La Côte d’Azur n’a pas besoin d’une liste de plus. Elle a besoin de quelqu’un qui tranche. Mametas est née de cette idée : garder la chaleur et la franchise d’une voix familière, puis faire le travail sérieux derrière — comparer, vérifier, choisir.</p><p>Les cinq femmes que vous voyez sont des personnages éditoriaux. Elles n’existent pas. Mais ce qu’elles incarnent, oui : la mémoire locale, l’affection pour ce coin de Méditerranée et une légère impatience devant les cagades évitables.</p></div></div><div class="about-portrait-row"><img src="/assets/editorial/about-mameta-2026-09-18.webp" alt="Portrait d’une des matriarches fictives de Mametas face à la Méditerranée" loading="lazy"><div class="about-portrait-copy"><span class="kicker">FICTIONAL LADIES. REAL WORK.</span><h2>Le personnage est inventé. La recommandation ne l’est pas.</h2><p>Les hôtels, restaurants, plages, musées et villages sont réels. On croise sources officielles, cartes, informations pratiques, menus et retours publics, puis on assume une opinion. Si une adresse n’a pas été visitée personnellement, on ne prétend pas le contraire.</p></div></div><p class="disclosure"><strong>Mametas Checked.</strong> Quand une information pratique a été vérifiée contre des sources identifiables, on le dit et on date la vérification. <a href="/methode/">Voir précisément ce que signifie le badge →</a></p><div class="verdict"><span class="label">LA PROMESSE MAMETAS</span><p>On ne veut pas vous faire tout voir. On veut vous aider à faire les bons choix — et vous laisser assez de temps pour vivre le reste.</p></div><div class="about-principles"><div class="about-principle"><strong>Documenter</strong><p>Les faits d’abord : accès, horaires, géographie, contraintes et ce qui peut réellement changer votre journée.</p></div><div class="about-principle"><strong>Choisir</strong><p>Pas cinquante options pour éviter de se tromper. Une sélection courte, avec le compromis quand il y en a un.</p></div><div class="about-principle"><strong>Rester libre</strong><p>Certains liens peuvent être affiliés. Ils financent Mametas ; ils ne décident jamais de ce que Mametas recommande.</p></div></div><p class="about-closing">Mametas aime la Riviera. Pas au point de lui pardonner tout. C’est probablement pour ça qu’on avait envie de faire ce guide.</p></div></section></main>'''

EN_ABOUT_MAIN = '''<main><section class="page-hero"><div class="wrap"><p class="eyebrow">ABOUT MAMETAS</p><h1>The Riviera, with a voice that knows the way.</h1><p class="lead">Most of us know someone like them: a mother, an aunt, a grandmother who knows where to eat, which road to take and, above all, where not to waste your time.</p></div></section><section class="section"><div class="wrap"><div class="about-story-grid"><div class="about-story-media"><img src="/assets/editorial/mametas-home-hero-2026-09-11.PNG" alt="The five fictional Mametas matriarchs on the Nice seafront" loading="eager"></div><div class="about-story-copy"><h2>Why Mametas exists</h2><p>The French Riviera does not need another endless list. It needs someone willing to make a call. Mametas started there: keep the warmth and candour of a familiar voice, then do the serious work behind it — compare, check, choose.</p><p>The five women you see are editorial characters. They are fictional. What they carry is not: local memory, affection for this stretch of the Mediterranean and a certain impatience with avoidable cagades.</p></div></div><div class="about-portrait-row"><img src="/assets/editorial/about-mameta-2026-09-18.webp" alt="Portrait of one of the fictional Mametas matriarchs by the Mediterranean" loading="lazy"><div class="about-portrait-copy"><span class="kicker">FICTIONAL LADIES. REAL WORK.</span><h2>The character is invented. The recommendation is not.</h2><p>The hotels, restaurants, beaches, museums and villages are real. We cross-check official sources, maps, practical information, menus and public feedback, then make a call. If somewhere has not been personally visited, we do not pretend otherwise.</p></div></div><p class="disclosure"><strong>Mametas Checked.</strong> When practical information has been checked against identifiable sources, we say so and date the check. <a href="/en/method/">Read exactly what the badge means →</a></p><div class="verdict"><span class="label">THE MAMETAS PROMISE</span><p>We are not here to make you see everything. We are here to help you make the right choices — and leave enough time to actually live the rest.</p></div><div class="about-principles"><div class="about-principle"><strong>Research</strong><p>Facts first: access, opening times, geography, constraints and the details that can genuinely change your day.</p></div><div class="about-principle"><strong>Choose</strong><p>Not fifty options to avoid being wrong. A short selection, with the compromise when there is one.</p></div><div class="about-principle"><strong>Stay independent</strong><p>Some links may be affiliate links. They help fund Mametas; they never decide what Mametas recommends.</p></div></div><p class="about-closing">Mametas loves the Riviera. Not enough to forgive it everything. That is probably why we wanted to make this guide.</p></div></section></main>'''

FR_HOME_ABOUT = '''<section class="about-home-strip" data-about-home="true"><div class="wrap"><div><p class="eyebrow">Derrière Mametas</p><h2>Qui sont ces dames ?</h2></div><div><p>Cinq matriarches fictives, une affection très réelle pour la Riviera et une idée simple : un guide peut être documenté sans perdre sa voix.</p><a href="/a-propos/">À propos de Mametas →</a></div></div></section>'''
EN_HOME_ABOUT = '''<section class="about-home-strip" data-about-home="true"><div class="wrap"><div><p class="eyebrow">Behind Mametas</p><h2>Who are these ladies?</h2></div><div><p>Five fictional matriarchs, a very real affection for the Riviera and one simple idea: a guide can be carefully researched without losing its voice.</p><a href="/en/about/">About Mametas →</a></div></div></section>'''

def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")

def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")

def replace_footer(text: str, footer: str) -> str:
    text = re.sub(r'<footer class="(?:v3-footer|site-footer)">.*?</footer>', footer, text, count=1, flags=re.S)
    return text

def fix_home(rel: str, fr: bool) -> None:
    text = read(rel)
    if fr:
        swaps = {
            '<li><a href="#planifier">Planifier</a></li>':'<li><a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a></li>',
            '<li><a href="#lieux">Lieux</a></li>':'<li><a href="/riviera-guide/">Lieux</a></li>',
            '<li><a href="#hotels">Dormir</a></li>':'<li><a href="/fr/dormir/nice/">Dormir</a></li>',
            '<li><a href="#maintenant">Maintenant</a></li>':'<li><a href="/bons-plans/">Maintenant</a></li>',
        }
        strip = FR_HOME_ABOUT
        footer = FR_FOOTER
    else:
        swaps = {
            '<li><a href="#plan">Plan</a></li>':'<li><a href="/plan/five-days-nice-no-car/">Plan</a></li>',
            '<li><a href="#places">Places</a></li>':'<li><a href="/en/riviera-guide/">Places</a></li>',
            '<li><a href="#stay">Stay</a></li>':'<li><a href="/stay/nice/">Stay</a></li>',
            '<li><a href="#now">Now</a></li>':'<li><a href="/en/good-finds/">Now</a></li>',
        }
        strip = EN_HOME_ABOUT
        footer = EN_FOOTER
    for old,new in swaps.items():
        text = text.replace(old,new)
    if 'data-about-home="true"' not in text:
        text = text.replace('</main>', strip + '</main>', 1)
    text = replace_footer(text, footer)
    write(rel, text)

def fix_now(rel: str, fr: bool) -> None:
    text = read(rel)
    if fr:
        text = text.replace('<p class="eyebrow">BONS PLANS</p><h1>Les choses qu’on aurait aimé vous dire avant</h1>', '<p class="eyebrow">MAINTENANT</p><h1>La Riviera maintenant : ce qu’il vaut mieux savoir</h1>')
        text = text.replace('<a class="card" href="/bons-plans/septembre-2026/">', '<a class="card seasonal-card" href="/bons-plans/septembre-2026/">', 1)
        text = replace_footer(text, FR_FOOTER)
    else:
        text = text.replace('<p class="eyebrow">GOOD FINDS</p><h1>Things worth knowing before you arrive</h1>', '<p class="eyebrow">NOW</p><h1>The Riviera now: what is worth knowing</h1>')
        text = text.replace('<a class="card" href="/en/good-finds/september-2026/">', '<a class="card seasonal-card" href="/en/good-finds/september-2026/">', 1)
        text = replace_footer(text, EN_FOOTER)
    write(rel, text)

def fix_about(rel: str, fr: bool) -> None:
    text = read(rel)
    text = re.sub(r'<main>.*?</main>', FR_ABOUT_MAIN if fr else EN_ABOUT_MAIN, text, count=1, flags=re.S)
    if fr:
        text = re.sub(r'<title>.*?</title>', '<title>À propos de Mametas | Le guide indépendant de la Côte d’Azur</title>', text, count=1, flags=re.S)
        text = replace_footer(text, FR_FOOTER)
    else:
        text = re.sub(r'<title>.*?</title>', '<title>About Mametas | Independent French Riviera guide</title>', text, count=1, flags=re.S)
        text = replace_footer(text, EN_FOOTER)
    write(rel, text)

def standardize_main_footers() -> None:
    for rel in MAIN_HUBS:
        text = read(rel)
        fr = '<html lang="fr"' in text or '<html lang="fr"' in text.lower()
        text = replace_footer(text, FR_FOOTER if fr else EN_FOOTER)
        write(rel, text)

def validate() -> None:
    errors = []
    en_home = read("index.html")
    fr_home = read("fr/index.html")
    for marker in ('href="/plan/five-days-nice-no-car/">Plan</a>', 'href="/en/riviera-guide/">Places</a>', 'href="/stay/nice/">Stay</a>', 'href="/en/good-finds/">Now</a>'):
        if marker not in en_home: errors.append("EN home nav missing " + marker)
    for marker in ('href="/fr/planifier/cinq-jours-nice-sans-voiture/">Planifier</a>', 'href="/riviera-guide/">Lieux</a>', 'href="/fr/dormir/nice/">Dormir</a>', 'href="/bons-plans/">Maintenant</a>'):
        if marker not in fr_home: errors.append("FR home nav missing " + marker)
    if 'seasonal-card' not in read("en/good-finds/index.html") or 'seasonal-card' not in read("bons-plans/index.html"):
        errors.append("NOW seasonal card distinction missing")
    for rel in ("stay/nice/index.html","fr/dormir/nice/index.html","en/riviera-guide/index.html","riviera-guide/index.html"):
        text = read(rel)
        if 'About Mametas' not in text and 'À propos de Mametas' not in text:
            errors.append(rel + ": standard About footer link missing")
        if 'About the project' in text:
            errors.append(rel + ": stale About the project label")
    for rel in ("en/about/index.html","a-propos/index.html"):
        text = read(rel)
        if '/assets/editorial/about-mameta-2026-09-18.webp' not in text:
            errors.append(rel + ": new Mameta portrait missing")
    if errors:
        raise SystemExit("Final recipe polish failed:\n- " + "\n- ".join(errors))
    print("Final recipe polish passed: homepage navigation, NOW hierarchy, standard hub footers and About Mametas are coherent.")

def main() -> int:
    fix_home("index.html", False)
    fix_home("fr/index.html", True)
    fix_now("en/good-finds/index.html", False)
    fix_now("bons-plans/index.html", True)
    fix_about("en/about/index.html", False)
    fix_about("a-propos/index.html", True)
    standardize_main_footers()
    validate()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
