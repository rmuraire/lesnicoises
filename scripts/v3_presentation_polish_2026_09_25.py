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
<div class="fit-preview-head"><div><p class="fit-tool-label">MAMETAS · RIVIERA FIT</p><h3 id="plan-riviera-fit-title">Cinq questions. Une base.</h3><p>Répondez aux choix qui changent vraiment la géographie du séjour. Riviera Fit tranche ensuite, compromis compris.</p></div><a class="fit-primary-action" href="/riviera-fit/">Lancer Riviera Fit →</a></div>
<div class="fit-preview-questions">
<div class="fit-preview-row"><span>01</span><strong>Combien de temps ?</strong><small>3 jours · 5 jours · 7+</small></div>
<div class="fit-preview-row"><span>02</span><strong>Quand partez-vous ?</strong><small>Printemps · Été · Automne · Hiver</small></div>
<div class="fit-preview-row"><span>03</span><strong>Comment vous déplacez-vous ?</strong><small>Sans voiture · Voiture · Peu importe</small></div>
<div class="fit-preview-row"><span>04</span><strong>Qu’est-ce qui compte le plus ?</strong><small>Glamour · Art · Mer · Calme · Décidez pour moi</small></div>
<div class="fit-preview-row"><span>05</span><strong>Quel rythme ?</strong><small>Lent · Équilibré · Ambitieux</small></div>
</div></section>"""
    return """<section class="plan-riviera-fit-panel" aria-labelledby="plan-riviera-fit-title">
<div class="fit-preview-head"><div><p class="fit-tool-label">MAMETAS · RIVIERA FIT</p><h3 id="plan-riviera-fit-title">Five questions. One base.</h3><p>Answer the choices that genuinely change the geography of the trip. Riviera Fit makes the call, trade-offs included.</p></div><a class="fit-primary-action" href="/en/riviera-fit/">Start Riviera Fit →</a></div>
<div class="fit-preview-questions">
<div class="fit-preview-row"><span>01</span><strong>How long do you have?</strong><small>3 days · 5 days · 7+</small></div>
<div class="fit-preview-row"><span>02</span><strong>When are you going?</strong><small>Spring · Summer · Autumn · Winter</small></div>
<div class="fit-preview-row"><span>03</span><strong>How will you move?</strong><small>No car · Car · Either</small></div>
<div class="fit-preview-row"><span>04</span><strong>What matters most?</strong><small>Glamour · Art · Sea · Peace · Decide for me</small></div>
<div class="fit-preview-row"><span>05</span><strong>What pace?</strong><small>Slow · Balanced · Ambitious</small></div>
</div></section>"""


def patch_plan(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = add_body_class(text, "hub-density-polished plan-product-polished")
    pattern = r'<a class="[^"]*architecture-card--tool[^"]*" href="[^"]*riviera-fit/".*?</a>'
    text, n = re.subn(pattern, fit_preview(lang), text, count=1, flags=re.S)
    if n != 1 and "plan-riviera-fit-panel" not in text:
        raise RuntimeError(f"{rel}: Riviera Fit Plan card not found")
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
        "plan/index.html": ("plan-riviera-fit-panel", "Five questions. One base.", "fit-primary-action"),
        "fr/planifier/index.html": ("plan-riviera-fit-panel", "Cinq questions. Une base.", "fit-primary-action"),
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
    if errors:
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
    patch_site_css()
    validate()
    print(f"V3 presentation polish passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
