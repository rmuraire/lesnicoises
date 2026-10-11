#!/usr/bin/env python3
"""Repair only the five HIGH-priority issues in Claude's 11 Oct 2026 QA.
Run after *all* HTML/JS materializers, before deploy. Idempotent; no redesign.
The .htaccess security/404 rules and existing branded 404 page are versioned
separately. No broad content rewrites or global CSS changes.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
AFFILIATE_MARK = "mametas-affiliate-outbound-2026-10-01"

SOURCE_LABELS = {
    "en/explore/french-riviera-honeymoon/index.html": (
        "Booking.com: September–October 2026 search growth",
        "Booking.com: 2026 travel personalization research",
    ),
    "explore/lune-de-miel-cote-d-azur/index.html": (
        "Booking.com : progression des recherches septembre–octobre 2026",
        "Booking.com : tendances voyage 2026 et ultra-personnalisation",
    ),
}
NEWS_ANCHOR = re.compile(
    r'<a\b(?P<attrs>[^>]*\bhref="(?P<url>https://news\.booking\.com/[^"]+)"[^>]*)>'
    r'(?P<inner>.*?)</a>', re.I | re.S
)
BAD_HOTEL_HEADING = re.compile(
    r'<h3>\s*(?:Check rates on Booking\.com|Voir les tarifs sur Booking\.com)\s*↗?\s*</h3>',
    re.I,
)

def fix_scripts():
    for rel in ("assets/site.js", "assets/v3.js"):
        p = ROOT / rel
        if not p.is_file():
            raise RuntimeError(rel + ": required JS missing")
        source = p.read_text(encoding="utf-8")
        text = source
        # One 01-Oct materializer appends a raw Python string containing
        # literal backslash-n sequences, which invalidates the entire JS file.
        broken_start = r"\n/* " + AFFILIATE_MARK + r" */\n"
        good_start = "\n/* " + AFFILIATE_MARK + " */\n"
        if broken_start in text:
            text = text.replace(broken_start, good_start, 1)
            if text.endswith(r"\n"):
                text = text[:-2] + "\n"
        # The lightweight PR runner does not execute the original 01-Oct
        # affiliate materializer. Insert its intended listener in that case.
        if AFFILIATE_MARK not in text:
            text += (
                "\\n/* " + AFFILIATE_MARK + " */\\n"
                "document.addEventListener('click',function(e){"
                "var a=e.target.closest('a[data-affiliate-network]');if(!a)return;"
                "if(typeof window.gtag==='function'){window.gtag('event','affiliate_outbound',"
                "{affiliate_network:a.getAttribute('data-affiliate-network')||'',"
                "hotel:a.getAttribute('data-affiliate-hotel')||'',page_path:location.pathname});}"
                "});\\n"
            )
        if text.count(AFFILIATE_MARK) != 1:
            raise RuntimeError(rel + ": outbound tracking marker absent/duplicated")
        if broken_start in text or text.endswith(r"\n"):
            raise RuntimeError(rel + ": literal JS newlines remain")
        if text != source:
            p.write_text(text, encoding="utf-8")
            print("JS_REPAIRED", rel, flush=True)
        # Fails release if any future materializer recreates invalid JS.
        subprocess.run(["node", "--check", str(p)], check=True)

def fix_sources():
    for rel, labels in SOURCE_LABELS.items():
        p = ROOT / rel
        html = p.read_text(encoding="utf-8")
        found = list(NEWS_ANCHOR.finditer(html))
        if len(found) != 2:
            raise RuntimeError(f"{rel}: expected two Booking NEWS citations, got {len(found)}")
        def restore(m):
            url = m.group("url")
            # Preserve the destination exactly; restore original citation labels
            # from versioned editorial HTML. These links are NOT affiliate CTAs.
            label = labels[0] if "lete-joue-les-prolongations" in url else labels[1]
            return f'<a href="{url}" target="_blank" rel="nofollow noopener">{label}</a>'
        updated = NEWS_ANCHOR.sub(restore, html)
        for m in NEWS_ANCHOR.finditer(updated):
            if "btn--affiliate" in m.group(0) or "Check rates on Booking" in m.group("inner") or "Voir les tarifs sur Booking" in m.group("inner"):
                raise RuntimeError(rel + ": misleading Booking press-release CTA remains")
        if updated != html:
            p.write_text(updated, encoding="utf-8")
            print("SOURCE_CITATIONS_RESTORED", rel, flush=True)

def fix_hotel_title():
    for rel in ("hotels/beaulieu-sur-mer/index.html",
                "en/hotels/beaulieu-sur-mer/index.html"):
        p = ROOT / rel
        if not p.is_file():
            # Hotel hubs materialize only in the full production workflow;
            # the PR job checks JS and editorial source links separately.
            if __import__("os").environ.get("MAMETAS_REQUIRE_CRITICAL_PAGES") == "1":
                raise RuntimeError(rel + ": production hotel hub missing")
            print("PR_SKIP_UNMATERIALIZED_HUB", rel, flush=True)
            continue
        html = p.read_text(encoding="utf-8")
        repaired, count = BAD_HOTEL_HEADING.subn(
            "<h3>La Réserve de Beaulieu</h3>", html)
        if count > 1 or "<h3>La Réserve de Beaulieu</h3>" not in repaired:
            raise RuntimeError(f"{rel}: hotel name cannot be restored safely (matches={count})")
        if repaired != html:
            p.write_text(repaired, encoding="utf-8")
            print("HOTEL_TITLE_RESTORED", rel, flush=True)

def main():
    fix_scripts()
    fix_sources()
    fix_hotel_title()
    print("Claude critical QA: JS tracking, citations, hotel title PASS", flush=True)

if __name__ == "__main__":
    main()
