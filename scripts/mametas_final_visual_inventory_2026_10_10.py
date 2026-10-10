#!/usr/bin/env python3
"""Final non-mutating user-facing layout audit of the LIVE Mametas site.

Render every sitemap page in desktop/mobile, take full-page evidence captures,
compare computed typography and component geometry with sibling pages.
Produces a ranked, actionable QA report. Does NOT write public site files.
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
    "/en/solo-female-french-riviera/where-to-stay/",
    "/en/solo-female-french-riviera/safety/",
    "/en/explore/retire-french-riviera/",
    "/en/practical/safety-emergencies/",
    "/en/culture/villa-ephrussi/",
    "/en/good-finds/nice-airport-transfer/",
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
  // Sample actual computed geometry. Static CSS tokens alone do not prove parity.
  const visible=el=>{const r=el.getBoundingClientRect(),c=getComputedStyle(el);return r.width>0&&r.height>2&&c.visibility!=='hidden'&&c.display!=='none'};
  const desc=el=>{const c=getComputedStyle(el),r=el.getBoundingClientRect();return {
    text:(el.innerText||'').trim().slice(0,80),cls:String(el.className||'').slice(0,100),
    font:parseFloat(c.fontSize),line:parseFloat(c.lineHeight)||null,w:Math.round(r.width),h:Math.round(r.height),
    bg:c.backgroundColor,display:c.display,border:parseFloat(c.borderBottomWidth)||0,
    parent:String(el.parentElement?.className||'').slice(0,80)
  }};
  const selects=(q)=>Array.from(main.querySelectorAll(q)).filter(visible);
  const maps=selects('a[href*="google.com/maps"],a[href*="maps.app.goo.gl"]');
  const hotels=selects('a[href*="/hotels/"],a[href*="/stay/"]')
      .filter(x=>/mametas hotel page|mametas hotel take|hotel fit/i.test(x.innerText||''));
  const actions=selects('a.btn,button,.btn,a.button,.button,.cta,a.rate-link');
  const article=selects('.article-body,.article,.culture-copy,.guide-content,.intent-detail .article-layout').slice(0,8);
  const images=selects('img');
  const badImg=images.filter(img=>img.complete&&img.naturalWidth===0);
  d.ui={
    maps:maps.slice(0,40).map(desc),
    hotelLinks:hotels.slice(0,35).map(desc),
    actions:actions.slice(0,65).map(desc),
    article:article.map(desc),
    imageCount:images.length,
    brokenImages:badImg.slice(0,12).map(img=>img.getAttribute('src')||''),
    headings:selects('h1,h2,h3').slice(0,30).map(desc),
    cards:selects('.hotel-card,.hotel-choice-card,.place,.intent-card,.culture-card,.destination-card').slice(0,50).map(desc),
    pageHeight:document.documentElement.scrollHeight
  };
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
    p=path.strip("/").lower()
    if p.startswith("en/"):p=p[3:]
    if p.startswith("fr/"):p=p[3:]
    if p.startswith(("solo-female-french-riviera/","voyage-femme-seule-cote-dazur/","cote-dazur-femme-solo/")):
        return "Solo Female"
    if p.startswith(("explore/","explorer/")):
        return "Explore"
    if p.startswith(("practical/","pratique/")):
        return "Practical"
    if p.startswith(("good-finds/","bons-plans/")):
        return "Good Finds"
    if p.startswith(("culture/","culture-et-musees/")):
        return "Culture"
    if p.startswith(("hotels/","stay/","dormir/")):
        return "Hotels"
    if p.startswith(("riviera-guide/","places/","destinations/")):
        return "Destinations"
    if p.startswith(("plan/","planifier/")):
        return "Plan"
    if p.startswith(("beaches/","plages/")):
        return "Beaches"
    if p.startswith(("restaurants/","restaurants-cote-dazur/")):
        return "Restaurants"
    if p.startswith(("day-trips/","escapades/")):
        return "Day trips"
    return "Other"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--focus",action="store_true")
    ap.add_argument("--max-pages",type=int,default=400)
    args=ap.parse_args()
    paths=load_urls(args.focus)[:args.max_pages]
    out=ROOT/"final-visual-audit"
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
                    record["ui"]=d["ui"]
                    name=f"{i:03d}_{re.sub('[^a-zA-Z0-9-]','-',path.strip('/'))[:95]}_{label}.jpg"
                    page.screenshot(path=str(shots/name),type="jpeg",quality=36,
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
    # Compare siblings; report outliers without changing any CSS.
    flags=[]
    for r in results:
        vp=r["viewport"];path=r["path"];fam=r["family"];ui=r.get("ui") or {}
        if r.get("status")!=200 or r.get("error"):
            flags.append(("P0",vp,path,"PAGE",f"HTTP={r.get('status')} error={r.get('error')}"))
            continue
        if r.get("horizontalOverflow"):
            flags.append(("P0",vp,path,"OVERFLOW","document wider than viewport"))
        if (r.get("pPx") or 0)>20:
            flags.append(("P1",vp,path,"BODY_TYPE",f"paragraph {r.get('pPx')}px"))
        h1=r.get("h1Px") or 0
        if h1>(90 if vp=="desktop" else 57):
            flags.append(("P1",vp,path,"H1_TYPE",f"H1 {h1}px"))
        if (r.get("h2Px") or 0)>(44 if vp=="desktop" else 38):
            flags.append(("P1",vp,path,"H2_TYPE",f"H2 {r.get('h2Px')}px"))
        for q in ui.get("article",[]):
            if vp=="desktop" and fam in ("Explore","Practical","Solo Female","Culture") and q["w"]<460 and q["h"]>450:
                flags.append(("P1",vp,path,"ARTICLE_WIDTH",f"{q['cls']}={q['w']}px"))
        if ui.get("brokenImages"):
            flags.append(("P0",vp,path,"BROKEN_IMAGES",str(ui["brokenImages"][:5])))
        for a in ui.get("actions",[]):
            if a["h"]>79 or (vp=="desktop" and a["w"]>500):
                flags.append(("P1",vp,path,"BUTTON_GEOMETRY",str(a)))
        for a in ui.get("maps",[]):
            if a["font"]>15.5 or a["h"]>36 or a["bg"] not in ("rgba(0, 0, 0, 0)","transparent"):
                flags.append(("P1",vp,path,"MAP_LINK_STYLE",str(a)))
        if fam=="Solo Female":
            for a in ui.get("hotelLinks",[]):
                if a["h"]>35 and "fit" not in a["text"].lower():
                    flags.append(("P1",vp,path,"HOTEL_LINK_STYLE",str(a)))
    for vp in ("desktop","mobile"):
        rows=[r for r in results if r["viewport"]==vp and r.get("status")==200]
        for fam in sorted(set(r["family"] for r in rows)):
            peers=[r for r in rows if r["family"]==fam]
            if len(peers)<4:continue
            for key,tolerance in (("pPx",3.2),("h2Px",8),("h3Px",8)):
                values=[r[key] for r in peers if isinstance(r.get(key),(int,float))]
                if len(values)<4:continue
                mid=statistics.median(values)
                for r in peers:
                    v=r.get(key)
                    if isinstance(v,(int,float)) and abs(v-mid)>tolerance:
                        flags.append(("P2",vp,r["path"],"PEER_TYPE",f"{key}={v:.1f}px vs {fam} median={mid:.1f}px"))
    dedup=list(dict.fromkeys(flags))
    totals=collections.Counter(f[0] for f in dedup)
    report.extend(["## User-facing visual exceptions (not code-format differences)",
        f"Exceptions: {len(dedup)}; priorities: {dict(totals)}.",
        "P0=broken/overflow, P1=noticeable display problem, P2=sibling typographic divergence.",
        ""])
    for pri,vp,path,kind,detail in sorted(dedup,key=lambda z:(z[0],z[1],z[2],z[3])):
        report.append(f"- **{pri}** {vp} {path} — {kind}: {detail[:200]}")
    out.joinpath("exceptions.json").write_text(json.dumps([
      {"priority":pri,"viewport":vp,"path":path,"issue":kind,"detail":detail}
      for pri,vp,path,kind,detail in dedup],ensure_ascii=False,indent=2),encoding="utf-8")
    print("VISUAL_AUDIT_SUMMARY",json.dumps({"pages":len(paths),"views":len(results),
      "exceptions":len(dedup),"priorities":dict(totals),
      "byKind":dict(collections.Counter(f[3] for f in dedup))}),flush=True)
    for f in dedup[:100]: print("VISUAL_EXCEPTION",json.dumps(f,ensure_ascii=False),flush=True)
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
