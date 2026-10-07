#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit lot 4A: localise Wikimedia editorial images.

The live site must not hotlink editorial photography. Existing Mametas-local
assets are reused first. Five missing Commons images are downloaded during the
build, resized to max 1600px and written as WebP under assets/editorial/culture/.
Credits already present in the HTML are preserved.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import io
import re

from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/editorial/culture"
OUT.mkdir(parents=True,exist_ok=True)

DOWNLOADS={
  "villa-ephrussi-wikimedia.webp":"https://upload.wikimedia.org/wikipedia/commons/1/1d/Villa_ephrussi_de_rothschild.jpg",
  "musee-fernand-leger-wikimedia.webp":"https://upload.wikimedia.org/wikipedia/commons/3/33/Biot_musee_f_leger.JPG",
  "musee-explorations-cannes-wikimedia.webp":"https://upload.wikimedia.org/wikipedia/commons/0/09/Musee_de_la_Castre%2C_Cannes%2C_Provence-Alpes-C%C3%B4te_d%27Azur%2C_France_-_panoramio.jpg",
  "musee-cocteau-bastion-wikimedia.webp":"https://upload.wikimedia.org/wikipedia/commons/6/60/Le_mus%C3%A9e_du_Bastion_Jean_Cocteau_%28Menton%2C_France%29_%2833757795078%29.jpg",
  "musee-oceanographique-monaco-wikimedia.webp":"https://upload.wikimedia.org/wikipedia/commons/7/72/Mus%C3%A9e_Oc%C3%A9anographique_de_Monaco.jpg",
  "nice-vieux-nice-wikimedia.webp":"https://upload.wikimedia.org/wikipedia/commons/1/16/Nice_Vieux-Nice_1.jpg",
}

def fetch_image(name,url):
    out=OUT/name
    if out.exists() and out.stat().st_size>20_000:
        print("media exists",out.relative_to(ROOT))
        return
    req=Request(url,headers={"User-Agent":"MametasEditorialImageLocalizer/1.0 (+https://www.mametas.com/)"})
    with urlopen(req,timeout=60) as r:
        data=r.read()
    with Image.open(io.BytesIO(data)) as im:
        im=ImageOps.exif_transpose(im).convert("RGB")
        if im.width>1600:
            h=round(im.height*1600/im.width)
            im=im.resize((1600,h),Image.Resampling.LANCZOS)
        im.save(out,"WEBP",quality=84,method=6)
    if out.stat().st_size<20_000:
        raise RuntimeError(f"Generated image suspiciously small: {out}")
    print("localised",out.relative_to(ROOT),out.stat().st_size)

# File-name based mapping covers both Special:Redirect and upload.wikimedia URLs.
MAP={
  "08_Fondation_Maeght.JPG":"/assets/editorial/fondation-maeght-waterborough.webp",
  "Villa_Ephrussi_de_Rothschild.jpg":"/assets/editorial/culture/villa-ephrussi-wikimedia.webp",
  "Villa%20Ephrussi%20de%20Rothschild.jpg":"/assets/editorial/culture/villa-ephrussi-wikimedia.webp",
  "Biot_musee_f_leger.JPG":"/assets/editorial/culture/musee-fernand-leger-wikimedia.webp",
  "Biot%20musee%20f%20leger.JPG":"/assets/editorial/culture/musee-fernand-leger-wikimedia.webp",
  "Musee_de_la_Castre%2C_Cannes%2C_Provence-Alpes-C%C3%B4te_d%27Azur%2C_France_-_panoramio.jpg":"/assets/editorial/culture/musee-explorations-cannes-wikimedia.webp",
  "Musee%20de%20la%20Castre%2C%20Cannes%2C%20Provence-Alpes-C%C3%B4te%20d%27Azur%2C%20France%20-%20panoramio.jpg":"/assets/editorial/culture/musee-explorations-cannes-wikimedia.webp",
  "Le_mus%C3%A9e_du_Bastion_Jean_Cocteau_%28Menton%2C_France%29_%2833757795078%29.jpg":"/assets/editorial/culture/musee-cocteau-bastion-wikimedia.webp",
  "Le%20mus%C3%A9e%20du%20Bastion%20Jean%20Cocteau%20%28Menton%2C%20France%29%20%2833757795078%29.jpg":"/assets/editorial/culture/musee-cocteau-bastion-wikimedia.webp",
  "Mus%C3%A9e_Oc%C3%A9anographique_de_Monaco.jpg":"/assets/editorial/culture/musee-oceanographique-monaco-wikimedia.webp",
  "Mus%C3%A9e%20Oc%C3%A9anographique%20de%20Monaco.jpg":"/assets/editorial/culture/musee-oceanographique-monaco-wikimedia.webp",
  "Le%20Cannet%20-%20Le%20mus%C3%A9e%20Bonnard.JPG":"/assets/editorial/culture-musee-bonnard-v2.webp",
  "Mus%C3%A9e%20Matisse%20de%20Nice.jpg":"/assets/editorial/culture-musee-matisse-v2.webp",
  "Antibes%20Museum%20Picasso.jpg":"/assets/editorial/culture-musee-picasso-antibes-v2.webp",
  "Villa%20K%C3%A9rylos%2C%20Beaulieu-sur-Mer%20P1030831.jpg":"/assets/editorial/culture-villa-kerylos-v2.webp",
  "Nice%20Vieux-Nice%201.jpg":"/assets/editorial/culture/nice-vieux-nice-wikimedia.webp",
}

def replacement(url):
    if "wikimedia.org" not in url and "wikipedia.org" not in url:
        return url
    for needle,local in MAP.items():
        if needle in url:
            return local
    return url

def patch_html():
    changed=0
    unresolved=[]
    attr_re=re.compile(r'(?P<prefix>\b(?:src|srcset)=["\'])(?P<url>[^"\']+)(?P<suffix>["\'])',re.I)
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {".git",".github","scripts","docs","backup",
                                         "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}:
            continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        old=s
        def repl(m):
            url=m.group("url")
            if "wikimedia.org" not in url and "wikipedia.org" not in url:
                return m.group(0)
            local=replacement(url)
            if local==url:
                unresolved.append((rel.as_posix(),url))
            return m.group("prefix")+local+m.group("suffix")
        s=attr_re.sub(repl,s)
        if s!=old:
            p.write_text(s,encoding="utf-8"); changed+=1
    print("Wikimedia localisation changed",changed,"HTML files")
    if unresolved:
        for rel,url in unresolved[:30]: print("UNRESOLVED",rel,url)
        raise RuntimeError(f"{len(unresolved)} remote Wikimedia image references have no mapping")

def validate():
    missing=[]
    for name in DOWNLOADS:
        p=OUT/name
        if not p.exists() or p.stat().st_size<20_000:
            missing.append(str(p.relative_to(ROOT)))
    if missing:
        raise RuntimeError("Missing localised media: "+", ".join(missing))
    remote=[]
    rx=re.compile(r'<img\b[^>]*(?:src|srcset)=["\'][^"\']*(?:wikimedia|wikipedia)[^"\']*["\']',re.I)
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {".git",".github","scripts","docs","backup",
                                         "lesnicoises-v8-no-mercy-update","lesnicoises-v8-no-mercy-update 2"}:
            continue
        s=p.read_text(encoding="utf-8",errors="ignore")
        if rx.search(s): remote.append(rel.as_posix())
    if remote:
        raise RuntimeError("Remote Wikimedia images survive: "+", ".join(remote[:30]))
    print("Wikimedia image localisation validation passed.")

def main():
    for name,url in DOWNLOADS.items():
        fetch_image(name,url)
    patch_html()
    validate()

if __name__=="__main__":
    main()
