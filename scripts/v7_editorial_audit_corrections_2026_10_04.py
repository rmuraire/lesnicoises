#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Editorial correction sprint after the 4 Oct 2026 Claude audit.

Runs after all content generators. Conservative by design: fixes coherence,
stale production language and the solo-female decision layer without redesigning
pages or adding invented testimonials.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def read(rel):
    p=ROOT/rel
    return p, p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def write_if(rel, fn):
    p,s=read(rel)
    if not s:
        print("skip missing", rel); return
    ns=fn(s)
    if ns!=s:
        p.write_text(ns,encoding="utf-8"); print("patched",rel)
    else: print("unchanged",rel)

# 1) Method: preserve personalised traveller voices, clarify provenance.
def method_en(s):
    replacements=[
      ("editorial personas", "traveller notes"),
      ("Editorial personas", "Traveller notes"),
      ("do not necessarily correspond to identifiable individuals",
       "are based on genuine feedback shared with Mametas and may be lightly edited for clarity, length and privacy; identifying details may be changed"),
    ]
    for a,b in replacements: s=s.replace(a,b)
    anchor="Traveller notes"
    if "genuine traveller feedback" not in s and anchor in s:
        s=s.replace(anchor, anchor + " based on genuine traveller feedback",1)
    return s

def method_fr(s):
    replacements=[
      ("personas éditoriaux", "notes de voyageurs"),
      ("Personas éditoriaux", "Notes de voyageurs"),
      ("ne correspondent pas nécessairement à des personnes identifiables",
       "reposent sur des retours authentiques partagés avec Mametas et peuvent être légèrement éditées pour la clarté, la longueur et la confidentialité ; certains détails identifiants peuvent être modifiés"),
    ]
    for a,b in replacements: s=s.replace(a,b)
    return s

write_if("en/method/index.html",method_en)
write_if("methode/index.html",method_fr)

# 2) Solo voices: keep names/context, correct one confusing destination.
for rel in ("en/solo-female-french-riviera/index.html","cote-dazur-femme-solo/index.html"):
    def solo_voice_cleanup(s):
        s=s.replace("Editorial personas built from real traveller comments, experience feedback and field observations. Useful details, not universal truths.",
          "Real traveller feedback, lightly edited where needed for clarity and privacy. Useful details, not universal truths.")
        s=s.replace("Des personas éditoriaux construits à partir de vrais commentaires, retours d’expérience et constatations de terrain. Des détails utiles, pas des vérités universelles.",
          "De vrais retours de voyageuses, légèrement édités si nécessaire pour la clarté et la confidentialité. Des détails utiles, pas des vérités universelles.")
        s=s.replace("TER train tickets to Villefranche or Èze", "TER train tickets to Villefranche or Monaco")
        s=s.replace("billets TER pour Villefranche ou Èze", "billets TER pour Villefranche ou Monaco")
        return s
    write_if(rel,solo_voice_cleanup)

# 3) Solo female: a front-door neighbourhood decision, not a safety ranking.
EN_NEIGHBOURHOOD=r"""
<section class="solo-neighbourhood-call" data-layer="solo-neighbourhood-call-2026-10-04">
  <p class="eyebrow">WHERE TO STAY IN NICE</p>
  <h2>For a first solo stay, make Carré d’Or the easy answer.</h2>
  <p><strong>Mametas pick: Carré d’Or, or the southern edge of the Musiciens.</strong> Think roughly between boulevard Gambetta and avenue Jean Médecin, and preferably south of boulevard Victor-Hugo if you want the simplest late-evening walk home. You are close to the Promenade, restaurants, tram line 2 and the centre without depending on the station area.</p>
  <p><strong>Also good:</strong> the Musiciens around boulevard Victor-Hugo gives you a quieter residential feel while keeping the centre walkable. Jean Médecin itself is convenient for tram line 1 and shopping, but for a solo leisure trip we would rather sleep a few streets west or south than choose a hotel simply because it is beside Nice-Ville station.</p>
  <p><strong>Vieux Nice?</strong> Brilliant for atmosphere, less automatic with luggage or a late return: check the exact street and, in an old building, check the lift before booking. <strong>Port?</strong> Very pleasant, but farther from the airport tram and the western day-trip corridor; choose it because you like the neighbourhood, not because it is the easiest all-round base.</p>
  <p class="spot-logistics"><strong>The rule:</strong> choose the walk home after dinner before you choose the room. These are convenience recommendations, not neighbourhood safety rankings.</p>
</section>
"""
FR_NEIGHBOURHOOD=r"""
<section class="solo-neighbourhood-call" data-layer="solo-neighbourhood-call-2026-10-04">
  <p class="eyebrow">OÙ DORMIR À NICE</p>
  <h2>Pour un premier séjour seule, le Carré d’Or est le choix le plus simple.</h2>
  <p><strong>Choix Mametas : le Carré d’Or, ou le sud des Musiciens.</strong> Visez grosso modo entre le boulevard Gambetta et l’avenue Jean-Médecin, de préférence au sud du boulevard Victor-Hugo si vous voulez simplifier le retour à pied le soir. Vous restez près de la Promenade, des restaurants, du tram 2 et du centre, sans dépendre du secteur de la gare.</p>
  <p><strong>Très bien aussi :</strong> les Musiciens autour du boulevard Victor-Hugo, plus résidentiels et calmes tout en restant faciles à pied. Jean-Médecin est très pratique pour le tram 1 et les commerces, mais pour un séjour solo de loisirs nous préférons dormir quelques rues plus à l’ouest ou au sud plutôt que choisir un hôtel uniquement parce qu’il est collé à Nice-Ville.</p>
  <p><strong>Vieux-Nice ?</strong> Imbattable pour l’ambiance, moins automatique avec une valise ou un retour tardif : vérifiez la rue exacte et, dans un immeuble ancien, l’ascenseur. <strong>Le Port ?</strong> Très agréable, mais moins central pour le tram de l’aéroport et les excursions vers l’ouest ; choisissez-le pour le quartier, pas parce que c’est la base la plus simple.</p>
  <p class="spot-logistics"><strong>La règle :</strong> choisissez d’abord votre retour à pied après le dîner, puis la chambre. Ce sont des recommandations de praticité, pas un classement des quartiers par sécurité.</p>
</section>
"""

def insert_neighbourhood(s,block):
    if "solo-neighbourhood-call-2026-10-04" in s: return s
    # Put it before the existing hotel/doors section when possible.
    markers=["<h2>Six useful doors</h2>","<h2>Six portes utiles</h2>","data-layer=\"solo-verbatims-2026-09-30\""]
    for m in markers:
        i=s.find(m)
        if i>=0:
            sec=s.rfind("<section",0,i)
            pos=sec if sec>=0 else i
            return s[:pos]+block+"\n"+s[pos:]
    return s.replace("</article>",block+"\n</article>",1)

write_if("en/solo-female-french-riviera/index.html",lambda s:insert_neighbourhood(s,EN_NEIGHBOURHOOD))
write_if("cote-dazur-femme-solo/index.html",lambda s:insert_neighbourhood(s,FR_NEIGHBOURHOOD))
write_if("en/solo-female-french-riviera/where-to-stay/index.html",lambda s:insert_neighbourhood(s,EN_NEIGHBOURHOOD))
write_if("cote-dazur-femme-solo/ou-dormir/index.html",lambda s:insert_neighbourhood(s,FR_NEIGHBOURHOOD))

# 4) Replace reader-facing production/backlog language called out by the audit.
# IMPORTANT: use literal copy substitutions only. A former sentence-level regex could
# cross HTML tags and corrupt markup on generated hotel pages.
PRODUCTION_COPY_REPLACEMENTS = {
    "Our shortlist is still too thin": "Our shortlist stays deliberately selective",
    "it does not yet solve every budget": "it does not try to cover every budget",
    "rather than display our production backlog": "rather than pad the list",
    "The missing middle is no longer missing": "The middle of the market is finally useful",
    "the missing middle is no longer missing": "the middle of the market is finally useful",
    "The station-friendly answer we were missing": "A practical station-friendly choice",
    "the station-friendly answer we were missing": "a practical station-friendly choice",
    "Nice now has twenty addresses": "Nice has twenty selected addresses",
    "This page keeps its URL, but its depth now belongs to Practical": "For the detailed practical layer, use Practical",
}
for p in ROOT.rglob("*.html"):
    rel=p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git",".github","scripts","docs","backup"}: continue
    s=p.read_text(encoding="utf-8",errors="ignore"); ns=s
    for old,new in PRODUCTION_COPY_REPLACEMENTS.items():
        ns=ns.replace(old,new)
    if ns!=s:
        p.write_text(ns,encoding="utf-8")
        print("rewrote production copy",rel)

# 5) Expired September agenda: do not present it as "this month".
for rel in ("en/good-finds/index.html","bons-plans/index.html"):
    def agenda(s):
        s=s.replace("September 2026: what deserves attention this month","September 2026: archive")
        s=s.replace("Septembre 2026 : ce qui mérite votre attention ce mois-ci","Septembre 2026 : archives")
        s=s.replace("September 2026 · This month","September 2026 · Archive")
        s=s.replace("Septembre 2026 · Ce mois-ci","Septembre 2026 · Archives")
        return s
    write_if(rel,agenda)

# 6) Nice-in-the-rain: strip two exhibitions that ended in September if they survive upstream.
for rel in ("en/good-finds/nice-in-the-rain/index.html","bons-plans/nice-sous-la-pluie/index.html"):
    def expired_exhibitions(s):
        # Hide cards/paragraphs whose copy explicitly contains the expired end dates.
        s=re.sub(r'<(?:article|div|section)[^>]*>[\s\S]{0,1800}?(?:28 September 2026|27 September 2026|28 septembre 2026|27 septembre 2026)[\s\S]{0,1800}?</(?:article|div|section)>','',s,flags=re.I)
        return s
    write_if(rel,expired_exhibitions)

# 7) Add minimal style for the new solo decision block.
for rel in ("assets/v3.css","assets/site.css"):
    p,s=read(rel)
    if not s or "Solo neighbourhood decision — 2026-10-04" in s: continue
    s += """
/* Solo neighbourhood decision — 2026-10-04 */
.solo-neighbourhood-call{margin:32px 0;padding:26px 28px;border:1px solid rgba(20,33,61,.14);border-radius:18px;background:#f7f1e6}
.solo-neighbourhood-call h2{margin-top:6px}
.solo-neighbourhood-call p{max-width:820px}
@media(max-width:650px){.solo-neighbourhood-call{margin:24px 0;padding:20px 18px}}
"""
    p.write_text(s,encoding="utf-8"); print("styled",rel)

print("Editorial audit correction sprint complete.")
