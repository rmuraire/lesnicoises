#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EN = '''<section class="v3-section" id="plan"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">First decision</p><h2>How many days do you actually have?</h2></div><p>This is now question one of the Mametas Riviera Chooser. Give us four answers and we will choose the base, the outings worth keeping and the part you can skip. <a href="/plan/five-days-nice-no-car/">Already know you want five days in Nice without a car? The full plan is still here.</a></p></div><div class="decision-grid"><a class="decision-card" href="/en/riviera-chooser/?days=3"><span class="decision-number">03 days</span><h3>Be ruthless</h3><p>Three days means one base and very few heroic transfers. We will decide what survives.</p><span class="text-link">Start the Chooser →</span></a><a class="decision-card" href="/en/riviera-chooser/?days=5"><span class="decision-number">05 days</span><h3>The useful middle</h3><p>Enough time for contrast, not enough time for every famous postcode. Excellent.</p><span class="text-link">Start the Chooser →</span></a><a class="decision-card" href="/en/riviera-chooser/?days=7"><span class="decision-number">07+ days</span><h3>More room, not more chaos</h3><p>A longer stay lets the right base breathe. It does not require a luggage relay race.</p><span class="text-link">Start the Chooser →</span></a></div><p style="margin-top:18px;color:var(--ink-soft);font-size:11px;line-height:1.6">Duration narrows the map first. Mobility comes next. Budget does not: that belongs to the hotel and restaurant decision after geography is settled.</p></div></section>'''

FR = '''<section class="v3-section" id="planifier"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">Première décision</p><h2>Combien de jours avez-vous vraiment ?</h2></div><p>C’est désormais la première question du Riviera Chooser Mametas. Donnez-nous quatre réponses : on choisit la base, les sorties qui valent le coup et ce que vous pouvez laisser tomber. <a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Vous savez déjà que vous voulez cinq jours à Nice sans voiture ? Le parcours complet est toujours là.</a></p></div><div class="decision-grid"><a class="decision-card" href="/riviera-chooser/?days=3"><span class="decision-number">03 jours</span><h3>Soyez impitoyable</h3><p>Trois jours, c’est une base et très peu de transferts héroïques. On décide de ce qui survit.</p><span class="text-link">Lancer le Chooser →</span></a><a class="decision-card" href="/riviera-chooser/?days=5"><span class="decision-number">05 jours</span><h3>Le bon milieu</h3><p>Assez de temps pour le contraste, pas assez pour chaque code postal célèbre. Parfait.</p><span class="text-link">Lancer le Chooser →</span></a><a class="decision-card" href="/riviera-chooser/?days=7"><span class="decision-number">07+ jours</span><h3>Plus d’air, pas plus de chaos</h3><p>Un séjour plus long laisse la bonne base respirer. Il n’impose pas un relais de valises.</p><span class="text-link">Lancer le Chooser →</span></a></div><p style="margin-top:18px;color:var(--ink-soft);font-size:11px;line-height:1.6">La durée réduit d’abord la carte. La mobilité vient ensuite. Pas le budget : lui descend dans le choix de l’hôtel et des restaurants une fois la géographie décidée.</p></div></section>'''

def patch(rel: str, section_id: str, replacement: str, old_hero: str, new_hero: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf'<section class="v3-section" id="{re.escape(section_id)}">.*?</section>\s*(?=<section class="v3-section" id="bases">)',
        re.S,
    )
    text, count = pattern.subn(replacement + "\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"{rel}: could not replace Chooser homepage entry")
    text = text.replace(old_hero, new_hero)
    path.write_text(text, encoding="utf-8")
    print(f"Riviera Chooser homepage entry applied: {rel}")

def main() -> int:
    patch(
        "index.html",
        "plan",
        EN,
        '<a class="button" href="/plan/five-days-nice-no-car/">Start with the 5-day plan</a>',
        '<a class="button" href="/en/riviera-chooser/">Start the Riviera Chooser</a>',
    )
    patch(
        "fr/index.html",
        "planifier",
        FR,
        '<a class="button" href="/fr/planifier/cinq-jours-nice-sans-voiture/">Commencer par le parcours 5 jours</a>',
        '<a class="button" href="/riviera-chooser/">Lancer le Riviera Chooser</a>',
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
