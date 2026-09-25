#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []


def save(rel: str, text: str, original: str) -> None:
    if text != original:
        (ROOT / rel).write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)


def add_body_class(text: str, cls: str) -> str:
    m = re.search(r"<body([^>]*)>", text, flags=re.I)
    if not m:
        return text
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs, flags=re.I)
    if cm:
        classes = cm.group(1).split()
        if cls not in classes:
            classes.append(cls)
        attrs = attrs[:cm.start()] + 'class="' + " ".join(classes) + '"' + attrs[cm.end():]
    else:
        attrs += f' class="{cls}"'
    return text[:m.start()] + "<body" + attrs + ">" + text[m.end():]


def journey_spine(lang: str) -> str:
    if lang == "fr":
        return '''<nav class="home-journey-spine" aria-label="Comment Mametas vous aide à préparer la Côte d’Azur"><div class="wrap home-journey-inner"><span class="home-journey-label">VOTRE SÉJOUR, SIMPLIFIÉ</span><a href="/riviera-fit/"><b>01</b><strong>Choisir la base</strong><small>Riviera Fit ou les destinations</small></a><a href="/hotels/finder/"><b>02</b><strong>Choisir l’hôtel</strong><small>Hotel Fit</small></a><a href="/explore/"><b>03</b><strong>Remplir les journées</strong><small>Plages, culture, balades, tables</small></a><a href="/pratique/"><b>04</b><strong>Faire fonctionner le séjour</strong><small>Transport, météo, réservations</small></a></div></nav>'''
    return '''<nav class="home-journey-spine" aria-label="How Mametas helps plan a French Riviera trip"><div class="wrap home-journey-inner"><span class="home-journey-label">YOUR TRIP, SIMPLIFIED</span><a href="/en/riviera-fit/"><b>01</b><strong>Choose the base</strong><small>Riviera Fit or browse Places</small></a><a href="/en/hotels/finder/"><b>02</b><strong>Choose the hotel</strong><small>Hotel Fit</small></a><a href="/en/explore/"><b>03</b><strong>Fill the days</strong><small>Beaches, culture, walks, tables</small></a><a href="/en/practical/"><b>04</b><strong>Make it work</strong><small>Transport, weather, bookings</small></a></div></nav>'''


def stay_intro(lang: str) -> str:
    if lang == "fr":
        return '''<div class="stay-intro adoption-stay-intro"><p class="fit-tool-label fit-tool-label--hotel">MAMETAS · HOTEL FIT</p><p class="eyebrow">ÉTAPE 02 · CHOISIR L’HÔTEL</p><h2>Un bel hôtel peut rester le mauvais hôtel.</h2><p>Une fois la base choisie, Hotel Fit réduit la liste à quelques adresses adaptées à votre façon de voyager, avec la raison et le compromis.</p><div class="hotel-selection-actions"><a class="button hotel-fit-home-cta" href="/hotels/finder/">Tester Hotel Fit</a><a class="button secondary" href="/hotels/">Explorer Dormir</a></div></div>'''
    return '''<div class="stay-intro adoption-stay-intro"><p class="fit-tool-label fit-tool-label--hotel">MAMETAS · HOTEL FIT</p><p class="eyebrow">STEP 02 · CHOOSE THE HOTEL</p><h2>A beautiful hotel can still be the wrong hotel.</h2><p>Once the base is settled, Hotel Fit cuts the list to a few addresses that match how you travel, with the reason and the catch.</p><div class="hotel-selection-actions"><a class="button hotel-fit-home-cta" href="/en/hotels/finder/">Try Hotel Fit</a><a class="button secondary" href="/en/hotels/">Browse Stay</a></div></div>'''


def patch_home(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "adoption-home")

    if "home-journey-spine" not in text:
        anchor = re.search(r'<section[^>]*class="[^"]*chooser-signature-section--fit[^"]*"[^>]*>', text, flags=re.S)
        if not anchor:
            raise RuntimeError(f"{rel}: Riviera Fit homepage section not found")
        text = text[:anchor.start()] + journey_spine(lang) + text[anchor.start():]

    if lang == "fr":
        text = text.replace("MAMETAS RIVIERA FIT · LA RECO", "MAMETAS · RIVIERA FIT")
        text = text.replace("EXEMPLE · VOTRE SÉJOUR", "EXEMPLE · CE QUE VOUS OBTENEZ")
        text = text.replace("LA RECO MAMETAS", "RÉSULTAT D’EXEMPLE")
        text = text.replace('href="/riviera-chooser/"', 'href="/riviera-fit/"')
    else:
        text = text.replace("MAMETAS RIVIERA FIT · THE CALL", "MAMETAS · RIVIERA FIT")
        text = text.replace("EXAMPLE · YOUR TRIP", "EXAMPLE · WHAT YOU GET")
        text = text.replace("THE MAMETAS CALL", "SAMPLE RESULT")
        text = text.replace('href="/en/riviera-chooser/"', 'href="/en/riviera-fit/"')

    pattern = re.compile(
        r'(<section class="v3-section" id="(?:stay|hotels)"><div class="wrap stay-layout">)'
        r'<div class="stay-intro">.*?(?=<div class="stay-list">)',
        flags=re.S,
    )
    text, count = pattern.subn(lambda m: m.group(1) + stay_intro(lang), text, count=1)
    if count != 1:
        # Accept repeat runs after the adoption class has already been added.
        pattern = re.compile(
            r'(<section class="v3-section" id="(?:stay|hotels)"><div class="wrap stay-layout">)'
            r'<div class="stay-intro adoption-stay-intro">.*?(?=<div class="stay-list">)',
            flags=re.S,
        )
        text, count = pattern.subn(lambda m: m.group(1) + stay_intro(lang), text, count=1)
    if count != 1:
        raise RuntimeError(f"{rel}: homepage Stay intro not found")

    save(rel, text, original)


def patch_css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 adoption layer 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 adoption layer 2026-09-25 */

/* The homepage explains the journey before exposing the depth of the site. */
.home-journey-spine{border-bottom:1px solid var(--line);background:rgba(255,253,248,.72)}
.home-journey-inner{display:grid;grid-template-columns:minmax(130px,.62fr) repeat(4,minmax(0,1fr));align-items:stretch}
.home-journey-label{display:flex;align-items:center;padding:16px 18px 16px 0;color:var(--ink-soft);font-size:8px;font-weight:800;letter-spacing:.14em;line-height:1.4;text-transform:uppercase}
.home-journey-inner>a{display:grid;grid-template-columns:auto 1fr;column-gap:10px;align-content:center;min-height:82px;padding:13px 16px;border-left:1px solid var(--line);text-decoration:none;transition:background .16s ease}
.home-journey-inner>a:hover,.home-journey-inner>a:focus-visible{background:var(--white)}
.home-journey-inner>a b{grid-row:1/3;color:var(--coral);font-family:var(--serif);font-size:14px;font-style:italic;font-weight:500}
.home-journey-inner>a strong{font-family:var(--serif);font-size:17px;font-weight:500;line-height:1.08}
.home-journey-inner>a small{margin-top:4px;color:var(--ink-soft);font-size:8.5px;line-height:1.35}

/* Riviera Fit remains important, but behaves like a product, not a second hero. */
.adoption-home .chooser-signature-section--fit{padding:clamp(48px,5vw,66px) 0;background:var(--paper);color:var(--ink)}
.adoption-home .riviera-fit-home{grid-template-columns:minmax(0,.82fr) minmax(420px,1.18fr);gap:clamp(30px,4.5vw,62px)}
.adoption-home .riviera-fit-home-copy .eyebrow{color:var(--blue-deep)}
.adoption-home .riviera-fit-home-copy h2{font-size:clamp(38px,4.1vw,56px)}
.adoption-home .riviera-fit-home-punch{color:var(--blue-deep)!important;font-size:clamp(19px,1.8vw,24px)!important}
.adoption-home .riviera-fit-home-copy>p:not(.eyebrow):not(.riviera-fit-home-punch){color:var(--ink-soft)}
.adoption-home .chooser-signature-primary{background:var(--blue);color:#fff}
.adoption-home .riviera-fit-home-demo{border:1px solid var(--line);background:var(--white);box-shadow:0 12px 30px rgba(20,33,61,.04)}
.adoption-home .riviera-fit-demo-label{display:inline-flex;color:var(--coral)!important}
.adoption-home .riviera-fit-home-demo>.riviera-fit-demo-label{margin:18px 20px 0!important;padding:6px 8px!important;border:1px solid rgba(199,91,61,.28);background:rgba(199,91,61,.05)}
.adoption-home .riviera-fit-demo-chips{padding:13px 20px 18px;border-bottom:1px solid var(--line)}
.adoption-home .riviera-fit-demo-chips span{border:1px solid var(--line);background:var(--paper);color:var(--ink);font-size:8.5px}
.adoption-home .riviera-fit-home-verdict{padding:18px 20px 20px;background:rgba(23,54,95,.035)}
.adoption-home .riviera-fit-home-verdict .riviera-fit-demo-label{padding:0;background:transparent}
.adoption-home .riviera-fit-home-verdict h3{color:var(--ink);font-size:clamp(29px,3vw,40px)}
.adoption-home .riviera-fit-home-verdict>p:not(.riviera-fit-demo-label){color:var(--ink-soft)}
.adoption-home .riviera-fit-home-verdict strong{color:var(--ink)}
.adoption-home .riviera-fit-reality{background:var(--line)}
.adoption-home .riviera-fit-reality span{background:var(--paper);color:var(--ink-soft)}
.adoption-home .riviera-fit-reality b{color:var(--ink)}

/* Hotel Fit is visible at the moment the hotel decision becomes relevant. */
.adoption-stay-intro .fit-tool-label--hotel{margin:0 0 10px;border-color:rgba(199,91,61,.42);background:rgba(199,91,61,.055);color:var(--coral)!important}
.adoption-stay-intro .eyebrow{margin-bottom:10px}
.adoption-stay-intro .hotel-selection-actions{margin-top:22px}
.adoption-stay-intro .hotel-fit-home-cta{background:var(--coral);border-color:var(--coral);color:#fff}

@media(max-width:1050px){
  .home-journey-inner{grid-template-columns:repeat(2,minmax(0,1fr))}
  .home-journey-label{grid-column:1/-1;padding:13px 0;border-bottom:1px solid var(--line)}
  .home-journey-inner>a:nth-of-type(odd){border-left:0}
  .home-journey-inner>a{border-bottom:1px solid var(--line)}
}
@media(max-width:760px){
  .home-journey-inner{grid-template-columns:1fr}
  .home-journey-label{padding-left:0}
  .home-journey-inner>a{min-height:68px;padding:11px 4px;border-left:0}
  .home-journey-inner>a strong{font-size:16px}
  .adoption-home .riviera-fit-home{grid-template-columns:1fr}
  .adoption-home .riviera-fit-home-demo{max-width:none}
}
'''
    save("assets/v3.css", text, original)


def validate() -> None:
    checks = {
        "index.html": (
            "home-journey-spine",
            "MAMETAS · RIVIERA FIT",
            "EXAMPLE · WHAT YOU GET",
            "SAMPLE RESULT",
            "MAMETAS · HOTEL FIT",
            "Try Hotel Fit",
        ),
        "fr/index.html": (
            "home-journey-spine",
            "MAMETAS · RIVIERA FIT",
            "EXEMPLE · CE QUE VOUS OBTENEZ",
            "RÉSULTAT D’EXEMPLE",
            "MAMETAS · HOTEL FIT",
            "Tester Hotel Fit",
        ),
    }
    errors: list[str] = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
        if "Riviera Chooser" in text:
            errors.append(f"{rel}: stale Riviera Chooser naming remains")
    css = (ROOT / "assets/v3.css").read_text(encoding="utf-8")
    if "V3 adoption layer 2026-09-25" not in css:
        errors.append("assets/v3.css: adoption layer CSS missing")
    if errors:
        raise SystemExit("V3 adoption layer failed:\n- " + "\n- ".join(errors))


def main() -> int:
    patch_home("index.html", "en")
    patch_home("fr/index.html", "fr")
    patch_css()
    validate()
    print(f"V3 adoption layer passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
