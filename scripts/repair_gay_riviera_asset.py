#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from io import BytesIO
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/editorial/refonte-2026/gay-riviera.webp"
URL="https://images.pexels.com/photos/2370009/pexels-photo-2370009.jpeg?cs=srgb&dl=pexels-den-cops-284450-2370009.jpg&fm=jpg"

req=Request(URL,headers={"User-Agent":"MametasBuild/1.0"})
with urlopen(req,timeout=60) as r:
    data=r.read()
if len(data)<100000:
    raise SystemExit(f"Downloaded Gay Riviera source unexpectedly small: {len(data)} bytes")

im=Image.open(BytesIO(data)).convert("RGB")
target_w=1200
if im.width>target_w:
    target_h=round(im.height*target_w/im.width)
    im=im.resize((target_w,target_h),Image.Resampling.LANCZOS)

OUT.parent.mkdir(parents=True,exist_ok=True)
im.save(OUT,"WEBP",quality=82,method=6)

check=Image.open(OUT)
check.verify()
check=Image.open(OUT)
print(f"Repaired Gay Riviera visual: {check.size} {check.format} {OUT.stat().st_size} bytes")
if check.width<800 or check.height<500 or OUT.stat().st_size<30000:
    raise SystemExit("Generated Gay Riviera visual failed quality guard")
