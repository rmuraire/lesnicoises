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


def patch_home_riviera_fit(rel, lang):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text

    # Riviera Fit is the single signature product on the homepage.
    text = re.sub(r'<section class="v3-section v3-product-proof".*?</section>\s*', '', text, count=1, flags=re.S)

    if lang == "fr":
        block = '''<section class="v3-section chooser-signature-section chooser-signature-section--fit" id="planifier"><div class="wrap riviera-fit-home"><div class="riviera-fit-home-copy"><p class="eyebrow">RIVIERA FIT · LA RECO MAMETAS</p><h2>Choisissez la bonne base avant le reste.</h2><p class="riviera-fit-home-punch"><a href="/lexique/#pichoun">Pichoun</a>, choisissez la ville avant le peignoir.</p><p>Durée, saison, mobilité, envies, rythme. Riviera Fit tranche entre Nice, Cannes, Antibes, Menton et les autres bases, puis explique pourquoi le choix fonctionne et ce que vous perdez en écartant les alternatives.</p><a class="button chooser-signature-primary" href="/riviera-chooser/">Tester Riviera Fit</a></div><div class="riviera-fit-home-demo" aria-label="Exemple de résultat Riviera Fit"><p class="riviera-fit-demo-label">EXEMPLE · VOTRE SÉJOUR</p><div class="riviera-fit-demo-chips"><span>5 jours</span><span>Sans voiture</span><span>Premier séjour</span><span>Juin</span><span>Équilibré</span></div><div class="riviera-fit-home-verdict"><p class="riviera-fit-demo-label">LA RECO MAMETAS</p><h3>Posez vos valises à Nice.</h3><p><strong>Pourquoi :</strong> meilleur réseau de transport et plus grande portée pour les excursions.</p><p><strong>Pourquoi pas Cannes :</strong> choisissez-la plutôt si sable et soirées comptent davantage.</p><div class="riviera-fit-reality"><span>Sans voiture <b>Excellent</b></span><span>Budget <b>€€</b></span><span>Friction <b>Faible</b></span><span>Saison <b>Très bonne</b></span></div></div></div></div></section>'''
        text = text.replace('>Lancer le Riviera Chooser</a>', '>Tester Riviera Fit</a>')
        text = text.replace('<a class="button" href="/hotels/finder/?base=nice">Trouver mon hôtel avec Hotel Fit</a><a class="button secondary" href="/fr/dormir/nice/">Voir toute la sélection Nice</a>',
                            '<a class="button" href="/hotels/">Explorer la rubrique Dormir</a><a class="button secondary" href="/fr/dormir/nice/">Voir toute la sélection Nice</a>')
        section_id = "planifier"
    else:
        block = '''<section class="v3-section chooser-signature-section chooser-signature-section--fit" id="plan"><div class="wrap riviera-fit-home"><div class="riviera-fit-home-copy"><p class="eyebrow">RIVIERA FIT · THE MAMETAS CALL</p><h2>Choose the right base before everything else.</h2><p class="riviera-fit-home-punch"><a href="/en/lexicon/#pichoun">Pichoun</a>, choose the town before the bathrobe.</p><p>Duration, season, mobility, priorities, pace. Riviera Fit makes the call between Nice, Cannes, Antibes, Menton and the other bases, then explains why the choice works and what you give up by skipping the alternatives.</p><a class="button chooser-signature-primary" href="/en/riviera-chooser/">Try Riviera Fit</a></div><div class="riviera-fit-home-demo" aria-label="Example Riviera Fit result"><p class="riviera-fit-demo-label">EXAMPLE · YOUR TRIP</p><div class="riviera-fit-demo-chips"><span>5 days</span><span>No car</span><span>First visit</span><span>June</span><span>Balanced</span></div><div class="riviera-fit-home-verdict"><p class="riviera-fit-demo-label">THE MAMETAS CALL</p><h3>Stay in Nice.</h3><p><strong>Why:</strong> strongest transport network and best reach for day trips.</p><p><strong>Why not Cannes:</strong> choose it instead if sand and nightlife matter more.</p><div class="riviera-fit-reality"><span>Car-free <b>Excellent</b></span><span>Budget <b>€€</b></span><span>Friction <b>Low</b></span><span>Season <b>Great</b></span></div></div></div></div></section>'''
        text = text.replace('>Start the Riviera Chooser</a>', '>Try Riviera Fit</a>')
        text = text.replace('<a class="button" href="/en/hotels/finder/?base=nice">Find my hotel with Hotel Fit</a><a class="button secondary" href="/stay/nice/">See the full Nice selection</a>',
                            '<a class="button" href="/en/hotels/">Explore Stay</a><a class="button secondary" href="/stay/nice/">See the full Nice selection</a>')
        section_id = "plan"

    pattern = re.compile(rf'<section class="v3-section chooser-signature-section" id="{section_id}">.*?</section>', re.S)
    text, count = pattern.subn(block, text, count=1)
    if count != 1:
        # Accept an already-upgraded class on repeat runs.
        pattern = re.compile(rf'<section class="v3-section chooser-signature-section chooser-signature-section--fit" id="{section_id}">.*?</section>', re.S)
        text, count = pattern.subn(block, text, count=1)
    if count != 1:
        raise RuntimeError(f"{rel}: Riviera Fit homepage block not found")
    save(rel, text, original)


def rebrand_riviera_fit(rel, lang):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace("RIVIERA FIT · LE DIAGNOSTIC MAMETAS", "RIVIERA FIT · LA RECO MAMETAS")
    else:
        text = text.replace("RIVIERA FIT · THE MAMETAS DIAGNOSIS", "RIVIERA FIT · THE MAMETAS CALL")
    save(rel, text, original)


def add_riviera_fit_home_css():
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 Riviera Fit homepage story 2026-09-25 */"
    if marker in text:
        return
    text += r'''

/* V3 Riviera Fit homepage story 2026-09-25 */
.chooser-signature-section--fit{padding:clamp(54px,6vw,78px) 0;background:var(--blue);color:var(--white)}
.riviera-fit-home{display:grid;grid-template-columns:minmax(0,.88fr) minmax(460px,1.12fr);gap:clamp(34px,5vw,72px);align-items:center}
.riviera-fit-home-copy{max-width:650px}
.riviera-fit-home-copy .eyebrow{color:#f7c966}
.riviera-fit-home-copy h2{max-width:11ch;margin:0 0 18px;font-family:var(--serif);font-size:clamp(42px,4.8vw,64px);font-weight:500;letter-spacing:-.045em;line-height:.98}
.riviera-fit-home-punch{margin:0 0 16px!important;color:#f7c966!important;font-family:var(--serif);font-size:clamp(21px,2vw,27px)!important;font-weight:600;line-height:1.2!important}
.riviera-fit-home-punch a{text-decoration:underline;text-underline-offset:4px}
.riviera-fit-home-copy>p:not(.eyebrow):not(.riviera-fit-home-punch){max-width:620px;margin:0 0 24px;color:rgba(255,255,255,.78);font-size:14px;line-height:1.68}
.riviera-fit-home-demo{overflow:hidden;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.08)}
.riviera-fit-demo-label{margin:0!important;color:#f7c966!important;font-size:9px!important;font-weight:800!important;letter-spacing:.16em;line-height:1.35!important;text-transform:uppercase}
.riviera-fit-home-demo>.riviera-fit-demo-label{padding:20px 22px 0}
.riviera-fit-demo-chips{display:flex;flex-wrap:wrap;gap:7px;padding:12px 22px 20px;border-bottom:1px solid rgba(255,255,255,.2)}
.riviera-fit-demo-chips span{padding:6px 9px;border:1px solid rgba(255,255,255,.26);background:rgba(255,255,255,.08);font-size:9px;font-weight:700;letter-spacing:.03em}
.riviera-fit-home-verdict{padding:21px 22px 22px;background:rgba(11,23,48,.34)}
.riviera-fit-home-verdict h3{margin:10px 0 14px;font-family:var(--serif);font-size:clamp(30px,3.2vw,43px);font-weight:500;line-height:1}
.riviera-fit-home-verdict>p:not(.riviera-fit-demo-label){margin:7px 0;color:rgba(255,255,255,.78);font-size:11px;line-height:1.55}
.riviera-fit-home-verdict strong{color:var(--white)}
.riviera-fit-reality{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;margin-top:18px;background:rgba(255,255,255,.2)}
.riviera-fit-reality span{padding:10px 8px;background:var(--blue-deep);color:rgba(255,255,255,.68);font-size:8px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.riviera-fit-reality b{display:block;margin-top:4px;color:var(--white);font-size:10px}
@media(max-width:940px){.riviera-fit-home{grid-template-columns:1fr}.riviera-fit-home-demo{max-width:760px}.riviera-fit-home-copy h2{max-width:14ch}}
@media(max-width:600px){.chooser-signature-section--fit{padding:46px 0}.riviera-fit-reality{grid-template-columns:repeat(2,1fr)}}
'''
    save("assets/v3.css", text, original)


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
        "index.html": ("RIVIERA FIT · THE MAMETAS CALL", "EXAMPLE · YOUR TRIP", "THE MAMETAS CALL", "Try Riviera Fit", "Explore Stay", "SHORT SELECTION · WHERE TO STAY IN NICE"),
        "fr/index.html": ("RIVIERA FIT · LA RECO MAMETAS", "EXEMPLE · VOTRE SÉJOUR", "LA RECO MAMETAS", "Tester Riviera Fit", "Explorer la rubrique Dormir", "SÉLECTION COURTE · OÙ DORMIR À NICE"),
        "riviera-chooser/index.html": ("RIVIERA FIT · LA RECO MAMETAS",),
        "en/riviera-chooser/index.html": ("RIVIERA FIT · THE MAMETAS CALL",),
        "hotels/finder/index.html": ("HOTEL FIT · LE MATCHING HÔTELIER MAMETAS", "Cinq choix. Puis seulement les hôtels qui collent."),
        "en/hotels/finder/index.html": ("HOTEL FIT · THE MAMETAS HOTEL MATCHER", "Five choices. Then only the hotels that fit."),
        "assets/v3.css": ("/* V3 Riviera Fit homepage story 2026-09-25 */", ".riviera-fit-home", ".riviera-fit-home-demo"),
    }
    errors = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
    for rel in ("index.html", "fr/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "v3-product-proof" in text or "WHAT MAMETAS DOES DIFFERENTLY" in text or "CE QUE MAMETAS FAIT DIFFÉREMMENT" in text:
            errors.append(f"{rel}: redundant product-proof block still present")
        if "Riviera Chooser" in text:
            errors.append(f"{rel}: old Riviera Chooser naming still visible")
        if "Hotel Fit" in text:
            errors.append(f"{rel}: Hotel Fit should not be promoted on the homepage")
    if errors:
        raise SystemExit("V3 product surface validation failed:\n- " + "\n- ".join(errors))

def main():
    add_home_product_proof("index.html", "en")
    add_home_product_proof("fr/index.html", "fr")
    patch_home_hotel_selection("index.html", "en")
    patch_home_hotel_selection("fr/index.html", "fr")
    patch_home_riviera_fit("index.html", "en")
    patch_home_riviera_fit("fr/index.html", "fr")
    rebrand_riviera_fit("riviera-chooser/index.html", "fr")
    rebrand_riviera_fit("en/riviera-chooser/index.html", "en")
    rebrand_hotel_fit("hotels/finder/index.html", "fr")
    rebrand_hotel_fit("en/hotels/finder/index.html", "en")
    add_css()
    add_riviera_fit_home_css()
    validate()
    print(f"V3 product surface passed; patched {len(changed)} generated file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
