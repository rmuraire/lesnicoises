#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
    "fr/planifier/cinq-jours-nice-sans-voiture/index.html": [
        ("Une bonne sélection, mais encore trop chère.", "Des options centrales plus posées, du milieu-haut au luxe."),
        ("Chic & mer", "Chic & expérience"),
        ("La partie la plus forte du catalogue actuel.", "Ici, l’hôtel fait volontairement partie du voyage."),
    ],
    "plan/five-days-nice-no-car/index.html": [
        ("The current shortlist is good, but still expensive.", "Calmer central options, from upper-mid to high-end."),
        ("Chic & sea", "Chic & experience"),
        ("The strongest part of the present catalogue.", "Here, the hotel deliberately becomes part of the trip."),
    ],
    "riviera-guide/nice-ou-cannes/index.html": [
        ("Nice offre davantage de personnalités et de localisations différentes, même si notre sélection Mametas actuelle est encore trop forte sur le haut de gamme et trop faible sur les prix raisonnables. On préfère corriger ce trou plutôt que le remplir avec des hôtels qu’on ne saurait défendre.", "Nice offre désormais vingt adresses avec davantage de personnalités, de localisations et de niveaux de dépense. Le bon filtre n’est plus « cher ou pas cher » : choisissez le rôle de l’hôtel, le quartier et votre plafond, puis comparez le tarif réel à vos dates."),
        ("Pratique, vivant, calme ou chic avec la mer.", "Pratique, vivant, calme ou hôtel-expérience, avec un vrai filtre budget."),
    ],
    "en/riviera-guide/nice-or-cannes/index.html": [
        ("Nice gives you a broader set of hotel personalities and locations, although our current Mametas shortlist is still stronger at the expensive end than at sensible mid-range prices. We are fixing that rather than filling the gap with recommendations we cannot defend.", "Nice now has twenty addresses across more locations, personalities and spend levels. The useful filter is no longer simply expensive or cheap: choose the hotel’s role, area and maximum spend, then compare the real rate for your dates."),
        ("Practical, lively, peaceful or chic by the sea.", "Practical, lively, peaceful or hotel-as-experience, with a real budget filter."),
    ],
}
def main() -> int:
    for rel, pairs in REPLACEMENTS.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in pairs:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"V1 release copy refreshed: {rel}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
