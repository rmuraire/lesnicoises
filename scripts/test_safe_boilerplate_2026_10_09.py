#!/usr/bin/env python3
"""Regression: removing repeated copy must never delete hotel cards/sections."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v19_final_post_parity_cleanup_2026_10_07 as cleanup

phrase="Ne choisissez pas seulement la chambre"
html="""<!DOCTYPE html><html lang="fr"><head><title>Hotel demo</title></head><body>
<section class="hotel-style-section" id="one">
  <div class="hotel-choice-grid"><article class="hotel-choice-card"><div>
   <p>Ne choisissez pas seulement la chambre : regardez le séjour.</p>
   <p>Example A.</p>
  </div></article></div>
</section>
<section class="hotel-style-section" id="two">
  <div class="hotel-choice-grid"><article class="hotel-choice-card"><div>
   <p>Ne choisissez pas seulement la chambre : regardez le séjour.</p>
   <p>Example B.</p>
  </div></article></div>
</section>
</body></html>"""
with TemporaryDirectory() as tmp:
    root=Path(tmp)
    (root/"index.html").write_text(html,encoding="utf-8")
    original=cleanup.ROOT
    cleanup.ROOT=root
    try:
        cleanup.dedupe_boilerplate()
    finally:
        cleanup.ROOT=original
    result=(root/"index.html").read_text(encoding="utf-8")
    assert result.count(phrase)==1,"Should deduplicate exactly one paragraph"
    assert result.count('<article class="hotel-choice-card"')==2,"Hotel cards must remain"
    assert result.count('</article>')==2,"Hotel card ends must remain"
    assert result.count('<section class="hotel-style-section"')==2,"Hotel sections must remain"
    assert result.count('</section>')==2,"Section closing tags must remain"
    assert "Example A." in result and "Example B." in result,"Editorial descriptions must remain"
print("PASS: boilerplate dedupe leaves cards, sections and descriptions intact")
