#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATCHES = {
    "hotels/finder/index.html": (
        "Choisissez tranquillement vos critères, puis lancez la recherche. Rien ne bouge avant que vous ayez fini. Ensuite, trois ou quatre adresses maximum — avec la raison et le compromis.",
        "Choisissez tranquillement vos critères, puis lancez la recherche. Si vous choisissez seulement une ville, Mametas vous montre toutes les adresses retenues dans cette ville. Dès que vous ajoutez un critère, le moteur resserre la sélection à trois ou quatre options — avec la raison et le compromis.",
        "Méthode : le moteur relit les sélections éditoriales Mametas par destination, puis pondère uniquement les critères explicitement décrits sur ces pages. Les tarifs et disponibilités restent ceux d’Expedia au moment où vous cliquez.",
        "Méthode : le moteur travaille uniquement à partir de la sélection éditoriale Mametas et de critères documentés. Les tarifs et disponibilités sont ceux du partenaire de réservation au moment où vous cliquez.",
    ),
    "en/hotels/finder/index.html": (
        "Choose your criteria first, then run the search. Nothing reshuffles while you are thinking. You get three or four addresses at most — with the reason and the catch.",
        "Choose your criteria first, then run the search. If you pick only a town, Mametas shows every hotel we kept there. Add another criterion and the finder narrows the result to three or four options — with the reason and the catch.",
        "Method: the finder reads Mametas’ destination hotel selections, then weights only criteria explicitly described on those pages. Rates and availability remain Expedia’s when you click.",
        "Method: the finder works only from the Mametas editorial selection and documented criteria. Rates and availability are those of the booking partner when you click.",
    ),
}


def main() -> int:
    changed = []
    for rel, (old_deck, new_deck, old_method, new_method) in PATCHES.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        original = text
        text = text.replace(old_deck, new_deck)
        text = text.replace(old_method, new_method)
        text = re.sub(r"/assets/hotel-engine\.js\?v=\d+", "/assets/hotel-engine.js?v=3", text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)
    print(f"Hotel finder hotfix updated {len(changed)} page(s).")
    for rel in changed:
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
