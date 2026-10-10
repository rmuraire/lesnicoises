#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restore the broken Maeght editorial photo from its existing CC BY-SA 3.0 source.

Waterborough, "08 Fondation Maeght.JPG", Wikimedia Commons, CC BY-SA 3.0:
https://commons.wikimedia.org/wiki/File:08_Fondation_Maeght.JPG
The image is downscaled from 2000×1500 and converted to WebP. The visual
and its caption exist in both EN/FR guides and Culture indexes already.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from io import BytesIO
from PIL import Image,ImageOps,UnidentifiedImageError

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"assets/editorial/fondation-maeght-waterborough.webp"
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/08_Fondation_Maeght.JPG?width=1200"

def valid(path):
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            return im.width >= 800 and im.height >= 550 and im.format=="WEBP"
    except (OSError,ValueError,UnidentifiedImageError):return False

def main():
    if valid(DEST):
        print("VALID Maeght media already on disk",DEST.stat().st_size,flush=True)
        return
    req=Request(SOURCE,headers={
        "User-Agent":"Mametas/1.0 (editorial-image; hello@mametas.com)",
        "Accept":"image/jpeg"})
    with urlopen(req,timeout=25) as resp:
        if resp.status!=200:raise RuntimeError(f"Wikimedia source status {resp.status}")
        raw=resp.read(4000000)
    with Image.open(BytesIO(raw)) as source:
        if source.width<900 or source.height<650:
            raise RuntimeError(f"Source image too small: {source.size}")
        transformed=ImageOps.exif_transpose(source).convert("RGB")
        transformed.thumbnail((1280,960))
        DEST.parent.mkdir(parents=True,exist_ok=True)
        transformed.save(DEST,"WEBP",quality=86,method=5)
    if not valid(DEST):
        raise RuntimeError("Generated Maeght WebP is not decodable")
    print("RESTORED Maeght image",DEST.stat().st_size,"bytes",flush=True)

if __name__=="__main__":
    main()
