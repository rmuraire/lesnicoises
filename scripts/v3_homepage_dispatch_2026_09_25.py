#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []


def save(rel: str, text: str, original: str | None = None) -> None:
    p = ROOT / rel
    if original is None:
        original = p.read_text(encoding="utf-8") if p.exists() else ""
    if text != original:
        p.write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)


def replace_section_by_heading(text: str, heading: str, replacement: str) -> tuple[str, bool]:
    for m in re.finditer(r'<section\b[^>]*>.*?</section>', text, flags=re.S):
        block = m.group(0)
        if heading in block:
            return text[:m.start()] + replacement + text[m.end():], True
    return text, False


def extract_lgbtq_banner(text: str) -> str:
    m = re.search(r'<div class="wrap home-lgbtq-wrap">.*?</div></section>', text, flags=re.S)
    if not m:
        return ""
    block = m.group(0)
    block = block[:-len("</section>")]
    return block


def strip_lgbtq_banner(text: str) -> str:
    return re.sub(r'<div class="wrap home-lgbtq-wrap">.*?</div>(?=</section>)', '', text, count=1, flags=re.S)


def home_experiences(lang: str) -> str:
    if lang == "fr":
        items = [
            ("/riviera-guide/nice/", "/assets/editorial/depositphotos/nice-pratique/nice-castle-hill-bay.webp", "PREMIER MATIN", "Vieux-Nice + Colline du Château", "Commencez par la ville avant de chercher à lui échapper."),
            ("/riviera-guide/villefranche-cap-ferrat/", "/assets/editorial/villefranche.jpg", "BAIGNADE", "Villefranche avant midi", "Une rade spectaculaire, une vraie plage, et Nice à cinq minutes de train."),
            ("/escapades/iles-de-lerins/", "/assets/editorial/iles-lerins.jpg", "SORTIR DE CANNES", "Les îles de Lérins", "Quand vous voulez changer d’ambiance, pas seulement de code postal."),
            ("/culture/fondation-maeght/", "/assets/editorial/fondation-maeght-waterborough.webp", "ART", "Fondation Maeght", "L’une des meilleures raisons de quitter le littoral."),
            ("/culture/musee-picasso-antibes/", "/assets/editorial/culture-musee-picasso-antibes-v2.webp", "CULTURE", "Picasso à Antibes", "Un musée qui fonctionne particulièrement bien avec la vieille ville autour."),
            ("/escapades/cap-ferrat-a-pied/", "/assets/editorial/cap-ferrat-aerial.jpg", "MARCHER", "Cap-Ferrat à pied", "Une promenade, une baignade, peut-être un jardin. Pas six cases à cocher."),
            ("/restaurants/nice/", "/assets/editorial/mametas-explore-restaurants-salad.webp", "MANGER", "Déjeuner niçois", "Socca, petits farcis, salade niçoise : une cuisine, pas un décor de terrasse."),
            ("/riviera-guide/menton/", "/assets/editorial/menton-day.jpg", "PLUS LENT", "Menton", "Couleur, jardins et une Riviera qui commence à parler italien."),
            ("/riviera-guide/saint-paul-de-vence/", "/assets/editorial/saint-paul-de-vence.jpg", "DANS LES TERRES", "Saint-Paul-de-Vence", "Pierre, art et une vraie rupture avec le rythme côtier."),
            ("/culture/musee-oceanographique-monaco/", "/assets/editorial/monaco-harbour.jpg", "MONACO", "Musée océanographique", "Le bon antidote au Monaco réduit aux voitures, yachts et vitrines."),
        ]
        eyebrow = "10 EXPÉRIENCES"
        title = "Dix raisons de lever les yeux du planning."
        desc = "Ce ne sont pas dix obligations. Ce sont dix expériences qui changent vraiment la journée. Ouvrez celle qui vous ressemble et laissez le reste tranquille."
        cta = "Tout Explorer →"
        explore = "/explore/"
    else:
        items = [
            ("/en/riviera-guide/nice/", "/assets/editorial/depositphotos/nice-pratique/nice-castle-hill-bay.webp", "FIRST MORNING", "Old Nice + Castle Hill", "Learn the city before trying to escape it."),
            ("/en/riviera-guide/villefranche-cap-ferrat/", "/assets/editorial/villefranche.jpg", "SWIM", "Villefranche before lunch", "A spectacular bay, a real beach and Nice five train minutes away."),
            ("/en/day-trips/iles-de-lerins/", "/assets/editorial/iles-lerins.jpg", "LEAVE CANNES", "Lérins Islands", "For when you want to change the mood, not just the postcode."),
            ("/en/culture/fondation-maeght/", "/assets/editorial/fondation-maeght-waterborough.webp", "ART", "Fondation Maeght", "One of the best reasons to leave the coast."),
            ("/en/culture/picasso-museum-antibes/", "/assets/editorial/culture-musee-picasso-antibes-v2.webp", "CULTURE", "Picasso in Antibes", "A museum that works especially well with the old town around it."),
            ("/en/day-trips/cap-ferrat-a-pied/", "/assets/editorial/cap-ferrat-aerial.jpg", "WALK", "Cap-Ferrat on foot", "One walk, one swim, perhaps a garden. Not six boxes to tick."),
            ("/en/restaurants/nice/", "/assets/editorial/mametas-explore-restaurants-salad.webp", "EAT", "A Niçois lunch", "Socca, petits farcis, salade niçoise: a cuisine, not a terrace backdrop."),
            ("/en/riviera-guide/menton/", "/assets/editorial/menton-day.jpg", "SLOWER", "Menton", "Colour, gardens and a Riviera beginning to speak Italian."),
            ("/en/riviera-guide/saint-paul-de-vence/", "/assets/editorial/saint-paul-de-vence.jpg", "INLAND", "Saint-Paul-de-Vence", "Stone, art and a real break from the coastal rhythm."),
            ("/en/culture/oceanographic-museum-monaco/", "/assets/editorial/monaco-harbour.jpg", "MONACO", "Oceanographic Museum", "The useful antidote to Monaco reduced to cars, yachts and shop windows."),
        ]
        eyebrow = "10 EXPERIENCES"
        title = "Ten reasons to look up from the itinerary."
        desc = "These are not ten obligations. They are ten experiences that can genuinely change the day. Open the one that fits and leave the rest alone."
        cta = "Open Explore →"
        explore = "/en/explore/"
    cards = "".join(
        f'<a class="home-experience-card" href="{href}"><img src="{img}" alt="{title_item}" loading="lazy" decoding="async"><span class="home-experience-copy"><small>{tag}</small><strong>{title_item}</strong><em>{copy}</em></span></a>'
        for href, img, tag, title_item, copy in items
    )
    return f'''<section class="v3-section home-experiences" id="explore"><div class="wrap"><div class="section-heading home-experiences-heading"><div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div><p>{desc}</p></div><div class="home-experience-grid">{cards}</div><div class="home-section-tail"><a class="button secondary" href="{explore}">{cta}</a></div></div></section>'''


def right_now_section(lang: str) -> str:
    if lang == "fr":
        return '''<section class="v3-section home-now-teaser" id="maintenant"><div class="wrap home-now-inner"><div><p class="eyebrow">EN CE MOMENT</p><h2>La Riviera bouge. Le guide doit suivre.</h2><p>Affluence, gros événements, fermetures et notes saisonnières qui peuvent réellement modifier votre séjour. Une couche courte, datée, séparée du contenu pratique permanent.</p></div><a class="home-now-card" href="/bons-plans/"><time datetime="2026-09">SEPTEMBRE 2026</time><strong>Voir ce qui mérite votre attention maintenant</strong><span>Ouvrir Right Now →</span></a></div></section>'''
    return '''<section class="v3-section home-now-teaser" id="now"><div class="wrap home-now-inner"><div><p class="eyebrow">RIGHT NOW</p><h2>The Riviera moves. The guide should too.</h2><p>Crowd pressure, major events, closures and seasonal notes that can genuinely change your trip. A short dated layer, kept separate from evergreen practical guidance.</p></div><a class="home-now-card" href="/en/good-finds/"><time datetime="2026-09">SEPTEMBER 2026</time><strong>See what deserves your attention now</strong><span>Open Right Now →</span></a></div></section>'''


def credibility_strip(lang: str) -> str:
    if lang == "fr":
        return '''<section class="home-credibility-strip"><div class="wrap"><div><p class="eyebrow">MAMETAS CHECKED</p><h2>Une voix, une méthode, un éditeur identifiable.</h2></div><div><p>Mametas est créé et édité par Renaud Muraire, Niçois. Les cinq Mametas sont des personnages éditoriaux fictifs ; les recommandations, sources et compromis sont documentés pour de vrai.</p><p class="home-credibility-links"><a href="/methode/">Méthode</a><a href="/corrections/">Corrections</a><a href="/presse/">Presse & professionnels</a><a href="/a-propos/">À propos</a></p></div></div></section>'''
    return '''<section class="home-credibility-strip"><div class="wrap"><div><p class="eyebrow">MAMETAS CHECKED</p><h2>One voice, one method, one identifiable editor.</h2></div><div><p>Mametas is created and edited by Renaud Muraire, a Niçois. The five Mametas are fictional editorial characters; the recommendations, sources and trade-offs are documented for real.</p><p class="home-credibility-links"><a href="/en/method/">Method</a><a href="/en/corrections/">Corrections</a><a href="/en/press/">Press & professionals</a><a href="/en/about/">About</a></p></div></div></section>'''


def patch_home(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = text.replace("<body>", '<body class="home-page">', 1)

    # Hero: product route and manual route are two equal entry doors.
    if lang == "fr":
        text = re.sub(
            r'<div class="hero-actions">.*?</div>',
            '<div class="hero-actions"><a class="button" href="/riviera-fit/">Tester Riviera Fit</a><a class="button secondary" href="/riviera-guide/">Choisir sa base</a></div>',
            text, count=1, flags=re.S
        )
    else:
        text = re.sub(
            r'<div class="hero-actions">.*?</div>',
            '<div class="hero-actions"><a class="button" href="/en/riviera-fit/">Try Riviera Fit</a><a class="button secondary" href="/en/riviera-guide/">Choose your base</a></div>',
            text, count=1, flags=re.S
        )

    # Riviera Fit remains the only product staged strongly on the homepage.
    if lang == "fr":
        text = text.replace('<p class="eyebrow">MAMETAS RIVIERA FIT · LA RECO</p>', '<p class="tool-badge">MAMETAS TOOL</p><p class="eyebrow">RIVIERA FIT · LA RECO</p>')
        text = text.replace('href="/riviera-chooser/"', 'href="/riviera-fit/"')
    else:
        text = text.replace('<p class="eyebrow">MAMETAS RIVIERA FIT · THE CALL</p>', '<p class="tool-badge">MAMETAS TOOL</p><p class="eyebrow">RIVIERA FIT · THE CALL</p>')
        text = text.replace('href="/en/riviera-chooser/"', 'href="/en/riviera-fit/"')

    # Places preview: keep four bases, add one explicit route to the full hub.
    lgbtq = extract_lgbtq_banner(text)
    text = strip_lgbtq_banner(text)
    places_heading = "Même côte. Pas le même séjour." if lang == "fr" else "Same coast. Different trip."
    for m in list(re.finditer(r'<section\b[^>]*>.*?</section>', text, flags=re.S)):
        block = m.group(0)
        if places_heading in block:
            if 'home-section-tail' not in block:
                cta = '<div class="wrap home-section-tail"><a class="button secondary" href="/riviera-guide/">Voir toutes les destinations →</a></div>' if lang == "fr" else '<div class="wrap home-section-tail"><a class="button secondary" href="/en/riviera-guide/">See all Places →</a></div>'
                block = block[:-len("</section>")] + cta + "</section>"
            text = text[:m.start()] + block + text[m.end():]
            break

    # Remove the second destination catalogue; it made the home substitute for Places.
    old_heading = "Ne collectionnez pas la Riviera. Choisissez-la." if lang == "fr" else "Do not collect the Riviera. Choose it."
    text, _ = replace_section_by_heading(text, old_heading, "")

    # Stay is a showcase, not a second product launch.
    if lang == "fr":
        text = text.replace('href="/hotels/finder/?base=nice">Trouver mon hôtel avec Hotel Fit</a>', 'href="/hotels/">Explorer Dormir</a>')
        text = text.replace('href="/fr/dormir/nice/">Voir toute la sélection Nice</a>', 'href="/hotels/">Voir les hôtels par base</a>')
    else:
        text = text.replace('href="/en/hotels/finder/?base=nice">Find my hotel with Hotel Fit</a>', 'href="/en/hotels/">Explore Stay</a>')
        text = text.replace('href="/stay/nice/">See the full Nice selection</a>', 'href="/en/hotels/">Browse hotels by base</a>')

    # Right Now is one temporal teaser, not three repeated cards pointing to the same page.
    now_heading = "La Riviera n’attend pas votre réservation." if lang == "fr" else "The Riviera does not stay still for your booking."
    text, ok = replace_section_by_heading(text, now_heading, right_now_section(lang))
    if not ok:
        # Accept a previous phase-3 wording if the source has already moved.
        alt = "Ce qui change maintenant sur la Riviera." if lang == "fr" else "What is changing on the Riviera now."
        text, _ = replace_section_by_heading(text, alt, right_now_section(lang))

    # Explore becomes the homepage-only 10 Experiences edit.
    explore_heading = "Ou simplement explorer." if lang == "fr" else "Or just explore."
    text, ok = replace_section_by_heading(text, explore_heading, home_experiences(lang))
    if not ok:
        raise RuntimeError(f"{rel}: Explore homepage section not found")

    # Keep LGBTQ+ visible, but outside the Places taxonomy.
    if lgbtq:
        marker = home_experiences(lang)
        pos = text.find(marker)
        if pos >= 0:
            end = pos + len(marker)
            text = text[:end] + f'<section class="home-lgbtq-section">{lgbtq}</section>' + text[end:]

    # Institutional proof closes the shop window.
    if "home-credibility-strip" not in text:
        insert_at = text.rfind("</main>")
        if insert_at >= 0:
            text = text[:insert_at] + credibility_strip(lang) + text[insert_at:]

    save(rel, text, original)


def css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 homepage dispatch 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 homepage dispatch 2026-09-25 */
.home-page .chooser-signature-section--fit{padding:clamp(48px,5vw,68px) 0}
.home-page .riviera-fit-home-copy h2{font-size:clamp(40px,4.4vw,60px)}
.home-page .stay-card{min-height:176px}
.home-page .stay-card img{max-height:210px}
.home-page .stay-card-copy{padding:19px 21px}
.home-page .stay-card h3{font-size:25px}
.home-page .stay-card p{font-size:12px}
.home-section-tail{margin-top:26px}
.home-now-teaser{background:var(--paper-deep);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.home-now-inner{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.72fr);gap:clamp(28px,6vw,80px);align-items:center}
.home-now-inner h2{max-width:12ch;margin:6px 0 12px;font-family:var(--serif);font-size:clamp(34px,4.5vw,54px);font-weight:500;letter-spacing:-.04em;line-height:1}
.home-now-inner>div>p:not(.eyebrow){max-width:680px;margin:0;color:var(--ink-soft);font-size:13px;line-height:1.65}
.home-now-card{display:flex;min-height:190px;padding:24px;flex-direction:column;border:1px solid var(--line);background:rgba(255,255,255,.42);text-decoration:none}
.home-now-card time{color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.13em}
.home-now-card strong{max-width:15ch;margin:28px 0 18px;font-family:var(--serif);font-size:28px;font-weight:500;line-height:1.05}
.home-now-card span{margin-top:auto;font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.home-experiences{padding-top:clamp(58px,7vw,88px);padding-bottom:clamp(58px,7vw,88px)}
.home-experiences-heading{margin-bottom:28px}
.home-experience-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.home-experience-card{display:block;overflow:hidden;border:1px solid var(--line);background:rgba(255,255,255,.24);text-decoration:none;transition:transform .18s ease,background .18s ease}
.home-experience-card:hover,.home-experience-card:focus-visible{transform:translateY(-2px);background:var(--white)}
.home-experience-card img{display:block;width:100%;height:118px;object-fit:cover}
.home-experience-copy{display:block;padding:14px 14px 16px}
.home-experience-copy small{display:block;margin-bottom:5px;color:var(--coral);font-size:8px;font-weight:800;letter-spacing:.11em}
.home-experience-copy strong{display:block;font-family:var(--serif);font-size:20px;font-weight:500;line-height:1.05}
.home-experience-copy em{display:block;margin-top:7px;color:var(--ink-soft);font-size:10px;font-style:normal;line-height:1.45}
.home-lgbtq-section{padding:0 0 clamp(42px,5vw,62px);background:var(--paper)}
.home-lgbtq-section .home-lgbtq-wrap{margin-top:0}
.home-credibility-strip{border-top:1px solid var(--line);background:var(--blue);color:var(--white)}
.home-credibility-strip>.wrap{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(30px,6vw,80px);padding-top:48px;padding-bottom:48px;align-items:end}
.home-credibility-strip .eyebrow{color:#f7c966}
.home-credibility-strip h2{max-width:12ch;margin:6px 0 0;font-family:var(--serif);font-size:clamp(34px,4vw,50px);font-weight:500;line-height:1}
.home-credibility-strip p{max-width:720px;margin:0;color:rgba(255,255,255,.78);font-size:12px;line-height:1.65}
.home-credibility-links{display:flex;flex-wrap:wrap;gap:16px!important;margin-top:18px!important}
.home-credibility-links a{color:#fff;font-size:9px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;border-bottom:1px solid rgba(255,255,255,.35)}
@media(max-width:1100px){.home-experience-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:760px){.home-now-inner,.home-credibility-strip>.wrap{grid-template-columns:1fr}.home-experience-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:480px){.home-experience-grid{grid-template-columns:1fr}.home-experience-card{display:grid;grid-template-columns:112px 1fr}.home-experience-card img{height:100%;min-height:118px}}
'''
    save("assets/v3.css", text, original)


def validate() -> None:
    errors = []
    specs = {
        "index.html": (
            'href="/en/riviera-fit/">Try Riviera Fit</a>',
            'href="/en/riviera-guide/">Choose your base</a>',
            '<p class="tool-badge">MAMETAS TOOL</p>',
            "10 EXPERIENCES",
            "home-now-teaser",
            "home-credibility-strip",
            "Explore Stay",
        ),
        "fr/index.html": (
            'href="/riviera-fit/">Tester Riviera Fit</a>',
            'href="/riviera-guide/">Choisir sa base</a>',
            '<p class="tool-badge">MAMETAS TOOL</p>',
            "10 EXPÉRIENCES",
            "home-now-teaser",
            "home-credibility-strip",
            "Explorer Dormir",
        ),
    }
    for rel, needles in specs.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
        experience_count = text.count('class="home-experience-card"')
        if experience_count != 10:
            errors.append(f"{rel}: expected 10 homepage experiences, found {experience_count}")
        if ("Do not collect the Riviera. Choose it." in text) or ("Ne collectionnez pas la Riviera. Choisissez-la." in text):
            errors.append(f"{rel}: duplicate second Places catalogue still present")
        if text.count('class="now-card"') > 0:
            errors.append(f"{rel}: old three-card Now grid still present")
    css_text = (ROOT / "assets/v3.css").read_text(encoding="utf-8")
    if "V3 homepage dispatch 2026-09-25" not in css_text:
        errors.append("assets/v3.css: homepage dispatch CSS missing")
    if errors:
        raise SystemExit("V3 homepage dispatch failed:\n- " + "\n- ".join(errors))


def main() -> int:
    patch_home("index.html", "en")
    patch_home("fr/index.html", "fr")
    css()
    validate()
    print(f"V3 homepage dispatch passed; changed {len(changed)} file(s).")
    for rel in changed:
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
