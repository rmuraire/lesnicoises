#!/usr/bin/env python3
from __future__ import annotations
import base64, io, re, tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'data' / 'hotels'
ALLOWED = ('hotels/', 'en/hotels/')
HUBS = {'hotels/index.html', 'en/hotels/index.html'}
HOTEL_CSS = '/assets/hotel-batch.css?v=1.2'
SPRITE_SVG = ROOT / 'assets' / 'hotels' / 'batch-sprite.svg'
SPRITE_JPG = ROOT / 'assets' / 'hotels' / 'batch-sprite.jpg'


def materialize_sprite_jpg() -> None:
    """Extract the embedded JPEG from the legacy SVG wrapper into a real JPG asset."""
    text = SPRITE_SVG.read_text(encoding='utf-8')
    marker = 'data:image/jpeg;base64,'
    start = text.find(marker)
    if start < 0:
        raise RuntimeError('Embedded hotel sprite JPEG marker not found in SVG wrapper')
    tail = text[start + len(marker):]
    alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
    chars = []
    for char in tail:
        if char in alphabet:
            chars.append(char)
        elif char.isspace():
            continue
        else:
            break
    encoded = ''.join(chars)
    if not encoded:
        raise RuntimeError('Embedded hotel sprite JPEG payload is empty')
    data = base64.b64decode(encoded, validate=True)
    if not (data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9')):
        raise RuntimeError('Decoded hotel sprite is not a valid JPEG stream')
    SPRITE_JPG.parent.mkdir(parents=True, exist_ok=True)
    SPRITE_JPG.write_bytes(data)
    print(f'Materialized {SPRITE_JPG.relative_to(ROOT).as_posix()} ({len(data)} bytes)')


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts:
        return False
    return any(name.startswith(prefix) for prefix in ALLOWED)


def normalize_html(data: bytes, name: str) -> bytes:
    """Keep one complete document, repair known paths and apply hotel-batch presentation fixes."""
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
        text = re.sub(
            r'/assets/hotel-batch\.css\?v=[^"\']+',
            HOTEL_CSS,
            text,
        )
    else:
        text = text.replace(
            '</head>',
            f'<link href="{HOTEL_CSS}" rel="stylesheet"></head>',
            1,
        )

    sprite_pattern = re.compile(
        r'<span class="batch-thumb" role="img" aria-label="([^"]*)" style="background-position:\s*(\d+)%\s+(\d+)%"></span>'
    )

    def sprite_replacement(match: re.Match[str]) -> str:
        label, x_raw, y_raw = match.groups()
        x = int(x_raw)
        y = int(y_raw)
        if x not in {0, 20, 40, 60, 80, 100} or y not in {0, 25, 50, 75, 100}:
            raise RuntimeError(f'{name}: unexpected hotel sprite position {x}% {y}%')
        left = -(x // 20) * 100
        top = -(y // 25) * 100
        return (
            f'<span class="batch-thumb" role="img" aria-label="{label}">'
            f'<img src="/assets/hotels/batch-sprite.jpg?v=1.2" alt="" loading="lazy" '
            f'style="left:{left}%;top:{top}%"></span>'
        )

    text = sprite_pattern.sub(sprite_replacement, text)

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
    return text.encode('utf-8')


def main() -> int:
    materialize_sprite_jpg()
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
