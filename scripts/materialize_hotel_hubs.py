#!/usr/bin/env python3
from __future__ import annotations
import base64, html, io, re, tarfile, unicodedata
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'data' / 'hotels'
ALLOWED = ('hotels/', 'en/hotels/')
HUBS = {'hotels/index.html', 'en/hotels/index.html'}
HOTEL_CSS = '/assets/hotel-batch.css?v=1.8'
SPRITE_PATH = ROOT / 'assets' / 'hotels' / 'batch-sprite.jpg'

HUB_LABEL_TO_SLUG = {
    'Le Saint Paul': 'le-saint-paul', 'Le Domaine du Mas de Pierre': 'domaine-du-mas-de-pierre',
    'Domaine du Mas de Pierre Hôtel Resort & Spa, Relais & Châteaux': 'domaine-du-mas-de-pierre',
    'Toile Blanche': 'toile-blanche', 'Hotel La Grande Bastide': 'la-grande-bastide',
    'Hôtel La Grande Bastide': 'la-grande-bastide', 'Hôtel Les Messugues': 'hotel-les-messugues',
    'Hôtel Les Bastides Saint-Paul': 'les-bastides-saint-paul', 'Hôtel Les Bastides Saint-Paul-de-Vence': 'les-bastides-saint-paul',
    'Hôtel Comté de Nice': 'hotel-comte-de-nice-beaulieu', 'ibis Styles Beaulieu-sur-Mer': 'ibis-styles-beaulieu',
    'Hôtel Frisia': 'hotel-frisia', 'Grand-Hôtel du Cap-Ferrat, A Four Seasons Hotel': 'grand-hotel-du-cap-ferrat',
    'Grand-Hotel du Cap-Ferrat, A Four Seasons Hotel': 'grand-hotel-du-cap-ferrat', 'Hôtel Hermitage Monte-Carlo': 'hotel-hermitage-monte-carlo',
    'Monte-Carlo Bay Hotel & Resort': 'monte-carlo-bay', 'Hôtel Victoria': 'hotel-victoria-roquebrune',
    'Ibis Roquebrune Cap Martin Menton': 'ibis-roquebrune-cap-martin', 'ibis Roquebrune Cap Martin Menton': 'ibis-roquebrune-cap-martin',
    'Hôtel Belles Rives': 'hotel-belles-rives', 'Hotel Juana': 'hotel-juana', 'Hôtel le Sud': 'hotel-le-sud', 'Hôtel Le Sud': 'hotel-le-sud',
    "Hôtel de L'Etoile": 'hotel-de-letoile-antibes', "Hôtel de l'Etoile": 'hotel-de-letoile-antibes',
    'Five Seas Hotel Cannes': 'five-seas-cannes', 'Hotel Verlaine': 'hotel-verlaine-cannes', 'Hôtel de Provence': 'hotel-de-provence-cannes',
    'Le Mas Candille': 'le-mas-candille', 'Hôtel Villa Sophia': 'villa-sophia-mougins',
    'Kube Saint-Tropez Hôtel': 'kube-saint-tropez', 'Kube Saint-Tropez Hotel': 'kube-saint-tropez',
    'Hôtel Villa Marie Saint-Tropez': 'villa-marie-saint-tropez', 'Hotel Sezz Saint-tropez': 'sezz-saint-tropez',
    'Hotel Sezz Saint-Tropez': 'sezz-saint-tropez', 'Hôtel La Ponche': 'la-ponche-saint-tropez',
    'Hôtel La Ponche · Saint Tropez': 'la-ponche-saint-tropez', 'Hotel Les Palmiers': 'les-palmiers-sainte-maxime',
    'Hotel La Romarine': 'la-romarine', "Hôtel La Ferme d'Augustin": 'la-ferme-daugustin',
}

SPRITE_SLUGS = [
    'le-saint-paul', 'domaine-du-mas-de-pierre', 'toile-blanche', 'la-grande-bastide', 'hotel-les-messugues', 'les-bastides-saint-paul',
    'hotel-comte-de-nice-beaulieu', 'ibis-styles-beaulieu', 'hotel-frisia', 'grand-hotel-du-cap-ferrat', 'hotel-hermitage-monte-carlo', 'monte-carlo-bay',
    'hotel-victoria-roquebrune', 'ibis-roquebrune-cap-martin', 'hotel-belles-rives', 'hotel-juana', 'hotel-le-sud', 'hotel-de-letoile-antibes',
    'five-seas-cannes', 'hotel-verlaine-cannes', 'hotel-de-provence-cannes', 'le-mas-candille', 'villa-sophia-mougins', 'kube-saint-tropez',
    'villa-marie-saint-tropez', 'sezz-saint-tropez', 'la-ponche-saint-tropez', 'les-palmiers-sainte-maxime', 'la-romarine', 'la-ferme-daugustin',
]
SPRITE_POSITION = {
    slug: ((i % 6) * 20, (i // 6) * 25)
    for i, slug in enumerate(SPRITE_SLUGS)
}

def normalized_label(value: str) -> str:
    value = html.unescape(value)
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace('&', ' and ')
    value = re.sub(r'[^a-z0-9]+', ' ', value)
    return ' '.join(token for token in value.split() if token != 'hotel')

NORMALIZED_LABEL_TO_SLUG = {normalized_label(label): slug for label, slug in HUB_LABEL_TO_SLUG.items()}

def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return not p.is_absolute() and '..' not in p.parts and any(name.startswith(prefix) for prefix in ALLOWED)

def normalize_html(data: bytes, name: str) -> bytes:
    text = data.decode('utf-8')
    lower = text.lower()
    if lower.count('<title>') > 1:
        body_end = lower.find('</body>')
        if body_end < 0:
            raise RuntimeError(f'{name}: duplicated document without closing body')
        text = text[: body_end + len('</body>')] + '</html>'
    else:
        end = lower.find('</html>')
        if end >= 0:
            text = text[: end + len('</html>')]

    text = text.replace('href="/hotels/hotel-de-paris-monte-carlo/"', 'href="/hotels/monaco/hotel-de-paris-monte-carlo/"')
    if '/assets/hotel-batch.css' in text:
        text = re.sub(r'/assets/hotel-batch\.css\?v=[^"\']+', HOTEL_CSS, text)
    else:
        text = text.replace('</head>', f'<link href="{HOTEL_CSS}" rel="stylesheet"></head>', 1)

    hub_pattern = re.compile(r'<span class="batch-thumb" role="img" aria-label="([^"]*)"(?: style="[^"]*")?></span>')
    def hub_replacement(match: re.Match[str]) -> str:
        raw_label = match.group(1)
        lookup = html.unescape(raw_label)
        slug = HUB_LABEL_TO_SLUG.get(lookup) or NORMALIZED_LABEL_TO_SLUG.get(normalized_label(lookup))
        if slug is None:
            raise RuntimeError(f'{name}: unknown hotel hub thumbnail label: {raw_label}')
        if slug not in SPRITE_POSITION:
            raise RuntimeError(f'{name}: missing HD sprite position for {slug}')
        x, y = SPRITE_POSITION[slug]
        return f'<span class="batch-thumb" role="img" aria-label="{raw_label}" style="background-position:{x}% {y}%"></span>'

    text = hub_pattern.sub(hub_replacement, text)

    if name in HUBS and 'practical-title-above' not in text:
        pattern = re.compile(r'<div class="practical-grid">\s*<div class="practical-title">(.*?)</div>(?=<a class="practical-link")', re.S)
        text, replaced = pattern.subn(r'<div class="practical-title practical-title-above">\1</div><div class="practical-grid practical-grid-ten">', text, count=1)
        if replaced != 1:
            raise RuntimeError(f'{name}: could not move practical title above ten-base grid')

    normalized = text.lower()
    if normalized.count('<title>') != 1:
        raise RuntimeError(f'{name}: expected one title after normalization')
    if normalized.count('<h1') != 1:
        raise RuntimeError(f'{name}: expected one h1 after normalization')
    if normalized.count('rel="canonical"') != 1:
        raise RuntimeError(f'{name}: expected one canonical after normalization')
    if 'batch-thumb.svg' in normalized:
        raise RuntimeError(f'{name}: legacy low-resolution thumbnail still present')
    if 'batch-thumb' in normalized and not SPRITE_PATH.is_file():
        raise RuntimeError(f'{name}: HD sprite asset is missing')
    return text.encode('utf-8')

def main() -> int:
    if not SPRITE_PATH.is_file():
        raise RuntimeError('HD hotel sprite is missing')
    part_files = sorted(PARTS.glob('hotel-hubs-2026-09-12.tgz.b64.part*'))
    if not part_files:
        raise RuntimeError('Hotel hub payload parts not found')
    encoded = ''.join(p.read_text(encoding='ascii') for p in part_files)
    raw = base64.b64decode(encoded, validate=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        members = [m for m in archive.getmembers() if m.isfile()]
        bad = [m.name for m in members if not safe_member(m.name)]
        if bad:
            raise RuntimeError(f'Unexpected hotel hub payload paths: {bad}')
        for member in members:
            target = ROOT / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f'Cannot read payload member: {member.name}')
            data = source.read()
            if member.name.endswith('.html'):
                data = normalize_html(data, member.name)
            target.write_bytes(data)
            print(f'Materialized {member.name}')
    print(f'Materialized {len(members)} hotel hub pages with HD sprite thumbnails')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
