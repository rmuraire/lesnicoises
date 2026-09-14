#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

FR_CTA = "Ce lien mène directement vers l’hôtel sur Expedia. Vérifiez le tarif et les conditions à vos dates."
EN_CTA = "This link goes directly to the hotel on Expedia. Check the rate and conditions for your dates."
FR_DISC = "Transparence : ce lien est affilié. Mametas peut percevoir une commission si vous réservez, sans que cela influence notre sélection."
EN_DISC = "Transparency: this is an affiliate link. Mametas may earn a commission if you book, without influencing our selection."

CITY_EXITS = {
    "nice": ("/fr/planifier/cinq-jours-nice-sans-voiture/", "/restaurants/nice/", "/riviera-guide/nice/",
             "/plan/five-days-nice-no-car/", "/en/restaurants/nice/", "/en/riviera-guide/nice/"),
    "cannes": ("/riviera-guide/nice-ou-cannes/", "/restaurants/cannes/", "/riviera-guide/cannes/",
               "/en/riviera-guide/nice-or-cannes/", "/en/restaurants/cannes/", "/en/riviera-guide/cannes/"),
    "antibes": ("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-quatre", "/restaurants/antibes/", "/riviera-guide/antibes/",
                "/plan/five-days-nice-no-car/#day-four", "/en/restaurants/antibes/", "/en/riviera-guide/antibes/"),
    "monaco": ("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois", "/restaurants/monaco/", "/riviera-guide/monaco/",
               "/plan/five-days-nice-no-car/#day-three", "/en/restaurants/monaco/", "/en/riviera-guide/monaco/"),
    "menton": ("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois", "/restaurants/menton/", "/riviera-guide/menton/",
               "/plan/five-days-nice-no-car/#day-three", "/en/restaurants/menton/", "/en/riviera-guide/menton/"),
}


def city_from_path(path: Path):
    parts = [p.lower() for p in path.parts]
    for city in CITY_EXITS:
        if city in parts:
            return city
    return None


def exit_markup(city: str, fr: bool) -> str:
    a,b,c,d,e,f = CITY_EXITS[city]
    if fr:
        return (f'<section class="next-decisions hotel-next"><p class="eyebrow">La suite logique</p>'
                f'<h2>Ne choisissez pas seulement la chambre. Replacez-la dans le voyage.</h2>'
                f'<div class="next-links"><a href="{a}">Voir l’itinéraire</a><a href="{b}">Choisir les restaurants</a><a href="{c}">Comprendre la destination</a></div></section>')
    return (f'<section class="next-decisions hotel-next"><p class="eyebrow">Next useful decisions</p>'
            f'<h2>Do not choose the room in isolation. Put it back into the trip.</h2>'
            f'<div class="next-links"><a href="{d}">See the itinerary</a><a href="{e}">Choose restaurants</a><a href="{f}">Understand the destination</a></div></section>')


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="affiliate-cta"' not in text:
        return False
    fr = '<html lang="fr"' in text
    cta = FR_CTA if fr else EN_CTA
    disc = FR_DISC if fr else EN_DISC
    original = text

    # Keep the conversion box focused on the click: title, one practical sentence, button.
    text = re.sub(r'(<div class="affiliate-cta"><div><span class="label">.*?</span><h2>.*?</h2>)<p>.*?</p>(</div><a class="cta-button")',
                  lambda m: m.group(1) + '<p>' + cta + '</p>' + m.group(2), text, count=1, flags=re.S)
    # One disclosure only, neutral and explicit.
    text = re.sub(r'<p class="disclosure">.*?</p>', '<p class="disclosure">' + disc + '</p>', text, count=1, flags=re.S)

    # Important hotel detail pages should not end at sources/footer.
    city = city_from_path(path)
    if city and 'class="hotel-next"' not in text:
        marker = '<div class="sources">'
        pos = text.find(marker)
        if pos >= 0:
            text = text[:pos] + exit_markup(city, fr) + text[pos:]

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    roots = [ROOT / "hotels", ROOT / "en" / "hotels", ROOT / "fr" / "dormir", ROOT / "stay"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("index.html"):
            if process(path):
                changed.append(path.relative_to(ROOT).as_posix())
    print(f"Affiliate/hotel-exit pass updated {len(changed)} pages")
    for p in changed:
        print(p)

if __name__ == "__main__":
    main()
