#!/usr/bin/env python3
"""Preserve the September 16 Astra UX decision paths after legacy materializers run.

This pass is intentionally narrow: no redesign, no new architecture. It prevents older
materializers from reintroducing competing next-decision blocks and keeps the 3/5/7-day
itinerary useful in both languages.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> tuple[Path, str]:
    path = ROOT / rel
    return path, path.read_text()


def write(path: Path, text: str) -> None:
    path.write_text(text)


def remove_legacy_trip_length(text: str) -> str:
    return re.sub(
        r'<div id="mametas-trip-length-edit" class="verdict-box" data-static-editorial="true">.*?</div>',
        '',
        text,
        count=1,
        flags=re.S,
    )


def replace_between(text: str, start_id: str, end_pattern: str, replacement: str, label: str) -> str:
    pattern = rf'<h2 id="{re.escape(start_id)}">.*?(?={end_pattern})'
    text, count = re.subn(pattern, replacement + '\n        ', text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f'Could not replace {label}')
    return text


def fix_nice_next_decision(rel: str, fr: bool = False) -> None:
    path, text = read(rel)
    if not fr:
        manual = (
            '<div class="verdict"><span class="label">YOUR NEXT DECISION</span>'
            '<p><strong>Nice it is. Have you sorted your hotel?</strong></p>'
            '<p><a href="/stay/nice/">Not yet — choose the right Nice base →</a><br/>'
            '<a href="/plan/five-days-nice-no-car/#make-it-five">Already booked — build the trip around it →</a></p></div>\n'
        )
        text = text.replace(manual, '', 1)
        label = 'YOUR NEXT DECISION'
        question = 'Nice it is. Have you sorted your hotel?'
        first_href = '/stay/nice/'
        first_label = 'Not yet — choose the right Nice base'
        second_href = '/plan/five-days-nice-no-car/#make-it-five'
        second_label = 'Already booked — build the trip around it'
    else:
        label = 'LA PROCHAINE DÉCISION'
        question = 'Nice, c’est décidé. Votre hôtel est réglé ?'
        first_href = '/fr/dormir/nice/'
        first_label = 'Pas encore — choisir le bon hôtel à Nice'
        second_href = '/fr/planifier/cinq-jours-nice-sans-voiture/#version-cinq'
        second_label = 'Déjà réservé — construire le séjour autour'

    replacement = (
        f'<div id="mametas-next-decision" class="verdict" data-static-editorial="true">'
        f'<span class="label">{label}</span>'
        f'<p><strong>{question}</strong></p>'
        f'<p><a href="{first_href}">{first_label} →</a><br>'
        f'<a href="{second_href}">{second_label} →</a></p></div>'
    )
    text, count = re.subn(
        r'<div id="mametas-next-decision" class="verdict" data-static-editorial="true">.*?</div>',
        replacement,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f'Could not replace Nice next-decision block in {rel}')
    write(path, text)


def fix_english_plan() -> None:
    path, text = read('plan/five-days-nice-no-car/index.html')
    text = remove_legacy_trip_length(text)
    booking = '''<h2 id="book-ahead">Book ahead: the short checklist</h2>
          <p>Reserve the things whose absence would genuinely damage the trip. For this route, that means the hotel first and only the timed experience you actually care about.</p>
          <h3>Two practical hotel fits</h3>
          <div class="itinerary-stay-prompt">
            <a href="https://expedia.com/affiliates/nice-hotels-hotel-66.6jm7Q6e" rel="sponsored nofollow noopener" target="_blank"><span>Practical pick</span><strong>Hotel 66 Nice</strong><small>Station-friendly and built for easy departures.</small></a>
            <a href="https://expedia.com/affiliates/nice-hotels-hotel-nice-cote-dazur.sQEIXGB" rel="sponsored nofollow noopener" target="_blank"><span>Compact &amp; central</span><strong>Boutique Hôtel Nice Côte d’Azur</strong><small>Good geography with less hotel theatre.</small></a>
          </div>
          <div class="verdict-box"><span>4–8 weeks before</span><p><strong>Hotel:</strong> lock in the base you actually want. <strong>Signature dinners:</strong> reserve one or two only if missing them would annoy you. Do not turn the rest of the week into an appointment calendar.</p></div>
          <div class="verdict-box"><span>1–2 weeks before</span><p>If the Oceanographic Museum defines your Monaco day, <a href="https://billetterie-oceano.tickeasy.com/en-GB/products" rel="nofollow noopener" target="_blank">check official museum tickets →</a> Recheck opening days for any other timed visit that genuinely anchors a day.</p></div>
          <div class="verdict-box"><span>24–48 hours before</span><p>Check official rail and bus planners, weather and disruption. Ordinary coastal train journeys belong to the flexible layer.</p></div>
          <div class="verdict-box"><span>Keep spontaneous</span><p>Most lunches, one half-day, the exact order of weather-sensitive days and the decision to stop for a swim instead of collecting another landmark.</p></div>'''
    text = replace_between(
        text,
        'book-ahead',
        r'<h2 id="make-it-three">',
        booking,
        'English booking section',
    )
    write(path, text)


def fix_french_plan() -> None:
    path, text = read('fr/planifier/cinq-jours-nice-sans-voiture/index.html')
    text = remove_legacy_trip_length(text)

    if 'data-astra-duration="true"' not in text:
        chooser = (
            '<div class="source-box" data-astra-duration="true"><strong>Vous restez combien de temps ?</strong> '
            '<a href="#version-trois">3 jours</a> · <a href="#version-cinq">5 jours</a> · '
            '<a href="#version-sept">7 jours</a>. Même base, ambition différente.</div>\n'
        )
        text = text.replace('<h2 id="avant-arrivee">', chooser + '<h2 id="avant-arrivee">', 1)

    if 'id="version-cinq"' not in text:
        five = (
            '<h2 id="version-cinq">Cinq jours : gardez tout le contraste.</h2>'
            '<p>Utilisez le parcours complet ci-dessous. Nice reste une vraie base, puis chaque journée change de direction et d’ambiance au lieu d’additionner les villes voisines.</p>\n'
        )
        text = text.replace('<div class="day-card" id="jour-un">', five + '<div class="day-card" id="jour-un">', 1)

    booking = '''<h2 id="reservations">Réserver à l’avance : la check-list courte</h2>
        <p>Bloquez ce dont l’absence gâcherait vraiment le séjour. Pour ce parcours, l’hôtel d’abord, puis seulement les expériences à créneau qui comptent réellement.</p>
        <h3>Deux hôtels pratiques pour ce parcours</h3>
        <div class="itinerary-stay-prompt">
          <a href="https://expedia.com/affiliates/nice-hotels-hotel-66.6jm7Q6e" rel="sponsored nofollow noopener" target="_blank"><span>Choix pratique</span><strong>Hotel 66 Nice</strong><small>Près de la gare et pensé pour des départs faciles.</small></a>
          <a href="https://expedia.com/affiliates/nice-hotels-hotel-nice-cote-dazur.sQEIXGB" rel="sponsored nofollow noopener" target="_blank"><span>Compact &amp; central</span><strong>Boutique Hôtel Nice Côte d’Azur</strong><small>Bonne géographie, moins de théâtre hôtelier.</small></a>
        </div>
        <div class="verdict-box"><span>4 à 8 semaines avant</span><p><strong>Hôtel :</strong> bloquez la base que vous voulez réellement. <strong>Dîners signature :</strong> réservez-en un ou deux seulement si vous regretteriez vraiment de les manquer. Le reste du séjour n’a pas besoin de devenir un calendrier de rendez-vous.</p></div>
        <div class="verdict-box"><span>1 à 2 semaines avant</span><p>Si le Musée océanographique définit votre journée à Monaco, <a href="https://billetterie-oceano.tickeasy.com/fr-FR/produits" rel="nofollow noopener" target="_blank">voir la billetterie officielle →</a> Revérifiez aussi les jours d’ouverture des autres visites à créneau qui structurent réellement une journée.</p></div>
        <div class="verdict-box"><span>24 à 48 h avant</span><p>Vérifiez les calculateurs officiels train/bus, la météo et les perturbations. Les trajets côtiers ordinaires restent dans la couche flexible.</p></div>
        <div class="verdict-box"><span>À garder spontané</span><p>La plupart des déjeuners, une demi-journée, l’ordre exact des journées sensibles à la météo et le droit de choisir une baignade plutôt qu’un monument supplémentaire.</p></div>'''
    text = replace_between(
        text,
        'reservations',
        r'<h2 id="version-trois">',
        booking,
        'French booking section',
    )

    three = '''<h2 id="version-trois">Trois jours. Voilà ce qui reste.</h2>
        <p>Coupez, ne compressez pas. Gardez Nice, choisissez une seule journée à l’est, puis Antibes comme contrepoint à l’ouest. Vous perdez de l’étendue, pas la logique du voyage.</p>
        <div class="day-card"><span class="day">Jour 1</span><h3>Nice</h3><p>Vieux-Nice, la mer et assez de temps pour comprendre la base au lieu de la traiter comme une gare avec des restaurants.</p><p><a class="inline-decision-link" href="/riviera-guide/nice/">Utiliser le guide de Nice →</a></p></div>
        <div class="day-card"><span class="day">Jour 2</span><h3>Choisissez une journée à l’est</h3><p><a href="/riviera-guide/villefranche-cap-ferrat/">Villefranche / Cap-Ferrat</a> pour la beauté et le rythme lent, ou <a href="/riviera-guide/monaco/">Monaco / Menton</a> pour davantage de contraste. Pas les deux.</p></div>
        <div class="day-card"><span class="day">Jour 3</span><h3>Antibes</h3><p>Vieille ville, remparts et changement d’ambiance à l’ouest sans passer la journée dans les transports.</p><p><a class="inline-decision-link" href="/riviera-guide/antibes/">Utiliser le guide d’Antibes →</a></p></div>
        <p><strong>Le compromis :</strong> Èze et la deuxième journée à l’est disparaissent. C’est volontaire. Trois jours doivent sembler édités, pas pressés.</p>
        <p><a class="inline-decision-link" href="/fr/dormir/nice/#pratique">Choisir un hôtel pour ces trois jours →</a></p>'''
    text = replace_between(
        text,
        'version-trois',
        r'<h2 id="version-sept">',
        three,
        'French 3-day section',
    )

    seven = '''<h2 id="version-sept">Sept jours. Ajoutez de l’air, pas des cases.</h2>
        <p>Gardez les cinq journées complètes. Les deux jours supplémentaires servent à ralentir et à ajouter une seule direction vraiment différente, pas à doubler le nombre d’épingles sur la carte.</p>
        <div class="day-card"><span class="day">Jour 6</span><h3>Nice sans objectif</h3><p>Musée, marché, plage, quartier laissé de côté et dîner sans tableau des départs.</p><p><a class="inline-decision-link" href="/riviera-guide/nice/">Revenir à Nice sans checklist →</a></p></div>
        <div class="day-card"><span class="day">Jour 7</span><h3>Choisissez une direction supplémentaire</h3><p><a href="/riviera-guide/cannes/">Cannes</a> pour la Croisette, les palaces et un TER très simple ; <a href="/riviera-guide/saint-paul-de-vence/">Saint-Paul-de-Vence</a> pour un contraste intérieur. Une seule suffit.</p></div>
        <p><strong>Le compromis :</strong> sept jours donnent de la respiration. Une deuxième base devient possible, mais Nice fonctionne toujours ; ne créez pas un problème de valise simplement parce que le calendrier s’allonge.</p>'''
    text = replace_between(
        text,
        'version-sept',
        r'<div class="source-box"><strong>Vérifications officielles',
        seven,
        'French 7-day section',
    )

    if 'data-astra-hotel-fork="true"' not in text:
        fork = (
            '<div class="verdict-box" data-astra-hotel-fork="true"><span>Une question utile</span>'
            '<p><strong>Votre hôtel est réglé ?</strong></p>'
            '<p><a class="inline-decision-link" href="/fr/dormir/nice/#pratique">Pas encore — voir la sélection pratique à Nice →</a><br>'
            '<a class="inline-decision-link" href="#reservations">Déjà réservé — vérifier ce qui mérite vraiment une réservation →</a></p></div>\n\n'
        )
        marker = '<div class="source-box"><strong>Vérifications officielles'
        if marker not in text:
            raise SystemExit('Could not place French hotel fork')
        text = text.replace(marker, fork + marker, 1)

    write(path, text)


def main() -> None:
    fix_nice_next_decision('en/riviera-guide/nice/index.html', fr=False)
    fix_nice_next_decision('riviera-guide/nice/index.html', fr=True)
    fix_english_plan()
    fix_french_plan()
    print('Astra UX decision paths applied.')


if __name__ == '__main__':
    main()
