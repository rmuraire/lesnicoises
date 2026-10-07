#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Localise every Wikimedia image used by public Mametas HTML.

This removes visitor-time dependencies on commons.wikimedia.org/upload.wikimedia.org.
Remote credit/source links are left untouched; only image URLs are localised.
Special:Redirect/file images request a 1600px derivative when supported.
"""
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode, parse_qsl, urlunparse
from urllib.request import Request, urlopen
import hashlib
import html as htmlmod
import mimetypes
import re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/editorial/culture-local"
OUT.mkdir(parents=True,exist_ok=True)
SKIP={".git",".github","scripts","docs","backup","lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}

REMOTE_RE=re.compile(r'https://(?:commons|upload)\.wikimedia\.org/[^"\'<>\s]+',re.I)

def clean_url(raw):
    return htmlmod.unescape(raw).rstrip('),.;')

def download_url(url):
    parsed=urlparse(url)
    if parsed.netloc.lower()=="commons.wikimedia.org" and "/Special:Redirect/file/" in parsed.path:
        q=dict(parse_qsl(parsed.query,keep_blank_values=True))
        q.setdefault("width","1600")
        parsed=parsed._replace(query=urlencode(q))
        url=urlunparse(parsed)
    req=Request(url,headers={"User-Agent":"MametasLocalImageBot/1.0 (+https://www.mametas.com/methode/)"})
    with urlopen(req,timeout=60) as r:
        data=r.read()
        ctype=(r.headers.get("Content-Type") or "").split(";")[0].lower()
        final=r.geturl()
    if not data:
        raise RuntimeError(f"empty image response: {url}")
    return data,ctype,final

def local_name(url,ctype):
    parsed=urlparse(url)
    name=unquote(Path(parsed.path).name)
    name=re.sub(r'^\d+px-','',name,flags=re.I)
    stem=Path(name).stem or "wikimedia-image"
    stem=re.sub(r'[^a-zA-Z0-9]+','-',stem).strip('-').lower()[:70] or "wikimedia-image"
    ext=Path(name).suffix.lower()
    if ext not in {".jpg",".jpeg",".png",".webp"}:
        ext={ "image/jpeg":".jpg","image/png":".png","image/webp":".webp" }.get(ctype,".jpg")
    if ext==".jpeg": ext=".jpg"
    digest=hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return f"wm-{stem}-{digest}{ext}"

def main():
    pages=[]
    urls=set()
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        found={clean_url(m.group(0)) for m in REMOTE_RE.finditer(text)}
        if found:
            pages.append((p,text,found))
            urls.update(found)

    print(f"Wikimedia localisation: {len(urls)} unique image URLs across {len(pages)} pages.")
    mapping={}
    for url in sorted(urls):
        data,ctype,final=download_url(url)
        filename=local_name(url,ctype)
        dst=OUT/filename
        dst.write_bytes(data)
        mapping[url]="/assets/editorial/culture-local/"+filename
        print(f"localized {url} -> {mapping[url]} ({len(data)} bytes; {ctype}; final={final})")

    changed=0
    for p,text,found in pages:
        new=text
        for url in found:
            # Handle raw and HTML-escaped variants.
            new=new.replace(url,mapping[url]).replace(htmlmod.escape(url,quote=False),mapping[url])
        if new!=text:
            p.write_text(new,encoding="utf-8")
            changed+=1
    print(f"rewrote {changed} HTML pages")

    leftovers=[]
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        if REMOTE_RE.search(text):
            leftovers.append(rel.as_posix())
    if leftovers:
        raise RuntimeError("Remote Wikimedia image URLs survived: "+", ".join(leftovers[:20]))

    if urls and not any(OUT.iterdir()):
        raise RuntimeError("No local Wikimedia assets were written")
    print("Wikimedia image localisation passed.")

if __name__=="__main__":
    main()
