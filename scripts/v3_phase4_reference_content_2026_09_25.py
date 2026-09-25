#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []

def save(rel: str, text: str, original: str | None = None) -> None:
    p = ROOT / rel
    if original is None:
        original = p.read_text(encoding="utf-8") if p.exists() else ""
    if text != original:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)

def nav(lang: str, active: str) -> str:
    if lang == "fr":
        items=[("plan","/fr/planifier/","Plan"),("places","/riviera-guide/","Destinations"),("stay","/hotels/","Dormir"),("explore","/explore/","Explorer"),("practical","/pratique/","Pratique")]
        aria="Navigation principale"; home="/fr/"
    else:
        items=[("plan","/plan/","Plan"),("places","/en/riviera-guide/","Places"),("stay","/en/hotels/","Stay"),("explore","/en/explore/","Explore"),("practical","/en/practical/","Practical")]
        aria="Primary navigation"; home="/"
    lis=[]
    for key,href,label in items:
        current=' aria-current="page"' if key==active else ''
        lis.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    return f'<header class="v3-header"><div class="v3-header-inner"><a class="v3-brand" href="{home}"><span class="v3-brand-name">Mametas</span><span class="v3-brand-line">They know the Riviera.</span></a><nav class="v3-nav" aria-label="{aria}"><ul>{"".join(lis)}</ul></nav></div></header>'

def footer(lang: str) -> str:
    if lang=="fr":
        return '<footer class="v3-footer"><div class="wrap"><div class="footer-bottom"><span>Sélection éditoriale indépendante · informations pratiques datées quand elles sont périssables.</span><span>© 2026 Mametas</span></div></div></footer>'
    return '<footer class="v3-footer"><div class="wrap"><div class="footer-bottom"><span>Independent editorial selection · changing practical facts are dated when relevant.</span><span>© 2026 Mametas</span></div></div></footer>'

def shell(lang: str, active: str, title: str, desc: str, canonical: str, fr_href: str, en_href: str, body: str) -> str:
    hreflang = f'<link rel="alternate" hreflang="fr" href="https://www.mametas.com{fr_href}"><link rel="alternate" hreflang="en" href="https://www.mametas.com{en_href}"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com{en_href}">'
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="https://www.mametas.com{canonical}">{hreflang}<meta name="robots" content="index,follow,max-image-preview:large"><link rel="stylesheet" href="/assets/v3.css?v=1.5"><link href="/favicon.svg" rel="icon" type="image/svg+xml"><script defer src="/assets/consent.js?v=1.0"></script></head><body>{nav(lang,active)}<main>{body}</main>{footer(lang)}<script src="/assets/v3.js?v=1.0"></script></body></html>'

def sources(items: list[tuple[str,str]], lang: str) -> str:
    label="Sources vérifiées · 25 septembre 2026" if lang=="fr" else "Checked sources · 25 September 2026"
    links=" · ".join(f'<a href="{url}" rel="nofollow noopener" target="_blank">{name}</a>' for name,url in items)
    return f'<div class="source-box phase4-sources"><strong>{label}</strong><br>{links}</div>'

def budget_page(lang: str) -> str:
    if lang=="fr":
        body='''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · BUDGET RÉEL</p><h1>Combien coûte vraiment cinq jours sur la Riviera ?</h1><p class="article-deck">Pas un “prix moyen” qui devient faux dès qu’un congrès arrive. Des enveloppes de planification transparentes, puis les coûts fixes que vous pouvez vérifier.</p><div class="article-meta"><span>Hors vols</span><span>5 nuits</span><span>Par personne, chambre double partagée</span></div></div></header>
<section class="v3-section"><div class="wrap article-body"><div class="verdict"><span class="label">LA RÈGLE</span><p>Le transport n’est généralement pas ce qui fait exploser le budget. L’hôtel, la saison et le nombre de “petits extras” le font beaucoup plus vite.</p></div>
<h2>Trois enveloppes pour planifier, pas trois promesses de prix</h2>
<div class="phase4-budget-grid">
<article><span>€</span><h3>Simple mais bien placé</h3><p><strong>Enveloppe Mametas :</strong> chambre ~160 €/nuit, nourriture ~40 €/jour/personne, transport 35–50 €, activités ~40 €.</p><p class="phase4-total">≈ 675 € / personne pour 5 nuits</p><small>Hypothèse : 2 personnes partagent la chambre. Ce n’est pas une moyenne de marché.</small></article>
<article><span>€€</span><h3>Confortable, sans chasse au centime</h3><p><strong>Enveloppe Mametas :</strong> chambre ~250 €/nuit, nourriture ~70 €/jour/personne, transport 50 €, activités ~95 €.</p><p class="phase4-total">≈ 1 120 € / personne</p><small>Le scénario le plus utile pour un premier séjour confortable.</small></article>
<article><span>€€€</span><h3>L’hôtel fait partie du voyage</h3><p><strong>Enveloppe Mametas :</strong> chambre ~450 €/nuit, nourriture ~120 €/jour/personne, transport 50 €, activités ~245 €.</p><p class="phase4-total">≈ 2 020 € / personne</p><small>Ici, la propriété et les restaurants deviennent des choix de séjour, pas de simples frais.</small></article>
</div>
<p class="ownership-note"><strong>Important :</strong> les montants d’hôtel et de restauration ci-dessus sont des <em>enveloppes de décision</em> Mametas, pas des prix moyens observés. Pour l’hôtel réel, utilisez <a href="/hotels/">Dormir / Hotel Fit</a>. Pour les tarifs transport, les chiffres datés vivent dans <a href="/pratique/">Pratique</a>.</p>
<h2>Les coûts fixes qui peuvent être vérifiés aujourd’hui</h2>
<ul class="phase4-facts"><li><strong>Lignes d’Azur :</strong> Solo 1 voyage 1,70 € ; Pass 1 jour 7 €, 2 jours 13 €, 7 jours 20 €.</li><li><strong>PASS Sud Azur Explore :</strong> 35 € pour 3 jours, 50 € pour 7 jours, 80 € pour 14 jours. Il couvre les réseaux de transport des Alpes-Maritimes et Monaco.</li><li><strong>TER plein tarif depuis Nice :</strong> Antibes 7 €, Cannes 9,70 €, Monaco 6,10 €, Menton 7,70 € par trajet, selon les pages officielles consultées le 25 septembre 2026.</li></ul>
<h2>Ce qu’on oublie presque toujours dans le budget</h2><p>Le transfert aéroport, les plages privées, deux taxis parce qu’on a raté le dernier bus utile, les billets de musée, le verre “juste avant dîner”, les événements qui font grimper les hôtels et la seconde base ajoutée pour gagner une demi-journée. Le bon budget n’est pas celui qui additionne tout au centime : c’est celui qui sait où vous avez décidé de dépenser.</p>
'''+sources([
("Lignes d’Azur · tarifs","https://www.lignesdazur.com/fr/telecharger-le-guide-tarifaire"),
("PASS Sud Azur Explore","https://zou.maregionsud.fr/pass-sud-azur-explore"),
("TER Nice–Cannes","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-cannes"),
("TER Nice–Antibes","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-antibes"),
("TER Nice–Monaco","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-monaco"),
("TER Nice–Menton","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-menton"),
],"fr")+'</div></section>'
        return shell("fr","plan","Budget Côte d’Azur : combien prévoir pour 5 jours ? | Mametas","Budget réaliste pour cinq jours sur la Côte d’Azur : enveloppes transparentes, transports vérifiés et coûts qu’on oublie.","/fr/planifier/budget-reel/","/fr/planifier/budget-reel/","/plan/real-budget/",body)
    body='''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · REAL BUDGET</p><h1>What does five days on the Riviera really cost?</h1><p class="article-deck">Not a fake “average price” that becomes wrong when a congress arrives. Transparent planning envelopes, then the fixed costs you can actually verify.</p><div class="article-meta"><span>Flights excluded</span><span>5 nights</span><span>Per person, sharing a double room</span></div></div></header>
<section class="v3-section"><div class="wrap article-body"><div class="verdict"><span class="label">THE RULE</span><p>Transport is rarely what blows up the budget. Hotel choice, season and the accumulation of small extras do it much faster.</p></div>
<h2>Three planning envelopes, not three price promises</h2>
<div class="phase4-budget-grid">
<article><span>€</span><h3>Simple, well located</h3><p><strong>Mametas envelope:</strong> room ~€160/night, food ~€40/day/person, transport €35–50, activities ~€40.</p><p class="phase4-total">≈ €675 / person for 5 nights</p><small>Assumes two people share the room. This is not a market average.</small></article>
<article><span>€€</span><h3>Comfortable, no penny-counting</h3><p><strong>Mametas envelope:</strong> room ~€250/night, food ~€70/day/person, transport €50, activities ~€95.</p><p class="phase4-total">≈ €1,120 / person</p><small>The most useful planning scenario for a comfortable first trip.</small></article>
<article><span>€€€</span><h3>The hotel is part of the trip</h3><p><strong>Mametas envelope:</strong> room ~€450/night, food ~€120/day/person, transport €50, activities ~€245.</p><p class="phase4-total">≈ €2,020 / person</p><small>Here the property and restaurants are trip choices, not background costs.</small></article>
</div>
<p class="ownership-note"><strong>Important:</strong> hotel and food figures above are Mametas <em>decision envelopes</em>, not observed market averages. Use <a href="/en/hotels/">Stay / Hotel Fit</a> for the live hotel choice. Dated transport detail belongs in <a href="/en/practical/">Practical</a>.</p>
<h2>The fixed costs you can verify today</h2>
<ul class="phase4-facts"><li><strong>Lignes d’Azur:</strong> Solo journey €1.70; 1-day pass €7, 2-day €13, 7-day €20.</li><li><strong>PASS Sud Azur Explore:</strong> €35 for 3 days, €50 for 7 days, €80 for 14 days, covering transport networks across Alpes-Maritimes and Monaco.</li><li><strong>Full-fare TER from Nice:</strong> Antibes €7, Cannes €9.70, Monaco €6.10, Menton €7.70 each way on the official pages checked 25 September 2026.</li></ul>
<h2>The costs almost everyone forgets</h2><p>Airport transfer, private beaches, two taxis because the useful bus has gone, museum tickets, the drink “just before dinner”, event weeks that lift hotel rates, and the second base added to save half a day. A good budget does not predict every euro. It knows where you have decided to spend.</p>
'''+sources([
("Lignes d’Azur fares","https://www.lignesdazur.com/fr/telecharger-le-guide-tarifaire"),
("PASS Sud Azur Explore","https://zou.maregionsud.fr/en/pass-sud-azur-explore"),
("TER Nice–Cannes","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-cannes"),
("TER Nice–Antibes","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-antibes"),
("TER Nice–Monaco","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-monaco"),
("TER Nice–Menton","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-menton"),
],"en")+'</div></section>'
    return shell("en","plan","French Riviera budget: what 5 days really cost | Mametas","A realistic five-day French Riviera budget with transparent planning envelopes and checked transport costs.","/plan/real-budget/","/fr/planifier/budget-reel/","/plan/real-budget/",body)

def car_page(lang: str) -> str:
    if lang=="fr":
        body='''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · VOITURE OU PAS</p><h1>Faut-il vraiment louer une voiture sur la Côte d’Azur ?</h1><p class="article-deck">La bonne réponse n’est pas “oui” ou “non”. Elle dépend de ce que vous voulez voir, de votre base et du nombre de journées où le rail cesse réellement de vous aider.</p></div></header><section class="v3-section"><div class="wrap article-body">
<div class="phase4-decision-table"><div><span>SANS VOITURE</span><h3>Choisissez ça par défaut</h3><p>Nice comme base, 3 à 5 jours, villes côtières, musées, plages accessibles, Monaco, Menton, Antibes, Cannes.</p></div><div><span>1–2 JOURS DE VOITURE</span><h3>Le compromis intelligent</h3><p>Votre séjour reste côtier, mais vous voulez Saint-Paul, Mougins, arrière-pays, plages isolées ou plusieurs villages dans la même journée.</p></div><div><span>VOITURE TOUT LE SÉJOUR</span><h3>Seulement si le voyage l’exige</h3><p>Villa isolée, arrière-pays dominant, horaires tardifs hors axes, plusieurs étapes rurales ou logistique familiale spécifique.</p></div></div>
<h2>Quand la voiture est surtout une charge</h2><p>Pour Nice centre, Cannes centre, Antibes centre et un séjour construit autour du TER, elle ajoute parking, embouteillages et arbitrages de retour. Le réseau côtier rend beaucoup de journées plus simples sans volant.</p>
<h2>Quand elle devient utile</h2><p>Dès que vous quittez la colonne vertébrale ferroviaire, la réponse change : villages de l’intérieur, certaines plages, routes panoramiques, départs de randonnée et journées combinant plusieurs lieux mal reliés entre eux.</p>
<div class="verdict"><span class="label">LA RECO MAMETAS</span><p>Ne louez pas cinq jours de voiture pour résoudre une journée de voiture. Construisez d’abord le séjour sans elle, puis ajoutez 24 ou 48 heures si un vrai morceau du voyage le justifie.</p></div>
<p class="ownership-note"><strong>Plan décide.</strong> Pour les billets, tarifs, parking, location et itinéraires de transport, passez dans <a href="/pratique/">Pratique</a>. Pour choisir un hôtel réellement pratique sans voiture, utilisez <a href="/hotels/sans-voiture/">Dormir sans voiture</a>.</p>
'''+sources([("PASS Sud Azur Explore","https://zou.maregionsud.fr/pass-sud-azur-explore"),("TER Nice–Cannes","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-cannes"),("TER Nice–Monaco","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-monaco"),("Lignes d’Azur","https://www.lignesdazur.com/fr/telecharger-le-guide-tarifaire")],"fr")+'</div></section>'
        return shell("fr","plan","Voiture ou pas sur la Côte d’Azur ? | Mametas","Décider s’il faut louer une voiture sur la Côte d’Azur, selon votre base, vos journées et la part d’arrière-pays.","/fr/planifier/voiture-ou-pas/","/fr/planifier/voiture-ou-pas/","/plan/car-or-no-car/",body)
    body='''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · CAR OR NO CAR</p><h1>Do you actually need a car on the French Riviera?</h1><p class="article-deck">The useful answer is not yes or no. It depends on the base, the trip you want and how many days the railway genuinely stops helping.</p></div></header><section class="v3-section"><div class="wrap article-body">
<div class="phase4-decision-table"><div><span>NO CAR</span><h3>Default to this</h3><p>Nice base, 3–5 days, coastal towns, museums, accessible beaches, Monaco, Menton, Antibes and Cannes.</p></div><div><span>CAR FOR 1–2 DAYS</span><h3>The intelligent compromise</h3><p>Mostly coastal trip, plus Saint-Paul, Mougins, hinterland, isolated beaches or several villages in one day.</p></div><div><span>CAR ALL TRIP</span><h3>Only when the trip demands it</h3><p>Remote villa, hinterland-heavy itinerary, late hours off the main axes, rural multi-stop days or specific family logistics.</p></div></div>
<h2>When the car is mostly baggage</h2><p>In central Nice, Cannes or Antibes, and on a trip built around the TER, a car adds parking, traffic and return-time decisions. The coastal rail spine makes many days simpler without one.</p>
<h2>When it becomes useful</h2><p>Once you leave that rail spine, the answer changes: inland villages, certain beaches, panoramic roads, hiking trailheads and days combining places that are poorly linked to each other.</p>
<div class="verdict"><span class="label">THE MAMETAS CALL</span><p>Do not rent five days of car to solve one car day. Build the trip without it first, then add 24 or 48 hours if a real part of the holiday earns the hassle.</p></div>
<p class="ownership-note"><strong>Plan decides.</strong> For tickets, fares, parking, rental and transport mechanics, use <a href="/en/practical/">Practical</a>. For a genuinely car-free hotel choice, use <a href="/en/hotels/without-a-car/">Stay without a car</a>.</p>
'''+sources([("PASS Sud Azur Explore","https://zou.maregionsud.fr/en/pass-sud-azur-explore"),("TER Nice–Cannes","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-cannes"),("TER Nice–Monaco","https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/trajet-nice-monaco"),("Lignes d’Azur","https://www.lignesdazur.com/fr/telecharger-le-guide-tarifaire")],"en")+'</div></section>'
    return shell("en","plan","Do you need a car on the French Riviera? | Mametas","A decision guide to renting a car on the French Riviera, based on your base, itinerary and inland days.","/plan/car-or-no-car/","/fr/planifier/voiture-ou-pas/","/plan/car-or-no-car/",body)

def season_page(lang: str) -> str:
    if lang=="fr":
        rows=[
            ("NOV–MARS","Ville et culture d’abord","Nice, Menton, Monaco, musées, restaurants. Journées plus courtes ; certaines activités balnéaires deviennent saisonnières.","Très bon si vous ne venez pas chercher une semaine de plage."),
            ("AVR–JUIN","Le meilleur équilibre","Journées longues, excursions faciles, pression moindre qu’en plein été. La baignade n’est pas le même projet en avril et fin juin.","Notre fenêtre préférée pour un premier séjour actif."),
            ("JUIL–AOÛT","Mer, chaleur, pression","Plages et soirées au maximum ; prix, circulation et réservations aussi. Commencez tôt, réservez ce qui compte, acceptez de couper.","Excellent si l’été est le voyage, moins si vous détestez planifier."),
            ("SEP–OCT","La Riviera respire","Mer encore centrale en début de période, rythme plus doux, belles journées possibles. Plus on avance, plus la météo et les horaires saisonniers demandent vérification.","Très forte fenêtre, surtout septembre."),
        ]
        cards="".join(f'<article><span>{a}</span><h3>{b}</h3><p>{c}</p><strong>{d}</strong></article>' for a,b,c,d in rows)
        body=f'''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · QUAND PARTIR</p><h1>La bonne saison dépend du voyage que vous voulez.</h1><p class="article-deck">La Côte d’Azur n’a pas une “meilleure période” universelle. Elle a des compromis différents entre mer, chaleur, prix, lumière, foule et horaires saisonniers.</p></div></header><section class="v3-section"><div class="wrap article-body"><div class="phase4-season-grid">{cards}</div><div class="verdict"><span class="label">MAMETAS</span><p>Pour un premier séjour de 3 à 7 jours où vous voulez réellement bouger, mai–juin et septembre sont les fenêtres les plus faciles à recommander. Juillet–août fonctionnent très bien si vous assumez que la plage, la chaleur et la réservation font partie du produit.</p></div><h2>Ce que Riviera Fit fait de cette information</h2><p>La saison n’est pas un décor. Elle modifie la base recommandée, la friction et ce qu’il vaut mieux couper. C’est pour cela qu’elle fait partie des cinq critères de Riviera Fit.</p><p class="ownership-note">Pour la météo concrète et les fermetures datées, consultez <a href="/pratique/">Pratique</a> et <a href="/bons-plans/">En ce moment</a>. Cette page reste volontairement une décision de voyage, pas une prévision météo.</p></div></section>'''
        return shell("fr","plan","Quand partir sur la Côte d’Azur ? | Mametas","Quand partir sur la Côte d’Azur selon votre type de séjour : printemps, été, automne ou hiver, avec les compromis réels.","/fr/planifier/quand-partir/","/fr/planifier/quand-partir/","/plan/when-to-go/",body)
    rows=[
        ("NOV–MAR","City and culture first","Nice, Menton, Monaco, museums and restaurants. Shorter days; some beach operations become seasonal.","Very good if you are not chasing a beach week."),
        ("APR–JUN","Best balance","Longer days, easy day trips and less pressure than peak summer. Swimming is a different proposition in April and late June.","Our easiest window for an active first trip."),
        ("JUL–AUG","Sea, heat, pressure","Beaches and evenings at full volume; prices, traffic and booking pressure too. Start early, reserve what matters, cut the rest.","Excellent if summer is the trip, less so if you hate planning."),
        ("SEP–OCT","The Riviera exhales","Sea remains central early in the period, pace softens, good days are common. Later on, weather and seasonal operations need checking.","A very strong window, especially September."),
    ]
    cards="".join(f'<article><span>{a}</span><h3>{b}</h3><p>{c}</p><strong>{d}</strong></article>' for a,b,c,d in rows)
    body=f'''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · WHEN TO GO</p><h1>The right season depends on the trip you want.</h1><p class="article-deck">The French Riviera does not have one universal “best time”. It has different trade-offs between sea, heat, price, light, crowds and seasonal operations.</p></div></header><section class="v3-section"><div class="wrap article-body"><div class="phase4-season-grid">{cards}</div><div class="verdict"><span class="label">MAMETAS</span><p>For a first 3–7 day trip where you actually want to move around, May–June and September are the easiest windows to recommend. July–August work very well if beach, heat and booking pressure are part of the product you want.</p></div><h2>What Riviera Fit does with this</h2><p>Season is not decoration. It can change the recommended base, friction and what should be cut. That is why it is one of Riviera Fit’s five criteria.</p><p class="ownership-note">For concrete weather and dated closures, use <a href="/en/practical/">Practical</a> and <a href="/en/good-finds/">Right Now</a>. This page is a trip decision, not a forecast.</p></div></section>'''
    return shell("en","plan","When to go to the French Riviera | Mametas","When to visit the French Riviera by trip type, with the real trade-offs of spring, summer, autumn and winter.","/plan/when-to-go/","/fr/planifier/quand-partir/","/plan/when-to-go/",body)

def itinerary_page(lang: str, days: int) -> str:
    assert days in (3,7)
    if lang=="fr":
        if days==3:
            title="Trois jours sur la Côte d’Azur : coupez, ne compressez pas."
            days_html='''<article><span>JOUR 1</span><h3>Nice d’abord</h3><p>Vieux-Nice, Colline du Château, bord de mer. Comprenez votre base avant de prendre le premier TER venu.</p></article><article><span>JOUR 2</span><h3>Villefranche + Cap-Ferrat</h3><p>La journée “beauté et respiration”. Si vous préférez spectacle et institutions, remplacez-la par Monaco, pas par Monaco + Menton + Èze.</p></article><article><span>JOUR 3</span><h3>Antibes</h3><p>Vieille ville, musée Picasso si vous aimez vraiment Picasso, Gravette et remparts. Retour à Nice pour le dernier soir.</p></article>'''
            verdict="Trois jours ne sont pas une version miniature de sept jours. Gardez une base et trois ambiances."
            desc="Itinéraire de 3 jours sur la Côte d’Azur depuis Nice, sans voiture et sans programme compressé."
            canonical="/fr/planifier/trois-jours-cote-d-azur/"
            en="/plan/three-days-riviera/"
        else:
            title="Sept jours sur la Côte d’Azur : ajoutez de l’air, pas des cases."
            days_html='''<article><span>JOUR 1</span><h3>Nice</h3><p>Vieux-Nice, Château, mer, dîner. Aucun train aujourd’hui.</p></article><article><span>JOUR 2</span><h3>Villefranche + Cap-Ferrat</h3><p>Baie, vieille ville, une seule vraie balade ou Villa Ephrussi. Pas tout.</p></article><article><span>JOUR 3</span><h3>Monaco</h3><p>Le Rocher, puis un choix : Musée océanographique ou Monte-Carlo. Une journée plus nette que deux demi-journées mélangées.</p></article><article><span>JOUR 4</span><h3>Menton</h3><p>Vieille ville, Saint-Michel, Sablettes, rythme plus doux. C’est le jour qui décompresse l’est.</p></article><article><span>JOUR 5</span><h3>Antibes</h3><p>Vieille ville, Picasso, Gravette. Le contrepoint ouest sans basculer dans la collection de villes.</p></article><article><span>JOUR 6</span><h3>Choisissez une direction</h3><p>Cannes + Lérins si vous voulez sable et mer ; Saint-Paul + Maeght si vous voulez art et intérieur.</p></article><article><span>JOUR 7</span><h3>Nice lentement</h3><p>Cimiez, Port, plage ou déjeuner long. Le jour qu’on oublie toujours de prévoir et qu’on apprécie le plus.</p></article>'''
            verdict="Une semaine permet d’ajouter une direction, pas de rendre obligatoires toutes les directions."
            desc="Itinéraire de 7 jours sur la Côte d’Azur depuis Nice, avec un rythme réaliste et des alternatives."
            canonical="/fr/planifier/sept-jours-cote-d-azur/"
            en="/plan/seven-days-riviera/"
        body=f'''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · {days} JOURS</p><h1>{title}</h1><p class="article-deck">Une base à Nice, pas de voiture par défaut, et une seule vraie ambiance dominante par journée.</p></div></header><section class="v3-section"><div class="wrap article-body"><div class="phase4-days-grid">{days_html}</div><div class="verdict"><span class="label">LA RÈGLE</span><p>{verdict}</p></div><p class="ownership-note">Pour un séjour de cinq jours, utilisez le <a href="/fr/planifier/cinq-jours-nice-sans-voiture/">parcours complet Nice sans voiture</a>. Pour changer de base, passez par <a href="/riviera-fit/">Riviera Fit</a>.</p></div></section>'''
        return shell("fr","plan",title+" | Mametas",desc,canonical,canonical,en,body)
    if days==3:
        title="Three days on the Riviera: cut, do not compress."
        days_html='''<article><span>DAY 1</span><h3>Nice first</h3><p>Old Nice, Castle Hill, the sea. Learn the base before taking the first TER out of it.</p></article><article><span>DAY 2</span><h3>Villefranche + Cap-Ferrat</h3><p>The beauty-and-breathing day. If you prefer spectacle and institutions, swap it for Monaco, not Monaco + Menton + Èze.</p></article><article><span>DAY 3</span><h3>Antibes</h3><p>Old town, Picasso if Picasso actually matters to you, Gravette and ramparts. Back to Nice for the last evening.</p></article>'''
        verdict="Three days are not a miniature seven-day trip. Keep one base and three distinct moods."
        desc="A realistic 3-day French Riviera itinerary from Nice, without a car and without compressed sightseeing."
        canonical="/plan/three-days-riviera/"; fr="/fr/planifier/trois-jours-cote-d-azur/"
    else:
        title="Seven days on the Riviera: add air, not boxes."
        days_html='''<article><span>DAY 1</span><h3>Nice</h3><p>Old Nice, Castle Hill, sea, dinner. No train today.</p></article><article><span>DAY 2</span><h3>Villefranche + Cap-Ferrat</h3><p>Bay, old town, one real walk or Villa Ephrussi. Not everything.</p></article><article><span>DAY 3</span><h3>Monaco</h3><p>The Rock, then one choice: Oceanographic Museum or Monte-Carlo. One clear day beats two muddled half-days.</p></article><article><span>DAY 4</span><h3>Menton</h3><p>Old town, Saint-Michel, Sablettes, slower pace. The day that decompresses the east.</p></article><article><span>DAY 5</span><h3>Antibes</h3><p>Old town, Picasso, Gravette. The western counterpoint without turning the trip into town collecting.</p></article><article><span>DAY 6</span><h3>Choose one direction</h3><p>Cannes + Lérins for sand and sea; Saint-Paul + Maeght for art and inland character.</p></article><article><span>DAY 7</span><h3>Slow Nice</h3><p>Cimiez, Port, beach or a long lunch. The day people forget to plan and are happiest to have.</p></article>'''
        verdict="A week lets you add one direction. It does not make every direction compulsory."
        desc="A realistic 7-day French Riviera itinerary from Nice, with a manageable pace and clear alternatives."
        canonical="/plan/seven-days-riviera/"; fr="/fr/planifier/sept-jours-cote-d-azur/"
    body=f'''<header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN · {days} DAYS</p><h1>{title}</h1><p class="article-deck">One Nice base, no car by default, and one dominant mood per day.</p></div></header><section class="v3-section"><div class="wrap article-body"><div class="phase4-days-grid">{days_html}</div><div class="verdict"><span class="label">THE RULE</span><p>{verdict}</p></div><p class="ownership-note">For five days, use the full <a href="/plan/five-days-nice-no-car/">Nice no-car plan</a>. To change the base, use <a href="/en/riviera-fit/">Riviera Fit</a>.</p></div></section>'''
    return shell("en","plan",title+" | Mametas",desc,canonical,fr,canonical,body)

def short_routes(lang: str) -> str:
    if lang=="fr":
        routes=[
            ("nice","Nice","2 h 30","Cours Saleya → Vieux-Nice → Colline du Château → Port","Commencez au marché/Cours Saleya, traversez le Vieux-Nice, montez au Château, redescendez côté Port. Si vous n’avez que 2 h, coupez le Port.","Premier aperçu de Nice","Montée au Château ; ascenseur possible selon horaires.","https://www.explorenicecotedazur.com/explorer/villes-villages/nice-la-capitale-de-la-cote-dazur/"),
            ("cannes","Cannes","3 h","Forville → Le Suquet → Place de la Castre → Vieux Port → Croisette","Le marché le matin si ouvert, puis la vieille ville avant de finir sur le port et la Croisette. C’est plus intéressant dans cet ordre que l’inverse.","Première visite courte","Forville est actuellement ouvert mardi–dimanche 7 h–13 h ; sinon commencez au Suquet.","https://www.cannes-france.com/que-faire/en-3-heures/"),
            ("antibes","Antibes","2 h 30","Gare → vieille ville → musée Picasso → remparts → Gravette","Si vous entrez au musée Picasso, faites-en le vrai temps fort du créneau. Si vous voulez surtout marcher, restez dehors et gardez les remparts + Gravette.","Vieille ville + culture","Le musée transforme la balade en visite culturelle ; ne le faites pas par réflexe.","https://www.antibesjuanlespins.com/decouvrir/les-incontournables/le-musee-picasso"),
            ("villefranche","Villefranche-sur-Mer","2 h","Gare → vieille ville → Rue Obscure → Citadelle → port → Marinières","Une boucle compacte entre ruelles, patrimoine et eau. Ne construisez pas le créneau autour du musée de la Citadelle : ses salles sont actuellement fermées pour rénovation.","Beauté sans journée entière","Escaliers et dénivelé léger à modéré.","https://www.explorenicecotedazur.com/explorer/villes-villages/littoral/villefranche-sur-mer/"),
            ("menton","Menton","2 h 30","Biovès → vieille ville → basilique Saint-Michel → Sablettes","Montez progressivement vers Saint-Michel, prenez le point de vue, redescendez vers la mer. Si vous avez 30 minutes de plus, prolongez vers le Bastion/Cocteau.","Couleur + vieille ville","La pente vers Saint-Michel est le seul vrai effort.","https://www.menton-riviera-merveilles.fr/menton-et-le-littoral/nos-incontournables/vieille-ville-de-menton/"),
            ("monaco","Monaco","2 h 30","Place d’Armes → Rocher → Palais → Cathédrale → jardins Saint-Martin → Musée océanographique extérieur","Le Rocher tient dans 2–3 h si vous restez dehors. Si vous entrez au Musée océanographique, faites-en le programme principal : VisitMonaco indique environ 3 h pour le musée seul.","Le Monaco historique","Ne mélangez pas Rocher + musée complet + Casino dans le même créneau.","https://www.visitmonaco.com/fr/parcours-et-balades/26633/parcours-famille"),
            ("saint-paul","Saint-Paul-de-Vence","2 h","Place de Gaulle → rue Grande → remparts → cimetière → retour village","Deux heures suffisent pour le village si vous flânez sans ajouter la Fondation Maeght. Si Maeght est votre priorité, donnez-lui le créneau : la visite moyenne annoncée est d’environ 90 minutes.","Village + atmosphère","Village + Fondation en 2 h = mauvais plan.","https://www.saint-pauldevence.com/fiches/musees-et-lieux-de-visites/fondation-maeght/"),
            ("eze","Èze","2–3 h","Village → ruelles → jardin / point de vue → église","Si vous arrivez directement au village, 2 h suffisent pour une vraie visite. Si vous partez d’Èze-sur-Mer, le chemin de Nietzsche mesure 2,1 km avec environ 350–400 m de dénivelé et demande 1 h à 1 h 30 rien que pour la montée.","Village perché","Le chemin de Nietzsche consomme une grosse partie du créneau ; ne faites pas comme s’il était un simple accès.","https://www.explorenicecotedazur.com/itineraire/chemin-de-nietzsche/"),
        ]
        title="Vous n’avez que 2 ou 3 heures ? Très bien."
        deck="Un créneau court n’est pas une demi-journée ratée. C’est souvent le meilleur antidote au programme trop ambitieux. Voici huit parcours qui tiennent réellement dans le temps annoncé."
        route_label="PARCOURS"; best="IDÉAL POUR"; catch="LE PIÈGE"; checked="Source officielle"
        canonical="/explore/2-3-heures/"; en="/en/explore/2-3-hours/"
    else:
        routes=[
            ("nice","Nice","2h30","Cours Saleya → Old Nice → Castle Hill → Port","Start around Cours Saleya, cross Old Nice, climb Castle Hill, descend toward the Port. If you only have 2 hours, cut the Port.","First look at Nice","Castle Hill climb; lift may be available depending on opening times.","https://www.explorenicecotedazur.com/explorer/villes-villages/nice-la-capitale-de-la-cote-dazur/"),
            ("cannes","Cannes","3h","Forville → Le Suquet → Place de la Castre → Old Port → Croisette","Use the market in the morning if open, then do the old town before finishing at the port and Croisette. It is more interesting in that order.","Short first visit","Forville is currently Tue–Sun 7am–1pm; otherwise start at Le Suquet.","https://www.cannes-france.com/que-faire/en-3-heures/"),
            ("antibes","Antibes","2h30","Station → old town → Picasso Museum → ramparts → Gravette","If you go inside the Picasso Museum, make it the real centre of the slot. If you mainly want the walk, stay outside and keep the ramparts + Gravette.","Old town + culture","The museum turns this into a culture visit. Do not enter by reflex.","https://www.antibesjuanlespins.com/decouvrir/les-incontournables/le-musee-picasso"),
            ("villefranche","Villefranche-sur-Mer","2h","Station → old town → Rue Obscure → Citadel → harbour → Marinières","A compact loop through lanes, heritage and water. Do not build the slot around the Citadel museum: its museum rooms are currently closed for renovation.","Beauty without a full day","Steps and light-to-moderate gradients.","https://www.explorenicecotedazur.com/explorer/villes-villages/littoral/villefranche-sur-mer/"),
            ("menton","Menton","2h30","Biovès → old town → Saint-Michel → Sablettes","Climb gradually to Saint-Michel, take the viewpoint, then come down toward the sea. With 30 minutes more, extend toward the Bastion/Cocteau.","Colour + old town","The climb to Saint-Michel is the only real effort.","https://www.menton-riviera-merveilles.fr/menton-et-le-littoral/nos-incontournables/vieille-ville-de-menton/"),
            ("monaco","Monaco","2h30","Place d’Armes → Rock → Palace → Cathedral → Saint-Martin gardens → Oceanographic Museum exterior","The Rock fits 2–3 hours if you stay outside. If you enter the Oceanographic Museum, make that the main programme: VisitMonaco gives about 3 hours for the museum alone.","Historic Monaco","Do not combine the Rock + full museum + Casino in the same slot.","https://www.visitmonaco.com/fr/parcours-et-balades/26633/parcours-famille"),
            ("saint-paul","Saint-Paul-de-Vence","2h","Place de Gaulle → Rue Grande → ramparts → cemetery → village","Two hours works for the village if you do not add Fondation Maeght. If Maeght is the priority, give it the slot: the official average visit is about 90 minutes.","Village + atmosphere","Village + Fondation in 2 hours is a bad plan.","https://www.saint-pauldevence.com/fiches/musees-et-lieux-de-visites/fondation-maeght/"),
            ("eze","Èze","2–3h","Village → lanes → garden / viewpoint → church","If you arrive at the village, two hours is enough for a real visit. From Èze-sur-Mer, the Nietzsche path is 2.1 km with roughly 350–400 m ascent and takes about 1–1.5 hours just to climb.","Perched village","The Nietzsche path consumes a large part of the slot. It is not a casual access path.","https://www.explorenicecotedazur.com/itineraire/chemin-de-nietzsche/"),
        ]
        title="Only got 2 or 3 hours? Good."
        deck="A short window is not a failed half-day. It is often the best antidote to an overpacked itinerary. These eight routes actually fit the time advertised."
        route_label="ROUTE"; best="BEST FOR"; catch="THE CATCH"; checked="Official source"
        canonical="/en/explore/2-3-hours/"; en=canonical
    cards=[]
    for slug,name,time,route,copy,bestfor,trap,url in routes:
        cards.append(f'''<article class="phase4-short-route" id="{slug}"><div class="phase4-short-route-head"><span>{time}</span><h2>{name}</h2></div><p class="phase4-route-line"><strong>{route_label}</strong> · {route}</p><p>{copy}</p><div class="phase4-route-meta"><p><b>{best}</b><br>{bestfor}</p><p><b>{catch}</b><br>{trap}</p></div><p class="phase4-source-link"><a href="{url}" target="_blank" rel="nofollow noopener">{checked} →</a></p></article>''')
    body=f'''<header class="article-hero"><div class="wrap"><p class="eyebrow">EXPLORE · 2–3 HOURS</p><h1>{title}</h1><p class="article-deck">{deck}</p><div class="article-meta"><span>8 parcours</span><span>Pas de voiture nécessaire par défaut</span><span>Temps réel, pas temps brochure</span></div></div></header><section class="v3-section"><div class="wrap phase4-short-routes">{"".join(cards)}</div></section>''' if lang=="fr" else f'''<header class="article-hero"><div class="wrap"><p class="eyebrow">EXPLORE · 2–3 HOURS</p><h1>{title}</h1><p class="article-deck">{deck}</p><div class="article-meta"><span>8 routes</span><span>No car by default</span><span>Real time, not brochure time</span></div></div></header><section class="v3-section"><div class="wrap phase4-short-routes">{"".join(cards)}</div></section>'''
    if lang=="fr":
        return shell("fr","explore","Que faire en 2 ou 3 heures sur la Côte d’Azur ? | Mametas","Huit balades et visites de 2 à 3 heures réellement faisables à Nice, Cannes, Antibes, Menton, Monaco, Villefranche, Saint-Paul et Èze.",canonical,canonical,en,body)
    return shell("en","explore","What to do in 2 or 3 hours on the French Riviera | Mametas","Eight realistic 2–3 hour routes in Nice, Cannes, Antibes, Menton, Monaco, Villefranche, Saint-Paul and Èze.",canonical,"/explore/2-3-heures/",canonical,body)

def climate_page(lang: str) -> str:
    if lang=="fr":
        body='''<header class="article-hero"><div class="wrap"><p class="eyebrow">PRATIQUE · CLIMAT</p><h1>La météo décide du plan B, pas de la valeur du séjour.</h1><p class="article-deck">Le climat général aide à choisir la saison. Pour la météo de cette semaine, regardez une prévision actuelle et Right Now, pas une moyenne annuelle.</p></div></header><section class="v3-section"><div class="wrap article-body"><h2>Printemps</h2><p>Très bon pour marcher, visiter et rayonner. La mer n’est pas encore l’argument principal au début de la saison ; prévoyez une vraie couche pour le soir.</p><h2>Été</h2><p>Chaleur, forte lumière, baignade et pression touristique. Les journées de marche longue gagnent à commencer tôt ; les lieux réservables gagnent à être réservés.</p><h2>Automne</h2><p>Septembre reste très orienté mer. Plus tard, la météo devient plus variable : gardez une activité intérieure ou urbaine prête à remplacer une journée plage.</p><h2>Hiver</h2><p>Nice, Menton et Monaco restent des bases urbaines crédibles. En revanche, certaines activités balnéaires et adresses saisonnières réduisent leur fonctionnement.</p><p class="ownership-note">Pour décider <em>quand partir</em>, revenez dans <a href="/fr/planifier/quand-partir/">Plan</a>. Pour une alerte datée ou une fermeture du mois, consultez <a href="/bons-plans/">En ce moment</a>.</p></div></section>'''
        return shell("fr","practical","Climat Côte d’Azur par saison | Mametas","Climat pratique de la Côte d’Azur par saison, avec ce que cela change réellement dans votre programme.","/pratique/climat-saisons/","/pratique/climat-saisons/","/en/practical/weather-by-season/",body)
    body='''<header class="article-hero"><div class="wrap"><p class="eyebrow">PRACTICAL · WEATHER</p><h1>Weather decides the backup plan, not the value of the trip.</h1><p class="article-deck">General climate helps choose the season. For this week’s weather, use a current forecast and Right Now, not an annual average.</p></div></header><section class="v3-section"><div class="wrap article-body"><h2>Spring</h2><p>Strong for walking, culture and day trips. The sea is not yet the main argument early in the season; keep a real evening layer.</p><h2>Summer</h2><p>Heat, strong light, swimming and visitor pressure. Long walking days work better early; reservable places work better when actually reserved.</p><h2>Autumn</h2><p>September remains strongly sea-oriented. Later, weather becomes more variable: keep an indoor or urban alternative ready to replace a beach day.</p><h2>Winter</h2><p>Nice, Menton and Monaco remain credible urban bases. Some beach operations and seasonal addresses reduce or pause service.</p><p class="ownership-note">To decide <em>when to go</em>, return to <a href="/plan/when-to-go/">Plan</a>. For a dated alert or current closure, use <a href="/en/good-finds/">Right Now</a>.</p></div></section>'''
    return shell("en","practical","French Riviera weather by season | Mametas","Practical French Riviera weather by season, focused on what it changes in a real itinerary.","/en/practical/weather-by-season/","/pratique/climat-saisons/","/en/practical/weather-by-season/",body)

def patch_plan_hub(rel: str, lang: str) -> None:
    p=ROOT/rel
    text=p.read_text(encoding="utf-8"); original=text
    if lang=="fr":
        block='''<section class="v3-section phase4-plan-depth"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">ALLER PLUS LOIN</p><h2>Plan doit répondre avant que Google ne le fasse mal.</h2></div><p>Durée, saison, voiture, budget. Quatre décisions qui structurent réellement un séjour de 3 à 7 jours.</p></div><div class="phase4-plan-grid"><a href="/fr/planifier/trois-jours-cote-d-azur/"><span>3 JOURS</span><strong>Coupez, ne compressez pas.</strong></a><a href="/fr/planifier/cinq-jours-nice-sans-voiture/"><span>5 JOURS</span><strong>Le parcours de référence sans voiture.</strong></a><a href="/fr/planifier/sept-jours-cote-d-azur/"><span>7 JOURS</span><strong>Ajoutez de l’air, pas des cases.</strong></a><a href="/fr/planifier/voiture-ou-pas/"><span>VOITURE ?</span><strong>Décidez avant de louer.</strong></a><a href="/fr/planifier/quand-partir/"><span>SAISON</span><strong>Quand venir selon le voyage voulu.</strong></a><a href="/fr/planifier/budget-reel/"><span>BUDGET</span><strong>Ce que cinq jours coûtent vraiment.</strong></a></div></div></section>'''
    else:
        block='''<section class="v3-section phase4-plan-depth"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">GO DEEPER</p><h2>Plan should answer before Google answers badly.</h2></div><p>Duration, season, car, budget. Four decisions that genuinely shape a 3–7 day trip.</p></div><div class="phase4-plan-grid"><a href="/plan/three-days-riviera/"><span>3 DAYS</span><strong>Cut, do not compress.</strong></a><a href="/plan/five-days-nice-no-car/"><span>5 DAYS</span><strong>The reference no-car route.</strong></a><a href="/plan/seven-days-riviera/"><span>7 DAYS</span><strong>Add air, not boxes.</strong></a><a href="/plan/car-or-no-car/"><span>CAR?</span><strong>Decide before you rent.</strong></a><a href="/plan/when-to-go/"><span>SEASON</span><strong>When to come for the trip you want.</strong></a><a href="/plan/real-budget/"><span>BUDGET</span><strong>What five days really cost.</strong></a></div></div></section>'''
    if "phase4-plan-depth" not in text:
        marker='</main>'
        pos=text.rfind(marker)
        if pos<0: raise RuntimeError(f"{rel}: main close not found")
        text=text[:pos]+block+text[pos:]
    save(rel,text,original)

def patch_explore_hub(rel: str, lang: str) -> None:
    p=ROOT/rel; text=p.read_text(encoding="utf-8"); original=text
    if lang=="fr":
        block='''<section class="v3-section phase4-short-entry"><div class="wrap"><div class="phase4-short-entry-inner"><div><p class="eyebrow">2 OU 3 HEURES</p><h2>Un petit créneau mérite mieux qu’une recherche au hasard.</h2><p>Nice, Cannes, Antibes, Menton, Monaco, Villefranche, Saint-Paul, Èze : huit parcours réellement dimensionnés pour deux ou trois heures.</p></div><a class="button" href="/explore/2-3-heures/">Ouvrir les parcours courts</a></div></div></section>'''
    else:
        block='''<section class="v3-section phase4-short-entry"><div class="wrap"><div class="phase4-short-entry-inner"><div><p class="eyebrow">2 OR 3 HOURS</p><h2>A short window deserves better than random searching.</h2><p>Nice, Cannes, Antibes, Menton, Monaco, Villefranche, Saint-Paul, Èze: eight routes genuinely sized for two or three hours.</p></div><a class="button" href="/en/explore/2-3-hours/">Open the short routes</a></div></div></section>'''
    if "phase4-short-entry" not in text:
        # Put it after the main category doors, before later editorial content.
        sec=list(re.finditer(r'<section\b[^>]*>.*?</section>',text,flags=re.S))
        if not sec: raise RuntimeError(f"{rel}: no sections")
        insert_after=sec[1].end() if len(sec)>1 else sec[0].end()
        text=text[:insert_after]+block+text[insert_after:]
    save(rel,text,original)

def patch_practical_hub(rel: str, lang: str) -> None:
    p=ROOT/rel; text=p.read_text(encoding="utf-8"); original=text
    href="/pratique/climat-saisons/" if lang=="fr" else "/en/practical/weather-by-season/"
    label="Climat par saison →" if lang=="fr" else "Weather by season →"
    if href not in text:
        marker='</section>'
        pos=text.find(marker)
        if pos>=0:
            text=text[:pos]+f'<p class="phase4-practical-extra"><a href="{href}">{label}</a></p>'+text[pos:]
    save(rel,text,original)

def css() -> None:
    p=ROOT/"assets/v3.css"; text=p.read_text(encoding="utf-8"); original=text
    marker="/* V3 phase 4 reference content 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 phase 4 reference content 2026-09-25 */
.phase4-budget-grid,.phase4-decision-table,.phase4-season-grid,.phase4-days-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:24px 0 34px}
.phase4-budget-grid article,.phase4-decision-table>div,.phase4-season-grid article,.phase4-days-grid article{padding:22px;border:1px solid var(--line);background:rgba(255,255,255,.32)}
.phase4-budget-grid span,.phase4-decision-table span,.phase4-season-grid span,.phase4-days-grid span{color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}
.phase4-budget-grid h3,.phase4-decision-table h3,.phase4-season-grid h3,.phase4-days-grid h3{margin:12px 0 9px;font-family:var(--serif);font-size:27px;font-weight:500;line-height:1.05}
.phase4-budget-grid p,.phase4-decision-table p,.phase4-season-grid p,.phase4-days-grid p{color:var(--ink-soft);font-size:12px;line-height:1.6}
.phase4-budget-grid small{display:block;margin-top:12px;color:var(--ink-soft);font-size:9px;line-height:1.5}
.phase4-total{margin-top:14px!important;color:var(--ink)!important;font-family:var(--serif);font-size:24px!important}
.phase4-facts{display:grid;gap:10px;margin:20px 0;padding:0;list-style:none}
.phase4-facts li{padding:15px 17px;border-left:3px solid var(--blue);background:rgba(23,54,95,.04);font-size:12px;line-height:1.6}
.phase4-season-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
.phase4-season-grid article strong{display:block;margin-top:15px;font-size:10px;line-height:1.5}
.phase4-days-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.phase4-plan-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.phase4-plan-grid a{display:flex;min-height:128px;padding:18px;flex-direction:column;justify-content:space-between;border:1px solid var(--line);background:rgba(255,255,255,.25);text-decoration:none}
.phase4-plan-grid span{color:var(--coral);font-size:8px;font-weight:800;letter-spacing:.12em}
.phase4-plan-grid strong{font-family:var(--serif);font-size:22px;font-weight:500;line-height:1.05}
.phase4-short-entry{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(23,54,95,.035)}
.phase4-short-entry-inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:35px;align-items:end}
.phase4-short-entry h2{max-width:14ch;margin:6px 0 10px;font-family:var(--serif);font-size:clamp(34px,4vw,52px);font-weight:500;line-height:1}
.phase4-short-entry p:not(.eyebrow){max-width:720px;color:var(--ink-soft);font-size:12px;line-height:1.6}
.phase4-short-routes{display:grid;gap:14px}
.phase4-short-route{padding:24px;border:1px solid var(--line);background:rgba(255,255,255,.24)}
.phase4-short-route-head{display:flex;justify-content:space-between;gap:20px;align-items:baseline}
.phase4-short-route-head span{color:var(--coral);font-size:10px;font-weight:800;letter-spacing:.12em}
.phase4-short-route-head h2{margin:0;font-family:var(--serif);font-size:clamp(30px,4vw,46px);font-weight:500}
.phase4-route-line{margin:16px 0!important;padding:10px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.phase4-route-meta{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.phase4-route-meta p{padding:13px;background:rgba(23,54,95,.035);font-size:11px;line-height:1.5}
.phase4-source-link{margin-top:12px!important;font-size:9px!important;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.phase4-sources{margin-top:32px}
.phase4-practical-extra{margin:22px 0 0;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
@media(max-width:900px){.phase4-budget-grid,.phase4-decision-table,.phase4-season-grid,.phase4-plan-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.phase4-short-entry-inner{grid-template-columns:1fr}}
@media(max-width:620px){.phase4-budget-grid,.phase4-decision-table,.phase4-season-grid,.phase4-days-grid,.phase4-plan-grid,.phase4-route-meta{grid-template-columns:1fr}}
'''
    save("assets/v3.css",text,original)


def patch_sitemap() -> None:
    p=ROOT/"sitemap.xml"
    if not p.exists(): return
    text=p.read_text(encoding="utf-8"); original=text
    urls=[
        "/plan/real-budget/","/fr/planifier/budget-reel/",
        "/plan/car-or-no-car/","/fr/planifier/voiture-ou-pas/",
        "/plan/when-to-go/","/fr/planifier/quand-partir/",
        "/plan/three-days-riviera/","/fr/planifier/trois-jours-cote-d-azur/",
        "/plan/seven-days-riviera/","/fr/planifier/sept-jours-cote-d-azur/",
        "/en/explore/2-3-hours/","/explore/2-3-heures/",
        "/en/practical/weather-by-season/","/pratique/climat-saisons/"
    ]
    additions=""
    for path in urls:
        url="https://www.mametas.com"+path
        if f"<loc>{url}</loc>" not in text:
            additions += f'  <url><loc>{url}</loc><lastmod>2026-09-25</lastmod></url>\n'
    if additions:
        text=text.replace("</urlset>",additions+"</urlset>")
    save("sitemap.xml",text,original)

def validate() -> None:
    checks={
        "plan/real-budget/index.html":("PASS Sud Azur Explore","€675","€2,020"),
        "fr/planifier/budget-reel/index.html":("PASS Sud Azur Explore","675 €","2 020 €"),
        "plan/car-or-no-car/index.html":("CAR FOR 1–2 DAYS","Practical"),
        "fr/planifier/voiture-ou-pas/index.html":("1–2 JOURS DE VOITURE","Pratique"),
        "plan/when-to-go/index.html":("APR–JUN","SEP–OCT"),
        "fr/planifier/quand-partir/index.html":("AVR–JUIN","SEP–OCT"),
        "plan/three-days-riviera/index.html":("DAY 1","DAY 3"),
        "fr/planifier/trois-jours-cote-d-azur/index.html":("JOUR 1","JOUR 3"),
        "plan/seven-days-riviera/index.html":("DAY 7","Choose one direction"),
        "fr/planifier/sept-jours-cote-d-azur/index.html":("JOUR 7","Choisissez une direction"),
        "en/explore/2-3-hours/index.html":("Only got 2 or 3 hours? Good.","Villefranche-sur-Mer","Èze"),
        "explore/2-3-heures/index.html":("Vous n’avez que 2 ou 3 heures ? Très bien.","Villefranche-sur-Mer","Èze"),
        "en/practical/weather-by-season/index.html":("Spring","Winter"),
        "pratique/climat-saisons/index.html":("Printemps","Hiver"),
        "plan/index.html":("phase4-plan-depth","real-budget"),
        "fr/planifier/index.html":("phase4-plan-depth","budget-reel"),
        "en/explore/index.html":("phase4-short-entry","/en/explore/2-3-hours/"),
        "explore/index.html":("phase4-short-entry","/explore/2-3-heures/"),
    }
    errors=[]
    for rel,needles in checks.items():
        p=ROOT/rel
        if not p.exists():
            errors.append(f"{rel}: missing"); continue
        text=p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text: errors.append(f"{rel}: missing {needle!r}")
    if "V3 phase 4 reference content 2026-09-25" not in (ROOT/"assets/v3.css").read_text(encoding="utf-8"):
        errors.append("assets/v3.css: phase4 CSS missing")
    if errors:
        raise SystemExit("V3 phase 4 failed:\n- "+"\n- ".join(errors))

def main() -> int:
    save("plan/real-budget/index.html",budget_page("en"))
    save("fr/planifier/budget-reel/index.html",budget_page("fr"))
    save("plan/car-or-no-car/index.html",car_page("en"))
    save("fr/planifier/voiture-ou-pas/index.html",car_page("fr"))
    save("plan/when-to-go/index.html",season_page("en"))
    save("fr/planifier/quand-partir/index.html",season_page("fr"))
    save("plan/three-days-riviera/index.html",itinerary_page("en",3))
    save("fr/planifier/trois-jours-cote-d-azur/index.html",itinerary_page("fr",3))
    save("plan/seven-days-riviera/index.html",itinerary_page("en",7))
    save("fr/planifier/sept-jours-cote-d-azur/index.html",itinerary_page("fr",7))
    save("en/explore/2-3-hours/index.html",short_routes("en"))
    save("explore/2-3-heures/index.html",short_routes("fr"))
    save("en/practical/weather-by-season/index.html",climate_page("en"))
    save("pratique/climat-saisons/index.html",climate_page("fr"))
    patch_plan_hub("plan/index.html","en")
    patch_plan_hub("fr/planifier/index.html","fr")
    patch_explore_hub("en/explore/index.html","en")
    patch_explore_hub("explore/index.html","fr")
    patch_practical_hub("en/practical/index.html","en")
    patch_practical_hub("pratique/index.html","fr")
    css()
    patch_sitemap()
    validate()
    print(f"V3 phase 4 passed; changed {len(changed)} file(s).")
    for rel in sorted(changed): print(rel)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
