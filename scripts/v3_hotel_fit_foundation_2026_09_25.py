#!/usr/bin/env python3
from __future__ import annotations

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FR_DESTINATIONS = {
    "riviera-guide/menton/index.html": "menton",
    "riviera-guide/antibes/index.html": "antibes",
    "riviera-guide/villefranche-cap-ferrat/index.html": "villefranche",
    "riviera-guide/monaco/index.html": "monaco",
    "riviera-guide/cannes/index.html": "cannes",
    "riviera-guide/eze/index.html": "eze",
}
EN_DESTINATIONS = {
    "en/riviera-guide/menton/index.html": "menton",
    "en/riviera-guide/antibes/index.html": "antibes",
    "en/riviera-guide/villefranche-cap-ferrat/index.html": "villefranche",
    "en/riviera-guide/monaco/index.html": "monaco",
    "en/riviera-guide/cannes/index.html": "cannes",
    "en/riviera-guide/eze/index.html": "eze",
}

FIT_PROFILES = {
    "fr": {
        "pratique-central": (["car-free","excursions","value","old-town"], ["hotel-as-trip","beach-first"], "Un séjour où la plage ou l’hôtel lui-même doit être le sujet.", "On gagne en simplicité et en déplacements ce qu’on perd en grand spectacle hôtelier."),
        "vivant-facile": (["city-life","beach-first","car-free"], ["quiet","excursions"], "Le calme absolu ou un séjour construit autour des départs en train.", "La plage et les soirées sont faciles. Le retrait l’est beaucoup moins."),
        "riviera-bord-de-mer": (["beach-first","hotel-as-trip","romantic"], ["value","excursions"], "Un séjour très rationnel ou centré sur les excursions.", "La mer et l’ambiance gagnent. Le budget et la logistique peuvent suivre derrière."),
        "palaces-grand-spectacle": (["hotel-as-trip","beach-first","city-life"], ["value","quiet"], "Un séjour discret ou attentif au budget.", "Vous payez aussi pour être dans le spectacle cannois. Autant vouloir le spectacle."),
        "luxe-central": (["hotel-as-trip","beach-first","city-life","car-free"], ["value","quiet"], "Le retrait total ou un arbitrage serré sur le prix.", "Très peu de friction sur place, mais un positionnement tarifaire qui sait où il habite."),
        "charme-plus-intime": (["city-life","car-free","romantic"], ["hotel-as-trip"], "Ceux qui veulent un grand hôtel-destination avec tous les services.", "Plus de personnalité et moins de cérémonial, avec des équipements souvent plus limités."),
        "port-sans-voiture": (["car-free","beach-first","old-town","quiet"], ["excursions"], "Un programme qui traverse la côte tous les jours.", "La baie est simple à vivre. Le rôle de hub régional est moins convaincant."),
        "grand-luxe-retrait": (["hotel-as-trip","quiet","romantic","beach-first"], ["value","excursions","city-life"], "Un séjour urbain, économique ou construit sur des départs quotidiens.", "On vient ici pour ralentir. Si vous partez toute la journée, vous payez une partie du produit sans l’utiliser."),
        "palace-classique": (["hotel-as-trip","city-life","romantic"], ["value","quiet"], "Un séjour sobre ou attentif au budget.", "L’adresse fait partie du voyage. À Monaco, le décor et le service se paient aussi."),
        "resort-plus-detendu": (["hotel-as-trip","quiet"], ["value","old-town"], "Ceux qui veulent tout faire à pied autour du Casino.", "Plus d’espace et de respiration, contre un peu moins d’immersion dans le cœur cérémoniel."),
        "pratique-budget": (["car-free","value","old-town","excursions"], ["hotel-as-trip"], "Un séjour où l’hôtel doit être une destination en soi.", "Très utile pour vivre Menton et rayonner à l’est, moins mémorable comme expérience hôtelière."),
        "mer-calme": (["beach-first","quiet","romantic","car-free"], ["city-life"], "Les voyageurs qui veulent surtout soirées et animation.", "La mer et le calme gagnent. Le centre reste accessible, mais n’est pas toujours sous la fenêtre."),
        "riviera-plus-chic": (["beach-first","hotel-as-trip","quiet","romantic"], ["value"], "Un séjour où le prix doit rester le premier arbitre.", "Plus de confort et de mer, avec un supplément Riviera assumé."),
        "retraite-chic": (["quiet","hotel-as-trip","romantic"], ["car-free","excursions","beach-first"], "Un séjour sans voiture ou centré sur la côte.", "Très bon pour ralentir. Beaucoup moins pour improviser dix déplacements par jour."),
        "simple-calme": (["quiet","value"], ["car-free","beach-first","city-life"], "Ceux qui veulent la mer, la ville ou les transports devant la porte.", "Le calme et le prix sont le sujet. La localisation demande davantage d’organisation."),
        "village-caractere": (["old-town","romantic","hotel-as-trip"], ["excursions","beach-first"], "Un séjour tourné vers la côte ou les transports quotidiens.", "Dormir dans ou près du village change l’expérience, mais pas la géographie de l’arrière-pays."),
        "calme-retraite": (["quiet","hotel-as-trip","romantic"], ["car-free","city-life"], "Ceux qui veulent sortir à pied le soir ou voyager sans voiture.", "Le retrait fonctionne précisément parce qu’il y a moins de choses au pied de la porte."),
        "design-raffine": (["hotel-as-trip","romantic","quiet"], ["value","excursions"], "Un séjour où l’hôtel sert surtout de base pratique.", "Vous payez la singularité du lieu. Il faut avoir envie d’en profiter."),
        "bon-equilibre": (["quiet","value","romantic"], ["beach-first","city-life"], "Une priorité plage ou vie urbaine.", "Bon compromis pour Saint-Paul, sans transformer l’adresse en destination à elle seule."),
        "saint-tropez-meme": (["city-life","hotel-as-trip","romantic"], ["value","excursions"], "Un séjour économique ou conçu pour parcourir toute la Côte.", "Vous achetez Saint-Tropez lui-même. Le tarif et la circulation font partie du paquet."),
        "ramatuelle-retrait": (["quiet","beach-first","hotel-as-trip","romantic"], ["car-free","city-life"], "Un séjour sans voiture ou des soirées spontanées au village.", "Pampelonne et le retrait gagnent. Les transferts deviennent une vraie variable."),
        "gassin-resort": (["hotel-as-trip","quiet","beach-first"], ["car-free","old-town"], "Ceux qui veulent Saint-Tropez à pied.", "Le resort fonctionne comme destination. Le village, lui, demande un déplacement."),
        "sainte-maxime-autre-rive": (["value","beach-first","city-life"], ["excursions"], "Ceux qui veulent être réellement basés à Saint-Tropez.", "Vous gagnez une autre échelle de prix, mais vous êtes de l’autre côté du golfe."),
        "pratique-sans-spectacle": (["car-free","quiet","value"], ["hotel-as-trip","city-life"], "Un hôtel-destination ou une vie nocturne importante.", "Beaulieu reste simple et calme. L’hôtel fait le travail sans chercher à devenir le voyage."),
        "port-riviera": (["beach-first","quiet","hotel-as-trip","romantic","car-free"], ["value","city-life"], "Une priorité budget ou vie urbaine.", "La mer et le calme sont très faciles. L’animation est ailleurs."),
    },
    "en": {
        "practical-central": (["car-free","excursions","value","old-town"], ["hotel-as-trip","beach-first"], "A trip where the beach or the hotel itself needs to be the point.", "You gain simplicity and movement, and give up some hotel theatre."),
        "lively-easy": (["city-life","beach-first","car-free"], ["quiet","excursions"], "Absolute quiet or a trip built around repeated train departures.", "Beach and evenings are easy. Retreat is much less so."),
        "riviera-seafront": (["beach-first","hotel-as-trip","romantic"], ["value","excursions"], "A highly practical or day-trip-heavy stay.", "Sea and atmosphere win. Budget and logistics may follow behind."),
        "palaces-spectacle": (["hotel-as-trip","beach-first","city-life"], ["value","quiet"], "A discreet stay or close budget control.", "You are also paying to be inside the Cannes spectacle. Better to want the spectacle."),
        "central-luxury": (["hotel-as-trip","beach-first","city-life","car-free"], ["value","quiet"], "Total retreat or a tight price trade-off.", "Very little friction on the ground, with rates that know exactly where they are."),
        "character-more-intimate": (["city-life","car-free","romantic"], ["hotel-as-trip"], "Travellers who want a full destination hotel with every service.", "More personality and less ceremony, usually with fewer facilities."),
        "harbour-car-free": (["car-free","beach-first","old-town","quiet"], ["excursions"], "An itinerary that crosses the coast every day.", "The bay is easy to live. The regional-hub role is less convincing."),
        "grand-luxury-retreat": (["hotel-as-trip","quiet","romantic","beach-first"], ["value","excursions","city-life"], "An urban, value-led or daily-departure trip.", "You come here to slow down. Leave all day and you are paying for product you do not use."),
        "classic-palace": (["hotel-as-trip","city-life","romantic"], ["value","quiet"], "A low-key stay or close budget control.", "The address is part of the trip. In Monaco, setting and service cost money too."),
        "resort-more-relaxed": (["hotel-as-trip","quiet"], ["value","old-town"], "Travellers who want everything around Casino Square on foot.", "More space and breathing room, with less immersion in the ceremonial core."),
        "practical-budget": (["car-free","value","old-town","excursions"], ["hotel-as-trip"], "A stay where the hotel needs to be a destination in itself.", "Very useful for Menton and the eastern coast, less memorable as a hotel experience."),
        "sea-quiet": (["beach-first","quiet","romantic","car-free"], ["city-life"], "Travellers mainly after nightlife and activity.", "Sea and calm win. The centre remains accessible, but is not always under the window."),
        "riviera-more-polished": (["beach-first","hotel-as-trip","quiet","romantic"], ["value"], "A trip where price needs to remain the first filter.", "More comfort and sea, with a clear Riviera premium."),
        "chic-retreat": (["quiet","hotel-as-trip","romantic"], ["car-free","excursions","beach-first"], "A car-free trip or one centred on the coast.", "Excellent for slowing down. Much less useful for ten improvised movements a day."),
        "simple-quiet": (["quiet","value"], ["car-free","beach-first","city-life"], "Travellers who want sea, city or transport at the door.", "Calm and price are the point. The location asks for more organisation."),
        "village-character": (["old-town","romantic","hotel-as-trip"], ["excursions","beach-first"], "A coast-led trip or one built on daily transport.", "Sleeping in or near the village changes the experience, not the inland geography."),
        "quiet-retreat": (["quiet","hotel-as-trip","romantic"], ["car-free","city-life"], "Travellers who want spontaneous evenings on foot or no car.", "The retreat works because there is less at the door."),
        "design-refined": (["hotel-as-trip","romantic","quiet"], ["value","excursions"], "A stay where the hotel is mainly a practical base.", "You are paying for the singularity of the place. You need to want to use it."),
        "balanced-choice": (["quiet","value","romantic"], ["beach-first","city-life"], "A beach-first or urban trip.", "A sound Saint-Paul compromise without making the hotel the entire destination."),
        "saint-tropez-itself": (["city-life","hotel-as-trip","romantic"], ["value","excursions"], "A value trip or one designed to cover the whole Riviera.", "You are buying Saint-Tropez itself. Rates and traffic come in the package."),
        "ramatuelle-retreat": (["quiet","beach-first","hotel-as-trip","romantic"], ["car-free","city-life"], "A car-free stay or spontaneous evenings in the village.", "Pampelonne and retreat win. Transfers become a real variable."),
        "gassin-resort": (["hotel-as-trip","quiet","beach-first"], ["car-free","old-town"], "Travellers who want Saint-Tropez on foot.", "The resort works as a destination. The village still requires a transfer."),
        "sainte-maxime-opposite-shore": (["value","beach-first","city-life"], ["excursions"], "Travellers who want to be genuinely based in Saint-Tropez.", "You gain another price scale, but you are on the other side of the gulf."),
        "practical-low-key": (["car-free","quiet","value"], ["hotel-as-trip","city-life"], "A destination hotel or important nightlife.", "Beaulieu stays simple and calm. The hotel does the job without trying to become the trip."),
        "harbour-riviera": (["beach-first","quiet","hotel-as-trip","romantic","car-free"], ["value","city-life"], "A budget-first or urban trip.", "Sea and calm are easy. The activity is elsewhere."),
    },
}

changed = []

def write_if_changed(rel: str, text: str, original: str) -> None:
    if text != original:
        path = ROOT / rel
        path.write_text(text, encoding="utf-8")
        changed.append(rel)

def patch_finder(rel: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text

    if lang == "fr":
        pairs = (
            ("<title>Trouver votre hôtel sur la Côte d’Azur | Mametas</title>",
             "<title>Hotel Fit : trouver l’hôtel qui colle à votre séjour | Mametas</title>"),
            ("L’outil Mametas réduit notre sélection d’hôtels sur la Côte d’Azur selon votre base, votre style de séjour et la géographie qui compte vraiment.",
             "Hotel Fit réduit la sélection Mametas selon votre base, votre budget, votre mobilité et ce que l’hôtel doit réellement faire pour le séjour."),
            ('<p class="eyebrow">Le moteur hôtel Mametas</p>',
             '<p class="eyebrow">HOTEL FIT · LE MOTEUR HÔTEL MAMETAS</p>'),
            ("<h1>Parlez-nous de votre séjour. On fait le tri.</h1>",
             "<h1>Dites-nous ce qui compte. On vous dit où dormir.</h1>"),
            ("Choisissez vos critères, puis laissez Mametas couper dans la liste. Trois ou quatre adresses maximum, avec la raison et le compromis.",
             "Pas une liste d’hôtels avec quinze filtres décoratifs. Donnez-nous la base, le rôle de l’hôtel, la géographie, la mobilité et le budget. Hotel Fit garde quelques options et explique pourquoi elles collent."),
            ("<h2>Cinq choix. Puis seulement les hôtels qui collent.</h2>",
             "<h2>Cinq choix. Une sélection courte et expliquée.</h2>"),
            ("Le moteur travaille sur les hôtels déjà retenus par Mametas. Il ne prétend pas connaître un prix en temps réel et ne classe jamais une adresse selon une commission.",
             "Hotel Fit travaille uniquement sur les hôtels déjà retenus par Mametas. Il ne connaît pas votre tarif en temps réel et ne classe jamais une adresse selon une commission."),
        )
    else:
        pairs = (
            ("<title>Find your French Riviera hotel | Mametas</title>",
             "<title>Hotel Fit: find the French Riviera hotel that fits | Mametas</title>"),
            ("The Mametas hotel finder narrows our French Riviera hotel selection by base, trip style and the geography that actually matters to you.",
             "Hotel Fit narrows the Mametas hotel selection by base, budget, mobility and what the hotel actually needs to do for your trip."),
            ('<p class="eyebrow">The Mametas hotel finder</p>',
             '<p class="eyebrow">HOTEL FIT · THE MAMETAS HOTEL TOOL</p>'),
            ("<h1>Tell us how you travel. We’ll make the shortlist.</h1>",
             "<h1>Tell us what matters. We’ll tell you where to sleep.</h1>"),
            ("Choose your criteria, then let Mametas cut the list down. Three or four addresses at most, with the reason and the catch.",
             "Not a hotel dump with fifteen decorative filters. Give us the base, the hotel’s role, geography, mobility and budget. Hotel Fit keeps a few options and explains why they fit."),
            ("<h2>Five choices. Then only the hotels that fit.</h2>",
             "<h2>Five choices. A short, explained selection.</h2>"),
            ("The finder works only from hotels already selected by Mametas. It does not pretend to know a live price and never ranks an address by commission.",
             "Hotel Fit works only from hotels already selected by Mametas. It does not know your live rate and never ranks an address by commission."),
        )

    for old, new in pairs:
        text = text.replace(old, new)

    text = re.sub(r"/assets/hotel-engine\.js\?v=\d+", "/assets/hotel-engine.js?v=7", text)
    text = re.sub(r"/assets/hotel-engine\.css\?v=\d+", "/assets/hotel-engine.css?v=8", text)
    text = text.replace("16 septembre 2026", "25 septembre 2026")
    text = text.replace("16 September 2026", "25 September 2026")

    write_if_changed(rel, text, original)

def patch_hotel_hub(rel: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace("<h2>Trouver votre hôtel</h2>", "<h2>Hotel Fit</h2>")
        text = text.replace(">Lancer l’outil hôtel</a>", ">Lancer Hotel Fit</a>")
        text = text.replace("Vous préférez qu’on tranche ?", "Vous préférez qu’on tranche ?")
    else:
        text = text.replace("<h2>Find your hotel</h2>", "<h2>Hotel Fit</h2>")
        text = text.replace(">Open the hotel finder</a>", ">Open Hotel Fit</a>")
    write_if_changed(rel, text, original)

def patch_chooser(rel: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace("<h3>Hotel Finder</h3>", "<h3>Hotel Fit</h3>")
        text = text.replace("Le Chooser décide de la Riviera. Le Hotel Finder résout le problème suivant une fois la géographie fixée.",
                            "Riviera Fit décide de la base. Hotel Fit résout le problème suivant une fois la géographie fixée.")
        text = text.replace("Le Chooser décide la Riviera. Le Hotel Finder résout le problème suivant une fois la géographie fixée.",
                            "Riviera Fit décide de la base. Hotel Fit résout le problème suivant une fois la géographie fixée.")
    else:
        text = text.replace("<h3>Hotel Finder</h3>", "<h3>Hotel Fit</h3>")
        text = text.replace("The Chooser decides the Riviera. The Hotel Finder solves the next problem once geography is already settled.",
                            "Riviera Fit decides the base. Hotel Fit solves the next problem once geography is settled.")
    write_if_changed(rel, text, original)

def inject_shortlist_cta(rel: str, base: str, lang: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text

    if 'data-hotel-fit-cta="true"' in text:
        return

    hotel_link = re.search(r'href="[^"]*/hotels/[^"]+"', text)
    if not hotel_link:
        raise RuntimeError(f"{rel}: expected at least one hotel link")

    paragraph_end = text.find("</p>", hotel_link.end())
    if paragraph_end < 0:
        raise RuntimeError(f"{rel}: no paragraph end after first hotel link")
    paragraph_end += len("</p>")

    if lang == "fr":
        url = f"/hotels/finder/?base={base}" if base != "eze" else "/hotels/finder/"
        block = (
            '<div class="source-box hotel-fit-cta" data-hotel-fit-cta="true">'
            '<strong>Sélection courte.</strong> Ces adresses servent de repères, pas de liste exhaustive. '
            f'<a href="{url}">Ouvrir Hotel Fit pour élargir selon votre budget, votre mobilité et le rôle de l’hôtel →</a>'
            '</div>'
        )
    else:
        url = f"/en/hotels/finder/?base={base}" if base != "eze" else "/en/hotels/finder/"
        block = (
            '<div class="source-box hotel-fit-cta" data-hotel-fit-cta="true">'
            '<strong>Short selection.</strong> These hotels are reference points, not the full list. '
            f'<a href="{url}">Open Hotel Fit to widen the search by budget, mobility and the hotel’s role →</a>'
            '</div>'
        )

    text = text[:paragraph_end] + block + text[paragraph_end:]
    write_if_changed(rel, text, original)

def inject_hub_fit_profiles() -> None:
    hub_pairs = []
    for path in sorted((ROOT / "hotels").glob("*/index.html")):
        if path.parent.name == "finder":
            continue
        hub_pairs.append((path, "fr"))
    for path in sorted((ROOT / "en" / "hotels").glob("*/index.html")):
        if path.parent.name == "finder":
            continue
        hub_pairs.append((path, "en"))

    for path, lang in hub_pairs:
        text = path.read_text(encoding="utf-8")
        original = text
        for section_id, profile in FIT_PROFILES[lang].items():
            best, not_for, not_for_text, tradeoff = profile
            section_re = re.compile(
                rf'(<section[^>]+id="{re.escape(section_id)}"[^>]*>)(.*?)(</section>)',
                re.S,
            )
            match = section_re.search(text)
            if not match:
                continue
            body = match.group(2)
            attrs = (
                f' data-fit-best="{escape(" ".join(best), quote=True)}"'
                f' data-fit-not-for="{escape(" ".join(not_for), quote=True)}"'
                f' data-fit-not-for-text="{escape(not_for_text, quote=True)}"'
                f' data-fit-tradeoff="{escape(tradeoff, quote=True)}"'
            )
            def card_repl(card_match: re.Match[str]) -> str:
                existing = card_match.group(1)
                existing = re.sub(r'\sdata-fit-(?:best|not-for|not-for-text|tradeoff)="[^"]*"', "", existing)
                return '<article class="hotel-choice-card"' + existing + attrs + '>'
            body = re.sub(r'<article class="hotel-choice-card"([^>]*)>', card_repl, body)
            text = text[:match.start(2)] + body + text[match.end(2):]

        if lang == "fr" and path.as_posix().endswith("hotels/villefranche-sur-mer/index.html"):
            text = text.replace("02 · Grand luxe &amp; retrait", "02 · Cap-Ferrat &amp; retrait")
            text = text.replace("<span>Grand luxe &amp; retrait</span>", "<span>Cap-Ferrat &amp; retrait</span>")
        if lang == "en" and path.as_posix().endswith("en/hotels/villefranche-sur-mer/index.html"):
            text = text.replace("02 · Grand luxury &amp; retreat", "02 · Cap-Ferrat &amp; retreat")
            text = text.replace("<span>Grand luxury &amp; retreat</span>", "<span>Cap-Ferrat &amp; retreat</span>")

        if text != original:
            rel = str(path.relative_to(ROOT))
            path.write_text(text, encoding="utf-8")
            if rel not in changed:
                changed.append(rel)

def validate() -> None:
    errors = []
    for rel in ("hotels/finder/index.html", "en/hotels/finder/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "Hotel Fit" not in text:
            errors.append(f"{rel}: Hotel Fit naming missing")
        if "/assets/hotel-engine.js?v=7" not in text:
            errors.append(f"{rel}: engine cache bust missing")

    for rel, base in {**FR_DESTINATIONS, **EN_DESTINATIONS}.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        if 'data-hotel-fit-cta="true"' not in text:
            errors.append(f"{rel}: Hotel Fit shortlist CTA missing")

    engine = (ROOT / "assets/hotel-engine.js").read_text(encoding="utf-8")
    for needle in ("bestForText(hotel)", "fitText(hotel, 'notForText')", "URLSearchParams"):
        if needle not in engine:
            errors.append(f"assets/hotel-engine.js: missing {needle}")

    if errors:
        raise SystemExit("V3 Hotel Fit foundation failed:\n- " + "\n- ".join(errors))

def main() -> int:
    patch_finder("hotels/finder/index.html", "fr")
    patch_finder("en/hotels/finder/index.html", "en")
    patch_hotel_hub("hotels/index.html", "fr")
    patch_hotel_hub("en/hotels/index.html", "en")
    patch_chooser("riviera-chooser/index.html", "fr")
    patch_chooser("en/riviera-chooser/index.html", "en")
    inject_hub_fit_profiles()

    for rel, base in FR_DESTINATIONS.items():
        inject_shortlist_cta(rel, base, "fr")
    for rel, base in EN_DESTINATIONS.items():
        inject_shortlist_cta(rel, base, "en")

    validate()
    print(f"V3 Hotel Fit foundation passed; patched {len(changed)} generated file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
