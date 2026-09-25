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
    m = re.search(r"<body(?P<attrs>[^>]*)>", text, flags=re.I)
    if not m:
        return text
    attrs = m.group("attrs")
    cm = re.search(r'class="([^"]*)"', attrs)
    if cm:
        classes = cm.group(1).split()
        if cls not in classes:
            classes.append(cls)
        new_attrs = attrs[:cm.start()] + f'class="{" ".join(classes)}"' + attrs[cm.end():]
    else:
        new_attrs = attrs + f' class="{cls}"'
    return text[:m.start()] + "<body" + new_attrs + ">" + text[m.end():]


def ensure_css(rel: str, marker: str, css: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if marker not in text:
        text += "\n\n" + marker + "\n" + css.strip() + "\n"
    save(rel, text, original)


def patch_fit_linkage() -> None:
    home = {
        "index.html": (
            ("IF YOU HAD THE FOLLOWING CRITERIA…", r"IF YOU HAD THE FOLLOWING CRITERIA(?:…)?"),
            ("↓ MAMETAS RIVIERA FIT WOULD SUGGEST", r"(?:↓\s*)?MAMETAS RIVIERA FIT WOULD SUGGEST"),
        ),
        "fr/index.html": (
            ("SI VOUS AVIEZ LES CRITÈRES SUIVANTS…", r"SI VOUS AVIEZ LES CRITÈRES SUIVANTS(?:…)?"),
            ("↓ MAMETAS RIVIERA FIT VOUS PROPOSERAIT", r"(?:↓\s*)?MAMETAS RIVIERA FIT VOUS PROPOSERAIT"),
        ),
    }
    for rel, pairs in home.items():
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        for replacement, pattern in pairs:
            text = re.sub(pattern, replacement, text)
        save(rel, text, original)

    hotel = {
        "en/hotels/index.html": (
            ("IF YOUR PRIORITIES WERE AS FOLLOWS…", r"IF YOUR PRIORITIES WERE AS FOLLOWS(?:…)?"),
            ("↓ MAMETAS HOTEL FIT WOULD SUGGEST", r"(?:↓\s*)?MAMETAS HOTEL FIT WOULD SUGGEST"),
        ),
        "hotels/index.html": (
            ("SI VOS PRIORITÉS ÉTAIENT LES SUIVANTES…", r"SI VOS PRIORITÉS ÉTAIENT LES SUIVANTES(?:…)?"),
            ("↓ MAMETAS HOTEL FIT VOUS PROPOSERAIT", r"(?:↓\s*)?MAMETAS HOTEL FIT VOUS PROPOSERAIT"),
        ),
    }
    for rel, pairs in hotel.items():
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        for replacement, pattern in pairs:
            text = re.sub(pattern, replacement, text)
        save(rel, text, original)


def fast_lane(lang: str) -> str:
    if lang == "fr":
        return '''<section class="explore-fast-lane" data-explore-fast-lane="true"><div class="wrap explore-fast-lane-inner"><div class="explore-fast-copy"><span>PRESSÉ, PICHOUN ?</span><strong>Deux ou trois heures, c’est largement assez pour faire quelque chose de bien. On vous dit quoi.</strong></div><div class="explore-fast-actions"><a class="button explore-fast-primary" href="/explore/2-3-heures/">J’AI 2 OU 3 HEURES</a><a class="explore-fast-secondary" href="/plages/">COMMENCER PAR LA MER →</a></div></div></section>'''
    return '''<section class="explore-fast-lane" data-explore-fast-lane="true"><div class="wrap explore-fast-lane-inner"><div class="explore-fast-copy"><span>IN A HURRY, PICHOUN?</span><strong>Two or three hours is still enough to do something good. We’ll tell you what.</strong></div><div class="explore-fast-actions"><a class="button explore-fast-primary" href="/en/explore/2-3-hours/">I HAVE 2 OR 3 HOURS</a><a class="explore-fast-secondary" href="/en/beaches/">START WITH THE SEA →</a></div></div></section>'''


def patch_explore_fast_lane() -> None:
    for rel, lang in (("en/explore/index.html", "en"), ("explore/index.html", "fr")):
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text

        # Remove the old action cluster from the Step 03 strip: the shortcut now
        # deserves its own full-width functional line.
        if lang == "en":
            text = text.replace(
                '<div class="hub-adoption-actions"><a class="button hub-primary-action" href="/en/explore/2-3-hours/">I have 2 or 3 hours</a><a class="hub-secondary-action" href="/en/beaches/">Start with the sea →</a></div>',
                ''
            )
        else:
            text = text.replace(
                '<div class="hub-adoption-actions"><a class="button hub-primary-action" href="/explore/2-3-heures/">J’ai 2 ou 3 heures</a><a class="hub-secondary-action" href="/plages/">Commencer par la mer →</a></div>',
                ''
            )

        if 'data-explore-fast-lane="true"' not in text:
            start = text.find('class="hub-adoption-cue hub-adoption-cue--step3"')
            if start < 0:
                raise RuntimeError(f"{rel}: Step 03 adoption cue not found")
            close = text.find("</aside>", start)
            if close < 0:
                raise RuntimeError(f"{rel}: Step 03 adoption cue closing tag not found")
            close += len("</aside>")
            text = text[:close] + fast_lane(lang) + text[close:]

        save(rel, text, original)


def restaurant_card(href: str, count: str, name: str, copy: str, more: str) -> str:
    return (
        f'<a class="restaurant-town-card" href="{href}">'
        f'<span class="restaurant-town-count">{count}</span>'
        f'<h3>{name}</h3><p>{copy}</p><span class="restaurant-town-more">{more}</span>'
        '</a>'
    )


def restaurant_block(lang: str) -> str:
    if lang == "fr":
        primary = [
            ("/restaurants/nice/", "12 ADRESSES", "Nice", "Socca, bistrots, mer et grand soir : la sélection la plus profonde."),
            ("/restaurants/villefranche-sur-mer/", "8 ADRESSES", "Villefranche · Beaulieu · Cap-Ferrat", "Quai, vieille ville, Beaulieu et grands soirs sur le Cap."),
            ("/restaurants/antibes/", "10 ADRESSES", "Antibes", "Vieille ville, Juan-les-Pins et Cap selon l’humeur."),
            ("/restaurants/cannes/", "10 ADRESSES", "Cannes", "Marché, bistrot, poisson, dîner chic ou très grand soir."),
            ("/restaurants/monaco/", "8 ADRESSES", "Monaco", "Du déjeuner simple au palace, sans prétendre que les prix n’existent pas."),
            ("/restaurants/menton/", "6 ADRESSES", "Menton", "Traditionnel, bistrot, pizza, feu de bois ou dîner-destination."),
            ("/restaurants/saint-tropez/", "8 ADRESSES", "Saint-Tropez", "Déjeuner facile, Ponche, port, soirée animée et grand soir."),
        ]
        secondary = [
            ("/restaurants/saint-paul-de-vence/", "4 ADRESSES", "Saint-Paul-de-Vence", "Du déjeuner léger à l’institution."),
            ("/restaurants/mougins/", "4 ADRESSES", "Mougins", "Bistrot, Provence, cuisine de produit ou soirée contemporaine."),
            ("/restaurants/theoule-sur-mer/", "4 ADRESSES", "Théoule-sur-Mer", "Brasserie, plage, poisson et grand dîner."),
            ("/restaurants/grasse/", "5 ADRESSES", "Grasse", "Vegan, bistrot, poisson, terrasse ou bastide."),
        ]
        more = "VOIR LES ADRESSES →"
        return (
            '<section class="restaurant-directory" data-restaurant-directory="true"><div class="wrap">'
            '<div class="restaurant-lead"><div class="restaurant-lead-copy"><span>LA RÈGLE</span>'
            '<h2>Choisissez d’abord la ville.</h2><p>Une excellente table à 45 minutes de votre journée reste une mauvaise recommandation. Choisissez la base, puis le restaurant. Mametas garde chaque liste assez courte pour permettre une vraie décision.</p>'
            '<a href="/riviera-guide/">Vous hésitez encore sur la base ? Comparez les villes →</a></div>'
            '<figure class="restaurant-lead-media"><img src="/assets/editorial/mametas-explore-restaurants-salad.webp" alt="Table de restaurant sur la Riviera" loading="eager" decoding="async"></figure></div>'
            '<div class="restaurant-group"><div class="restaurant-group-head"><span>LES BASES PRINCIPALES</span><p>Le plus de profondeur, sans annuaire.</p></div><div class="restaurant-town-grid">'
            + ''.join(restaurant_card(*x, more) for x in primary)
            + '</div></div><div class="restaurant-group restaurant-group--secondary"><div class="restaurant-group-head"><span>PLUS PETIT, TOUJOURS UTILE</span><p>Moins d’adresses. Pas de remplissage.</p></div><div class="restaurant-town-grid restaurant-town-grid--secondary">'
            + ''.join(restaurant_card(*x, more) for x in secondary)
            + '</div></div></div></section>'
        )
    primary = [
        ("/en/restaurants/nice/", "12 ADDRESSES", "Nice", "Socca, bistros, sea and the big night: the deepest list."),
        ("/en/restaurants/villefranche-sur-mer/", "8 ADDRESSES", "Villefranche · Beaulieu · Cap-Ferrat", "Quay, old town, Beaulieu and big nights on the Cap."),
        ("/en/restaurants/antibes/", "10 ADDRESSES", "Antibes", "Old town, Juan-les-Pins and the Cap according to the mood."),
        ("/en/restaurants/cannes/", "10 ADDRESSES", "Cannes", "Market, bistro, seafood, polished dinner or the full occasion."),
        ("/en/restaurants/monaco/", "8 ADDRESSES", "Monaco", "From a simple lunch to palace dining, without pretending prices do not exist."),
        ("/en/restaurants/menton/", "6 ADDRESSES", "Menton", "Traditional, bistro, pizza, wood fire or destination dinner."),
        ("/en/restaurants/saint-tropez/", "8 ADDRESSES", "Saint-Tropez", "Easy lunch, La Ponche, harbour, lively dinner and the big night."),
    ]
    secondary = [
        ("/en/restaurants/saint-paul-de-vence/", "4 ADDRESSES", "Saint-Paul-de-Vence", "From light lunch to institution."),
        ("/en/restaurants/mougins/", "4 ADDRESSES", "Mougins", "Bistro, Provence, product-led cooking or a contemporary evening."),
        ("/en/restaurants/theoule-sur-mer/", "4 ADDRESSES", "Théoule-sur-Mer", "Brasserie, beach, seafood and the big dinner."),
        ("/en/restaurants/grasse/", "5 ADDRESSES", "Grasse", "Vegan, bistro, seafood, terrace or bastide."),
    ]
    more = "SEE THE ADDRESSES →"
    return (
        '<section class="restaurant-directory" data-restaurant-directory="true"><div class="wrap">'
        '<div class="restaurant-lead"><div class="restaurant-lead-copy"><span>THE RULE</span>'
        '<h2>Choose the town first.</h2><p>A brilliant restaurant 45 minutes away from your day is still a bad recommendation. Pick the base, then the table. Mametas keeps every list short enough to make an actual decision.</p>'
        '<a href="/en/riviera-guide/">Still choosing the base? Compare the towns →</a></div>'
        '<figure class="restaurant-lead-media"><img src="/assets/editorial/mametas-explore-restaurants-salad.webp" alt="A Riviera restaurant table" loading="eager" decoding="async"></figure></div>'
        '<div class="restaurant-group"><div class="restaurant-group-head"><span>MAIN BASES</span><p>The deepest coverage, without turning into a directory.</p></div><div class="restaurant-town-grid">'
        + ''.join(restaurant_card(*x, more) for x in primary)
        + '</div></div><div class="restaurant-group restaurant-group--secondary"><div class="restaurant-group-head"><span>SMALLER DETOURS</span><p>Fewer addresses. No filler.</p></div><div class="restaurant-town-grid restaurant-town-grid--secondary">'
        + ''.join(restaurant_card(*x, more) for x in secondary)
        + '</div></div></div></section>'
    )


def patch_restaurants() -> None:
    for rel, lang in (("en/restaurants/index.html", "en"), ("restaurants/index.html", "fr")):
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        text = add_body_class(text, "restaurant-hub-polished")

        m = re.search(r'(<section class="page-hero">.*?</section>)(.*?)(</main>)', text, flags=re.S)
        if not m:
            raise RuntimeError(f"{rel}: restaurant page hero/main structure not found")
        block = restaurant_block(lang)
        text = text[:m.start()] + m.group(1) + block + m.group(3) + text[m.end():]
        save(rel, text, original)


PLACE_SLUGS = (
    "nice", "cannes", "antibes", "villefranche-cap-ferrat", "monaco",
    "menton", "eze", "saint-paul-de-vence", "saint-tropez",
)


def patch_places_width() -> None:
    for slug in PLACE_SLUGS:
        for rel in (f"en/riviera-guide/{slug}/index.html", f"riviera-guide/{slug}/index.html"):
            p = ROOT / rel
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            original = text
            text = add_body_class(text, "places-unified")
            save(rel, text, original)


def patch_css() -> None:
    ensure_css(
        "assets/v3.css",
        "/* Final marginal recipe 2026-09-25 */",
        r'''
/* FIT examples: one light narrative, not a dark slab. */
.adoption-home .riviera-fit-home-demo{box-shadow:none}
.adoption-home .riviera-fit-home-verdict{background:var(--white);border-top:1px solid var(--line)}
.adoption-home .riviera-fit-reality{background:transparent;border-top:1px solid var(--line)}
.adoption-home .riviera-fit-reality span{background:transparent}
.adoption-home .riviera-fit-home-demo>.riviera-fit-demo-label,
.adoption-home .riviera-fit-home-verdict .riviera-fit-demo-label{letter-spacing:.14em}
.adoption-home .riviera-fit-home-verdict .riviera-fit-demo-label{color:var(--coral)!important}

/* 2–3 hours is a product line of its own. */
.explore-fast-lane{border-top:3px solid var(--coral);border-bottom:1px solid var(--line);background:rgba(216,108,78,.055)}
.explore-fast-lane-inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:40px;align-items:center;padding-top:28px;padding-bottom:28px}
.explore-fast-copy span{display:block;margin-bottom:7px;color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
.explore-fast-copy strong{display:block;max-width:760px;font-family:var(--serif);font-size:clamp(24px,2.55vw,34px);font-weight:500;line-height:1.08}
.explore-fast-actions{display:flex;align-items:center;gap:18px;white-space:nowrap}
.explore-fast-primary{background:var(--coral);border-color:var(--coral)}
.explore-fast-secondary{font-size:9px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.adoption-hub--explore .hub-adoption-cue-inner{grid-template-columns:1fr}
.adoption-hub--explore .hub-adoption-actions{display:none}

/* Places: wide, but consistently centred. */
.places-unified main .wrap{width:min(100%,1180px)}
.places-unified .article-hero h1{max-width:1050px}
.places-unified .article-deck{max-width:900px}
.places-unified .article-cover{max-width:1180px;margin-left:auto;margin-right:auto}

@media(max-width:760px){
  .explore-fast-lane-inner{grid-template-columns:1fr;gap:18px}
  .explore-fast-actions{align-items:flex-start;flex-direction:column;white-space:normal}
  .explore-fast-primary{width:100%}
}
'''
    )

    ensure_css(
        "assets/site.css",
        "/* Final marginal recipe 2026-09-25 */",
        r'''
/* Restaurants: one visual lead, one coherent directory. */
.restaurant-hub-polished .page-hero{padding-bottom:50px}
.restaurant-directory{border-top:1px solid var(--line);padding:0 0 72px}
.restaurant-lead{display:grid;grid-template-columns:minmax(0,.82fr) minmax(420px,1.18fr);gap:44px;align-items:center;padding:46px 0}
.restaurant-lead-copy>span,.restaurant-group-head>span{display:block;margin-bottom:10px;color:var(--gold);font-size:10px;font-weight:700;letter-spacing:.17em;text-transform:uppercase}
.restaurant-lead-copy h2{margin:0 0 14px;font-size:clamp(34px,4vw,52px)}
.restaurant-lead-copy p{max-width:620px;margin:0 0 20px;color:var(--ink);font-size:16px;line-height:1.72}
.restaurant-lead-copy a{font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid var(--gold)}
.restaurant-lead-media{margin:0;overflow:hidden;background:var(--cream-deep)}
.restaurant-lead-media img{width:100%;aspect-ratio:16/9;object-fit:cover}
.restaurant-group{padding-top:34px;border-top:1px solid var(--line)}
.restaurant-group--secondary{margin-top:42px}
.restaurant-group-head{display:flex;align-items:end;justify-content:space-between;gap:24px;margin-bottom:18px}
.restaurant-group-head p{margin:0;color:var(--ink);font-size:12px}
.restaurant-town-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.restaurant-town-card{min-height:188px;padding:20px;border:1px solid var(--line);background:rgba(255,255,255,.17);display:flex;flex-direction:column}
.restaurant-town-card:hover{background:var(--cream-deep)}
.restaurant-town-count{color:var(--med-blue);font-size:9px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.restaurant-town-card h3{margin:12px 0 9px;font-size:clamp(23px,2.2vw,30px);line-height:1.06}
.restaurant-town-card p{margin:0;color:var(--ink);font-size:12.5px;line-height:1.55}
.restaurant-town-more{margin-top:auto;padding-top:16px;color:var(--gold);font-size:9px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}
.restaurant-town-grid--secondary .restaurant-town-card{min-height:165px}

/* Legacy Places pages now use the same wide-centred frame as V3 pages. */
.places-unified .article{max-width:1180px}
.places-unified .article>h1{max-width:1050px;margin-left:auto;margin-right:auto}
.places-unified .article>.standfirst{max-width:900px;margin-left:auto;margin-right:auto}
.places-unified .article>p,
.places-unified .article>h2,
.places-unified .article>h3,
.places-unified .article>ul,
.places-unified .article>.mini-rule,
.places-unified .article>.route-step,
.places-unified .article>.verdict,
.places-unified .article>.sources,
.places-unified .article>.source-box{
  max-width:820px;margin-left:auto;margin-right:auto
}
.places-unified .article>.fact-grid,
.places-unified .article>.destination-practical,
.places-unified .article>.destination-reality{max-width:1040px;margin-left:auto;margin-right:auto}
.places-unified .article>.article-visual,
.places-unified .article>.article-visual-pair,
.places-unified .article>.itinerary-stay-prompt{max-width:1000px;margin-left:auto;margin-right:auto}

@media(max-width:980px){
  .restaurant-lead{grid-template-columns:1fr}
  .restaurant-town-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:620px){
  .restaurant-directory{padding-bottom:54px}
  .restaurant-lead{gap:24px;padding:32px 0}
  .restaurant-town-grid{grid-template-columns:1fr}
  .restaurant-group-head{display:block}
  .restaurant-group-head p{margin-top:7px}
  .restaurant-town-card{min-height:0}
}
'''
    )

    ensure_css(
        "assets/hotel-engine.css",
        "/* Hotel Fit light demo refinement 2026-09-25 */",
        r'''
.hotel-fit-demo-panel{box-shadow:none}
.hotel-fit-demo-card{
  border-color:rgba(20,33,61,.16);
  background:var(--white);
  color:var(--ink);
}
.hotel-fit-demo-card h3{color:var(--ink)}
.hotel-fit-demo-card .hotel-fit-demo-copy p{color:var(--ink-soft)!important}
.hotel-fit-demo-card .hotel-fit-demo-copy strong{color:var(--ink)}
.hotel-fit-demo-card .hotel-fit-demo-catch{border-top-color:var(--line)}
.hotel-fit-demo-card:hover,.hotel-fit-demo-card:focus-visible{box-shadow:0 10px 24px rgba(20,33,61,.08)}
.hotel-fit-demo-section-label{display:flex;align-items:center;gap:7px}
'''
    )


def validate() -> None:
    checks = {
        "index.html": ("IF YOU HAD THE FOLLOWING CRITERIA…", "↓ MAMETAS RIVIERA FIT WOULD SUGGEST"),
        "fr/index.html": ("SI VOUS AVIEZ LES CRITÈRES SUIVANTS…", "↓ MAMETAS RIVIERA FIT VOUS PROPOSERAIT"),
        "en/hotels/index.html": ("IF YOUR PRIORITIES WERE AS FOLLOWS…", "↓ MAMETAS HOTEL FIT WOULD SUGGEST"),
        "hotels/index.html": ("SI VOS PRIORITÉS ÉTAIENT LES SUIVANTES…", "↓ MAMETAS HOTEL FIT VOUS PROPOSERAIT"),
        "en/explore/index.html": ('data-explore-fast-lane="true"', "IN A HURRY, PICHOUN?", "I HAVE 2 OR 3 HOURS"),
        "explore/index.html": ('data-explore-fast-lane="true"', "PRESSÉ, PICHOUN ?", "J’AI 2 OU 3 HEURES"),
        "en/restaurants/index.html": ('data-restaurant-directory="true"', "Choose the town first.", "mametas-explore-restaurants-salad.webp"),
        "restaurants/index.html": ('data-restaurant-directory="true"', "Choisissez d’abord la ville.", "mametas-explore-restaurants-salad.webp"),
    }
    errors: list[str] = []
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")

    for slug in PLACE_SLUGS:
        for rel in (f"en/riviera-guide/{slug}/index.html", f"riviera-guide/{slug}/index.html"):
            p = ROOT / rel
            if p.exists() and "places-unified" not in p.read_text(encoding="utf-8"):
                errors.append(f"{rel}: unified Places class missing")

    for rel, marker in (
        ("assets/v3.css", "/* Final marginal recipe 2026-09-25 */"),
        ("assets/site.css", "/* Final marginal recipe 2026-09-25 */"),
        ("assets/hotel-engine.css", "/* Hotel Fit light demo refinement 2026-09-25 */"),
    ):
        if marker not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel}: final recipe CSS missing")

    if errors:
        raise SystemExit("Final marginal recipe failed:\n- " + "\n- ".join(errors))


def main() -> int:
    patch_fit_linkage()
    patch_explore_fast_lane()
    patch_restaurants()
    patch_places_width()
    patch_css()
    validate()
    print(f"Final marginal recipe passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
