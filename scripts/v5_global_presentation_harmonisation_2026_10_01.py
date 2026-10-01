#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Global presentation harmonisation for Mametas editorial pages — 2026-10-01."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
MARK="V5 global presentation harmonisation — 2026-10-01"

CSS=r'''
/* V5 global presentation harmonisation — 2026-10-01 */
:root{--mametas-coral:#d86c4e;--mametas-coral-soft:#f6e4dd}

/* One editorial hero rule: calm 16:9 media at the same reading width. */
.intent-detail .article-cover,
.article .solo-female-hero,
.article .universal-editorial-hero{
  width:min(100%,820px)!important;
  max-width:820px!important;
  height:auto!important;
  aspect-ratio:16/9!important;
  margin:0 auto 42px!important;
  overflow:hidden;
  position:relative;
  background:var(--cream-deep,#efe7d6);
}
.intent-detail .article-cover img,
.article .solo-female-hero img,
.article .universal-editorial-hero img{
  width:100%!important;height:100%!important;aspect-ratio:16/9!important;object-fit:cover!important;
}
.article .universal-editorial-hero figcaption,
.article .solo-female-hero figcaption{
  margin-top:8px;font-size:10.5px;line-height:1.45;color:var(--ink,#4b5266);
}

/* FAQ and sources always sit on the editorial axis, even when generated outside article-body. */
.intent-detail > .intent-faq,
.intent-detail > .sources{
  width:min(calc(100% - 2 * var(--gutter)),780px)!important;
  max-width:780px!important;
  margin-left:auto!important;
  margin-right:auto!important;
}
.article > .intent-faq{width:100%;max-width:100%;margin-left:auto;margin-right:auto}

/* Shared table treatment, including Gay pages that do not carry .intent-detail. */
.article .table-wrap,
.intent-detail .table-wrap{
  width:100%;margin:20px 0 36px;overflow-x:auto;-webkit-overflow-scrolling:touch;
  border:1px solid var(--line);background:rgba(255,253,248,.55);
}
.article .intent-table,
.intent-detail .intent-table{
  width:100%;min-width:640px;border-collapse:collapse;color:var(--ink-soft,var(--ink));
  font-size:12.5px;line-height:1.5;
}
.article .intent-table th,
.intent-detail .intent-table th{
  padding:12px 14px;background:var(--navy,var(--ink));color:#fff;font-size:9px;font-weight:700;
  letter-spacing:.12em;text-align:left;text-transform:uppercase;vertical-align:bottom;
}
.article .intent-table td,
.intent-detail .intent-table td{
  padding:14px;border-top:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top;
}
.article .intent-table td:last-child,.article .intent-table th:last-child,
.intent-detail .intent-table td:last-child,.intent-detail .intent-table th:last-child{border-right:0}
.article .intent-table tbody tr:first-child td,.intent-detail .intent-table tbody tr:first-child td{border-top:0}
.article .intent-table strong,.intent-detail .intent-table strong{color:var(--navy,var(--ink))}

/* Shared FAQ treatment. */
.article .intent-faq,
.intent-detail .intent-faq{margin-top:50px;padding-top:26px;border-top:1px solid var(--line)}
.article .intent-faq h2,.intent-detail .intent-faq h2{margin:0 0 12px}
.article .intent-faq details,.intent-detail .intent-faq details{border-top:1px solid var(--line)}
.article .intent-faq details:last-child,.intent-detail .intent-faq details:last-child{border-bottom:1px solid var(--line)}
.article .intent-faq summary,.intent-detail .intent-faq summary{
  position:relative;padding:17px 34px 17px 0;color:var(--navy,var(--ink));cursor:pointer;
  font-family:var(--serif);font-size:18px;font-weight:500;line-height:1.35;list-style:none;
}
.article .intent-faq summary::-webkit-details-marker,.intent-detail .intent-faq summary::-webkit-details-marker{display:none}
.article .intent-faq summary::after,.intent-detail .intent-faq summary::after{
  content:"+";position:absolute;right:2px;top:15px;color:var(--med-blue,#3c7186);
  font-family:var(--sans);font-size:20px;font-weight:400;
}
.article .intent-faq details[open] summary::after,.intent-detail .intent-faq details[open] summary::after{content:"–"}
.article .intent-faq details p,.intent-detail .intent-faq details p{
  max-width:690px;margin:0 0 18px!important;color:var(--ink)!important;font-size:14px!important;line-height:1.68!important;
}

/* Sources: compact reference strip rather than a second article. */
.article .sources,.intent-detail .sources{margin-top:48px;padding-top:22px;border-top:1px solid var(--line)}
.article .sources h2,.intent-detail .sources h2{
  margin:0 0 14px;font-family:var(--sans);font-size:10px;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:var(--med-blue,#3c7186)
}
.article .sources ul,.intent-detail .sources ul{
  display:flex;flex-wrap:wrap;gap:7px 0;list-style:none;margin:0;padding:0;
}
.article .sources li,.intent-detail .sources li{
  display:inline;margin:0;padding:0;color:var(--ink);font-size:11px;line-height:1.5;
}
.article .sources li:not(:last-child)::after,.intent-detail .sources li:not(:last-child)::after{
  content:"·";display:inline-block;margin:0 10px;color:rgba(20,33,61,.35);
}
.article .sources a,.intent-detail .sources a{text-decoration:underline;text-underline-offset:3px}

/* One Booking CTA language and one visual weight. */
.hotel-card-cta,
.booking-quiet-cta{
  display:inline-flex!important;align-items:center!important;justify-content:center!important;
  width:auto!important;min-height:38px!important;padding:9px 14px!important;border:1px solid var(--navy,#16223d)!important;
  border-radius:999px!important;background:var(--navy,#16223d)!important;color:#fff!important;
  font-family:var(--sans)!important;font-size:10px!important;font-weight:800!important;
  letter-spacing:.065em!important;line-height:1!important;text-transform:uppercase!important;text-decoration:none!important;
}
.hotel-card-take{
  min-height:38px!important;padding:9px 14px!important;border-radius:999px!important;
  background:transparent!important;border:1px solid rgba(20,33,61,.18)!important;color:var(--navy,#16223d)!important;
}
.booking-quiet-cta:hover,.hotel-card-cta:hover{opacity:.88}

/* Share: visible, but secondary to conversion. */
.mametas-share-button{
  border:1px solid var(--mametas-coral)!important;background:var(--mametas-coral-soft)!important;
  color:#813b2c!important;font-size:9.5px!important;font-weight:800!important;padding:8px 12px!important;
  box-shadow:none!important;
}
.mametas-share-button:hover,.mametas-share-button:focus-visible{
  background:#efd5cb!important;border-color:#c75d42!important;color:#6f3024!important;transform:none!important;
}

/* Keep profile-card imagery disciplined. */
.travel-profile-media{overflow:hidden;background:var(--cream-deep,#efe7d6)}
.travel-profile-media img{width:100%;height:100%;object-fit:cover}

@media(max-width:760px){
  .intent-detail > .intent-faq,.intent-detail > .sources{width:calc(100% - 2 * var(--gutter))!important}
  .article .intent-table,.intent-detail .intent-table{min-width:600px}
  .article .sources li,.intent-detail .sources li{font-size:10.5px}
}
'''

EN_NAV=[
 ("/plan/","Plan"),("/en/riviera-guide/","Places"),("/en/hotels/","Stay"),
 ("/en/explore/","Explore"),("/en/practical/","Practical")
]
FR_NAV=[
 ("/fr/planifier/","Préparer"),("/riviera-guide/","Destinations"),("/hotels/","Dormir"),
 ("/explore/","Explorer"),("/pratique/","Pratique")
]

def current_index(rel, lang):
    p="/"+rel.replace("index.html","")
    if lang=="en":
        if "/practical/" in p or "/good-finds/" in p: return 4
        if "/explore/" in p or "/gay-" in p or "/solo-female-" in p: return 3
        if "/hotels/" in p or "/stay/" in p: return 2
        if "/riviera-guide/" in p: return 1
        if "/plan/" in p or "/riviera-" in p: return 0
    else:
        if "/pratique/" in p or "/bons-plans/" in p: return 4
        if "/explore/" in p or "gay" in p or "femme-solo" in p: return 3
        if "/hotels/" in p or "/dormir/" in p: return 2
        if "/riviera-guide/" in p: return 1
        if "/planifier/" in p or "/riviera-" in p: return 0
    return None

def nav_ul(items, active):
    out=[]
    for i,(href,label) in enumerate(items):
        cur=' aria-current="page"' if active==i else ''
        out.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return '<ul>'+''.join(out)+'</ul>'

def harmonise_nav(s, rel, lang):
    items=EN_NAV if lang=="en" else FR_NAV
    ul=nav_ul(items,current_index(rel,lang))
    # Desktop nav.
    s=re.sub(
      r'(<nav\s+class="(?:v3-nav|primary-nav)"[^>]*>)<ul>[\s\S]*?</ul>(</nav>)',
      lambda m:m.group(1)+ul+m.group(2),s,count=1
    )
    # Mobile nav: support both site.css and V3 menu generations.
    for mobile_class in ("mobile-nav","mobile-menu"):
        pattern='(<div class="'+mobile_class+'"[^>]*>.*?)(<ul>.*?</ul>)(.*?</div>)'
        m=re.search(pattern,s,re.S)
        if m:
            s=s[:m.start()]+m.group(1)+ul+m.group(3)+s[m.end():]
            break
    return s

def add_class(attr, cls):
    if 'class="' in attr:
        return re.sub(r'class="([^"]*)"',lambda m:f'class="{m.group(1)} {cls}"' if cls not in m.group(1).split() else m.group(0),attr,1)
    return attr[:-1]+f' class="{cls}">'

def harmonise_booking_ctas(s, lang):
    label="Check dates" if lang=="en" else "Voir les disponibilités"
    pat=re.compile(r'<a([^>]*href="https://www\.kqzyfj\.com/click-101875476-15734754[^"]*"[^>]*)>([\s\S]*?)</a>',re.I)
    def repl(m):
        attrs=m.group(1)
        inner=re.sub(r'<[^>]+>',' ',m.group(2))
        text=' '.join(inner.split()).lower()
        if 'hotel-card-cta' in attrs:
            return m.group(0)
        if ('booking' in text or 'check rate' in text or 'voir les tarifs' in text or 'rates on' in text):
            full='<a'+attrs+'>'
            full=add_class(full,'booking-quiet-cta')
            return full+label+'</a>'
        return m.group(0)
    return pat.sub(repl,s)

def patch_html(p):
    rel=p.relative_to(ROOT).as_posix()
    s=p.read_text(encoding="utf-8",errors="ignore")
    original=s
    lang="fr" if re.search(r'<html[^>]+lang="fr',s,re.I) else "en"
    s=harmonise_nav(s,rel,lang)
    s=harmonise_booking_ctas(s,lang)

    # Cache-bust the unified presentation layer on every generated page.
    s=re.sub(r'/assets/site[.]css(?:[?]v=[^"]+)?','/assets/site.css?v=24.1',s)
    s=re.sub(r'/assets/v3[.]css(?:[?]v=[^"]+)?','/assets/v3.css?v=1.3',s)
    s=re.sub(r'/assets/site[.]js(?:[?]v=[^"]+)?','/assets/site.js?v=1.4',s)
    s=re.sub(r'/assets/v3[.]js(?:[?]v=[^"]+)?','/assets/v3.js?v=0.8',s)

    # Gay Riviera: correct social image and add a proper visible hero.
    if rel in ("en/gay-french-riviera/index.html","cote-dazur-gay/index.html"):
        s=s.replace("https://www.mametas.com/assets/editorial/mametas-five-women-hero.webp",
                    "https://www.mametas.com/assets/editorial/refonte-2026/gay-riviera.webp")
        if "/assets/editorial/refonte-2026/gay-riviera.webp" not in s.split("<main",1)[-1]:
            credit="Photo: den-cops / Pexels"
            alt="Gay travellers on the French Riviera" if lang=="en" else "Voyageurs gay sur la Côte d’Azur"
            fig=(f'<figure class="universal-editorial-hero"><img src="/assets/editorial/refonte-2026/gay-riviera.webp" '
                 f'alt="{alt}" loading="eager"><figcaption>{credit}</figcaption></figure>')
            stand=re.search(r'(<p class="standfirst">[\s\S]*?</p>)',s)
            if stand:
                s=s[:stand.end()]+fig+s[stand.end():]

    # Solo evenings page: Menton was the wrong city.
    if rel in ("en/solo-female-french-riviera/eating-going-out-alone/index.html",
               "cote-dazur-femme-solo/manger-sortir-seule/index.html"):
        s=s.replace('/assets/editorial/menton-evening.jpg','/assets/editorial/nice-riviera.jpg')
        s=s.replace('alt="An evening on the French Riviera"','alt="Nice on the French Riviera"')
        s=s.replace('alt="Une soirée sur la Côte d’Azur"','alt="Nice sur la Côte d’Azur"')

    if s!=original:
        p.write_text(s,encoding="utf-8")
        return True
    return False

changed=[]
skip_top={".git",".github","docs","scripts","data","lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}
for p in ROOT.rglob("*.html"):
    rel=p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in skip_top: continue
    if patch_html(p): changed.append(rel.as_posix())

for rel in ("assets/site.css","assets/v3.css"):
    p=ROOT/rel
    if not p.exists(): continue
    s=p.read_text(encoding="utf-8")
    if MARK not in s:
        p.write_text(s.rstrip()+"\n\n"+CSS.strip()+"\n",encoding="utf-8")
        changed.append(rel)

print(f"Global presentation harmonisation updated {len(changed)} files")
for rel in changed[:120]: print(rel)
