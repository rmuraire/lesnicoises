#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
HUBS = [
    ("fr/dormir/nice/index.html",20),("stay/nice/index.html",20),
    ("hotels/antibes/index.html",11),("en/hotels/antibes/index.html",11),
    ("hotels/cannes/index.html",15),("en/hotels/cannes/index.html",15),
    ("hotels/villefranche-sur-mer/index.html",6),("en/hotels/villefranche-sur-mer/index.html",6),
    ("hotels/monaco/index.html",7),("en/hotels/monaco/index.html",7),
    ("hotels/menton/index.html",9),("en/hotels/menton/index.html",9),
    ("hotels/saint-paul-de-vence/index.html",8),("en/hotels/saint-paul-de-vence/index.html",8),
    ("hotels/beaulieu-sur-mer/index.html",6),("en/hotels/beaulieu-sur-mer/index.html",6),
    ("hotels/mougins/index.html",6),("en/hotels/mougins/index.html",6),
    ("hotels/saint-tropez/index.html",12),("en/hotels/saint-tropez/index.html",12),
]
def main() -> int:
    errors=[]; total=0; booking=0
    for rel, expected in HUBS:
        text=(ROOT/rel).read_text(encoding="utf-8")
        cards=re.findall(r'<article class="hotel-choice-card".*?</article>',text,flags=re.S)
        total += len(cards)
        if len(cards)!=expected: errors.append(f"{rel}: expected {expected} hotel cards, found {len(cards)}")
        if any('data-price-band=' not in c or 'hotel-price-band' not in c for c in cards):
            errors.append(f"{rel}: at least one hotel card is missing its relative price band")
        if "Liens Expedia affiliés signalés" in text or "Affiliate Expedia links clearly marked" in text:
            errors.append(f"{rel}: stale Expedia hub label")
        booking += text.count("Booking.com")
    for rel in ("hotels/finder/index.html","en/hotels/finder/index.html"):
        text=(ROOT/rel).read_text(encoding="utf-8")
        if 'data-engine-group="budget"' not in text: errors.append(f"{rel}: budget criterion missing")
        if "/assets/hotel-engine.js?v=10" not in text: errors.append(f"{rel}: Hotel Fit engine version not bumped")
        if not any(label in text for label in ("Cinq choix", "Cinq décisions", "Five choices", "Five decisions")): errors.append(f"{rel}: five-decision copy missing")
        if "Hotel Fit" not in text: errors.append(f"{rel}: Hotel Fit product naming missing")
    activity_links=sum((ROOT/rel).read_text(encoding="utf-8").count("partner_id=CEAKUVS") for rel in (
        "riviera-guide/nice/index.html","en/riviera-guide/nice/index.html","escapades/index.html","en/day-trips/index.html"))
    if activity_links < 10: errors.append(f"GetYourGuide: expected at least 10 FR/EN affiliate occurrences, found {activity_links}")
    stale=("encore trop chère","still expensive","encore trop forte sur le haut de gamme","still stronger at the expensive end")
    for rel in ("fr/planifier/cinq-jours-nice-sans-voiture/index.html","plan/five-days-nice-no-car/index.html","riviera-guide/nice-ou-cannes/index.html","en/riviera-guide/nice-or-cannes/index.html"):
        text=(ROOT/rel).read_text(encoding="utf-8").lower()
        for phrase in stale:
            if phrase in text: errors.append(f"{rel}: stale pre-consolidation copy remains: {phrase!r}")
    if booking < 20: errors.append(f"Booking.com: expected conversion copy across hotel hubs, found only {booking} mentions")
    if errors:
        print(f"V1 release validation failed with {len(errors)} issue(s):")
        for e in errors: print(f"- {e}")
        return 1
    print(f"V1 release validation passed: {total} FR/EN hotel-card instances carry price bands; budget finder, Booking/CJ and GetYourGuide layers present.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
