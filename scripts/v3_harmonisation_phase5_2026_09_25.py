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
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)


def add_body_class(text: str, cls: str) -> str:
    m = re.search(r"<body([^>]*)>", text, flags=re.I)
    if not m:
        return text
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs, flags=re.I)
    wanted = cls.split()
    if cm:
        classes = cm.group(1).split()
        for item in wanted:
            if item not in classes:
                classes.append(item)
        attrs2 = attrs[: cm.start()] + f'class="{" ".join(classes)}"' + attrs[cm.end():]
    else:
        attrs2 = attrs + f' class="{" ".join(wanted)}"'
    return text[:m.start()] + "<body" + attrs2 + ">" + text[m.end():]


def insert_after_article_hero(text: str, html: str, marker: str) -> str:
    if marker in text:
        return text
    m = re.search(r'(<header class="article-hero">.*?</header>)', text, flags=re.S)
    if not m:
        return text
    return text[:m.end()] + html + text[m.end():]


def insert_before(text: str, needle: str, html: str, marker: str) -> str:
    if marker in text or needle not in text:
        return text
    return text.replace(needle, html + needle, 1)


def patch_plan(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "plan-harmonised")
    text = text.replace('class="architecture-card architecture-card--tool"', 'class="architecture-card architecture-card--tool architecture-card--featured"', 1)
    if lang == "fr":
        fig = '<figure class="hub-hero-visual hub-hero-visual--plan harmonisation-plan-visual"><img src="/assets/editorial/nice-riviera.jpg" alt="La baie de Nice et la Côte d’Azur" loading="eager"></figure>'
    else:
        fig = '<figure class="hub-hero-visual hub-hero-visual--plan harmonisation-plan-visual"><img src="/assets/editorial/nice-riviera.jpg" alt="Nice and the French Riviera coastline" loading="eager"></figure>'
    text = insert_after_article_hero(text, fig, "harmonisation-plan-visual")
    m = re.search(r'(<section class="v3-section phase4-plan-depth">.*?</section>)', text, flags=re.S)
    if m and "architecture-next" in text and m.start() > text.find("architecture-next"):
        block = m.group(1)
        text = text[:m.start()] + text[m.end():]
        pos = text.find('<section class="v3-section architecture-next">')
        text = text[:pos] + block + text[pos:]
    save(rel, text, original)


def patch_practical(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "practical-harmonised")
    if lang == "fr":
        fig = '<figure class="hub-hero-visual harmonisation-practical-visual"><img src="/assets/editorial/riviera-train-hugo.webp" alt="Train régional le long de la Côte d’Azur" loading="eager"></figure>'
    else:
        fig = '<figure class="hub-hero-visual harmonisation-practical-visual"><img src="/assets/editorial/riviera-train-hugo.webp" alt="Regional train along the French Riviera" loading="eager"></figure>'
    text = insert_after_article_hero(text, fig, "harmonisation-practical-visual")
    text = re.sub(
        r'<p class="phase4-practical-extra"><a href="([^"]+)">([^<]+)</a></p>',
        r'<a class="practical-extra-card" href="\1"><span>SEASON</span><strong>\2</strong></a>',
        text,
        count=1,
    )
    save(rel, text, original)


def patch_explore(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "explore-harmonised")
    text = text.replace('class="lgbtq-banner"', 'class="lgbtq-banner lgbtq-banner--fifth"', 1)
    if lang == "fr":
        text = text.replace(
            "Quatre portes d’entrée. On commence par la question qui revient chaque jour, généralement vers midi : où est-ce qu’on mange ?",
            "Quatre grandes portes d’entrée, puis un guide transversal LGBTQ+. On commence par la question qui revient chaque jour, généralement vers midi : où est-ce qu’on mange ?",
        )
    else:
        text = text.replace(
            "Four doors in. We start with the question that returns every day, usually around noon: where are we eating?",
            "Four main doors in, plus one LGBTQ+ guide that cuts across the lot. We start with the question that returns every day, usually around noon: where are we eating?",
        )
    save(rel, text, original)


def patch_hotels(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "hotels-harmonised")
    if lang == "fr":
        h1 = "Trouvez le bon hôtel. Commencez par la bonne base."
        deck = "Un bel hôtel au mauvais endroit reste au mauvais endroit. Choisissez d’abord la ville qui correspond au séjour. Les peignoirs peuvent attendre."
    else:
        h1 = "Find the right hotel. Start with the right base."
        deck = "A beautiful hotel in the wrong place is still in the wrong place. Choose the town that fits the trip first. The bathrobes can wait."
    text = re.sub(r'(<header class="article-hero">.*?<h1>).*?(</h1>)', lambda m: m.group(1)+h1+m.group(2), text, count=1, flags=re.S)
    text = re.sub(r'(<header class="article-hero">.*?<p class="article-deck">).*?(</p>)', lambda m: m.group(1)+deck+m.group(2), text, count=1, flags=re.S)
    save(rel, text, original)


def patch_without_car(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "legacy-harmonised practical-article")
    if "harmonisation-without-car-visual" not in text:
        alt = "Train on the French Riviera coast" if lang == "en" else "Train sur le littoral de la Côte d’Azur"
        fig = f'<figure class="harmonisation-visual harmonisation-without-car-visual"><img src="/assets/editorial/riviera-train-hugo.webp" alt="{alt}" loading="lazy"></figure>'
        text = insert_before(text, '<div class="note">', fig, "harmonisation-without-car-visual")
    if "next-decisions-compact" not in text:
        if lang == "fr":
            nxt = '''<div class="next-decisions-compact"><span>CONTINUEZ</span><a href="/bons-plans/train-ou-bus/">Train ou bus ? →</a><a href="/fr/planifier/voiture-ou-pas/">Avez-vous vraiment besoin d’une voiture ? →</a><a href="/hotels/">Choisir l’hôtel →</a></div>'''
        else:
            nxt = '''<div class="next-decisions-compact"><span>KEEP GOING</span><a href="/en/good-finds/train-or-bus/">Train or bus? →</a><a href="/plan/car-or-no-car/">Do you actually need a car? →</a><a href="/en/hotels/">Choose the hotel →</a></div>'''
        text = insert_before(text, '<div class="sources">', nxt, "next-decisions-compact")
    save(rel, text, original)


def patch_train_bus(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "legacy-harmonised practical-article")
    if "harmonisation-train-visual" not in text:
        alt = "Regional train on the French Riviera" if lang == "en" else "Train régional sur la Côte d’Azur"
        fig = f'<figure class="harmonisation-visual harmonisation-train-visual"><img src="/assets/editorial/riviera-train-hugo.webp" alt="{alt}" loading="lazy"></figure>'
        text = insert_before(text, '<div class="verdict">', fig, "harmonisation-train-visual")
    if "next-decisions-compact" not in text:
        if lang == "fr":
            nxt = '''<div class="next-decisions-compact"><span>À CÔTÉ</span><a href="/bons-plans/transfert-aeroport-nice/">Aéroport vers votre base →</a><a href="/fr/planifier/voiture-ou-pas/">Voiture ou pas ? →</a><a href="/hotels/sans-voiture/">Où dormir sans voiture →</a></div>'''
        else:
            nxt = '''<div class="next-decisions-compact"><span>RELATED</span><a href="/en/good-finds/nice-airport-transfer/">Airport to your base →</a><a href="/plan/car-or-no-car/">Car or no car? →</a><a href="/en/hotels/without-a-car/">Where to stay without a car →</a></div>'''
        text = insert_before(text, '<div class="sources">', nxt, "next-decisions-compact")
    save(rel, text, original)


def append_after_section_paragraph(text: str, heading: str, html: str) -> str:
    marker_match = re.search(r'class="([^"]*rain-logistics-\d+[^"]*)"', html)
    marker = marker_match.group(1) if marker_match else html[:30]
    if marker in text:
        return text
    pattern = rf'(<h2>{re.escape(heading)}</h2>\s*<p>.*?</p>)'
    return re.sub(pattern, lambda m: m.group(1)+html, text, count=1, flags=re.S)


def patch_rain(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "legacy-harmonised rain-harmonised")
    if "harmonisation-rain-visuals" not in text:
        pair = '''<div class="harmonisation-visual-pair harmonisation-rain-visuals"><figure><img src="/assets/editorial/culture-musee-matisse.webp" alt="Musée Matisse, Nice" loading="lazy"></figure><figure><img src="/assets/editorial/culture-palais-lascaris.webp" alt="Palais Lascaris, Nice" loading="lazy"></figure></div>'''
        text = insert_before(text, '<div class="verdict">', pair, "harmonisation-rain-visuals")

    if lang == "en":
        rows = [
            ("1. Matisse Museum", "Cimiez · allow 60–90 min", "https://www.google.com/maps/search/?api=1&query=Musee+Matisse+Nice", "https://www.explorenicecotedazur.com/en/culture/musee-matisse-nice/"),
            ("2. Marc Chagall National Museum", "Cimiez edge · allow 60–90 min", "https://www.google.com/maps/search/?api=1&query=Musee+National+Marc+Chagall+Nice", "https://www.explorenicecotedazur.com/culture/musee-national-marc-chagall/"),
            ("3. Palais Lascaris", "Old Nice · allow 45–60 min", "https://www.google.com/maps/search/?api=1&query=Palais+Lascaris+Nice", "https://www.explorenicecotedazur.com/culture/palais-lascaris/"),
            ("4. Charles Nègre Photography Museum", "Cours Saleya · allow 45–75 min", "https://www.google.com/maps/search/?api=1&query=Musee+de+la+Photographie+Charles+Negre+Nice", "https://www.nice.fr/lieux/musee-de-la-photographie-charles-negre/"),
            ("5. Villa Masséna", "Promenade · allow 60–90 min", "https://www.google.com/maps/search/?api=1&query=Villa+Massena+Nice", "https://www.explorenicecotedazur.com/en/culture/villa-massena-musee-dart-et-dhistoire/"),
            ("6. Jules Chéret Fine Arts Museum", "Baumettes · allow 60–90 min", "https://www.google.com/maps/search/?api=1&query=Musee+des+Beaux-Arts+Jules+Cheret+Nice", "https://www.nice.fr/lieux/musee-des-beaux-arts/"),
        ]
        for idx, (h, meta, mp, off) in enumerate(rows, 1):
            html = f'<p class="spot-logistics rain-logistics-{idx}"><strong>{meta}.</strong> <a href="{mp}" target="_blank" rel="noopener">Map ↗</a> · <a href="{off}" target="_blank" rel="nofollow noopener">Official ↗</a></p>'
            text = append_after_section_paragraph(text, h, html)
        if "rain-day-flow" not in text:
            flow = '''<div class="rain-day-flow"><div><span>MORNING</span><strong>Matisse or Chagall</strong><p>Give one major museum proper time rather than collecting entrances.</p></div><div><span>LUNCH</span><strong>Back to the centre</strong><p>Old Nice or the Carré d’Or keeps the day walkable.</p></div><div><span>AFTERNOON</span><strong>Lascaris or photography</strong><p>Compact, central and easy to combine without turning rain into admin.</p></div></div>'''
            text = text.replace('<h2>1. Matisse Museum</h2>', flow+'<h2>1. Matisse Museum</h2>', 1)
    else:
        rows = [
            ("1. Musée Matisse", "Cimiez · comptez 60–90 min", "https://www.google.com/maps/search/?api=1&query=Musee+Matisse+Nice", "https://www.explorenicecotedazur.com/en/culture/musee-matisse-nice/"),
            ("2. Musée National Marc Chagall", "Bord de Cimiez · comptez 60–90 min", "https://www.google.com/maps/search/?api=1&query=Musee+National+Marc+Chagall+Nice", "https://www.explorenicecotedazur.com/culture/musee-national-marc-chagall/"),
            ("3. Palais Lascaris", "Vieux-Nice · comptez 45–60 min", "https://www.google.com/maps/search/?api=1&query=Palais+Lascaris+Nice", "https://www.explorenicecotedazur.com/culture/palais-lascaris/"),
            ("4. Musée de la Photographie Charles Nègre", "Cours Saleya · comptez 45–75 min", "https://www.google.com/maps/search/?api=1&query=Musee+de+la+Photographie+Charles+Negre+Nice", "https://www.nice.fr/lieux/musee-de-la-photographie-charles-negre/"),
            ("5. Villa Masséna", "Promenade · comptez 60–90 min", "https://www.google.com/maps/search/?api=1&query=Villa+Massena+Nice", "https://www.explorenicecotedazur.com/en/culture/villa-massena-musee-dart-et-dhistoire/"),
            ("6. Musée des Beaux-Arts Jules Chéret", "Baumettes · comptez 60–90 min", "https://www.google.com/maps/search/?api=1&query=Musee+des+Beaux-Arts+Jules+Cheret+Nice", "https://www.nice.fr/lieux/musee-des-beaux-arts/"),
        ]
        for idx, (h, meta, mp, off) in enumerate(rows, 1):
            html = f'<p class="spot-logistics rain-logistics-{idx}"><strong>{meta}.</strong> <a href="{mp}" target="_blank" rel="noopener">Carte ↗</a> · <a href="{off}" target="_blank" rel="nofollow noopener">Officiel ↗</a></p>'
            text = append_after_section_paragraph(text, h, html)
        if "rain-day-flow" not in text:
            flow = '''<div class="rain-day-flow"><div><span>MATIN</span><strong>Matisse ou Chagall</strong><p>Donnez du temps à un grand musée plutôt que de collectionner les entrées.</p></div><div><span>DÉJEUNER</span><strong>Retour au centre</strong><p>Vieux-Nice ou Carré d’Or gardent la journée simple à pied.</p></div><div><span>APRÈS-MIDI</span><strong>Lascaris ou photographie</strong><p>Compact, central et facile à combiner sans transformer la pluie en logistique.</p></div></div>'''
            text = text.replace('<h2>1. Musée Matisse</h2>', flow+'<h2>1. Musée Matisse</h2>', 1)
    save(rel, text, original)


def patch_beaches(rel: str, lang: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "beach-harmonised")
    if "beach-visual-pair" not in text:
        if lang == "en":
            alt1, alt2 = "La Gravette beach in Antibes", "A cove on Cap-Ferrat"
        else:
            alt1, alt2 = "Plage de la Gravette à Antibes", "Une crique du Cap-Ferrat"
        pair = f'''<div class="beach-visual-pair"><figure><img src="/assets/editorial/antibes-gravette.jpg" alt="{alt1}" loading="lazy"></figure><figure><img src="/assets/editorial/cap-ferrat-cove.jpg" alt="{alt2}" loading="lazy"></figure></div>'''
        text = text.replace('<h2 class="beach-zone-title">', pair+'<h2 class="beach-zone-title">', 1)
    save(rel, text, original)


def patch_v3_css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 harmonisation and clarification 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 harmonisation and clarification 2026-09-25 */
.hub-hero-visual{width:min(calc(100% - 2 * var(--gutter)),var(--max));height:clamp(280px,36vw,500px);margin:0 auto;overflow:hidden;background:var(--paper-deep)}
.hub-hero-visual img{width:100%;height:100%;object-fit:cover}
.plan-harmonised .article-hero,.practical-harmonised .article-hero{padding-bottom:54px}
.plan-harmonised .v3-section,.practical-harmonised .v3-section{padding-top:clamp(52px,5.5vw,78px);padding-bottom:clamp(52px,5.5vw,78px)}
.plan-harmonised .architecture-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:12px}
.plan-harmonised .architecture-card--featured{grid-column:1/-1;min-height:270px;padding:34px}
.plan-harmonised .architecture-card--featured h3{font-size:clamp(44px,5vw,64px)}
.plan-harmonised .architecture-card--featured p{max-width:720px;font-size:14px}
.plan-harmonised .architecture-card:not(.architecture-card--featured){grid-column:span 2;min-height:205px}
.plan-harmonised .phase4-plan-depth{background:rgba(23,54,95,.035)}
.plan-harmonised .architecture-next{padding-top:48px;padding-bottom:54px}
.plan-harmonised .architecture-next .decision-card{min-height:220px}
.practical-harmonised .practical-architecture-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.practical-extra-card{display:flex;min-height:78px;margin-top:14px;padding:18px 20px;align-items:center;justify-content:space-between;gap:24px;border:1px solid var(--line);background:rgba(216,173,82,.10);text-decoration:none}
.practical-extra-card span{color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}
.practical-extra-card strong{font-family:var(--serif);font-size:22px;font-weight:500}
.explore-harmonised .base-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:2px}
.explore-harmonised .base-card{min-height:390px}
.explore-harmonised .lgbtq-banner--fifth{min-height:170px;margin-top:2px;padding:30px;background:rgba(255,253,248,.55)}
.explore-harmonised .lgbtq-banner--fifth .lgbtq-banner-title{font-size:clamp(34px,4vw,48px)}
.hotels-harmonised .article-hero h1{max-width:900px}
@media(max-width:900px){
  .plan-harmonised .architecture-grid{grid-template-columns:1fr 1fr}
  .plan-harmonised .architecture-card--featured{grid-column:1/-1}
  .plan-harmonised .architecture-card:not(.architecture-card--featured){grid-column:auto}
}
@media(max-width:700px){
  .hub-hero-visual{width:100%;height:260px}
  .plan-harmonised .architecture-grid,.practical-harmonised .practical-architecture-grid,.explore-harmonised .base-grid{grid-template-columns:1fr}
  .plan-harmonised .architecture-card--featured{grid-column:auto;min-height:230px;padding:26px}
  .explore-harmonised .base-card{min-height:330px}
  .practical-extra-card{align-items:flex-start;flex-direction:column;gap:7px}
}
'''
    save("assets/v3.css", text, original)


def patch_site_css() -> None:
    p = ROOT / "assets/site.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 harmonisation legacy editorial pages 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 harmonisation legacy editorial pages 2026-09-25 */
.legacy-harmonised .article{padding-top:56px;padding-bottom:64px}
.legacy-harmonised .article .standfirst{margin-bottom:34px}
.legacy-harmonised .article h2{margin-top:40px}
.legacy-harmonised .article h3{margin-top:26px}
.legacy-harmonised .place{margin:14px 0;padding:22px;border:1px solid var(--line);background:rgba(255,255,255,.16)}
.harmonisation-visual{margin:30px 0 36px;overflow:hidden;background:var(--cream-deep)}
.harmonisation-visual img{width:100%;aspect-ratio:16/8;object-fit:cover}
.harmonisation-visual-pair,.beach-visual-pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:30px 0 38px}
.harmonisation-visual-pair figure,.beach-visual-pair figure{margin:0;overflow:hidden;background:var(--cream-deep)}
.harmonisation-visual-pair img,.beach-visual-pair img{width:100%;aspect-ratio:4/3;object-fit:cover}
.next-decisions-compact{display:flex;flex-wrap:wrap;gap:9px 12px;margin:42px 0 12px;padding-top:24px;border-top:1px solid var(--line)}
.next-decisions-compact>span{width:100%;color:var(--med-blue);font-size:9px;font-weight:700;letter-spacing:.15em;text-transform:uppercase}
.next-decisions-compact a{display:inline-flex;min-height:38px;padding:9px 12px;align-items:center;border:1px solid var(--line);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.next-decisions-compact a:hover{background:var(--cream-deep)}
.rain-day-flow{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:28px 0 36px;border:1px solid var(--line);background:var(--line)}
.rain-day-flow>div{padding:18px;background:var(--cream)}
.rain-day-flow span{display:block;margin-bottom:8px;color:var(--med-blue);font-size:9px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.rain-day-flow strong{display:block;font-family:var(--serif);font-size:20px;font-weight:500}
.rain-day-flow p{margin:8px 0 0!important;font-size:12px!important;line-height:1.55!important}
.rain-harmonised .spot-logistics{margin:8px 0 26px;padding:10px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:11px!important;line-height:1.55!important;color:var(--med-blue)!important}
.rain-harmonised .spot-logistics a{border-bottom:1px solid var(--gold)}
.beach-harmonised .section{padding-top:52px;padding-bottom:58px}
.beach-harmonised .beach-zone-title{margin-top:0}
@media(max-width:700px){
  .harmonisation-visual-pair,.beach-visual-pair,.rain-day-flow{grid-template-columns:1fr}
  .legacy-harmonised .article{padding-top:44px}
}
'''
    save("assets/site.css", text, original)


def validate() -> None:
    checks = {
        "plan/index.html": ("plan-harmonised", "architecture-card--featured", "harmonisation-plan-visual", "phase4-plan-depth"),
        "fr/planifier/index.html": ("plan-harmonised", "architecture-card--featured", "harmonisation-plan-visual", "phase4-plan-depth"),
        "en/practical/index.html": ("practical-harmonised", "harmonisation-practical-visual", "practical-extra-card"),
        "pratique/index.html": ("practical-harmonised", "harmonisation-practical-visual", "practical-extra-card"),
        "en/explore/index.html": ("explore-harmonised", "lgbtq-banner--fifth"),
        "explore/index.html": ("explore-harmonised", "lgbtq-banner--fifth"),
        "en/hotels/index.html": ("Find the right hotel. Start with the right base.",),
        "hotels/index.html": ("Trouvez le bon hôtel. Commencez par la bonne base.",),
        "en/hotels/without-a-car/index.html": ("harmonisation-without-car-visual", "next-decisions-compact"),
        "hotels/sans-voiture/index.html": ("harmonisation-without-car-visual", "next-decisions-compact"),
        "en/good-finds/train-or-bus/index.html": ("harmonisation-train-visual", "next-decisions-compact"),
        "bons-plans/train-ou-bus/index.html": ("harmonisation-train-visual", "next-decisions-compact"),
        "en/good-finds/nice-in-the-rain/index.html": ("harmonisation-rain-visuals", "rain-day-flow", "rain-logistics-6"),
        "bons-plans/nice-quand-il-pleut/index.html": ("harmonisation-rain-visuals", "rain-day-flow", "rain-logistics-6"),
        "en/beaches/index.html": ("beach-harmonised", "beach-visual-pair"),
        "plages/index.html": ("beach-harmonised", "beach-visual-pair"),
    }
    errors = []
    for rel, needles in checks.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: missing")
            continue
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
    for rel, needle in (("assets/v3.css", "V3 harmonisation and clarification 2026-09-25"), ("assets/site.css", "V3 harmonisation legacy editorial pages 2026-09-25")):
        if needle not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel}: missing harmonisation CSS")
    if errors:
        raise SystemExit("V3 harmonisation failed:\n- " + "\n- ".join(errors))


def main() -> int:
    patch_plan("plan/index.html", "en")
    patch_plan("fr/planifier/index.html", "fr")
    patch_practical("en/practical/index.html", "en")
    patch_practical("pratique/index.html", "fr")
    patch_explore("en/explore/index.html", "en")
    patch_explore("explore/index.html", "fr")
    patch_hotels("en/hotels/index.html", "en")
    patch_hotels("hotels/index.html", "fr")
    patch_without_car("en/hotels/without-a-car/index.html", "en")
    patch_without_car("hotels/sans-voiture/index.html", "fr")
    patch_train_bus("en/good-finds/train-or-bus/index.html", "en")
    patch_train_bus("bons-plans/train-ou-bus/index.html", "fr")
    patch_rain("en/good-finds/nice-in-the-rain/index.html", "en")
    patch_rain("bons-plans/nice-quand-il-pleut/index.html", "fr")
    patch_beaches("en/beaches/index.html", "en")
    patch_beaches("plages/index.html", "fr")
    patch_v3_css()
    patch_site_css()
    validate()
    print(f"V3 harmonisation passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
