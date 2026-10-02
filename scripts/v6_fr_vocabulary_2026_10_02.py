#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPL={
 'Une ville à Nice, pas de voiture par défaut':'Nice comme point de chute, pas de voiture par défaut',
 'Une ville à Nice, plusieurs ambiances':'Nice comme point de chute, plusieurs ambiances',
 'Une ville à Nice, puis la Riviera':'Nice comme point de chute, puis la Riviera',
 'APRÈS LA VILLE · CHOISIR L’HÔTEL':'APRÈS LE POINT DE CHUTE · CHOISIR L’HÔTEL',
 'La ville est décidée ? Maintenant seulement, choisissez l’hôtel.':'Le point de chute est décidé ? Maintenant seulement, choisissez l’hôtel.',
 'Une fois la ville choisie, Hotel Fit':'Une fois le point de chute choisi, Hotel Fit',
 'Antibes comme base sur la Côte d’Azur':'Antibes comme point de chute sur la Côte d’Azur',
 'Nice comme base : ville, plages':'Nice comme point de chute : ville, plages',
 '<a href="#base">Comme ville</a>':'<a href="#base">Comme point de chute</a>',
 '<a href="#villefranche">Villefranche comme ville</a>':'<a href="#villefranche">Villefranche comme point de chute</a>',
 '<h2 id="villefranche">Villefranche comme ville</h2>':'<h2 id="villefranche">Villefranche comme point de chute</h2>',
 '<h2 id="base">Antibes comme ville</h2>':'<h2 id="base">Antibes comme point de chute</h2>',
 '<h2 id="base">Menton comme ville</h2>':'<h2 id="base">Menton comme point de chute</h2>',
}
TARGETS=[
 'fr/index.html','riviera-guide/index.html','hotels/index.html','cote-dazur-gay/index.html',
 'cote-dazur-gay/itineraire-5-jours/index.html','fr/planifier/trois-jours-cote-d-azur/index.html',
 'fr/planifier/sept-jours-cote-d-azur/index.html','riviera-guide/villefranche-cap-ferrat/index.html',
 'riviera-guide/antibes/index.html','riviera-guide/menton/index.html',
]

def main():
 changed=[]
 for rel in TARGETS:
  p=ROOT/rel
  if not p.exists(): raise RuntimeError(f'missing {rel}')
  s=p.read_text(encoding='utf-8',errors='ignore'); before=s
  for old,new in REPL.items(): s=s.replace(old,new)
  if s!=before:
   p.write_text(s,encoding='utf-8'); changed.append(rel)
 print('V6 FR vocabulary normalized on',len(changed),'files')

if __name__=='__main__': main()
