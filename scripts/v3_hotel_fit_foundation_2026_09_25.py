#!/usr/bin/env python3
from __future__ import annotations

import re
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

    text = re.sub(r"/assets/hotel-engine\.js\?v=\d+", "/assets/hotel-engine.js?v=6", text)
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

def validate() -> None:
    errors = []
    for rel in ("hotels/finder/index.html", "en/hotels/finder/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "Hotel Fit" not in text:
            errors.append(f"{rel}: Hotel Fit naming missing")
        if "/assets/hotel-engine.js?v=6" not in text:
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
