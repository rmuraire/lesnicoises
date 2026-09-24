#!/usr/bin/env python3
from __future__ import annotations
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if os.environ.get("MAMETAS_ROOT"):
    ROOT = Path(os.environ["MAMETAS_ROOT"]).resolve()

changed = []

def save(rel, text, original):
    if text != original:
        (ROOT / rel).write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)

def patch(rel, pairs):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        text = text.replace(old, new)
    save(rel, text, original)

def remove_expired_home_card(rel, fr=False):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if fr:
        old = '<a class="now-card" href="/bons-plans/septembre-2026/"><time datetime="2026-09-08">8-13 septembre</time><h3>Cannes change de rythme</h3><p>Une grosse semaine nautique : improviser son hôtel devient un loisir discutable.</p></a>'
    else:
        old = '<a class="now-card" href="/en/good-finds/september-2026/"><time datetime="2026-09-08">8-13 September</time><h3>Cannes changes gear</h3><p>A major yachting week: accommodation improvisation becomes a poor hobby.</p></a>'
    if text.count(old) != 1:
        raise RuntimeError(f"{rel}: expired Cannes card not found exactly once")
    save(rel, text.replace(old, ""), original)

def patch_september():
    patch("en/good-finds/september-2026/index.html", [
        ("Sources checked 29 August 2026 · see method", "Sources checked 24 September 2026 · see method"),
        ('<div class="fact"><b>6 things</b><span>Some worth doing, some worth planning around. No need to turn your holiday into a shared calendar.</span></div><div class="fact"><b>12-13 Sept</b><span>Ironman in Nice: excellent if you are racing. Less charming if you planned to drive across the Promenade.</span></div><div class="fact"><b>Updated</b><span>29 August 2026. Yes, this page is supposed to change. That is rather the point.</span></div>',
         '<div class="fact"><b>Now</b><span>Late September: Fondation Maeght remains an easy cultural win; Monaco is busier during the Yacht Show.</span></div><div class="fact"><b>23-26 Sept</b><span>Monaco Yacht Show: expect Port Hercule, hotels and transport around the harbour to be busier than usual.</span></div><div class="fact"><b>Updated</b><span>24 September 2026. This page changes because September does.</span></div>'),
        ("<h2>5 September, Festa de la Sant Bertoumiéu, Nice</h2>", "<h2>Past · 5 September, Festa de la Sant Bertoumiéu, Nice</h2>"),
        ("<h2>8-13 September, Cannes Yachting Festival</h2>", "<h2>Past · 8-13 September, Cannes Yachting Festival</h2>"),
        ('<h2 id="ironman">12-13 September, IRONMAN 70.3 World Championship, Nice</h2>', '<h2 id="ironman">Past · 12-13 September, IRONMAN 70.3 World Championship, Nice</h2>'),
        ('<h2>Our pick</h2><p>For a proper Riviera day: Fondation Maeght on a weekday, lunch in Saint-Paul-de-Vence, then back towards the sea. For a bit of local Nice: Sant Bertoumiéu. For the big events: Cannes if yachting genuinely interests you. Otherwise, you are under no obligation to collect entry wristbands. The Mediterranean is still there.</p>',
         '<h2>Our pick</h2><p>Right now: Fondation Maeght on a weekday, lunch in Saint-Paul-de-Vence, then back towards the sea. Monaco Yacht Show only if yachting is genuinely the point of the day; otherwise give Port Hercule a little breathing room until the event ends. The Mediterranean is still there.</p>'),
        ("Independent editorial selection. Checked 29 August 2026. This page is deliberately temporary: September will eventually become October.",
         "Independent editorial selection. Checked 24 September 2026. This page is deliberately temporary: September will eventually become October."),
    ])
    patch("bons-plans/septembre-2026/index.html", [
        ("Sources vérifiées le 29 août 2026 · voir la méthode", "Sources vérifiées le 24 septembre 2026 · voir la méthode"),
        ('<div class="fact"><b>6 repères</b><span>Des choses à faire, des choses à éviter, et aucune obligation de transformer vos vacances en agenda partagé.</span></div><div class="fact"><b>12-13 sept.</b><span>Ironman à Nice : très bien si vous courez. Beaucoup moins drôle si vous comptiez traverser la Promenade en voiture.</span></div><div class="fact"><b>Mis à jour</b><span>29 août 2026. Oui, cette page est censée changer. C’est précisément le principe.</span></div>',
         '<div class="fact"><b>Maintenant</b><span>Fin septembre : la Fondation Maeght reste une valeur sûre ; Monaco est plus chargé pendant le Yacht Show.</span></div><div class="fact"><b>23-26 sept.</b><span>Monaco Yacht Show : attendez-vous à davantage de monde autour de Port Hercule, dans les hôtels et les transports.</span></div><div class="fact"><b>Mis à jour</b><span>24 septembre 2026. Cette page change parce que septembre change.</span></div>'),
        ("<h2>5 septembre, Festa de la Sant Bertoumiéu, Nice</h2>", "<h2>Terminé · 5 septembre, Festa de la Sant Bertoumiéu, Nice</h2>"),
        ("<h2>8-13 septembre, Cannes Yachting Festival</h2>", "<h2>Terminé · 8-13 septembre, Cannes Yachting Festival</h2>"),
        ('<h2 id="ironman">12-13 septembre, Championnats du monde Ironman 70.3, Nice</h2>', '<h2 id="ironman">Terminé · 12-13 septembre, Championnats du monde Ironman 70.3, Nice</h2>'),
        ('<h2>Notre choix</h2><p>Pour une vraie journée Riviera : Fondation Maeght en semaine, déjeuner à Saint-Paul-de-Vence, puis retour vers la mer. Pour sentir Nice : Sant Bertoumiéu. Pour les grands événements : Cannes si le yachting vous intéresse. Pour le reste, ne vous sentez pas obligé de collectionner les bracelets d’entrée. La Méditerranée est toujours là.</p>',
         '<h2>Notre choix</h2><p>En ce moment : Fondation Maeght en semaine, déjeuner à Saint-Paul-de-Vence, puis retour vers la mer. Monaco Yacht Show uniquement si le yachting est vraiment le sujet de la journée ; sinon, laissez un peu respirer Port Hercule jusqu’à la fin de l’événement. La Méditerranée est toujours là.</p>'),
        ("Sélection éditoriale indépendante. Vérifié le 29 août 2026. Cette page est volontairement temporaire : septembre finira par devenir octobre.",
         "Sélection éditoriale indépendante. Vérifié le 24 septembre 2026. Cette page est volontairement temporaire : septembre finira par devenir octobre."),
    ])

def patch_cannes():
    patch("plages/cannes/index.html", [
        ('<div class="note"><strong>For the best swimming day from Cannes:</strong> consider the Lérins Islands. They are 15-20 minutes by boat and give you coves, clear water and a completely different rhythm from the Croisette.</div>',
         '<div class="note"><strong>Pour la meilleure journée baignade depuis Cannes :</strong> pensez aux îles de Lérins. Elles sont à 15-20 minutes en bateau et offrent criques, eau claire et un rythme très différent de la Croisette.</div>'),
        ('<p class="spot-logistics"><a href="/en/day-trips/iles-de-lerins/">Read our Lérins guide →</a></p>',
         '<p class="spot-logistics"><a href="/escapades/iles-de-lerins/">Voir notre guide des îles de Lérins →</a></p>'),
    ])

def patch_destination_duplicates():
    targets = [
        "en/riviera-guide/villefranche-cap-ferrat/index.html", "riviera-guide/villefranche-cap-ferrat/index.html",
        "en/riviera-guide/monaco/index.html", "riviera-guide/monaco/index.html",
        "en/riviera-guide/menton/index.html", "riviera-guide/menton/index.html",
    ]
    rx = re.compile(r'<section id="(?:what-not-to-miss|indispensables)" data-static-editorial="true">.*?</section>\s*', re.S)
    for rel in targets:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        text, n = rx.subn("", text, count=1)
        if n != 1:
            raise RuntimeError(f"{rel}: expected exactly one duplicate essentials block")
        if rel.startswith("en/"):
            text = text.replace("Practical details checked on 2 September 2026.", "Practical details checked on 23 September 2026.")
        else:
            text = text.replace("Détails pratiques vérifiés le 2 septembre 2026.", "Détails pratiques vérifiés le 23 septembre 2026.")
        save(rel, text, original)

def patch_daytrip_navigation():
    patch("en/day-trips/index.html", [
        ('href="/#plan">Plan</a>', 'href="/en/riviera-chooser/">Plan</a>'),
        ('href="/stay/nice/">Stay</a>', 'href="/en/hotels/">Stay</a>'),
        ('href="/en/restaurants/">Eat &amp; Do</a>', 'href="/en/explore/">Explore</a>'),
    ])
    patch("escapades/index.html", [
        ('href="/fr/#planifier">Planifier</a>', 'href="/riviera-chooser/">Planifier</a>'),
        ('href="/fr/dormir/nice/">Dormir</a>', 'href="/hotels/">Dormir</a>'),
        ('href="/restaurants/">Manger &amp; faire</a>', 'href="/explore/">Explorer</a>'),
    ])

def fix_expedia_labels():
    targets = [
        "hotels/antibes/index.html", "en/hotels/antibes/index.html",
        "hotels/villefranche-sur-mer/index.html", "en/hotels/villefranche-sur-mer/index.html",
        "hotels/beaulieu-sur-mer/index.html", "en/hotels/beaulieu-sur-mer/index.html",
    ]
    rx = re.compile(r'(<a\b[^>]*href="https?://(?:www\.)?expedia\.com/[^"]*"[^>]*>)(.*?)(</a>)', re.I | re.S)
    for rel in targets:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        text = rx.sub(lambda m: m.group(1) + m.group(2).replace("Booking.com", "Expedia") + m.group(3), text)
        save(rel, text, original)

def validate():
    errors = []
    en_home = (ROOT / "index.html").read_text(encoding="utf-8")
    fr_home = (ROOT / "fr/index.html").read_text(encoding="utf-8")
    if 'datetime="2026-09-08"' in en_home or "Cannes changes gear" in en_home: errors.append("EN homepage expired Cannes card")
    if 'datetime="2026-09-08"' in fr_home or "Cannes change de rythme" in fr_home: errors.append("FR homepage expired Cannes card")

    checks = {
        "en/good-finds/september-2026/index.html": ("Sources checked 24 September 2026", "Past · 5 September", "Past · 8-13 September", "Past · 12-13 September", "23-26 Sept"),
        "bons-plans/septembre-2026/index.html": ("Sources vérifiées le 24 septembre 2026", "Terminé · 5 septembre", "Terminé · 8-13 septembre", "Terminé · 12-13 septembre", "23-26 sept."),
        "plages/cannes/index.html": ("Pour la meilleure journée baignade depuis Cannes", "/escapades/iles-de-lerins/"),
    }
    for rel, needles in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text: errors.append(f"{rel}: missing {needle!r}")

    fr_cannes = (ROOT / "plages/cannes/index.html").read_text(encoding="utf-8")
    if "Read our Lérins guide" in fr_cannes or "/en/day-trips/iles-de-lerins/" in fr_cannes:
        errors.append("FR Cannes beach page still contains EN Lérins content")

    dests = [
        "en/riviera-guide/villefranche-cap-ferrat/index.html", "riviera-guide/villefranche-cap-ferrat/index.html",
        "en/riviera-guide/monaco/index.html", "riviera-guide/monaco/index.html",
        "en/riviera-guide/menton/index.html", "riviera-guide/menton/index.html",
    ]
    for rel in dests:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if 'id="what-not-to-miss"' in text or 'id="indispensables"' in text:
            errors.append(f"{rel}: duplicate essentials block remains")
        if rel.startswith("en/") and "Practical details checked on 23 September 2026." not in text:
            errors.append(f"{rel}: EN footer date mismatch")
        if not rel.startswith("en/") and "Détails pratiques vérifiés le 23 septembre 2026." not in text:
            errors.append(f"{rel}: FR footer date mismatch")

    expedia_anchor = re.compile(r'<a\b[^>]*href="https?://(?:www\.)?expedia\.com/[^"]*"[^>]*>(.*?)</a>', re.I | re.S)
    hotel_targets = [
        "hotels/antibes/index.html", "en/hotels/antibes/index.html",
        "hotels/villefranche-sur-mer/index.html", "en/hotels/villefranche-sur-mer/index.html",
        "hotels/beaulieu-sur-mer/index.html", "en/hotels/beaulieu-sur-mer/index.html",
    ]
    for rel in hotel_targets:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if any("Booking.com" in m.group(1) for m in expedia_anchor.finditer(text)):
            errors.append(f"{rel}: Expedia link still labeled Booking.com")

    for rel, needles in {
        "en/day-trips/index.html": ("/en/riviera-chooser/", "/en/hotels/", "/en/explore/"),
        "escapades/index.html": ("/riviera-chooser/", "/hotels/", "/explore/"),
    }.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text: errors.append(f"{rel}: missing canonical navigation {needle}")

    if errors:
        raise SystemExit("V2 closure audit failed:\n- " + "\n- ".join(errors))

def main():
    remove_expired_home_card("index.html")
    remove_expired_home_card("fr/index.html", True)
    patch_september()
    patch_cannes()
    patch_destination_duplicates()
    patch_daytrip_navigation()
    fix_expedia_labels()
    validate()
    print(f"V2 closure audit fixes passed; patched {len(changed)} generated file(s).")
    for rel in sorted(changed): print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
