#!/usr/bin/env python3
"""One-time normalization of active Mametas HTML pages.

Repairs two legacy issues detected by the production validator:
1. stale /explorer/ internal links -> /explore/
2. pages missing the consent controller -> add the standard deferred script in <head>
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSENT = '<script defer src="/assets/consent.js?v=1.0"></script>'


def active_html():
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part.startswith("lesnicoises-v8") for part in path.relative_to(ROOT).parts)
    )


def main() -> int:
    changed = []
    for path in active_html():
        text = path.read_text(encoding="utf-8")
        original = text
        text = text.replace('href="/explorer/"', 'href="/explore/"')
        text = text.replace("href='/explorer/'", "href='/explore/'")
        if "/assets/consent.js" not in text:
            if "</head>" not in text:
                raise RuntimeError(f"{path.relative_to(ROOT)} has no </head> tag")
            text = text.replace("</head>", f"{CONSENT}\n</head>", 1)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    print(f"Repaired {len(changed)} active HTML file(s).")
    for item in changed:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
