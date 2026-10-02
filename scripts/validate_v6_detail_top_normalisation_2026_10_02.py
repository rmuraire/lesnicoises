#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('norm',ROOT/'scripts/v6_detail_top_normalisation_2026_10_02.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
errors=[]
for rel,(href,label,eyebrow) in mod.PAGES.items():
 s=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
 if s.count(f'<a class="back" href="{href}">{label}</a>')!=1: errors.append(f'{rel}: back')
 if s.count(f'<p class="eyebrow">{eyebrow}</p>')!=1: errors.append(f'{rel}: eyebrow')
 if 'class="breadcrumbs"' in s: errors.append(f'{rel}: breadcrumb remains')
 if rel in mod.HOTEL_TAKES:
  if 'MAMETAS HOTEL TAKE' in s: errors.append(f'{rel}: old hotel eyebrow')
  if rel.startswith('en/') and '>Check dates<' in s: errors.append(f'{rel}: old booking CTA')
  if not rel.startswith('en/') and '>Voir les dates<' in s: errors.append(f'{rel}: old booking CTA')
for rel in ['en/beaches/nice/index.html','en/day-trips/nice-to-menton-by-train/index.html']:
 s=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
 for bad in ['Nice : the beaches','train : the day trip','Option 1 :']:
  if bad in s: errors.append(f'{rel}: EN colon spacing {bad}')
if errors:
 print('V6 detail-top validation failed:')
 for e in errors: print(' -',e)
 raise SystemExit(1)
print('V6 detail-top validation passed on',len(mod.PAGES),'mapped pages')
