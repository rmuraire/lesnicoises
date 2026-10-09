#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Global browser anomaly sweep for Mametas.

This is intentionally non-editorial. It renders every URL in sitemap.xml at a
phone and desktop viewport after the full build has materialised, and only
flags gross presentation failures: HTTP errors, horizontal overflow, duplicate
or missing visible H1s, implausibly large buttons, broken local images in the
initial viewport, malformed mobile article covers, and mobile menus that do
not behave as opaque fixed overlays.

It does not compare screenshots or enforce taste.
"""
from __future__ import annotations

from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import shutil
import threading
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
VIEWPORTS = [
    ("mobile", 390, 844),
    ("desktop", 1440, 1000),
]

BASE_DESTINATION_PATHS = {
    "/en/riviera-guide/nice/", "/riviera-guide/nice/",
    "/en/riviera-guide/villefranche-cap-ferrat/", "/riviera-guide/villefranche-cap-ferrat/",
    "/en/riviera-guide/antibes/", "/riviera-guide/antibes/",
    "/en/riviera-guide/cannes/", "/riviera-guide/cannes/",
    "/en/riviera-guide/monaco/", "/riviera-guide/monaco/",
    "/en/riviera-guide/menton/", "/riviera-guide/menton/",
}


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


def sitemap_paths() -> list[str]:
    root = ET.parse(SITEMAP).getroot()
    paths: list[str] = []
    seen: set[str] = set()
    for node in root.iter():
        if not node.tag.endswith("loc") or not node.text:
            continue
        parsed = urlparse(node.text.strip())
        path = parsed.path or "/"
        if not path.endswith("/") and "." not in Path(path).name:
            path += "/"
        if path not in seen:
            seen.add(path)
            paths.append(path)
    return paths


def check_common(page, label: str, width: int, mobile: bool) -> list[str]:
    data = page.evaluate(
        """() => {
          const root = document.documentElement;
          const visible = el => {
            const s = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
          };
          const h1s = Array.from(document.querySelectorAll('h1')).filter(visible);
          const ids = Array.from(document.querySelectorAll('[id]')).map(n => n.id).filter(Boolean);
          const dupes = [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))];
          const buttons = Array.from(document.querySelectorAll(
            '.button,.btn,.rate-link,.affiliate-hotel-link,.cta-button,.hotel-card-actions .rate-link'
          )).filter(visible).map(el => {
            const r = el.getBoundingClientRect();
            const s = getComputedStyle(el);
            return {
              w:r.width,h:r.height,
              fs:parseFloat(s.fontSize),
              text:(el.innerText||'').replace(/\s+/g,' ').trim().slice(0,80)
            };
          });
          const broken = Array.from(document.images).filter(img => {
            if (!img.complete || img.naturalWidth !== 0) return false;
            const u = new URL(img.currentSrc || img.src, location.href);
            return u.origin === location.origin;
          }).map(img => img.getAttribute('src') || img.currentSrc).slice(0,8);
          return {
            scrollWidth: root.scrollWidth,
            clientWidth: root.clientWidth,
            h1Count: h1s.length,
            h1Sizes: h1s.map(h => parseFloat(getComputedStyle(h).fontSize)),
            dupes, buttons, broken
          };
        }"""
    )
    errors: list[str] = []
    if data["scrollWidth"] > width + 4:
        errors.append(f"{label}: horizontal overflow {data['scrollWidth']}px > {width}px")
    if data["h1Count"] != 1:
        errors.append(f"{label}: visible H1 count {data['h1Count']}, expected 1")
    h1_limit = 100 if mobile else 124
    if data["h1Sizes"] and max(data["h1Sizes"]) > h1_limit:
        errors.append(f"{label}: H1 {max(data['h1Sizes']):.0f}px > {h1_limit}px")
    if data["dupes"]:
        errors.append(f"{label}: duplicate ids {data['dupes'][:6]}")
    for b in data["buttons"]:
        if b["h"] > 92:
            errors.append(f"{label}: oversized button {b['h']:.0f}px high ({b['text']})")
        if not mobile and b["w"] > 700:
            errors.append(f"{label}: oversized desktop button {b['w']:.0f}px wide ({b['text']})")
    if data["broken"]:
        errors.append(f"{label}: broken local images {data['broken']}")
    return errors


def check_mobile_cover(page, label: str) -> list[str]:
    data = page.evaluate(
        """() => {
          const cover = document.querySelector('.article-cover');
          if (!cover) return null;
          const img = cover.querySelector('img');
          const cr = cover.getBoundingClientRect();
          const ir = img ? img.getBoundingClientRect() : null;
          const next = cover.nextElementSibling;
          const nr = next ? next.getBoundingClientRect() : null;
          return {
            w:cr.width,h:cr.height,
            iw:ir ? ir.width : 0, ih:ir ? ir.height : 0,
            gap:nr ? nr.top - cr.bottom : null
          };
        }"""
    )
    if not data or not data["w"] or not data["h"]:
        return []
    errors: list[str] = []
    ratio = data["w"] / data["h"]
    if ratio < 1.55 or ratio > 2.0:
        errors.append(f"{label}: article cover ratio {ratio:.2f} is not landscape")
    if abs(data["iw"] - data["w"]) > 3 or abs(data["ih"] - data["h"]) > 3:
        errors.append(f"{label}: article cover image does not fill frame")
    if data["gap"] is not None and (data["gap"] < -2 or data["gap"] > 90):
        errors.append(f"{label}: article cover to next-section gap {data['gap']:.0f}px")
    return errors


def check_mobile_menu(page, label: str) -> list[str]:
    has = page.evaluate("() => !!document.querySelector('[data-v3-menu-open], [data-menu-open]')")
    if not has:
        return []
    page.evaluate("window.scrollTo(0, Math.min(420, Math.max(0, document.body.scrollHeight-innerHeight)))")
    page.wait_for_timeout(20)
    before = page.evaluate("window.scrollY")
    page.evaluate(
        """() => {
          const b=document.querySelector('[data-v3-menu-open], [data-menu-open]');
          if (b) b.click();
        }"""
    )
    page.wait_for_timeout(35)
    data = page.evaluate(
        """() => {
          const menu=document.querySelector('.mobile-menu.open, .mobile-nav.open');
          if (!menu) return {missing:true};
          const r=menu.getBoundingClientRect(), s=getComputedStyle(menu);
          const main=document.querySelector('main');
          return {
            missing:false, top:r.top,left:r.left,w:r.width,h:r.height,
            vw:innerWidth,vh:innerHeight,position:s.position,bg:s.backgroundColor,
            bodyPosition:getComputedStyle(document.body).position,
            bodyTop:document.body.style.top,
            mainVisibility:main ? getComputedStyle(main).visibility : ''
          };
        }"""
    )
    errors: list[str] = []
    if data.get("missing"):
        return [f"{label}: mobile menu did not open"]
    if data["position"] != "fixed":
        errors.append(f"{label}: mobile menu position {data['position']} is not fixed")
    if abs(data["top"]) > 2 or abs(data["left"]) > 2:
        errors.append(f"{label}: mobile menu origin {data['left']:.0f},{data['top']:.0f}")
    if data["w"] < data["vw"] - 2 or data["h"] < data["vh"] - 2:
        errors.append(f"{label}: mobile menu {data['w']:.0f}x{data['h']:.0f} does not cover {data['vw']}x{data['vh']}")
    if data["bg"] in ("transparent", "rgba(0, 0, 0, 0)"):
        errors.append(f"{label}: mobile menu background is transparent")
    if data["bodyPosition"] != "fixed" or not data["bodyTop"].startswith("-"):
        errors.append(f"{label}: mobile scroll lock inactive")
    if data["mainVisibility"] != "hidden":
        errors.append(f"{label}: page content remains visible behind menu")
    page.evaluate(
        """() => {
          const b=document.querySelector('[data-v3-menu-close], [data-menu-close]');
          if (b) b.click();
        }"""
    )
    page.wait_for_timeout(25)
    after = page.evaluate("window.scrollY")
    if abs(after-before) > 4:
        errors.append(f"{label}: menu close moved scroll {before:.0f}->{after:.0f}")
    return errors


def check_destination_tool_link(page, label: str, path: str) -> list[str]:
    if path not in BASE_DESTINATION_PATHS:
        return []
    bad = page.evaluate(
        """() => Array.from(document.querySelectorAll(
          'p a.btn[href*="/hotels/finder/"],p a.button[href*="/hotels/finder/"]'
        )).map(a => (a.innerText||'').replace(/\s+/g,' ').trim()).slice(0,5)"""
    )
    return [f"{label}: Hotel Fit button inside destination paragraph {bad}"] if bad else []


def check_family_consistency(page, label: str, path: str, mobile: bool) -> list[str]:
    data = page.evaluate(
        """() => {
          const visible = el => {
            const s=getComputedStyle(el), r=el.getBoundingClientRect();
            return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0;
          };

          const maps=Array.from(document.querySelectorAll(
            'a[href*="google.com/maps"],a[href*="maps.app.goo.gl"]'
          )).filter(visible).map(a=>{
            const s=getComputedStyle(a);
            return {
              border:parseFloat(s.borderBottomWidth)||0,
              bg:s.backgroundColor,
              display:s.display,
              classes:a.className||''
            };
          });

          const affiliateNotes=Array.from(document.querySelectorAll('p,div,small,span'))
            .filter(el => visible(el) && /^Affiliate links?:/i.test((el.innerText||'').trim()))
            .map(note=>{
              const nr=note.getBoundingClientRect();
              let prev=note.previousElementSibling;
              while(prev && !visible(prev)) prev=prev.previousElementSibling;
              if(!prev) return {gap:null};
              const pr=prev.getBoundingClientRect();
              return {gap:nr.top-pr.bottom};
            });

          const cards=Array.from(document.querySelectorAll(
            '.hotel-card,.hotel-choice-card,.itinerary-stay-prompt>a,.chooser-hotel-card'
          )).filter(visible).map(card=>{
            const r=card.getBoundingClientRect();
            const img=card.querySelector('img');
            const labelEl=card.querySelector('.kicker,.hotel-choice-tags,span');
            const title=card.querySelector('h3,h4,strong');
            const lr=labelEl ? labelEl.getBoundingClientRect() : null;
            const tr=title ? title.getBoundingClientRect() : null;
            const actions=Array.from(card.querySelectorAll(
              '.hotel-card-actions a,.hotel-card-actions button,.btn,.rate-link,.affiliate-hotel-link'
            )).filter(visible).map(a=>{
              const ar=a.getBoundingClientRect();
              return {l:ar.left,r:ar.right,t:ar.top,b:ar.bottom};
            });
            return {
              top:r.top,bottom:r.bottom,h:r.height,
              hasImg:!!img,
              imgLoaded:img ? (!img.complete && img.loading === 'lazy' ? null : (img.complete && img.naturalWidth>0)) : true,
              textGap:(lr&&tr)?tr.top-lr.bottom:null,
              actions
            };
          });

          const exploreCards=Array.from(document.querySelectorAll(
            '.intent-detail .hotel-card,.explore-page .hotel-card,.solo-female-page .hotel-card'
          )).filter(visible).map(card=>{
            const cr=card.getBoundingClientRect();
            const action=card.querySelector('.hotel-card-actions,.affiliate-hotel-link,.rate-link,.btn');
            const ar=action&&visible(action)?action.getBoundingClientRect():null;
            return {top:cr.top,bottom:cr.bottom,actionBottom:ar?ar.bottom:null};
          });

          const fitLinks=Array.from(document.querySelectorAll(
            '.article-body a[href*="/hotels/finder/"], article.article a[href*="/hotels/finder/"]'
          )).filter(visible);

          const legacy=document.querySelector('body.rg-legacy-final article.article');
          const legacyRect=legacy&&visible(legacy)?legacy.getBoundingClientRect():null;

          const practical=document.querySelector('.rg-v3-final .ux-contained-practical');
          const practicalStyle=practical&&visible(practical)?getComputedStyle(practical):null;

          return {
            maps,affiliateNotes,cards,exploreCards,
            fitCount:fitLinks.length,
            legacy:legacyRect?{left:legacyRect.left,right:legacyRect.right,vw:innerWidth}:null,
            practical:practicalStyle?{
              bg:practicalStyle.backgroundColor,
              borderLeft:parseFloat(practicalStyle.borderLeftWidth)||0
            }:null
          };
        }"""
    )
    errors: list[str] = []

    for i,m in enumerate(data["maps"]):
        if m["border"] < 1 or m["bg"] not in ("rgba(0, 0, 0, 0)","transparent"):
            errors.append(f"{label}: Google Maps link {i+1} does not use canonical inline-link styling")
        if "btn" in str(m["classes"]).split() or "button" in str(m["classes"]).split():
            errors.append(f"{label}: Google Maps link {i+1} still carries button styling")

    for i,note in enumerate(data["affiliateNotes"]):
        if note["gap"] is not None and note["gap"] < 10:
            errors.append(f"{label}: affiliate disclosure {i+1} is only {note['gap']:.0f}px below preceding control")

    for i,card in enumerate(data["cards"]):
        if card["hasImg"] and card["imgLoaded"] is False:
            errors.append(f"{label}: hotel card {i+1} has an unloaded image")
        if card["textGap"] is not None and card["textGap"] < 5:
            errors.append(f"{label}: hotel card {i+1} label/title gap is only {card['textGap']:.0f}px")
        acts=card["actions"]
        for a in range(len(acts)):
            for b in range(a+1,len(acts)):
                x=max(0,min(acts[a]["r"],acts[b]["r"])-max(acts[a]["l"],acts[b]["l"]))
                y=max(0,min(acts[a]["b"],acts[b]["b"])-max(acts[a]["t"],acts[b]["t"]))
                if x*y > 2:
                    errors.append(f"{label}: hotel card {i+1} has overlapping actions")

    # Cards sharing a desktop row should end on the same visual baseline.
    if not mobile and data["exploreCards"]:
        rows={}
        for card in data["exploreCards"]:
            key=round(card["top"]/12)*12
            rows.setdefault(key,[]).append(card)
        for row in rows.values():
            bottoms=[x["bottom"] for x in row]
            action_bottoms=[x["actionBottom"] for x in row if x["actionBottom"] is not None]
            if len(bottoms)>1 and max(bottoms)-min(bottoms)>5:
                errors.append(f"{label}: Explore hotel cards in one row differ by {max(bottoms)-min(bottoms):.0f}px in height")
            if len(action_bottoms)>1 and max(action_bottoms)-min(action_bottoms)>12:
                errors.append(f"{label}: Explore hotel actions float on different baselines")

    if path in BASE_DESTINATION_PATHS and data["fitCount"] > 1:
        errors.append(f"{label}: {data['fitCount']} visible Hotel Fit links remain in destination article")

    if data["legacy"]:
        center=(data["legacy"]["left"]+data["legacy"]["right"])/2
        if abs(center-data["legacy"]["vw"]/2)>5:
            errors.append(f"{label}: legacy Riviera Guide content is not centred")

    if "monaco" in path and data["practical"]:
        if data["practical"]["bg"] in ("rgba(0, 0, 0, 0)","transparent") or data["practical"]["borderLeft"] < 3:
            errors.append(f"{label}: Monaco practical block is visually unformatted")

    return errors


def main() -> None:
    paths = sitemap_paths()
    errors: list[str] = []
    counts = {"mobile": 0, "desktop": 0}
    print("V26 GLOBAL BROWSER SWEEP")
    print("sitemap URLs:", len(paths))

    with local_server() as base, sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            executable_path=browser_executable(),
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        try:
            for vp_name, width, height in VIEWPORTS:
                mobile = vp_name == "mobile"
                context = browser.new_context(viewport={"width": width, "height": height})
                page = context.new_page()

                def route_handler(route):
                    if route.request.url.startswith(base):
                        route.continue_()
                    else:
                        route.abort()

                page.route("**/*", route_handler)
                for n, path in enumerate(paths, 1):
                    label = f"{vp_name} {path}"
                    try:
                        response = page.goto(base + path, wait_until="domcontentloaded", timeout=12000)
                        if response is None or response.status >= 400:
                            errors.append(f"{label}: HTTP {response.status if response else 'no response'}")
                            continue
                        page.wait_for_timeout(20)
                        errors.extend(check_common(page, label, width, mobile))
                        if mobile:
                            errors.extend(check_mobile_cover(page, label))
                            errors.extend(check_mobile_menu(page, label))
                            errors.extend(check_destination_tool_link(page, label, path))
                        errors.extend(check_family_consistency(page, label, path, mobile))
                        counts[vp_name] += 1
                    except Exception as exc:
                        errors.append(f"{label}: browser exception {type(exc).__name__}: {exc}")
                    if n % 25 == 0:
                        print(f"{vp_name}: checked {n}/{len(paths)}")
                context.close()
        finally:
            browser.close()

    print("rendered:", counts)
    if errors:
        print("GLOBAL BROWSER SWEEP FAILURES:", len(errors))
        for e in errors[:240]:
            print("FAIL:", e)
        if len(errors) > 240:
            print("... plus", len(errors)-240, "more")
        raise SystemExit(f"{len(errors)} gross browser anomaly/anomalies")

    print(f"PASS: {len(paths)} sitemap URLs rendered cleanly at both viewports.")


if __name__ == "__main__":
    main()
