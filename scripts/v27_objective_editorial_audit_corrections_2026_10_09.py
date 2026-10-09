#!/usr/bin/env python3
"""Small verified factual/editorial corrections from Claude and Astra audits.

Runs after all materialization and text passes, before final production checks.
No HTML structure, layout, user testimonials, hotel pricing or links rewritten.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
CORRECTIONS={
 "en/good-finds/mipim-cannes/index.html":[
   ("CROISETTE · WEST", "CROISETTE · EAST"),
 ],
 "bons-plans/mipim-cannes/index.html":[
   ("CROISETTE · OUEST", "CROISETTE · EST"),
 ],
 "en/practical/index.html":[
   ("Carnival, MIPIM, Ironman. The Riviera has its own calendar. The Riviera runs on its own calendar.",
    "Carnival, MIPIM, Ironman. The Riviera has its own calendar."),
 ],
 "pratique/index.html":[
   ("Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier. La Riviera a son propre calendrier.",
    "Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier."),
 ],
 "en/gay-french-riviera/index.html":[
   ("Event dates change. Check the current Nice / LGBTQ+ agenda before booking around Pride.",
    "Nice’s Pink Parade took place on 11 July in 2026. For 2027, confirm the date with the official local LGBTQ+ organisers before booking travel around the event."),
   ('<div class="segment-hotel-price">Sea-view room shown from about €366</div>',""),
 ],
 "cote-dazur-gay/index.html":[
   ("Les dates peuvent bouger. Vérifiez l’agenda LGBTQIA+ officiel avant de réserver autour d’un événement.",
    "La Pink Parade de Nice a eu lieu le 11 juillet en 2026. Pour 2027, confirmez la date auprès des organisateurs LGBTQIA+ locaux avant de réserver un séjour autour de l’événement."),
 ],
}
def main():
    touched=0
    for rel,replacements in CORRECTIONS.items():
        path=ROOT/rel
        if not path.exists():
            print("CONTENT AUDIT SKIP not materialized:",rel,flush=True)
            continue
        s=path.read_text(encoding="utf-8")
        original=s
        for old,new in replacements:
            if old in s:
                s=s.replace(old,new)
                print("CONTENT AUDIT corrected:",rel,old[:65],flush=True)
            elif new not in s:
                raise RuntimeError(f"Content audit expected phrase missing: {rel}: {old[:65]}")
        for old,new in replacements:
            if old in s:
                raise RuntimeError(f"Content audit stale phrase survived: {rel}: {old[:65]}")
            if new and new not in s:
                raise RuntimeError(f"Content audit replacement missing: {rel}: {new[:65]}")
        if s!=original:
            path.write_text(s,encoding="utf-8")
            touched+=1
    print("CONTENT AUDIT targeted corrections:",touched,"pages changed",flush=True)
if __name__=="__main__":
    main()
