#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EN = '''<section class="v3-section chooser-signature-section" id="plan"><div class="wrap chooser-signature"><div class="chooser-signature-lockup"><span class="chooser-signature-kicker">MAMETAS</span><h2><span>Riviera</span><span>Chooser</span></h2><p class="chooser-signature-tagline">4 questions. One verdict.</p></div><div class="chooser-signature-copy"><p class="eyebrow">THE DECISION TOOL</p><h3>Tell us about your trip. We’ll make the call.</h3><p>Duration, mobility, what you want most, pace. Mametas chooses one base, the outings worth keeping and what you can leave for another trip. Hotel and restaurant budgets come later.</p><a class="button chooser-signature-primary" href="/en/riviera-chooser/">Start the Riviera Chooser</a><div class="chooser-signature-shortcuts"><span>Know your duration?</span><a href="/en/riviera-chooser/?days=3">3 days</a><a href="/en/riviera-chooser/?days=5">5 days</a><a href="/en/riviera-chooser/?days=7">7+ days</a></div><p class="chooser-signature-plan">Already know you want five days in Nice without a car? <a href="/plan/five-days-nice-no-car/">Open the full plan →</a></p></div></div></section>'''

FR = '''<section class="v3-section chooser-signature-section" id="planifier"><div class="wrap chooser-signature"><div class="chooser-signature-lockup"><span class="chooser-signature-kicker">MAMETAS</span><h2><span>Riviera</span><span>Chooser</span></h2><p class="chooser-signature-tagline">4 questions. Un verdict.</p></div><div class="chooser-signature-copy"><p class="eyebrow">L’OUTIL DE DÉCISION</p><h3>Parlez-nous de votre séjour. On tranche pour vous.</h3><p>Durée, mobilité, ce que vous voulez vraiment, rythme. Mametas choisit une seule base, les sorties à garder et ce que vous pouvez laisser pour une autre fois. Le budget hôtel et restaurants vient après.</p><a class="button chooser-signature-primary" href="/riviera-chooser/">Lancer le Riviera Chooser</a><div class="chooser-signature-shortcuts"><span>Vous connaissez déjà la durée ?</span><a href="/riviera-chooser/?days=3">3 jours</a><a href="/riviera-chooser/?days=5">5 jours</a><a href="/riviera-chooser/?days=7">7+ jours</a></div><p class="chooser-signature-plan">Vous savez déjà que vous voulez cinq jours à Nice sans voiture ? <a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Ouvrir le parcours complet →</a></p></div></div></section>'''

def patch(rel: str, section_id: str, replacement: str, old_hero: str, new_hero: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf'<section class="v3-section(?: chooser-signature-section)?" id="{re.escape(section_id)}">.*?</section>\s*(?=<section class="v3-section" id="bases">)',
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
        '<a class="button" href="/fr/planifier/cinq-jours-nice-sans-voiture/">Commencer par les 5 jours</a>',
        '<a class="button" href="/riviera-chooser/">Lancer le Riviera Chooser</a>',
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
