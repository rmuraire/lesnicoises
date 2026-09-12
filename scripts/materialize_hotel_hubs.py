#!/usr/bin/env python3
from __future__ import annotations
import base64, io, tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'data' / 'hotels'
ALLOWED = ('hotels/', 'en/hotels/')


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts:
        return False
    return any(name.startswith(prefix) for prefix in ALLOWED)


def normalize_html(data: bytes, name: str) -> bytes:
    """Keep one complete HTML document and repair known legacy hotel paths."""
    text = data.decode('utf-8')
    end = text.lower().find('</html>')
    if end >= 0:
        text = text[: end + len('</html>')]
    text = text.replace(
        'href="/hotels/hotel-de-paris-monte-carlo/"',
        'href="/hotels/monaco/hotel-de-paris-monte-carlo/"',
    )
    if text.lower().count('<title>') != 1:
        raise RuntimeError(f'{name}: expected one title after normalization')
    if text.lower().count('<h1') != 1:
        raise RuntimeError(f'{name}: expected one h1 after normalization')
    return text.encode('utf-8')


def main() -> int:
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
