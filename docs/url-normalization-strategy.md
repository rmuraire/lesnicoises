# Mametas FR/EN URL normalization strategy

Status: documented during the 13 September 2026 audit remediation. No global URL migration is part of this patch.

## Why the current split is being preserved

Mametas currently mixes legacy French root paths (for example `/restaurants/`, `/riviera-guide/`, `/hotels/`) with newer `/fr/` paths, while English content uses both root English experiences and `/en/` sections. Rewriting those URLs in one pass would create avoidable SEO and navigation risk unless redirects, canonicals, hreflang pairs, sitemaps and internal links move together.

## Preconditions for a future normalization

1. Inventory every indexable FR/EN URL and its traffic/backlink value.
2. Choose one permanent URL policy for French and English.
3. Produce a one-to-one old → new redirect map. Use permanent redirects; do not rely on JavaScript or navigation-only redirects.
4. Update canonical URLs on every destination page to the final URL.
5. Make hreflang reciprocal for every real FR/EN pair and keep an intentional x-default.
6. Update all internal navigation, contextual links, XML sitemaps, structured data and social metadata in the same release.
7. Preserve pages that do not have a genuine translation rather than inventing a language pair.
8. Validate redirect chains, loops, orphan pages and 404s before deployment, then monitor crawl/indexing after release.

## Rule until that project exists

Do not globally rewrite FR/EN paths. New or materially rebuilt bilingual pages should use explicit reciprocal canonical/hreflang metadata and should link to existing stable URLs. Local navigation fixes are allowed when they remove dead-ends without changing the public URL contract.
