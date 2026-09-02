#!/usr/bin/env python3
"""Run production-safety checks against the active Mametas static site."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
OLD_TRACES = ("lesnicoises.com", "Les Niçoises", "LES NIÇOISES", "RIVIERA INSIDERS")


def active_html() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part.startswith("lesnicoises-v8") for part in path.relative_to(ROOT).parts)
    )


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.canonicals: list[str] = []
        self.titles = 0
        self.h1s = 0
        self.html_lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang") or ""
        elif tag == "title":
            self.titles += 1
        elif tag == "h1":
            self.h1s += 1
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href") or "")

        for attribute in ("href", "src", "poster"):
            value = values.get(attribute)
            if value:
                self.links.append((attribute, value))
        if values.get("srcset"):
            for candidate in values["srcset"].split(","):
                self.links.append(("srcset", candidate.strip().split()[0]))


def internal_target(value: str) -> Path | None:
    if not value.startswith("/") or value.startswith("//"):
        return None
    clean = unquote(urlsplit(value).path)
    if clean == "/":
        return ROOT / "index.html"
    target = ROOT / clean.lstrip("/")
    if clean.endswith("/"):
        target /= "index.html"
    return target


def main() -> int:
    errors: list[str] = []
    pages = active_html()
    canonical_urls: dict[str, Path] = {}

    for path in pages:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        parser = PageParser()
        try:
            parser.feed(text)
        except Exception as exc:  # pragma: no cover - defensive audit path
            errors.append(f"{relative}: HTML parser error: {exc}")
            continue

        for trace in OLD_TRACES:
            if trace in text:
                errors.append(f"{relative}: old-brand trace {trace!r}")
        if not parser.html_lang:
            errors.append(f"{relative}: missing html lang")
        if parser.titles != 1:
            errors.append(f"{relative}: expected one title, found {parser.titles}")
        if relative.as_posix() != "404.html" and parser.h1s != 1:
            errors.append(f"{relative}: expected one h1, found {parser.h1s}")
        if relative.as_posix() != "404.html":
            if len(parser.canonicals) != 1:
                errors.append(f"{relative}: expected one canonical, found {len(parser.canonicals)}")
            elif not parser.canonicals[0].startswith("https://www.mametas.com/"):
                errors.append(f"{relative}: non-production canonical {parser.canonicals[0]}")
            elif relative.as_posix() == "en/index.html":
                pass
            elif parser.canonicals[0] in canonical_urls:
                errors.append(
                    f"{relative}: duplicate canonical also used by {canonical_urls[parser.canonicals[0]].relative_to(ROOT)}"
                )
            else:
                canonical_urls[parser.canonicals[0]] = path

        if "/assets/consent.js" not in text:
            errors.append(f"{relative}: missing consent controller")
        if "googletagmanager.com/gtag/js" in text:
            errors.append(f"{relative}: eager Analytics loading")
        if relative.as_posix() == "en/index.html" and "noindex,follow" not in text:
            errors.append("en/index.html: former homepage must remain noindex before its production redirect")

        for attribute, value in parser.links:
            target = internal_target(value)
            if target is not None and not target.exists():
                errors.append(f"{relative}: missing {attribute} target {value}")

        for match in re.finditer(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text,
            flags=re.DOTALL | re.IGNORECASE,
        ):
            try:
                json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"{relative}: invalid JSON-LD: {exc}")

    try:
        ET.parse(ROOT / "sitemap.xml")
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml: invalid XML: {exc}")

    if "https://www.mametas.com/sitemap.xml" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
        errors.append("robots.txt: wrong sitemap URL")

    if errors:
        print(f"Mametas validation failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Mametas validation passed: {len(pages)} HTML pages, "
        f"{len(canonical_urls)} unique canonicals, sitemap XML valid, internal targets present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
