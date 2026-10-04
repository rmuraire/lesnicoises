#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prescriber credibility gates from Claude audit, 4 Oct 2026.
No traveller-voice rewriting here: testimonials are a separate reviewed pass.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

def patch(rel, fn):
    p=ROOT/rel
    if not p.exists(): print("skip",rel); return
    s=p.read_text(encoding="utf-8",errors="ignore"); n=fn(s)
    if n!=s: p.write_text(n,encoding="utf-8"); print("patched",rel)
    else: print("unchanged",rel)

# C4/C5: flagship Nice copy: repair template residue and French machine-like errors.
patch("en/riviera-guide/nice/index.html",lambda s:s.replace("exist, . Remember","exist, gari. Remember"))
def nice_fr(s):
    for a,b in {
      "exister, . Gardez":"exister, pichoun. Gardez",
      "C’est la meilleur premier point de chute":"C’est le meilleur premier point de chute",
      "C'est la meilleur premier point de chute":"C'est le meilleur premier point de chute",
      "transformer Nice en camp de ville uniquement":"traiter Nice uniquement comme un camp de base",
      "transformer Nice en camp de ville":"transformer Nice en camp de base",
      "C’est là que la ville devient vraiment une ville":"C’est là que Nice commence vraiment à fonctionner comme point de chute",
      "C'est là que la ville devient vraiment une ville":"C'est là que Nice commence vraiment à fonctionner comme point de chute",
    }.items(): s=s.replace(a,b)
    return s
patch("riviera-guide/nice/index.html",nice_fr)

# C2: IRONMAN. The audit establishes 2026 cancellation and reports 12 Sep 2027,
# but also notes conflicting earlier dates. State cancellation; do not overclaim 2027 until official confirmation.
def iron_en(s):
    s=s.replace("The 2027 date is not yet published on the official event page as of 28 September 2026.",
      "The 2026 IRONMAN France Nice was cancelled during the June heatwave. Recheck the official event page before booking around the 2027 race date.")
    s=s.replace("<b>2026 landmarks</b><span>Village at Jardin Albert-Ier, start at Plage des Ponchettes, finish opposite Ruhl Plage.</span>",
      "<b>2026 edition</b><span>Cancelled because of the June heatwave. Do not use the planned 2026 timetable as proof of 2027 logistics.</span>")
    s=s.replace("The 2026 race-week hub.","The planned 2026 race-week hub; confirm the 2027 layout in the current Athlete Guide.")
    return s
def iron_fr(s):
    s=s.replace("La date 2027 n’est pas encore publiée sur la page officielle au 28 septembre 2026.",
      "L’IRONMAN France Nice 2026 a été annulé pendant la canicule de juin. Vérifiez la page officielle avant de réserver autour de la date 2027.")
    s=s.replace("<b>Repères 2026</b><span>Village au Jardin Albert-Ier, départ Plage des Ponchettes, arrivée face à Ruhl Plage.</span>",
      "<b>Édition 2026</b><span>Annulée en raison de la canicule de juin. N’utilisez pas le programme prévu en 2026 comme preuve de la logistique 2027.</span>")
    s=s.replace("Le centre de gravité de la semaine de course en 2026.","Le village prévu en 2026 ; confirmez l’implantation 2027 dans le guide athlète de l’année.")
    return s
patch("en/good-finds/ironman-nice/index.html",iron_en)
patch("bons-plans/ironman-nice/index.html",iron_fr)

# C3: stale monthly page: archive language, no longer "now".
def archive_en(s):
    s=s.replace("Now · Late September","Archive · September 2026").replace("NOW · LATE SEPTEMBER","ARCHIVE · SEPTEMBER 2026")
    s=s.replace("this month","in September 2026").replace("This month","September 2026")
    return s
def archive_fr(s):
    s=s.replace("Maintenant · Fin septembre","Archives · Septembre 2026").replace("MAINTENANT · FIN SEPTEMBRE","ARCHIVES · SEPTEMBRE 2026")
    s=s.replace("ce mois-ci","en septembre 2026").replace("Ce mois-ci","Septembre 2026")
    return s
patch("en/good-finds/september-2026/index.html",archive_en)
patch("bons-plans/septembre-2026/index.html",archive_fr)

# C7: PUMa wording. Preserve uncertainty: law created the contribution; decree controls application.
def puma_en(s):
    patterns=[
      r"New in 2026:[^<]{0,400}?(?:1 October|October 1)[^<]*\.",
      r"New in 2026:[^<]{0,500}?contribution[^<]*\."
    ]
    repl=("New in 2026: the Social Security Financing Act created a contribution for certain PUMa beneficiaries "
          "who are exempt from CSG under a tax treaty. The amount and application timetable depend on an implementing decree; "
          "check the current official position before making a residency or budget decision.")
    for pat in patterns: s=re.sub(pat,repl,s,count=1,flags=re.I)
    return s
def puma_fr(s):
    patterns=[
      r"Nouveau en 2026\s*:[^<]{0,500}?contribution[^<]*\.",
      r"En 2026[^<]{0,500}?contribution[^<]*\."
    ]
    repl=("Nouveau en 2026 : la loi de financement de la Sécurité sociale a créé une contribution pour certains bénéficiaires "
          "de la PUMa exonérés de CSG au titre d’une convention fiscale. Son montant et son calendrier d’application dépendent "
          "d’un décret d’application ; vérifiez la position officielle à jour avant toute décision de résidence ou de budget.")
    for pat in patterns: s=re.sub(pat,repl,s,count=1,flags=re.I)
    return s
patch("en/explore/retire-french-riviera/index.html",puma_en)
patch("explore/retraite-cote-d-azur/index.html",puma_fr)

# C8: never allow sponsored/affiliate links in a Sources checked block.
def clean_sources(s):
    def block(m):
        x=m.group(0)
        x=re.sub(r'<li>[^<]*(?:<a[^>]+(?:kqzyfj\.com|rel="[^"]*sponsored)[^>]*>.*?</a>)[\s\S]*?</li>','',x,flags=re.I)
        return x
    return re.sub(r'<div class="sources">[\s\S]*?</div>',block,s,flags=re.I)
patch("en/gay-french-riviera/where-to-stay/index.html",clean_sources)
patch("cote-dazur-gay/ou-dormir/index.html",clean_sources)

# C10: remove internal workshop language from reader-facing hotel copy.
for rel in ("en/hotels/nice/index.html","fr/dormir/nice/index.html","stay/nice/index.html","hotels/nice/index.html","en/hotels/nice/villa-victoria/index.html","hotels/nice/villa-victoria/index.html"):
    def workshop(s):
        replacements={
          "Our new practical pick":"A practical central pick",
          "New calm pick":"Calm central pick",
          "Villa Victoria finally gives us a central calm card below the palace logic":"Villa Victoria suits travellers who want a calmer central stay without moving out to the seafront palaces",
          "Villa Victoria gives the Nice shortlist something it badly needed":"Villa Victoria is strongest for travellers who value a garden, a calmer street and a central location",
          "Notre nouveau choix pratique":"Un choix central et pratique",
          "Nouveau choix calme":"Choix central et calme",
        }
        for a,b in replacements.items(): s=s.replace(a,b)
        return s
    patch(rel,workshop)

# D3 was already added in v7. Add a decision-useful typical-last-return box, explicitly non-timetable.
EN_LAST=r'''<section class="solo-last-return" data-layer="solo-last-return-2026-10-04"><p class="eyebrow">DINNER OUT OF TOWN?</p><h2>Check the last return before you order dessert.</h2><p>Regional trains are excellent for daytime Riviera trips, but evening frequency thins out and the last useful return depends on the destination, day and season. For Monaco, Menton, Antibes or Cannes, open SNCF Connect on the day and check the final two departures back to Nice <strong>before</strong> dinner. If the last train would make the evening stressful, eat in Nice or budget for a taxi/VTC home.</p><p class="spot-logistics"><strong>Nice itself is easier late:</strong> the tram runs substantially later than most day-trip trains, but published times still change by day and works. Treat the app/operator timetable as the source of truth, not a screenshot from this guide.</p></section>'''
FR_LAST=r'''<section class="solo-last-return" data-layer="solo-last-return-2026-10-04"><p class="eyebrow">DÎNER HORS DE NICE ?</p><h2>Regardez le dernier retour avant de commander le dessert.</h2><p>Les TER sont excellents pour parcourir la Riviera en journée, mais la fréquence baisse le soir et le dernier retour utile varie selon la destination, le jour et la saison. Pour Monaco, Menton, Antibes ou Cannes, ouvrez SNCF Connect le jour même et regardez les deux derniers départs vers Nice <strong>avant</strong> le dîner. Si le dernier train transforme la soirée en course, dînez à Nice ou prévoyez le budget taxi/VTC.</p><p class="spot-logistics"><strong>À Nice, c’est plus simple tard :</strong> le tram circule nettement plus tard que la plupart des trains d’excursion, mais les horaires changent aussi selon le jour et les travaux. La source de vérité reste l’application ou l’opérateur, pas une capture d’écran de ce guide.</p></section>'''
def add_before_sources(s,block,token):
    if token in s:return s
    i=s.find('<div class="sources">')
    if i<0:i=s.find('</article>')
    return s[:i]+block+s[i:] if i>=0 else s
for rel in ("en/solo-female-french-riviera/getting-around/index.html","en/solo-female-french-riviera/index.html"):
    patch(rel,lambda s,b=EN_LAST:add_before_sources(s,b,"solo-last-return-2026-10-04"))
for rel in ("cote-dazur-femme-solo/se-deplacer/index.html","cote-dazur-femme-solo/index.html"):
    patch(rel,lambda s,b=FR_LAST:add_before_sources(s,b,"solo-last-return-2026-10-04"))

# Gay FAQs: make Pride and beach answers useful, while keeping them date-safe.
for rel in ("en/gay-french-riviera/index.html","en/gay-nice/index.html"):
    def gay_en(s):
        s=s.replace("Event dates change. Check the current official programme before you build the trip around Pride.",
          "Nice’s Pink Parade is typically a July event. The 2026 parade ran on Saturday 11 July; check the current official programme before building a future trip around it.")
        s=s.replace("There is no single official gay beach.", "There is no single official gay beach. For the practical differences between Castel, Coco Beach and Saint-Laurent-d’Èze, use our beaches-without-a-car guide.")
        return s
    patch(rel,gay_en)
for rel in ("cote-dazur-gay/index.html","guide-gay-nice/index.html"):
    def gay_fr(s):
        s=s.replace("Les dates changent. Vérifiez le programme officiel", "La Pink Parade de Nice a généralement lieu en juillet. L’édition 2026 s’est tenue le samedi 11 juillet ; vérifiez le programme officiel")
        s=s.replace("Il n’y a pas une seule plage gay officielle.", "Il n’existe pas une unique plage gay officielle. Pour comparer concrètement Castel, Coco Beach et Saint-Laurent-d’Èze, utilisez notre guide des plages sans voiture.")
        return s
    patch(rel,gay_fr)

# Validation: trust-breaker strings must not survive if the target pages exist.
checks=[
 ("en/riviera-guide/nice/index.html",[", ."]),
 ("riviera-guide/nice/index.html",[", .","la meilleur premier"]),
 ("en/good-finds/ironman-nice/index.html",["2027 date is not yet published","2026 landmarks"]),
 ("bons-plans/ironman-nice/index.html",["date 2027 n’est pas encore publiée","Repères 2026"]),
]
for rel,bad in checks:
    p=ROOT/rel
    if p.exists():
        s=p.read_text(encoding="utf-8",errors="ignore")
        for x in bad:
            if x.lower() in s.lower(): raise RuntimeError(f"{rel}: stale credibility string: {x}")
print("Prescriber credibility gates passed.")
