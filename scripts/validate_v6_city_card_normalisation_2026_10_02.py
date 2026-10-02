#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=['nice','villefranche-cap-ferrat','antibes','cannes','monaco','menton']
DETOUR=['eze','saint-paul-de-vence','saint-tropez']
ALL=BASE+DETOUR
errors=[]
for lang,rel in [('en','en/riviera-guide/index.html'),('fr','riviera-guide/index.html')]:
 s=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
 if s.count('/assets/mametas-city-card-v1.css?v=1.0')!=1: errors.append(f'{rel}: CSS')
 if s.count('class="mametas-city-card"')!=9: errors.append(f'{rel}: expected 9 city cards')
 for key in ALL:
  if s.count(f'data-city-card="{key}"')!=1: errors.append(f'{rel}: {key}')
 if 'class="place-card"' in s: errors.append(f'{rel}: legacy place-card remains')
for lang,rel in [('en','index.html'),('fr','fr/index.html')]:
 s=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
 if s.count('/assets/mametas-city-card-v1.css?v=1.0')!=1: errors.append(f'{rel}: CSS')
 if s.count('class="mametas-city-card"')!=9: errors.append(f'{rel}: expected 9 city cards')
 if s.count('data-home-city-detours="true"')!=1: errors.append(f'{rel}: detour section')
 for key in ALL:
  if s.count(f'data-city-card="{key}"')!=1: errors.append(f'{rel}: {key}')
 base_area=s[s.find('mametas-city-grid--bases'):s.find('home-section-tail')]
 detour_start=s.find('data-home-city-detours="true"')
 detour_end=s.find('</section>',detour_start)
 detour_area=s[detour_start:detour_end]
 for key in BASE:
  if f'data-city-card="{key}"' not in base_area: errors.append(f'{rel}: {key} not in bases')
 for key in DETOUR:
  if f'data-city-card="{key}"' not in detour_area: errors.append(f'{rel}: {key} not in detours')
 for key in ['monaco','menton']:
  if f'data-city-card="{key}"' in detour_area: errors.append(f'{rel}: {key} misclassified as detour')
 if lang=='fr':
  if 'Ne collectionnez pas la Riviera. Choisissez-la.' not in s: errors.append('FR missing parity section')
  if 'Meilleur premier point de chute' not in s: errors.append('FR point de chute vocabulary')
if errors:
 print('V6 city card validation failed:')
 for e in errors: print(' -',e)
 raise SystemExit(1)
print('V6 city card validation passed: 36 canonical card instances across home + Places')
