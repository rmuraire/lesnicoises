#!/usr/bin/env python3
"""Open external Mametas links in a new tab while preserving internal navigation.

Adds target="_blank" and rel="noopener" to external HTTP(S) anchors.
Existing rel tokens such as sponsored/nofollow are preserved. Mametas links,
relative links, anchors, mailto and tel links remain in the same tab.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_TOP_LEVEL = {
    ".git",
    ".github",
    "docs",
    "scripts",
    "data",
    "lesnicoises-v8-no-mercy-update",
    "lesnicoises-v8-no-mercy-update 2",
}
ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.IGNORECASE)
HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)
TARGET_RE = re.compile(r"\btarget\s*=\s*([\"']).*?\1", re.IGNORECASE | re.DOTALL)
REL_RE = re.compile(r"\brel\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)


def is_external(href: str) -> bool:
    try:
        parsed = urlsplit(href)
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname.lower().rstrip(".")
    return host != "mametas.com" and not host.endswith(".mametas.com")


def rewrite_anchor(match: re.Match[str]) -> str:
    tag = match.group(0)
    href_match = HREF_RE.search(tag)
    if not href_match or not is_external(href_match.group(2)):
        return tag

    if TARGET_RE.search(tag):
        tag = TARGET_RE.sub('target="_blank"', tag, count=1)
    else:
        tag = tag[:-1] + ' target="_blank">'

    rel_match = REL_RE.search(tag)
    if rel_match:
        tokens = rel_match.group(2).split()
        if "noopener" not in {token.lower() for token in tokens}:
            tokens.append("noopener")
        replacement = 'rel="' + " ".join(tokens) + '"'
        tag = tag[: rel_match.start()] + replacement + tag[rel_match.end() :]
    else:
        tag = tag[:-1] + ' rel="noopener">'
    return tag


def active_html_files():
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP_LEVEL:
            continue
        yield path


def main() -> int:
    changed = []
    anchor_count = 0
    for path in active_html_files():
        text = path.read_text(encoding="utf-8")
        rewritten, count = ANCHOR_RE.subn(rewrite_anchor, text)
        if rewritten != text:
            path.write_text(rewritten, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
            anchor_count += count
    print(f"External-link pass updated {len(changed)} HTML file(s).")
    print(f"Scanned {anchor_count} anchor start tags on changed files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
