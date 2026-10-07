#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Browser-level presentation smoke test for the Mametas release candidate.

Runs only in PR/coherence CI after all mutating passes. It serves the built
workspace locally and renders representative pages at 390px and 1440px using
the system Chromium through Playwright.

The goal is not pixel-perfect snapshot testing. It catches the failures a
static gate cannot see: horizontal overflow, broken local images, overlapping
journey cells, CTA styling leaking into the homepage journey, malformed
what-to-book panels, and inconsistent hotel media geometry.
"""
from __future__ import annotations

from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import threading
import time

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    ("/", "home"),
    ("/fr/", "home"),
    ("/en/good-finds/what-to-book/", "booking"),
    ("/bons-plans/que-reserver/", "booking"),
    ("/en/riviera-fit/", "tool"),
    ("/riviera-fit/", "tool"),
    ("/en/hotels/finder/", "tool"),
    ("/hotels/finder/", "tool"),
    ("/stay/nice/", "hotels"),
    ("/fr/dormir/nice/", "hotels"),
    ("/en/hotels/antibes/", "hotels"),
    ("/hotels/antibes/", "hotels"),
    ("/en/gay-french-riviera/", "editorial"),
    ("/cote-dazur-gay/", "editorial"),
    ("/en/restaurants/", "editorial"),
    ("/en/culture/", "editorial"),
]

VIEWPORTS = [
    ("mobile", 390, 844),
    ("desktop", 1440, 1000),
]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return


@contextmanager
def local_server():
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def browser_executable() -> str:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("No system Chromium/Chrome executable found")


def local_image_health(page) -> list[str]:
    page.eval_on_selector_all(
        "img",
        """imgs => imgs.forEach(img => { img.loading = 'eager'; img.removeAttribute('loading'); })""",
    )
    # Trigger lazy regions without changing the final viewport.
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(180)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(120)
    return page.evaluate(
        """() => Array.from(document.images)
          .filter(img => {
            const u = new URL(img.currentSrc || img.src, location.href);
            return u.origin === location.origin && img.complete && img.naturalWidth === 0;
          })
          .map(img => img.getAttribute('src') || img.currentSrc)"""
    )


def common_metrics(page) -> dict:
    return page.evaluate(
        """() => {
          const root = document.documentElement;
          const ids = Array.from(document.querySelectorAll('[id]')).map(n => n.id).filter(Boolean);
          const dupes = [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))];
          return {
            viewport: window.innerWidth,
            scrollWidth: root.scrollWidth,
            clientWidth: root.clientWidth,
            dupes,
          };
        }"""
    )


def check_home(page, label: str) -> list[str]:
    errors: list[str] = []
    data = page.evaluate(
        """() => {
          const nav = document.querySelector('.home-journey-spine');
          if (!nav) return {missing:true};
          const links = Array.from(nav.querySelectorAll('.home-journey-inner > a'));
          const rects = links.map(a => {
            const r = a.getBoundingClientRect();
            const s = getComputedStyle(a);
            return {
              left:r.left, right:r.right, top:r.top, bottom:r.bottom,
              width:r.width, height:r.height,
              display:s.display, background:s.backgroundColor,
              textTransform:s.textTransform, cls:a.className,
              text:a.innerText.replace(/\s+/g,' ').trim()
            };
          });
          return {missing:false, count:links.length, rects};
        }"""
    )
    if data.get("missing"):
        return [f"{label}: homepage journey missing"]
    if data["count"] != 4:
        errors.append(f"{label}: homepage journey has {data['count']} links, expected 4")

    rects = data["rects"]
    for i, r in enumerate(rects):
        if "btn" in str(r["cls"]).split():
            errors.append(f"{label}: journey link {i+1} still has .btn")
        if r["display"] != "grid":
            errors.append(f"{label}: journey link {i+1} display is {r['display']}, expected grid")
        if r["textTransform"] not in ("none", ""):
            errors.append(f"{label}: journey link {i+1} text-transform leaked ({r['textTransform']})")
        if r["background"] in ("rgb(20, 33, 61)", "rgb(22, 34, 61)", "rgb(18, 33, 61)"):
            errors.append(f"{label}: journey link {i+1} is still a navy CTA block")
        if r["width"] <= 0 or r["height"] <= 0:
            errors.append(f"{label}: journey link {i+1} has zero geometry")

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            x = max(0, min(a["right"], b["right"]) - max(a["left"], b["left"]))
            y = max(0, min(a["bottom"], b["bottom"]) - max(a["top"], b["top"]))
            if x * y > 2:
                errors.append(f"{label}: journey links {i+1} and {j+1} overlap")
    return errors


def check_booking(page, label: str) -> list[str]:
    errors: list[str] = []
    data = page.evaluate(
        """() => {
          const cards = Array.from(document.querySelectorAll('.practical-guide-page .article > .place'));
          return cards.map(el => {
            const s = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return {
              paddingLeft: parseFloat(s.paddingLeft),
              paddingRight: parseFloat(s.paddingRight),
              borderTop: parseFloat(s.borderTopWidth),
              bg: s.backgroundColor,
              width: r.width,
              right: r.right,
            };
          });
        }"""
    )
    if len(data) < 3:
        errors.append(f"{label}: only {len(data)} booking panels found")
        return errors
    for i, d in enumerate(data):
        if d["paddingLeft"] < 15 or d["paddingRight"] < 15:
            errors.append(f"{label}: booking panel {i+1} padding too small")
        if d["borderTop"] < 1:
            errors.append(f"{label}: booking panel {i+1} has no visible border")
        if d["bg"] in ("rgba(0, 0, 0, 0)", "transparent"):
            errors.append(f"{label}: booking panel {i+1} has transparent background")
    return errors


def check_hotels(page, label: str) -> list[str]:
    errors: list[str] = []
    data = page.evaluate(
        """() => Array.from(document.querySelectorAll('.hotel-choice-card')).map((card, idx) => {
          const media = card.querySelector('.hotel-choice-media');
          const img = card.querySelector('.hotel-choice-media img');
          const thumb = card.querySelector('.hotel-choice-media .batch-thumb');
          const r = media ? media.getBoundingClientRect() : null;
          const actions = Array.from(card.querySelectorAll('.btn, .rate-link')).map(a => {
            const ar = a.getBoundingClientRect();
            return {w:ar.width, h:ar.height, text:a.innerText.trim()};
          });
          return {
            idx,
            hasVisual: !!(img || thumb),
            naturalWidth: img ? img.naturalWidth : (thumb ? 1 : 0),
            mediaW: r ? r.width : 0,
            mediaH: r ? r.height : 0,
            actions
          };
        })"""
    )
    for d in data:
        if not d["hasVisual"] or d["naturalWidth"] == 0:
            errors.append(f"{label}: hotel card {d['idx']+1} has no loaded visual")
        if d["mediaW"] and d["mediaH"]:
            ratio = d["mediaW"] / d["mediaH"]
            if ratio < 1.35 or ratio > 1.65:
                errors.append(f"{label}: hotel card {d['idx']+1} media ratio {ratio:.2f}, expected ~1.50")
        for a in d["actions"]:
            if a["h"] < 40:
                errors.append(f"{label}: hotel CTA '{a['text'][:28]}' is only {a['h']:.0f}px high")
    return errors


def main() -> None:
    exe = browser_executable()
    errors: list[str] = []
    print("V25 BROWSER SMOKE")
    print("browser:", exe)

    with local_server() as base, sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            executable_path=exe,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        try:
            for viewport_name, width, height in VIEWPORTS:
                context = browser.new_context(viewport={"width": width, "height": height})
                page = context.new_page()

                def route_handler(route):
                    if route.request.url.startswith(base):
                        route.continue_()
                    else:
                        route.abort()

                page.route("**/*", route_handler)

                for path, kind in PAGES:
                    label = f"{viewport_name} {path}"
                    response = page.goto(base + path.lstrip("/"), wait_until="domcontentloaded", timeout=15000)
                    if response is None or response.status >= 400:
                        errors.append(f"{label}: HTTP {response.status if response else 'no response'}")
                        continue
                    page.wait_for_timeout(120)

                    metrics = common_metrics(page)
                    if metrics["scrollWidth"] > width + 2:
                        errors.append(
                            f"{label}: horizontal overflow {metrics['scrollWidth']}px > {width}px"
                        )
                    if metrics["dupes"]:
                        errors.append(f"{label}: duplicate ids {metrics['dupes'][:6]}")

                    broken = local_image_health(page)
                    if broken:
                        errors.append(f"{label}: broken local images {broken[:6]}")

                    if kind == "home":
                        errors.extend(check_home(page, label))
                    elif kind == "booking":
                        errors.extend(check_booking(page, label))
                    elif kind == "hotels":
                        errors.extend(check_hotels(page, label))

                    print(
                        f"OK geometry {label}: scroll={metrics['scrollWidth']} "
                        f"viewport={width} broken={len(broken)}"
                    )
                context.close()
        finally:
            browser.close()

    if errors:
        print("BROWSER SMOKE FAILURES")
        for e in errors:
            print("FAIL:", e)
        raise SystemExit(f"{len(errors)} browser presentation failure(s)")

    print("PASS: representative pages render cleanly at 390px and 1440px.")


if __name__ == "__main__":
    main()
