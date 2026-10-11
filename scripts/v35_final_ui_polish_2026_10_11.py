#!/usr/bin/env python3
"""Mametas 2026-10-11: final PRESENTATION-only family QA fixes.

Idempotent materialization pass: never rewrites editorial copy except translating
five existing FAQ answers into the FR Gay hub to match its EN sibling.
Runs after V34 and before the browser sweep / OVH deploy. No global CSS edits.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/assets/mametas-v35-ui-polish.css?v=2">'
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
    """Never add a second FAQ when the earlier materializers supplied one."""
    # Existing accessible disclosures are authoritative. Do not duplicate them.
    if 'class="mametas-faq-parity"' in s or (
        s.count('<details') >= 3 and ('class="intent-faq"' in s or 'faq-list' in s)
    ):
        return s
    # Real production already contains five static H3/P FAQ items. Replace
    # *that exact section* with native accordions, preserving its original copy.
    pattern = re.compile(
        r'<h2[^>]*>\s*FAQ\s*</h2>\s*'
        r'((?:<div class="place">\s*<h3>.*?</h3>\s*'
        r'<p class="why">.*?</p>\s*</div>\s*)+)',
        re.S | re.I,
    )
    matches = list(pattern.finditer(s))
    if matches:
        if len(matches) != 1:
            raise RuntimeError("FR Gay hub: multiple static FAQ sections")
        questions = FAQ_PLACE.findall(matches[0].group(1))
        if len(questions) < 3 or FAQ_PLACE.sub('', matches[0].group(1)).strip():
            raise RuntimeError("FR Gay hub: unexpected pre-existing FAQ markup")
        faq = '<section class="mametas-faq-parity"><h2>FAQ</h2>'
        faq += ''.join(detail(q, a) for q, a in questions) + '</section>'
        return s[:matches[0].start()] + faq + s[matches[0].end():]
    if re.search(r'<h2[^>]*>\s*FAQ\s*</h2>', s, re.I):
        raise RuntimeError("FR Gay hub: FAQ heading exists but could not be converted")
    # Some earlier generator variants omit the FAQ entirely; only these may
    # receive a fallback section.
    anchor = '<h2>Quatre portes utiles</h2>'
    if s.count(anchor) != 1:
        raise RuntimeError("FR Gay hub: insertion point changed")
    faq = '<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq += ''.join(detail(q, a) for q, a in fr_faq) + '</section>'
    faq = re.sub(r' (?=[!?;:])', '\u00a0', faq)
    return s.replace(anchor, faq + anchor, 1)


def fix_en_gay_faq(s):
    # Production and CI materializers do not always leave the same headings
    # after the FAQ. Never depend on the next H2's editorial wording.
    if 'class="mametas-faq-parity"' in s:
        return s
    if s.count('<details') >= 3 and ('class="intent-faq"' in s or 'faq-list' in s):
        return s
    heading = re.search(r'<h2[^>]*>\s*FAQ\s*</h2>', s, re.I)
    if heading is None:
        at = s.lower().find('faq')
        raise RuntimeError(f"EN Gay FAQ heading absent; details={s.count('<details')}; context={s[max(0,at-100):at+900]!r}")
    cursor = heading.end()
    qa = []
    for _ in range(5):
        spaces = re.match(r'\s*', s[cursor:])
        cursor += spaces.end()
        match = FAQ_PLACE.match(s, cursor)
        if match is None:
            raise RuntimeError(f"EN Gay FAQ has only {len(qa)} expected Q&A items; next={s[cursor:cursor+500]!r}")
        qa.append(match.groups())
        cursor = match.end()
    faq = '<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq += ''.join(detail(q, a) for q, a in qa) + '</section>'
    return s[:heading.start()] + faq + s[cursor:]


def fix_en_gay_subguide_faq(s, rel):
    """Respect native FAQ accordions already materialized by earlier passes."""
    if '<div class="faq-list">' in s:
        if s.count('class="faq-item"') < 3:
            raise RuntimeError(f"{rel}: existing FAQ accordion is incomplete")
        return s
    if 'class="mametas-faq-parity"' in s:
        return s
    pattern = re.compile(
        r'<h2>FAQ</h2>\s*((?:<div class="place">\s*<h3>.*?</h3>\s*<p class="why">.*?</p>\s*</div>\s*)+)',
        re.S,
    )
    matches = list(pattern.finditer(s))
    if len(matches) != 1:
        raise RuntimeError(f"{rel}: expected existing FAQ questions, got {len(matches)}")
    questions = FAQ_PLACE.findall(matches[0].group(1))
    if len(questions) != 3 or FAQ_PLACE.sub('', matches[0].group(1)).strip():
        raise RuntimeError(f"{rel}: unexpected FAQ markup, not modifying")
    faq = '<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq += ''.join(detail(q, a) for q, a in questions) + '</section>'
    return s[:matches[0].start()] + faq + s[matches[0].end():]



def fix_fr_gay_subguide_faq(s, rel):
    """Normalize static French Gay subguide FAQs, preserving existing native accordions."""
    if 'class="mametas-faq-parity"' in s or (
        s.count('<details') >= 3 and ('class="intent-faq"' in s or 'faq-list' in s)
    ):
        return s
    heading = re.search(r'<h2[^>]*>\s*(?:FAQ|Questions fréquentes)\s*</h2>', s, re.I)
    if heading is None:
        return s  # This subguide has no FAQ; do not invent editorial answers.
    pattern = re.compile(
        r'<h2[^>]*>\s*(?:FAQ|Questions fréquentes)\s*</h2>\s*'
        r'((?:<div class="place">\s*<h3>.*?</h3>\s*<p class="why">.*?</p>\s*</div>\s*)+)',
        re.S | re.I,
    )
    matches = list(pattern.finditer(s))
    if len(matches) != 1:
        raise RuntimeError(f"{rel}: static FR FAQ has unexpected markup, refusing to leave it unconverted")
    questions = FAQ_PLACE.findall(matches[0].group(1))
    if not (3 <= len(questions) <= 8) or FAQ_PLACE.sub('', matches[0].group(1)).strip():
        raise RuntimeError(f"{rel}: incomplete or inconsistent FR FAQ")
    faq = '<section class="mametas-faq-parity"><h2>FAQ</h2>'
    faq += ''.join(detail(q, a) for q, a in questions) + '</section>'
    return s[:matches[0].start()] + faq + s[matches[0].end():]


# The six legacy FR-only cards must not survive the final rendered HTML,
# regardless of CSS class, image replacement, or the materializer version.
FR_EXTRA_HOTELS = (
    "Hôtel Belles Rives",
    "Five Seas Hotel Cannes",
    "Grand-Hôtel du Cap-Ferrat",
    "Hôtel Hermitage Monte-Carlo",
    "Le Domaine du Mas de Pierre",
    "Hôtel La Ponche",
)

class _DivBounds(HTMLParser):
    """Find balanced div elements without reserializing/altering page HTML."""
    def __init__(self, source):
        super().__init__()
        self.line_starts = [0] + [m.end() for m in re.finditer(r"\n", source)]
        self.stack = []
        self.bounds = []

    def _pos(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "div":
            self.stack.append(self._pos())

    def handle_endtag(self, tag):
        if tag.lower() == "div" and self.stack:
            self.bounds.append((self.stack.pop(), self._pos() + len("</div>")))


def fix_fr_hotels(s):
    """Preserve the FR rule and ten-base routing, remove only the extra six-card grid."""
    decoded = unescape(s)
    present = [name for name in FR_EXTRA_HOTELS if name in decoded]
    if not present:
        return s
    if len(present) != len(FR_EXTRA_HOTELS):
        raise RuntimeError(f"FR Stay hub has partial legacy selection: {present}")
    parser = _DivBounds(s)
    parser.feed(s)
    options = []
    for start, end in parser.bounds:
        fragment = s[start:end]
        text = unescape(fragment)
        if (
            end - start < 18000
            and all(name in text for name in FR_EXTRA_HOTELS)
            and len(re.findall(r"<h3\b", fragment, re.I)) >= 6
            and "La règle Mametas" not in text
            and "Hotel Fit" not in text
        ):
            options.append((end - start, start, end))
    if not options:
        raise RuntimeError("FR Stay hub: cannot isolate six-card block safely")
    _, start, end = min(options)
    cleaned = s[:start] + s[end:]
    if any(name in unescape(cleaned) for name in FR_EXTRA_HOTELS):
        raise RuntimeError("FR Stay hub: legacy hotel cards remain after removal")
    return cleaned


def fix_beaches_around_nice_images(s):
    """Suppress only missing photo panels, never substitute a false location.

    The three source files have never been committed. External Commons
    redirects are not supported by the release's image provenance policy.
    Preserve all surviving licensed local beach photos and written guidance.
    """
    missing = (
        'fossettes-commons.jpg',
        'passable-pexels.jpg',
        'mala-commons.jpg',
    )
    for filename in missing:
        # Match a figure with the missing *image src*, including its caption.
        pat = re.compile(
            r'<figure\b[^>]*class="beach-place-visual"[^>]*>'
            r'(?:(?!</figure>).)*?'
            r'<img\b[^>]*src="[^"]*/' + re.escape(filename) +
            r'(?:\?[^"]*)?"[^>]*>'
            r'(?:(?!</figure>).)*?</figure>',
            re.S
        )
        s, count = pat.subn('', s)
        if count != 1:
            raise RuntimeError(f"Expected one absent beach photo figure: {filename}, got {count}")
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
        if rel == 'guide-gay-nice/index.html' or rel.startswith('cote-dazur-gay/'):
            s=fix_fr_gay_subguide_faq(s,rel)
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
        if path.startswith('hotels/'):
            if 'batch-thumb' in page or any(name in unescape(page) for name in FR_EXTRA_HOTELS):
                raise RuntimeError("FR hotel hub still contains the six unwanted cards")
            if "La règle Mametas" not in unescape(page):
                raise RuntimeError("FR hotel hub lost the editorial rule")
        # Production can replace the legacy .practical-grid with a new layout.
        # Test the actual destination anchors, not a brittle CSS class.
        links = set(re.findall(r'<a\b[^>]*href="([^"]+)"', page))
        bases = [href for href in links if href.startswith(
            ('/hotels/', '/en/hotels/', '/stay/', '/fr/dormir/')
        )]
        if len(bases) < 5:
            snippet = page[page.find('<main'):][:1100]
            raise RuntimeError(f"{path}: hotel base navigation missing; links={bases[:10]}; snippet={snippet!r}")
    fr=(ROOT/'cote-dazur-gay/index.html').read_text(encoding='utf-8')
    en=(ROOT/'en/gay-french-riviera/index.html').read_text(encoding='utf-8')
    # FR must have exactly one FAQ after deduplication. EN is allowed a
    # localized heading / already-materialized intent-faq component.
    fr_faq_heading_count = len(re.findall(r'<h2[^>]*>\s*FAQ\s*</h2>', fr, re.I))
    if fr_faq_heading_count != 1:
        raise RuntimeError(f"FR Gay hub has {fr_faq_heading_count} FAQ headings (expected one)")
    for lang, html in (('FR',fr),('EN',en)):
        our_disclosure='<section class="mametas-faq-parity">' in html
        previous_disclosure=('faq-list' in html or 'class="intent-faq"' in html or '<h2>FAQ</h2>' in html) and html.count('<details')>=3
        if not (our_disclosure or previous_disclosure):
            raise RuntimeError(f"{lang} Gay FAQ parity missing")
    if fr.count('<details') < 3 or en.count('<details') < 3:
        raise RuntimeError("Gay FAQ must have at least three native disclosures in each language")
    for path in (
        'guide-gay-nice/index.html',
        'cote-dazur-gay/ou-dormir/index.html',
        'cote-dazur-gay/plages-sans-voiture/index.html',
        'cote-dazur-gay/itineraire-5-jours/index.html',
    ):
        html = (ROOT/path).read_text(encoding='utf-8')
        if re.search(r'<h2[^>]*>\s*(?:FAQ|Questions fréquentes)\s*</h2>', html, re.I) and (
            '<section class="mametas-faq-parity">' not in html
            and 'class="intent-faq"' not in html
            and 'class="faq-list"' not in html
        ):
            raise RuntimeError(f"{path}: FR Gay FAQ remains static")
    for path in ('en/gay-nice/index.html',
                 'en/gay-french-riviera/where-to-stay/index.html',
                 'en/gay-french-riviera/beaches-without-a-car/index.html'):
        h=(ROOT/path).read_text(encoding='utf-8')
        normalized = h.count('<section class="mametas-faq-parity">')==1 and h.count('<details>')==3
        existing = '<div class="faq-list">' in h and h.count('class="faq-item"') >= 3
        if not (normalized or existing):
            raise RuntimeError(f"{path}: FAQ accordion parity incomplete")
    print(f"V35 PRESENTATION: {modified} pages, {compact} compact editorial pages, "
          f"{card_count} semantic Good Finds cards, {fr.count('<details>')} Gay FAQ pairs, "
          "removed broken FR hotel batch; CSS component rules loaded.")

if __name__=='__main__':run()
