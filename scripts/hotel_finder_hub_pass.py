#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = '/assets/hotel-engine.css?v=3'

ENTRY_FR = '''<section class="v3-section hotel-finder-entry" data-hotel-finder-entry="true"><div class="wrap"><div class="finder-entry-inner"><div><p class="eyebrow">1 · Vous préférez qu’on tranche ?</p><h2>Trouver votre hôtel</h2><p>Choisissez votre base — ou laissez-la ouverte — puis dites-nous ce qui compte vraiment. Mametas réduit la sélection à trois ou quatre adresses, avec la raison et le compromis.</p></div><a class="button" href="/hotels/finder/">Lancer l’outil hôtel</a></div></div></section>'''

ENTRY_EN = '''<section class="v3-section hotel-finder-entry" data-hotel-finder-entry="true"><div class="wrap"><div class="finder-entry-inner"><div><p class="eyebrow">1 · Prefer us to narrow it down?</p><h2>Find your hotel</h2><p>Choose a base — or leave it open — then tell us what actually matters. Mametas cuts the selection to three or four addresses, with the reason and the catch.</p></div><a class="button" href="/en/hotels/finder/">Open the hotel finder</a></div></div></section>'''

EN_BASE_SECTION = '''<section class="v3-section practical hotel-base-entry"><div class="wrap"><p class="eyebrow">2 · Already know where you want to stay?</p><div class="practical-title practical-title-above"><h2>Choose your base and explore our selection.</h2><p>Nice, Cannes, Antibes, Menton… go straight to a base to see the hotels we kept, with the differences and trade-offs that actually matter.</p></div><div class="practical-grid practical-grid-ten"><a class="practical-link" href="/stay/nice/"><span>01</span><h3>Nice</h3><p>The all-round base: practical, lively, quiet or polished by the sea.</p></a><a class="practical-link" href="/en/hotels/antibes/"><span>02</span><h3>Antibes &amp; Juan-les-Pins</h3><p>Old-town ease, livelier Juan-les-Pins or a more dressed-up Riviera stay.</p></a><a class="practical-link" href="/en/hotels/cannes/"><span>03</span><h3>Cannes</h3><p>Palaces, central luxury and more intimate counterpoints.</p></a><a class="practical-link" href="/en/hotels/villefranche-sur-mer/"><span>04</span><h3>Villefranche &amp; Cap-Ferrat</h3><p>Harbour beauty or a grander retreat on the Cap. Beauty first.</p></a><a class="practical-link" href="/en/hotels/monaco/"><span>05</span><h3>Monaco</h3><p>Stay when Monaco itself is part of the trip, not merely a day out.</p></a><a class="practical-link" href="/en/hotels/menton/"><span>06</span><h3>Menton &amp; Roquebrune</h3><p>A slower eastern base, from practical to more polished.</p></a><a class="practical-link" href="/en/hotels/saint-paul-de-vence/"><span>07</span><h3>Saint-Paul-de-Vence</h3><p>Sleeping after the day-trippers leave changes the village completely.</p></a><a class="practical-link" href="/en/hotels/beaulieu-sur-mer/"><span>08</span><h3>Beaulieu-sur-Mer</h3><p>Quieter than Nice, less theatrical than Monaco.</p></a><a class="practical-link" href="/en/hotels/mougins/"><span>09</span><h3>Mougins</h3><p>The hills as a chic retreat or a gentler base.</p></a><a class="practical-link" href="/en/hotels/saint-tropez/"><span>10</span><h3>Saint-Tropez &amp; peninsula</h3><p>Village, Ramatuelle, Gassin or Sainte-Maxime: geography before the sunbed.</p></a></div></div></section>'''


def ensure_css(text: str) -> str:
    if '/assets/hotel-engine.css' in text:
        return re.sub(r'/assets/hotel-engine\.css\?v=[^"\']+', CSS, text)
    return text.replace('</head>', f'<link rel="stylesheet" href="{CSS}"></head>', 1)


def inject_entry(text: str, entry: str) -> str:
    if 'data-hotel-finder-entry="true"' in text:
        return text
    main = text.find('<main')
    if main < 0:
        raise RuntimeError('Missing <main> in hotel hub')
    hero_end = text.find('</header>', main)
    if hero_end < 0:
        raise RuntimeError('Missing article hero closing header in hotel hub')
    hero_end += len('</header>')
    return text[:hero_end] + entry + text[hero_end:]


def replace_first_practical(text: str, replacement: str) -> str:
    pattern = re.compile(r'<section class="v3-section practical">.*?</section>', re.S)
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError('Could not replace English base grid')
    return text


def relabel_french_base_intro(text: str) -> str:
    pattern = re.compile(
        r'<section class="v3-section practical"><div class="wrap">'
        r'<p class="eyebrow">Choisir sa base</p>'
        r'<div class="practical-title practical-title-above"><h2>.*?</h2><p>.*?</p></div>',
        re.S,
    )
    replacement = (
        '<section class="v3-section practical hotel-base-entry"><div class="wrap">'
        '<p class="eyebrow">2 · Vous savez déjà où dormir ?</p>'
        '<div class="practical-title practical-title-above">'
        '<h2>Choisissez votre base et explorez notre sélection.</h2>'
        '<p>Nice, Cannes, Antibes, Menton… entrez directement dans une base pour voir les hôtels que nous avons retenus, avec leurs différences et leurs compromis.</p>'
        '</div>'
    )
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError('Could not relabel French base grid')
    return text


def patch_hub(rel: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    text = ensure_css(text)
    if lang == 'fr':
        text = text.replace('40+ adresses éditorialisées', '90+ adresses éditorialisées')
        text = relabel_french_base_intro(text)
        text = inject_entry(text, ENTRY_FR)
    else:
        text = text.replace('28+ selected addresses', '90+ selected addresses')
        text = replace_first_practical(text, EN_BASE_SECTION)
        text = inject_entry(text, ENTRY_EN)
    path.write_text(text, encoding='utf-8')
    print(f'Hotel finder entry added to {rel}')


def patch_sitemap() -> None:
    path = ROOT / 'sitemap.xml'
    text = path.read_text(encoding='utf-8')
    additions = []
    if 'https://www.mametas.com/hotels/finder/' not in text:
        additions.append('  <url><loc>https://www.mametas.com/hotels/finder/</loc><lastmod>2026-09-16</lastmod></url>')
    if 'https://www.mametas.com/en/hotels/finder/' not in text:
        additions.append('  <url><loc>https://www.mametas.com/en/hotels/finder/</loc><lastmod>2026-09-16</lastmod></url>')
    if additions:
        text = text.replace('</urlset>', '\n'.join(additions) + '\n</urlset>', 1)
        path.write_text(text, encoding='utf-8')
        print('Hotel finder URLs added to sitemap.xml')


def main() -> int:
    patch_hub('hotels/index.html', 'fr')
    patch_hub('en/hotels/index.html', 'en')
    patch_sitemap()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
