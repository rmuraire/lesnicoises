#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re
import html

ROOT=Path(__file__).resolve().parents[1]
SKIP_TOP={'.git','.github','docs','scripts','data','backup','lesnicoises-v8-no-mercy-update','lesnicoises-v8-no-mercy-update 2'}

def page_lang(s,rel):
    m=re.search(r'<html\b[^>]*\blang=["\']([^"\']+)',s,re.I)
    if m: return 'fr' if m.group(1).lower().startswith('fr') else 'en'
    return 'en' if rel.startswith(('en/','plan/','stay/')) else 'fr'

def replace_href(attrs,new_href):
    return re.sub(r'(\bhref\s*=\s*["\'])[^"\']*(["\'])',lambda m:m.group(1)+new_href+m.group(2),attrs,count=1,flags=re.I)

def plain_anchor_pass(s,lang):
    patt=re.compile(r'<a(?P<attrs>[^>]*)>(?P<text>[^<>]{1,120})</a>',re.I)
    def cb(m):
        attrs=m.group('attrs'); raw=m.group('text'); text=html.unescape(raw).strip()
        hm=re.search(r'\bhref\s*=\s*["\']([^"\']+)',attrs,re.I)
        if not hm or text in {'FR','EN'}: return m.group(0)
        href=hm.group(1); low=href.lower()
        out_text=None; new_href=href
        if 'riviera-fit' in low or 'riviera-chooser' in low or low.endswith('#riviera-fit'):
            new_href='/en/riviera-fit/' if lang=='en' else '/riviera-fit/'
            if ('profile' in text.lower()) or ('profil' in text.lower()):
                out_text='Run my profile through Riviera Fit →' if lang=='en' else 'Tester mon profil dans Riviera Fit →'
            else:
                out_text='Try Riviera Fit →' if lang=='en' else 'Tester Riviera Fit →'
        elif '/hotels/finder/' in low:
            out_text='Try Hotel Fit →' if lang=='en' else 'Tester Hotel Fit →'
        else:
            norm=text.lower().replace('→','').strip()
            hotel_review_en={'see our full take','see the hotel','mametas hotel page','mametas hotel take','see our full review','read our full review'}
            hotel_review_fr={'voir notre avis','voir la fiche hôtel','fiche hôtel mametas','notre avis','lire notre avis complet'}
            if (lang=='en' and norm in hotel_review_en) or (lang=='fr' and norm in hotel_review_fr):
                out_text='Read our full review →' if lang=='en' else 'Lire notre avis complet →'
        if out_text is None: return m.group(0)
        attrs2=replace_href(attrs,new_href) if new_href!=href else attrs
        return '<a'+attrs2+'>'+out_text+'</a>'
    return patt.sub(cb,s)

def booking_button_pass(s,lang):
    patt=re.compile(r'<a(?P<attrs>[^>]*class=["\'][^"\']*(?:cta-button|booking-quiet-cta)[^"\']*["\'][^>]*)>(?P<text>[^<>]{1,100})</a>',re.I)
    def cb(m):
        attrs=m.group('attrs')
        hm=re.search(r'\bhref\s*=\s*["\']([^"\']+)',attrs,re.I)
        if not hm: return m.group(0)
        href=html.unescape(hm.group(1)); low=href.lower()
        if 'booking.com' in low or 'kqzyfj.com' in low:
            txt='Check rates on Booking.com' if lang=='en' else 'Voir les tarifs sur Booking.com'
        elif 'expedia.' in low:
            txt='Check rates on Expedia' if lang=='en' else 'Voir les tarifs sur Expedia'
        else:
            return m.group(0)
        return '<a'+attrs+'>'+txt+'</a>'
    return patt.sub(cb,s)

def main():
    changed=0
    for p in ROOT.rglob('*.html'):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP: continue
        s=p.read_text(encoding='utf-8',errors='ignore')
        before=s; lang=page_lang(s,rel.as_posix())
        s=re.sub(r'href=(["\'])/en/riviera-chooser/\1',r'href=\1/en/riviera-fit/\1',s,flags=re.I)
        s=re.sub(r'href=(["\'])/riviera-chooser/\1',r'href=\1/riviera-fit/\1',s,flags=re.I)
        s=re.sub(r'href=(["\'])/#riviera-fit\1',r'href=\1/en/riviera-fit/\1' if lang=='en' else r'href=\1/riviera-fit/\1',s,flags=re.I)
        s=plain_anchor_pass(s,lang)
        s=booking_button_pass(s,lang)
        if s!=before:
            p.write_text(s,encoding='utf-8'); changed+=1
    print('V6 CTA lexicon normalized on',changed,'HTML files')

if __name__=='__main__': main()
