#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final presentation stabilization.

This is deliberately the last mutating pass. It protects the canonical visual
system from late legacy transformations and closes only presentation defects
that are obvious to a reader:
- restore the homepage four-step journey after global CTA normalisation;
- complete hotel choice cards when a Mametas detail page / affiliate rate exists;
- repair the known Solo Female Hotel 66 card media gap when that page is materialised;
- remove a small set of high-visibility opposition tics without flattening Mametas voice;
- run a focused presentation audit before release.
"""
from __future__ import annotations

from pathlib import Path
import html as htmlmod
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".github", "scripts", "docs", "backup",
        "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2"}

JOURNEY_EN = '<nav class="home-journey-spine" aria-label="How Mametas helps plan a French Riviera trip"><div class="wrap home-journey-inner"><span class="home-journey-label">YOUR TRIP, SIMPLIFIED</span><a href="/en/riviera-fit/"><b>01</b><strong>Choose the base</strong><small>Riviera Fit or browse Places</small></a><a href="/en/hotels/finder/"><b>02</b><strong>Choose the hotel</strong><small>Hotel Fit</small></a><a href="/en/explore/"><b>03</b><strong>Fill the days</strong><small>Beaches, culture, walks, tables</small></a><a href="/en/practical/"><b>04</b><strong>Make it work</strong><small>Transport, weather, bookings</small></a></div></nav>'
JOURNEY_FR = '<nav class="home-journey-spine" aria-label="Comment Mametas vous aide à préparer la Côte d’Azur"><div class="wrap home-journey-inner"><span class="home-journey-label">VOTRE SÉJOUR, SIMPLIFIÉ</span><a href="/riviera-fit/"><b>01</b><strong>Choisir la base</strong><small>Riviera Fit ou les destinations</small></a><a href="/hotels/finder/"><b>02</b><strong>Choisir l’hôtel</strong><small>Hotel Fit</small></a><a href="/explore/"><b>03</b><strong>Remplir les journées</strong><small>Plages, culture, balades, tables</small></a><a href="/pratique/"><b>04</b><strong>Faire fonctionner le séjour</strong><small>Transport, météo, réservations</small></a></div></nav>'

AFFILIATE_HOSTS = (
    "booking.com", "kqzyfj.com", "expedia.com/affiliates",
    "getyourguide.com", "gyg.me",
)

DESTINATION_TOOL_PAGES = tuple(
    f"{prefix}riviera-guide/{slug}/index.html"
    for prefix in ("", "en/")
    for slug in ("nice", "villefranche-cap-ferrat", "antibes", "cannes", "monaco", "menton")
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def write(rel: str, text: str, old: str) -> bool:
    if text == old:
        return False
    (ROOT / rel).write_text(text, encoding="utf-8")
    print("patched", rel)
    return True


def visible_text(s: str) -> str:
    s = re.sub(r"<(script|style)\b[^>]*>[\s\S]*?</\1>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", htmlmod.unescape(s)).strip()


def restore_home_journey(rel: str, nav: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8", errors="ignore")
    old = s
    pat = re.compile(r'<nav\b[^>]*class=["\'][^"\']*home-journey-spine[^"\']*["\'][\s\S]*?</nav>', re.I)
    if pat.search(s):
        s = pat.sub(nav, s, count=1)
    else:
        hero = re.search(r'<section\b[^>]*class=["\'][^"\']*home-hero[^"\']*["\'][\s\S]*?</section>', s, re.I)
        if hero:
            s = s[:hero.end()] + nav + s[hero.end():]
    write(rel, s, old)


def replace_many(rel: str, replacements: list[tuple[str, str]]) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8", errors="ignore")
    old = s
    for a, b in replacements:
        s = s.replace(a, b)
    write(rel, s, old)


def affiliate_from_detail(href: str) -> str | None:
    rel = href.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    if not rel.endswith("/"):
        rel += "/"
    p = ROOT / rel / "index.html"
    if not p.exists():
        return None
    s = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'<a\b(?P<attrs>[^>]*)href=["\'](?P<href>https?://[^"\']+)["\'](?P<rest>[^>]*)>', s, re.I):
        tag = (m.group("attrs") + " " + m.group("rest")).lower()
        url = m.group("href")
        low = url.lower()
        if any(host in low for host in AFFILIATE_HOSTS) and ("sponsored" in tag or "affiliate" in tag or "rate" in tag):
            return url
    # Some legacy detail pages have a valid affiliate URL but incomplete class/rel metadata.
    for m in re.finditer(r'href=["\'](?P<href>https?://[^"\']+)["\']', s, re.I):
        url = m.group("href")
        if any(host in url.lower() for host in AFFILIATE_HOSTS):
            return url
    return None


def neutralize_external_card_navigation(block: str) -> str:
    """Keep reservation partners behind the explicit rate CTA only."""
    media_patterns = (
        re.compile(
            r'<a(?P<pre>[^>]*)class=["\'](?P<class>[^"\']*hotel-choice-media[^"\']*)["\'](?P<mid>[^>]*)href=["\'](?P<href>https?://[^"\']+)["\'](?P<post>[^>]*)>(?P<body>[\s\S]*?)</a>',
            re.I,
        ),
        re.compile(
            r'<a(?P<pre>[^>]*)href=["\'](?P<href>https?://[^"\']+)["\'](?P<mid>[^>]*)class=["\'](?P<class>[^"\']*hotel-choice-media[^"\']*)["\'](?P<post>[^>]*)>(?P<body>[\s\S]*?)</a>',
            re.I,
        ),
    )

    def media_repl(m: re.Match[str]) -> str:
        href = m.group("href").lower()
        if not any(host in href for host in AFFILIATE_HOSTS):
            return m.group(0)
        return '<div class="hotel-choice-media">' + m.group("body") + '</div>'

    for pat in media_patterns:
        block = pat.sub(media_repl, block)

    h3_pat = re.compile(
        r'(<h3>\s*)<a\b[^>]*href=["\'](?P<href>https?://[^"\']+)["\'][^>]*>(?P<label>[\s\S]*?)</a>(\s*</h3>)',
        re.I,
    )

    def h3_repl(m: re.Match[str]) -> str:
        href = m.group("href").lower()
        if not any(host in href for host in AFFILIATE_HOSTS):
            return m.group(0)
        return m.group(1) + m.group("label") + m.group(4)

    return h3_pat.sub(h3_repl, block)


def patch_hotel_choice_cards(rel: str) -> None:
    p = ROOT / rel
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8", errors="ignore")
    old = s
    fr = bool(re.search(r'<html\b[^>]*\blang=["\']fr', s, re.I))
    pat = re.compile(r'<article\b(?P<attrs>[^>]*)class=["\'](?P<class>[^"\']*hotel-choice-card[^"\']*)["\'](?P<tail>[^>]*)>(?P<body>[\s\S]*?)</article>', re.I)

    def repl(m: re.Match[str]) -> str:
        block = neutralize_external_card_navigation(m.group(0))
        internal = re.search(r'href=["\'](?P<href>/(?:en/)?hotels/[^"\']+/[^"\']+/)["\']', block, re.I)
        detail = internal.group("href") if internal else None
        detail_exists = False
        if detail:
            detail_rel = detail.split("#", 1)[0].split("?", 1)[0].lstrip("/")
            detail_exists = (ROOT / detail_rel / "index.html").exists()
        has_primary = bool(re.search(r'btn--primary|Read our take|Lire notre avis', block, re.I))
        has_aff = bool(re.search(r'href=["\']https?://[^"\']*(?:booking\.com|kqzyfj\.com|expedia\.com/affiliates|getyourguide\.com|gyg\.me)', block, re.I))
        additions = ""
        if detail and detail_exists and not has_primary:
            label = "Lire notre avis" if fr else "Read our take"
            additions += f'<a class="btn btn--primary" href="{detail}">{label}</a>'
        if detail and not has_aff:
            aff = affiliate_from_detail(detail)
            if aff:
                label = "Voir les tarifs ↗" if fr else "Check rates ↗"
                additions += f'<a class="btn btn--affiliate" href="{aff}" target="_blank" rel="sponsored nofollow noopener">{label}</a>'
        if not additions:
            return block
        # hotel-choice-copy is the final div inside the article in this family.
        return re.sub(r'</div>\s*</article>\s*$', additions + '</div></article>', block, count=1, flags=re.I)

    s, n = pat.subn(repl, s)
    if write(rel, s, old):
        print("hotel choice cards normalised", rel, n)


def patch_all_hotel_choice_cards() -> None:
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "hotel-choice-card" in s:
            patch_hotel_choice_cards(rel.as_posix())


def patch_solo_hotel66_media() -> None:
    for rel in ("cote-dazur-femme-solo/index.html", "en/solo-female-french-riviera/index.html"):
        p = ROOT / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        old = s
        pat = re.compile(
            r'(<div class=["\']hotel-card["\']>)(\s*<div class=["\']hotel-card-body["\']>\s*<h3>Hotel 66</h3>)',
            re.I,
        )
        if pat.search(s):
            media = '<div class="hotel-card-media"><img src="/assets/hotels/hotel-66/hero.jpg" alt="Hotel 66 Nice" loading="lazy"></div>'
            s = pat.sub(r'\1' + media + r'\2', s, count=1)
        write(rel, s, old)


def _normalise_class_attr(attrs: str, add: tuple[str, ...] = (), remove: tuple[str, ...] = ()) -> str:
    m = re.search(r'\sclass=["\']([^"\']*)["\']', attrs, re.I)
    classes = m.group(1).split() if m else []
    classes = [x for x in classes if x not in set(remove)]
    for x in add:
        if x not in classes:
            classes.append(x)
    value = " ".join(classes)
    if m:
        return attrs[:m.start()] + (f' class="{value}"' if value else "") + attrs[m.end():]
    return attrs + (f' class="{value}"' if value else "")


def normalize_inline_tool_ctas() -> None:
    """A button must never be injected into running editorial copy.

    Earlier audit passes intentionally normalise Hotel Fit launch labels, but on
    destination pages that can turn an inline editorial link into a navy button
    in the middle of a sentence. Keep the link, demote it to editorial-link
    geometry, and mark the paragraph so the last CSS layer can place it cleanly.
    """
    para_pat = re.compile(r'<p(?P<attrs>[^>]*)>(?P<body>[\s\S]*?)</p>', re.I)
    anchor_pat = re.compile(r'<a\b(?P<attrs>[^>]*)>(?P<label>[\s\S]*?)</a>', re.I)

    for rel_name in DESTINATION_TOOL_PAGES:
        p = ROOT / rel_name
        if not p.exists():
            continue
        rel = p.relative_to(ROOT)
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "/hotels/finder/" not in s and "/en/hotels/finder/" not in s:
            continue
        old = s

        def para_repl(pm: re.Match[str]) -> str:
            attrs = pm.group("attrs")
            body = pm.group("body")
            touched = False

            def anchor_repl(am: re.Match[str]) -> str:
                nonlocal touched
                aattrs = am.group("attrs")
                href_m = re.search(r'\bhref=["\']([^"\']+)["\']', aattrs, re.I)
                if not href_m or not re.match(r'^/(?:en/)?hotels/finder/', href_m.group(1), re.I):
                    return am.group(0)
                cm = re.search(r'\sclass=["\']([^"\']*)["\']', aattrs, re.I)
                classes = set(cm.group(1).split()) if cm else set()
                paragraph_is_bridge = "destination-hotel-fit-cta" in attrs
                if not paragraph_is_bridge and not classes.intersection({"btn", "btn--primary", "button"}):
                    return am.group(0)
                touched = True
                aattrs = _normalise_class_attr(
                    aattrs,
                    add=("inline-decision-link", "editorial-tool-link"),
                    remove=("btn", "btn--primary", "button"),
                )
                return f'<a{aattrs}>{am.group("label")}</a>'

            new_body = anchor_pat.sub(anchor_repl, body)
            if not touched:
                return pm.group(0)
            new_attrs = _normalise_class_attr(attrs, add=("editorial-tool-bridge",))
            return f'<p{new_attrs}>{new_body}</p>'

        s = para_pat.sub(para_repl, s)

        # Keep one Hotel Fit bridge per destination article. Late audit passes can
        # inject the same tool launch more than once (after Stay, after comparisons,
        # or before sources), which is what made the CTA appear to wander.
        kept_bridge = False
        def dedupe_bridge(pm: re.Match[str]) -> str:
            nonlocal kept_bridge
            attrs = pm.group("attrs")
            body = pm.group("body")
            if not re.search(r'href=["\']/(?:en/)?hotels/finder/', body, re.I):
                return pm.group(0)
            if kept_bridge:
                return ""
            kept_bridge = True
            attrs = _normalise_class_attr(
                attrs,
                add=("destination-hotel-fit-bridge", "editorial-tool-bridge"),
                remove=("destination-hotel-fit-cta",),
            )
            def clean_anchor(am: re.Match[str]) -> str:
                aattrs = am.group("attrs")
                href_m = re.search(r'\bhref=["\']([^"\']+)["\']', aattrs, re.I)
                if not href_m or not re.match(r'^/(?:en/)?hotels/finder/', href_m.group(1), re.I):
                    return am.group(0)
                aattrs = _normalise_class_attr(
                    aattrs,
                    add=("inline-decision-link", "editorial-tool-link"),
                    remove=("btn", "btn--primary", "button"),
                )
                return f'<a{aattrs}>{am.group("label")}</a>'
            body = anchor_pat.sub(clean_anchor, body)
            return f'<p{attrs}>{body}</p>'

        s = para_pat.sub(dedupe_bridge, s)
        write(rel.as_posix(), s, old)


def targeted_copy_cleanup() -> None:
    replace_many("index.html", [
        ("Do not collect the Riviera. Choose it.", "Choose the Riviera that fits your trip."),
        ("Pick the detour that changes the mood, not the one that merely adds another pin.", "Pick the detour that genuinely changes the mood."),
        ("A useful guide should help you decide. It should not turn every day into homework.", "A useful guide should help you decide while leaving room to wander."),
        ("This is not the full shortlist. Our cards start with the use case and end with the catch.", "These examples show different trip logics. The full shortlist is in Stay, with the use case and the catch."),
    ])
    replace_many("fr/index.html", [
        ("Ne collectionnez pas la Riviera. Choisissez-la.", "Choisissez la Riviera qui correspond à votre séjour."),
        ("Choisissez le détour qui change l’ambiance, pas celui qui ajoute simplement une épingle.", "Choisissez le détour qui change réellement l’ambiance."),
        ("Un guide utile doit vous aider à décider. Il ne doit pas transformer chaque journée en devoir.", "Un guide utile doit vous aider à décider tout en laissant de la place à l’improvisation."),
        ("Ce n’est pas la sélection complète. Nos cartes commencent par l’usage et se terminent par le compromis.", "Ces exemples montrent plusieurs logiques de séjour. La sélection complète est dans Dormir, avec l’usage et le compromis."),
    ])
    replace_many("en/good-finds/what-to-book/index.html", [
        ("The Riviera rewards a little planning. Not a military operation. Reserve the things with limited capacity; leave the rest enough room to breathe.",
         "The Riviera rewards a little planning. A few well-chosen reservations are enough; leave the rest enough room to breathe."),
        ("This one is not theoretical.", "This rule is concrete."),
        ("Do not rebuild the trip around a ferry ticket that was never scarce.", "Keep the trip flexible around a ferry ticket that was never scarce."),
        ("For a flexible Nice afternoon, do not turn every museum into an appointment.", "For a flexible Nice afternoon, keep the museums flexible too."),
    ])
    replace_many("bons-plans/que-reserver/index.html", [
        ("La Riviera récompense un peu d’anticipation. Pas une opération militaire. Réservez ce qui a une capacité limitée ; laissez le reste respirer.",
         "La Riviera récompense un peu d’anticipation. Quelques réservations bien choisies suffisent ; laissez le reste respirer."),
        ("Ici, ce n’est pas théorique.", "Ici, la règle est concrète."),
        ("Ne reconstruisez pas le séjour autour d’un ferry qui n’était pas rare.", "Gardez le séjour flexible autour d’un ferry qui n’était pas rare."),
        ("Pour un après-midi improvisé à Nice, ne transformez pas chaque musée en rendez-vous.", "Pour un après-midi improvisé à Nice, gardez aussi les musées flexibles."),
    ])


def audit_cards() -> list[str]:
    problems: list[str] = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        rp = rel.as_posix()

        # Hotel choice cards have a clean <article> boundary. A batch-thumb is
        # a genuine visual (background image sprite) and counts as media.
        for m in re.finditer(r'<article\b[^>]*class=["\'][^"\']*hotel-choice-card[^"\']*["\'][^>]*>([\s\S]*?)</article>', s, re.I):
            block = m.group(1)
            if "<img" not in block.lower() and "batch-thumb" not in block:
                problems.append(rp + " :: hotel-choice-card without visual")
                break
            # Only the explicit rate CTA may point directly to a reservation partner.
            if re.search(r'<(?:a)\b[^>]*class=["\'][^"\']*hotel-choice-media[^"\']*["\'][^>]*href=["\']https?://', block, re.I):
                problems.append(rp + " :: hotel-choice media links directly to reservation partner")
                break
            if re.search(r'<h3>\s*<a\b[^>]*href=["\']https?://', block, re.I):
                problems.append(rp + " :: hotel-choice title links directly to reservation partner")
                break

        # Legacy hotel cards: match the exact class token. "hotel-card-body" is
        # not another card and must never create a false media failure.
        starts = []
        for sm in re.finditer(r'<div\b(?P<attrs>[^>]*)>', s, re.I):
            cm = re.search(r'\bclass=["\']([^"\']*)["\']', sm.group("attrs"), re.I)
            if cm and "hotel-card" in cm.group(1).split():
                starts.append(sm.start())
        for i, start in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else min(len(s), start + 3500)
            block = s[start:end]
            if "hotel-card-body" in block and "<img" not in block.lower() and "batch-thumb" not in block:
                problems.append(rp + " :: hotel-card without visual")
                break
    return problems


def audit_presentation() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    for rel, label, nav in (
        ("index.html", "YOUR TRIP, SIMPLIFIED", JOURNEY_EN),
        ("fr/index.html", "VOTRE SÉJOUR, SIMPLIFIÉ", JOURNEY_FR),
    ):
        s = read(rel)
        if s.count("home-journey-spine") != 1:
            errors.append(f"{rel}: expected one homepage journey spine")
        if label not in s:
            errors.append(f"{rel}: journey label missing")
        m = re.search(r'<nav\b[^>]*home-journey-spine[\s\S]*?</nav>', s, re.I)
        if m and re.search(r'class=["\'][^"\']*\bbtn\b', m.group(0), re.I):
            errors.append(f"{rel}: journey links still inherit CTA button classes")
        if m and ("Try Riviera Fit</" in m.group(0) or "Try Hotel Fit</" in m.group(0) or "Tester Riviera Fit</" in m.group(0) or "Tester Hotel Fit</" in m.group(0)):
            errors.append(f"{rel}: journey step labels were replaced by CTA labels")

    for rel in ("en/good-finds/what-to-book/index.html", "bons-plans/que-reserver/index.html"):
        p = ROOT / rel
        if not p.exists():
            errors.append(rel + ": booking guide missing")
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "practical-guide-page" not in s:
            errors.append(rel + ": practical guide page scope missing")
        if not any(src in s for src in (
            "/assets/editorial/iles-de-lerins-bruno-attuyt.webp",
            "/assets/editorial/iles-lerins.jpg",
        )):
            errors.append(rel + ": Lérins local visual missing")

    errors.extend(audit_cards())

    # Editorial copy must never contain a Hotel Fit button inside a paragraph.
    for rel_name in DESTINATION_TOOL_PAGES:
        p = ROOT / rel_name
        if not p.exists():
            continue
        rel = p.relative_to(ROOT)
        s = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(
            r'<p\b[^>]*>[\s\S]*?<a\b[^>]*class=["\'][^"\']*\b(?:btn|button)\b[^"\']*["\'][^>]*href=["\']/(?:en/)?hotels/finder/',
            s,
            re.I,
        ):
            errors.append(rel.as_posix() + ": Hotel Fit button still injected inside destination paragraph")

    # Key-page local image integrity.
    key_pages = [
        "index.html", "fr/index.html",
        "en/good-finds/what-to-book/index.html", "bons-plans/que-reserver/index.html",
        "stay/nice/index.html", "fr/dormir/nice/index.html",
        "en/riviera-fit/index.html", "riviera-fit/index.html",
        "en/hotels/finder/index.html", "hotels/finder/index.html",
    ]
    for rel in key_pages:
        p = ROOT / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        for src in re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', s, re.I):
            if src.startswith("/assets/"):
                fp = ROOT / src.lstrip("/")
                if not fp.exists():
                    errors.append(f"{rel}: missing local image {src}")

        ids = re.findall(r'\bid=["\']([^"\']+)["\']', s, re.I)
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        if dupes:
            errors.append(f"{rel}: duplicate ids {dupes[:8]}")

    # Editorial tell diagnostic: never rewrite blindly here; surface only high-visibility fragments.
    for rel in key_pages:
        p = ROOT / rel
        if not p.exists():
            continue
        # Hotel Fit legitimately repeats "Pas de préférence" as filter labels;
        # those are UI choices, not opposition-style editorial fragments.
        if rel.endswith("hotels/finder/index.html"):
            continue
        txt = visible_text(p.read_text(encoding="utf-8", errors="ignore"))
        fragments = len(re.findall(r'(?:(?:^|[.!?]\s+)(?:Not|Pas)\s+\w+)', txt))
        if fragments > 2:
            warnings.append(f"{rel}: {fragments} opposition fragments remain for editorial review")

    print("V24 FINAL PRESENTATION AUDIT")
    for w in warnings:
        print("WARN:", w)
    if errors:
        for e in errors:
            print("FAIL:", e)
        raise SystemExit(f"{len(errors)} presentation failure(s)")
    print("PASS: canonical journey, booking guide, hotel-card and key-page integrity checks passed.")


def repair_nested_antibes_hub() -> None:
    """Recover only corrupted Antibes hotel grids, preserving the current page shell.

    Earlier passes can produce nested hotel-choice-card markup. Restoring the
    entire committed file here would also remove the modern global header,
    mobile navigation, and the final stylesheet installed by v23.
    """
    import subprocess

    marker = '<section class="hotel-style-section" id="pratique-central">'
    for rel in ("hotels/antibes/index.html", "en/hotels/antibes/index.html"):
        p = ROOT / rel
        if not p.exists():
            continue
        current = p.read_text(encoding="utf-8", errors="ignore")
        if current.count('<article class="hotel-choice-card"') == current.count("</article>"):
            continue
        original = subprocess.check_output(
            ["git", "show", "HEAD:" + rel], cwd=str(ROOT), text=True
        )
        first = current.find(marker)
        first_original = original.find(marker)
        last = current.find("</main>", first)
        last_original = original.find("</main>", first_original)
        if min(first, first_original, last, last_original) < 0:
            raise RuntimeError(rel + ": cannot locate original Antibes hotel section boundaries")
        restored = original[first_original:last_original]
        if restored.count('<article class="hotel-choice-card"') != restored.count("</article>"):
            raise RuntimeError(rel + ": original hotel cards are unbalanced")
        # Retain the page head, foundation stylesheet, global shell, and
        # every correction outside the three hotel-card sections.
        repaired = current[:first] + restored + current[last:]
        if repaired.count('<article class="hotel-choice-card"') != repaired.count("</article>"):
            raise RuntimeError(rel + ": hotel cards are still unbalanced")
        p.write_text(repaired, encoding="utf-8")
        print("Restored Antibes card sections only; retained global shell:", rel, flush=True)


def main() -> None:
    repair_nested_antibes_hub()
    restore_home_journey("index.html", JOURNEY_EN)
    restore_home_journey("fr/index.html", JOURNEY_FR)
    patch_solo_hotel66_media()
    patch_all_hotel_choice_cards()
    normalize_inline_tool_ctas()
    targeted_copy_cleanup()
    audit_presentation()


if __name__ == "__main__":
    main()
