#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final late-stage Hotel Fit wording guard for Claude audit recipe.

Runs after all content/parity/layout generators so earlier scripts cannot
reintroduce the old dash wording or French "match" anglicism.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"assets/hotel-engine.js"

def main():
    s=P.read_text(encoding="utf-8",errors="ignore")
    old=s
    replacements={
      "Aucun match exact.":"Aucune correspondance exacte.",
      " - with the trade-offs made explicit.":", with the trade-offs made explicit.",
      " - with the trade-offs":", with the trade-offs",
      " — with the trade-offs made explicit.":", with the trade-offs made explicit.",
      " - avec les critères qu’il faut accepter de relâcher.":", avec les critères qu’il faut accepter de relâcher.",
      " — avec les critères qu’il faut accepter de relâcher.":", avec les critères qu’il faut accepter de relâcher.",
      " — clearly flagged as above budget.":", clearly flagged as above budget.",
      " - clearly flagged as above budget.":", clearly flagged as above budget.",
      " — clairement signalées comme au-dessus du budget.":", clairement signalées comme au-dessus du budget.",
      " - clairement signalées comme au-dessus du budget.":", clairement signalées comme au-dessus du budget.",
    }
    for a,b in replacements.items():
        s=s.replace(a,b)
    if s!=old:
        P.write_text(s,encoding="utf-8")
        print("patched late Hotel Fit wording")
    else:
        print("late Hotel Fit wording already clean")

    bad=("Aucun match exact."," - with the trade-offs"," — with the trade-offs",
         " — clearly flagged"," - clearly flagged",
         " - avec les critères"," — avec les critères")
    survive=[x for x in bad if x in s]
    if survive:
        raise RuntimeError("late Hotel Fit wording survives: "+repr(survive))
    for good in ("Aucune correspondance exacte.","invalidDetailPaths"):
        if good not in s:
            raise RuntimeError("required Hotel Fit token missing: "+good)
    print("Late Hotel Fit audit wording guard passed.")

if __name__=="__main__":
    main()
