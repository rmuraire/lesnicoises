# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "solo-practical-layout-closure-2026-09-30"

def patch(path, fn):
    p = ROOT / path
    if not p.exists():
        print("skip missing", path)
        return
    s = p.read_text(encoding="utf-8")
    ns = fn(s)
    if ns != s:
        p.write_text(ns, encoding="utf-8")
        print("patched", path)
    else:
        print("unchanged", path)

def remove_duplicate_hero(s):
    # Older solo layer left a generic five-women hero immediately before the
    # dedicated Nice solo-female image. Keep only the specific editorial image.
    s = re.sub(
        r'<figure\s+style="margin:0 0 42px"><img[^>]+mametas-five-women-hero\.webp[^>]*></figure>\s*',
        '',
        s,
        count=1,
        flags=re.I,
    )
    return s

for path in [
    "en/solo-female-french-riviera/index.html",
    "cote-dazur-femme-solo/index.html",
]:
    patch(path, remove_duplicate_hero)

site = ROOT / "assets/site.css"
if site.exists():
    s = site.read_text(encoding="utf-8")
    marker = "/* Solo hero final spacing — 2026-09-30 */"
    if marker not in s:
        s += """
%s
.solo-female-hero{margin:0 0 30px!important}
.solo-female-hero img{display:block;width:100%%}
@media(max-width:650px){
  .solo-female-hero{margin:0 0 24px!important}
}
""" % marker
        site.write_text(s, encoding="utf-8")
        print("patched assets/site.css")

v3 = ROOT / "assets/v3.css"
if v3.exists():
    s = v3.read_text(encoding="utf-8")
    marker = "/* Practical safety compact card — 2026-09-30 */"
    if marker not in s:
        s += """
%s
.practical-safety-entry{
  padding:34px 0!important;
  background:var(--ink)!important;
  border-bottom:1px solid rgba(255,255,255,.18)!important
}
.practical-safety-entry .practical-feature-card--safety{
  display:block!important;
  min-height:0!important;
  grid-template-columns:1fr!important;
  border:0!important;
  background:transparent!important;
  color:var(--white)!important
}
.practical-safety-entry .practical-feature-copy{
  display:block!important;
  max-width:980px;
  padding:0!important
}
.practical-safety-entry .practical-feature-copy small{
  color:#f7c966!important;
  font-size:10px!important
}
.practical-safety-entry .practical-feature-copy strong{
  max-width:24ch;
  margin:8px 0 10px!important;
  color:var(--white)!important;
  font-size:clamp(28px,3.2vw,44px)!important;
  line-height:1.05!important
}
.practical-safety-entry .practical-feature-copy p{
  max-width:720px;
  margin:0 0 15px!important;
  color:rgba(255,255,255,.76)!important;
  font-size:14px!important;
  line-height:1.55!important
}
.practical-safety-entry .practical-feature-copy b{
  color:#f7c966!important
}
@media(max-width:760px){
  .practical-safety-entry{padding:28px 0!important}
  .practical-safety-entry .practical-feature-copy strong{font-size:30px!important}
}
""" % marker
        v3.write_text(s, encoding="utf-8")
        print("patched assets/v3.css")

print("solo/practical layout closure complete")
