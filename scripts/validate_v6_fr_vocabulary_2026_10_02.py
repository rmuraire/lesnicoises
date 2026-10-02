#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks={
 'fr/index.html':['APRÈS LA VILLE · CHOISIR L’HÔTEL','Une fois la ville choisie'],
 'riviera-guide/index.html':['Une ville à Nice, plusieurs ambiances'],
 'hotels/index.html':['APRÈS LA VILLE · CHOISIR L’HÔTEL','La ville est décidée ?'],
 'cote-dazur-gay/index.html':['Une ville à Nice, puis la Riviera'],
 'cote-dazur-gay/itineraire-5-jours/index.html':['Nice comme base : ville, plages'],
 'fr/planifier/trois-jours-cote-d-azur/index.html':['Une ville à Nice, pas de voiture par défaut'],
 'fr/planifier/sept-jours-cote-d-azur/index.html':['Une ville à Nice, pas de voiture par défaut'],
 'riviera-guide/villefranche-cap-ferrat/index.html':['Villefranche comme ville'],
 'riviera-guide/antibes/index.html':['Antibes comme base sur la Côte d’Azur','Antibes comme ville','>Comme ville<'],
 'riviera-guide/menton/index.html':['Menton comme ville','>Comme ville<'],
}
errors=[]
for rel,bad in checks.items():
 s=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
 for token in bad:
  if token in s: errors.append(f'{rel}: {token!r}')
if 'point de chute' not in (ROOT/'fr/index.html').read_text(encoding='utf-8'): errors.append('FR home: point de chute absent')
if errors:
 print('V6 FR vocabulary validation failed:')
 for e in errors: print(' -',e)
 raise SystemExit(1)
print('V6 FR vocabulary validation passed')
