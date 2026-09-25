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


def nav_html(lang: str, active: str = "") -> str:
    if lang == "fr":
        items = [
            ("plan", "/fr/planifier/", "Plan"),
            ("places", "/riviera-guide/", "Destinations"),
            ("stay", "/hotels/", "Dormir"),
            ("explore", "/explore/", "Explorer"),
            ("practical", "/pratique/", "Pratique"),
        ]
        aria = "Navigation principale"
    else:
        items = [
            ("plan", "/plan/", "Plan"),
            ("places", "/en/riviera-guide/", "Places"),
            ("stay", "/en/hotels/", "Stay"),
            ("explore", "/en/explore/", "Explore"),
            ("practical", "/en/practical/", "Practical"),
        ]
        aria = "Primary navigation"
    lis = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for key, href, label in items
    )
    return f'<nav class="v3-nav" aria-label="{aria}"><ul>{lis}</ul></nav>'


def header(lang: str, active: str, fr_href: str, en_href: str) -> str:
    is_fr = lang == "fr"
    home = "/fr/" if is_fr else "/"
    brand_aria = "Mametas, accueil" if is_fr else "Mametas, home"
    lang_aria = "Langue" if is_fr else "Language"
    open_label = "Ouvrir le menu" if is_fr else "Open menu"
    return (
        f'<header class="v3-header"><div class="v3-header-inner">'
        f'<a class="v3-brand" href="{home}" aria-label="{brand_aria}"><span class="v3-brand-name">Mametas</span>'
        f'<span class="v3-brand-line">They know the Riviera.</span></a>'
        f'{nav_html(lang, active)}'
        f'<div class="lang-switch" aria-label="{lang_aria}">'
        f'<a href="{fr_href}"{" aria-current=\"page\"" if is_fr else ""}>FR</a><span>/</span>'
        f'<a href="{en_href}"{" aria-current=\"page\"" if not is_fr else ""}>EN</a></div>'
        f'<button class="menu-button" type="button" aria-label="{open_label}" data-v3-menu-open>'
        f'<span></span><span></span><span></span></button></div></header>'
    )


def footer(lang: str) -> str:
    if lang == "fr":
        return '''<footer class="v3-footer"><div class="wrap"><div class="footer-grid"><div class="footer-brand"><span class="v3-brand-name">Mametas</span><p>Des décisions Riviera indépendantes, avec les options inutiles en moins.</p></div><div class="footer-col"><h2>Décider</h2><a href="/fr/planifier/">Plan</a><a href="/riviera-fit/">Riviera Fit</a><a href="/hotels/">Dormir</a></div><div class="footer-col"><h2>Comprendre</h2><a href="/riviera-guide/">Destinations</a><a href="/explore/">Explorer</a><a href="/pratique/">Pratique</a></div></div><div class="footer-bottom"><span>Sélection éditoriale indépendante.</span><span>© 2026 Mametas</span></div></div></footer>'''
    return '''<footer class="v3-footer"><div class="wrap"><div class="footer-grid"><div class="footer-brand"><span class="v3-brand-name">Mametas</span><p>Independent Riviera decisions, with the unnecessary options removed.</p></div><div class="footer-col"><h2>Decide</h2><a href="/plan/">Plan</a><a href="/en/riviera-fit/">Riviera Fit</a><a href="/en/hotels/">Stay</a></div><div class="footer-col"><h2>Understand</h2><a href="/en/riviera-guide/">Places</a><a href="/en/explore/">Explore</a><a href="/en/practical/">Practical</a></div></div><div class="footer-bottom"><span>Independent editorial selection.</span><span>© 2026 Mametas</span></div></div></footer>'''


def plan_page(lang: str) -> str:
    if lang == "fr":
        return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Planifier un séjour sur la Côte d’Azur | Mametas</title><meta name="description" content="Construire un séjour sur la Côte d’Azur : choisir la bonne base avec Riviera Fit, décider voiture ou non et partir d’itinéraires réalistes."><link rel="canonical" href="https://www.mametas.com/fr/planifier/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/fr/planifier/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/plan/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/plan/"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="stylesheet" href="/assets/v3.css?v=1.4"><link href="/favicon.svg" rel="icon" type="image/svg+xml"><script defer src="/assets/consent.js?v=1.0"></script></head><body><a class="skip-link" href="#main">Aller au contenu</a>{header("fr","plan","/fr/planifier/","/plan/")}<main id="main"><header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN</p><h1>Construisez le voyage avant de remplir les journées.</h1><p class="article-deck">La première décision n’est pas le musée du mardi. C’est la base, le rythme, la saison et la quantité de logistique que vous avez réellement envie de supporter.</p><div class="article-meta"><span>3 à 7 jours</span><span>Base avant hôtel</span><span>Voiture seulement si elle aide</span></div></div></header><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">COMMENCEZ ICI</p><h2>Les décisions qui enlèvent des options.</h2></div><p>Plan n’est pas un itinéraire géant. C’est l’endroit où l’on tranche les choix qui changent tout le reste du séjour.</p></div><div class="architecture-grid"><a class="architecture-card architecture-card--tool" href="/riviera-fit/"><span>MAMETAS TOOL</span><h3>Riviera Fit</h3><p>Cinq critères : durée, saison, mobilité, priorité et rythme. Une base recommandée, les compromis compris.</p><b>Tester Riviera Fit →</b></a><a class="architecture-card" href="/fr/planifier/cinq-jours-nice-sans-voiture/"><span>5 JOURS</span><h3>Nice sans voiture</h3><p>Un séjour réaliste avec une seule base, des excursions qui tiennent debout et aucune chorégraphie de valises.</p><b>Ouvrir le parcours →</b></a><a class="architecture-card" href="/hotels/sans-voiture/"><span>VOITURE ?</span><h3>Décider avant de louer.</h3><p>La côte se fait très bien sans voiture. L’arrière-pays et certaines plages changent la réponse.</p><b>Voir la logique →</b></a><a class="architecture-card" href="/riviera-guide/"><span>ENCORE UN DOUTE ?</span><h3>Comprendre les destinations.</h3><p>Nice, Cannes, Antibes, Villefranche, Menton ou Monaco : ce que chaque base donne et ce qu’elle vous fait accepter.</p><b>Ouvrir Destinations →</b></a></div></div></section><section class="v3-section architecture-next"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">BASE CHOISIE ?</p><h2>Plan a fini son travail.</h2></div><p>Passez à l’hôtel, aux journées ou à la logistique. Pas besoin de suivre Mametas dans un ordre imposé.</p></div><div class="decision-grid"><a class="decision-card" href="/hotels/"><span class="decision-number">01</span><h3>Dormir</h3><p>Hotel Fit et les hôtels par base.</p><span class="text-link">Choisir l’hôtel →</span></a><a class="decision-card" href="/explore/"><span class="decision-number">02</span><h3>Explorer</h3><p>Culture, plages, restaurants et excursions.</p><span class="text-link">Remplir les journées →</span></a><a class="decision-card" href="/pratique/"><span class="decision-number">03</span><h3>Pratique</h3><p>Transports, arrivée, billets et réservations.</p><span class="text-link">Régler la logistique →</span></a></div></div></section></main>{footer("fr")}<script src="/assets/v3.js?v=1.0"></script></body></html>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan a French Riviera trip | Mametas</title><meta name="description" content="Plan a French Riviera trip by choosing the right base with Riviera Fit, deciding whether you need a car and starting from realistic itineraries."><link rel="canonical" href="https://www.mametas.com/plan/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/fr/planifier/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/plan/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/plan/"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="stylesheet" href="/assets/v3.css?v=1.4"><link href="/favicon.svg" rel="icon" type="image/svg+xml"><script defer src="/assets/consent.js?v=1.0"></script></head><body><a class="skip-link" href="#main">Skip to content</a>{header("en","plan","/fr/planifier/","/plan/")}<main id="main"><header class="article-hero"><div class="wrap"><p class="eyebrow">PLAN</p><h1>Build the trip before you fill the days.</h1><p class="article-deck">The first decision is not Tuesday’s museum. It is the base, pace, season and amount of logistics you actually want to live with.</p><div class="article-meta"><span>3 to 7 days</span><span>Base before hotel</span><span>Car only when it helps</span></div></div></header><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">START HERE</p><h2>The decisions that remove options.</h2></div><p>Plan is not one enormous itinerary. It is where Mametas settles the choices that change everything else.</p></div><div class="architecture-grid"><a class="architecture-card architecture-card--tool" href="/en/riviera-fit/"><span>MAMETAS TOOL</span><h3>Riviera Fit</h3><p>Five criteria: duration, season, mobility, priority and pace. One recommended base, trade-offs included.</p><b>Try Riviera Fit →</b></a><a class="architecture-card" href="/plan/five-days-nice-no-car/"><span>5 DAYS</span><h3>Nice without a car</h3><p>One realistic base, day trips that hold together and no heroic luggage choreography.</p><b>Open the plan →</b></a><a class="architecture-card" href="/en/hotels/without-a-car/"><span>CAR?</span><h3>Decide before you rent.</h3><p>The coast works remarkably well without a car. Inland villages and certain beaches change the answer.</p><b>See the logic →</b></a><a class="architecture-card" href="/en/riviera-guide/"><span>STILL UNSURE?</span><h3>Understand the places.</h3><p>Nice, Cannes, Antibes, Villefranche, Menton or Monaco: what each base gives you and what it makes you accept.</p><b>Open Places →</b></a></div></div></section><section class="v3-section architecture-next"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">BASE SORTED?</p><h2>Plan has done its job.</h2></div><p>Move to the hotel, the days or the logistics. You do not need to follow Mametas in a compulsory order.</p></div><div class="decision-grid"><a class="decision-card" href="/en/hotels/"><span class="decision-number">01</span><h3>Stay</h3><p>Hotel Fit and hotels by base.</p><span class="text-link">Choose the hotel →</span></a><a class="decision-card" href="/en/explore/"><span class="decision-number">02</span><h3>Explore</h3><p>Culture, beaches, restaurants and day trips.</p><span class="text-link">Fill the days →</span></a><a class="decision-card" href="/en/practical/"><span class="decision-number">03</span><h3>Practical</h3><p>Transport, arrival, tickets and booking rules.</p><span class="text-link">Sort the logistics →</span></a></div></div></section></main>{footer("en")}<script src="/assets/v3.js?v=1.0"></script></body></html>'''


def practical_page(lang: str) -> str:
    if lang == "fr":
        return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pratique Côte d’Azur : transports, arrivée, réservations | Mametas</title><meta name="description" content="Le pratique Mametas pour la Côte d’Azur : aéroport, train, bus, tram, réservations et plans de repli quand la météo change."><link rel="canonical" href="https://www.mametas.com/pratique/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/pratique/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/en/practical/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/en/practical/"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="stylesheet" href="/assets/v3.css?v=1.4"><link href="/favicon.svg" rel="icon" type="image/svg+xml"><script defer src="/assets/consent.js?v=1.0"></script></head><body><a class="skip-link" href="#main">Aller au contenu</a>{header("fr","practical","/pratique/","/en/practical/")}<main id="main"><header class="article-hero"><div class="wrap"><p class="eyebrow">PRATIQUE</p><h1>Faites fonctionner le voyage sans cagade.</h1><p class="article-deck">Ici vivent les détails qui changent : billets, transports, arrivée, réservations et plans de repli. Les pages destination peuvent les résumer. Les chiffres à jour vivent ici par défaut.</p></div></header><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">LES ESSENTIELS</p><h2>Réglez la mécanique. Puis oubliez-la.</h2></div><p>Des guides courts, sourcés et datés pour les décisions qui deviennent pénibles lorsqu’on les découvre sur le quai.</p></div><div class="architecture-grid practical-architecture-grid"><a class="architecture-card" href="/bons-plans/transfert-aeroport-nice/"><span>ARRIVÉE</span><h3>Aéroport vers votre base</h3><p>Tram, Saint-Augustin, TER, cars directs et taxi.</p><b>Régler l’arrivée →</b></a><a class="architecture-card" href="/bons-plans/train-ou-bus/"><span>TRANSPORT</span><h3>Train ou bus ?</h3><p>TER côtier, tram, ZOU!, billets et pass utiles.</p><b>Choisir le transport →</b></a><a class="architecture-card" href="/bons-plans/que-reserver/"><span>RÉSERVATIONS</span><h3>Que faut-il réserver ?</h3><p>Plages privées, bateaux, musées et ce qui peut attendre.</p><b>Voir les règles →</b></a><a class="architecture-card" href="/bons-plans/nice-quand-il-pleut/"><span>MÉTÉO</span><h3>Nice quand il pleut</h3><p>Un plan de repli concret pour ne pas sacrifier la journée.</p><b>Sauver la journée →</b></a></div></div></section><section class="v3-section right-now-bridge"><div class="wrap"><div class="right-now-bridge-inner"><div><p class="eyebrow">RIGHT NOW</p><h2>Le pratique change. Le calendrier aussi.</h2><p>Événements, affluence, fermetures et informations du mois restent dans une couche séparée du contenu pérenne.</p></div><a class="button secondary" href="/bons-plans/septembre-2026/">Voir ce qui se passe maintenant</a></div></div></section></main>{footer("fr")}<script src="/assets/v3.js?v=1.0"></script></body></html>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>French Riviera practical guide: transport, arrival, booking | Mametas</title><meta name="description" content="Mametas practical guide to the French Riviera: airport transfers, trains, buses, trams, booking rules and useful backup plans."><link rel="canonical" href="https://www.mametas.com/en/practical/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/pratique/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/en/practical/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/en/practical/"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="stylesheet" href="/assets/v3.css?v=1.4"><link href="/favicon.svg" rel="icon" type="image/svg+xml"><script defer src="/assets/consent.js?v=1.0"></script></head><body><a class="skip-link" href="#main">Skip to content</a>{header("en","practical","/pratique/","/en/practical/")}<main id="main"><header class="article-hero"><div class="wrap"><p class="eyebrow">PRACTICAL</p><h1>Make the trip work without the cagades.</h1><p class="article-deck">This is where changing details live: tickets, transport, arrival, booking rules and backup plans. Destination pages may summarise them. Current operational detail lives here by default.</p></div></header><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">THE ESSENTIALS</p><h2>Sort the mechanics. Then forget about them.</h2></div><p>Short, sourced and dated guides for the decisions that become irritating when you discover them on the platform.</p></div><div class="architecture-grid practical-architecture-grid"><a class="architecture-card" href="/en/good-finds/nice-airport-transfer/"><span>ARRIVAL</span><h3>Airport to your base</h3><p>Tram, Saint-Augustin, TER, airport coaches and taxi.</p><b>Solve arrival →</b></a><a class="architecture-card" href="/en/good-finds/train-or-bus/"><span>TRANSPORT</span><h3>Train or bus?</h3><p>Coastal TER, tram, ZOU!, tickets and useful passes.</p><b>Choose transport →</b></a><a class="architecture-card" href="/en/good-finds/what-to-book/"><span>BOOKING</span><h3>What should you book?</h3><p>Private beaches, boats, museums and what can safely wait.</p><b>See the rules →</b></a><a class="architecture-card" href="/en/good-finds/nice-in-the-rain/"><span>WEATHER</span><h3>Nice in the rain</h3><p>A concrete backup plan so the day does not disappear with the sun.</p><b>Save the day →</b></a></div></div></section><section class="v3-section right-now-bridge"><div class="wrap"><div class="right-now-bridge-inner"><div><p class="eyebrow">RIGHT NOW</p><h2>Practical facts change. So does the calendar.</h2><p>Events, crowd pressure, closures and monthly notes stay in a separate temporal layer rather than being mixed into evergreen guidance.</p></div><a class="button secondary" href="/en/good-finds/september-2026/">See what matters right now</a></div></div></section></main>{footer("en")}<script src="/assets/v3.js?v=1.0"></script></body></html>'''


def rebuild_fr_places() -> None:
    cards = [
        ("nice","/assets/editorial/nice-riviera.jpg","Nice","Meilleure première base.","Transport, restaurants, culture et une vraie ville après dîner."),
        ("villefranche-cap-ferrat","/assets/editorial/villefranche.jpg","Villefranche & Cap-Ferrat","Pour la beauté et le calme.","Moins de choix, beaucoup plus de raisons de ralentir."),
        ("antibes","/assets/editorial/antibes-gravette.jpg","Antibes","Meilleur équilibre.","Vieille ville, sable et gare utile sans le spectacle cannois."),
        ("cannes","/assets/editorial/cannes-suquet-harbour.jpg","Cannes","Pour la plage et le vernis.","Compacte, sableuse et sérieuse sur le rôle de l’hôtel."),
        ("monaco","/assets/editorial/monaco-harbour.jpg","Monaco","Quand Monaco est le voyage.","Excursion facile, base chère, spectacle très efficace."),
        ("menton","/assets/editorial/menton-day.jpg","Menton","Pour l’est plus calme.","Plus douce, plus lente, presque italienne."),
    ]
    main_cards = "".join(f'<a class="place-card" href="/riviera-guide/{slug}/"><div class="place-card-media"><img src="{img}" alt="{name}" loading="lazy"></div><h3>{name}</h3><p><strong>{best}</strong> {desc}</p></a>' for slug,img,name,best,desc in cards)
    detours = [
        ("eze","/assets/editorial/eze-village.jpg","Èze","Pour le panorama.","Petit, raide, spectaculaire. L’heure d’arrivée compte presque autant que la vue."),
        ("saint-paul-de-vence","/assets/editorial/saint-paul-de-vence.jpg","Saint-Paul-de-Vence","Pour l’art dans les terres.","Remparts, galeries et Fondation Maeght."),
        ("saint-tropez","/assets/editorial/saint-tropez.jpg","Saint-Tropez","Quand vous le voulez vraiment.","Une vraie expédition, pas un ajout désinvolte avant dîner."),
    ]
    detour_cards = "".join(f'<a class="place-card" href="/riviera-guide/{slug}/"><div class="place-card-media"><img src="{img}" alt="{name}" loading="lazy"></div><h3>{name}</h3><p><strong>{best}</strong> {desc}</p></a>' for slug,img,name,best,desc in detours)
    html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Destinations Côte d’Azur : quelle base vous correspond ? | Mametas</title><meta name="description" content="Nice, Cannes, Antibes, Villefranche, Monaco, Menton : comprendre les bases de la Côte d’Azur, leurs forces, leurs compromis et quand choisir autre chose."><link rel="canonical" href="https://www.mametas.com/riviera-guide/"><link rel="alternate" hreflang="fr" href="https://www.mametas.com/riviera-guide/"><link rel="alternate" hreflang="en" href="https://www.mametas.com/en/riviera-guide/"><link rel="alternate" hreflang="x-default" href="https://www.mametas.com/en/riviera-guide/"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="stylesheet" href="/assets/v3.css?v=1.4"><link href="/favicon.svg" rel="icon" type="image/svg+xml"><script defer src="/assets/consent.js?v=1.0"></script></head><body><a class="skip-link" href="#main">Aller au contenu</a>{header("fr","places","/riviera-guide/","/en/riviera-guide/")}<main id="main"><header class="article-hero"><div class="wrap"><p class="eyebrow">COMPRENDRE LA BASE</p><h1>La Riviera, ville par ville. Compromis compris.</h1><p class="article-deck">Riviera Fit peut choisir une base. Destinations explique pourquoi ce choix fonctionne, quand il ne fonctionne pas et ce que les autres villes changent réellement.</p><div class="article-meta"><span>Premier séjour · Nice reste sûre</span><span>Sans voiture · très réaliste</span><span>Chaque base a son prix à payer</span></div></div></header><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">COMMENT LES BASES DIFFÈRENT</p><h2>Même côte. Pas le même séjour.</h2></div><p>Une base ne gagne pas parce qu’elle est la plus belle sur une photo. Elle gagne parce qu’elle rend plus simples les journées que vous voulez réellement vivre.</p></div><div class="place-grid">{main_cards}</div></div></section><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">QUITTER LA LIGNE PRINCIPALE</p><h2>Trois détours qui changent le voyage.</h2></div><p>Ils demandent un peu plus de logistique. Ils la méritent quand l’envie est la bonne.</p></div><div class="place-grid">{detour_cards}</div></div></section><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">ENCORE EN TRAIN D’HÉSITER ?</p><h2>Laissez Plan enlever des options.</h2></div><p>Comprendre les villes est utile. Les comparer pendant trois soirées l’est beaucoup moins.</p></div><div class="decision-grid"><a class="decision-card" href="/riviera-guide/nice-ou-cannes/"><span class="decision-number">01</span><h3>Nice ou Cannes ?</h3><p>Ville contre vernis, galets contre sable, centre du réseau contre biais ouest.</p><span class="text-link">Comparer →</span></a><a class="decision-card" href="/fr/planifier/"><span class="decision-number">02</span><h3>Sans voiture ?</h3><p>Plan possède la décision macro. Le train fait souvent plus de travail que les brochures ne l’admettent.</p><span class="text-link">Ouvrir Plan →</span></a><a class="decision-card" href="/fr/planifier/cinq-jours-nice-sans-voiture/"><span class="decision-number">03</span><h3>Cinq jours ?</h3><p>Une base à Nice, plusieurs ambiances et aucune chorégraphie de valises.</p><span class="text-link">Ouvrir le parcours →</span></a></div></div></section><section class="v3-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">LA BASE TIENT TOUJOURS ?</p><h2>Très bien. Arrêtez de comparer les villes.</h2></div><p>Passez à l’hôtel, aux activités ou à la logistique. Vous pouvez aussi revenir à Riviera Fit si quelque chose ne colle plus.</p></div><div class="decision-grid"><a class="decision-card" href="/hotels/"><span class="decision-number">01</span><h3>Choisir l’hôtel</h3><p>Hotel Fit et navigation par base.</p><span class="text-link">Dormir →</span></a><a class="decision-card" href="/explore/"><span class="decision-number">02</span><h3>Remplir les journées</h3><p>Culture, plages, restaurants et excursions.</p><span class="text-link">Explorer →</span></a><a class="decision-card" href="/pratique/"><span class="decision-number">03</span><h3>Régler la logistique</h3><p>Transports, arrivée, billets et réservations.</p><span class="text-link">Pratique →</span></a></div></div></section></main>{footer("fr")}<script src="/assets/v3.js?v=1.0"></script></body></html>'''
    save("riviera-guide/index.html", html)


def patch_en_places() -> None:
    rel = "en/riviera-guide/index.html"
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = text.replace('<p class="eyebrow">Choose the base before the hotel</p>', '<p class="eyebrow">UNDERSTAND THE BASE</p>')
    text = text.replace('<h1>The Riviera, by the trip you want.</h1>', '<h1>The Riviera, town by town. Trade-offs included.</h1>')
    text = text.replace('Nice, Villefranche, Antibes, Cannes, Monaco and Menton share a railway line and very little personality. Choose what you want the holiday to feel like before opening the booking tabs.', 'Riviera Fit can choose a base. Places explains why that choice works, when it does not, and what the other towns would actually change.')
    text = text.replace('<p class="eyebrow">The main decision</p>', '<p class="eyebrow">HOW THE BASES DIFFER</p>')
    text = text.replace('href="/en/hotels/without-a-car/"><span class="decision-number">02</span><h3>Without a car?</h3>', 'href="/plan/"><span class="decision-number">02</span><h3>Without a car?</h3>')
    text = text.replace('<span class="text-link">See the logic →</span>', '<span class="text-link">Open Plan →</span>', 1)
    save(rel, text, original)


BASES = [
    ("nice","Nice","/assets/editorial/nice-riviera.jpg","Best all-round first base","Meilleure première base"),
    ("antibes","Antibes / Juan-les-Pins","/assets/editorial/antibes-gravette.jpg","Old town + sand","Vieille ville + sable"),
    ("cannes","Cannes","/assets/editorial/cannes-suquet-harbour.jpg","Beach + polish","Plage + vernis"),
    ("villefranche","Villefranche / Cap-Ferrat","/assets/editorial/villefranche.jpg","Beauty + slower pace","Beauté + rythme lent"),
    ("monaco","Monaco","/assets/editorial/monaco-harbour.jpg","Stay for the spectacle","Dormir pour le spectacle"),
    ("menton","Menton","/assets/editorial/menton-day.jpg","Quiet eastern base","Base calme à l’est"),
    ("saint-paul","Saint-Paul-de-Vence","/assets/editorial/saint-paul-de-vence.jpg","Art inland","Art dans les terres"),
    ("beaulieu","Beaulieu-sur-Mer","/assets/hotels/v3/la-reserve-de-beaulieu/hero.jpg","Calm + train-friendly","Calme + train facile"),
    ("mougins","Mougins","/assets/editorial/mougins-village.jpg","Village retreat","Retraite village"),
    ("saint-tropez","Saint-Tropez","/assets/editorial/saint-tropez.jpg","Deliberate destination","Destination assumée"),
]


def section_spans(text: str):
    for m in re.finditer(r'<section\b[^>]*>.*?</section>', text, flags=re.S):
        yield m


def replace_section_containing(text: str, needle: str, replacement: str) -> tuple[str, bool]:
    for m in section_spans(text):
        if needle in m.group(0):
            return text[:m.start()] + replacement + text[m.end():], True
    return text, False


def patch_stay_hub(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    cards = []
    for base, name, img, en_tag, fr_tag in BASES:
        href = f"/hotels/finder/?base={base}" if lang == "fr" else f"/en/hotels/finder/?base={base}"
        tag = fr_tag if lang == "fr" else en_tag
        cards.append(
            f'<a class="stay-base-card" href="{href}"><img src="{img}" alt="{name}" loading="lazy">'
            f'<span class="stay-base-shade"></span><span class="stay-base-copy"><small>{tag}</small><strong>{name}</strong>'
            f'<em>{"Voir les hôtels →" if lang == "fr" else "Browse hotels →"}</em></span></a>'
        )
    if lang == "fr":
        block = f'''<section class="v3-section stay-base-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">PAR BASE</p><h2>Vous savez où dormir ? Entrez par la ville.</h2></div><p>Chaque carte ouvre Hotel Fit avec la base déjà fixée. Vous pouvez parcourir toute la sélection de la ville ou ajouter ensuite vos critères.</p></div><div class="stay-base-grid">{"".join(cards)}</div></div></section>'''
        needles = ("Choisissez votre base", "Choisir sa base")
    else:
        block = f'''<section class="v3-section stay-base-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">BY BASE</p><h2>Know the town? Enter through the place.</h2></div><p>Each card opens Hotel Fit with the base already set. Browse the full selection for that town, or add your criteria from there.</p></div><div class="stay-base-grid">{"".join(cards)}</div></div></section>'''
        needles = ("Choose your base",)
    done = False
    for needle in needles:
        text2, ok = replace_section_containing(text, needle, block)
        if ok:
            text, done = text2, True
            break
    if not done:
        marker = '<section class="v3-section hotel-finder-entry'
        pos = text.find(marker)
        if pos >= 0:
            end = text.find('</section>', pos)
            if end >= 0:
                end += len('</section>')
                text = text[:end] + block + text[end:]
                done = True
    if not done:
        raise RuntimeError(f"{rel}: base navigation section not found")
    save(rel, text, original)


def patch_hotel_fit_boundary(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace("1 · Où voulez-vous dormir ?", "1 · Dans quelle base dormez-vous ?")
        gate = '<p class="engine-base-gate">Hotel Fit commence quand la géographie est réglée. Vous hésitez encore entre les villes ? <a href="/riviera-fit/">Commencez par Riviera Fit →</a></p>'
        label = "Je ne sais pas encore"
    else:
        text = text.replace("1 · Where do you want to stay?", "1 · Which base are you staying in?")
        gate = '<p class="engine-base-gate">Hotel Fit starts once geography is settled. Still deciding between towns? <a href="/en/riviera-fit/">Start with Riviera Fit →</a></p>'
        label = "Not sure yet"
    field = re.search(r'<fieldset><legend>1 · .*?</legend>(.*?)</fieldset>', text, flags=re.S)
    if field:
        whole = field.group(0)
        whole = re.sub(
            rf'<button[^>]+data-engine-group="base"[^>]+data-engine-choice="any"[^>]*>{re.escape(label)}</button>',
            "",
            whole,
            count=1,
        )
        if 'engine-base-gate' not in whole:
            whole = whole.replace("</legend>", "</legend>" + gate, 1)
        text = text[:field.start()] + whole + text[field.end():]
    text = re.sub(r"/assets/hotel-engine\.js\?v=\d+", "/assets/hotel-engine.js?v=10", text)
    save(rel, text, original)


def patch_explore(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    text = re.sub(r'<section class="v3-section practical explore-practical">.*?</section>', "", text, count=1, flags=re.S)
    heading = "Commencez où vous voulez." if lang == "fr" else "Start anywhere."
    text, _ = replace_section_containing(text, f"<h2>{heading}</h2>", "")
    if lang == "fr":
        text = text.replace("Mametas peut vous dire où vous poser et quoi réserver. Il peut aussi vous laisser tranquille.", "Mametas peut vous aider à choisir la base et l’hôtel. Ici, il vous laisse respirer.")
    else:
        text = text.replace("Mametas can tell you where to base yourself and what to book. It can also get out of the way.", "Mametas can help you choose the base and hotel. Here, it gets out of the way.")
    save(rel, text, original)


def patch_riviera_fit(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if 'class="tool-badge"' not in text:
        if lang == "fr":
            text = text.replace('<p class="eyebrow">MAMETAS RIVIERA FIT · LA RECO</p>', '<p class="tool-badge">MAMETAS TOOL</p><p class="eyebrow">RIVIERA FIT · LA RECO</p>')
        else:
            text = text.replace('<p class="eyebrow">MAMETAS RIVIERA FIT · THE CALL</p>', '<p class="tool-badge">MAMETAS TOOL</p><p class="eyebrow">RIVIERA FIT · THE CALL</p>')
    save(rel, text, original)


def patch_home(rel: str, lang: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if lang == "fr":
        text = text.replace("Lancer le Riviera Chooser", "Tester Riviera Fit")
        text = text.replace("Riviera Chooser", "Riviera Fit")
    else:
        text = text.replace("Start the Riviera Chooser", "Try Riviera Fit")
        text = text.replace("Riviera Chooser", "Riviera Fit")
    save(rel, text, original)


def patch_css() -> None:
    p = ROOT / "assets/v3.css"
    text = p.read_text(encoding="utf-8")
    original = text
    marker = "/* V3 architecture phase 2 2026-09-25 */"
    if marker not in text:
        text += r'''

/* V3 architecture phase 2 2026-09-25 */
.architecture-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.architecture-card{display:block;min-height:230px;padding:24px;border:1px solid var(--line);background:rgba(255,253,248,.7);text-decoration:none;transition:transform .18s ease,border-color .18s ease,background .18s ease}
.architecture-card:hover,.architecture-card:focus-visible{transform:translateY(-2px);border-color:rgba(23,54,95,.35);background:var(--white)}
.architecture-card>span{display:block;margin-bottom:22px;color:var(--coral);font-size:9px;font-weight:800;letter-spacing:.15em;text-transform:uppercase}
.architecture-card h3{margin:0 0 10px;font-family:var(--serif);font-size:clamp(27px,3vw,36px);font-weight:500;line-height:1.02}
.architecture-card p{max-width:560px;margin:0 0 20px;color:var(--ink-soft);font-size:12px;line-height:1.65}
.architecture-card b{font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.architecture-card--tool{background:var(--blue);border-color:var(--blue);color:var(--white)}
.architecture-card--tool>span,.architecture-card--tool b{color:#f7c966}
.architecture-card--tool p{color:rgba(255,255,255,.76)}
.architecture-next{border-top:1px solid var(--line)}
.right-now-bridge{border-top:1px solid var(--line);background:rgba(23,54,95,.035)}
.right-now-bridge-inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:30px;align-items:end}
.right-now-bridge-inner h2{margin:6px 0 10px;font-family:var(--serif);font-size:clamp(32px,4vw,46px);font-weight:500}
.right-now-bridge-inner p:not(.eyebrow){max-width:720px;margin:0;color:var(--ink-soft);font-size:13px;line-height:1.65}
.stay-base-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.stay-base-card{position:relative;display:block;min-height:205px;overflow:hidden;background:var(--blue-deep);color:#fff;text-decoration:none}
.stay-base-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .3s ease}
.stay-base-card:hover img,.stay-base-card:focus-visible img{transform:scale(1.035)}
.stay-base-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,17,35,.08) 18%,rgba(8,17,35,.82) 100%)}
.stay-base-copy{position:absolute;left:0;right:0;bottom:0;padding:17px;z-index:2}
.stay-base-copy small{display:block;margin-bottom:5px;color:#f7c966;font-size:8px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.stay-base-copy strong{display:block;font-family:var(--serif);font-size:23px;font-weight:500;line-height:1}
.stay-base-copy em{display:block;margin-top:10px;font:700 8px/1.3 var(--sans);font-style:normal;letter-spacing:.08em;text-transform:uppercase}
.tool-badge,.hotel-fit-launch-label{display:inline-flex!important;width:auto!important;align-items:center;padding:6px 9px;border:1px solid rgba(199,91,61,.45);border-radius:999px;background:rgba(199,91,61,.06);color:var(--coral)!important;font-size:8px!important;font-weight:800!important;letter-spacing:.14em!important;text-transform:uppercase}
.engine-base-gate{margin:0 0 12px!important;padding:10px 12px;border-left:2px solid var(--coral);background:rgba(199,91,61,.04);color:var(--ink-soft)!important;font-size:10px!important;line-height:1.5!important}
.engine-base-gate a{font-weight:700;text-decoration:underline;text-underline-offset:3px}
#riviera-first-trip-edit .first-trip-card{min-height:132px;padding:17px 19px 15px}
#riviera-first-trip-edit .first-trip-card h3{margin-bottom:7px}
#riviera-first-trip-edit .first-trip-card p{line-height:1.48}
@media(max-width:1180px){.stay-base-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:820px){.architecture-grid{grid-template-columns:1fr}.right-now-bridge-inner{grid-template-columns:1fr}.stay-base-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.stay-base-grid{grid-template-columns:1fr}.stay-base-card{min-height:175px}}
'''
    save("assets/v3.css", text, original)

    p2 = ROOT / "assets/riviera-chooser.css"
    c = p2.read_text(encoding="utf-8")
    orig = c
    marker2 = "/* V3 architecture compact Riviera Fit 2026-09-25 */"
    if marker2 not in c:
        c += r'''

/* V3 architecture compact Riviera Fit 2026-09-25 */
.chooser-page-intro{margin-bottom:26px}
.chooser-engine{gap:0;border:1px solid var(--line);background:rgba(255,253,248,.35)}
.chooser-step{display:grid;grid-template-columns:minmax(235px,.85fr) minmax(0,1.15fr);gap:24px;align-items:center;padding:17px 20px;border:0;border-bottom:1px solid var(--line);background:transparent}
.chooser-step:last-of-type{border-bottom:0}
.chooser-step-head{grid-template-columns:38px minmax(0,1fr);gap:11px;align-items:start;margin:0}
.chooser-step-number{font-size:26px}
.chooser-step h2{margin:0 0 3px;font-size:clamp(20px,2.2vw,27px)}
.chooser-step p{font-size:10px;line-height:1.45}
.chooser-options{gap:7px}
.chooser-options button{min-height:37px;padding:8px 11px;font-size:10px}
.chooser-submit-row{padding:18px 20px;border-top:1px solid var(--line)}
@media(max-width:780px){.chooser-step{grid-template-columns:1fr;gap:12px;padding:16px}.chooser-step-head{grid-template-columns:34px minmax(0,1fr)}.chooser-options button{flex:1 1 calc(50% - 7px)}}
@media(max-width:480px){.chooser-options button{flex:1 1 100%}}
'''
    save("assets/riviera-chooser.css", c, orig)


def active_for(rel: str, lang: str) -> str:
    if lang == "fr":
        if rel.startswith("fr/planifier/") or rel.startswith("riviera-fit/"): return "plan"
        if rel.startswith("riviera-guide/"): return "places"
        if rel.startswith("hotels/") or rel.startswith("fr/dormir/"): return "stay"
        if rel.startswith(("explore/","culture/","restaurants/","plages/","escapades/")): return "explore"
        if rel.startswith("pratique/") or rel.startswith(("bons-plans/transfert-aeroport-nice/","bons-plans/train-ou-bus/","bons-plans/que-reserver/","bons-plans/nice-quand-il-pleut/")): return "practical"
    else:
        if rel.startswith("plan/") or rel.startswith("en/riviera-fit/"): return "plan"
        if rel.startswith("en/riviera-guide/"): return "places"
        if rel.startswith("en/hotels/") or rel.startswith("stay/"): return "stay"
        if rel.startswith(("en/explore/","en/culture/","en/restaurants/","en/beaches/","en/day-trips/")): return "explore"
        if rel.startswith("en/practical/") or rel.startswith(("en/good-finds/nice-airport-transfer/","en/good-finds/train-or-bus/","en/good-finds/what-to-book/","en/good-finds/nice-in-the-rain/")): return "practical"
    return ""


def patch_static_navs() -> None:
    nav_re = re.compile(r'(<nav\b[^>]*class="[^"]*(?:v3-nav|primary-nav)[^"]*"[^>]*>\s*<ul>).*?(</ul>)', re.S)
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        original = text
        lang = "fr" if re.search(r'<html[^>]+lang="fr', text, flags=re.I) else "en"
        active = active_for(rel, lang)
        if lang == "fr":
            items = [("plan","/fr/planifier/","Plan"),("places","/riviera-guide/","Destinations"),("stay","/hotels/","Dormir"),("explore","/explore/","Explorer"),("practical","/pratique/","Pratique")]
        else:
            items = [("plan","/plan/","Plan"),("places","/en/riviera-guide/","Places"),("stay","/en/hotels/","Stay"),("explore","/en/explore/","Explore"),("practical","/en/practical/","Practical")]
        lis = "".join(f'<li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>' for key,href,label in items)
        text = nav_re.sub(lambda m: m.group(1) + lis + m.group(2), text)
        if text != original:
            save(rel, text, original)


def patch_sitemap() -> None:
    p = ROOT / "sitemap.xml"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    urls = [
        "https://www.mametas.com/plan/",
        "https://www.mametas.com/fr/planifier/",
        "https://www.mametas.com/en/practical/",
        "https://www.mametas.com/pratique/",
    ]
    additions = ""
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            additions += f'  <url><loc>{url}</loc><lastmod>2026-09-25</lastmod></url>\n'
    if additions:
        text = text.replace("</urlset>", additions + "</urlset>")
    save("sitemap.xml", text, original)


def validate() -> None:
    errors = []
    for rel, needles in {
        "plan/index.html": ("Build the trip before you fill the days.", "/en/riviera-fit/", "/en/practical/"),
        "fr/planifier/index.html": ("Construisez le voyage avant de remplir les journées.", "/riviera-fit/", "/pratique/"),
        "en/practical/index.html": ("Make the trip work without the cagades.", "RIGHT NOW", "/en/good-finds/train-or-bus/"),
        "pratique/index.html": ("Faites fonctionner le voyage sans cagade.", "RIGHT NOW", "/bons-plans/train-ou-bus/"),
        "en/hotels/index.html": ("stay-base-grid", "MAMETAS HOTEL FIT"),
        "hotels/index.html": ("stay-base-grid", "MAMETAS HOTEL FIT"),
        "en/hotels/finder/index.html": ("engine-base-gate", "Riviera Fit"),
        "hotels/finder/index.html": ("engine-base-gate", "Riviera Fit"),
        "riviera-guide/index.html": ("COMPRENDRE LA BASE", "Destinations"),
    }.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: missing")
            continue
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")
    for rel in ("en/explore/index.html","explore/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "explore-practical" in text:
            errors.append(f"{rel}: Practical block still present")
        if "Start anywhere." in text or "Commencez où vous voulez." in text:
            errors.append(f"{rel}: mixed Start anywhere block still present")
    for asset, needle in (("assets/v3.css","V3 architecture phase 2"),("assets/riviera-chooser.css","V3 architecture compact Riviera Fit"),("assets/hotel-engine.js","chooseBase")):
        if needle not in (ROOT / asset).read_text(encoding="utf-8"):
            errors.append(f"{asset}: missing {needle!r}")
    if errors:
        raise SystemExit("V3 architecture phase 2 failed:\n- " + "\n- ".join(errors))


def main() -> int:
    save("plan/index.html", plan_page("en"))
    save("fr/planifier/index.html", plan_page("fr"))
    save("en/practical/index.html", practical_page("en"))
    save("pratique/index.html", practical_page("fr"))
    rebuild_fr_places()
    patch_en_places()
    patch_stay_hub("hotels/index.html","fr")
    patch_stay_hub("en/hotels/index.html","en")
    patch_hotel_fit_boundary("hotels/finder/index.html","fr")
    patch_hotel_fit_boundary("en/hotels/finder/index.html","en")
    patch_explore("explore/index.html","fr")
    patch_explore("en/explore/index.html","en")
    patch_riviera_fit("riviera-chooser/index.html","fr")
    patch_riviera_fit("en/riviera-chooser/index.html","en")
    patch_home("fr/index.html","fr")
    patch_home("index.html","en")
    patch_css()
    patch_static_navs()
    patch_sitemap()
    validate()
    print(f"V3 architecture phase 2 passed; changed {len(changed)} file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
