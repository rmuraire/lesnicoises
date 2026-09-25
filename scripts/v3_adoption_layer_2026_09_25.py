#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []


def save(rel: str, text: str, original: str) -> None:
    if text != original:
        (ROOT / rel).write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)


def add_body_class(text: str, cls: str) -> str:
    m = re.search(r"<body([^>]*)>", text, flags=re.I)
    if not m:
        return text
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs, flags=re.I)
    if cm:
        classes = cm.group(1).split()
        if cls not in classes:
            classes.append(cls)
        attrs = attrs[:cm.start()] + 'class="' + " ".join(classes) + '"' + attrs[cm.end():]
    else:
        attrs += f' class="{cls}"'
    return text[:m.start()] + "<body" + attrs + ">" + text[m.end():]


def journey_spine(lang: str) -> str:
    if lang == "fr":
        return '''<nav class="home-journey-spine" aria-label="Comment Mametas vous aide à préparer la Côte d’Azur"><div class="wrap home-journey-inner"><span class="home-journey-label">VOTRE SÉJOUR, SIMPLIFIÉ</span><a href="/riviera-fit/"><b>01</b><strong>Choisir la base</strong><small>Riviera Fit ou les destinations</small></a><a href="/hotels/finder/"><b>02</b><strong>Choisir l’hôtel</strong><small>Hotel Fit</small></a><a href="/explore/"><b>03</b><strong>Remplir les journées</strong><small>Plages, culture, balades, tables</small></a><a href="/pratique/"><b>04</b><strong>Faire fonctionner le séjour</strong><small>Transport, météo, réservations</small></a></div></nav>'''
    return '''<nav class="home-journey-spine" aria-label="How Mametas helps plan a French Riviera trip"><div class="wrap home-journey-inner"><span class="home-journey-label">YOUR TRIP, SIMPLIFIED</span><a href="/en/riviera-fit/"><b>01</b><strong>Choose the base</strong><small>Riviera Fit or browse Places</small></a><a href="/en/hotels/finder/"><b>02</b><strong>Choose the hotel</strong><small>Hotel Fit</small></a><a href="/en/explore/"><b>03</b><strong>Fill the days</strong><small>Beaches, culture, walks, tables</small></a><a href="/en/practical/"><b>04</b><strong>Make it work</strong><small>Transport, weather, bookings</small></a></div></nav>'''


def stay_intro(lang: str) -> str:
    if lang == "fr":
        return '''<div class="stay-intro adoption-stay-intro"><p class="fit-tool-label fit-tool-label--hotel">MAMETAS · HOTEL FIT</p><p class="eyebrow">ÉTAPE 02 · CHOISIR L’HÔTEL</p><h2>Un bel hôtel peut rester le mauvais hôtel.</h2><p>Une fois la base choisie, Hotel Fit réduit la liste à quelques adresses adaptées à votre façon de voyager, avec la raison et le compromis.</p><div class="hotel-selection-actions"><a class="button hotel-fit-home-cta" href="/hotels/finder/">Tester Hotel Fit</a><a class="button secondary" href="/hotels/">Explorer Dormir</a></div></div>'''
    return '''<div class="stay-intro adoption-stay-intro"><p class="fit-tool-label fit-tool-label--hotel">MAMETAS · HOTEL FIT</p><p class="eyebrow">STEP 02 · CHOOSE THE HOTEL</p><h2>A beautiful hotel can still be the wrong hotel.</h2><p>Once the base is settled, Hotel Fit cuts the list to a few addresses that match how you travel, with the reason and the catch.</p><div class="hotel-selection-actions"><a class="button hotel-fit-home-cta" href="/en/hotels/finder/">Try Hotel Fit</a><a class="button secondary" href="/en/hotels/">Browse Stay</a></div></div>'''


def patch_home(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "adoption-home")

    if "home-journey-spine" not in text:
        anchor = re.search(r'<section[^>]*class="[^"]*chooser-signature-section--fit[^"]*"[^>]*>', text, flags=re.S)
        if not anchor:
            raise RuntimeError(f"{rel}: Riviera Fit homepage section not found")
        text = text[:anchor.start()] + journey_spine(lang) + text[anchor.start():]

    text = re.sub(
        r'<p class="eyebrow">[^<]*RIVIERA FIT[^<]*</p>',
        '<p class="eyebrow">MAMETAS · RIVIERA FIT</p>',
        text,
        count=1,
        flags=re.I,
    )
    if lang == "fr":
        text = text.replace("EXEMPLE · VOTRE SÉJOUR", "EXEMPLE · CE QUE VOUS OBTENEZ")
        text = text.replace("LA RECO MAMETAS", "RÉSULTAT D’EXEMPLE")
        text = text.replace('href="/riviera-chooser/"', 'href="/riviera-fit/"')
    else:
        text = text.replace("EXAMPLE · YOUR TRIP", "EXAMPLE · WHAT YOU GET")
        text = text.replace("THE MAMETAS CALL", "SAMPLE RESULT")
        text = text.replace('href="/en/riviera-chooser/"', 'href="/en/riviera-fit/"')

    pattern = re.compile(
        r'(<section class="v3-section" id="(?:stay|hotels)"><div class="wrap stay-layout">)'
        r'<div class="stay-intro">.*?(?=<div class="stay-list">)',
        flags=re.S,
    )
    text, count = pattern.subn(lambda m: m.group(1) + stay_intro(lang), text, count=1)
    if count != 1:
        # Accept repeat runs after the adoption class has already been added.
        pattern = re.compile(
            r'(<section class="v3-section" id="(?:stay|hotels)"><div class="wrap stay-layout">)'
            r'<div class="stay-intro adoption-stay-intro">.*?(?=<div class="stay-list">)',
            flags=re.S,
        )
        text, count = pattern.subn(lambda m: m.group(1) + stay_intro(lang), text, count=1)
    if count != 1:
        raise RuntimeError(f"{rel}: homepage Stay intro not found")

    save(rel, text, original)



def insert_after_article_hero(text: str, block: str) -> str:
    if "hub-adoption-cue" in text:
        return text
    m = re.search(r'<header class="article-hero">.*?</header>', text, flags=re.S)
    if not m:
        raise RuntimeError("article hero not found")
    return text[:m.end()] + block + text[m.end():]


def hub_cue(kind: str, lang: str) -> str:
    if lang == "fr":
        blocks = {
            "plan": '''<aside class="hub-adoption-cue hub-adoption-cue--step1"><div class="wrap hub-adoption-cue-inner"><div><span>ÉTAPE 01 · CONSTRUIRE LE VOYAGE</span><strong>Commencez par la base. Le reste devient beaucoup plus simple.</strong><p>Riviera Fit tranche rapidement. Destinations vous laisse comparer si vous préférez comprendre avant de choisir.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="#plan-riviera-fit-title">Utiliser Riviera Fit</a><a class="hub-secondary-action" href="/riviera-guide/">Comparer les destinations →</a></div></div></aside>''',
            "places": '''<aside class="hub-adoption-cue hub-adoption-cue--step1"><div class="wrap hub-adoption-cue-inner"><div><span>ÉTAPE 01 · CONFIRMER LA BASE</span><strong>Ici, on compare les villes. Pas les hôtels.</strong><p>Vous voulez comprendre les compromis ? Continuez. Vous voulez simplement une réponse ? Riviera Fit peut trancher.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="/riviera-fit/">Laisser Riviera Fit choisir</a><a class="hub-secondary-action" href="/fr/planifier/">Revenir à Plan →</a></div></div></aside>''',
            "stay": '''<aside class="hub-adoption-cue hub-adoption-cue--step2"><div class="wrap hub-adoption-cue-inner"><div><span>ÉTAPE 02 · CHOISIR L’HÔTEL</span><strong>La base est décidée ? Maintenant seulement, choisissez l’hôtel.</strong><p>Hotel Fit réduit la liste selon votre façon de voyager. Si vous préférez parcourir, entrez directement par la ville.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action hub-primary-action--hotel" href="/hotels/finder/">Utiliser Hotel Fit</a><a class="hub-secondary-action" href="#stay-by-base">Parcourir par base →</a></div></div></aside>''',
            "explore": '''<aside class="hub-adoption-cue hub-adoption-cue--step3"><div class="wrap hub-adoption-cue-inner"><div><span>ÉTAPE 03 · REMPLIR LES JOURNÉES</span><strong>Choisissez une envie, pas une liste de choses à cocher.</strong><p>Restaurants, baignade, culture ou balade : partez de l’humeur du jour. Mametas garde le tri court.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="/explore/2-3-heures/">J’ai 2 ou 3 heures</a><a class="hub-secondary-action" href="/plages/">Commencer par la mer →</a></div></div></aside>''',
            "practical": '''<aside class="hub-adoption-cue hub-adoption-cue--step4"><div class="wrap hub-adoption-cue-inner"><div><span>ÉTAPE 04 · FAIRE FONCTIONNER LE SÉJOUR</span><strong>Réglez les détails une fois. Puis arrêtez d’y penser.</strong><p>Transport, arrivée, météo et réservations : ici, l’information est pratique, datée et conçue pour être exécutée.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="/bons-plans/train-ou-bus/">Train ou bus ?</a><a class="hub-secondary-action" href="/bons-plans/que-reserver/">Que réserver ? →</a></div></div></aside>''',
        }
    else:
        blocks = {
            "plan": '''<aside class="hub-adoption-cue hub-adoption-cue--step1"><div class="wrap hub-adoption-cue-inner"><div><span>STEP 01 · SHAPE THE TRIP</span><strong>Start with the base. Everything else gets easier.</strong><p>Riviera Fit makes the call quickly. Places lets you compare if you would rather understand before deciding.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="#plan-riviera-fit-title">Use Riviera Fit</a><a class="hub-secondary-action" href="/en/riviera-guide/">Compare the places →</a></div></div></aside>''',
            "places": '''<aside class="hub-adoption-cue hub-adoption-cue--step1"><div class="wrap hub-adoption-cue-inner"><div><span>STEP 01 · CONFIRM THE BASE</span><strong>Compare towns here. Not hotels.</strong><p>Want to understand the trade-offs? Keep browsing. Want the answer faster? Riviera Fit can make the call.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="/en/riviera-fit/">Let Riviera Fit decide</a><a class="hub-secondary-action" href="/plan/">Back to Plan →</a></div></div></aside>''',
            "stay": '''<aside class="hub-adoption-cue hub-adoption-cue--step2"><div class="wrap hub-adoption-cue-inner"><div><span>STEP 02 · CHOOSE THE HOTEL</span><strong>Base settled? Only now choose the hotel.</strong><p>Hotel Fit cuts the list according to how you travel. If you prefer to browse, enter directly through the town.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action hub-primary-action--hotel" href="/en/hotels/finder/">Use Hotel Fit</a><a class="hub-secondary-action" href="#stay-by-base">Browse by base →</a></div></div></aside>''',
            "explore": '''<aside class="hub-adoption-cue hub-adoption-cue--step3"><div class="wrap hub-adoption-cue-inner"><div><span>STEP 03 · FILL THE DAYS</span><strong>Choose a mood, not a checklist.</strong><p>Food, swimming, culture or a walk: start with what the day feels like. Mametas keeps the shortlist short.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="/en/explore/2-3-hours/">I have 2 or 3 hours</a><a class="hub-secondary-action" href="/en/beaches/">Start with the sea →</a></div></div></aside>''',
            "practical": '''<aside class="hub-adoption-cue hub-adoption-cue--step4"><div class="wrap hub-adoption-cue-inner"><div><span>STEP 04 · MAKE THE TRIP WORK</span><strong>Sort the details once. Then stop thinking about them.</strong><p>Transport, arrival, weather and booking rules: practical, dated information designed to be used.</p></div><div class="hub-adoption-actions"><a class="button hub-primary-action" href="/en/good-finds/train-or-bus/">Train or bus?</a><a class="hub-secondary-action" href="/en/good-finds/what-to-book/">What to book →</a></div></div></aside>''',
        }
    return blocks[kind]


def next_step(kind: str, lang: str) -> str:
    if lang == "fr":
        blocks = {
            "base": '''<section class="hub-next-step"><div class="wrap hub-next-step-inner"><div><span>ÉTAPE 02</span><h2>Base choisie ? Passez à l’hôtel.</h2><p>Hotel Fit garde la géographie et réduit la sélection à quelques adresses adaptées à votre séjour.</p></div><div class="hub-next-actions"><a class="button hub-primary-action hub-primary-action--hotel" href="/hotels/finder/">Ouvrir Hotel Fit</a><a href="/hotels/">Ou parcourir Dormir →</a></div></div></section>''',
            "stay": '''<section class="hub-next-step"><div class="wrap hub-next-step-inner"><div><span>ÉTAPE 03</span><h2>Hôtel choisi ? Remplissez les journées.</h2><p>Plages, culture, restaurants, balades et excursions, sans transformer les vacances en tableau Excel.</p></div><div class="hub-next-actions"><a class="button hub-primary-action" href="/explore/">Explorer</a><a href="/pratique/">Ou régler la logistique →</a></div></div></section>''',
            "explore": '''<section class="hub-next-step"><div class="wrap hub-next-step-inner"><div><span>ÉTAPE 04</span><h2>La journée tient debout ? Réglez la mécanique.</h2><p>Train, bus, arrivée, météo et ce qu’il faut réellement réserver.</p></div><div class="hub-next-actions"><a class="button hub-primary-action" href="/pratique/">Ouvrir Pratique</a><a href="/bons-plans/septembre-2026/">Voir Right Now →</a></div></div></section>''',
            "practical": '''<section class="hub-next-step hub-next-step--quiet"><div class="wrap hub-next-step-inner"><div><span>C’EST BON</span><h2>La mécanique est réglée. Retournez au voyage.</h2><p>Le pratique doit disparaître dès qu’il a fait son travail.</p></div><div class="hub-next-actions"><a class="button secondary" href="/explore/">Retourner à Explore</a><a href="/riviera-guide/">Revoir les destinations →</a></div></div></section>''',
        }
    else:
        blocks = {
            "base": '''<section class="hub-next-step"><div class="wrap hub-next-step-inner"><div><span>STEP 02</span><h2>Base chosen? Move to the hotel.</h2><p>Hotel Fit keeps the geography and cuts the shortlist to a few addresses that fit the trip.</p></div><div class="hub-next-actions"><a class="button hub-primary-action hub-primary-action--hotel" href="/en/hotels/finder/">Open Hotel Fit</a><a href="/en/hotels/">Or browse Stay →</a></div></div></section>''',
            "stay": '''<section class="hub-next-step"><div class="wrap hub-next-step-inner"><div><span>STEP 03</span><h2>Hotel chosen? Fill the days.</h2><p>Beaches, culture, restaurants, walks and day trips without turning the holiday into a spreadsheet.</p></div><div class="hub-next-actions"><a class="button hub-primary-action" href="/en/explore/">Explore</a><a href="/en/practical/">Or sort the logistics →</a></div></div></section>''',
            "explore": '''<section class="hub-next-step"><div class="wrap hub-next-step-inner"><div><span>STEP 04</span><h2>Day shaped? Sort the mechanics.</h2><p>Train, bus, arrival, weather and the things that genuinely need booking.</p></div><div class="hub-next-actions"><a class="button hub-primary-action" href="/en/practical/">Open Practical</a><a href="/en/good-finds/september-2026/">See Right Now →</a></div></div></section>''',
            "practical": '''<section class="hub-next-step hub-next-step--quiet"><div class="wrap hub-next-step-inner"><div><span>DONE</span><h2>The mechanics are sorted. Get back to the trip.</h2><p>Practical information should disappear once it has done its job.</p></div><div class="hub-next-actions"><a class="button secondary" href="/en/explore/">Back to Explore</a><a href="/en/riviera-guide/">Revisit Places →</a></div></div></section>''',
        }
    return blocks[kind]


def replace_section_containing_adoption(text: str, needle: str, replacement: str) -> tuple[str, bool]:
    for m in re.finditer(r'<section\b[^>]*>.*?</section>', text, flags=re.S):
        if needle in m.group(0):
            return text[:m.start()] + replacement + text[m.end():], True
    return text, False


def patch_hub(rel: str, lang: str, kind: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "adoption-hub")
    text = add_body_class(text, f"adoption-hub--{kind}")
    text = insert_after_article_hero(text, hub_cue(kind, lang))

    if kind == "stay":
        text = re.sub(r'<section class="v3-section stay-base-section">', '<section class="v3-section stay-base-section" id="stay-by-base">', text, count=1)
        if "hub-next-step" not in text:
            pos = text.rfind("</main>")
            text = text[:pos] + next_step("stay", lang) + text[pos:]
    elif kind == "explore":
        if "hub-next-step" not in text:
            pos = text.rfind("</main>")
            text = text[:pos] + next_step("explore", lang) + text[pos:]
    elif kind == "practical":
        if "hub-next-step" not in text:
            pos = text.rfind("</main>")
            text = text[:pos] + next_step("practical", lang) + text[pos:]
    elif kind == "plan":
        text2, ok = replace_section_containing_adoption(text, 'class="v3-section architecture-next"', next_step("base", lang))
        if ok:
            text = text2
        elif "hub-next-step" not in text:
            pos = text.rfind("</main>")
            text = text[:pos] + next_step("base", lang) + text[pos:]
    elif kind == "places":
        needles = (
            "Good. Now stop comparing towns.",
            "Très bien. Arrêtez de comparer les villes.",
            "Base chosen?",
            "LA BASE TIENT TOUJOURS ?",
        )
        replaced = False
        for needle in needles:
            text2, ok = replace_section_containing_adoption(text, needle, next_step("base", lang))
            if ok:
                text, replaced = text2, True
                break
        if not replaced and "hub-next-step" not in text:
            pos = text.rfind("</main>")
            text = text[:pos] + next_step("base", lang) + text[pos:]

    save(rel, text, original)


def patch_css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 adoption layer 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 adoption layer 2026-09-25 */

/* The homepage explains the journey before exposing the depth of the site. */
.home-journey-spine{border-bottom:1px solid var(--line);background:rgba(255,253,248,.72)}
.home-journey-inner{display:grid;grid-template-columns:minmax(130px,.62fr) repeat(4,minmax(0,1fr));align-items:stretch}
.home-journey-label{display:flex;align-items:center;padding:16px 18px 16px 0;color:var(--ink-soft);font-size:8px;font-weight:800;letter-spacing:.14em;line-height:1.4;text-transform:uppercase}
.home-journey-inner>a{display:grid;grid-template-columns:auto 1fr;column-gap:10px;align-content:center;min-height:82px;padding:13px 16px;border-left:1px solid var(--line);text-decoration:none;transition:background .16s ease}
.home-journey-inner>a:hover,.home-journey-inner>a:focus-visible{background:var(--white)}
.home-journey-inner>a b{grid-row:1/3;color:var(--coral);font-family:var(--serif);font-size:14px;font-style:italic;font-weight:500}
.home-journey-inner>a strong{font-family:var(--serif);font-size:17px;font-weight:500;line-height:1.08}
.home-journey-inner>a small{margin-top:4px;color:var(--ink-soft);font-size:8.5px;line-height:1.35}

/* Riviera Fit remains important, but behaves like a product, not a second hero. */
.adoption-home .chooser-signature-section--fit{padding:clamp(48px,5vw,66px) 0;background:var(--paper);color:var(--ink)}
.adoption-home .riviera-fit-home{grid-template-columns:minmax(0,.82fr) minmax(420px,1.18fr);gap:clamp(30px,4.5vw,62px)}
.adoption-home .riviera-fit-home-copy .eyebrow{color:var(--blue-deep)}
.adoption-home .riviera-fit-home-copy h2{font-size:clamp(38px,4.1vw,56px)}
.adoption-home .riviera-fit-home-punch{color:var(--blue-deep)!important;font-size:clamp(19px,1.8vw,24px)!important}
.adoption-home .riviera-fit-home-copy>p:not(.eyebrow):not(.riviera-fit-home-punch){color:var(--ink-soft)}
.adoption-home .chooser-signature-primary{background:var(--blue);color:#fff}
.adoption-home .riviera-fit-home-demo{border:1px solid var(--line);background:var(--white);box-shadow:0 12px 30px rgba(20,33,61,.04)}
.adoption-home .riviera-fit-demo-label{display:inline-flex;color:var(--coral)!important}
.adoption-home .riviera-fit-home-demo>.riviera-fit-demo-label{margin:18px 20px 0!important;padding:6px 8px!important;border:1px solid rgba(199,91,61,.28);background:rgba(199,91,61,.05)}
.adoption-home .riviera-fit-demo-chips{padding:13px 20px 18px;border-bottom:1px solid var(--line)}
.adoption-home .riviera-fit-demo-chips span{border:1px solid var(--line);background:var(--paper);color:var(--ink);font-size:8.5px}
.adoption-home .riviera-fit-home-verdict{padding:18px 20px 20px;background:rgba(23,54,95,.035)}
.adoption-home .riviera-fit-home-verdict .riviera-fit-demo-label{padding:0;background:transparent}
.adoption-home .riviera-fit-home-verdict h3{color:var(--ink);font-size:clamp(29px,3vw,40px)}
.adoption-home .riviera-fit-home-verdict>p:not(.riviera-fit-demo-label){color:var(--ink-soft)}
.adoption-home .riviera-fit-home-verdict strong{color:var(--ink)}
.adoption-home .riviera-fit-reality{background:var(--line)}
.adoption-home .riviera-fit-reality span{background:var(--paper);color:var(--ink-soft)}
.adoption-home .riviera-fit-reality b{color:var(--ink)}

/* Hotel Fit is visible at the moment the hotel decision becomes relevant. */
.adoption-stay-intro .fit-tool-label--hotel{margin:0 0 10px;border-color:rgba(199,91,61,.42);background:rgba(199,91,61,.055);color:var(--coral)!important}
.adoption-stay-intro .eyebrow{margin-bottom:10px}
.adoption-stay-intro .hotel-selection-actions{margin-top:22px}
.adoption-stay-intro .hotel-fit-home-cta{background:var(--coral);border-color:var(--coral);color:#fff}

/* Hub adoption: one job, one next move. */
.hub-adoption-cue{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(23,54,95,.025)}
.hub-adoption-cue-inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:34px;align-items:center;padding-top:20px;padding-bottom:20px}
.hub-adoption-cue span,.hub-next-step span{display:block;margin-bottom:5px;color:var(--coral);font-size:8px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.hub-adoption-cue strong{display:block;font-family:var(--serif);font-size:clamp(20px,2vw,27px);font-weight:500;line-height:1.08}
.hub-adoption-cue p{max-width:760px;margin:6px 0 0;color:var(--ink-soft);font-size:10.5px;line-height:1.55}
.hub-adoption-actions{display:flex;align-items:center;gap:14px;white-space:nowrap}
.hub-secondary-action,.hub-next-actions>a:not(.button){font-size:9px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
.hub-primary-action{background:var(--blue);border-color:var(--blue);color:#fff}
.hub-primary-action--hotel{background:var(--coral);border-color:var(--coral);color:#fff}
.hub-next-step{border-top:1px solid var(--line);background:rgba(255,253,248,.76)}
.hub-next-step--quiet{background:rgba(23,54,95,.025)}
.hub-next-step-inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:38px;align-items:center;padding-top:34px;padding-bottom:34px}
.hub-next-step h2{margin:0 0 7px;font-family:var(--serif);font-size:clamp(29px,3.3vw,43px);font-weight:500;line-height:1}
.hub-next-step p{max-width:720px;margin:0;color:var(--ink-soft);font-size:11px;line-height:1.55}
.hub-next-actions{display:flex;flex-direction:column;align-items:flex-start;gap:10px;min-width:170px}
.adoption-hub--plan .architecture-next{display:none}
.adoption-hub--places .decision-grid+.hub-next-step{margin-top:0}

@media(max-width:1050px){
  .home-journey-inner{grid-template-columns:repeat(2,minmax(0,1fr))}
  .home-journey-label{grid-column:1/-1;padding:13px 0;border-bottom:1px solid var(--line)}
  .home-journey-inner>a:nth-of-type(odd){border-left:0}
  .home-journey-inner>a{border-bottom:1px solid var(--line)}
}
@media(max-width:760px){
  .home-journey-inner{grid-template-columns:1fr}
  .home-journey-label{padding-left:0}
  .home-journey-inner>a{min-height:68px;padding:11px 4px;border-left:0}
  .home-journey-inner>a strong{font-size:16px}
  .adoption-home .riviera-fit-home{grid-template-columns:1fr}
  .adoption-home .riviera-fit-home-demo{max-width:none}
  .hub-adoption-cue-inner,.hub-next-step-inner{grid-template-columns:1fr;gap:18px}
  .hub-adoption-actions{align-items:flex-start;flex-direction:column;white-space:normal}
  .hub-next-actions{min-width:0}
}
'''
    save("assets/v3.css", text, original)


def validate() -> None:
    checks = {
        "index.html": (
            "home-journey-spine",
            "MAMETAS · RIVIERA FIT",
            "EXAMPLE · WHAT YOU GET",
            "SAMPLE RESULT",
            "MAMETAS · HOTEL FIT",
            "Try Hotel Fit",
        ),
        "fr/index.html": (
            "home-journey-spine",
            "MAMETAS · RIVIERA FIT",
            "EXEMPLE · CE QUE VOUS OBTENEZ",
            "RÉSULTAT D’EXEMPLE",
            "MAMETAS · HOTEL FIT",
            "Tester Hotel Fit",
        ),
    }
    errors: list[str] = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
        if "Riviera Chooser" in text:
            errors.append(f"{rel}: stale Riviera Chooser naming remains")
    hub_checks = {
        "plan/index.html": ("hub-adoption-cue", "STEP 01", "hub-next-step", "Open Hotel Fit"),
        "fr/planifier/index.html": ("hub-adoption-cue", "ÉTAPE 01", "hub-next-step", "Ouvrir Hotel Fit"),
        "en/riviera-guide/index.html": ("hub-adoption-cue", "CONFIRM THE BASE", "hub-next-step", "Open Hotel Fit"),
        "riviera-guide/index.html": ("hub-adoption-cue", "CONFIRMER LA BASE", "hub-next-step", "Ouvrir Hotel Fit"),
        "en/hotels/index.html": ("hub-adoption-cue", "STEP 02", 'id="stay-by-base"', "hub-next-step"),
        "hotels/index.html": ("hub-adoption-cue", "ÉTAPE 02", 'id="stay-by-base"', "hub-next-step"),
        "en/explore/index.html": ("hub-adoption-cue", "STEP 03", "hub-next-step", "Open Practical"),
        "explore/index.html": ("hub-adoption-cue", "ÉTAPE 03", "hub-next-step", "Ouvrir Pratique"),
        "en/practical/index.html": ("hub-adoption-cue", "STEP 04", "hub-next-step", "Back to Explore"),
        "pratique/index.html": ("hub-adoption-cue", "ÉTAPE 04", "hub-next-step", "Retourner à Explore"),
    }
    for rel, needles in hub_checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing hub adoption marker {needle!r}")
    css = (ROOT / "assets/v3.css").read_text(encoding="utf-8")
    if "V3 adoption layer 2026-09-25" not in css:
        errors.append("assets/v3.css: adoption layer CSS missing")
    if errors:
        raise SystemExit("V3 adoption layer failed:\n- " + "\n- ".join(errors))


def main() -> int:
    patch_home("index.html", "en")
    patch_home("fr/index.html", "fr")
    patch_hub("plan/index.html", "en", "plan")
    patch_hub("fr/planifier/index.html", "fr", "plan")
    patch_hub("en/riviera-guide/index.html", "en", "places")
    patch_hub("riviera-guide/index.html", "fr", "places")
    patch_hub("en/hotels/index.html", "en", "stay")
    patch_hub("hotels/index.html", "fr", "stay")
    patch_hub("en/explore/index.html", "en", "explore")
    patch_hub("explore/index.html", "fr", "explore")
    patch_hub("en/practical/index.html", "en", "practical")
    patch_hub("pratique/index.html", "fr", "practical")
    patch_css()
    validate()
    print(f"V3 adoption layer passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
