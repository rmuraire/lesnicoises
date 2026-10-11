#!/usr/bin/env python3
"""Mametas 2026-10-11: final PRESENTATION-only family QA fixes.

Idempotent materialization pass: never rewrites editorial copy except translating
five existing FAQ answers into the FR Gay hub to match its EN sibling.
Runs after V34 and before the browser sweep / OVH deploy. No global CSS edits.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/assets/mametas-v35-ui-polish.css?v=1">'
FAQ_PLACE = re.compile(
    r'<div class="place">\s*<h3>(.*?)</h3>\s*<p class="why">(.*?)</p>\s*</div>',
    re.S,
)
fr_faq = [
    ("La Côte d’Azur est-elle gay-friendly ?",
     "Nice possède l’infrastructure LGBTQ+ la plus visible du littoral. Ailleurs, choisissez surtout votre destination en fonction de ce que vous avez envie de faire."),
    ("Nice ou Cannes pour un séjour gay ?",
     "Nice pour la vie communautaire et la base sans voiture. Cannes si l’ouest de la Riviera est au centre de votre séjour."),
    ("Monaco est-il gay-friendly ?",
     "Pour la plupart des voyageurs, Monaco fonctionne mieux comme excursion. Nice reste la meilleure base pour sortir."),
    ("Quand a lieu la Pride de Nice ?",
     "Les dates évoluent. Vérifiez le calendrier LGBTQIA+ officiel avant de réserver autour de l’événement."),
    ("Faut-il une voiture ?",
     "Pas pour un premier séjour basé à Nice : train, tram et marche couvrent l’essentiel de la côte. Une voiture aide davantage pour certains hébergements à l’intérieur des terres."),
]

def detail(q, a):
    return '<details><summary>'+q+'</summary><p>'+a+'</p></details>'

def add_body_class(html, token):
    m = re.search(r'<body\b[^>]*>', html, flags=re.I)
    if not m: raise RuntimeError("Body not found")
    tag = m.group()
    if token in tag: return html
    c = re.search(r'class="([^"]*)"', tag)
    if c:
        new = tag[:c.start(1)] + c.group(1)+' '+token +tag[c.end(1):]
    else:
        new = tag[:-1]+' class="'+token+'">'
    return html[:m.start()]+new+html[m.end():]

def fix_fr_gay_faq(s):
    # EN FAQ uses genuine Q+A records; give FR exactly the same functional UX.
    if 'class="mametas-faq-parity"' in s: return s
    anchor='<h2>Quatre portes utiles</h2>'
    if s.count(anchor)!=1:
        raise RuntimeError("FR Gay hub: insertion point changed")
    faq='<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq+=''.join(detail(q,a) for q,a in fr_faq)+'</section>'
    # French punctuation uses non-breaking spacing for ? ! : ; across the site.
    faq=re.sub(r' (?=[!?;:])','\u00a0',faq)
    return s.replace(anchor,faq+anchor,1)

def fix_en_gay_faq(s):
    if 'class="mametas-faq-parity"' in s:return s
    start=s.find('<h2>FAQ</h2>')
    end=s.find('<h2>Four useful doors</h2>',start)
    if start<0 or end<start:raise RuntimeError("EN Gay FAQ boundaries missing")
    raw=s[start+len('<h2>FAQ</h2>'):end]
    matches=FAQ_PLACE.findall(raw)
    if len(matches)!=5:raise RuntimeError(f"EN Gay FAQ: expected 5 questions, got {len(matches)}")
    if FAQ_PLACE.sub('',raw).strip():raise RuntimeError("Unexpected content in Gay FAQ")
    faq='<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq+=''.join(detail(q,a) for q,a in matches)+'</section>'
    return s[:start]+faq+s[end:]

def fix_en_gay_subguide_faq(s, rel):
    """Convert an existing static Q&A cluster, never alter its actual answers."""
    if 'class="mametas-faq-parity"' in s:
        return s
    pattern = re.compile(
        r'<h2>FAQ</h2>\\s*((?:<div class="place">\\s*<h3>.*?</h3>\\s*<p class="why">.*?</p>\\s*</div>\\s*)+)',
        re.S,
    )
    matches = list(pattern.finditer(s))
    if len(matches) != 1:
        raise RuntimeError(f"{rel}: expected exactly one existing FAQ cluster, got {len(matches)}")
    questions = FAQ_PLACE.findall(matches[0].group(1))
    if len(questions) != 3 or FAQ_PLACE.sub('', matches[0].group(1)).strip():
        raise RuntimeError(f"{rel}: unexpected FAQ markup, not modifying")
    faq = '<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq += ''.join(detail(q, a) for q, a in questions) + '</section>'
    return s[:matches[0].start()] + faq + s[matches[0].end():]


def fix_fr_hotels(s):
    # The broken affiliate-sprite selection has no EN-equivalent asset treatment.
    # Keep the fully functional 10-base guide, delete only its obsolete tail.
    if 'batch-thumb' not in s: return s
    start=s.rfind('<section class="v3-section">')
    end=s.find('</main>',start)
    if start<0 or end<start:raise RuntimeError("French Stay hub structure changed")
    removed=s[start:end]
    if 'batch-thumb' not in removed or 'place-grid' not in removed:
        raise RuntimeError("Refusing to remove a non-batch Stay section")
    return s[:start]+s[end:]

def fix_beaches_around_nice_images(s):
    # Three 2026-local image paths in FR+EN pointed to files never committed.
    # Use verified exact-location public-domain/CC Commons sources instead
    # of quietly displaying broken image rectangles.
    photos = {
        '/assets/editorial/beaches/fossettes-commons.jpg?v=20260926-final':
            'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cap-Ferrat_les_Fossettes.jpg',
        '/assets/editorial/beaches/passable-pexels.jpg?v=20260926-final':
            'https://commons.wikimedia.org/wiki/Special:Redirect/file/Plage_de_Passable.jpg',
        '/assets/editorial/beaches/mala-commons.jpg?v=20260926-final':
            'https://commons.wikimedia.org/wiki/Special:Redirect/file/Plage_Mala%2C_Cap_d%27Ail_-_panoramio.jpg',
    }
    for before,after in photos.items():
        if before not in s and after not in s:
            raise RuntimeError(f"Missing source photo markup: {before}")
        s=s.replace(before,after)
    # License/source for Passable changed: Pexels generic coast -> documented
    # exact Plage de Passable image by Tangopaso (public domain).
    s=s.replace(
        '<a href="https://www.pexels.com/fr-fr/photo/baie-rochers-cailloux-cote-13781215/" target="_blank" rel="noopener">Pexels</a>',
        '<a href="https://commons.wikimedia.org/wiki/File:Plage_de_Passable.jpg" target="_blank" rel="noopener">Tangopaso / Wikimedia Commons · domaine public</a>',
    )
    s=s.replace(
        '<a href="https://www.pexels.com/fr-fr/photo/baie-rochers-cailloux-cote-13781215/" target="_blank" rel="noopener">Pexels</a>',
        '<a href="https://commons.wikimedia.org/wiki/File:Plage_de_Passable.jpg" target="_blank" rel="noopener">Tangopaso / Wikimedia Commons · public domain</a>',
    )
    return s

def make_event_cards_clickable(s, rel):
    """Clickable event tiles without breaking their independent official/map links."""
    if 'right-now-clean' not in s:
        return s  # Other Good Finds templates already use full <a class="card">.
    if 'mametas-card-overlay' in s:
        return s
    pat = re.compile(r'(<div class="card">)(.*?)(</div>)', re.S)
    count = [0]

    def wrap(m):
        inner = m.group(2)
        cta = re.search(r'<a class="more" href="([^"]+)"', inner)
        heading = re.search(r'<h3[^>]*>(.*?)</h3>', inner, re.S)
        if not cta or not heading:
            raise RuntimeError(f"{rel}: agenda tile missing primary destination or H3")
        count[0] += 1
        title = re.sub(r'<[^>]+>', '', heading.group(1)).strip()
        lang = 'fr' if rel.startswith('bons-plans/') else 'en'
        label = ('Ouvrir : ' if lang == 'fr' else 'Open: ') + title
        overlay = (f'<a class="mametas-card-overlay" href="{escape(cta.group(1), quote=True)}" '
                   f'aria-label="{escape(label, quote=True)}"></a>')
        return m.group(1) + overlay + inner + m.group(3)

    s, _ = pat.subn(wrap, s)
    if count[0] < 3:
        raise RuntimeError(f"{rel}: only {count[0]} agenda cards are fully clickable")
    return add_body_class(s, 'mametas-good-finds-hub')


class CardAnchorCounter(HTMLParser):
    """Count real semantic card anchors, regardless of attribute order/classes."""
    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        data = dict(attrs)
        if data.get('href') and 'card' in (data.get('class') or '').split():
            self.count += 1

def run():
    modified=0; compact=0; card_count=0
    files=list(ROOT.rglob('index.html'))
    for f in files:
        if any(x.startswith('.') for x in f.relative_to(ROOT).parts):continue
        rel=f.relative_to(ROOT).as_posix()
        s=f.read_text(encoding='utf-8')
        old=s
        if rel in ('plages/autour-de-nice/index.html','en/beaches/around-nice/index.html'):
            s=fix_beaches_around_nice_images(s)
        if rel.startswith(('restaurants/','en/restaurants/')) and 'class="article"' in s:
            s=add_body_class(s,'mametas-restaurant-detail')
        if rel=='en/gay-french-riviera/index.html':s=fix_en_gay_faq(s)
        if rel=='cote-dazur-gay/index.html':s=fix_fr_gay_faq(s)
        if rel in (
            'en/gay-nice/index.html',
            'en/gay-french-riviera/where-to-stay/index.html',
            'en/gay-french-riviera/beaches-without-a-car/index.html',
        ):
            s=fix_en_gay_subguide_faq(s,rel)
        if rel=='hotels/index.html':s=fix_fr_hotels(s)
        # One consistent small-scale editorial hierarchy for standard site.css
        # articles (beaches, Practical, Gay, Good Finds, etc.), not V3 intent.
        if 'class="article"' in s and 'site.css' in s:
            s=add_body_class(s,'mametas-compact-article')
            compact+=1
        if rel in ('bons-plans/index.html','en/good-finds/index.html'):
            s=make_event_cards_clickable(s,rel)
            # Additional presentation classes are legitimately appended by the
            # previous materializers; do not require class="card" exactly.
            parser = CardAnchorCounter()
            parser.feed(s)
            if parser.count < 8 and s.count('class="mametas-card-overlay"') < 3:
                raise RuntimeError(
                    f"{rel}: no complete clickable card set (anchors={parser.count})"
                )
            card_count+=parser.count
        # CSS is a tiny scoped extra stylesheet, appended last, and works
        # across currently materialized HTML/links without changing source CSS.
        needs_css = ('class="article"' in s or 'class="intent-detail' in s
            or 'spot-logistics' in s or 'class="grid"' in s
            or rel.startswith(('cote-dazur-gay/','en/gay-french-riviera/',
                'explore/','en/explore/','bons-plans/','en/good-finds/',
                'plages/','en/beaches/','riviera-guide/','en/riviera-guide/')))
        if needs_css and '</head>' in s and CSS not in s:
            s=s.replace('</head>',CSS+'</head>',1)
        if s!=old:
            f.write_text(s,encoding='utf-8')
            modified+=1
    for path in ('hotels/index.html','en/hotels/index.html'):
        page=(ROOT/path).read_text(encoding='utf-8')
        if path.startswith('hotels/') and 'batch-thumb' in page:
            raise RuntimeError("FR hotel batch still present")
        if 'class="practical-grid"' not in page:
            raise RuntimeError(f"{path}: hotel base guide missing")
    fr=(ROOT/'cote-dazur-gay/index.html').read_text(encoding='utf-8')
    en=(ROOT/'en/gay-french-riviera/index.html').read_text(encoding='utf-8')
    if '<section class="mametas-faq-parity">' not in fr or '<section class="mametas-faq-parity">' not in en:
        raise RuntimeError("Gay FAQ parity missing")
    if fr.count('<details>')!=en.count('<details>'):
        raise RuntimeError("Gay FAQ disclosure count mismatch")
    for path in ('en/gay-nice/index.html',
                 'en/gay-french-riviera/where-to-stay/index.html',
                 'en/gay-french-riviera/beaches-without-a-car/index.html'):
        h=(ROOT/path).read_text(encoding='utf-8')
        if h.count('<section class="mametas-faq-parity">')!=1 or h.count('<details>')!=3:
            raise RuntimeError(f"{path}: FAQ accordion parity incomplete")
    print(f"V35 PRESENTATION: {modified} pages, {compact} compact editorial pages, "
          f"{card_count} semantic Good Finds cards, {fr.count('<details>')} Gay FAQ pairs, "
          "removed broken FR hotel batch; CSS component rules loaded.")

if __name__=='__main__':run()
