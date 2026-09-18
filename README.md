# Mametas — production notes

Mametas is the editorial decision guide for a first 3–7 day stay on the French Riviera.

## V1 product state — September 2026

The V1 architecture is considered frozen after the September 18 acquisition / QA pass. New work should favour visibility, indexation fixes, content quality, conversion and verified bug fixes rather than adding navigation layers or redesigning the site.

Core path: Home → trip length / base → destination → Stay / hotel finder → hotel → affiliate exit, with contextual branches to restaurants, beaches, culture and selected activities.

## URL / language policy

Current production URLs are intentionally mixed because the site evolved from an earlier structure:

- French pages are generally at the root, with some newer decision pages under `/fr/`.
- English pages are generally under `/en/`, with a small number of established English decision URLs outside that pattern.
- Existing production URLs must not be globally renamed merely to make the structure look cleaner.
- Canonicals and hreflang must describe the URLs that actually exist in production.
- Any future FR/EN URL normalisation is a migration project, not a cleanup: first define the complete old→new mapping, then ship server-side permanent redirects, self-referencing canonicals, reciprocal hreflang and sitemap changes together. Validate internal links and Search Console after release.
- Never delete or move an indexed URL without an explicit redirect destination.

This policy is deliberately conservative: preserving accumulated indexing and inbound signals matters more than cosmetic URL symmetry.

## Deployment safety

Production is deployed from branch `mametas-v3` through `.github/workflows/mametas-production.yml`. The workflow materialises editorial/hotel layers, runs targeted passes, validates the static site, deploys changed public files to OVH, re-syncs critical assets and checks the public homepage.

`python scripts/validate_mametas.py` is the blocking static validation. It checks, among other things, HTML language, one H1/title, production canonicals, internal file targets, JSON-LD validity, sitemap XML and the production sitemap declaration in robots.txt.

## Editorial rules

Mametas is not an exhaustive directory. Keep selections short and decision-led. Preserve the 5-day no-car plan as the main first-trip spine, clear Mametas verdict / catch / rule framing, transparent affiliate disclosures and no invented live prices, availability or first-hand experience.

Hotel `€ / €€ / €€€ / €€€€` labels, when used, are relative positioning only; they are not live nightly rates.

## Historical note

The repository originated as Les Niçoises and contains old version notes. They are historical artefacts, not current production guidance. The active public brand and canonical domain are Mametas / `https://www.mametas.com/`.
