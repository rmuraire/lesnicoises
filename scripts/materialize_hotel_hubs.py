#!/usr/bin/env python3
from __future__ import annotations
import base64, io, re, tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'data' / 'hotels'
ALLOWED = ('hotels/', 'en/hotels/')
HUBS = {'hotels/index.html', 'en/hotels/index.html'}
HOTEL_CSS = '/assets/hotel-batch.css?v=1.6'

# 6 columns x 5 rows. Coordinates were verified against the 30 source thumbnails.
SPRITE_POSITIONS = {
    'domaine-du-mas-de-pierre': (0, 0),
    'five-seas-cannes': (1, 0),
    'grand-hotel-du-cap-ferrat': (2, 0),
    'hotel-belles-rives': (3, 0),
    'hotel-comte-de-nice-beaulieu': (4, 0),
    'hotel-de-letoile-antibes': (5, 0),
    'hotel-de-provence-cannes': (0, 1),
    'hotel-frisia': (1, 1),
    'hotel-hermitage-monte-carlo': (2, 1),
    'hotel-juana': (3, 1),
    'hotel-le-sud': (4, 1),
    'hotel-les-messugues': (5, 1),
    'hotel-verlaine-cannes': (0, 2),
    'hotel-victoria-roquebrune': (1, 2),
    'ibis-roquebrune-cap-martin': (2, 2),
    'ibis-styles-beaulieu': (3, 2),
    'kube-saint-tropez': (4, 2),
    'la-ferme-daugustin': (5, 2),
    'la-grande-bastide': (0, 3),
    'la-ponche-saint-tropez': (1, 3),
    'la-romarine': (2, 3),
    'le-mas-candille': (3, 3),
    'le-saint-paul': (4, 3),
    'les-bastides-saint-paul': (5, 3),
    'les-palmiers-sainte-maxime': (0, 4),
    'monte-carlo-bay': (1, 4),
    'sezz-saint-tropez': (2, 4),
    'toile-blanche': (3, 4),
    'villa-marie-saint-tropez': (4, 4),
    'villa-sophia-mougins': (5, 4),
}

HUB_LABEL_TO_SLUG = {
    'Hôtel Belles Rives': 'hotel-belles-rives',
    'Five Seas Hotel Cannes': 'five-seas-cannes',
    'Grand-Hôtel du Cap-Ferrat, A Four Seasons Hotel': 'grand-hotel-du-cap-ferrat',
    'Hôtel Hermitage Monte-Carlo': 'hotel-hermitage-monte-carlo',
    'Le Domaine du Mas de Pierre': 'domaine-du-mas-de-pierre',
    'Hôtel La Ponche': 'la-ponche-saint-tropez',
}


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts:
        return False
    return any(name.startswith(prefix) for prefix in ALLOWED)


def ensure_real_jpeg(sprite: Path) -> None:
    data = sprite.read_bytes()
    if data.startswith(b'\xff\xd8\xff'):
        return
    try:
        raw = base64.b64decode(b''.join(data.split()), validate=True)
    except Exception as exc:
        raise RuntimeError('Hotel sprite is neither JPEG bytes nor valid base64 text') from exc
    if not raw.startswith(b'\xff\xd8\xff') or not raw.endswith(b'\xff\xd9'):
        raise RuntimeError('Decoded hotel sprite is not a valid JPEG stream')
    sprite.write_bytes(raw)
    print(f'Decoded hotel sprite to binary JPEG ({len(raw)} bytes)')


def sprite_markup(slug: str, label: str) -> str:
    if slug not in SPRITE_POSITIONS:
        raise RuntimeError(f'Unknown hotel sprite slug: {slug}')
    col, row = SPRITE_POSITIONS[slug]
    x = col * 20
    y = row * 25
    return (
        f'<span class="batch-thumb" role="img" aria-label="{label}" '
        f'style="background-position:{x}% {y}%"></span>'
    )


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

    text = text.replace(
        'href="/hotels/hotel-de-paris-monte-carlo/"',
        'href="/hotels/monaco/hotel-de-paris-monte-carlo/"',
    )

    if '/assets/hotel-batch.css' in text:
        text = re.sub(r'/assets/hotel-batch\.css\?v=[^"\']+', HOTEL_CSS, text)
    else:
        text = text.replace('</head>', f'<link href="{HOTEL_CSS}" rel="stylesheet"></head>', 1)

    thumb_pattern = re.compile(
        r'<img\s+alt="([^"]*)"\s+loading="lazy"\s+src="/assets/hotels/([^/]+)/batch-thumb\.svg"\s*/?>'
    )

    def thumb_replacement(match: re.Match[str]) -> str:
        label, slug = match.groups()
        return sprite_markup(slug, label)

    text = thumb_pattern.sub(thumb_replacement, text)

    hub_pattern = re.compile(
        r'<span class="batch-thumb" role="img" aria-label="([^"]*)"(?: style="[^"]*")?></span>'
    )

    def hub_replacement(match: re.Match[str]) -> str:
        label = match.group(1)
        slug = HUB_LABEL_TO_SLUG.get(label)
        if slug is None:
            return match.group(0)
        return sprite_markup(slug, label)

    text = hub_pattern.sub(hub_replacement, text)

    if name in HUBS and 'practical-title-above' not in text:
        pattern = re.compile(
            r'<div class="practical-grid">\s*<div class="practical-title">(.*?)</div>(?=<a class="practical-link")',
            re.S,
        )
        text, replaced = pattern.subn(
            r'<div class="practical-title practical-title-above">\1</div><div class="practical-grid practical-grid-ten">',
            text,
            count=1,
        )
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
        raise RuntimeError(f'{name}: legacy batch thumbnail reference still present')
    if 'batch-thumb>img' in normalized:
        raise RuntimeError(f'{name}: obsolete inline sprite image markup still present')
    return text.encode('utf-8')


def main() -> int:
    sprite = ROOT / 'assets' / 'hotels' / 'batch-sprite.jpg'
    if not sprite.is_file():
        raise RuntimeError('Hotel sprite JPG is missing from the repository')
    ensure_real_jpeg(sprite)

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
    print(f'Materialized {len(members)} hotel hub pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
