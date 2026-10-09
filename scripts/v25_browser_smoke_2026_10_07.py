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
    ("/plan/", "editorial"),
    ("/fr/planifier/", "editorial"),
    ("/en/riviera-guide/", "editorial"),
    ("/riviera-guide/", "editorial"),
    ("/en/riviera-guide/nice/", "destination"),
    ("/riviera-guide/nice/", "destination"),
    ("/en/riviera-guide/villefranche-cap-ferrat/", "destination"),
    ("/riviera-guide/villefranche-cap-ferrat/", "destination"),
    ("/en/riviera-guide/antibes/", "destination"),
    ("/riviera-guide/antibes/", "destination"),
    ("/en/riviera-guide/cannes/", "destination"),
    ("/riviera-guide/cannes/", "destination"),
    ("/en/riviera-guide/monaco/", "destination"),
    ("/riviera-guide/monaco/", "destination"),
    ("/en/riviera-guide/menton/", "destination"),
    ("/riviera-guide/menton/", "destination"),
    ("/en/practical/", "editorial"),
    ("/pratique/", "editorial"),
    ("/en/explore/", "editorial"),
    ("/explore/", "editorial"),
    ("/en/good-finds/", "editorial"),
    ("/bons-plans/", "editorial"),
    ("/en/good-finds/what-to-book/", "booking"),
    ("/bons-plans/que-reserver/", "booking"),
    ("/en/riviera-chooser/", "tool"),
    ("/riviera-chooser/", "tool"),
    ("/en/riviera-chooser/?days=5&season=summer&mobility=nocar&mood=peace&pace=balanced&base=villefranche", "chooser-result"),
    ("/en/hotels/finder/", "tool"),
    ("/hotels/finder/", "tool"),
    ("/stay/nice/", "hotels"),
    ("/fr/dormir/nice/", "hotels"),
    ("/en/hotels/antibes/", "hotels"),
    ("/hotels/antibes/", "hotels"),
    ("/en/hotels/cannes/", "hotels"),
    ("/hotels/cannes/", "hotels"),
    ("/en/hotels/nice/le-negresco/", "editorial"),
    ("/hotels/nice/le-negresco/", "editorial"),
    ("/en/beaches/nice/", "editorial"),
    ("/plages/nice/", "editorial"),
    ("/en/gay-french-riviera/", "editorial"),
    ("/cote-dazur-gay/", "editorial"),
    ("/en/restaurants/", "editorial"),
    ("/en/restaurants/grasse/", "editorial"),
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
          const h1s = Array.from(document.querySelectorAll('h1')).filter(h => {
            const s = getComputedStyle(h);
            return s.display !== 'none' && s.visibility !== 'hidden';
          });
          const buttonSel = '.button,.btn,.rate-link,.affiliate-hotel-link,.cta-button,.hotel-card-actions .rate-link';
          const buttons = Array.from(document.querySelectorAll(buttonSel)).map(el => {
            const r = el.getBoundingClientRect();
            return {w:r.width,h:r.height,text:(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,60)};
          }).filter(x => x.w > 0 && x.h > 0);
          return {
            viewport: window.innerWidth,
            scrollWidth: root.scrollWidth,
            clientWidth: root.clientWidth,
            dupes,
            h1Count: h1s.length,
            h1Sizes: h1s.map(h => parseFloat(getComputedStyle(h).fontSize)),
            buttons,
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
              text:a.innerText.replace(/\\s+/g,' ').trim()
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


def check_mobile_menu(page, label: str) -> list[str]:
    errors: list[str] = []
    has_menu = page.evaluate(
        """() => !!document.querySelector('[data-v3-menu-open], [data-menu-open]')"""
    )
    if not has_menu:
        return errors

    page.evaluate("window.scrollTo(0, Math.min(520, Math.max(0, document.body.scrollHeight - innerHeight)))")
    page.wait_for_timeout(60)
    before = page.evaluate("window.scrollY")
    page.evaluate(
        """() => {
          const b = document.querySelector('[data-v3-menu-open], [data-menu-open]');
          if (b) b.click();
        }"""
    )
    page.wait_for_timeout(100)
    data = page.evaluate(
        """() => {
          const menu = document.querySelector('.mobile-menu.open, .mobile-nav.open');
          if (!menu) return {missing:true};
          const r = menu.getBoundingClientRect();
          const s = getComputedStyle(menu);
          const main = document.querySelector('main');
          return {
            missing:false,
            top:r.top, left:r.left, width:r.width, height:r.height,
            position:s.position, bg:s.backgroundColor,
            bodyFixed:getComputedStyle(document.body).position,
            bodyTop:document.body.style.top,
            mainVisibility:main ? getComputedStyle(main).visibility : '',
            viewportW:innerWidth, viewportH:innerHeight
          };
        }"""
    )
    if data.get("missing"):
        return [f"{label}: mobile menu did not open"]
    if data["position"] != "fixed":
        errors.append(f"{label}: mobile menu position is {data['position']}, expected fixed")
    if abs(data["top"]) > 2 or abs(data["left"]) > 2:
        errors.append(f"{label}: mobile menu does not start at viewport origin ({data['left']:.0f},{data['top']:.0f})")
    if data["width"] < data["viewportW"] - 2 or data["height"] < data["viewportH"] - 2:
        errors.append(
            f"{label}: mobile menu does not cover viewport ({data['width']:.0f}x{data['height']:.0f} vs {data['viewportW']}x{data['viewportH']})"
        )
    if data["bg"] in ("rgba(0, 0, 0, 0)", "transparent"):
        errors.append(f"{label}: mobile menu background is transparent")
    if data["bodyFixed"] != "fixed" or not data["bodyTop"].startswith("-"):
        errors.append(f"{label}: iPhone scroll lock is not active")
    if data["mainVisibility"] != "hidden":
        errors.append(f"{label}: page content remains visible behind open mobile menu")

    page.evaluate(
        """() => {
          const b = document.querySelector('[data-v3-menu-close], [data-menu-close]');
          if (b) b.click();
        }"""
    )
    page.wait_for_timeout(100)
    after = page.evaluate("window.scrollY")
    if abs(after - before) > 3:
        errors.append(f"{label}: closing mobile menu changed scroll position {before:.0f}->{after:.0f}")
    return errors


def check_editorial_mobile(page, label: str) -> list[str]:
    errors: list[str] = []
    data = page.evaluate(
        """() => {
          const bad = Array.from(document.querySelectorAll(
            'p a.btn[href*="/hotels/finder/"], p a.button[href*="/hotels/finder/"]'
          )).map(a => (a.innerText || '').trim());
          const cover = document.querySelector('.article-cover');
          if (!cover) return {bad, cover:null};
          const cr = cover.getBoundingClientRect();
          const img = cover.querySelector('img');
          const ir = img ? img.getBoundingClientRect() : null;
          const layout = document.querySelector('.article-cover + .v3-section .article-layout');
          const lr = layout ? layout.getBoundingClientRect() : null;
          return {
            bad,
            cover:{
              width:cr.width, height:cr.height,
              imageWidth:ir ? ir.width : 0, imageHeight:ir ? ir.height : 0,
              gap:lr ? lr.top - cr.bottom : null
            }
          };
        }"""
    )
    if data["bad"]:
        errors.append(f"{label}: Hotel Fit button still sits inside paragraph text: {data['bad'][:3]}")
    cover = data.get("cover")
    if cover and cover["width"] and cover["height"]:
        ratio = cover["width"] / cover["height"]
        if ratio < 1.65 or ratio > 1.90:
            errors.append(f"{label}: mobile article cover ratio is {ratio:.2f}, expected landscape ~16:9")
        if abs(cover["imageWidth"] - cover["width"]) > 2 or abs(cover["imageHeight"] - cover["height"]) > 2:
            errors.append(f"{label}: article cover image does not fill its frame")
        if cover["gap"] is not None and (cover["gap"] < 20 or cover["gap"] > 80):
            errors.append(f"{label}: article cover to content gap is {cover['gap']:.0f}px")
    return errors


def check_chooser_result(page, label: str) -> list[str]:
    errors: list[str] = []
    page.wait_for_timeout(350)
    data = page.evaluate(
        """() => Array.from(document.querySelectorAll('.chooser-hotel-card')).map(card => {
          const media=card.querySelector('.chooser-hotel-media');
          const img=media && media.querySelector('img');
          const r=media ? media.getBoundingClientRect() : null;
          return {
            name:card.getAttribute('data-hotel-name') || '',
            hasMedia:!!media,
            loaded:!!(img && img.complete && img.naturalWidth>0),
            w:r ? r.width : 0,
            h:r ? r.height : 0
          };
        })"""
    )
    if len(data) != 3:
        errors.append(f"{label}: Riviera Fit rendered {len(data)} hotel cards, expected 3")
    for item in data:
        if not item["hasMedia"] or not item["loaded"]:
            errors.append(f"{label}: Riviera Fit hotel '{item['name']}' has no loaded media")
        elif item["w"] and item["h"]:
            ratio=item["w"]/item["h"]
            if ratio < 1.45 or ratio > 1.58:
                errors.append(f"{label}: Riviera Fit hotel '{item['name']}' media ratio {ratio:.2f}, expected 3:2")
    return errors


def check_family_visuals(page, label: str, kind: str) -> list[str]:
    errors: list[str] = []
    data = page.evaluate(
        """() => {
          const visible = el => {
            const r = el.getBoundingClientRect();
            const s = getComputedStyle(el);
            return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
          };
          const fitLinks = Array.from(document.querySelectorAll(
            '.article-body a[href*="/hotels/finder/"], article.article a[href*="/hotels/finder/"]'
          )).filter(visible);
          const stayCards = Array.from(document.querySelectorAll('.itinerary-stay-prompt > a')).filter(visible).map(card => {
            const r = card.getBoundingClientRect();
            const span = card.querySelector('span');
            const strong = card.querySelector('strong');
            const sr = span ? span.getBoundingClientRect() : null;
            const tr = strong ? strong.getBoundingClientRect() : null;
            return {h:r.height, gap:(sr && tr) ? tr.top - sr.bottom : null};
          });
          const actionGroups = Array.from(document.querySelectorAll('.hotel-card-actions')).filter(visible).map(group => {
            const actions = Array.from(group.querySelectorAll('a,button')).filter(visible).map(a => {
              const r=a.getBoundingClientRect(); return {l:r.left,r:r.right,t:r.top,b:r.bottom,text:(a.innerText||'').trim()};
            });
            return actions;
          });
          const maps = Array.from(document.querySelectorAll('a[href*="google.com/maps"],a[href*="maps.app.goo.gl"]')).filter(visible).map(a => {
            const s=getComputedStyle(a);
            return {border:parseFloat(s.borderBottomWidth)||0, decoration:s.textDecorationLine, color:s.color};
          });
          const affiliateNotes = Array.from(document.querySelectorAll('.affiliate-note,.affiliate-disclosure,.affiliate-inline,.mametas-affiliate-disclosure')).filter(visible).map(n => {
            const s=getComputedStyle(n); return {marginTop:parseFloat(s.marginTop)||0};
          });
          const legacy = document.querySelector('body.rg-legacy-final article.article');
          const lr = legacy ? legacy.getBoundingClientRect() : null;
          const practical = document.querySelector('.rg-v3-final .ux-contained-practical');
          const ps = practical ? getComputedStyle(practical) : null;
          return {
            viewport:innerWidth,
            fitCount:fitLinks.length,
            stayCards,
            actionGroups,
            maps,
            affiliateNotes,
            legacy:lr ? {left:lr.left,right:lr.right,width:lr.width,viewport:innerWidth} : null,
            practical:ps ? {bg:ps.backgroundColor,borderLeft:parseFloat(ps.borderLeftWidth)||0} : null
          };
        }"""
    )

    if kind == "destination" and data["fitCount"] > 1:
        errors.append(f"{label}: {data['fitCount']} visible Hotel Fit links remain in destination article")

    cards = data["stayCards"]
    if cards:
        for i, card in enumerate(cards):
            if card["gap"] is not None and card["gap"] < 6:
                errors.append(f"{label}: Riviera Guide hotel card {i+1} label/title gap is only {card['gap']:.0f}px")
        # Equal-height matters only when cards share a desktop row. On mobile,
        # stacked cards should size naturally to their content.
        if data.get("viewport", 0) > 760:
            heights = [x["h"] for x in cards[:3]]
            if len(heights) > 1 and max(heights) - min(heights) > 4:
                errors.append(f"{label}: Riviera Guide hotel cards differ by {max(heights)-min(heights):.0f}px in height")

    for gi, group in enumerate(data["actionGroups"]):
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a,b = group[i],group[j]
                x=max(0,min(a["r"],b["r"])-max(a["l"],b["l"]))
                y=max(0,min(a["b"],b["b"])-max(a["t"],b["t"]))
                if x*y > 2:
                    errors.append(f"{label}: hotel action buttons overlap in group {gi+1}")

    for i, note in enumerate(data["affiliateNotes"]):
        if note["marginTop"] < 10:
            errors.append(f"{label}: affiliate disclosure {i+1} is too close to preceding action")

    for i, m in enumerate(data["maps"]):
        if m["border"] < 1 and "underline" not in m["decoration"]:
            errors.append(f"{label}: Google Maps link {i+1} has no consistent text affordance")

    legacy=data.get("legacy")
    if legacy:
        center=(legacy["left"]+legacy["right"])/2
        if abs(center-legacy["viewport"]/2) > 4:
            errors.append(f"{label}: legacy Riviera Guide article is not centred")

    practical=data.get("practical")
    if practical and (practical["bg"] in ("rgba(0, 0, 0, 0)","transparent") or practical["borderLeft"] < 3):
        errors.append(f"{label}: contained practical block has no visual treatment")

    return errors


def check_hotels(page, label: str) -> list[str]:
    errors: list[str] = []
    data = page.evaluate(
        """() => Array.from(document.querySelectorAll('.hotel-choice-card')).map((card, idx) => {
          const media = card.querySelector('.hotel-choice-media');
          const img = card.querySelector('.hotel-choice-media img');
          const thumb = card.querySelector('.hotel-choice-media .batch-thumb');
          const r = media ? media.getBoundingClientRect() : null;
          const ms = media ? getComputedStyle(media) : null;
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
            aspect: ms ? ms.aspectRatio : '',
            flex: ms ? ms.flex : '',
            heightStyle: ms ? ms.height : '',
            widthStyle: ms ? ms.width : '',
            position: ms ? ms.position : '',
            display: ms ? ms.display : '',
            actions
          };
        })"""
    )
    for d in data:
        if not d["hasVisual"] or d["naturalWidth"] == 0:
            errors.append(f"{label}: hotel card {d['idx']+1} has no loaded visual")
        if d["mediaW"] and d["mediaH"]:
            ratio = d["mediaW"] / d["mediaH"]
            if ratio < 1.22 or ratio > 1.45:
                errors.append(
                    f"{label}: hotel card {d['idx']+1} media ratio {ratio:.2f}, expected ~1.33 "
                    f"(computed aspect={d['aspect']}, flex={d['flex']}, size={d['widthStyle']}×{d['heightStyle']}, "
                    f"display={d['display']}, position={d['position']})"
                )
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
                    response = page.goto(base + path, wait_until="domcontentloaded", timeout=15000)
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
                    if metrics["h1Count"] != 1:
                        errors.append(f"{label}: visible H1 count is {metrics['h1Count']}, expected 1")
                    h1_limit = (96 if viewport_name == "mobile" else 120) if kind == "home" else (60 if viewport_name == "mobile" else 80)
                    if metrics["h1Sizes"] and max(metrics["h1Sizes"]) > h1_limit:
                        errors.append(
                            f"{label}: H1 is {max(metrics['h1Sizes']):.0f}px, above {h1_limit}px guardrail"
                        )
                    for b in metrics["buttons"]:
                        if b["h"] > 72:
                            errors.append(f"{label}: oversized button height {b['h']:.0f}px ({b['text']})")
                        if viewport_name == "desktop" and b["w"] > 460:
                            errors.append(f"{label}: oversized desktop button width {b['w']:.0f}px ({b['text']})")

                    broken = local_image_health(page)
                    if broken:
                        errors.append(f"{label}: broken local images {broken[:6]}")

                    if kind == "home":
                        errors.extend(check_home(page, label))
                    elif kind == "booking":
                        errors.extend(check_booking(page, label))
                    elif kind == "hotels":
                        errors.extend(check_hotels(page, label))
                    elif kind == "chooser-result":
                        errors.extend(check_chooser_result(page, label))

                    if viewport_name == "mobile":
                        errors.extend(check_mobile_menu(page, label))
                        if kind == "destination":
                            errors.extend(check_editorial_mobile(page, label))

                    errors.extend(check_family_visuals(page, label, kind))

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
