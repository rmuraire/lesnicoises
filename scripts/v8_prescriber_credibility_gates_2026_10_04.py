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

# C2: IRONMAN. 2026 was cancelled in the June heatwave. IRONMAN France project
# director Yves Cordier announced Sunday 12 September 2027 for the next full-distance
# and 70.3 races. Attribute that date and still tell readers to recheck the official page.
def iron_en(s):
    s=s.replace(
      "The 2027 date is not yet published on the official event page as of 28 September 2026.",
      "The 2026 edition was cancelled during the June heatwave. IRONMAN France project director Yves Cordier announced Sunday 12 September 2027 for the next full-distance and 70.3 races; recheck the official event page before booking because race-week logistics can still change.")
    s=s.replace(
      "<b>Next edition</b><span>The 2026 edition was cancelled during the June heatwave. IRONMAN France project director Yves Cordier announced Sunday 12 September 2027 for the next full-distance and 70.3 races; recheck the official event page before booking because race-week logistics can still change.</span>",
      "<b>Next edition</b><span>Sunday 12 September 2027, announced by IRONMAN France project director Yves Cordier. Recheck before booking.</span>")
    s=s.replace(
      "<b>2026 landmarks</b><span>Village at Jardin Albert-Ier, start at Plage des Ponchettes, finish opposite Ruhl Plage.</span>",
      "<b>2026 edition</b><span>Cancelled because of the June heatwave. The planned 2026 layout is historical context, not a 2027 timetable.</span>")
    s=s.replace("The 2026 race-week hub.","The planned 2026 race-week hub; confirm the 2027 layout in the current Athlete Guide.")
    if "TRI247 — 2027 date announcement" not in s and '<div class="sources">' in s:
        s=s.replace("</ul></div>", '<li><a href="https://www.tri247.com/triathlon-news/elite/postponed-ironman-nice-will-not-be-rescheduled-athletes-options-revealed" target="_blank" rel="nofollow noopener">TRI247 — 2027 date announcement quoting IRONMAN France project director</a></li></ul></div>',1)
    return s

def iron_fr(s):
    s=s.replace(
      "La date 2027 n’est pas encore publiée sur la page officielle au 28 septembre 2026.",
      "L’édition 2026 a été annulée pendant la canicule de juin. Yves Cordier, directeur de projet IRONMAN France, a annoncé le dimanche 12 septembre 2027 pour les prochaines courses longue distance et 70.3 ; revérifiez la page officielle avant de réserver, car la logistique de course peut encore évoluer.")
    s=s.replace(
      "<b>Prochaine édition</b><span>L’édition 2026 a été annulée pendant la canicule de juin. Yves Cordier, directeur de projet IRONMAN France, a annoncé le dimanche 12 septembre 2027 pour les prochaines courses longue distance et 70.3 ; revérifiez la page officielle avant de réserver, car la logistique de course peut encore évoluer.</span>",
      "<b>Prochaine édition</b><span>Dimanche 12 septembre 2027, date annoncée par Yves Cordier, directeur de projet IRONMAN France. À revérifier avant réservation.</span>")
    s=s.replace(
      "<b>Repères 2026</b><span>Village au Jardin Albert-Ier, départ Plage des Ponchettes, arrivée face à Ruhl Plage.</span>",
      "<b>Édition 2026</b><span>Annulée en raison de la canicule de juin. Le dispositif prévu en 2026 reste un repère historique, pas le programme 2027.</span>")
    s=s.replace("Le centre de gravité de la semaine de course en 2026.","Le village prévu en 2026 ; confirmez l’implantation 2027 dans le guide athlète de l’année.")
    if "TRI247 — annonce de la date 2027" not in s and '<div class="sources">' in s:
        s=s.replace("</ul></div>", '<li><a href="https://www.tri247.com/triathlon-news/elite/postponed-ironman-nice-will-not-be-rescheduled-athletes-options-revealed" target="_blank" rel="nofollow noopener">TRI247 — annonce de la date 2027 citant le directeur de projet IRONMAN France</a></li></ul></div>',1)
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
for rel in ("en/solo-female-french-riviera/getting-around-without-a-car/index.html","en/solo-female-french-riviera/index.html"):
    patch(rel,lambda s,b=EN_LAST:add_before_sources(s,b,"solo-last-return-2026-10-04"))
for rel in ("cote-dazur-femme-solo/se-deplacer-sans-voiture/index.html","cote-dazur-femme-solo/index.html"):
    patch(rel,lambda s,b=FR_LAST:add_before_sources(s,b,"solo-last-return-2026-10-04"))


# D2: do not fake lift / AC / step-free filters until inventory coverage is documented.
# Instead, make the limitation useful and explicit on Hotel Fit.
HOTEL_FIT_NOTE_EN=r'''<div class="verdict" data-layer="hotel-fit-comfort-check-2026-10-04"><span class="label">ONE FILTER WE REFUSE TO FAKE</span><p><strong>Need a lift, air conditioning or genuinely step-free access?</strong> Hotel Fit does not yet turn those into yes/no filters across the whole Riviera because we do not have verified room-level data for every hotel. Where we have checked them, the full Mametas hotel page says so. If any of the three is non-negotiable, confirm the exact room and access route with the hotel before paying.</p></div>'''
HOTEL_FIT_NOTE_FR=r'''<div class="verdict" data-layer="hotel-fit-comfort-check-2026-10-04"><span class="label">UN FILTRE QUE NOUS REFUSONS DE SIMULER</span><p><strong>Ascenseur, climatisation ou accès réellement sans marche indispensables ?</strong> Hotel Fit n’en fait pas encore des filtres oui/non sur toute la Riviera : nous n’avons pas de données vérifiées au niveau de chaque chambre pour tous les hôtels. Quand l’information a été contrôlée, la fiche Mametas le précise. Si l’un de ces trois critères est non négociable, confirmez la chambre et le chemin d’accès exacts auprès de l’hôtel avant de payer.</p></div>'''
def add_hotel_fit_note(s,block):
    token="hotel-fit-comfort-check-2026-10-04"
    if token in s:return s
    needle='<p class="finder-method">'
    i=s.find(needle)
    if i<0: raise RuntimeError("Hotel Fit method marker missing")
    return s[:i]+block+s[i:]
patch("en/hotels/finder/index.html",lambda s:add_hotel_fit_note(s,HOTEL_FIT_NOTE_EN))
patch("hotels/finder/index.html",lambda s:add_hotel_fit_note(s,HOTEL_FIT_NOTE_FR))

# C3, hub side: September stays accessible as an archive but is no longer promoted as current.
def agenda_hub_en(s):
    s=s.replace("Carnival, Ironman, an exhibition closing soon. The Riviera runs on its own calendar.",
                "Carnival, MIPIM, Ironman. The Riviera runs on its own calendar.")
    s=s.replace('<span class="kicker">Nice · next edition</span>',
                '<span class="kicker">Nice · 12 September 2027 (announced)</span>')
    s=s.replace('>2026 start ↗</a>','>Ponchettes area ↗</a>')
    s=re.sub(r'<a class="card" href="/en/good-finds/september-2026/">[\s\S]*?</a>','',s,count=1,flags=re.I)
    return s

def agenda_hub_fr(s):
    s=s.replace("Carnaval, Ironman, une expo qui ferme bientôt. La Riviera a son propre calendrier.",
                "Carnaval, MIPIM, Ironman. La Riviera a son propre calendrier.")
    s=s.replace('<span class="kicker">Nice · prochaine édition</span>',
                '<span class="kicker">Nice · 12 septembre 2027 (annoncé)</span>')
    s=s.replace('>Départ 2026 ↗</a>','>Secteur des Ponchettes ↗</a>')
    s=re.sub(r'<a class="card" href="/bons-plans/septembre-2026/">[\s\S]*?</a>','',s,count=1,flags=re.I)
    return s

patch("en/good-finds/index.html",agenda_hub_en)
patch("bons-plans/index.html",agenda_hub_fr)

# C6: one canonical itinerary per length. Rebuild the standalone 3- and 7-day pages
# to the same decision standard as the five-day flagship instead of redirecting them.
PLAN3_EN=r'''<div class="phase4-days-grid">
<article><span>DAY 1</span><h3>Nice</h3><p>Old Nice, the sea and enough time to understand the base rather than treating it as a station with restaurants. Keep the first evening in Nice.</p><p><a href="/en/riviera-guide/nice/">Use the Nice guide →</a></p></article>
<article><span>DAY 2</span><h3>Choose one eastern day</h3><p>Pick <a href="/en/riviera-guide/villefranche-cap-ferrat/">Villefranche / Cap-Ferrat</a> for beauty and a slower rhythm, or <a href="/en/riviera-guide/monaco/">Monaco / Menton</a> for more contrast. Do not attempt both.</p></article>
<article><span>DAY 3</span><h3>Antibes</h3><p>Old town, ramparts and a western change of mood without spending the day in transit. Return to Nice for the last evening.</p><p><a href="/en/riviera-guide/antibes/">Use the Antibes guide →</a></p></article>
</div>
<div class="verdict"><span class="label">THE CANONICAL 3-DAY RULE</span><p>Cut, do not compress. Èze and the second eastern day disappear on purpose. Three days should feel edited, not hurried.</p></div>
<div class="fact-grid"><div class="fact"><b>Base</b><span>Nice, all three nights</span></div><div class="fact"><b>Car</b><span>No by default</span></div><div class="fact"><b>Transport</b><span>Tram + TER, with walking at each end</span></div></div>
<h2>The transport logic</h2><p>Nice keeps the airport tram, the main TER corridor and the evenings in one place. Villefranche, Monaco, Menton and Antibes all sit on the coastal rail line; Cap-Ferrat is the deliberate bus/walk exception. Check the live timetable before each outing rather than planning from an old screenshot.</p>
<h2>What deserves a reservation</h2><p>Usually very little. If the Oceanographic Museum is the anchor of a Monaco day, buy that ticket ahead. For restaurants and weather-sensitive days, keep some freedom. <a href="/en/good-finds/what-to-book/">See the Mametas booking guide →</a></p>
<div class="source-box"><strong>Checked 4 October 2026.</strong> Transport logic checked against <a href="https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur" target="_blank" rel="nofollow noopener">TER Sud / SNCF</a> and <a href="https://www.lignesdazur.com/en" target="_blank" rel="nofollow noopener">Lignes d’Azur</a>. Timetables and disruptions change.</div>
<p class="ownership-note">This is the same three-day logic used inside the <a href="/plan/five-days-nice-no-car/#make-it-three">five-day flagship</a>. For five days, use the full route. To test a different base, use <a href="/en/riviera-fit/">Riviera Fit</a>.</p>'''

PLAN3_FR=r'''<div class="phase4-days-grid">
<article><span>JOUR 1</span><h3>Nice</h3><p>Vieux-Nice, la mer et assez de temps pour comprendre la ville au lieu de la traiter comme une gare avec des restaurants. Gardez la première soirée à Nice.</p><p><a href="/riviera-guide/nice/">Utiliser le guide de Nice →</a></p></article>
<article><span>JOUR 2</span><h3>Choisissez une journée à l’est</h3><p><a href="/riviera-guide/villefranche-cap-ferrat/">Villefranche / Cap-Ferrat</a> pour la beauté et le rythme lent, ou <a href="/riviera-guide/monaco/">Monaco / Menton</a> pour davantage de contraste. Pas les deux.</p></article>
<article><span>JOUR 3</span><h3>Antibes</h3><p>Vieille ville, remparts et changement d’ambiance à l’ouest sans passer la journée dans les transports. Retour à Nice pour la dernière soirée.</p><p><a href="/riviera-guide/antibes/">Utiliser le guide d’Antibes →</a></p></article>
</div>
<div class="verdict"><span class="label">LA RÈGLE CANONIQUE DES 3 JOURS</span><p>Coupez, ne compressez pas. Èze et la seconde journée à l’est disparaissent volontairement. Trois jours doivent sembler choisis, pas précipités.</p></div>
<div class="fact-grid"><div class="fact"><b>Point de chute</b><span>Nice, trois nuits</span></div><div class="fact"><b>Voiture</b><span>Non par défaut</span></div><div class="fact"><b>Transports</b><span>Tram + TER, avec marche à l’arrivée</span></div></div>
<h2>La logique des transports</h2><p>Nice rassemble le tram de l’aéroport, l’axe TER principal et les soirées au même endroit. Villefranche, Monaco, Menton et Antibes sont sur la ligne côtière ; Cap-Ferrat est l’exception volontaire en bus et à pied. Vérifiez les horaires du jour plutôt que de planifier depuis une vieille capture d’écran.</p>
<h2>Ce qui mérite une réservation</h2><p>En général, peu de choses. Si le Musée océanographique structure votre journée à Monaco, achetez ce billet à l’avance. Pour les restaurants et les journées sensibles à la météo, gardez de la souplesse. <a href="/bons-plans/que-reserver/">Voir le guide Mametas des réservations →</a></p>
<div class="source-box"><strong>Vérifié le 4 octobre 2026.</strong> Logique de transport vérifiée auprès de <a href="https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur" target="_blank" rel="nofollow noopener">TER Sud / SNCF</a> et <a href="https://www.lignesdazur.com/" target="_blank" rel="nofollow noopener">Lignes d’Azur</a>. Horaires et perturbations évoluent.</div>
<p class="ownership-note">C’est la même logique trois jours que dans le <a href="/fr/planifier/cinq-jours-nice-sans-voiture/#make-it-three">parcours cinq jours de référence</a>. Pour cinq jours, utilisez le parcours complet. Pour tester un autre point de chute, utilisez <a href="/riviera-fit/">Riviera Fit</a>.</p>'''

PLAN7_EN=r'''<div class="phase4-days-grid">
<article><span>DAY 1</span><h3>Nice</h3><p>Old Nice, Castle Hill, sea and dinner. Learn the base before escaping it.</p></article>
<article><span>DAY 2</span><h3>Villefranche + Cap-Ferrat</h3><p>Bay, old town and one real walk or Villa Ephrussi. The beauty-and-breathing day.</p></article>
<article><span>DAY 3</span><h3>Monaco + Menton</h3><p>Monaco for spectacle first, Menton to exhale afterwards. Keep the day east; do not add Èze.</p></article>
<article><span>DAY 4</span><h3>Antibes</h3><p>Old town, ramparts, Gravette and the western counterpoint. Picasso only if Picasso actually matters to you.</p></article>
<article><span>DAY 5</span><h3>Èze</h3><p>Village early, then leave before you start collecting viewpoints. On a seven-day trip, keep Èze here and save the slow Nice option for tomorrow.</p></article>
<article><span>DAY 6</span><h3>Slow Nice</h3><p>Cimiez, Port, beach, market or a long lunch. No departure board. This is the breathing room the five-day version has to compromise on.</p></article>
<article><span>DAY 7</span><h3>Choose one extra direction</h3><p><a href="/en/riviera-guide/cannes/">Cannes</a> for Croisette, beach and an easy coastal TER; <a href="/en/riviera-guide/saint-paul-de-vence/">Saint-Paul-de-Vence</a> for art and an inland contrast. One is enough.</p></article>
</div>
<div class="verdict"><span class="label">THE CANONICAL 7-DAY RULE</span><p>Keep the five-day route, then add one slow Nice day and one genuinely different direction. Seven days buys breathing room, not a licence to double the number of towns.</p></div>
<div class="fact-grid"><div class="fact"><b>Base</b><span>Nice all week</span></div><div class="fact"><b>Car</b><span>No for this version</span></div><div class="fact"><b>Extra day</b><span>Cannes or Saint-Paul, not both</span></div></div>
<h2>The transport logic</h2><p>TER handles the coastal spine; tram handles Nice and the airport. Cap-Ferrat and Saint-Paul-de-Vence are the deliberate bus/walk exceptions. If Saint-Paul is your Day 7, check the current bus connection before you leave; if Cannes is Day 7, the TER keeps the day simpler.</p>
<h2>What deserves a reservation</h2><p>Reserve only the anchors that would genuinely spoil the day if sold out: a must-have museum slot, a specific high-demand restaurant or a boat that is central to your plan. Keep weather-sensitive days movable. <a href="/en/good-finds/what-to-book/">See what Mametas would actually book →</a></p>
<div class="source-box"><strong>Checked 4 October 2026.</strong> Transport logic checked against <a href="https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur" target="_blank" rel="nofollow noopener">TER Sud / SNCF</a> and <a href="https://www.lignesdazur.com/en" target="_blank" rel="nofollow noopener">Lignes d’Azur</a>. Timetables and disruptions change.</div>
<p class="ownership-note">This is the seven-day extension of the <a href="/plan/five-days-nice-no-car/#make-it-seven">five-day flagship</a>, not a competing itinerary. To test a different base, use <a href="/en/riviera-fit/">Riviera Fit</a>.</p>'''

PLAN7_FR=r'''<div class="phase4-days-grid">
<article><span>JOUR 1</span><h3>Nice</h3><p>Vieux-Nice, Colline du Château, mer et dîner. Comprenez le point de chute avant de le fuir.</p></article>
<article><span>JOUR 2</span><h3>Villefranche + Cap-Ferrat</h3><p>Baie, vieille ville et une vraie balade ou la Villa Ephrussi. La journée beauté et respiration.</p></article>
<article><span>JOUR 3</span><h3>Monaco + Menton</h3><p>Monaco pour le spectacle, Menton pour redescendre ensuite. Gardez la journée à l’est ; n’ajoutez pas Èze.</p></article>
<article><span>JOUR 4</span><h3>Antibes</h3><p>Vieille ville, remparts, Gravette et contrepoint à l’ouest. Picasso seulement si Picasso compte vraiment pour vous.</p></article>
<article><span>JOUR 5</span><h3>Èze</h3><p>Village tôt, puis partez avant de commencer à collectionner les panoramas. Sur sept jours, gardez Èze ici et la journée lente à Nice pour demain.</p></article>
<article><span>JOUR 6</span><h3>Nice sans objectif</h3><p>Cimiez, Port, plage, marché ou long déjeuner. Aucun tableau des départs. C’est l’air que la version cinq jours doit parfois sacrifier.</p></article>
<article><span>JOUR 7</span><h3>Choisissez une direction supplémentaire</h3><p><a href="/riviera-guide/cannes/">Cannes</a> pour la Croisette, la plage et un TER simple ; <a href="/riviera-guide/saint-paul-de-vence/">Saint-Paul-de-Vence</a> pour l’art et le contraste intérieur. Une seule suffit.</p></article>
</div>
<div class="verdict"><span class="label">LA RÈGLE CANONIQUE DES 7 JOURS</span><p>Gardez le parcours cinq jours, puis ajoutez une journée lente à Nice et une direction réellement différente. Sept jours achètent du temps, pas le droit de doubler le nombre de villes.</p></div>
<div class="fact-grid"><div class="fact"><b>Point de chute</b><span>Nice toute la semaine</span></div><div class="fact"><b>Voiture</b><span>Non dans cette version</span></div><div class="fact"><b>Jour bonus</b><span>Cannes ou Saint-Paul, pas les deux</span></div></div>
<h2>La logique des transports</h2><p>Le TER gère l’axe côtier ; le tram gère Nice et l’aéroport. Cap-Ferrat et Saint-Paul-de-Vence sont les exceptions volontaires en bus et à pied. Si vous choisissez Saint-Paul au jour 7, vérifiez la liaison du jour avant de partir ; avec Cannes, le TER simplifie davantage la journée.</p>
<h2>Ce qui mérite une réservation</h2><p>Réservez seulement les points d’ancrage dont l’absence gâcherait réellement la journée : un musée indispensable, un restaurant très demandé ou un bateau central dans votre programme. Gardez mobiles les journées sensibles à la météo. <a href="/bons-plans/que-reserver/">Voir ce que Mametas réserverait vraiment →</a></p>
<div class="source-box"><strong>Vérifié le 4 octobre 2026.</strong> Logique de transport vérifiée auprès de <a href="https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur" target="_blank" rel="nofollow noopener">TER Sud / SNCF</a> et <a href="https://www.lignesdazur.com/" target="_blank" rel="nofollow noopener">Lignes d’Azur</a>. Horaires et perturbations évoluent.</div>
<p class="ownership-note">C’est l’extension sept jours du <a href="/fr/planifier/cinq-jours-nice-sans-voiture/#make-it-seven">parcours cinq jours de référence</a>, pas un itinéraire concurrent. Pour tester un autre point de chute, utilisez <a href="/riviera-fit/">Riviera Fit</a>.</p>'''

def replace_plan_body(s, block):
    pat=r'<div class="phase4-days-grid">[\s\S]*?<p class="ownership-note">[\s\S]*?</p>'
    ns,n=re.subn(pat,block,s,count=1,flags=re.I)
    if n!=1:
        raise RuntimeError("Could not locate canonical Plan body")
    return ns

patch("plan/three-days-riviera/index.html",lambda s:replace_plan_body(s,PLAN3_EN))
patch("fr/planifier/trois-jours-cote-d-azur/index.html",lambda s:replace_plan_body(s,PLAN3_FR))
patch("plan/seven-days-riviera/index.html",lambda s:replace_plan_body(s,PLAN7_EN))
patch("fr/planifier/sept-jours-cote-d-azur/index.html",lambda s:replace_plan_body(s,PLAN7_FR))

# Remove the only remaining ambiguity from the flagship seven-day extension.
for rel in ("plan/five-days-nice-no-car/index.html","fr/planifier/cinq-jours-nice-sans-voiture/index.html"):
    def seven_extension(s):
        s=s.replace(
          "Use the day the five-day version deliberately keeps flexible: museum, market, beach, a neighbourhood you skipped and dinner without a departure board.",
          "On the seven-day version, keep Èze on Day 5 and use Day 6 for the slow Nice option: museum, market, beach, a neighbourhood you skipped and dinner without a departure board.")
        s=s.replace(
          "Musée, marché, plage, quartier laissé de côté et dîner sans tableau des départs.",
          "Dans la version sept jours, gardez Èze au jour 5 et utilisez le jour 6 pour Nice sans objectif : musée, marché, plage, quartier laissé de côté et dîner sans tableau des départs.")
        return s
    patch(rel,seven_extension)

# C9: a hotel name/media is editorial navigation, not a disguised affiliate CTA.
# Keep clearly-labelled rate buttons affiliate; route to a Mametas page where one exists.
INTERNAL_EN={
  "Hôtel Le Grimaldi by Happyculture":"/en/hotels/nice/hotel-le-grimaldi-by-happyculture/",
  "Hotel Beau Rivage":"/en/hotels/nice/hotel-beau-rivage/",
  "Boscolo Nice Hôtel &amp; Spa":"/en/hotels/nice/boscolo-nice-hotel-and-spa/",
}
INTERNAL_FR={
  "Hôtel Le Grimaldi by Happyculture":"/hotels/nice/hotel-le-grimaldi-by-happyculture/",
  "Hotel Beau Rivage":"/hotels/nice/hotel-beau-rivage/",
  "Boscolo Nice Hôtel &amp; Spa":"/hotels/nice/boscolo-nice-hotel-and-spa/",
}
CUT_HOTELS={
  "Hotel 64 Nice","Hotel Florence Nice","Hotel Byakko Nice","Hôtel KHLA Nice",
  "Hotel Amour Nice","Hôtel Aston La Scala","Hotel West End Nice Promenade",
}
def trim_hotel_hub(s):
    def keep_or_cut(m):
        card=m.group(0)
        h=re.search(r'<h3>([\s\S]*?)</h3>',card,re.I)
        name=re.sub(r'<[^>]+>','',h.group(1)).strip() if h else ""
        return "" if name in CUT_HOTELS else card
    s=re.sub(r'<article class="hotel-choice-card"[\s\S]*?</article>',keep_or_cut,s,flags=re.I)
    replacements={
      "Twenty hotels, four trip styles":"Thirteen hotels, four trip styles",
      "20 selected hotels":"13 selected hotels",
      "Twenty addresses. Four clear logics.":"Thirteen addresses. Four clear logics.",
      "Vingt hôtels, quatre styles de séjour":"Treize hôtels, quatre styles de séjour",
      "20 hôtels sélectionnés":"13 hôtels sélectionnés",
      "Vingt adresses. Quatre logiques claires.":"Treize adresses. Quatre logiques claires.",
      "Hotel 64 · Florence · Hotel 66 · Byakko":"Hotel 66 · Boutique Hôtel Nice Côte d’Azur · Apollinaire",
      "Villa Victoria · Le Grimaldi · Hotel Amour · Beau Rivage":"Villa Victoria · Le Grimaldi · Beau Rivage",
    }
    for old,new in replacements.items():
        s=s.replace(old,new)
    return s

def editorialise_hotel_hub(s,mapping):
    s=trim_hotel_hub(s)
    for name,url in mapping.items():
        esc=re.escape(name)
        s=re.sub(r'<a aria-label="'+esc+r'" class="hotel-choice-media" href="https://www\.kqzyfj\.com[^"]*"[^>]*>([\s\S]*?)</a>',
                 lambda m:f'<a aria-label="{name}" class="hotel-choice-media" href="{url}">{m.group(1)}</a>',s,count=1,flags=re.I)
        s=re.sub(r'<h3><a href="https://www\.kqzyfj\.com[^"]*"[^>]*>'+esc+r'</a></h3>',
                 f'<h3><a href="{url}">{name}</a></h3>',s,count=1,flags=re.I)
    # Hotels without a Mametas detail page keep a visible rate CTA, but the name and image stop linking straight to the till.
    s=re.sub(r'<a aria-label="([^"]+)" class="hotel-choice-media" href="https://www\.kqzyfj\.com[^"]*"[^>]*>([\s\S]*?)</a>',
             r'<div aria-label="\1" class="hotel-choice-media">\2</div>',s,flags=re.I)
    s=re.sub(r'<h3><a href="https://www\.kqzyfj\.com[^"]*"[^>]*>([\s\S]*?)</a></h3>',
             r'<h3>\1</h3>',s,flags=re.I)
    return s
patch("stay/nice/index.html",lambda s:editorialise_hotel_hub(s,INTERNAL_EN))
patch("fr/dormir/nice/index.html",lambda s:editorialise_hotel_hub(s,INTERNAL_FR))

# D5: the October hotel pages must add a practical reason to use Mametas rather than
# simply duplicate the booking listing. Facts below are deliberately limited to official/
# destination-office claims checked on 4 Oct 2026.
HOTEL_EN={
"en/hotels/nice/hotel-windsor/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>24-hour reception</b><span>Plus luggage storage</span></div><div class="fact"><b>Air conditioning</b><span>Listed by the hotel</span></div><div class="fact"><b>Seasonal pool</b><span>Heated May to late October</span></div></div><h2>Why choose it</h2><p>The Windsor makes most sense when you want central Nice without a chain-hotel feel. The tropical garden and small seasonal pool are unusual this close to the centre; the 24-hour reception and luggage storage remove some arrival-day friction.</p><h2>The catch</h2><p>This is personality-first, not a resort. Rooms are individually decorated and the pool is seasonal, so book it because that character appeals to you, not because you expect a standardized room.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Hotel facts checked 4 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://www.hotelwindsornice.com/en/" target="_blank" rel="nofollow noopener">Hôtel Windsor — official site</a></li></ul></div>''',
"en/hotels/nice/mercure-nice-centre-grimaldi/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>About 10 min</b><span>Walk to Nice-Ville, per Accor</span></div><div class="fact"><b>Lift + AC</b><span>Lift to all floors; individual air control</span></div><div class="fact"><b>Accessible</b><span>Wheelchair-accessible; 3 adapted rooms listed</span></div></div><h2>Why choose it</h2><p>This is a particularly rational scouting-trip base: roughly 500 m from the Promenade, central enough to walk the city, and close enough to Nice-Ville for day trips. Accor lists air conditioning, an elevator to every floor and wheelchair access.</p><h2>The catch</h2><p>The rooftop is a useful extra, but this is still a city-base decision rather than a sea-front fantasy. Choose it for low friction and central geography.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Hotel facts checked 4 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://all.accor.com/hotel/2186/index.en.shtml" target="_blank" rel="nofollow noopener">Accor — Mercure Nice Centre Grimaldi official page</a></li></ul></div>''',
"en/hotels/beaulieu-sur-mer/hotel-select/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>About 2 min</b><span>From Beaulieu station</span></div><div class="fact"><b>Air conditioning</b><span>Renovated rooms</span></div><div class="fact"><b>&lt;300 m</b><span>Beach, per local tourism office</span></div></div><h2>Why choose it</h2><p>The Select is about removing friction: on Place Marinoni in the centre, about two minutes from the station and within a short walk of the sea. That makes it unusually useful if Beaulieu is your base for train-heavy days.</p><h2>The catch</h2><p>Do not choose it for resort theatre. This is the practical, smaller-hotel answer. If step-free access is essential, verify the exact room and route before booking rather than assuming from the central location.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Hotel facts checked 4 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://destination.beaulieusurmer.fr/hotellerie/le-select/" target="_blank" rel="nofollow noopener">Beaulieu-sur-Mer tourism office — Hôtel Select</a></li></ul></div>''',
"en/hotels/beaulieu-sur-mer/hotel-carlton/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>Heated pool</b><span>May to October</span></div><div class="fact"><b>Air conditioning</b><span>Individual control listed</span></div><div class="fact"><b>Near the sea</b><span>Hotel describes beaches about a minute away</span></div></div><h2>Why choose it</h2><p>The Carlton sits in the useful middle between a pure transport hotel and a palace stay: Art Deco character, a guest-only heated pool in season and easy access to the sea, while still keeping Beaulieu compact and walkable.</p><h2>The catch</h2><p>Do not book it as a substitute for La Réserve. It is the smaller, easier-going option. If accessibility matters, request the adapted shower/room configuration when booking rather than assuming every room is equivalent.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Hotel facts checked 4 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://www.carlton-beaulieu.com/en/luxury-hotel-cote-azur/services/" target="_blank" rel="nofollow noopener">Hôtel Carlton — official services</a></li><li><a href="https://www.carlton-beaulieu.com/en/luxury-hotel-cote-azur/rooms/" target="_blank" rel="nofollow noopener">Hôtel Carlton — official rooms</a></li></ul></div>''',
"en/hotels/beaulieu-sur-mer/la-reserve-de-beaulieu/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>400 m</b><span>Walk from Beaulieu station</span></div><div class="fact"><b>Heated seawater pool</b><span>Outdoor, seasonal hours</span></div><div class="fact"><b>Garage + valet</b><span>Private secure parking</span></div></div><h2>Why choose it</h2><p>This is the opposite of a bed-only hotel. The waterfront setting, spa and heated seawater pool justify staying put; the station is still only about 400 m away when you do want to move.</p><h2>The catch</h2><p>You are paying for the property to be part of the holiday. If most days are spent on trains and day trips, a simpler Beaulieu hotel is the more rational buy.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Hotel facts checked 4 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://www.reservebeaulieu.com/luxury-hotel/practical-information-french-luxury-hotel/" target="_blank" rel="nofollow noopener">La Réserve de Beaulieu — official practical information</a></li></ul></div>''',
"en/hotels/menton/riva-art-spa/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>About 900 m</b><span>From Menton station</span></div><div class="fact"><b>Lift + AC</b><span>Listed by the tourism office</span></div><div class="fact"><b>Step-free option</b><span>Hotel states PMR access; adapted room listed</span></div></div><h2>Why choose it</h2><p>Riva works well for a no-car Menton test because the seafront is outside the door, the station is roughly 900 m away and the hotel lists accessible facilities. The rooftop spa is a genuine extra rather than the reason the transport logic works.</p><h2>The catch</h2><p>Nine hundred metres with luggage is still nine hundred metres. If that walk is the deciding factor, use a taxi from the station or choose a more station-centric address.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Hotel facts checked 4 October 2026</p><h2>Sources checked</h2><ul><li><a href="https://www.rivahotel.com/en/hotel-spa-menton-french-riviera/access-contact-hotel-french-riviera/" target="_blank" rel="nofollow noopener">Riva Art & Spa — official access information</a></li><li><a href="https://www.menton-riviera-merveilles.fr/offres/hotel-riva-art-spa-menton-fr-3051462/" target="_blank" rel="nofollow noopener">Menton Riviera & Merveilles tourism office</a></li></ul></div>'''
}
HOTEL_FR={
"hotels/nice/hotel-windsor/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>Réception 24h/24</b><span>Avec bagagerie</span></div><div class="fact"><b>Climatisation</b><span>Indiquée par l’hôtel</span></div><div class="fact"><b>Piscine saisonnière</b><span>Chauffée de mai à fin octobre</span></div></div><h2>Pourquoi le choisir</h2><p>Le Windsor a surtout du sens si vous voulez Nice centre sans l’ambiance d’une chaîne. Le jardin tropical et la petite piscine saisonnière sont rares aussi près du centre ; réception 24h/24 et bagagerie simplifient l’arrivée.</p><h2>Le point faible</h2><p>C’est un hôtel de personnalité, pas un resort. Les chambres sont toutes différentes et la piscine est saisonnière : choisissez-le parce que ce caractère vous plaît, pas pour une chambre standardisée.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Informations hôtel vérifiées le 4 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://www.hotelwindsornice.com/" target="_blank" rel="nofollow noopener">Hôtel Windsor — site officiel</a></li></ul></div>''',
"hotels/nice/mercure-nice-centre-grimaldi/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>Environ 10 min</b><span>À pied de Nice-Ville, selon Accor</span></div><div class="fact"><b>Ascenseur + clim</b><span>Tous les étages ; réglage individuel</span></div><div class="fact"><b>Accessible</b><span>3 chambres PMR indiquées</span></div></div><h2>Pourquoi le choisir</h2><p>C’est un point de chute très rationnel pour un séjour de repérage : environ 500 m de la Promenade, assez central pour marcher, et assez proche de Nice-Ville pour les excursions. Accor indique climatisation, ascenseur à tous les étages et accessibilité PMR.</p><h2>Le point faible</h2><p>Le rooftop est un vrai plus, mais la décision reste celle d’un hôtel de ville, pas d’un fantasme face à la mer. Choisissez-le pour la faible friction et la géographie.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Informations hôtel vérifiées le 4 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://all.accor.com/hotel/2186/index.fr.shtml" target="_blank" rel="nofollow noopener">Accor — Mercure Nice Centre Grimaldi, page officielle</a></li></ul></div>''',
"hotels/beaulieu-sur-mer/hotel-select/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>Environ 2 min</b><span>De la gare de Beaulieu</span></div><div class="fact"><b>Climatisation</b><span>Chambres rénovées</span></div><div class="fact"><b>&lt;300 m</b><span>De la plage, selon l’office de tourisme</span></div></div><h2>Pourquoi le choisir</h2><p>Le Select supprime de la friction : place Marinoni en plein centre, environ deux minutes de la gare et quelques minutes de la mer. C’est particulièrement utile si Beaulieu sert de point de chute pour des journées en train.</p><h2>Le point faible</h2><p>Ne le choisissez pas pour un séjour façon resort. C’est la petite adresse pratique. Si l’accès sans marche est indispensable, vérifiez la chambre et le chemin exact avant de réserver plutôt que de l’inférer de l’emplacement central.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Informations hôtel vérifiées le 4 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://destination.beaulieusurmer.fr/hotellerie/le-select/" target="_blank" rel="nofollow noopener">Office de tourisme de Beaulieu-sur-Mer — Hôtel Select</a></li></ul></div>''',
"hotels/beaulieu-sur-mer/hotel-carlton/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>Piscine chauffée</b><span>De mai à octobre</span></div><div class="fact"><b>Climatisation</b><span>Réglage individuel indiqué</span></div><div class="fact"><b>Mer proche</b><span>L’hôtel annonce les plages à environ une minute</span></div></div><h2>Pourquoi le choisir</h2><p>Le Carlton occupe un milieu utile entre l’hôtel purement logistique et le palace : caractère Art déco, piscine chauffée réservée aux clients en saison et mer très proche, tout en gardant Beaulieu compact et facile à pied.</p><h2>Le point faible</h2><p>Ne le réservez pas comme substitut à La Réserve. C’est l’option plus petite et décontractée. Si l’accessibilité compte, demandez la configuration de douche/chambre adaptée au moment de réserver plutôt que de considérer toutes les chambres comme équivalentes.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Informations hôtel vérifiées le 4 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://www.carlton-beaulieu.com/hotel-luxe-cote-azur/services/" target="_blank" rel="nofollow noopener">Hôtel Carlton — services officiels</a></li><li><a href="https://www.carlton-beaulieu.com/hotel-luxe-cote-azur/chambres/" target="_blank" rel="nofollow noopener">Hôtel Carlton — chambres officielles</a></li></ul></div>''',
"hotels/beaulieu-sur-mer/la-reserve-de-beaulieu/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>400 m</b><span>À pied de la gare</span></div><div class="fact"><b>Piscine d’eau de mer chauffée</b><span>Extérieure, horaires saisonniers</span></div><div class="fact"><b>Garage + voiturier</b><span>Parking privé sécurisé</span></div></div><h2>Pourquoi la choisir</h2><p>C’est l’inverse d’un hôtel où l’on ne fait que dormir. Bord de mer, spa et piscine d’eau de mer chauffée justifient de rester sur place ; la gare reste pourtant à environ 400 m quand vous voulez bouger.</p><h2>Le point faible</h2><p>Vous payez pour que l’hôtel fasse partie du voyage. Si vos journées se passent surtout en TER et en excursions, une adresse plus simple à Beaulieu est l’achat le plus rationnel.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Informations hôtel vérifiées le 4 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://www.reservebeaulieu.fr/hotel-luxe/informations-pratiques/" target="_blank" rel="nofollow noopener">La Réserve de Beaulieu — informations pratiques officielles</a></li></ul></div>''',
"hotels/menton/riva-art-spa/index.html":r'''<div class="fact-grid hotel-practical-facts"><div class="fact"><b>Environ 900 m</b><span>De la gare de Menton</span></div><div class="fact"><b>Ascenseur + clim</b><span>Indiqués par l’office de tourisme</span></div><div class="fact"><b>Option PMR</b><span>L’hôtel indique un accès PMR et une chambre adaptée</span></div></div><h2>Pourquoi le choisir</h2><p>Riva fonctionne bien pour tester Menton sans voiture : front de mer devant la porte, gare à environ 900 m et équipements accessibles indiqués. Le spa sur le toit est un vrai plus, pas la raison pour laquelle la logistique fonctionne.</p><h2>Le point faible</h2><p>Neuf cents mètres avec une valise restent neuf cents mètres. Si cette marche décide du séjour, prenez un taxi depuis la gare ou choisissez une adresse plus proche de celle-ci.</p><div class="sources hotel-fact-sources"><p class="mametas-source-date">Informations hôtel vérifiées le 4 octobre 2026</p><h2>Sources vérifiées</h2><ul><li><a href="https://www.rivahotel.com/hotel-spa-menton-cote-azur/acces-contact-hotel-riviera/" target="_blank" rel="nofollow noopener">Riva Art & Spa — accès officiel</a></li><li><a href="https://www.menton-riviera-merveilles.fr/offres/hotel-riva-art-spa-menton-fr-3051462/" target="_blank" rel="nofollow noopener">Office de tourisme Menton, Riviera & Merveilles</a></li></ul></div>'''
}
def enrich_hotel(s, block):
    if "hotel-practical-facts" in s:return s
    marker='<div class="affiliate-cta">'
    if marker not in s: raise RuntimeError("Hotel refonte page has no affiliate CTA marker")
    return s.replace(marker,block+marker,1)
patch("en/hotels/beaulieu-sur-mer/hotel-select/index.html",
      lambda s:s.replace("No pool; the point is simplicity, price and the ability to move around the Riviera without making transport a project.",
                         "The point is simplicity and the ability to move around the Riviera without making transport a project."))
patch("hotels/beaulieu-sur-mer/hotel-select/index.html",
      lambda s:s.replace("Pas de piscine : l’intérêt est la simplicité, le prix et la possibilité de bouger sur la Riviera sans transformer les transports en projet.",
                         "L’intérêt est la simplicité et la possibilité de bouger sur la Riviera sans transformer les transports en projet."))
for rel,block in HOTEL_EN.items(): patch(rel,lambda s,b=block:enrich_hotel(s,b))
for rel,block in HOTEL_FR.items(): patch(rel,lambda s,b=block:enrich_hotel(s,b))

# D4: a compact first-90-days layer, using authoritative links rather than pretending
# Mametas is an immigration or health-administration portal.
EXPAT_EN=r'''<section data-layer="expat-first-90-days-2026-10-04"><h2>Your first 90 days: three boring things that make the place livable</h2><div class="fact-grid"><div class="fact"><b>Meet people</b><span>AVF Antibes Juan-les-Pins exists specifically to welcome new arrivals and build local social ties.</span></div><div class="fact"><b>Validate the visa</b><span>If your visa is a VLS-TS, France-Visas says it must be validated online within three months of arrival.</span></div><div class="fact"><b>Find a doctor</b><span>Once you are in the French health system, choosing and declaring a médecin traitant matters for the coordinated-care pathway.</span></div></div><p>This is a starting checklist, not legal advice. Your nationality, visa category and health-cover route can change the order. Use the official pages for the actual procedure: <a href="https://www.avfantibesjuanlespins.fr/page/2964558-accueil2" target="_blank" rel="nofollow noopener">AVF Antibes Juan-les-Pins</a> · <a href="https://www.france-visas.gouv.fr/en/web/france-visas/visa-de-long-sejour" target="_blank" rel="nofollow noopener">France-Visas</a> · <a href="https://www.ameli.fr/assure/droits-demarches/principes/choisir-et-declarer-votre-medecin-traitant" target="_blank" rel="nofollow noopener">Assurance Maladie</a>.</p></section>'''
EXPAT_FR=r'''<section data-layer="expat-first-90-days-2026-10-04"><h2>Vos 90 premiers jours : trois choses peu glamour qui rendent la ville habitable</h2><div class="fact-grid"><div class="fact"><b>Créer du lien</b><span>L’AVF Antibes Juan-les-Pins a précisément pour mission d’accueillir les nouveaux arrivants et de créer un réseau local.</span></div><div class="fact"><b>Valider le visa</b><span>Si votre visa est un VLS-TS, France-Visas indique qu’il doit être validé en ligne dans les trois mois suivant l’arrivée.</span></div><div class="fact"><b>Trouver un médecin</b><span>Une fois dans le système français, choisir et déclarer un médecin traitant compte pour le parcours de soins coordonnés.</span></div></div><p>C’est une check-list de départ, pas un conseil juridique. Nationalité, type de visa et couverture santé peuvent changer l’ordre des démarches. Utilisez les pages officielles pour la procédure : <a href="https://www.avfantibesjuanlespins.fr/page/2964558-accueil2" target="_blank" rel="nofollow noopener">AVF Antibes Juan-les-Pins</a> · <a href="https://www.france-visas.gouv.fr/web/france-visas/visa-de-long-sejour" target="_blank" rel="nofollow noopener">France-Visas</a> · <a href="https://www.ameli.fr/assure/droits-demarches/principes/choisir-et-declarer-votre-medecin-traitant" target="_blank" rel="nofollow noopener">Assurance Maladie</a>.</p></section>'''
patch("en/explore/living-antibes-expat/index.html",lambda s:add_before_sources(s,EXPAT_EN,"expat-first-90-days-2026-10-04"))
patch("explore/vivre-antibes-expatrie/index.html",lambda s:add_before_sources(s,EXPAT_FR,"expat-first-90-days-2026-10-04"))

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


# Gay vertical: close the obvious audience gap without inventing a directory.
GAY_SCOPE_EN=r'''<section data-layer="gay-scope-queer-women-trans-2026-10-04"><h2>A note for queer women, trans and non-binary travellers</h2><p>This guide currently has more concrete nightlife detail for gay men because that is where the dedicated venue offer we can verify is most visible. Do not read fewer venue cards as “nothing for you”. For current community events, mixed LGBTQIA+ nights and support, use Nice Côte d’Azur’s live LGBTQIA+ calendar and the Centre LGBTQIA+ Côte d’Azur; then use the ordinary Nice evening guide for the rest of the night. We would rather say where our coverage is strongest than pretend one men-only club represents everybody.</p><p><a href="https://www.explorenicecotedazur.com/en/events/special-lgbt-calendar/" target="_blank" rel="nofollow noopener">Current LGBTQIA+ calendar →</a> · <a href="/en/gay-nice/">Gay Nice local guide →</a></p></section>'''
GAY_SCOPE_FR=r'''<section data-layer="gay-scope-queer-women-trans-2026-10-04"><h2>Un mot pour les femmes queer, les personnes trans et non-binaires</h2><p>Ce guide donne aujourd’hui davantage de détails nocturnes aux hommes gays parce que c’est là que l’offre de lieux dédiés que nous pouvons vérifier est la plus visible. Moins de cartes ne signifie pas « rien pour vous ». Pour les événements communautaires, soirées LGBTQIA+ mixtes et ressources, utilisez l’agenda LGBTQIA+ vivant de Nice Côte d’Azur et le Centre LGBTQIA+ Côte d’Azur ; pour le reste de la soirée, revenez au guide général de Nice. Nous préférons dire clairement où notre couverture est la plus forte plutôt que faire comme si un club masculin représentait tout le monde.</p><p><a href="https://www.explorenicecotedazur.com/evenements/agenda-special-lgbt/" target="_blank" rel="nofollow noopener">Agenda LGBTQIA+ actuel →</a> · <a href="/guide-gay-nice/">Guide local Nice gay →</a></p></section>'''
patch("en/gay-french-riviera/index.html",lambda s:add_before_sources(s,GAY_SCOPE_EN,"gay-scope-queer-women-trans-2026-10-04"))
patch("cote-dazur-gay/index.html",lambda s:add_before_sources(s,GAY_SCOPE_FR,"gay-scope-queer-women-trans-2026-10-04"))

# Validation: fail the build on the credibility regressions this pass is intended to close.
checks=[
 ("en/riviera-guide/nice/index.html",[", ."]),
 ("riviera-guide/nice/index.html",[", .","la meilleur premier","camp de ville uniquement"]),
 ("en/good-finds/ironman-nice/index.html",["2027 date is not yet published","2026 landmarks"]),
 ("bons-plans/ironman-nice/index.html",["date 2027 n’est pas encore publiée","Repères 2026"]),
 ("en/good-finds/index.html",["What deserves attention this month","an exhibition closing soon"]),
 ("bons-plans/index.html",["Ce qui mérite votre attention ce mois-ci","une expo qui ferme bientôt"]),
 ("stay/nice/index.html",["Our new practical pick","New calm pick","answer we were missing"]),
]
for rel,bad in checks:
    p=ROOT/rel
    if p.exists():
        s=p.read_text(encoding="utf-8",errors="ignore")
        for x in bad:
            if x.lower() in s.lower(): raise RuntimeError(f"{rel}: stale credibility string: {x}")

# Structural guard: the late editorial passes must never corrupt HTML around common block tags.
bad_markup=re.compile(r'<</(?:p|h[1-6]|div|span|section|article)>',re.I)
for p in ROOT.rglob("*.html"):
    rel=p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git",".github","scripts","docs","backup"}: continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    if bad_markup.search(s):
        raise RuntimeError(f"{rel}: malformed HTML introduced by editorial cleanup")

# Canonical Plan pages must contain decision depth and dated transport sourcing.
for rel in ("plan/three-days-riviera/index.html","plan/seven-days-riviera/index.html",
            "fr/planifier/trois-jours-cote-d-azur/index.html","fr/planifier/sept-jours-cote-d-azur/index.html"):
    p=ROOT/rel
    if not p.exists(): raise RuntimeError(f"Missing canonical Plan page: {rel}")
    s=p.read_text(encoding="utf-8",errors="ignore")
    for token in ("4 October 2026" if not rel.startswith("fr/") else "4 octobre 2026",
                  "phase4-days-grid","source-box"):
        if token not in s: raise RuntimeError(f"{rel}: missing canonical plan token {token}")

# The last-return guidance belongs on the dedicated solo transport page, not just the hub.
for rel in ("en/solo-female-french-riviera/getting-around-without-a-car/index.html",
            "cote-dazur-femme-solo/se-deplacer-sans-voiture/index.html"):
    p=ROOT/rel
    if not p.exists() or "solo-last-return-2026-10-04" not in p.read_text(encoding="utf-8",errors="ignore"):
        raise RuntimeError(f"{rel}: missing last-return decision layer")

# Hotel hub rule: an editorial hotel name must never be a direct CJ affiliate link.
for rel in ("stay/nice/index.html","fr/dormir/nice/index.html"):
    p=ROOT/rel
    if p.exists():
        s=p.read_text(encoding="utf-8",errors="ignore")
        if re.search(r'<h3><a href="https://www\.kqzyfj\.com',s,re.I):
            raise RuntimeError(f"{rel}: hotel name still links directly to affiliate checkout")
        card_count=len(re.findall(r'<article class="hotel-choice-card"',s,re.I))
        if card_count != 13:
            names=[re.sub(r'<[^>]+>','',x).strip() for x in re.findall(r'<h3>([\s\S]*?)</h3>',s,re.I)]
            raise RuntimeError(f"{rel}: defended shortlist should contain 13 hotel cards; found {card_count}: {names}")

# The formerly thin October pages now need a real practical layer.
for rel in list(HOTEL_EN)+list(HOTEL_FR):
    p=ROOT/rel
    if not p.exists() or "hotel-practical-facts" not in p.read_text(encoding="utf-8",errors="ignore"):
        raise RuntimeError(f"{rel}: hotel practical layer missing")

# Do not reintroduce an unverified pool claim for Hôtel Select.
for rel in ("en/hotels/beaulieu-sur-mer/hotel-select/index.html","hotels/beaulieu-sur-mer/hotel-select/index.html"):
    p=ROOT/rel
    if p.exists():
        body=p.read_text(encoding="utf-8",errors="ignore")
        for stale in ("No pool", "Pas de piscine"):
            if stale in body:
                raise RuntimeError(f"{rel}: unverified Hotel Select pool claim survived")

print("Prescriber credibility gates passed.")
