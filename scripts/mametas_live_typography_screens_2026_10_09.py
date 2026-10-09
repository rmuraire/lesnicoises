#!/usr/bin/env python3
"""Live typography screenshots and computed-style inventory, not a CSS rewrite.

Screens every URL in the live sitemap at mobile and desktop widths. The
three requested pages are always first. Outputs captures plus CSV/JSON/MD.
"""
from __future__ import annotations
import argparse, collections, csv, json, os, re, shutil, statistics, sys, time
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE="https://www.mametas.com"
FOCUS=[
    "/en/good-finds/mipim-cannes/",
    "/en/hotels/eze/la-chevre-d-or/",
    "/en/riviera-guide/villefranche-cap-ferrat/",
]
VIEWPORTS=[("desktop",1440,900),("mobile",390,844)]
JS=r"""() => {
  const main=document.querySelector('main')||document.body;
  const all=sel=>Array.from(main.querySelectorAll(sel)).filter(el=>{
    const s=getComputedStyle(el),r=el.getBoundingClientRect();
    return r.height>2&&s.display!=='none'&&s.visibility!=='hidden'
      &&!el.closest('header,footer,nav,.site-header,.site-footer');
  });
  const data=el=>{const s=getComputedStyle(el);
    return {tag:el.tagName.toLowerCase(),text:(el.innerText||'').trim().slice(0,145),
      fontPx:parseFloat(s.fontSize),linePx:parseFloat(s.lineHeight)||null,
      weight:s.fontWeight,family:s.fontFamily,
      selector:el.className&&typeof el.className==='string'?el.className.slice(0,110):''};
  };
  const d={h1:all('h1').slice(0,3).map(data),
    h2:all('h2').slice(0,35).map(data),
    h3:all('h3').slice(0,50).map(data),
    p:all('p').filter(el=>(el.innerText||'').trim().length>35).slice(0,90).map(data),
    leads:all('.hero-lead,.lead,.intro,.deck,.editorial-intro,.rg-lead,.site-lead')
       .slice(0,9).map(data)};
  d.stylesheets=Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
    .map(el=>el.getAttribute('href')).filter(Boolean);
  d.scrollWidth=document.documentElement.scrollWidth;
  d.bodyWidth=document.documentElement.clientWidth;
  return d;
}"""
def mode(values):
    if not values:return None
    v=[float(x["fontPx"]) for x in values if isinstance(x.get("fontPx"),(int,float))]
    if not v:return None
    return statistics.median(v)
def load_urls(focus):
    if focus:return FOCUS[:]
    urls=[]
    try:
        raw=urlopen(BASE+"/sitemap.xml",timeout=15).read()
        tree=ET.fromstring(raw)
        urls=[x.text.strip() for x in tree.findall(".//{*}url/{*}loc") if x.text]
    except Exception as e:
        print("WARN live sitemap failed:",repr(e),flush=True)
    if not urls:
        p=ROOT/"sitemap.xml"
        tree=ET.fromstring(p.read_bytes())
        urls=[x.text.strip() for x in tree.findall(".//{*}url/{*}loc") if x.text]
    paths=[]
    for u in urls:
        parsed=urlparse(u)
        if parsed.hostname not in ("www.mametas.com","mametas.com"):continue
        path=parsed.path or "/"
        if not path.endswith("/") and not path.endswith(".html"):continue
        if path not in paths:paths.append(path)
    return FOCUS+[p for p in paths if p not in FOCUS]
def classify(path):
    p=path.removeprefix("/en/").removeprefix("/fr/").strip("/")
    if p.startswith(("good-finds/","bons-plans/")):return "Explore / Good Finds"
    if p.startswith(("hotels/","stay/","dormir/")):return "Hotels"
    if p.startswith(("riviera-guide/","places/")):return "Destination"
    if p.startswith(("plan/","planifier/")):return "Plan"
    if p.startswith(("culture/","beaches/","plages/","restaurants/")):return "Explore detail"
    return "Other"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--focus",action="store_true")
    ap.add_argument("--max-pages",type=int,default=400)
    args=ap.parse_args()
    paths=load_urls(args.focus)[:args.max_pages]
    out=ROOT/"typography-screen-audit"
    shots=out/"screens"
    shots.mkdir(parents=True,exist_ok=True)
    browser_path=next((shutil.which(x) for x in
      ("google-chrome","google-chrome-stable","chromium","chromium-browser")
      if shutil.which(x)),None)
    print("TYPOGRAPHY AUDIT MODE", "focus" if args.focus else "all",
          "pages",len(paths),"browser",browser_path,flush=True)
    results=[]
    with sync_playwright() as pw:
        launch_kwargs={"headless":True, "args":["--no-sandbox","--disable-dev-shm-usage"]}
        if browser_path:launch_kwargs["executable_path"]=browser_path
        browser=pw.chromium.launch(**launch_kwargs)
        contexts={label:browser.new_context(viewport={"width":w,"height":h},
             device_scale_factor=1,ignore_https_errors=True)
             for label,w,h in VIEWPORTS}
        pages={name:context.new_page() for name,context in contexts.items()}
        for i,path in enumerate(paths):
            for label,w,h in VIEWPORTS:
                page=pages[label]
                record={"path":path,"family":classify(path),"viewport":label,
                        "width":w,"status":None,"error":None}
                try:
                    resp=page.goto(BASE+path,wait_until="domcontentloaded",timeout=20000)
                    record["status"]=resp.status if resp else None
                    try:page.evaluate("() => document.fonts && document.fonts.ready",timeout=5000)
                    except Exception:pass
                    page.wait_for_timeout(160)
                    d=page.evaluate(JS)
                    for tag in ("h1","h2","h3","p"):
                        record[tag+"Px"]=mode(d[tag])
                        record[tag+"Count"]=len(d[tag])
                    record["leadPx"]=mode(d["leads"])
                    record["sheets"]=";".join(d["stylesheets"])
                    record["horizontalOverflow"]=d["scrollWidth"]>d["bodyWidth"]+2
                    record["samples"]={tag:d[tag][:6] for tag in ("h1","h2","h3","p","leads")}
                    name=f"{i:03d}_{re.sub('[^a-zA-Z0-9-]','-',path.strip('/'))[:95]}_{label}.jpg"
                    page.screenshot(path=str(shots/name),type="jpeg",quality=48,
                        full_page=True,timeout=25000,animations="disabled")
                    record["capture"]=name
                except Exception as e:
                    record["error"]=str(e)[:300]
                    print("ERROR",label,path,record["error"],flush=True)
                results.append(record)
                if i<3:print("FOCUS",json.dumps({
                    k:v for k,v in record.items()
                    if k in ("path","viewport","status","h1Px","h2Px","h3Px","pPx","leadPx","sheets","horizontalOverflow","error")
                },ensure_ascii=False),flush=True)
            if i>2 and i%20==0:
                print("PROGRESS",i,"/",len(paths),flush=True)
        browser.close()
    out.joinpath("computed-styles.json").write_text(
        json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    fields=["path","family","viewport","width","status","h1Px","h2Px",
      "h3Px","pPx","leadPx","h1Count","h2Count","h3Count","pCount",
      "horizontalOverflow","sheets","capture","error"]
    with (out/"computed-styles.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        for r in results:writer.writerow({key:r.get(key) for key in fields})
    report=["# Mametas live typography and screenshot audit",
      f"Pages visited: {len(paths)}; viewport captures requested: {len(results)}.",
      "Measurements use actual browser computed style, after DOM scripts.",
      ""]
    for viewport in ("desktop","mobile"):
        report.append("## "+viewport)
        rows=[r for r in results if r["viewport"]==viewport and r["status"]==200]
        for family in sorted(set(r["family"] for r in rows)):
            group=[r for r in rows if r["family"]==family]
            vals={k:[v[k] for v in group if isinstance(v.get(k),(int,float))] for k in ("h2Px","h3Px","pPx")}
            fmt=lambda x: ("%.1f"%statistics.median(x)) if x else "n/a"
            report.append(f"- {family} ({len(group)}): H2={fmt(vals['h2Px'])}px; H3={fmt(vals['h3Px'])}px; body={fmt(vals['pPx'])}px")
        report.append("")
        for p in FOCUS:
            r=next((x for x in rows if x["path"]==p),None)
            if r:report.append(f"- FOCUS {p}: H1={r.get('h1Px')} H2={r.get('h2Px')} H3={r.get('h3Px')} p={r.get('pPx')}; styles: {r.get('sheets')}")
        report.append("")
        big=[r for r in rows if (r.get("pPx") or 0)>=22 or (r.get("h2Px") or 0)>=44]
        report.append("### Pages with body >=22px or H2 >=44px")
        for r in big:
            report.append(f"- {r['path']}: body={r.get('pPx')}px H2={r.get('h2Px')}px")
        report.append("")
    errors=[r for r in results if r.get("error") or r.get("status")!=200]
    report.extend(["## Unavailable pages / screenshot errors"]+
     [f"- {r['viewport']} {r['path']}: HTTP {r.get('status')} {r.get('error')}" for r in errors])
    out.joinpath("report.md").write_text("\n".join(report),encoding="utf-8")
    print("\n".join(report[:min(len(report),120)]),flush=True)
    print("AUDIT COMPLETE",len(paths),"pages",len(results)-len(errors),"captures completed",
        len(errors),"errors",flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
