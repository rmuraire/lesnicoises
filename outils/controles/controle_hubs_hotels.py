#!/usr/bin/env python3
"""Contrôle de structure des pages hubs d'hôtels FR/EN (dossier site/).

Vérifie que chaque hub est bien formé : au moins deux sections d'hôtels
aux identifiants uniques, chaque section non vide, aucune carte d'hôtel
hors section ni imbriquée dans une autre carte. Le nombre exact d'hôtels
n'est pas imposé, pour qu'ajouter ou retirer un hôtel reste une simple
modification de page. Bloquant.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2] / "site"

# Hubs d'hôtels par ville (FR, EN). Nice utilise une autre famille de page.
HUBS = {
    "antibes": ("hotels/antibes/index.html", "en/hotels/antibes/index.html"),
    "cannes": ("hotels/cannes/index.html", "en/hotels/cannes/index.html"),
    "villefranche": ("hotels/villefranche-sur-mer/index.html", "en/hotels/villefranche-sur-mer/index.html"),
    "monaco": ("hotels/monaco/index.html", "en/hotels/monaco/index.html"),
    "menton": ("hotels/menton/index.html", "en/hotels/menton/index.html"),
    "saint-paul": ("hotels/saint-paul-de-vence/index.html", "en/hotels/saint-paul-de-vence/index.html"),
    "beaulieu": ("hotels/beaulieu-sur-mer/index.html", "en/hotels/beaulieu-sur-mer/index.html"),
    "mougins": ("hotels/mougins/index.html", "en/hotels/mougins/index.html"),
    "saint-tropez": ("hotels/saint-tropez/index.html", "en/hotels/saint-tropez/index.html"),
}


class HotelHubParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.articles = []
        self.sections = []
        self.cards = 0
        self.cards_per_section = Counter()
        self.section_ids = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        classes = set((props.get("class") or "").split())
        if tag == "section":
            section_id = props.get("id") if "hotel-style-section" in classes else None
            self.sections.append(section_id)
            if section_id:
                self.section_ids.append(section_id)
        if tag == "article":
            choice = "hotel-choice-card" in classes
            if choice:
                if any(self.articles):
                    self.errors.append("carte d'hôtel imbriquée dans une autre carte")
                self.cards += 1
                section = next((s for s in reversed(self.sections) if s), None)
                self.cards_per_section[section] += 1
            self.articles.append(choice)

    def handle_endtag(self, tag):
        if tag == "article":
            if self.articles:
                self.articles.pop()
            else:
                self.errors.append("</article> inattendu")
        if tag == "section":
            if self.sections:
                self.sections.pop()
            else:
                self.errors.append("</section> inattendu")


def main():
    errors = []
    count = 0
    for city, paths in HUBS.items():
        for rel in paths:
            path = ROOT / rel
            if not path.is_file():
                errors.append(f"{rel} : page hub absente")
                continue
            parser = HotelHubParser()
            parser.feed(path.read_text(encoding="utf-8"))
            if parser.cards < 1:
                errors.append(f"{rel} : aucune carte d'hôtel")
            if len(parser.section_ids) < 2:
                errors.append(f"{rel} : {len(parser.section_ids)} section(s), au moins 2 attendues")
            if len(set(parser.section_ids)) != len(parser.section_ids):
                errors.append(f"{rel} : identifiants de section en double")
            for section in parser.section_ids:
                if parser.cards_per_section[section] < 1:
                    errors.append(f"{rel} : section vide {section}")
            if parser.cards_per_section[None]:
                errors.append(f"{rel} : {parser.cards_per_section[None]} carte(s) hors section")
            errors.extend(f"{rel} : {e}" for e in parser.errors)
            count += 1
            print(f"Hub {rel} : {parser.cards} hôtels, {len(parser.section_ids)} sections")
    if errors:
        for error in errors:
            print("DÉFAUT HUB :", error)
        sys.exit(f"Structure des hubs d'hôtels : {len(errors)} défaut(s)")
    print(f"Structure des hubs d'hôtels conforme : {count} pages FR/EN")


if __name__ == "__main__":
    main()
