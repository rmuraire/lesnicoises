#!/usr/bin/env python3
from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if os.environ.get("MAMETAS_ROOT"):
    ROOT = Path(os.environ["MAMETAS_ROOT"]).resolve()

def patch_about(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    if 'data-editor-identity="true"' in text:
        return
    if lang == "fr":
        anchor = '<h2>D’où vient Mametas</h2>'
        block = '''<section class="editor-identity" data-editor-identity="true"><span class="kicker">ÉDITEUR</span><h2>Créé et édité par Renaud Muraire.</h2><p>Niçois, Renaud a grandi avec la Côte d’Azur comme territoire familier, pas comme décor de brochure. Mametas combine cette connaissance personnelle avec un travail documenté sur les sources officielles, la géographie, les transports et les informations pratiques. Lorsqu’un lieu n’a pas été visité personnellement, le site ne prétend pas le contraire.</p><p><a href="/methode/">Lire la méthode Mametas Checked →</a> · <a href="/presse/">Presse & professionnels →</a></p></section>'''
    else:
        anchor = '<h2>Where Mametas comes from</h2>'
        block = '''<section class="editor-identity" data-editor-identity="true"><span class="kicker">EDITOR</span><h2>Created and edited by Renaud Muraire.</h2><p>A Niçois, Renaud grew up with the French Riviera as familiar territory rather than brochure scenery. Mametas combines that personal knowledge with documented work on official sources, geography, transport and practical information. When somewhere has not been personally visited, the site does not pretend otherwise.</p><p><a href="/en/method/">Read the Mametas Checked method →</a> · <a href="/en/press/">Press & professionals →</a></p></section>'''
    if anchor not in text:
        raise RuntimeError(f"{rel}: About anchor missing")
    text = text.replace(anchor, block + anchor, 1)
    p.write_text(text, encoding="utf-8")

def page(lang: str) -> str:
    if lang == "fr":
        return '''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Presse & professionnels | Mametas</title><meta name="description" content="Mametas en une phrase, sa méthode, ses outils Riviera Fit et Hotel Fit, et le contact presse et professionnels du tourisme."><link rel="canonical" href="https://www.mametas.com/presse/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/presse/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/en/press/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/en/press/"><meta name="robots" content="index,follow"><link rel="stylesheet" href="/assets/v3.css?v=1.2"><link href="/favicon.svg" rel="icon" type="image/svg+xml"></head><body><header class="v3-header"><div class="v3-header-inner"><a class="v3-brand" href="/fr/"><span class="v3-brand-name">Mametas</span><span class="v3-brand-line">They know the Riviera.</span></a><nav class="v3-nav"><ul><li><a href="/riviera-chooser/">Planifier</a></li><li><a href="/riviera-guide/">Lieux</a></li><li><a href="/hotels/">Dormir</a></li><li><a href="/explore/">Explorer</a></li><li><a href="/bons-plans/">Maintenant</a></li></ul></nav><div class="lang-switch"><a aria-current="page" href="/presse/">FR</a><span>/</span><a href="/en/press/">EN</a></div></div></header><main><header class="article-hero"><div class="wrap"><p class="eyebrow">PRESSE & PROFESSIONNELS</p><h1>Un guide qui tranche, puis montre son raisonnement.</h1><p class="article-deck">Mametas transforme la Côte d’Azur en problème de décision : où dormir, faut-il une voiture, quel hôtel correspond au séjour, quelle friction accepter et ce qu’on peut laisser tomber sans regret.</p></div></header><section class="v3-section"><div class="wrap press-grid"><article><span>01</span><h2>Mametas en une phrase</h2><p>La plupart des guides disent ce qu’il y a. Mametas dit ce qui vous correspond, et ce qu’il vaut mieux éviter.</p></article><article><span>02</span><h2>Les trois produits</h2><p><strong>Riviera Fit</strong> choisit une base. <strong>Hotel Fit</strong> réduit la sélection d’hôtels selon le séjour. <strong>Reality Check</strong> expose voiture, budget, saison et friction.</p></article><article><span>03</span><h2>La méthode</h2><p>Sources identifiables, dates de vérification visibles et séparation nette entre faits vérifiés et jugement éditorial. <a href="/methode/">Voir Mametas Checked →</a></p></article><article><span>04</span><h2>Éditeur</h2><p>Mametas est créé et édité par Renaud Muraire, Niçois. Les cinq Mametas sont des personnages éditoriaux fictifs. <a href="/a-propos/">À propos →</a></p></article></div><div class="wrap press-contact"><p class="eyebrow">CONTACT</p><h2>Journalistes, offices de tourisme, hôtels et acteurs de la Riviera.</h2><p>Pour une information, un visuel, une correction documentée, une interview ou un partenariat éditorial : <a href="mailto:hello@mametas.com">hello@mametas.com</a>.</p></div></section></main><footer class="v3-footer"><div class="wrap"><div class="footer-bottom"><span>Sélection éditoriale indépendante.</span><span>© 2026 Mametas</span></div></div></footer><script src="/assets/v3.js?v=0.9"></script></body></html>'''
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Press & professionals | Mametas</title><meta name="description" content="Mametas in one sentence, its method, Riviera Fit and Hotel Fit, plus press and tourism-industry contact details."><link rel="canonical" href="https://www.mametas.com/en/press/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/presse/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/en/press/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/en/press/"><meta name="robots" content="index,follow"><link rel="stylesheet" href="/assets/v3.css?v=1.2"><link href="/favicon.svg" rel="icon" type="image/svg+xml"></head><body><header class="v3-header"><div class="v3-header-inner"><a class="v3-brand" href="/"><span class="v3-brand-name">Mametas</span><span class="v3-brand-line">They know the Riviera.</span></a><nav class="v3-nav"><ul><li><a href="/en/riviera-chooser/">Plan</a></li><li><a href="/en/riviera-guide/">Places</a></li><li><a href="/en/hotels/">Stay</a></li><li><a href="/en/explore/">Explore</a></li><li><a href="/en/good-finds/">Now</a></li></ul></nav><div class="lang-switch"><a href="/presse/">FR</a><span>/</span><a aria-current="page" href="/en/press/">EN</a></div></div></header><main><header class="article-hero"><div class="wrap"><p class="eyebrow">PRESS & PROFESSIONALS</p><h1>A guide that makes the call, then shows its reasoning.</h1><p class="article-deck">Mametas turns the French Riviera into a decision problem: where to stay, whether you need a car, which hotel fits the trip, which friction is worth accepting and what you can skip without regret.</p></div></header><section class="v3-section"><div class="wrap press-grid"><article><span>01</span><h2>Mametas in one sentence</h2><p>Most Riviera guides tell you what’s there. Mametas tells you what fits, and what to skip.</p></article><article><span>02</span><h2>The three products</h2><p><strong>Riviera Fit</strong> chooses a base. <strong>Hotel Fit</strong> narrows the hotel selection to the trip. <strong>Reality Check</strong> exposes car, budget, season and friction.</p></article><article><span>03</span><h2>The method</h2><p>Identifiable sources, visible check dates and a clear separation between checked facts and editorial judgement. <a href="/en/method/">See Mametas Checked →</a></p></article><article><span>04</span><h2>Editor</h2><p>Mametas is created and edited by Renaud Muraire, a Niçois. The five Mametas are fictional editorial characters. <a href="/en/about/">About →</a></p></article></div><div class="wrap press-contact"><p class="eyebrow">CONTACT</p><h2>Journalists, tourist offices, hotels and Riviera professionals.</h2><p>For information, imagery, a documented correction, an interview or an editorial partnership: <a href="mailto:hello@mametas.com">hello@mametas.com</a>.</p></div></section></main><footer class="v3-footer"><div class="wrap"><div class="footer-bottom"><span>Independent editorial selection.</span><span>© 2026 Mametas</span></div></div></footer><script src="/assets/v3.js?v=0.9"></script></body></html>'''

def add_css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    marker = "/* V3 credibility layer 2026-09-25 */"
    if marker not in text:
        text += '''
/* V3 credibility layer 2026-09-25 */
.editor-identity{margin:18px 0 36px;padding:24px 26px;border:1px solid var(--line);background:rgba(23,54,95,.035)}
.editor-identity h2{margin:7px 0 12px}
.editor-identity p{max-width:820px}
.press-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.press-grid article{padding:26px;background:var(--paper)}
.press-grid article>span{color:var(--coral);font-family:var(--serif);font-size:22px;font-style:italic}
.press-grid h2{margin:10px 0;font-family:var(--serif);font-size:28px;font-weight:500}
.press-grid p,.press-contact p{color:var(--ink-soft);font-size:13px;line-height:1.65}
.press-contact{margin-top:40px;padding:28px;border-left:3px solid var(--coral);background:rgba(255,253,248,.55)}
.press-contact h2{max-width:760px;margin:8px 0 12px;font-family:var(--serif);font-size:clamp(28px,4vw,42px);font-weight:500}
@media(max-width:720px){.press-grid{grid-template-columns:1fr}}
'''
        p.write_text(text,encoding="utf-8")

def main() -> int:
    patch_about("a-propos/index.html","fr")
    patch_about("en/about/index.html","en")
    for rel,lang in (("presse/index.html","fr"),("en/press/index.html","en")):
        p=ROOT/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(page(lang),encoding="utf-8")
    add_css()
    sitemap = ROOT / "sitemap.xml"
    sm = sitemap.read_text(encoding="utf-8")
    entries = [
        '  <url><loc>https://www.mametas.com/presse/</loc><lastmod>2026-09-25</lastmod></url>',
        '  <url><loc>https://www.mametas.com/en/press/</loc><lastmod>2026-09-25</lastmod></url>',
    ]
    for entry in entries:
        if entry not in sm:
            sm = sm.replace("</urlset>", entry + "\n</urlset>")
    sitemap.write_text(sm, encoding="utf-8")
    print("V3 credibility layer passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
