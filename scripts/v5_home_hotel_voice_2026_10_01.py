# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARK = 'home-hotel-voice-daniel-2026-03'

VOICES = {
    'index.html': (
        'IN THEIR OWN WORDS',
        '“Our location in Cannes was great, but the apartment was super drafty and freezing at night, and the place felt pretty rustic. Honestly, next time we’re definitely booking a hotel with proper heating.”',
        '<strong>Daniel</strong> · Berlin · couple · March 2026',
        r'(<h2>A beautiful hotel can still be the wrong hotel\.</h2>\s*<p>.*?</p>)',
    ),
    'fr/index.html': (
        'ILS L’ONT VÉCU',
        '« Notre emplacement à Cannes était super, mais l’appartement était plein de courants d’air et glacial la nuit, et l’endroit était assez rustique. Franchement, la prochaine fois, on réservera clairement un hôtel avec un vrai chauffage. »',
        '<strong>Daniel</strong> · Berlin · en couple · mars 2026',
        r'(<h2>Un bel hôtel peut rester le mauvais hôtel\.</h2>\s*<p>.*?</p>)',
    ),
}

for rel, (kicker, quote, meta, pattern) in VOICES.items():
    p = ROOT / rel
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('unchanged', rel)
        continue
    block = f'''<div class="home-hotel-voice" data-home-hotel-voice="{MARK}"><span>{kicker}</span><blockquote>{quote}</blockquote><p>{meta}</p></div>'''
    new, n = re.subn(pattern, lambda m: m.group(1) + '\n' + block, s, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f'Hotel Fit intro not found in {rel}')
    p.write_text(new, encoding='utf-8')
    print('patched', rel)

css = r'''
/* Homepage Hotel Fit traveller voice — 2026-10-01 */
.home-hotel-voice{
  margin:22px 0 20px;
  padding:17px 0 0;
  border-top:1px solid rgba(20,33,61,.18);
}
.home-hotel-voice>span{
  display:block;
  margin-bottom:8px;
  color:#17748a;
  font-size:9px;
  font-weight:800;
  letter-spacing:.13em;
  text-transform:uppercase;
}
.home-hotel-voice blockquote{
  margin:0;
  color:#14213d;
  font-family:var(--serif,"Fraunces",Georgia,serif);
  font-size:17px;
  font-weight:400;
  line-height:1.45;
}
.home-hotel-voice p{
  margin:9px 0 0!important;
  color:#5f6570!important;
  font-size:10px!important;
  line-height:1.4!important;
}
@media(max-width:650px){
  .home-hotel-voice{margin:18px 0 18px;padding-top:14px}
  .home-hotel-voice blockquote{font-size:16px}
}
'''
for rel in ('assets/v3.css','assets/site.css'):
    p = ROOT / rel
    if not p.exists():
        continue
    s = p.read_text(encoding='utf-8')
    if 'Homepage Hotel Fit traveller voice — 2026-10-01' not in s:
        p.write_text(s.rstrip() + '\n\n' + css.strip() + '\n', encoding='utf-8')
        print('styled', rel)
