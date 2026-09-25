#!/usr/bin/env python3
from __future__ import annotations
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if os.environ.get("MAMETAS_ROOT"):
    ROOT = Path(os.environ["MAMETAS_ROOT"]).resolve()

changed = []

def save(rel, text, original):
    if text != original:
        (ROOT / rel).write_text(text, encoding="utf-8")
        changed.append(rel)

def patch_file(rel, pairs):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        text = text.replace(old, new)
    save(rel, text, original)

def add_home_product_proof(rel, lang):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if "v3-product-proof" in text:
        return

    if lang == "fr":
        block = '''<section class="v3-section v3-product-proof" aria-labelledby="product-proof-title"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">CE QUE MAMETAS FAIT DIFFÉREMMENT</p><h2 id="product-proof-title">On ne vous donne pas plus d’options. On vous aide à choisir.</h2></div><p>Trois couches, une seule logique : vos contraintes d’abord, les recommandations ensuite.</p></div><div class="product-proof-grid"><article class="product-proof-card"><span class="product-proof-number">01</span><p class="eyebrow">RIVIERA FIT</p><h3>5 jours · sans voiture · première visite · juin</h3><p class="product-proof-result"><strong>→ Nice</strong></p><p><b>Pourquoi :</b> meilleur réseau de transport et plus grande portée pour les excursions.</p><p><b>Pourquoi pas Cannes :</b> à choisir comme base si sable et soirées comptent davantage.</p><a href="/riviera-chooser/">Tester Riviera Fit →</a></article><article class="product-proof-card"><span class="product-proof-number">02</span><p class="eyebrow">HOTEL FIT</p><h3>€€ · calme · plage · couple</h3><p class="product-proof-result"><strong>→ une sélection courte, avec le compromis</strong></p><p>Pas une liste d’hôtels. Des adresses classées selon le rôle qu’elles doivent jouer dans votre séjour.</p><a href="/hotels/finder/">Ouvrir Hotel Fit →</a></article><article class="product-proof-card"><span class="product-proof-number">03</span><p class="eyebrow">REALITY CHECK</p><h3>Voiture · budget · saison · friction</h3><p class="product-proof-result"><strong>→ ce qui change vraiment la décision</strong></p><p>Un même lieu peut être excellent en juin sans voiture et pénible en août avec un programme trop ambitieux.</p><a href="/riviera-chooser/">Voir comment le verdict change →</a></article></div></div></section>'''
        anchor = '<section class="v3-section" id="bases">'
    else:
        block = '''<section class="v3-section v3-product-proof" aria-labelledby="product-proof-title"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">WHAT MAMETAS DOES DIFFERENTLY</p><h2 id="product-proof-title">We do not give you more options. We help you choose.</h2></div><p>Three layers, one logic: your constraints first, recommendations second.</p></div><div class="product-proof-grid"><article class="product-proof-card"><span class="product-proof-number">01</span><p class="eyebrow">RIVIERA FIT</p><h3>5 days · no car · first visit · June</h3><p class="product-proof-result"><strong>→ Nice</strong></p><p><b>Why:</b> strongest transport network and best reach for day trips.</p><p><b>Why not Cannes:</b> make it the base when sand and nightlife matter more.</p><a href="/en/riviera-chooser/">Try Riviera Fit →</a></article><article class="product-proof-card"><span class="product-proof-number">02</span><p class="eyebrow">HOTEL FIT</p><h3>€€ · quiet · beach · couple</h3><p class="product-proof-result"><strong>→ a short selection, with the catch</strong></p><p>Not a hotel list. Addresses ranked by the role they should play in your trip.</p><a href="/en/hotels/finder/">Open Hotel Fit →</a></article><article class="product-proof-card"><span class="product-proof-number">03</span><p class="eyebrow">REALITY CHECK</p><h3>Car · budget · season · friction</h3><p class="product-proof-result"><strong>→ what actually changes the decision</strong></p><p>The same place can be excellent in June without a car and irritating in August with an overpacked plan.</p><a href="/en/riviera-chooser/">See how the verdict changes →</a></article></div></div></section>'''
        anchor = '<section class="v3-section" id="bases">'

    if anchor not in text:
        raise RuntimeError(f"{rel}: homepage bases anchor not found")
    text = text.replace(anchor, block + "\n" + anchor, 1)
    save(rel, text, original)

def patch_home_hotel_selection(rel, lang):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text

    if lang == "fr":
        section_id = "hotels"
        new = '<div class="stay-intro"><p class="eyebrow">SÉLECTION COURTE · OÙ DORMIR À NICE</p><h2>Un bel hôtel peut rester le mauvais hôtel.</h2><p>Trois exemples pour montrer trois logiques de séjour. Ce n’est pas notre sélection complète. Nos cartes commencent par l’usage et se terminent par le compromis.</p><div class="hotel-selection-actions"><a class="button" href="/hotels/finder/?base=nice">Trouver mon hôtel avec Hotel Fit</a><a class="button secondary" href="/fr/dormir/nice/">Voir toute la sélection Nice</a></div></div>'
    else:
        section_id = "stay"
        new = '<div class="stay-intro"><p class="eyebrow">SHORT SELECTION · WHERE TO STAY IN NICE</p><h2>A beautiful hotel can still be the wrong hotel.</h2><p>Three examples, three different trip logics. This is not the full shortlist. Our cards start with the use case and end with the catch.</p><div class="hotel-selection-actions"><a class="button" href="/en/hotels/finder/?base=nice">Find my hotel with Hotel Fit</a><a class="button secondary" href="/stay/nice/">See the full Nice selection</a></div></div>'

    section_pattern = re.compile(
        rf'(<section class="v3-section" id="{section_id}"><div class="wrap stay-layout">)'
        r'<div class="stay-intro">.*?</div>(<div class="stay-list">)',
        re.S,
    )
    text, count = section_pattern.subn(r'\1' + new + r'\2', text, count=1)
    if count != 1:
        raise RuntimeError(f"{rel}: homepage hotel section not found")
    save(rel, text, original)

def rebrand_hotel_fit(rel, lang):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text

    if lang == "fr":
        pairs = [
            ("<title>Trouver votre hôtel sur la Côte d’Azur | Mametas</title>", "<title>Hotel Fit : quel hôtel correspond à votre séjour ? | Mametas</title>"),
            ('<p class="eyebrow">Le moteur hôtel Mametas</p>', '<p class="eyebrow">HOTEL FIT · LE MATCHING HÔTELIER MAMETAS</p>'),
            ("<h1>Parlez-nous de votre séjour. On fait le tri.</h1>", "<h1>Dites-nous comment vous voyagez. On réduit la liste.</h1>"),
            ("Choisissez vos critères, puis laissez Mametas couper dans la liste. Trois ou quatre adresses maximum — avec la raison et le compromis.", "Choisissez vos critères. Hotel Fit retient trois ou quatre adresses maximum, avec la raison, le compromis et ce qui les rend moins adaptées à d’autres séjours."),
            ("<p class=\"eyebrow\">Votre séjour</p><h2>Quatre choix. Puis seulement les hôtels qui collent.</h2>", "<p class=\"eyebrow\">VOTRE HOTEL FIT</p><h2>Cinq choix. Puis seulement les hôtels qui collent.</h2>"),
        ]
    else:
        pairs = [
            ("<title>Find your French Riviera hotel | Mametas</title>", "<title>Hotel Fit: which hotel fits your Riviera trip? | Mametas</title>"),
            ('<p class="eyebrow">The Mametas hotel finder</p>', '<p class="eyebrow">HOTEL FIT · THE MAMETAS HOTEL MATCHER</p>'),
            ("<h1>Tell us how you travel. We’ll make the shortlist.</h1>", "<h1>Tell us how you travel. We’ll cut the list down.</h1>"),
            ("Choose your criteria, then let Mametas cut the list down. Three or four addresses at most — with the reason and the catch.", "Choose your criteria. Hotel Fit keeps three or four addresses at most, with the reason, the catch and who each hotel is less suited to."),
            ("<p class=\"eyebrow\">Your trip</p><h2>Four choices. Then only the hotels that fit.</h2>", "<p class=\"eyebrow\">YOUR HOTEL FIT</p><h2>Five choices. Then only the hotels that fit.</h2>"),
        ]
    for old, new in pairs:
        text = text.replace(old, new)
    save(rel, text, original)

def add_css():
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 product surface 2026-09-25 */"
    if marker in text:
        return
    text += r'''

/* V3 product surface 2026-09-25 */
.v3-product-proof{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(23,54,95,.025)}
.product-proof-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:26px}
.product-proof-card{position:relative;min-height:330px;padding:24px;border:1px solid var(--line);background:rgba(255,253,248,.72)}
.product-proof-number{position:absolute;top:18px;right:20px;color:var(--coral);font-family:var(--serif);font-size:26px;font-style:italic}
.product-proof-card h3{max-width:85%;margin:12px 0 20px;font-family:var(--serif);font-size:clamp(24px,2.5vw,31px);font-weight:500;line-height:1.08}
.product-proof-card p{margin:9px 0;color:var(--ink-soft);font-size:12px;line-height:1.58}
.product-proof-card p b{color:var(--ink)}
.product-proof-result{padding:13px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);color:var(--ink)!important}
.product-proof-result strong{font-family:var(--serif);font-size:21px;font-weight:500}
.product-proof-card>a{display:inline-block;margin-top:16px;padding-bottom:2px;border-bottom:1px solid var(--coral);color:var(--ink);font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;text-decoration:none}
.hotel-selection-actions{display:flex;flex-wrap:wrap;gap:9px;margin-top:20px}
@media(max-width:900px){.product-proof-grid{grid-template-columns:1fr}.product-proof-card{min-height:0}}
@media(max-width:760px){.hotel-selection-actions .button{width:100%;justify-content:center}}
'''
    save("assets/v3.css", text, original)

def validate():
    checks = {
        "index.html": ("v3-product-proof", "Open Hotel Fit", "SHORT SELECTION · WHERE TO STAY IN NICE"),
        "fr/index.html": ("v3-product-proof", "Trouver mon hôtel avec Hotel Fit", "SÉLECTION COURTE · OÙ DORMIR À NICE"),
        "hotels/finder/index.html": ("HOTEL FIT · LE MATCHING HÔTELIER MAMETAS", "Cinq choix. Puis seulement les hôtels qui collent."),
        "en/hotels/finder/index.html": ("HOTEL FIT · THE MAMETAS HOTEL MATCHER", "Five choices. Then only the hotels that fit."),
        "assets/v3.css": ("/* V3 product surface 2026-09-25 */", ".product-proof-grid", ".hotel-selection-actions"),
    }
    errors = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
    if errors:
        raise SystemExit("V3 product surface validation failed:\n- " + "\n- ".join(errors))

def main():
    add_home_product_proof("index.html", "en")
    add_home_product_proof("fr/index.html", "fr")
    patch_home_hotel_selection("index.html", "en")
    patch_home_hotel_selection("fr/index.html", "fr")
    rebrand_hotel_fit("hotels/finder/index.html", "fr")
    rebrand_hotel_fit("en/hotels/finder/index.html", "en")
    add_css()
    validate()
    print(f"V3 product surface passed; patched {len(changed)} generated file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
