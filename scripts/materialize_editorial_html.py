#!/usr/bin/env python3
"""Materialize Mametas decision-support content into public HTML before validation/deploy.

The JS layers remain as progressive enhancement, but the important editorial content
must be present in the server-delivered HTML for search engines, AI readers and users
with JavaScript disabled.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DESTINATIONS = {
    "en/riviera-guide/nice/index.html": {
        "must_id":"what-not-to-miss","must_title":"What not to miss in Nice","must_intro":"Five things earn their place on a first visit. The rest can negotiate for your second trip.",
        "must":[("Old Nice + Cours Saleya","Go in the morning, then lose the map for a while. Market and old town belong together."),("Castle Hill","The fastest way to understand Nice geographically: bay on one side, port on the other."),("The Port + Cap de Nice","Walk east from Port Lympia towards Franck Pilatte for a quieter coastline."),("One proper swim","Ponchettes is easy; La Réserve and Coco Beach change the mood."),("Cimiez — if you have a second day","Matisse, Roman remains, olive gardens and the monastery gardens are the useful counterpoint to the seafront."),("The Promenade — but not all of it","Seven kilometres is a fact, not an assignment.")],
        "practical_title":"Before you overcomplicate Nice","practical":[("Train before car","For Antibes, Cannes, Monaco and Menton, assume the train is the answer first."),("Plan around the heat","Put climbs, markets and long walks early; keep swims, museums or lunch for the hardest hours."),("If it rains, stop chasing the postcard","Switch to Cimiez, museums, a long lunch or central shopping. The sea will still be there tomorrow.")],
        "catch":"Classic mistake: treating Nice only as a base. Keep at least one proper day for the city.",
        "next":[("/stay/nice/","Choose the right Nice hotel"),("/plan/five-days-nice-no-car/","Build the 5-day trip"),("/en/restaurants/nice/","Decide where to eat")]
    },
    "riviera-guide/nice/index.html": {
        "must_id":"indispensables","must_title":"Les choses à voir absolument à Nice","must_intro":"Six choses méritent vraiment leur place lors d’une première visite. Le reste peut attendre le deuxième séjour.",
        "must":[("Vieux-Nice + Cours Saleya","Venez le matin, puis rangez la carte un moment. Marché et vieille ville forment un même mouvement."),("La Colline du Château","Le moyen le plus rapide de comprendre Nice : baie des Anges d’un côté, port de l’autre."),("Le Port + le Cap de Nice","Marchez vers l’est depuis Port Lympia jusqu’à Franck Pilatte."),("Une vraie baignade","Ponchettes est simple ; La Réserve et Coco Beach changent l’ambiance."),("Cimiez — si vous avez un deuxième jour","Matisse, vestiges romains, oliveraie et jardins du monastère offrent le bon contrepoint au bord de mer."),("La Promenade — mais pas ses 7 km","Sept kilomètres est une mesure, pas une consigne.")],
        "practical_title":"Avant de vous compliquer Nice","practical":[("Train plutôt que voiture","Pour Antibes, Cannes, Monaco et Menton, partez d’abord du principe que le train est la solution."),("Gardez la chaleur dans l’équation","En été, placez montées, marchés et longues marches le matin ; gardez baignade, musée ou déjeuner pour les heures les plus dures."),("S’il pleut, ne forcez pas la carte postale","Basculez vers Cimiez, musées, déjeuner long ou shopping central. La mer sera encore là demain.")],
        "catch":"Erreur classique : transformer Nice en camp de base uniquement. Gardez au moins une vraie journée pour la ville.",
        "next":[("/fr/dormir/nice/","Choisir le bon hôtel à Nice"),("/fr/planifier/cinq-jours-nice-sans-voiture/","Construire les 5 jours"),("/restaurants/nice/","Décider où manger")]
    },
    "en/riviera-guide/villefranche-cap-ferrat/index.html": {
        "must_id":"what-not-to-miss","must_title":"What not to miss: Villefranche & Cap-Ferrat","must_intro":"The bay is the headline. Do not bury it under twelve stops.",
        "must":[("Villefranche old town + harbour","Walk down through the old town to the waterfront before doing anything ambitious."),("A swim in Villefranche","This is one place where building the day around a swim makes sense."),("One Cap-Ferrat coastal walk","Choose a section and actually walk it."),("Villa Ephrussi — if gardens are your thing","A strong single cultural stop; pair it with a walk or swim."),("One long lunch","Protect some slack in the schedule.")],
        "practical_title":"The logistics trap","practical":[("Train to Villefranche","From Nice, rail is usually the simple move. Then accept that walking is part of the day."),("One main Cap objective","Choose coastal walk, villa/garden or beach. Combining all three in summer heat turns elegance into endurance."),("Protect some slack","A swim or lunch that runs long is exactly what this day is good at.")],
        "catch":"Classic mistake: trying to maximise the peninsula. Empty space in the schedule is part of the product here.",
        "next":[("/plan/five-days-nice-no-car/#day-two","Fit it into the 5-day plan"),("/en/restaurants/villefranche-sur-mer/","Choose lunch by the bay"),("/en/day-trips/","Compare another day trip")]
    },
    "riviera-guide/villefranche-cap-ferrat/index.html": {
        "must_id":"indispensables","must_title":"Les indispensables : Villefranche & Cap-Ferrat","must_intro":"La rade est le sujet. Inutile de l’enterrer sous douze étapes.",
        "must":[("Vieille ville + port de Villefranche","Descendez jusqu’au front de mer avant toute ambition supplémentaire."),("Une baignade à Villefranche","Ici, construire la journée autour d’une baignade a du sens."),("Un morceau du sentier du Cap-Ferrat","Choisissez une portion de côte et marchez-la vraiment."),("Villa Ephrussi — si les jardins vous parlent","Un excellent arrêt culturel, pas le début d’un inventaire."),("Un long déjeuner","Villefranche et Cap-Ferrat récompensent le vide dans l’agenda.")],
        "practical_title":"Le piège logistique","practical":[("Train pour Villefranche","Depuis Nice, le train est généralement le mouvement simple. Ensuite, acceptez de marcher."),("Un seul objectif sur le Cap","Choisissez sentier, villa/jardin ou plage. Les trois en pleine chaleur transforment vite l’élégance en épreuve."),("Gardez une marge","Un bain ou un déjeuner qui s’allonge est précisément ce que cette journée fait bien.")],
        "catch":"Erreur classique : vouloir rentabiliser la presqu’île. Ici, le vide dans l’agenda fait partie du programme.",
        "next":[("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-deux","L’intégrer aux 5 jours"),("/restaurants/villefranche-sur-mer/","Choisir le déjeuner sur la rade"),("/escapades/","Comparer une autre excursion")]
    },
    "en/riviera-guide/antibes/index.html": {
        "must_id":"what-not-to-miss","must_title":"What not to miss in Antibes","must_intro":"Antibes works because the essentials fit together. Resist the urge to add an entire cape before lunch.",
        "must":[("Old Antibes + the ramparts","Walk the old town, market area and ramparts as one sequence."),("Picasso Museum","The cultural stop that most naturally belongs in a first Antibes day."),("La Gravette","A sandy beach beside the old town is unusually convenient."),("Cap d’Antibes — only with time","The Cap deserves a separate rhythm."),("Cannes — only if you want Cannes","The train makes it easy. That does not make it mandatory.")],
        "practical_title":"Antibes without wasting the day","practical":[("Train for Old Antibes","From Nice or Cannes, rail drops you into a visit that works naturally on foot."),("Cap d’Antibes is another rhythm","Coves and coastal paths need more time and transport."),("Rain: culture before stubbornness","Picasso Museum and a long lunch beat pretending a beach day is still happening.")],
        "catch":"Classic mistake: adding Cannes because the train keeps going. Proximity is not an obligation.",
        "next":[("/plan/five-days-nice-no-car/#day-four","Put Antibes into the itinerary"),("/en/restaurants/antibes/","Choose where to eat"),("/en/beaches/antibes/","Choose the swim")]
    },
    "riviera-guide/antibes/index.html": {
        "must_id":"indispensables","must_title":"Les choses à voir absolument à Antibes","must_intro":"Antibes fonctionne parce que l’essentiel tient bien ensemble. Résistez à l’envie d’ajouter tout le Cap avant le déjeuner.",
        "must":[("Vieil Antibes + remparts","Faites vieille ville, marché et remparts dans un même mouvement."),("Musée Picasso","L’arrêt culturel qui s’intègre le plus naturellement à une première journée."),("La Gravette","Une plage de sable collée à la vieille ville : profitez-en."),("Cap d’Antibes — seulement avec le temps","Le Cap mérite un autre rythme."),("Cannes — seulement si vous voulez Cannes","Le train rend l’ajout facile. Il ne le rend pas obligatoire.")],
        "practical_title":"Antibes sans perdre la journée","practical":[("Train pour le Vieil Antibes","Depuis Nice ou Cannes, le train vous dépose dans une logique de visite à pied."),("Cap d’Antibes = autre rythme","Criques et sentiers demandent davantage de temps et de transport."),("Pluie : culture avant obstination","Musée Picasso et déjeuner en ville font un meilleur plan B qu’une journée plage forcée.")],
        "catch":"Erreur classique : ajouter Cannes parce que le train continue. La proximité n’est pas une obligation.",
        "next":[("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-quatre","Mettre Antibes dans le parcours"),("/restaurants/antibes/","Choisir où manger"),("/plages/antibes/","Choisir la baignade")]
    },
    "en/riviera-guide/monaco/index.html": {
        "must_id":"what-not-to-miss","must_title":"What not to miss in Monaco","must_intro":"Monaco is small enough to edit hard. Four priorities are plenty for a first day.",
        "must":[("The Rock + old town","Start with Monaco-Ville and the Palace area."),("Oceanographic Museum","If you choose one major attraction, this is the most distinctive candidate."),("Port Hercule on foot","Walk between the Rock and Monte-Carlo rather than teleporting between icons."),("Monte-Carlo + Casino square","See the architecture and spectacle even if gambling is not your hobby."),("Menton afterwards — only if Monaco stays edited","The pair works by contrast: Monaco performs, Menton exhales.")],
        "practical_title":"Monaco: manage the verticality","practical":[("Train from Nice","For a first visit it removes parking and traffic from the equation."),("Do not schedule two Monacos","The Rock, museum, harbour and Monte-Carlo are enough."),("Heat: start high","Do climbs and the Rock early, then use museums and lunch when the sun becomes less diplomatic.")],
        "catch":"Classic mistake: confusing a small territory with a small day. Monaco is compact, not flat.",
        "next":[("/plan/five-days-nice-no-car/#day-three","Fit Monaco into the 5-day plan"),("/en/riviera-guide/menton/","Continue to Menton — or do not"),("/en/restaurants/monaco/","Choose where to eat")]
    },
    "riviera-guide/monaco/index.html": {
        "must_id":"indispensables","must_title":"Les choses à voir absolument à Monaco","must_intro":"Monaco est assez petit pour trier sévèrement. Quatre priorités suffisent largement à une première journée.",
        "must":[("Le Rocher + Monaco-Ville","Commencez par la vieille ville et le secteur du Palais."),("Musée océanographique","S’il faut choisir une grande visite, c’est la candidate la plus singulière."),("Port Hercule à pied","Marchez entre le Rocher et Monte-Carlo plutôt que de téléporter la visite d’icône en icône."),("Monte-Carlo + place du Casino","Regardez l’architecture et le spectacle même si le jeu ne vous intéresse pas."),("Menton ensuite — seulement si Monaco reste édité","Le duo fonctionne par contraste : Monaco montre, Menton respire.")],
        "practical_title":"Monaco : gérez surtout la verticalité","practical":[("Train depuis Nice","Pour une première visite, il évite parking et circulation."),("Ne programmez pas deux Monaco","Rocher, musée, port et Monte-Carlo suffisent."),("Chaleur : commencez par les hauteurs","Faites les montées et le Rocher tôt, puis utilisez musée et déjeuner quand le soleil devient moins diplomate.")],
        "catch":"Erreur classique : confondre petit territoire et petite journée. Monaco est compact, pas plat.",
        "next":[("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois","Mettre Monaco dans le parcours"),("/riviera-guide/menton/","Continuer vers Menton — ou pas"),("/restaurants/monaco/","Choisir où manger")]
    },
    "en/riviera-guide/menton/index.html": {
        "must_id":"what-not-to-miss","must_title":"What not to miss in Menton","must_intro":"Menton is best when you stop trying to justify the train ride with quantity.",
        "must":[("Old town + Saint-Michel","Climb through the old town to the basilica and viewpoints."),("One garden","Pick one rather than turning horticulture into endurance sport."),("One Cocteau stop","The Bastion or wedding room gives Menton a cultural thread beyond lemons."),("Sablettes + a swim","Let the itinerary loosen below the old town."),("Do less","A long lunch, old town and one afternoon choice is a successful day.")],
        "practical_title":"Menton: leave room","practical":[("Train for the coastal day trip","From Nice or Monaco, rail is the natural move."),("Old town early or late","The stairs and light are kinder outside the hottest part of the day."),("Rain or serious heat","One Cocteau stop, a long lunch or a carefully chosen garden beats heroic checklist behaviour.")],
        "catch":"Classic mistake: trying to justify the journey by adding attractions. Menton did not ask.",
        "next":[("/plan/five-days-nice-no-car/#day-three","See how Menton fits the plan"),("/en/riviera-guide/monaco/","Compare the Monaco pairing"),("/en/restaurants/menton/","Choose where to eat")]
    },
    "riviera-guide/menton/index.html": {
        "must_id":"indispensables","must_title":"Les choses à voir absolument à Menton","must_intro":"Menton devient meilleure dès qu’on arrête de vouloir rentabiliser le billet de train par la quantité.",
        "must":[("Vieille ville + Saint-Michel","Montez jusqu’à la basilique et aux points de vue."),("Un jardin","Choisissez-en un au lieu de transformer la botanique en sport d’endurance."),("Un arrêt Cocteau","Le Bastion ou la salle des mariages donnent un fil culturel au-delà des citrons."),("Sablettes + baignade","Laissez le parcours se détendre sous la vieille ville."),("Faites moins","Un long déjeuner, la vieille ville et un choix d’après-midi suffisent.")],
        "practical_title":"Menton : laissez de la place","practical":[("Train pour l’aller-retour côtier","Depuis Nice ou Monaco, c’est le mouvement naturel."),("Vieille ville tôt ou tard","Les escaliers et la lumière sont plus aimables hors du cœur chaud de la journée."),("Pluie ou grosse chaleur","Un arrêt Cocteau, un déjeuner long ou un jardin choisi selon les conditions valent mieux qu’une checklist héroïque.")],
        "catch":"Erreur classique : vouloir justifier le trajet en ajoutant des visites. Menton n’a rien demandé.",
        "next":[("/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois","Voir comment Menton tient dans le parcours"),("/riviera-guide/monaco/","Comparer le duo avec Monaco"),("/restaurants/menton/","Choisir où manger")]
    },
}

REGIONAL_EN = [
("Give Nice a day before using it as a station","Old Nice, Castle Hill and one real swim give you the measure of the place.","/en/riviera-guide/nice/"),
("Villefranche + one Cap-Ferrat idea","The bay, a swim, then choose: coastal walk, garden or long lunch.","/en/riviera-guide/villefranche-cap-ferrat/"),
("Edit Monaco hard","The Rock, one major attraction and Monte-Carlo are plenty.","/en/riviera-guide/monaco/"),
("Use Menton to slow down","Old town, Saint-Michel, one garden or Cocteau, then the sea.","/en/riviera-guide/menton/"),
("Choose Antibes for balance","Old town, ramparts, Picasso and a swim: little logistics, a lot of Riviera.","/en/riviera-guide/antibes/"),
("Do Cannes only if you want Cannes","A convenient train does not make the Croisette compulsory.","/en/riviera-guide/nice-or-cannes/"),
("Treat Èze as a logistics choice","Hilltop beauty comes with bus, gradient and crowds.","/en/day-trips/"),
("Use Saint-Paul when art and stone matter","A strong inland excursion, not a decorative add-on.","/en/riviera-guide/saint-paul-de-vence/"),
("Take one proper swim","On the Riviera, the sea is not wallpaper.","/en/beaches/"),
("Protect one half-day with no ambition","Market, coffee, long lunch, beach or museum according to mood.","/plan/five-days-nice-no-car/#make-it-seven")]
REGIONAL_FR = [
("Nice d’abord, pas Nice en transit","Vieux-Nice, Colline du Château et une vraie baignade donnent déjà le ton.","/riviera-guide/nice/"),
("Villefranche + une seule idée au Cap-Ferrat","La rade, une baignade, puis un choix : sentier, jardin ou long déjeuner.","/riviera-guide/villefranche-cap-ferrat/"),
("Une journée Monaco vraiment éditée","Rocher, une grande visite et Monte-Carlo suffisent.","/riviera-guide/monaco/"),
("Menton pour ralentir","Vieille ville, Saint-Michel, un jardin ou Cocteau, puis la mer.","/riviera-guide/menton/"),
("Antibes pour l’équilibre","Vieille ville, remparts, Picasso et baignade : peu de logistique, beaucoup de Riviera.","/riviera-guide/antibes/"),
("Cannes seulement si vous voulez Cannes","Un train pratique ne rend pas la Croisette obligatoire.","/riviera-guide/nice-ou-cannes/"),
("Èze avec la logistique en tête","Le village perché implique bus, pente et affluence.","/escapades/"),
("Saint-Paul si l’art et la pierre comptent","Une vraie excursion intérieure, pas un ajout décoratif.","/riviera-guide/saint-paul-de-vence/"),
("Une vraie baignade","Sur la Riviera, la mer n’est pas un fond d’écran.","/plages/"),
("Un demi-jour sans ambition","Marché, café, déjeuner long, plage ou musée selon l’humeur.","/fr/planifier/cinq-jours-nice-sans-voiture/#version-sept")]


def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")


def decision_block(cfg, fr=False):
    must = ''.join(f'<p class="mini-rule"><strong>{esc(t)}</strong> {esc(d)}</p>' for t,d in cfg["must"])
    practical = ''.join(f'<p class="mini-rule"><strong>{esc(t)}</strong> {esc(d)}</p>' for t,d in cfg["practical"])
    links = ' &nbsp; '.join(f'<a href="{href}">{esc(label)} →</a>' for href,label in cfg["next"])
    return f'''\n<!-- MAMETAS_STATIC_DECISIONS_START -->
<section id="{cfg['must_id']}" data-static-editorial="true"><h2>{cfg['must_title']}</h2><p>{cfg['must_intro']}</p>{must}</section>
<section class="practical-decision-layer" data-static-editorial="true"><h2>{cfg['practical_title']}</h2>{practical}<div class="verdict"><span class="label">{'LE PIÈGE MAMETAS' if fr else 'THE MAMETAS CATCH'}</span><p>{cfg['catch']}</p></div></section>
<div id="mametas-next-decision" class="verdict" data-static-editorial="true"><span class="label">{'LA PROCHAINE DÉCISION' if fr else 'THE NEXT DECISION'}</span><p>{'Faites avancer le voyage plutôt que de remonter au menu.' if fr else 'Move the trip forward instead of climbing back to the menu.'}</p><p>{links}</p></div>
<!-- MAMETAS_STATIC_DECISIONS_END -->\n'''


def insert_before_sources(text, block):
    if "MAMETAS_STATIC_DECISIONS_START" in text:
        return text
    marker = '<div class="sources">'
    if marker in text:
        return text.replace(marker, block + marker, 1)
    return text.replace('</article>', block + '</article>', 1)


def regional_block(fr=False):
    items = REGIONAL_FR if fr else REGIONAL_EN
    cards = ''.join(f'<div class="day-card"><span class="day">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p><p><a class="inline-decision-link" href="{href}">{"Décider en détail" if fr else "Make the detailed decision"} →</a></p></div>' for i,(t,d,href) in enumerate(items,1))
    return f'''<section class="v3-section" id="riviera-first-trip-edit" data-static-editorial="true"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">{'Le premier séjour, vraiment édité' if fr else 'The first trip, properly edited'}</p><h2>{'10 expériences qui structurent vraiment la Côte d’Azur' if fr else '10 experiences that actually shape a first Riviera trip'}</h2></div><p>{'Pas un Top 50. Dix choix qui donnent une colonne vertébrale à trois, cinq ou sept jours.' if fr else 'Not a Top 50. Ten choices that give three, five or seven days a spine.'}</p></div><div class="article-body">{cards}</div></div></section>'''


def materialize_home(path, fr=False):
    p = ROOT/path
    text = p.read_text()
    # Fix the two homepage promises so they lead to the promised place.
    if fr:
        text = text.replace('href="/escapades/"><div class="place-card-media"><img src="/assets/editorial/saint-paul-de-vence.jpg"','href="/riviera-guide/saint-paul-de-vence/"><div class="place-card-media"><img src="/assets/editorial/saint-paul-de-vence.jpg"')
        text = text.replace('href="/escapades/"><div class="place-card-media"><img src="/assets/editorial/saint-tropez.jpg"','href="/riviera-guide/saint-tropez/"><div class="place-card-media"><img src="/assets/editorial/saint-tropez.jpg"')
    else:
        text = text.replace('href="/en/day-trips/"><div class="place-card-media"><img src="/assets/editorial/saint-paul-de-vence.jpg"','href="/en/riviera-guide/saint-paul-de-vence/"><div class="place-card-media"><img src="/assets/editorial/saint-paul-de-vence.jpg"')
        text = text.replace('href="/en/day-trips/"><div class="place-card-media"><img src="/assets/editorial/saint-tropez.jpg"','href="/en/riviera-guide/saint-tropez/"><div class="place-card-media"><img src="/assets/editorial/saint-tropez.jpg"')
    if 'id="riviera-first-trip-edit"' not in text:
        marker = '<section class="v3-section" id="stay">' if not fr else '<section class="v3-section" id="hotels">'
        if marker in text:
            text = text.replace(marker, regional_block(fr) + marker, 1)
    p.write_text(text)


def materialize_plan(path, fr=False):
    p=ROOT/path; text=p.read_text()
    trip_id='version-trois' if fr else 'make-it-three'
    if 'id="mametas-trip-length-edit"' not in text:
        block = ('<div id="mametas-trip-length-edit" class="verdict-box" data-static-editorial="true"><span>3, 5 ou 7 jours : la vraie différence</span><p><strong>3 jours :</strong> Nice + une journée à l’est + une journée à l’ouest. Coupez, ne compressez pas. <strong>5 jours :</strong> le bon équilibre sans changer d’hôtel. <strong>7 jours :</strong> ajoutez de l’air — une journée lente et une excursion intérieure — plutôt qu’une nouvelle obligation quotidienne.</p></div>' if fr else '<div id="mametas-trip-length-edit" class="verdict-box" data-static-editorial="true"><span>3, 5 or 7 days: what actually changes</span><p><strong>3 days:</strong> Nice + one eastern day + one western day. Cut; do not compress. <strong>5 days:</strong> the sweet spot without moving hotels. <strong>7 days:</strong> add air — one slow day and one inland excursion — rather than a new obligation every morning.</p></div>')
        text=text.replace(f'<h2 id="{trip_id}">', block+f'<h2 id="{trip_id}">',1)
    if 'data-itinerary-must-see="true"' not in text:
        recap = ('<section data-itinerary-must-see="true" id="indispensables-parcours"><h2>Les choses à voir absolument sur ce parcours</h2><p>Le noyau dur tient en cinq décisions : Nice ; Villefranche et un choix au Cap-Ferrat ; le Rocher à Monaco puis la vieille ville de Menton ; le Vieil Antibes et ses remparts ; enfin Èze ou une vraie respiration niçoise. Tout le reste est complément.</p></section>' if fr else '<section data-itinerary-must-see="true" id="itinerary-must-sees"><h2>What not to miss on this itinerary</h2><p>The hard core is five decisions: Nice; Villefranche plus one Cap-Ferrat choice; the Rock in Monaco then Menton old town; Old Antibes and the ramparts; finally Èze or a genuinely slow Nice day. Everything else is optional.</p></section>')
        text=text.replace('<h2 id="transport">' if not fr else '<h2 id="transports">', recap + ('<h2 id="transport">' if not fr else '<h2 id="transports">'),1)
    p.write_text(text)


def normalize_navigation_and_chooser():
    for p in ROOT.rglob('*.html'):
        if any(part.startswith('.') for part in p.parts):
            continue
        text=p.read_text()
        original=text
        text=text.replace('<li><a href="/en/restaurants/">Eat &amp; Do</a></li>','<li><a href="/en/explore/">Explore</a></li>')
        text=text.replace('<li><a href="/restaurants/">Manger &amp; faire</a></li>','<li><a href="/explore/">Explorer</a></li>')
        if p.as_posix().endswith('/stay/nice/index.html'):
            old='<a href="#practical"><span>01</span><strong>Practical</strong><small>Easy days out, no car</small></a><a href="#active"><span>02</span><strong>Lively</strong><small>Restaurants nearby</small></a><a href="#quiet"><span>03</span><strong>Peaceful</strong><small>Calm matters</small></a><a href="#chic"><span>04</span><strong>Chic & sea</strong><small>Hotel as experience</small></a>'
            new='<a href="#practical"><span>01</span><strong>Practical</strong><small>Easy days out, no car</small></a><a href="#quiet"><span>02</span><strong>Peaceful</strong><small>Calm matters</small></a><a href="#active"><span>03</span><strong>Lively</strong><small>Restaurants nearby</small></a><a href="#chic"><span>04</span><strong>Chic & sea</strong><small>Hotel as experience</small></a>'
            text=text.replace(old,new)
        if text!=original:
            p.write_text(text)


def update_sitemap():
    p=ROOT/'sitemap.xml'
    if not p.exists(): return
    text=p.read_text()
    urls=[
      'https://www.mametas.com/en/riviera-guide/saint-tropez/',
      'https://www.mametas.com/riviera-guide/saint-tropez/',
      'https://www.mametas.com/en/riviera-guide/saint-paul-de-vence/',
      'https://www.mametas.com/riviera-guide/saint-paul-de-vence/'
    ]
    additions=''.join(f'\n  <url><loc>{u}</loc></url>' for u in urls if u not in text)
    if additions:
        text=text.replace('</urlset>',additions+'\n</urlset>')
        p.write_text(text)


def main():
    for rel,cfg in DESTINATIONS.items():
        p=ROOT/rel
        if not p.exists():
            print('skip missing',rel); continue
        text=p.read_text(); text=insert_before_sources(text,decision_block(cfg, rel.startswith('riviera-guide/'))); p.write_text(text)
    materialize_home('index.html',False)
    materialize_home('fr/index.html',True)
    materialize_plan('plan/five-days-nice-no-car/index.html',False)
    materialize_plan('fr/planifier/cinq-jours-nice-sans-voiture/index.html',True)
    normalize_navigation_and_chooser()
    update_sitemap()
    print('Mametas static editorial materialization complete.')

if __name__=='__main__':
    main()
