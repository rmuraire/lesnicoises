#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_ROOTS = [
    ROOT / "index.html",
    ROOT / "fr" / "index.html",
    ROOT / "en" / "index.html",
    ROOT / "a-propos" / "index.html",
    ROOT / "en" / "about" / "index.html",
]
ACTIVE_GLOBS = [
    "riviera-guide/**/*.html",
    "en/riviera-guide/**/*.html",
    "restaurants/**/*.html",
    "en/restaurants/**/*.html",
    "culture/**/*.html",
    "en/culture/**/*.html",
    "plages/**/*.html",
    "en/beaches/**/*.html",
    "escapades/**/*.html",
    "en/day-trips/**/*.html",
    "explore/**/*.html",
    "en/explore/**/*.html",
    "hotels/**/*.html",
    "en/hotels/**/*.html",
    "fr/dormir/**/*.html",
    "stay/**/*.html",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")
    print(f"Voice pass: {rel}")


def replace_many(text: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def replace_main(rel: str, main_html: str, replacements: list[tuple[str, str]] | None = None) -> None:
    text = read(rel)
    if replacements:
        text = replace_many(text, replacements)
    text, count = re.subn(r"<main>.*?</main>", main_html, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Could not replace <main> in {rel}")
    write(rel, text)


def update_home_en(rel: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    text = replace_many(text, [
        ("Plan a first French Riviera trip without opening forty tabs. Mametas helps you choose where to stay, what to book, how to move — then leaves room to explore.",
         "Plan a first French Riviera trip without opening forty tabs. Tell us how many days you have. We’ll tell you where to stay, what is worth your time and when the train beats the car."),
        ("The opinionated French Riviera guide for first-time visitors — with room to wander.",
         "The French Riviera guide with opinions. We love this coast. We also know when to tell you no."),
        ("We’ll tell you where to stay, what’s worth your time and how to get around. We won’t make you a local, pitchoun. But we might save you a few cagades.",
         "Tell us how many days you have. We’ll tell you where to sleep, what is actually worth your time and when the train beats the car. We won’t make you a local, pichoun. But we can save you a few cagades."),
        ("For first-time visitors planning 3 to 7 days. An independent editorial project embodied by fictional matriarchs; the places, logistics and compromises are researched for real.",
         "The Mametas are fictional. The Riviera in here isn’t. We’re from Nice, we love this coast a little too much, and we’d rather tell you what we really think than sell you the postcard."),
        ("Five fictional matriarchs. Real research. Independent recommendations.",
         "Five fictional Mametas. One very real love affair with the Riviera."),
        ("The Riviera is excellent at turning five days into nine ideas and three logistical mistakes. Start with the shape of the trip: one sensible base, realistic day trips and only the reservations worth making before you land.",
         "Tell us how many days you have. We’ll do the editing. Five days is plenty if you stop trying to collect the whole Riviera before lunch."),
        ("It may not win every beauty contest. It keeps winning when you look at the train map.",
         "Our favourite first base. Yes, we said it. Nice keeps winning the minute you look at the train map."),
        ("The bay does the seducing. The timetable asks for a little more attention.",
         "Possibly our favourite bay on the coast. We could stare at it all morning. The timetable is less romantic."),
        ("Beaches and hotels delivered with a straighter face.",
         "We like Cannes more than people expect us to. It knows exactly what it is."),
        ("Old town, proper beach, less theatre than Cannes.",
         "One of our favourites. Old town, proper beach, very little need to perform."),
        ("A beautiful hotel can still be the wrong hotel.",
         "We love a beautiful hotel. Obviously. We just love the right hotel more."),
        ("Nice is our default first-trip base. Our cards start with the use case and end with the catch. Rates move. A bad location remains impressively loyal.",
         "For a first trip, we’d usually stay in Nice. Pick the use case first, then the room. Rates move. A bad location stays impressively loyal."),
        ("Do not collect the Riviera. Choose it.",
         "Don’t collect the Riviera. Choose it."),
        ("Start with the places that solve a real first-trip decision. Saint-Tropez has its own logistics; geography has never promised that everything photogenic belongs in the same afternoon.",
         "We love all of it. That does not mean you should do all of it. Saint-Tropez has its own logistics, and no, every photogenic place does not belong in the same afternoon."),
        ("A useful guide should help you decide. It should not turn every day into homework. The museums, swims, walks and restaurants are still here — now with their own front door.",
         "A guide should help you decide, then leave you alone. Museums, swims, walks and restaurants are all here. Pick what you fancy. Skip the rest."),
    ])
    path.write_text(text, encoding="utf-8")
    print(f"Voice pass: {rel}")


def update_home_fr(rel: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    text = replace_many(text, [
        ("Préparez un premier séjour sur la Côte d’Azur sans ouvrir quarante onglets. Mametas vous aide à choisir où dormir, quoi réserver et comment circuler — puis laisse de la place à la découverte.",
         "Préparez un premier séjour sur la Côte d’Azur sans ouvrir quarante onglets. Dites-nous combien de jours vous avez. On vous dira où dormir, ce qui vaut vraiment le coup et quand le train gagne sur la voiture."),
        ("Le guide de décision de la Côte d’Azur pour un premier séjour — sans interdire de flâner.",
         "Le guide de la Côte d’Azur qui a des opinions. On aime cette côte. On sait aussi vous dire non."),
        ("On vous dira où dormir, ce qui mérite vraiment votre temps et comment circuler. On ne fera pas de vous un enfant du pays, pitchoun. Mais on peut vous éviter quelques cagades.",
         "Dites-nous combien de jours vous avez. On vous dira où dormir, ce qui vaut vraiment votre temps et quand le train vaut mieux que la voiture. On ne fera pas de vous un enfant du pays, pitchoun. Mais on peut vous éviter quelques cagades."),
        ("Pour un premier séjour de 3 à 7 jours. Un projet éditorial indépendant incarné par des matriarches fictives ; les lieux, la logistique et les compromis, eux, sont réellement documentés.",
         "Les Mametas sont fictives. La Côte d’Azur qu’on raconte, non. On est Niçois, on aime cette côte un peu trop fort, et on préfère vous dire ce qu’on pense vraiment plutôt que vous vendre la carte postale."),
        ("Cinq matriarches fictives. Des recherches réelles. Des recommandations indépendantes.",
         "Cinq Mametas fictives. Une histoire d’amour très réelle avec la Côte d’Azur."),
        ("La Côte d’Azur sait très bien transformer cinq jours en neuf idées et trois erreurs de logistique. Commencez par la forme du séjour : une base sensée, des excursions réalistes et seulement les réservations qui méritent d’être faites avant l’arrivée.",
         "Dites-nous combien de jours vous avez. On fera le tri. Cinq jours, c’est très bien si vous arrêtez d’essayer de collectionner toute la Côte d’Azur avant le déjeuner."),
        ("Elle ne gagne pas tous les concours de beauté. Elle gagne souvent dès qu’on ouvre la carte des trains.",
         "Notre première base préférée. Oui, on l’a dit. Nice recommence à gagner dès qu’on ouvre la carte des trains."),
        ("La rade se charge de séduire. Les horaires demandent un peu plus d’attention.",
         "Peut-être notre plus belle rade. On pourrait la regarder toute la matinée. Les horaires, eux, sont moins romantiques."),
        ("Plages et hôtels servis avec un visage très sérieux.",
         "On aime Cannes plus qu’on ne nous prête l’intention de l’aimer. Elle sait exactement ce qu’elle est."),
        ("Vieille ville, vraie plage, moins de théâtre qu’à Cannes.",
         "Une de nos préférées. Vieille ville, vraie plage, et très peu besoin d’en faire des tonnes."),
        ("Un bel hôtel peut rester le mauvais hôtel.",
         "On adore les beaux hôtels. Évidemment. On adore encore plus le bon hôtel."),
        ("Pour un premier séjour, Nice reste notre base par défaut. Nos cartes commencent par l’usage et se terminent par le compromis. Les prix bougent. Un mauvais emplacement reste remarquablement fidèle.",
         "Pour un premier séjour, nous, on dormirait généralement à Nice. Choisissez d’abord l’usage, ensuite la chambre. Les prix bougent. Un mauvais emplacement, lui, reste remarquablement fidèle."),
        ("Ne collectionnez pas la Riviera. Choisissez-la.",
         "Ne collectionnez pas la Riviera. Choisissez-la."),
        ("Commencez par les lieux qui règlent une vraie décision de premier séjour. Saint-Tropez a sa propre logistique ; la géographie n’a jamais promis que tout ce qui est photogénique tenait dans le même après-midi.",
         "On aime tout. Ça ne veut pas dire qu’il faut tout faire. Saint-Tropez a sa propre logistique et, non, tout ce qui est photogénique ne rentre pas dans le même après-midi."),
        ("Un guide utile doit vous aider à décider. Il ne doit pas transformer chaque journée en devoirs. Musées, baignades, balades et restaurants restent là — avec leur propre porte d’entrée.",
         "Un guide doit vous aider à décider, puis vous laisser tranquille. Musées, baignades, balades et restaurants sont là. Prenez ce qui vous fait envie. Laissez le reste."),
    ])
    path.write_text(text, encoding="utf-8")
    print(f"Voice pass: {rel}")


ABOUT_EN = '''<main><section class="page-hero"><div class="wrap"><p class="eyebrow">ABOUT</p><h1>Why grandmothers? Because Nice would not be Nice without them.</h1><p class="lead">We love these women. The ones who sit by the sea, talk for three hours, know half the neighbourhood and soften absolutely nothing. Mametas starts there.</p></div></section><section class="section"><div class="wrap">
<h2>Why Mametas?</h2>
<div class="article" style="padding-left:0;padding-right:0;padding-top:10px;padding-bottom:10px">
<p><strong>Mametas means grandmothers in Nissart, the language of Nice.</strong> We chose the name because we love the Niçoises who carry this city in their voices, habits, stories and opinions. You see them in the morning by the sea. Eight o’clock, nine o’clock, ten o’clock. They always have something to say. About the weather. The neighbour. The price of tomatoes. Where you should have eaten. Listen long enough and Nice starts making more sense.</p>
<p>The five women on this site are fictional. The affection is not. They are our little tribute to those women, to their character, their humour and that wonderfully local way of saying exactly what they think.</p>
<div class="manifesto-mosaic">
<article class="manifesto-mosaic-card manifesto-mosaic-card--hero"><div class="manifesto-mosaic-media"><img alt="Portrait of a fictional Mameta by the bay" loading="lazy" src="/assets/editorial/nicoise-blonde-front-v2.jpg"/></div><div class="manifesto-mosaic-quote"><p><strong>Sit down, pichoun. First tell us how many days you have. No, you are not doing Monaco, Menton and Saint-Tropez tomorrow.</strong></p></div></article>
<article class="manifesto-mosaic-card manifesto-mosaic-card--hero"><div class="manifesto-mosaic-media"><img alt="Portrait of a fictional Mameta wearing red sunglasses" loading="lazy" src="/assets/editorial/nicoise-blonde-red-glasses-v2.jpg"/></div><div class="manifesto-mosaic-quote"><p><strong>We really like it. That’s the review. You don’t need fourteen adjectives.</strong></p></div></article>
<article class="manifesto-mosaic-card manifesto-mosaic-card--hero"><div class="manifesto-mosaic-media"><img alt="Profile portrait of a fictional Mameta" loading="lazy" src="/assets/editorial/nicoise-brunette-profile-v2.jpg"/></div><div class="manifesto-mosaic-quote"><p><strong>Yes, the view is amazing. No, that does not give an average plate a pardon.</strong></p></div></article>
</div>
<div class="about-character"><div class="about-character-copy"><span class="kicker">WHY FIVE OF THEM?</span><h3>Because one Niçoise with an opinion was never going to be enough.</h3><p>They are fictional editorial characters, not a fake documentary and not a real committee of retired ladies. Think of them as the voice of the site. Warm, nosy, affectionate, occasionally impatient. They like beautiful things. They also know when something is a cagade.</p></div><div class="about-character-media"><img alt="Portrait of a fictional Mameta facing the sea" loading="lazy" src="/assets/editorial/nicoise-blonde-profile-v2.jpg"/></div></div>
<h2>And us?</h2>
<p>Mametas is edited by people from Nice. Nice is where we grew up, where family and friends still are, and where we keep going back. We are madly in love with the French Riviera. Passionately. Not blindly. That part matters.</p>
<p>Loving a place also means knowing when it is too crowded, what is not worth the detour, which view really is extraordinary, which restaurant we would book again tomorrow and when the clever thing to do is stop planning and order another coffee.</p>
<h2>What we want to show you</h2>
<p>Not a “secret Riviera locals don’t want you to know”. Please. Nice has been welcoming visitors for a very long time. We just want to show you the Riviera we know and love, with its grand hotels and tiny tables, its beautiful mornings, its traffic, its pebbles, its absurd prices in August and the places that still make us stop and say, every single time, <em>look at that.</em></p>
<p>So yes, we have favourites. We say so. We dislike some things. We say that too. A guide with no opinion is a directory.</p>
<div class="verdict"><span class="label">HOUSE RULE</span><p>If we love it, we’ll tell you. If we don’t, we won’t invent enthusiasm to fill a page.</p></div>
<h2>We still check things. Obviously.</h2>
<p>The hotels, restaurants, beaches, museums and villages are real. We verify practical information, maps, menus, programmes, official sources and public feedback before publishing. When somewhere has not been personally visited, we do not pretend otherwise. Research is not a personality. It is simply the minimum.</p>
<h2>And the money?</h2>
<p>Some links, especially hotel links, are affiliate links. If you book through them, Mametas may earn a commission at no extra cost to you. Good. The site needs paying for. But an affiliate link does not buy an opinion, and a commission will never make us suddenly adore a bad location.</p>
<p>If we send you somewhere mediocre, you will stop trusting us. We would rather you came back. Much rather.</p>
<div class="note"><strong>A tiny lexicon. We are not translating it every time.</strong><br/>Mèfi: watch out. Pichoun: little one, affectionately. Cagade: a stupid avoidable mistake. Dégun: nobody. Ficanas: gossips and busybodies. Empégué: the person who looks completely out of it, particularly behind the wheel. Niocou: fool. Paillassou: not exactly the sharpest knife in the drawer. Hu: put it wherever you like.</div>
</div></div></section></main>'''

ABOUT_FR = '''<main><section class="page-hero"><div class="wrap"><p class="eyebrow">À PROPOS</p><h1>Pourquoi des mamies ? Parce que Nice ne serait pas Nice sans elles.</h1><p class="lead">On les adore. Celles qui s’installent face à la mer, parlent pendant trois heures, savent ce qui se passe dans tout le quartier et n’ont aucune raison d’arrondir les angles. Mametas part de là.</p></div></section><section class="section"><div class="wrap">
<h2>Pourquoi Mametas ?</h2>
<div class="article" style="padding-left:0;padding-right:0;padding-top:10px;padding-bottom:10px">
<p><strong>Mametas, ce sont les grands-mères en nissart, la langue de Nice.</strong> On a choisi ce nom parce qu’on aime ces Niçoises qui portent la ville dans leur accent, leurs habitudes, leurs histoires et leurs avis. On les croise le matin au bord de mer. Huit heures, neuf heures, dix heures. Elles ont toujours quelque chose à se raconter. Le temps. La voisine. Le prix des tomates. Le restaurant où vous auriez dû aller. Écoutez-les assez longtemps et Nice devient plus claire.</p>
<p>Les cinq femmes du site sont fictives. L’affection, elle, est bien réelle. C’est notre petit hommage à ces dames, à leur caractère, à leur humour et à cette façon très niçoise de dire exactement ce qu’elles pensent.</p>
<div class="manifesto-mosaic">
<article class="manifesto-mosaic-card manifesto-mosaic-card--hero"><div class="manifesto-mosaic-media"><img alt="Portrait d'une Mameta fictive sur fond de baie" loading="lazy" src="/assets/editorial/nicoise-blonde-front-v2.jpg"/></div><div class="manifesto-mosaic-quote"><p><strong>Assieds-toi, pitchoun. D’abord, combien de jours tu as ? Non, tu ne fais pas Monaco, Menton et Saint-Tropez demain.</strong></p></div></article>
<article class="manifesto-mosaic-card manifesto-mosaic-card--hero"><div class="manifesto-mosaic-media"><img alt="Portrait d'une Mameta fictive en lunettes rouges" loading="lazy" src="/assets/editorial/nicoise-blonde-red-glasses-v2.jpg"/></div><div class="manifesto-mosaic-quote"><p><strong>Nous, on adore cette adresse. Voilà. Pas besoin de quatorze adjectifs.</strong></p></div></article>
<article class="manifesto-mosaic-card manifesto-mosaic-card--hero"><div class="manifesto-mosaic-media"><img alt="Portrait de profil d'une Mameta fictive" loading="lazy" src="/assets/editorial/nicoise-brunette-profile-v2.jpg"/></div><div class="manifesto-mosaic-quote"><p><strong>Oui, la vue est dingue. Non, ça ne donne pas l’absolution à une assiette moyenne.</strong></p></div></article>
</div>
<div class="about-character"><div class="about-character-copy"><span class="kicker">POURQUOI CINQ ?</span><h3>Parce qu’une seule Niçoise avec un avis, ça n’allait jamais suffire.</h3><p>Ce sont des personnages éditoriaux fictifs. Pas un faux documentaire, pas une vraie rédaction de retraitées. Pensez-les comme la voix du site. Chaleureuse, curieuse, affectueuse, parfois un peu brusque. Elles aiment les belles choses. Elles savent aussi reconnaître une cagade.</p></div><div class="about-character-media"><img alt="Portrait d'une Mameta fictive face à la mer" loading="lazy" src="/assets/editorial/nicoise-blonde-profile-v2.jpg"/></div></div>
<h2>Et nous ?</h2>
<p>Mametas est édité par des Niçois. Nice, c’est là qu’on a grandi. La famille et les amis sont encore là, et on y revient tout le temps. On est fous amoureux de la Côte d’Azur. Passionnément. Pas aveuglément. C’est important.</p>
<p>Aimer un endroit, c’est aussi savoir quand il est trop plein, ce qui ne mérite pas le détour, quelle vue est vraiment extraordinaire, dans quel restaurant on retournerait demain et quand la meilleure décision consiste à arrêter de planifier et commander un autre café.</p>
<h2>Ce qu’on veut vous montrer</h2>
<p>Pas une “Côte d’Azur secrète que les locaux veulent vous cacher”. Mèfi. Nice accueille des visiteurs depuis très longtemps. On veut simplement vous montrer la Côte d’Azur qu’on connaît et qu’on aime, avec ses grands hôtels et ses petites tables, ses matins magnifiques, ses embouteillages, ses galets, ses prix parfois absurdes en août et ces endroits qui nous font encore dire, à chaque fois, <em>regarde-moi ça.</em></p>
<p>Donc oui, on a des préférences. On les dit. Il y a des choses qu’on aime moins. On le dit aussi. Un guide sans opinion, c’est un annuaire.</p>
<div class="verdict"><span class="label">LA RÈGLE DE LA MAISON</span><p>Si on adore, on vous le dira. Si on n’adore pas, on ne va pas inventer de l’enthousiasme pour remplir une page.</p></div>
<h2>On vérifie quand même les choses. Évidemment.</h2>
<p>Les hôtels, restaurants, plages, musées et villages sont bien réels. On vérifie les informations pratiques, les cartes, les menus, les programmes, les sources officielles et les avis publics avant de publier. Quand une adresse n’a pas été visitée personnellement, on ne prétend pas le contraire. La recherche n’est pas une personnalité. C’est juste le minimum.</p>
<h2>Et l’argent ?</h2>
<p>Certains liens, notamment vers les hôtels, sont affiliés. Si vous réservez par leur intermédiaire, Mametas peut toucher une commission, sans surcoût pour vous. Tant mieux, le site doit bien se financer. Mais un lien affilié n’achète pas une opinion, et une commission ne nous fera pas soudain adorer un mauvais emplacement.</p>
<p>Si on vous envoie dans des endroits médiocres, vous ne nous ferez plus confiance. On préfère largement que vous reveniez. Vraiment largement.</p>
<div class="note"><strong>Le petit lexique. On ne traduira pas à chaque fois.</strong><br/>Mèfi : attention. Pitchoun : le petit, affectueusement. Cagade : la belle connerie évitable. Dégun : personne. Ficanas : les commères, ceux qui se mêlent de tout. Empégué : le type qui a l’air à côté de ses pompes, notamment au volant. Niocou : le niais. Paillassou : celui qui n’est pas exactement le couteau le plus affûté du tiroir. Hu : mettez-le à peu près où vous voulez.</div>
</div></div></section></main>'''


def update_about_pages() -> None:
    replace_main("en/about/index.html", ABOUT_EN, [
        ("The Mametas manifesto: five fictional characters, real places, researched recommendations and very little diplomacy.",
         "Why Mametas? A love letter to the women, voices and opinions that make Nice feel like Nice, plus the Riviera advice we actually give our friends."),
        ("Who's behind Mametas? Does it really matter?", "Why grandmothers? Because Nice would not be Nice without them."),
    ])
    replace_main("a-propos/index.html", ABOUT_FR, [
        ("Le manifeste de Mametas : cinq matriarches fictives, des lieux réels, une sélection documentée et très peu de diplomatie.",
         "Pourquoi Mametas ? Une déclaration d’amour aux Niçoises, à leurs voix, à leur caractère et à la Côte d’Azur qu’on a envie de faire découvrir."),
        ("Qui parle ? Peut-être pas la bonne question.", "Pourquoi des mamies ? Parce que Nice ne serait pas Nice sans elles."),
    ])


def update_nice_restaurants() -> None:
    rel = "en/restaurants/nice/index.html"
    text = read(rel)
    text = replace_many(text, [
        ("Twelve addresses. At eight, we could tell you where to go. At twelve, we can finally help you choose.",
         "Twelve addresses. Some we love. A few we love for one very specific reason. That’s more useful than pretending every restaurant is a must."),
        ("Start with what you feel like eating, then look at the price. Reversing that order has produced many sad salads on the Promenade.",
         "Tell us what you feel like eating and how much you want to spend. We’ll narrow it down. And please, no sad salad on the Promenade unless you genuinely wanted the salad."),
        ("Dominique Le Stanc’s institution stays focused on the Niçoise repertoire. <strong>The catch:</strong> small room and limited availability; plan ahead.",
         "We really like La Mérenda. Tiny room, serious Niçoise cooking, no circus. <strong>But:</strong> it fills up. Book."),
        ("Socca is the main reason to come. The tourist office quotes an average spend around €15–20 in 2026. <strong>The catch:</strong> this is casual and local, not a three-hour dinner.",
         "Come for the socca. That’s the point. Eat it hot and don’t overthink it. <strong>But:</strong> this is quick, casual and popular, not a three hour dinner."),
        ("A family house since 1927, carrying the Cuisine Nissarde label. <strong>The catch:</strong> classic by design; if you want avant-garde, keep walking.",
         "We like it for a first proper Niçoise meal. Family run, classic, no need to reinvent the wheel. <strong>But:</strong> if you want avant garde, keep walking."),
        ("A recognised bistro with southern accents. <strong>The catch:</strong> popular and busy; booking is more effective than optimism.",
         "One of our favourites for a lively central dinner. <strong>But:</strong> it’s popular. Book. Optimism is not a reservation."),
        ("Seasonal cooking above the sea. <strong>The catch:</strong> part of the bill is the setting; come because you actually want the setting.",
         "One of our favourite views in Nice. Yes, really. <strong>But:</strong> part of the bill is the setting, so come because you actually want the setting."),
        ("A family restaurant since 1953, with Niçoise cooking, fresh produce and a terrace. <strong>The catch:</strong> more neighbourhood table than spectacular destination — often a compliment.",
         "We like Chez Davia precisely because it feels like a neighbourhood table. Niçoise cooking, fresh produce, terrace. <strong>But:</strong> don’t come looking for spectacle. That’s the compliment."),
    ])
    write(rel, text)

    rel = "restaurants/nice/index.html"
    text = read(rel)
    text = replace_many(text, [
        ("Douze adresses, parce qu’à huit on vous disait où aller. À douze, on commence enfin à vous aider à choisir.",
         "Douze adresses. Il y en a qu’on adore. D’autres qu’on aime pour une raison très précise. C’est plus utile que de prétendre que tout est incontournable."),
        ("Commencez par l’envie, puis regardez le prix. Faire l’inverse finit souvent en salade triste sur la Promenade.",
         "Dites-nous ce que vous avez envie de manger et combien vous voulez dépenser. On fera le tri. Et pitié, pas de salade triste sur la Promenade sauf si vous aviez vraiment envie d’une salade."),
        ("Une institution de Dominique Le Stanc, centrée sur le répertoire niçois. <strong>Le compromis :</strong> petite salle et disponibilité limitée ; on anticipe.",
         "Nous, on aime vraiment La Mérenda. Petite salle, vraie cuisine niçoise, pas de cirque. <strong>Le hic :</strong> ça se remplit. Réservez."),
        ("La socca est la raison principale de venir. Ticket moyen annoncé autour de 15–20 € par l’Office de tourisme en 2026. <strong>Le compromis :</strong> on vient pour le registre populaire, pas pour un dîner posé de trois heures.",
         "Venez pour la socca. C’est le sujet. Mangez-la chaude et ne compliquez pas tout. <strong>Le hic :</strong> c’est rapide, populaire, vivant. Pas un dîner de trois heures."),
        ("Maison familiale depuis 1927, labellisée Cuisine Nissarde. <strong>Le compromis :</strong> c’est classique par choix ; si vous cherchez l’avant-garde, continuez de marcher.",
         "On aime Acchiardo pour une première vraie assiette niçoise. Familial, classique, aucune raison de réinventer la roue. <strong>Le hic :</strong> si vous cherchez l’avant-garde, continuez de marcher."),
        ("Une table de bistrot reconnue, avec accents du Sud. <strong>Le compromis :</strong> adresse connue et salle animée ; réservez plutôt que de négocier avec le destin.",
         "Une de nos préférées pour un dîner central et vivant. <strong>Le hic :</strong> c’est connu. Réservez. L’optimisme n’est pas une réservation."),
        ("Une adresse posée au-dessus de la mer, avec cuisine saisonnière. <strong>Le compromis :</strong> vous payez aussi le cadre ; c’est précisément pour cela qu’il faut vouloir le cadre.",
         "Une de nos vues préférées à Nice. Oui, vraiment. <strong>Le hic :</strong> vous payez aussi le cadre. Venez parce que vous voulez le cadre."),
        ("Maison familiale depuis 1953, cuisine niçoise, produits frais, terrasse. <strong>Le compromis :</strong> davantage table de quartier que destination spectaculaire — ce qui est souvent un compliment.",
         "On aime Chez Davia précisément parce que ça ressemble à une table de quartier. Cuisine niçoise, produits frais, terrasse. <strong>Le hic :</strong> ne venez pas chercher le grand spectacle. C’est le compliment."),
    ])
    write(rel, text)


def soften_repetition_and_dashes() -> None:
    paths: set[Path] = set(p for p in ACTIVE_ROOTS if p.is_file())
    for pattern in ACTIVE_GLOBS:
        paths.update(ROOT.glob(pattern))
    for path in sorted(paths):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        new = text.replace(" — ", ", ")
        if path.as_posix().find("/en/") >= 0 or path == ROOT / "index.html" or path.as_posix().find("/stay/") >= 0:
            new = new.replace("Classic mistake:", "Mèfi:")
        else:
            new = new.replace("Erreur classique :", "Mèfi :")
        if "/en/restaurants/" in path.as_posix():
            new = new.replace("<strong>The catch:</strong>", "<strong>But:</strong>")
        if "/restaurants/" in path.as_posix() and "/en/restaurants/" not in path.as_posix():
            new = new.replace("<strong>Le compromis :</strong>", "<strong>Le hic :</strong>")
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"Voice polish: {path.relative_to(ROOT)}")


def main() -> int:
    update_home_en("index.html")
    update_home_en("en/index.html")
    update_home_fr("fr/index.html")
    update_about_pages()
    update_nice_restaurants()
    soften_repetition_and_dashes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
