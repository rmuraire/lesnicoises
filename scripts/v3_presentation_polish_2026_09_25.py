#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []


def save(rel: str, text: str, original: str) -> None:
    if text != original:
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)


def add_body_class(text: str, cls: str) -> str:
    m = re.search(r"<body([^>]*)>", text, flags=re.I)
    if not m:
        return text
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs, flags=re.I)
    wanted = cls.split()
    if cm:
        classes = cm.group(1).split()
        for item in wanted:
            if item not in classes:
                classes.append(item)
        attrs2 = attrs[:cm.start()] + 'class="' + " ".join(classes) + '"' + attrs[cm.end():]
    else:
        attrs2 = attrs + ' class="' + " ".join(wanted) + '"'
    return text[:m.start()] + "<body" + attrs2 + ">" + text[m.end():]


def fit_preview(lang: str) -> str:
    if lang == "fr":
        return """<section class="plan-riviera-fit-panel" aria-labelledby="plan-riviera-fit-title">
<div class="fit-preview-head"><div><p class="fit-tool-label">MAMETAS · RIVIERA FIT</p><h3 id="plan-riviera-fit-title">Cinq questions. Une base.</h3><p>Pas une liste de villes. Répondez ici : Riviera Fit choisit la base, explique pourquoi et vous montre les compromis.</p></div></div>
<div class="plan-fit-engine" data-riviera-chooser><div class="chooser-engine">
<section class="chooser-step" data-step="1"><div class="chooser-step-head"><span class="chooser-step-number">01</span><div><h2>Combien de jours avez-vous vraiment ?</h2><p>Sept jours, ce n’est pas trois jours avec quatre étapes de plus.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="days" data-choice="3">3 jours</button><button type="button" aria-pressed="false" data-group="days" data-choice="5">5 jours</button><button type="button" aria-pressed="false" data-group="days" data-choice="7">7 jours ou plus</button></div></section>
<section class="chooser-step" data-step="2"><div class="chooser-step-head"><span class="chooser-step-number">02</span><div><h2>Quand venez-vous ?</h2><p>La Riviera ne joue pas la même partie en février et en août.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="season" data-choice="winter">Novembre à mars</button><button type="button" aria-pressed="false" data-group="season" data-choice="spring">Avril à juin</button><button type="button" aria-pressed="false" data-group="season" data-choice="summer">Juillet et août</button><button type="button" aria-pressed="false" data-group="season" data-choice="autumn">Septembre et octobre</button></div></section>
<section class="chooser-step" data-step="3"><div class="chooser-step-head"><span class="chooser-step-number">03</span><div><h2>Comment allez-vous vous déplacer ?</h2><p>Parfois le train gagne. Parfois absolument pas.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="mobility" data-choice="nocar">Sans voiture</button><button type="button" aria-pressed="false" data-group="mobility" data-choice="car">Avec voiture</button><button type="button" aria-pressed="false" data-group="mobility" data-choice="either">Les deux me vont</button></div></section>
<section class="chooser-step" data-step="4"><div class="chooser-step-head"><span class="chooser-step-number">04</span><div><h2>Qu’attendez-vous le plus de la Riviera ?</h2><p>Choisissez ce qui vous manquerait vraiment si le séjour ne vous le donnait pas.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="mood" data-choice="decide">Décidez pour moi</button><button type="button" aria-pressed="false" data-group="mood" data-choice="sea">Mer &amp; baignade</button><button type="button" aria-pressed="false" data-group="mood" data-choice="food">Restaurants &amp; ville</button><button type="button" aria-pressed="false" data-group="mood" data-choice="culture">Art &amp; villages</button><button type="button" aria-pressed="false" data-group="mood" data-choice="glamour">Glamour Riviera</button><button type="button" aria-pressed="false" data-group="mood" data-choice="peace">Calme &amp; beauté</button></div></section>
<section class="chooser-step" data-step="5"><div class="chooser-step-head"><span class="chooser-step-number">05</span><div><h2>Quel rythme ressemble encore à des vacances ?</h2><p>Le rythme décide jusqu’où on vous envoie.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="pace" data-choice="slow">Tranquille</button><button type="button" aria-pressed="false" data-group="pace" data-choice="balanced">Équilibré</button><button type="button" aria-pressed="false" data-group="pace" data-choice="ambitious">Ambitieux</button></div></section>
<div class="chooser-submit-row"><button class="button plan-fit-submit" type="button" data-chooser-submit disabled>Donnez-moi le verdict</button><a class="plan-fit-full-link" href="/riviera-fit/">Voir Riviera Fit en plein écran →</a></div>
</div><section class="chooser-result" data-chooser-result hidden aria-live="polite"></section></div></section>"""
    return """<section class="plan-riviera-fit-panel" aria-labelledby="plan-riviera-fit-title">
<div class="fit-preview-head"><div><p class="fit-tool-label">MAMETAS · RIVIERA FIT</p><h3 id="plan-riviera-fit-title">Five questions. One base.</h3><p>Not a list of towns. Answer here: Riviera Fit picks the base, explains why and shows the trade-offs.</p></div></div>
<div class="plan-fit-engine" data-riviera-chooser><div class="chooser-engine">
<section class="chooser-step" data-step="1"><div class="chooser-step-head"><span class="chooser-step-number">01</span><div><h2>How long do you actually have?</h2><p>Seven days is not three days with four extra stops.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="days" data-choice="3">3 days</button><button type="button" aria-pressed="false" data-group="days" data-choice="5">5 days</button><button type="button" aria-pressed="false" data-group="days" data-choice="7">7 days or more</button></div></section>
<section class="chooser-step" data-step="2"><div class="chooser-step-head"><span class="chooser-step-number">02</span><div><h2>When are you coming?</h2><p>The Riviera is not playing the same game in February and August.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="season" data-choice="winter">November to March</button><button type="button" aria-pressed="false" data-group="season" data-choice="spring">April to June</button><button type="button" aria-pressed="false" data-group="season" data-choice="summer">July and August</button><button type="button" aria-pressed="false" data-group="season" data-choice="autumn">September and October</button></div></section>
<section class="chooser-step" data-step="3"><div class="chooser-step-head"><span class="chooser-step-number">03</span><div><h2>How are you moving around?</h2><p>Sometimes the train wins. Sometimes it absolutely does not.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="mobility" data-choice="nocar">No car</button><button type="button" aria-pressed="false" data-group="mobility" data-choice="car">I’ll have a car</button><button type="button" aria-pressed="false" data-group="mobility" data-choice="either">Either is fine</button></div></section>
<section class="chooser-step" data-step="4"><div class="chooser-step-head"><span class="chooser-step-number">04</span><div><h2>What do you want most from the Riviera?</h2><p>Pick the thing you would actually notice if the trip failed to deliver it.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="mood" data-choice="decide">Decide for me</button><button type="button" aria-pressed="false" data-group="mood" data-choice="sea">Sea &amp; swimming</button><button type="button" aria-pressed="false" data-group="mood" data-choice="food">Food &amp; city life</button><button type="button" aria-pressed="false" data-group="mood" data-choice="culture">Art &amp; villages</button><button type="button" aria-pressed="false" data-group="mood" data-choice="glamour">Riviera glamour</button><button type="button" aria-pressed="false" data-group="mood" data-choice="peace">Peace &amp; beauty</button></div></section>
<section class="chooser-step" data-step="5"><div class="chooser-step-head"><span class="chooser-step-number">05</span><div><h2>What pace still feels like a holiday?</h2><p>Pace decides how far we send you.</p></div></div><div class="chooser-options"><button type="button" aria-pressed="false" data-group="pace" data-choice="slow">Slow</button><button type="button" aria-pressed="false" data-group="pace" data-choice="balanced">Balanced</button><button type="button" aria-pressed="false" data-group="pace" data-choice="ambitious">Ambitious</button></div></section>
<div class="chooser-submit-row"><button class="button plan-fit-submit" type="button" data-chooser-submit disabled>Give me the verdict</button><a class="plan-fit-full-link" href="/en/riviera-fit/">Open Riviera Fit full screen →</a></div>
</div><section class="chooser-result" data-chooser-result hidden aria-live="polite"></section></div></section>"""


def patch_plan(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "hub-density-polished plan-product-polished")
    pattern = r'<a class="[^"]*architecture-card--tool[^"]*" href="[^"]*riviera-fit/".*?</a>'
    text, n = re.subn(pattern, fit_preview(lang), text, count=1, flags=re.S)
    if n != 1 and "plan-riviera-fit-panel" not in text:
        raise RuntimeError(f"{rel}: Riviera Fit Plan card not found")
    if "/assets/riviera-chooser.css?v=5" not in text:
        text = re.sub(
            r'(<link rel="stylesheet" href="/assets/v3\.css\?v=[^"]+">)',
            '<link rel="stylesheet" href="/assets/riviera-chooser.css?v=5">\\1',
            text,
            count=1,
        )
    if "/assets/riviera-chooser.js?v=9" not in text:
        text = text.replace("</body>", '<script src="/assets/riviera-chooser.js?v=9"></script></body>', 1)
    save(rel, text, original)


def patch_riviera_fit(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "riviera-fit-polished hub-density-polished")
    text = re.sub(r'<p class="tool-badge">MAMETAS TOOL</p>', "", text, count=1)
    label = "MAMETAS · RIVIERA FIT"
    text = re.sub(
        r'<p class="eyebrow">(?:MAMETAS )?RIVIERA FIT[^<]*</p>',
        f'<p class="fit-tool-label">{label}</p>',
        text,
        count=1,
    )
    if "riviera-fit-start" not in text:
        cta = "Commencer Riviera Fit →" if lang == "fr" else "Start Riviera Fit →"
        text = re.sub(
            r'(<p class="article-deck">.*?</p>)',
            lambda m: m.group(1) + f'<a class="riviera-fit-start" href="#riviera-fit-questions">{cta}</a>',
            text,
            count=1,
            flags=re.S,
        )
    text = text.replace(
        '<div class="wrap chooser-shell" data-riviera-chooser>',
        '<div class="wrap chooser-shell" id="riviera-fit-questions" data-riviera-chooser>',
        1,
    )
    save(rel, text, original)


def patch_explore(rel: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "hub-density-polished explore-product-polished")
    save(rel, text, original)


def patch_hub_density(rel: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "hub-density-polished")
    save(rel, text, original)


def patch_booking(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "legacy-harmonised booking-polished")
    if "booking-visuals" not in text:
        alt1 = "Private beach on the French Riviera" if lang == "en" else "Plage privée sur la Côte d’Azur"
        alt2 = "Lérins Islands off Cannes" if lang == "en" else "Îles de Lérins au large de Cannes"
        pair = f'''<div class="booking-visuals"><figure><img src="/assets/editorial/cannes-beach-sophie-kat.jpg" alt="{alt1}" loading="lazy"></figure><figure><img src="/assets/editorial/iles-de-lerins-bruno-attuyt.webp" alt="{alt2}" loading="lazy"></figure></div>'''
        text, n = re.subn(
            r'(<div class="verdict">.*?</div>)',
            lambda m: m.group(1) + pair,
            text,
            count=1,
            flags=re.S,
        )
        if n != 1:
            raise RuntimeError(f"{rel}: booking verdict anchor not found")
    save(rel, text, original)


def patch_gay_nice(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace(
            '<p><a href="/fr/dormir/nice/">Voir le sélecteur complet d’hôtels Mametas →</a></p>',
            '<p><a href="/hotels/finder/">Trouvez le bon hôtel à Nice avec Hotel Fit →</a></p>',
        )
        text = text.replace("sélecteur complet d’hôtels Mametas", "Hotel Fit Mametas")
    else:
        text = text.replace(
            '<p><a href="/stay/nice/">See the full Mametas Nice hotel chooser →</a></p>',
            '<p><a href="/en/hotels/finder/">Find the right Nice hotel with Hotel Fit →</a></p>',
        )
        text = text.replace("Mametas Nice hotel chooser", "Mametas Hotel Fit")
    save(rel, text, original)


def patch_v3_css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 presentation polish 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 presentation polish 2026-09-25 */
.hub-density-polished .article-hero{padding-top:clamp(58px,6.5vw,88px);padding-bottom:44px}
.hub-density-polished .v3-section{padding-top:clamp(44px,4.7vw,64px);padding-bottom:clamp(44px,4.7vw,64px)}
.hub-density-polished .section-heading{margin-bottom:28px}
.hub-density-polished .architecture-next{padding-top:42px;padding-bottom:46px}
.plan-product-polished .architecture-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.plan-product-polished .plan-riviera-fit-panel{grid-column:1/-1;border:1px solid rgba(23,54,95,.22);background:rgba(23,54,95,.035)}
.fit-preview-head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:28px;align-items:end;padding:27px 28px 22px}
.fit-tool-label{margin:0 0 9px;color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.15em;text-transform:uppercase}
.fit-preview-head h3{margin:0 0 8px;font-family:var(--serif);font-size:clamp(34px,4vw,48px);font-weight:500;line-height:1}
.fit-preview-head p:not(.fit-tool-label){max-width:690px;margin:0;color:var(--ink-soft);font-size:12px;line-height:1.6}
.fit-primary-action,.riviera-fit-start{display:inline-flex;min-height:44px;padding:12px 17px;align-items:center;justify-content:center;background:var(--blue);color:var(--white);font-size:10px;font-weight:800;letter-spacing:.09em;text-decoration:none;text-transform:uppercase;transition:transform .16s ease,opacity .16s ease}
.fit-primary-action:hover,.fit-primary-action:focus-visible,.riviera-fit-start:hover,.riviera-fit-start:focus-visible{transform:translateY(-1px);opacity:.9}
.fit-preview-questions{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-top:1px solid var(--line)}
.fit-preview-row{min-height:112px;padding:18px;border-right:1px solid var(--line)}
.fit-preview-row:last-child{border-right:0}
.fit-preview-row>span{display:block;margin-bottom:14px;color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.12em}
.fit-preview-row strong{display:block;margin-bottom:7px;font-family:var(--serif);font-size:18px;font-weight:500;line-height:1.1}
.fit-preview-row small{display:block;color:var(--ink-soft);font-size:9px;line-height:1.5}
.riviera-fit-polished .chooser-hero h1{max-width:900px;font-size:clamp(48px,6vw,76px)}
.riviera-fit-polished .chooser-page-intro{margin-bottom:0}
.riviera-fit-polished .riviera-fit-start{margin-top:22px}
.riviera-fit-polished .article-meta{margin-top:22px}
.riviera-fit-polished .chooser-rule{margin-bottom:18px}
.riviera-fit-polished .chooser-engine{box-shadow:none}
.riviera-fit-polished .chooser-step{padding-top:15px;padding-bottom:15px}
.explore-product-polished .base-grid{gap:10px}
.explore-product-polished .base-card{min-height:255px}
.explore-product-polished .base-card-content{padding:20px}
.explore-product-polished .base-card-content h3{font-size:clamp(27px,3vw,38px)}
.explore-product-polished .base-card-content p{max-width:520px;font-size:11px;line-height:1.5}
.explore-product-polished .lgbtq-banner--fifth{min-height:132px;padding:24px}
.explore-product-polished .lgbtq-banner--fifth .lgbtq-banner-title{font-size:clamp(30px,3.2vw,42px)}
@media(max-width:980px){
  .fit-preview-questions{grid-template-columns:repeat(2,minmax(0,1fr))}
  .fit-preview-row{border-bottom:1px solid var(--line)}
  .fit-preview-row:nth-child(2n){border-right:0}
  .fit-preview-row:last-child{grid-column:1/-1}
}
@media(max-width:760px){
  .fit-preview-head{grid-template-columns:1fr;padding:23px 20px 18px}
  .fit-primary-action{width:100%}
  .plan-product-polished .architecture-grid{grid-template-columns:1fr}
  .fit-preview-questions{grid-template-columns:1fr}
  .fit-preview-row,.fit-preview-row:nth-child(2n){min-height:0;border-right:0;border-bottom:1px solid var(--line)}
  .fit-preview-row:last-child{grid-column:auto;border-bottom:0}
  .explore-product-polished .base-card{min-height:220px}
}
'''
    save("assets/v3.css", text, original)


def patch_riviera_css() -> None:
    p = ROOT / "assets/riviera-chooser.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* Plan embedded Riviera Fit 2026-09-25 */"
    if marker not in text:
        text += r'''

/* Plan embedded Riviera Fit 2026-09-25 */
.plan-product-polished .plan-riviera-fit-panel .chooser-engine{border:0;border-top:1px solid var(--line);background:transparent}
.plan-product-polished .plan-riviera-fit-panel .chooser-step{grid-template-columns:minmax(220px,.72fr) minmax(0,1.28fr);gap:20px;padding:14px 20px;background:rgba(255,253,248,.28)}
.plan-product-polished .plan-riviera-fit-panel .chooser-step h2{font-size:clamp(18px,1.8vw,23px)}
.plan-product-polished .plan-riviera-fit-panel .chooser-step p{font-size:9.5px}
.plan-product-polished .plan-riviera-fit-panel .chooser-options button{min-height:34px;padding:7px 10px;font-size:9px}
.plan-product-polished .plan-riviera-fit-panel .chooser-submit-row{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:18px 20px;border-top:1px solid var(--line)}
.plan-product-polished .plan-riviera-fit-panel .plan-fit-submit{background:var(--blue);color:#fff}
.plan-fit-full-link{font-size:9px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;text-decoration:none}
.plan-product-polished .plan-riviera-fit-panel .chooser-result{margin:0 20px 22px}
@media(max-width:780px){
  .plan-product-polished .plan-riviera-fit-panel .chooser-step{grid-template-columns:1fr;gap:10px;padding:14px 16px}
  .plan-product-polished .plan-riviera-fit-panel .chooser-submit-row{align-items:stretch;flex-direction:column}
  .plan-product-polished .plan-riviera-fit-panel .plan-fit-submit{width:100%}
}
'''
    save("assets/riviera-chooser.css", text, original)


def patch_site_css() -> None:
    p = ROOT / "assets/site.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 booking visual polish 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 booking visual polish 2026-09-25 */
.booking-polished .article{padding-top:48px;padding-bottom:60px}
.booking-polished .article h2{margin-top:38px}
.booking-visuals{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:30px 0 38px}
.booking-visuals figure{margin:0;overflow:hidden;background:var(--cream-deep)}
.booking-visuals img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
@media(max-width:700px){.booking-visuals{grid-template-columns:1fr}}
'''
    save("assets/site.css", text, original)


def validate() -> None:
    checks = {
        "plan/index.html": ("plan-riviera-fit-panel", "Five questions. One base.", 'data-riviera-chooser', 'data-group="days"', 'data-chooser-submit', "/assets/riviera-chooser.js?v=9"),
        "fr/planifier/index.html": ("plan-riviera-fit-panel", "Cinq questions. Une base.", 'data-riviera-chooser', 'data-group="days"', 'data-chooser-submit', "/assets/riviera-chooser.js?v=9"),
        "en/riviera-fit/index.html": ("riviera-fit-polished", "fit-tool-label", "riviera-fit-start", 'id="riviera-fit-questions"'),
        "riviera-fit/index.html": ("riviera-fit-polished", "fit-tool-label", "riviera-fit-start", 'id="riviera-fit-questions"'),
        "en/explore/index.html": ("explore-product-polished",),
        "explore/index.html": ("explore-product-polished",),
        "en/good-finds/what-to-book/index.html": ("booking-visuals", "cannes-beach-sophie-kat.jpg"),
        "bons-plans/que-reserver/index.html": ("booking-visuals", "iles-de-lerins-bruno-attuyt.webp"),
        "en/gay-nice/index.html": ("Find the right Nice hotel with Hotel Fit",),
        "guide-gay-nice/index.html": ("Trouvez le bon hôtel à Nice avec Hotel Fit",),
    }
    errors: list[str] = []
    for rel, needles in checks.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: missing")
            continue
        body = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in body:
                errors.append(f"{rel}: missing {needle!r}")
    if "V3 presentation polish 2026-09-25" not in (ROOT / "assets/v3.css").read_text(encoding="utf-8"):
        errors.append("assets/v3.css: presentation polish missing")
    if "V3 booking visual polish 2026-09-25" not in (ROOT / "assets/site.css").read_text(encoding="utf-8"):
        errors.append("assets/site.css: booking polish missing")
    if "Plan embedded Riviera Fit 2026-09-25" not in (ROOT / "assets/riviera-chooser.css").read_text(encoding="utf-8"):\n        errors.append("assets/riviera-chooser.css: embedded Plan tool polish missing")\n    if errors:
        raise SystemExit("V3 presentation polish failed:\n- " + "\n- ".join(errors))


def main() -> int:
    patch_plan("plan/index.html", "en")
    patch_plan("fr/planifier/index.html", "fr")
    patch_riviera_fit("en/riviera-fit/index.html", "en")
    patch_riviera_fit("riviera-fit/index.html", "fr")
    patch_explore("en/explore/index.html")
    patch_explore("explore/index.html")
    for rel in ("en/riviera-guide/index.html", "riviera-guide/index.html", "en/hotels/index.html", "hotels/index.html", "en/practical/index.html", "pratique/index.html"):
        patch_hub_density(rel)
    patch_booking("en/good-finds/what-to-book/index.html", "en")
    patch_booking("bons-plans/que-reserver/index.html", "fr")
    patch_gay_nice("en/gay-nice/index.html", "en")
    patch_gay_nice("guide-gay-nice/index.html", "fr")
    patch_v3_css()
    patch_riviera_css()
    patch_site_css()
    validate()
    print(f"V3 presentation polish passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
