#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = '/assets/activity-affiliates.css?v=1'

LINKS = {
    'nice_walk': 'https://www.getyourguide.com/nice-l314/nice-old-town-castle-hill-informative-guided-walking-tour-t421076/?partner_id=CEAKUVS&utm_medium=online_publisher',
    'eze_monaco': 'https://www.getyourguide.com/nice-l314/from-nice-eze-monaco-monte-carlo-half-day-trip-t197245/?partner_id=CEAKUVS&utm_medium=online_publisher',
    'west': 'https://www.getyourguide.com/cannes-l15/from-nice-cannes-antibes-saint-paul-de-vence-tour-t5969/?partner_id=CEAKUVS&utm_medium=online_publisher',
    'boat': 'https://www.getyourguide.com/nice-l314/nice-1-hour-sightseeing-cruise-to-villefranche-bay-t33840/?partner_id=CEAKUVS&utm_medium=online_publisher',
    'st_tropez': 'https://www.getyourguide.com/nice-l314/nice-saint-tropez-return-transfer-by-boat-t34024/?partner_id=CEAKUVS&utm_medium=online_publisher',
}


def html_url(url: str) -> str:
    return url.replace('&', '&amp;')


def cta(url: str, label: str, slot: str) -> str:
    return (
        f'<a class="mametas-activity-cta" href="{html_url(url)}" target="_blank" '
        f'rel="sponsored noopener noreferrer" data-affiliate-provider="getyourguide" '
        f'data-affiliate-slot="{slot}">{label}</a>'
    )


NICE_FR = f'''<aside class="mametas-activity-inline" data-mametas-activity-block="nice-walk">
<img src="/assets/editorial/activity-nice-castle-hill.avif" alt="Nice et la Baie des Anges" loading="lazy"/>
<div class="mametas-activity-copy"><p class="mametas-activity-kicker">ACTIVITÉ · PREMIER JOUR</p><h3>Vieux-Nice + Colline du Château, avec un guide</h3>
<p><strong>Verdict Mametas.</strong> Nice se visite très bien sans guide. Mais si vous voulez comprendre la ville au lieu d’aligner des photos dès le premier matin, cette visite à pied est une option qui a du sens.</p>
<p><strong>Pour qui.</strong> Premier séjour court, envie de contexte, Vieux-Nice et Colline du Château déjà au programme.</p>
<p class="mametas-catch"><strong>Mèfi.</strong> Vous ne payez pas pour accéder au quartier ou à la colline : vous payez pour le commentaire et le fil conducteur. Nuance utile.</p>
{cta(LINKS['nice_walk'], 'Voir les disponibilités sur GetYourGuide', 'nice-old-town-castle-hill')}
<p class="mametas-affiliate-disclosure">Lien affilié GetYourGuide : Mametas peut recevoir une commission si vous réservez via ce lien. La sélection reste éditoriale.</p></div></aside>'''

NICE_EN = f'''<aside class="mametas-activity-inline" data-mametas-activity-block="nice-walk">
<img src="/assets/editorial/activity-nice-castle-hill.avif" alt="Nice and the Baie des Anges" loading="lazy"/>
<div class="mametas-activity-copy"><p class="mametas-activity-kicker">ACTIVITY · FIRST DAY</p><h3>Old Nice + Castle Hill, with a guide</h3>
<p><strong>Mametas verdict.</strong> Nice is perfectly walkable without a guide. But if you want context rather than a sequence of photo stops on your first morning, this walking tour makes sense.</p>
<p><strong>For.</strong> A short first stay, people who want context, and anyone already planning Old Nice and Castle Hill.</p>
<p class="mametas-catch"><strong>The catch.</strong> You are not paying for access to the old town or the hill. You are paying for the commentary and a coherent route. Useful distinction.</p>
{cta(LINKS['nice_walk'], 'Check availability on GetYourGuide', 'nice-old-town-castle-hill')}
<p class="mametas-affiliate-disclosure">GetYourGuide affiliate link: Mametas may receive a commission if you book through this link. The selection remains editorial.</p></div></aside>'''


def card(image: str, alt: str, kicker: str, title: str, verdict: str, audience: str, catch: str, url: str, label: str, slot: str) -> str:
    return f'''<article class="mametas-activity-card"><img src="{image}" alt="{alt}" loading="lazy"/><div class="mametas-activity-copy"><p class="mametas-activity-kicker">{kicker}</p><h3>{title}</h3><p><strong>{'Verdict Mametas.' if label.startswith('Voir') else 'Mametas verdict.'}</strong> {verdict}</p><p><strong>{'Pour qui.' if label.startswith('Voir') else 'For.'}</strong> {audience}</p><p class="mametas-catch"><strong>{'Mèfi.' if label.startswith('Voir') else 'The catch.'}</strong> {catch}</p>{cta(url, label, slot)}</div></article>'''


DAY_FR = f'''<section class="mametas-activities" data-mametas-activity-block="day-trips-curated"><div class="mametas-activities-head"><p class="eyebrow">ACTIVITÉS QUE NOUS RÉSERVERIONS</p><h2>Quand payer quelqu’un pour la logistique a du sens.</h2><p>La plupart des journées sur la Riviera n’ont pas besoin d’un tour organisé. Celles-ci peuvent en revanche vous éviter de transformer les vacances en exercice de correspondances.</p></div><div class="mametas-activity-grid">
{card('/assets/editorial/activity-eze-monaco.avif','Èze au-dessus de la Méditerranée','EST · SANS VOITURE','Èze + Monaco + Monte-Carlo','Bon usage d’une excursion organisée : deux étapes très différentes, sans passer la journée à résoudre la logistique.','Premier séjour court, sans voiture, avec Èze et Monaco réellement prioritaires.','Vous échangez de la liberté contre de l’efficacité. Si vous aimez traîner deux heures de plus à Èze, gardez plutôt la journée pour vous.',LINKS['eze_monaco'],'Voir les disponibilités sur GetYourGuide','eze-monaco')}
{card('/assets/editorial/activity-cannes-antibes-saint-paul.avif','Antibes et la Méditerranée','OUEST · APERÇU','Cannes + Antibes + Saint-Paul-de-Vence','Nous vous disons d’habitude d’en faire moins. Ici, l’intérêt est précisément de laisser quelqu’un d’autre gérer les liaisons si vous tenez à voir les trois.','Voyage court, première lecture de l’ouest de la Riviera, sans envie de conduire.','Trois lieux dans une journée restent trois aperçus. Ne confondez pas efficacité et lenteur méditerranéenne.',LINKS['west'],'Voir les disponibilités sur GetYourGuide','cannes-antibes-saint-paul')}
{card('/assets/editorial/activity-villefranche-cap-ferrat-boat.avif','Cap-Ferrat et la côte vus depuis la mer','MER · FACILE','Nice + baie de Villefranche en bateau','Une heure sur l’eau peut apporter plus à la journée qu’une heure supplémentaire dans un bus. Format court, côte vue autrement, puis vous reprenez votre programme.','Ceux qui veulent une vraie parenthèse en mer sans sacrifier une demi-journée.','C’est une croisière panoramique, pas une journée plage ni une grande expédition nautique. Gardez les attentes à la bonne taille.',LINKS['boat'],'Voir les disponibilités sur GetYourGuide','nice-villefranche-boat')}
{card('/assets/editorial/activity-saint-tropez-boat.avif','Saint-Tropez sur la Côte d’Azur','MER · JOURNÉE DÉDIÉE','Saint-Tropez depuis Nice, par bateau','Depuis Nice et sans voiture, le bateau est la version de l’excursion à Saint-Tropez que nous défendons le plus facilement. La côte fait enfin partie du trajet.','Ceux qui veulent vraiment Saint-Tropez et acceptent de lui donner une journée entière.','Saint-Tropez n’est toujours pas à côté de Nice parce que la carte paraît petite. Faites-en le programme du jour, pas un arrêt entre deux autres idées.',LINKS['st_tropez'],'Voir les disponibilités sur GetYourGuide','nice-saint-tropez-boat')}
</div><p class="mametas-affiliate-disclosure">Liens affiliés GetYourGuide : Mametas peut recevoir une commission si vous réservez via ces liens. Nous ne listons pas tout ; seulement les activités qui ont une place claire dans un premier séjour.</p></section>'''

DAY_EN = f'''<section class="mametas-activities" data-mametas-activity-block="day-trips-curated"><div class="mametas-activities-head"><p class="eyebrow">ACTIVITIES WE WOULD ACTUALLY BOOK</p><h2>When paying someone else to handle the logistics makes sense.</h2><p>Most Riviera days do not need an organised tour. These are the cases where outsourcing the choreography can stop the holiday becoming a connections exercise.</p></div><div class="mametas-activity-grid">
{card('/assets/editorial/activity-eze-monaco.avif','Èze above the Mediterranean','EAST · NO CAR','Èze + Monaco + Monte-Carlo','A sensible use of an organised excursion: two very different stops without spending the day solving the logistics.','A short first trip, no car, with Èze and Monaco genuinely high on the list.','You trade freedom for efficiency. If you like lingering two hours longer in Èze, keep the day in your own hands.',LINKS['eze_monaco'],'Check availability on GetYourGuide','eze-monaco')}
{card('/assets/editorial/activity-cannes-antibes-saint-paul.avif','Antibes and the Mediterranean','WEST · OVERVIEW','Cannes + Antibes + Saint-Paul-de-Vence','We usually tell you to do less. Here, the point is to let somebody else handle the links if you insist on seeing all three.','A short trip, a first look west, and no desire to drive.','Three places in one day are still three samples. Efficiency is not the same thing as Mediterranean slowness.',LINKS['west'],'Check availability on GetYourGuide','cannes-antibes-saint-paul')}
{card('/assets/editorial/activity-villefranche-cap-ferrat-boat.avif','Cap-Ferrat and the Riviera coastline from above','SEA · EASY','Nice + Villefranche Bay by boat','An hour on the water can add more to the day than another hour on a bus. Short format, a different view of the coast, then back to your own plans.','Anyone who wants a proper sea interlude without surrendering half the day.','This is a sightseeing cruise, not a beach day or a grand boating expedition. Keep the expectations the same size as the format.',LINKS['boat'],'Check availability on GetYourGuide','nice-villefranche-boat')}
{card('/assets/editorial/activity-saint-tropez-boat.avif','Saint-Tropez on the French Riviera','SEA · DEDICATED DAY','Saint-Tropez from Nice, by boat','From Nice without a car, the boat is the version of a Saint-Tropez day trip we can defend most easily. At least the coast becomes part of the journey.','Travellers who really want Saint-Tropez and are willing to give it the whole day.','Saint-Tropez is still not next door to Nice because the map looks small. Make it the day, not a stop between two other ideas.',LINKS['st_tropez'],'Check availability on GetYourGuide','nice-saint-tropez-boat')}
</div><p class="mametas-affiliate-disclosure">GetYourGuide affiliate links: Mametas may receive a commission if you book through these links. We do not list everything; only activities with a clear role in a first trip.</p></section>'''


def ensure_css(text: str) -> str:
    if '/assets/activity-affiliates.css' in text:
        return text
    return text.replace('</head>', f'<link rel="stylesheet" href="{CSS}"/></head>', 1)


def inject_after_heading_div(text: str, heading: str, block: str) -> str:
    if 'data-mametas-activity-block="nice-walk"' in text:
        return text
    idx = text.find(heading)
    if idx < 0:
        raise RuntimeError(f'Could not locate activity anchor: {heading}')
    end = text.find('</div>', idx)
    if end < 0:
        raise RuntimeError(f'Could not close activity anchor: {heading}')
    end += len('</div>')
    return text[:end] + block + text[end:]


def inject_before_main_close(text: str, block: str) -> str:
    if 'data-mametas-activity-block="day-trips-curated"' in text:
        return text
    idx = text.rfind('</main>')
    if idx < 0:
        raise RuntimeError('Could not locate </main>')
    return text[:idx] + block + text[idx:]


def patch(path_rel: str, kind: str, lang: str) -> None:
    path = ROOT / path_rel
    text = path.read_text(encoding='utf-8')
    text = ensure_css(text)
    if kind == 'nice':
        text = inject_after_heading_div(
            text,
            '<h3>Monter à la Colline du Château</h3>' if lang == 'fr' else '<h3>Castle Hill</h3>',
            NICE_FR if lang == 'fr' else NICE_EN,
        )
    else:
        text = inject_before_main_close(text, DAY_FR if lang == 'fr' else DAY_EN)
    path.write_text(text, encoding='utf-8')
    print(f'GetYourGuide activity merchandising applied to {path_rel}')


def main() -> int:
    patch('riviera-guide/nice/index.html', 'nice', 'fr')
    patch('en/riviera-guide/nice/index.html', 'nice', 'en')
    patch('escapades/index.html', 'day', 'fr')
    patch('en/day-trips/index.html', 'day', 'en')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
