# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "solo-verbatims-2026-09-30"

EN_BLOCK = r"""
<section class="solo-voices" data-layer="solo-verbatims-2026-09-30">
  <p class="eyebrow">SOLO, IN THEIR OWN WORDS</p>
  <h2>Four small things solo travellers noticed</h2>
  <p class="solo-voices-intro">Not surveys. Not universal truths. Just useful details from women who actually made the trip.</p>
  <div class="solo-voices-grid">
    <figure class="solo-voice">
      <blockquote>“I was worried that waiters would ignore me or give me a terrible table in the back because I was alone, but I was totally wrong. Places were really welcoming, even on busy summer evenings.”</blockquote>
      <figcaption><strong>Hannah</strong> · London · Solo · August 2025</figcaption>
    </figure>
    <figure class="solo-voice">
      <blockquote>“The best part of traveling alone here was the total freedom. Eating socca on the beach at 9pm or taking the train to spend the afternoon in Villefranche without negotiating with anyone.”</blockquote>
      <figcaption><strong>Ella</strong> · Paris · Solo · May 2026</figcaption>
    </figure>
    <figure class="solo-voice">
      <blockquote>“The SNCF app saved me so much stress. Buying TER train tickets to Villefranche or Èze directly on my phone meant I didn't have to figure out ticket machines or queue up alone when I was tired.”</blockquote>
      <figcaption><strong>Laura</strong> · Montréal · Solo · April 2026</figcaption>
    </figure>
    <figure class="solo-voice">
      <blockquote>“Old Nice walk-ups are brutal if you're on your own. I dragged my 20kg suitcase up five flights of narrow stairs because many old buildings don't have lifts. Definitely double-check amenities before booking an Airbnb or opt for a hotel.”</blockquote>
      <figcaption><strong>Clara</strong> · Berlin · Solo · October 2025</figcaption>
    </figure>
  </div>
</section>
"""

FR_BLOCK = r"""
<section class="solo-voices" data-layer="solo-verbatims-2026-09-30">
  <p class="eyebrow">ELLES L'ONT VÉCU</p>
  <h2>Quatre petits détails remarqués en voyageant seule</h2>
  <p class="solo-voices-intro">Pas un sondage. Pas des vérités universelles. Juste des détails utiles racontés par des voyageuses qui ont réellement fait le voyage.</p>
  <div class="solo-voices-grid">
    <figure class="solo-voice">
      <blockquote>« J'avais peur que les serveurs m'ignorent ou me donnent une mauvaise table au fond parce que j'étais seule, mais je me trompais complètement. L'accueil a été vraiment chaleureux, même pendant les soirées d'été très chargées. »</blockquote>
      <figcaption><strong>Hannah</strong> · Londres · Solo · août 2025</figcaption>
    </figure>
    <figure class="solo-voice">
      <blockquote>« Le meilleur dans le voyage solo ici, c'était la liberté totale. Manger de la socca sur la plage à 21 h ou prendre le train pour passer l'après-midi à Villefranche sans avoir à négocier avec personne. »</blockquote>
      <figcaption><strong>Ella</strong> · Paris · Solo · mai 2026</figcaption>
    </figure>
    <figure class="solo-voice">
      <blockquote>« L'appli SNCF m'a évité tellement de stress. Acheter mes billets TER pour Villefranche ou Èze directement sur mon téléphone m'évitait de comprendre les distributeurs ou de faire la queue seule quand j'étais fatiguée. »</blockquote>
      <figcaption><strong>Laura</strong> · Montréal · Solo · avril 2026</figcaption>
    </figure>
    <figure class="solo-voice">
      <blockquote>« Les immeubles sans ascenseur du Vieux-Nice peuvent être rudes quand on est seule. J'ai monté ma valise de 20 kg sur cinq étages dans un escalier étroit. Vérifiez vraiment les équipements avant de réserver un Airbnb, ou choisissez un hôtel. »</blockquote>
      <figcaption><strong>Clara</strong> · Berlin · Solo · octobre 2025</figcaption>
    </figure>
  </div>
</section>
"""

CSS = r"""
/* Solo traveller voices 2026-09-30 */
.solo-voices{margin:2.2rem 0}
.solo-voices .eyebrow{margin-bottom:.45rem}
.solo-voices-intro{max-width:760px;margin-bottom:1.25rem}
.solo-voices-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
.solo-voice{margin:0;padding:1.25rem 1.3rem;border:1px solid rgba(23,55,82,.14);border-radius:18px;background:#f7f1e6}
.solo-voice blockquote{margin:0;font-size:1rem;line-height:1.62}
.solo-voice figcaption{margin-top:.9rem;font-size:.82rem;line-height:1.4;opacity:.72}
@media(max-width:760px){.solo-voices-grid{grid-template-columns:1fr}.solo-voice{padding:1.05rem 1.1rem}}
"""

def insert_before(path, marker, block):
    p = ROOT / path
    if not p.exists():
        print("skip missing", path)
        return
    s = p.read_text(encoding="utf-8")
    if TOKEN in s:
        print("unchanged", path)
        return
    if marker not in s:
        raise SystemExit(f"marker not found in {path}: {marker}")
    p.write_text(s.replace(marker, block + "\n" + marker, 1), encoding="utf-8")
    print("patched", path)

insert_before("en/solo-female-french-riviera/index.html", "<h2>Six useful doors</h2>", EN_BLOCK)
insert_before("cote-dazur-femme-solo/index.html", "<h2>Six portes utiles</h2>", FR_BLOCK)

for rel in ("assets/v3.css", "assets/site.css"):
    p = ROOT / rel
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    if "Solo traveller voices 2026-09-30" not in s:
        p.write_text(s.rstrip() + "\n\n" + CSS.strip() + "\n", encoding="utf-8")
        print("styled", rel)

print("solo traveller voices complete")
