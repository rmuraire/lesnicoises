#!/usr/bin/env python3
"""Keep generated decision-support blocks inside the V3 editorial column.

The legacy materializer appends its static decision sections immediately before
</article> on destination pages without a .sources block. On V3 pages that puts
the content outside .wrap.article-layout / .article-body and makes it render flush
against the viewport. This post-pass moves only that generated block back inside
the article body.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = (
    "riviera-guide/menton/index.html",
    "riviera-guide/monaco/index.html",
    "riviera-guide/villefranche-cap-ferrat/index.html",
    "riviera-guide/antibes/index.html",
    "en/riviera-guide/menton/index.html",
    "en/riviera-guide/monaco/index.html",
    "en/riviera-guide/villefranche-cap-ferrat/index.html",
    "en/riviera-guide/antibes/index.html",
)

START = "<!-- MAMETAS_STATIC_DECISIONS_START -->"
END = "<!-- MAMETAS_STATIC_DECISIONS_END -->"
V3_CLOSE = "</div></div></section>"


def fix_page(rel: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")

    start = text.find(START)
    end = text.find(END, start)
    if start < 0 or end < 0:
        raise RuntimeError(f"Generated decision block not found in {rel}")
    end += len(END)

    block = text[start:end]
    text = text[:start] + text[end:]

    article_end = text.rfind("</article>")
    if article_end < 0:
        raise RuntimeError(f"Article closing tag not found in {rel}")

    insert_at = text.rfind(V3_CLOSE, 0, article_end)
    if insert_at < 0:
        raise RuntimeError(f"V3 article column closing tags not found in {rel}")

    text = text[:insert_at] + "\n" + block + "\n" + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print(f"Aligned generated Places content: {rel}")


def main() -> None:
    for rel in PAGES:
        fix_page(rel)
    print("Places layout hotfix complete.")


if __name__ == "__main__":
    main()
