#!/usr/bin/env python3
from __future__ import annotations
import base64, io, re, tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'data' / 'hotels'
ALLOWED = ('hotels/', 'en/hotels/')
HUBS = {'hotels/index.html', 'en/hotels/index.html'}
HOTEL_CSS = '/assets/hotel-batch.css?v=1.7'
THUMB_BUNDLE = PARTS / 'hotel-thumbs-2026-09-12.tgz.b64'

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


def safe_thumb_member(name: str) -> tuple[bool, str | None]:
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or len(p.parts) != 2:
        return False, None
    slug, filename = p.parts
    if filename != 'batch-thumb.svg' or not re.fullmatch(r'[a-z0-9-]+', slug):
        return False, None
    return True, slug


def decode_bundle_text(text: str) -> bytes:
    """Decode the versioned thumbnail bundle even if it contains wrapping artifacts.

    Older connector writes may have introduced harmless separators around an otherwise
    valid base64 payload. Strip anything outside the standard/url-safe alphabets, then
    try standard base64 first and url-safe base64 as a fallback.
    """
    compact = re.sub(r'[^A-Za-z0-9+/=_-]', '', text)
    compact += '=' * (-len(compact) % 4)
    errors: list[Exception] = []
    for decoder in (base64.b64decode, base64.urlsafe_b64decode):
        try:
            raw = decoder(compact)
            if raw.startswith(b'\x1f\x8b'):
                return raw
        except Exception as exc:
            errors.append(exc)
    raise RuntimeError('Hotel thumbnail bundle is not valid base64/gzip') from (errors[-1] if errors else None)


def materialize_thumbnails() -> int:
    if not THUMB_BUNDLE.is_file():
        raise RuntimeError('Hotel thumbnail bundle is missing from the repository')
    raw = decode_bundle_text(THUMB_BUNDLE.read_text(encoding='ascii'))
    count = 0
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        members = [m for m in archive.getmembers() if m.isfile()]
        if len(members) != 30:
            raise RuntimeError(f'Expected 30 hotel thumbnails, found {len(members)}')
        for member in members:
            ok, slug = safe_thumb_member(member.name)
            if not ok or slug is None:
                raise RuntimeError(f'Unexpected thumbnail path: {member.name}')
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f'Cannot read thumbnail: {member.name}')
            data = source.read()
            if b'<svg' not in data[:200] or b'data:image/webp;base64,' not in data:
                raise RuntimeError(f'Invalid hotel thumbnail SVG: {member.name}')
            target = ROOT / 'assets' / 'hotels' / slug / 'batch-thumb.svg'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            count += 1
    print(f'Materialized {count} individual hotel thumbnails')
    return count


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

    hub_pattern = re.compile(
        r'<span class="batch-thumb" role="img" aria-label="([^"]*)"(?: style="[^"]*")?></span>'
    )

    def hub_replacement(match: re.Match[str]) -> str:
        label = match.group(1)
        slug = HUB_LABEL_TO_SLUG.get(label)
        if slug is None:
            raise RuntimeError(f'{name}: unknown hotel hub thumbnail label: {label}')
        return (
            f'<img alt="{label}" loading="lazy" '
            f'src="/assets/hotels/{slug}/batch-thumb.svg">'
        )

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
    if '<span class="batch-thumb"' in normalized:
        raise RuntimeError(f'{name}: obsolete sprite span still present')

    for slug in re.findall(r'src="/assets/hotels/([^/]+)/batch-thumb\.svg"', text):
        target = ROOT / 'assets' / 'hotels' / slug / 'batch-thumb.svg'
        if not target.is_file():
            raise RuntimeError(f'{name}: missing thumbnail asset for {slug}')

    return text.encode('utf-8')


def main() -> int:
    materialize_thumbnails()

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
