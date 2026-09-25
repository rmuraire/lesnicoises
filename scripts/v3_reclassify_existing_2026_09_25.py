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


def replace_once(rel: str, old: str, new: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if old in text:
        text = text.replace(old, new, 1)
    save(rel, text, original)


def right_now_hub(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        main = '''<main><section class="page-hero"><div class="wrap"><p class="eyebrow">EN CE MOMENT</p><h1>Ce qui change maintenant sur la Riviera.</h1><p class="lead">Événements, affluence, fermetures et détails saisonniers : uniquement ce qui peut modifier votre séjour aujourd’hui. Pour le transport, les billets et les règles durables, passez par Pratique.</p></div></section><section class="section right-now-clean"><div class="wrap"><div class="grid"><a class="card" href="/bons-plans/septembre-2026/"><span class="kicker">Septembre 2026</span><h3>Ce qui mérite votre attention ce mois-ci</h3><p>Les dates chargées, les grands événements et les informations saisonnières qui peuvent changer une réservation ou une journée.</p><span class="more">Voir septembre</span></a><a class="card right-now-practical-card" href="/pratique/"><span class="kicker">Informations permanentes</span><h3>Vous cherchez le pratique ?</h3><p>Aéroport, train, bus, réservations, pluie et règles qui évitent les cagades vivent désormais dans une rubrique dédiée.</p><span class="more">Ouvrir Pratique</span></a></div></div></section></main>'''
    else:
        main = '''<main><section class="page-hero"><div class="wrap"><p class="eyebrow">RIGHT NOW</p><h1>What is changing on the Riviera now.</h1><p class="lead">Events, crowd pressure, closures and seasonal details: only the things that can change your trip today. For transport, tickets and durable rules, use Practical.</p></div></section><section class="section right-now-clean"><div class="wrap"><div class="grid"><a class="card" href="/en/good-finds/september-2026/"><span class="kicker">September 2026</span><h3>What deserves attention this month</h3><p>Busy dates, major events and seasonal details that can change a booking or a day.</p><span class="more">See September</span></a><a class="card right-now-practical-card" href="/en/practical/"><span class="kicker">Evergreen guidance</span><h3>Looking for the practical stuff?</h3><p>Airport, trains, buses, booking rules, rain and the things that prevent cagades now live in a dedicated section.</p><span class="more">Open Practical</span></a></div></div></section></main>'''
    text, n = re.subn(r'<main>.*?</main>', main, text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"{rel}: main not found")
    save(rel, text, original)


def practical_legacy(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace('href="/bons-plans/">← Retour</a>', 'href="/pratique/">← Retour à Pratique</a>')
        text = text.replace('href="/bons-plans/">Retour</a>', 'href="/pratique/">Retour à Pratique</a>')
        note = '<div class="ownership-note" data-phase3-owner="practical"><strong>Rubrique Pratique.</strong> Cette page garde son URL, mais sa profondeur appartient désormais à Pratique : données opérationnelles, billets, horaires, réservations et solutions de repli. <a href="/pratique/">Voir tout le pratique →</a></div>'
    else:
        text = text.replace('href="/en/good-finds/">← Back</a>', 'href="/en/practical/">← Back to Practical</a>')
        text = text.replace('href="/en/good-finds/">Back</a>', 'href="/en/practical/">Back to Practical</a>')
        note = '<div class="ownership-note" data-phase3-owner="practical"><strong>Practical section.</strong> This page keeps its URL, but its depth now belongs to Practical: operational detail, tickets, timetables, booking rules and backup plans. <a href="/en/practical/">See all Practical guides →</a></div>'
    if 'data-phase3-owner="practical"' not in text:
        m = re.search(r'(<p class="standfirst">.*?</p>)', text, flags=re.S)
        if m:
            text = text[:m.end()] + note + text[m.end():]
        else:
            h1 = re.search(r'</h1>', text)
            if h1:
                text = text[:h1.end()] + note + text[h1.end():]
    save(rel, text, original)


def car_free_stay(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        note = '<div class="ownership-note ownership-note--split" data-phase3-owner="carfree"><strong>Cette page répond à une seule question : où dormir sans voiture.</strong> Pour décider si vous devez louer une voiture, allez dans <a href="/fr/planifier/">Plan</a>. Pour les tarifs, billets et la mécanique train/tram/bus, allez dans <a href="/pratique/">Pratique</a>.</div>'
        hotel = '<div class="source-box phase3-hotel-fit"><strong>Base choisie ?</strong> Ouvrez <a href="/hotels/finder/">Hotel Fit</a> pour choisir l’hôtel selon budget, rôle, mobilité et géographie.</div>'
    else:
        note = '<div class="ownership-note ownership-note--split" data-phase3-owner="carfree"><strong>This page answers one question: where to stay without a car.</strong> To decide whether you need to rent one, use <a href="/plan/">Plan</a>. For fares, tickets and train/tram/bus mechanics, use <a href="/en/practical/">Practical</a>.</div>'
        hotel = '<div class="source-box phase3-hotel-fit"><strong>Base chosen?</strong> Open <a href="/en/hotels/finder/">Hotel Fit</a> to choose the hotel by budget, role, mobility and geography.</div>'
    if 'data-phase3-owner="carfree"' not in text:
        m = re.search(r'(<p class="standfirst">.*?</p>)', text, flags=re.S)
        if m:
            text = text[:m.end()] + note + text[m.end():]
    if 'phase3-hotel-fit' not in text:
        pos = text.find('<div class="sources">')
        if pos >= 0:
            text = text[:pos] + hotel + text[pos:]
        else:
            text = text.replace('</article>', hotel + '</article>', 1)
    save(rel, text, original)


def nice_places(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        boundary = '<div class="source-box place-stay-boundary" data-phase3-owner="stay"><strong>Ici, on choisit le quartier, pas l’hôtel.</strong> Gardez cette section pour comprendre Nice-Ville, Masséna, Vieux-Nice et le Port. Pour passer aux adresses, <a href="/hotels/finder/?base=nice">ouvrez Hotel Fit pour Nice →</a></div>'
        old_air = re.compile(r'<h2>Depuis l’aéroport</h2>\s*<p>.*?</p>', re.S)
        new_air = '<h2>Depuis l’aéroport</h2><p>Le tram relie directement l’aéroport au centre et au Port. C’est l’information utile pour juger Nice comme base. Pour les tarifs, fréquences, Saint-Augustin, TER et taxi à jour, <a href="/bons-plans/transfert-aeroport-nice/">ouvrez le guide Pratique aéroport →</a></p>'
        text = old_air.sub(new_air, text, count=1)
        text = text.replace('<p><a href="/fr/dormir/nice/">Voir le sélecteur d’hôtels de Nice par style de séjour →</a></p>', '<p><a href="/hotels/finder/?base=nice">Passer de la logique de quartier à Hotel Fit pour Nice →</a></p>')
        text = text.replace('<a href="/fr/dormir/nice/">Not yet - choose the right Nice base →</a>', '<a href="/hotels/finder/?base=nice">Choisir maintenant l’hôtel avec Hotel Fit →</a>')
    else:
        boundary = '<div class="source-box place-stay-boundary" data-phase3-owner="stay"><strong>This section chooses the neighbourhood, not the hotel.</strong> Use it to understand Nice-Ville, Masséna, Old Nice and the Port. For actual addresses, <a href="/en/hotels/finder/?base=nice">open Hotel Fit for Nice →</a></div>'
        old_air = re.compile(r'<h2>From the airport</h2>\s*<p>.*?</p>', re.S)
        new_air = '<h2>From the airport</h2><p>The tram links the airport directly with the centre and Port. That is the useful fact when judging Nice as a base. For current fares, frequency, Saint-Augustin, TER and taxi detail, <a href="/en/good-finds/nice-airport-transfer/">open the Practical airport guide →</a></p>'
        text = old_air.sub(new_air, text, count=1)
        text = text.replace('<p><a href="/stay/nice/">See the Nice hotel chooser by trip style →</a></p>', '<p><a href="/en/hotels/finder/?base=nice">Move from neighbourhood logic to Hotel Fit for Nice →</a></p>')
        text = text.replace('<a href="/stay/nice/">Not yet - choose the right Nice base →</a>', '<a href="/en/hotels/finder/?base=nice">Choose the hotel now with Hotel Fit →</a>')
    if 'place-stay-boundary' not in text:
        marker = '<h2>Où dormir à Nice' if lang == "fr" else '<h2>Where to stay in Nice'
        pos = text.find(marker)
        if pos >= 0:
            text = text[:pos] + boundary + text[pos:]
    save(rel, text, original)


def compact_antibes_hotels(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        pattern = re.compile(r'<h2 id="dormir">Où dormir à Antibes</h2>.*?(?=<h2 id="cannes">)', re.S)
        block = '''<h2 id="dormir">Où dormir à Antibes</h2><p>Le choix utile ici est géographique : Antibes centre si vous voulez vieille ville, restaurants, gare et plage à pied ; le Cap si l’hôtel, le calme et la mer doivent prendre davantage de place.</p><div class="source-box place-stay-boundary" data-phase3-owner="stay"><strong>On s’arrête au choix de zone.</strong> Pour comparer les hôtels retenus par Mametas selon votre budget et vos priorités, <a href="/hotels/finder/?base=antibes">ouvrez Hotel Fit pour Antibes →</a></div>'''
    else:
        pattern = re.compile(r'<h2 id="stay">Where to stay in Antibes</h2>.*?(?=<h2 id="cannes">)', re.S)
        block = '''<h2 id="stay">Where to stay in Antibes</h2><p>The useful choice here is geographical: central Antibes for old town, restaurants, station and beach on foot; the Cap when the hotel, calm and sea should take a bigger role.</p><div class="source-box place-stay-boundary" data-phase3-owner="stay"><strong>Places stops at the area choice.</strong> To compare Mametas-selected hotels by budget and priorities, <a href="/en/hotels/finder/?base=antibes">open Hotel Fit for Antibes →</a></div>'''
    text, n = pattern.subn(block, text, count=1)
    if n != 1:
        raise RuntimeError(f"{rel}: Antibes stay section not found")
    save(rel, text, original)


def compact_villefranche_hotels(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        pattern = re.compile(r'<h2 id="dormir">Où dormir : trois façons sensées de le faire</h2>.*?(?=<h2 id="journee">)', re.S)
        block = '''<h2 id="dormir">Où dormir : trois géographies différentes</h2><p><strong>Villefranche</strong> pour le port et la vieille ville devant la porte. <strong>Cap-Ferrat</strong> pour un séjour où l’hôtel et la mer deviennent une destination. <strong>Beaulieu</strong> pour une base plus calme et plus rationnelle côté train.</p><div class="source-box place-stay-boundary" data-phase3-owner="stay"><strong>La page destination choisit la géographie, pas la chambre.</strong> <a href="/hotels/finder/?base=villefranche">Ouvrir Hotel Fit pour Villefranche / Cap-Ferrat →</a></div>'''
    else:
        pattern = re.compile(r'<h2 id="stay">Where to stay: three sensible ways to do it</h2>.*?(?=<h2 id="day">)', re.S)
        block = '''<h2 id="stay">Where to stay: three different geographies</h2><p><strong>Villefranche</strong> for harbour and old town at the door. <strong>Cap-Ferrat</strong> for a stay where hotel and sea become the destination. <strong>Beaulieu</strong> for a calmer, more rational train-side base.</p><div class="source-box place-stay-boundary" data-phase3-owner="stay"><strong>The destination page chooses the geography, not the room.</strong> <a href="/en/hotels/finder/?base=villefranche">Open Hotel Fit for Villefranche / Cap-Ferrat →</a></div>'''
    text, n = pattern.subn(block, text, count=1)
    if n != 1:
        raise RuntimeError(f"{rel}: Villefranche stay section not found")
    save(rel, text, original)


def cannes_exits(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace('<a href="/hotels/cannes/">Choisir le bon hôtel à Cannes →</a>', '<a href="/hotels/finder/?base=cannes">Choisir le bon hôtel avec Hotel Fit →</a>')
        text = text.replace('Gardez la voiture pour les jours où le rail cesse réellement d’aider.</p>', 'Gardez la voiture pour les jours où le rail cesse réellement d’aider. Pour décider au niveau du séjour, <a href="/fr/planifier/">revenez à Plan</a> ; pour les billets et tarifs, <a href="/pratique/">ouvrez Pratique</a>.</p>')
    else:
        text = text.replace('<a href="/en/hotels/cannes/">Choose the right Cannes hotel →</a>', '<a href="/en/hotels/finder/?base=cannes">Choose the right hotel with Hotel Fit →</a>')
        text = text.replace('Save the car for the days where the railway genuinely stops helping.</p>', 'Save the car for the days where the railway genuinely stops helping. For the trip-level decision, <a href="/plan/">return to Plan</a>; for tickets and fares, <a href="/en/practical/">open Practical</a>.</p>')
    save(rel, text, original)


def update_active_nav_js() -> None:
    for rel in ("assets/site.js","assets/v3.js"):
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        if rel.endswith("site.js"):
            text = text.replace("path.indexOf('/bons-plans/nice-quand-il-pleut/')===0)", "path.indexOf('/bons-plans/nice-quand-il-pleut/')===0 || path.indexOf('/bons-plans/erreurs-riviera/')===0)")
            text = text.replace("path.indexOf('/en/good-finds/nice-in-the-rain/')===0)", "path.indexOf('/en/good-finds/nice-in-the-rain/')===0 || path.indexOf('/en/good-finds/riviera-mistakes/')===0)")
        else:
            text = text.replace('path.indexOf("/bons-plans/nice-quand-il-pleut/") === 0)', 'path.indexOf("/bons-plans/nice-quand-il-pleut/") === 0 || path.indexOf("/bons-plans/erreurs-riviera/") === 0)')
            text = text.replace('path.indexOf("/en/good-finds/nice-in-the-rain/") === 0)', 'path.indexOf("/en/good-finds/nice-in-the-rain/") === 0 || path.indexOf("/en/good-finds/riviera-mistakes/") === 0)')
        save(rel, text, original)


def css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 phase 3 content ownership 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 phase 3 content ownership 2026-09-25 */
.ownership-note{margin:22px 0;padding:17px 19px;border-left:3px solid var(--blue);background:rgba(23,54,95,.045);color:var(--ink-soft);font-size:12px;line-height:1.65}
.ownership-note strong{color:var(--ink)}
.ownership-note a,.place-stay-boundary a{font-weight:700;text-decoration:underline;text-underline-offset:3px}
.ownership-note--split{border-left-color:var(--coral)}
.place-stay-boundary{margin:18px 0 22px}
.phase3-hotel-fit{margin-top:28px}
.right-now-clean .grid{grid-template-columns:repeat(2,minmax(0,1fr));max-width:900px}
.right-now-practical-card{background:rgba(23,54,95,.035)}
@media(max-width:720px){.right-now-clean .grid{grid-template-columns:1fr}}
'''
    save("assets/v3.css", text, original)


def validate() -> None:
    errors = []
    checks = {
        "en/good-finds/index.html": ("RIGHT NOW", "/en/practical/", "September 2026"),
        "bons-plans/index.html": ("EN CE MOMENT", "/pratique/", "Septembre 2026"),
        "en/hotels/without-a-car/index.html": ('data-phase3-owner="carfree"', "/plan/", "/en/practical/", "phase3-hotel-fit"),
        "hotels/sans-voiture/index.html": ('data-phase3-owner="carfree"', "/fr/planifier/", "/pratique/", "phase3-hotel-fit"),
        "en/riviera-guide/nice/index.html": ("This section chooses the neighbourhood, not the hotel.", "/en/hotels/finder/?base=nice", "Practical airport guide"),
        "riviera-guide/nice/index.html": ("Ici, on choisit le quartier, pas l’hôtel.", "/hotels/finder/?base=nice", "guide Pratique aéroport"),
        "en/riviera-guide/antibes/index.html": ("Places stops at the area choice.", "/en/hotels/finder/?base=antibes"),
        "riviera-guide/antibes/index.html": ("On s’arrête au choix de zone.", "/hotels/finder/?base=antibes"),
        "en/riviera-guide/villefranche-cap-ferrat/index.html": ("three different geographies", "/en/hotels/finder/?base=villefranche"),
        "riviera-guide/villefranche-cap-ferrat/index.html": ("trois géographies différentes", "/hotels/finder/?base=villefranche"),
        "en/riviera-guide/cannes/index.html": ("/en/hotels/finder/?base=cannes", "/en/practical/"),
        "riviera-guide/cannes/index.html": ("/hotels/finder/?base=cannes", "/pratique/"),
    }
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
    for rel in ("en/riviera-guide/antibes/index.html","riviera-guide/antibes/index.html","en/riviera-guide/villefranche-cap-ferrat/index.html","riviera-guide/villefranche-cap-ferrat/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if '<div class="itinerary-stay-prompt">' in text:
            errors.append(f"{rel}: detailed hotel mini-guide still present")
    for rel in (
        "en/good-finds/nice-airport-transfer/index.html","en/good-finds/train-or-bus/index.html",
        "en/good-finds/what-to-book/index.html","en/good-finds/nice-in-the-rain/index.html",
        "en/good-finds/riviera-mistakes/index.html","bons-plans/transfert-aeroport-nice/index.html",
        "bons-plans/train-ou-bus/index.html","bons-plans/que-reserver/index.html",
        "bons-plans/nice-quand-il-pleut/index.html","bons-plans/erreurs-riviera/index.html"
    ):
        if 'data-phase3-owner="practical"' not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel}: Practical ownership note missing")
    if "€10" in (ROOT / "en/riviera-guide/nice/index.html").read_text(encoding="utf-8"):
        errors.append("en/riviera-guide/nice/index.html: live airport fare still duplicated")
    if "10 €" in (ROOT / "riviera-guide/nice/index.html").read_text(encoding="utf-8"):
        errors.append("riviera-guide/nice/index.html: live airport fare still duplicated")
    if errors:
        raise SystemExit("V3 phase 3 reclassification failed:\n- " + "\n- ".join(errors))


def main() -> int:
    right_now_hub("en/good-finds/index.html","en")
    right_now_hub("bons-plans/index.html","fr")

    for rel in (
        "en/good-finds/nice-airport-transfer/index.html","en/good-finds/train-or-bus/index.html",
        "en/good-finds/what-to-book/index.html","en/good-finds/nice-in-the-rain/index.html",
        "en/good-finds/riviera-mistakes/index.html"
    ):
        practical_legacy(rel,"en")
    for rel in (
        "bons-plans/transfert-aeroport-nice/index.html","bons-plans/train-ou-bus/index.html",
        "bons-plans/que-reserver/index.html","bons-plans/nice-quand-il-pleut/index.html",
        "bons-plans/erreurs-riviera/index.html"
    ):
        practical_legacy(rel,"fr")

    car_free_stay("en/hotels/without-a-car/index.html","en")
    car_free_stay("hotels/sans-voiture/index.html","fr")

    nice_places("en/riviera-guide/nice/index.html","en")
    nice_places("riviera-guide/nice/index.html","fr")
    compact_antibes_hotels("en/riviera-guide/antibes/index.html","en")
    compact_antibes_hotels("riviera-guide/antibes/index.html","fr")
    compact_villefranche_hotels("en/riviera-guide/villefranche-cap-ferrat/index.html","en")
    compact_villefranche_hotels("riviera-guide/villefranche-cap-ferrat/index.html","fr")
    cannes_exits("en/riviera-guide/cannes/index.html","en")
    cannes_exits("riviera-guide/cannes/index.html","fr")

    update_active_nav_js()
    css()
    validate()
    print(f"V3 phase 3 reclassification passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
