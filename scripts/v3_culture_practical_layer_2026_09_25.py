#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "culture/musee-matisse/index.html": {
        "lang":"fr",
        "address":"164 avenue des Arènes de Cimiez, 06000 Nice",
        "access":"Depuis le centre de Nice : bus Lignes d’Azur vers Cimiez. Le train n’est pas utile pour cette visite.",
        "time":"1 h 30 à 2 h. Ajoutez du temps si vous restez dans les arènes et le jardin de Cimiez.",
        "hours":"10 h-18 h jusqu’au 31 octobre, fermé le mardi. Plein tarif : 12 €.",
        "booking":"Billet en ligne utile les jours chargés. Les visites guidées ont leurs propres conditions de réservation.",
        "map":"https://www.google.com/maps/search/?api=1&query=Mus%C3%A9e+Matisse+Nice",
    },
    "en/culture/matisse-museum/index.html": {
        "lang":"en",
        "address":"164 avenue des Arènes de Cimiez, 06000 Nice",
        "access":"From central Nice: use the Lignes d’Azur bus network to Cimiez. The train is not useful for this visit.",
        "time":"1.5 to 2 hours. Add time if you stay around the Roman arena and Cimiez gardens.",
        "hours":"10am-6pm until 31 October, closed Tuesday. Full rate: €12.",
        "booking":"Online tickets are useful on busy days. Guided visits have their own booking rules.",
        "map":"https://www.google.com/maps/search/?api=1&query=Mus%C3%A9e+Matisse+Nice",
    },
    "culture/fondation-maeght/index.html": {
        "lang":"fr",
        "address":"623 chemin des Gardettes, 06570 Saint-Paul-de-Vence",
        "access":"Pas de train direct. TER jusqu’à Cagnes-sur-Mer puis bus 655. Arrêt Fondation Maeght : 10 à 12 min de marche avec pente raide.",
        "time":"2 à 3 h. Ici, les jardins comptent autant que les salles.",
        "hours":"Tous les jours 10 h-18 h, 10 h-19 h en juillet et août. Plein tarif : 18 €.",
        "booking":"Pas de réservation obligatoire pour les individuels. Billetterie en ligne disponible.",
        "map":"https://www.google.com/maps/search/?api=1&query=Fondation+Maeght+Saint-Paul-de-Vence",
    },
    "en/culture/fondation-maeght/index.html": {
        "lang":"en",
        "address":"623 chemin des Gardettes, 06570 Saint-Paul-de-Vence",
        "access":"No direct train. Take the TER to Cagnes-sur-Mer, then bus 655. Fondation Maeght stop: 10-12 min walk with a steep section.",
        "time":"2 to 3 hours. The gardens matter as much as the galleries here.",
        "hours":"Daily 10am-6pm, 10am-7pm in July and August. Full rate: €18.",
        "booking":"No reservation required for individual visitors. Online ticketing is available.",
        "map":"https://www.google.com/maps/search/?api=1&query=Fondation+Maeght+Saint-Paul-de-Vence",
    },
    "culture/musee-picasso-antibes/index.html": {
        "lang":"fr",
        "address":"Place Mariejol, 06600 Antibes",
        "access":"Depuis la gare d’Antibes, continuez à pied vers la vieille ville. Le musée est dans le château Grimaldi ; inutile de transformer ce trajet en correspondance de bus.",
        "time":"1 h 30 à 2 h. Plus si vous vous attardez sur la terrasse et dans la vieille ville.",
        "hours":"Depuis le 16 septembre : 10 h-13 h et 14 h-18 h, fermé le lundi. Plein tarif : 12 €.",
        "booking":"E-billet disponible. Réservation obligatoire pour les groupes de plus de 10 personnes.",
        "map":"https://www.google.com/maps/search/?api=1&query=Mus%C3%A9e+Picasso+Antibes+Place+Mariejol",
    },
    "en/culture/picasso-museum-antibes/index.html": {
        "lang":"en",
        "address":"Place Mariejol, 06600 Antibes",
        "access":"From Antibes station, continue on foot into the old town. The museum is in Château Grimaldi; there is little point inventing a bus connection for this last stretch.",
        "time":"1.5 to 2 hours. Longer if you linger on the terrace and in the old town.",
        "hours":"From 16 September: 10am-1pm and 2pm-6pm, closed Monday. Full rate: €12.",
        "booking":"E-tickets are available. Booking is required for groups over 10.",
        "map":"https://www.google.com/maps/search/?api=1&query=Mus%C3%A9e+Picasso+Antibes+Place+Mariejol",
    },
    "culture/villa-ephrussi/index.html": {
        "lang":"fr",
        "address":"1 avenue Ephrussi de Rothschild, 06230 Saint-Jean-Cap-Ferrat",
        "access":"TER jusqu’à Beaulieu-sur-Mer, puis bus 15 vers Passable-Rothschild, ou bus 607 jusqu’à Pont Saint-Jean puis environ 15 min à pied.",
        "time":"2 h 30 à 3 h. Les jardins sont la moitié de la visite, ne les traitez pas comme la sortie.",
        "hours":"10 h-18 h jusqu’au 1er novembre 2026. Plein tarif : 18 €.",
        "booking":"Réservation en ligne conseillée. Aucun créneau horaire n’est imposé pour la visite standard.",
        "map":"https://www.google.com/maps/search/?api=1&query=Villa+Ephrussi+de+Rothschild",
    },
    "en/culture/villa-ephrussi/index.html": {
        "lang":"en",
        "address":"1 avenue Ephrussi de Rothschild, 06230 Saint-Jean-Cap-Ferrat",
        "access":"TER train to Beaulieu-sur-Mer, then bus 15 towards Passable-Rothschild, or bus 607 to Pont Saint-Jean followed by about a 15-minute walk.",
        "time":"2.5 to 3 hours. The gardens are half the visit, not the exit route.",
        "hours":"10am-6pm until 1 November 2026. Full rate: €18.",
        "booking":"Online booking is recommended. No timed slot is imposed for the standard visit.",
        "map":"https://www.google.com/maps/search/?api=1&query=Villa+Ephrussi+de+Rothschild",
    },
    "culture/villa-kerylos/index.html": {
        "lang":"fr",
        "address":"Rue Gustave Eiffel, 06310 Beaulieu-sur-Mer",
        "access":"TER jusqu’à Beaulieu-sur-Mer. Bus 600 ou 15, arrêt Kérylos. En raison de travaux, la rue Gustave Eiffel est actuellement accessible uniquement aux piétons.",
        "time":"1 h à 1 h 30. C’est une vraie visite, pas une demi-journée.",
        "hours":"Jusqu’au 30 septembre : 10 h-18 h. Plein tarif : 15 €.",
        "booking":"Billetterie disponible. Un billet jumelé avec la Villa Ephrussi est proposé.",
        "map":"https://www.google.com/maps/search/?api=1&query=Villa+Kerylos+Beaulieu-sur-Mer",
    },
    "en/culture/villa-kerylos/index.html": {
        "lang":"en",
        "address":"Rue Gustave Eiffel, 06310 Beaulieu-sur-Mer",
        "access":"TER to Beaulieu-sur-Mer. Bus 600 or 15, Kérylos stop. Due to works, Rue Gustave Eiffel is currently pedestrian-only.",
        "time":"Allow 1 to 1.5 hours. This is a proper visit, not a half-day.",
        "hours":"Until 30 September: 10am-6pm. Full rate: €15.",
        "booking":"Ticketing is available. A combined ticket with Villa Ephrussi is offered.",
        "map":"https://www.google.com/maps/search/?api=1&query=Villa+Kerylos+Beaulieu-sur-Mer",
    },
    "culture/musee-oceanographique-monaco/index.html": {
        "lang":"fr",
        "address":"Avenue Saint-Martin, 98000 Monaco",
        "access":"TER jusqu’à Monaco-Monte-Carlo, puis environ 20 min à pied avec la bonne sortie, ou bus 1 / 2 jusqu’à Monaco-Ville. Parking des Pêcheurs sous le musée.",
        "time":"Environ 2 h, durée recommandée par le musée.",
        "hours":"En septembre : 10 h-19 h. Plein tarif adulte : 20,50 €.",
        "booking":"Billetterie en ligne disponible. Dernière entrée 30 min avant la fermeture.",
        "map":"https://www.google.com/maps/search/?api=1&query=Musee+Oceanographique+Monaco",
    },
    "en/culture/oceanographic-museum-monaco/index.html": {
        "lang":"en",
        "address":"Avenue Saint-Martin, 98000 Monaco",
        "access":"TER to Monaco-Monte-Carlo, then about 20 minutes on foot with the right station exit, or buses 1 / 2 to Monaco-Ville. Pêcheurs car park sits below the museum.",
        "time":"About 2 hours, the museum’s own recommended visit time.",
        "hours":"In September: 10am-7pm. Full adult rate: €20.50.",
        "booking":"Online ticketing is available. Last admission is 30 minutes before closing.",
        "map":"https://www.google.com/maps/search/?api=1&query=Oceanographic+Museum+Monaco",
    }
}

def block(data: dict[str,str]) -> str:
    fr = data["lang"] == "fr"
    labels = {
        "title":"LE PRATIQUE QUI CHANGE LA JOURNÉE" if fr else "THE PRACTICAL BIT THAT CHANGES THE DAY",
        "address":"Adresse" if fr else "Address",
        "access":"Y aller" if fr else "Getting there",
        "time":"Temps sur place" if fr else "Time needed",
        "hours":"Horaires & tarif" if fr else "Hours & rate",
        "booking":"Réservation" if fr else "Booking",
        "map":"Google Maps" if fr else "Google Maps",
        "mapcta":"Ouvrir la carte ↗" if fr else "Open map ↗",
        "checked":"Vérifié le 25 septembre 2026" if fr else "Checked 25 September 2026",
    }
    return (
        '<section class="culture-logistics" data-culture-logistics="true">'
        f'<div class="culture-logistics-head"><span>{labels["title"]}</span><small>{labels["checked"]}</small></div>'
        '<div class="culture-logistics-grid">'
        f'<div><b>{labels["address"]}</b><span>{data["address"]}</span></div>'
        f'<div><b>{labels["access"]}</b><span>{data["access"]}</span></div>'
        f'<div><b>{labels["time"]}</b><span>{data["time"]}</span></div>'
        f'<div><b>{labels["hours"]}</b><span>{data["hours"]}</span></div>'
        f'<div><b>{labels["booking"]}</b><span>{data["booking"]}</span></div>'
        f'<div><b>{labels["map"]}</b><span><a href="{data["map"].replace("&","&amp;")}" target="_blank" rel="noopener">{labels["mapcta"]}</a></span></div>'
        '</div></section>'
    )

def patch(rel: str, data: dict[str,str]) -> bool:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    original = text
    new_block = block(data)

    if 'data-culture-logistics="true"' in text:
        text = re.sub(r'<section class="culture-logistics" data-culture-logistics="true">.*?</section>', new_block, text, count=1, flags=re.S)
    else:
        text, n = re.subn(r'<div class="culture-practical">.*?</div>', new_block, text, count=1, flags=re.S)
        if n != 1:
            raise RuntimeError(f"{rel}: practical block not found")

    fr = data["lang"] == "fr"
    if "mametas-checked" in text:
        if fr:
            text = re.sub(r'(<a class="mametas-checked"[^>]*><span>Mametas Checked</span><small>).*?(</small></a>)',
                          r'\1Informations pratiques revérifiées · 25 septembre 2026\2', text, count=1, flags=re.S)
        else:
            text = re.sub(r'(<a class="mametas-checked"[^>]*><span>Mametas Checked</span><small>).*?(</small></a>)',
                          r'\1Practical information rechecked · 25 September 2026\2', text, count=1, flags=re.S)
    else:
        badge = ('<a class="mametas-checked" href="/methode/"><span>Mametas Checked</span><small>Informations pratiques revérifiées · 25 septembre 2026</small></a>'
                 if fr else
                 '<a class="mametas-checked" href="/en/method/"><span>Mametas Checked</span><small>Practical information rechecked · 25 September 2026</small></a>')
        m = re.search(r'(<p class="standfirst">.*?</p>)', text, flags=re.S)
        if not m:
            raise RuntimeError(f"{rel}: standfirst not found")
        text = text[:m.end()] + badge + text[m.end():]

    if fr:
        text = re.sub(r'Vérifié (?:le |en )?(?:\d{1,2} [a-zûé]+ 2026|août 2026)\. Les horaires changent\.',
                      'Vérifié le 25 septembre 2026. Les horaires changent.', text)
    else:
        text = re.sub(r'Checked (?:on |in )?(?:\d{1,2} [A-Za-z]+ 2026|August 2026)\. Opening hours change\.',
                      'Checked 25 September 2026. Opening hours change.', text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False

def main() -> int:
    changed=[]
    for rel,data in PAGES.items():
        if patch(rel,data):
            changed.append(rel)
    for rel in PAGES:
        text=(ROOT/rel).read_text(encoding="utf-8")
        if 'data-culture-logistics="true"' not in text:
            raise RuntimeError(f"{rel}: logistics block missing")
        if "25 septembre 2026" not in text and "25 September 2026" not in text:
            raise RuntimeError(f"{rel}: freshness date missing")
    print(f"Culture practical V3 layer passed; patched {len(changed)} pages.")
    for rel in changed:
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
