# Mametas coherence system — 2 October 2026

This document is the maintenance contract for the coherence cleanup started after the site-wide Claude audit. It is deliberately conservative: preserve the live product and editorial voice, remove historical template drift, and make future changes land through shared systems rather than one-off page patches.

## Principles

1. Do not apply audit findings blindly. Check the current source and the materialised build first. The audit is a map of suspected drift, not a command to overwrite newer work.
2. Editorial body copy stays page-owned. Shared passes may normalise navigation, labels, reusable facts and component structure, but must not rewrite H1s or editorial sections unless a separate content change is explicitly intended.
3. Late build passes are the convergence layer. Historical source generations may coexist temporarily; the final materialised HTML must converge before validation and deployment.
4. Every convergence pass has a blocking validator. A normalisation without a regression check is incomplete.
5. No URL renaming for cosmetic symmetry. Existing canonical routes are preserved unless there is a separate SEO/product reason and a redirect plan.
6. Preserve commercial integrity. Existing affiliate targets are not replaced merely for visual consistency. Booking reservation URLs must remain CJ-wrapped.
7. FR/EN are one product. Language links should target the exact equivalent page when one exists.

## Build order

The coherence layer runs after the historical V1–V5 materialisation/presentation scripts, so it can neutralise template drift introduced upstream without rewriting all old scripts.

Current order:
1. Historical content/materialisation passes
2. Presentation System / Riviera UI
3. V6 global shell
4. V6 destination system
5. Future component systems (hotels, city cards, CTA/source vocabulary)
6. Blocking coherence validators
7. Standard production validation
8. Deployment + live checks

## Canonical systems

### Global shell

Owned by:
- scripts/v6_coherence_envelope_2026_10_02.py
- scripts/validate_v6_coherence_envelope_2026_10_02.py
- assets/mametas-shell-v1.css

Invariant:
- one global header
- one mobile navigation
- one exact FR/EN selector
- one global footer
- no historical Now / Eat & Do / homepage-anchor navigation in the shell
- real editorial content accidentally placed before a legacy header must survive shell replacement

### Destination system

Canonical data: scripts/mametas_coherence_config.py
Materialisation: scripts/v6_destination_system_2026_10_02.py
Validation: scripts/validate_v6_destination_system_2026_10_02.py

Invariant:
- 6 bases: Nice, Villefranche & Cap-Ferrat, Antibes, Cannes, Monaco, Menton
- 3 detours: Èze, Saint-Paul-de-Vence, Saint-Tropez
- one canonical tag per destination
- Reality Check labels EN: Getting around / Budget / Season / Logistics
- Reality Check labels FR: Déplacements / Budget / Saison / Logistique
- destination editorial H1s remain free
- Èze keeps the village / Èze-sur-Mer distinction

## Next systems

Create these as shared late passes rather than page-by-page fixes:

1. Hotel detail envelope: canonical parent link and eyebrow; Area/Format/Best for/Budget labels; provider-specific but standard reservation CTA wording; preserve existing affiliate URL/provider; short Hotel Take pages may stay short.
2. City-card data: reuse destination names, groups and tags from scripts/mametas_coherence_config.py; presentation may vary by context (Home / Places / Stay / Restaurants); classification and core facts must not vary by context.
3. Vocabulary: closed CTA lexicon for Riviera Fit, Hotel Fit, booking, map and official source; one source/date format; one next-decision label; one agenda name; one French term for the trip base.
4. Family components: restaurant cards; beach cards; culture practical block; photo-credit format.

## Explicit non-goals

Do not standardise away:
- editorial H1 voice
- family-specific facts that serve different purposes
- tool submit labels (Give me the verdict, Show my shortlist)
- experience cards that are not city cards
- existing URL structure solely for visual symmetry

## Release discipline

For each phase:
1. branch from current mametas-v3
2. change the smallest shared layer possible
3. run a dedicated branch check where useful
4. inspect the PR diff
5. merge only after the previous production run has finished
6. verify build validator, deployment and representative live pages
7. only then start the next production merge

This sequencing is intentional: the cleanup is important, but preserving a working live site is more important than completing it quickly.
