# -*- coding: utf-8 -*-
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MARK='data-v5-intent-architecture="true"'

def card(href, icon, small, title, copy, cta):
    return f'''<a class="travel-profile-card" href="{href}"><span class="travel-profile-icon travel-profile-icon--v5" aria-hidden="true">{icon}</span><span class="travel-profile-copy"><small>{small}</small><strong>{title}</strong><p>{copy}</p><b>{cta} →</b></span></a>'''

def patch(path, lang):
    p=ROOT/path
    s=p.read_text(encoding='utf-8')
    if MARK in s:
        print('unchanged',path)
        return

    if lang=='en':
        sec_id='by-travel'
        eyebrow_old='<p class="eyebrow">BY HOW YOU TRAVEL</p>'
        eyebrow_new='<p class="eyebrow">TRAVEL YOUR WAY</p>'
        additions=''.join([
            card('/en/explore/french-riviera-honeymoon/','♥','COUPLES · HONEYMOON','French Riviera honeymoon','One strong base, a slower rhythm and the romantic upgrades actually worth paying for.','Read the guide'),
            card('/en/explore/french-riviera-babymoon/','◌','COMFORT FIRST · BABYMOON','French Riviera babymoon','Easy transport, calm hotels and realistic days without turning the trip into an endurance test.','Read the guide'),
            card('/en/explore/french-riviera-proposal/','✦','THE QUESTION · PROPOSAL','Planning a proposal','The view matters. Timing, crowds, the exit and a credible plan B matter too.','Read the guide'),
        ])
        living=f'''<section class="v3-section v5-living-section" data-v5-living="true"><div class="wrap">
<div class="section-heading"><div><p class="eyebrow">LIVING ON THE RIVIERA</p><h2>When Tuesday matters too.</h2></div><p>Two deeper guides for people testing the Riviera as a place to live, not simply a place to spend a week.</p></div>
<div class="travel-profile-grid">
{card('/en/explore/living-antibes-expat/','A','EXPAT LIFE · ANTIBES','Living in Antibes as an expat','Sophia, Port Vauban, neighbourhoods, commuting, housing and the boring test week worth doing first.','Read the guide')}
{card('/en/explore/retire-french-riviera/','☀','LONG TERM · RETIREMENT','Retiring on the French Riviera','Nice, Antibes or Menton, with healthcare, residency, tax and everyday-life reality checks.','Read the guide')}
</div></div></section>'''
        bridge='<section class="v3-section explore-practical-bridge">'
    else:
        sec_id='par-voyage'
        eyebrow_old='<p class="eyebrow">PAR FAÇON DE VOYAGER</p>'
        eyebrow_new='<p class="eyebrow">VOYAGER À VOTRE FAÇON</p>'
        additions=''.join([
            card('/explore/lune-de-miel-cote-d-azur/','♥','COUPLE · LUNE DE MIEL','Lune de miel sur la Côte d’Azur','Un bon point de chute, un rythme plus lent et les upgrades romantiques qui valent réellement le prix.','Lire le guide'),
            card('/explore/babymoon-cote-d-azur/','◌','CONFORT D’ABORD · BABYMOON','Babymoon sur la Côte d’Azur','Transports faciles, hôtels calmes et journées réalistes sans transformer le séjour en épreuve.','Lire le guide'),
            card('/explore/demande-en-mariage-cote-d-azur/','✦','LA QUESTION · DEMANDE','Préparer une demande en mariage','La vue compte. L’horaire, la foule, la sortie et un vrai plan B aussi.','Lire le guide'),
        ])
        living=f'''<section class="v3-section v5-living-section" data-v5-living="true"><div class="wrap">
<div class="section-heading"><div><p class="eyebrow">VIVRE SUR LA RIVIERA</p><h2>Quand le mardi compte aussi.</h2></div><p>Deux guides plus profonds pour ceux qui testent la Côte d’Azur comme lieu de vie, pas seulement comme destination d’une semaine.</p></div>
<div class="travel-profile-grid">
{card('/explore/vivre-antibes-expatrie/','A','VIE D’EXPAT · ANTIBES','Vivre à Antibes en expatrié','Sophia, Port Vauban, quartiers, trajets, logement et la semaine ennuyeuse à tester avant de déménager.','Lire le guide')}
{card('/explore/retraite-cote-d-azur/','☀','LONG TERME · RETRAITE','Prendre sa retraite sur la Côte d’Azur','Nice, Antibes ou Menton, avec santé, séjour, fiscalité et réalité du quotidien.','Lire le guide')}
</div></div></section>'''
        bridge='<section class="v3-section explore-practical-bridge">'

    open_tag=f'<section class="v3-section" id="{sec_id}">'
    pos=s.find(open_tag)
    if pos<0:
        raise RuntimeError(f'{path}: travel section missing')
    s=s.replace(open_tag,open_tag[:-1]+' '+MARK+'>',1)
    if eyebrow_old not in s:
        raise RuntimeError(f'{path}: travel eyebrow missing')
    s=s.replace(eyebrow_old,eyebrow_new,1)

    pos=s.find(f'id="{sec_id}"')
    grid=s.find('<div class="travel-profile-grid">',pos)
    if grid<0:
        raise RuntimeError(f'{path}: travel grid missing')
    close=s.find('</div>',grid)
    if close<0:
        raise RuntimeError(f'{path}: travel grid close missing')
    s=s[:close]+additions+s[close:]

    bridge_pos=s.find(bridge,close+len(additions))
    if bridge_pos<0:
        raise RuntimeError(f'{path}: practical bridge missing')
    s=s[:bridge_pos]+living+'\n'+s[bridge_pos:]
    p.write_text(s,encoding='utf-8')
    print('patched',path)

patch('en/explore/index.html','en')
patch('explore/index.html','fr')

urls=[
'/en/explore/french-riviera-honeymoon/','/explore/lune-de-miel-cote-d-azur/',
'/en/explore/french-riviera-babymoon/','/explore/babymoon-cote-d-azur/',
'/en/explore/french-riviera-proposal/','/explore/demande-en-mariage-cote-d-azur/',
'/en/explore/living-antibes-expat/','/explore/vivre-antibes-expatrie/',
'/en/explore/retire-french-riviera/','/explore/retraite-cote-d-azur/'
]
sp=ROOT/'sitemap.xml'
sm=sp.read_text(encoding='utf-8')
missing=[u for u in urls if f'<loc>https://www.mametas.com{u}</loc>' not in sm]
if missing:
    block='\n'.join(f'  <url><loc>https://www.mametas.com{u}</loc><lastmod>2026-10-01</lastmod></url>' for u in missing)
    if '</urlset>' not in sm: raise RuntimeError('sitemap closing tag missing')
    sm=sm.replace('</urlset>',block+'\n</urlset>')
    sp.write_text(sm,encoding='utf-8')
    print('sitemap added',len(missing))

css=r'''
/* V5 intent architecture — 2026-10-01 */
.travel-profile-icon--v5{font:500 36px/1 var(--serif);color:var(--navy)}
.v5-living-section{border-top:1px solid rgba(18,38,65,.12)}
'''
for rel in ('assets/v3.css','assets/site.css'):
    p=ROOT/rel
    if not p.exists(): continue
    s=p.read_text(encoding='utf-8')
    if 'V5 intent architecture — 2026-10-01' not in s:
        p.write_text(s.rstrip()+'\n\n'+css.strip()+'\n',encoding='utf-8')
        print('styled',rel)
