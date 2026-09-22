/* Mametas Riviera Chooser V1
   Doctrine first: duration + mobility constrain; mood selects; pace modifies hub value and excursion density.
*/
(function(){
  var ROOTS=document.querySelectorAll('[data-riviera-chooser]');
  if(!ROOTS.length) return;

  var MATRIX={
    nice:{type:'default',sea:2.2,food:3,culture:3,glamour:2,peace:1.2,hub:3},
    cannes:{type:'default',sea:3,food:2.6,culture:1.6,glamour:3,peace:1.2,hub:2.5},
    antibes:{type:'default',sea:3,food:2.4,culture:2.5,glamour:2.1,peace:2.1,hub:2.2},
    villefranche:{type:'default',sea:3.25,food:1.7,culture:1.6,glamour:2.2,peace:3.1,hub:1.5},
    menton:{type:'default',sea:2.5,food:2.2,culture:2.4,glamour:1.5,peace:3,hub:1.9},
    monaco:{type:'intentional',sea:1.4,food:2.9,culture:2.3,glamour:3.2,peace:1.1,hub:1.8},
    'saint-tropez':{type:'intentional',sea:3.1,food:2.6,culture:1.3,glamour:3.2,peace:2,hub:.5},
    'saint-paul':{type:'intentional',sea:.2,food:2,culture:3.2,glamour:2,peace:3.1,hub:.4}
  };
  var DEFAULT_ORDER=['nice','cannes','antibes','villefranche','menton'];
  var PACE_HUB={slow:.25,balanced:1,ambitious:1.65};
  var MOBILITY={
    nocar:{nice:1.4,cannes:1,antibes:.8,villefranche:.6,menton:.8,monaco:.8,'saint-tropez':-4,'saint-paul':-1.8},
    car:{nice:0,cannes:.1,antibes:.2,villefranche:.2,menton:0,monaco:0,'saint-tropez':1.3,'saint-paul':1.1},
    either:{nice:.5,cannes:.4,antibes:.4,villefranche:.3,menton:.3,monaco:.2,'saint-tropez':0,'saint-paul':.2}
  };
  var DAYS={
    3:{nice:.9,cannes:.5,antibes:.5,villefranche:.1,menton:-.2,monaco:-.4,'saint-tropez':-3,'saint-paul':-1},
    5:{nice:0,cannes:0,antibes:0,villefranche:0,menton:0,monaco:0,'saint-tropez':0,'saint-paul':0},
    7:{nice:.1,cannes:.1,antibes:.1,villefranche:.2,menton:.2,monaco:.3,'saint-tropez':.5,'saint-paul':.4}
  };
  var INTENT_TRIGGERS={
    monaco:['glamour','food'],
    'saint-tropez':['glamour','sea'],
    'saint-paul':['culture','peace']
  };
  var INTENT_MARGIN={monaco:.25,'saint-tropez':.45,'saint-paul':.45};

  var COPY={
    en:{
      progress:function(n){return 'Decision '+n+' of 4';},
      reset:'Start again',
      back:'Back',
      questions:[
        {key:'days',title:'How long do you actually have?',deck:'Time is the first filter. Three days and seven days should not produce the same Riviera.',options:[
          ['3','3 days','Cut hard. One base, very few heroic transfers.'],
          ['5','5 days','The useful middle: enough contrast without turning the trip into admin.'],
          ['7','7 days or more','More range, but still no obligation to collect the coast.']
        ]},
        {key:'mobility',title:'How are you moving around?',deck:'This changes the geography before taste gets a vote.',options:[
          ['nocar','No car','Train, bus and feet. Parking can remain somebody else’s character-building exercise.'],
          ['car','With a car','The inland and western edges open up. Traffic still exists, pichoun.'],
          ['either','Either is fine','We will choose on the trip, not on principle.']
        ]},
        {key:'mood',title:'What do you want most from the Riviera?',deck:'Pick the thing you would be annoyed to miss. If you genuinely do not know, hand us the scissors.',options:[
          ['sea','Sea & swimming','Beach time, coves, sand or water worth building a day around.'],
          ['food','Food & city life','Restaurants, evenings and somewhere that still works after the beach bag is put away.'],
          ['culture','Art & villages','Museums, foundations, old towns and inland detours with a reason to exist.'],
          ['glamour','Riviera glamour','Hotels, polished evenings and a little theatre. No apology required.'],
          ['peace','Peace & beauty','A beautiful base with the volume turned down.'],
          ['decide','Decide for me','No dominant obsession. Give me the strongest first-trip logic.']
        ]},
        {key:'pace',title:'How do you like to travel?',deck:'Pace does not choose your taste. It decides how much a good transport hub should matter, and how much we let you attempt.',options:[
          ['slow','Slow','Fewer moves. The base has to earn the hours you spend in it.'],
          ['balanced','Balanced','A proper base, a few strong excursions and no medal for exhaustion.'],
          ['ambitious','Ambitious','You want range. We will allow it, but the logistics have to behave.']
        ]}
      ],
      labels:{verdict:'THE MAMETAS VERDICT',do:'What earns the days',cut:'THE MAMETAS CUT',hotels:'Then choose the hotel level',hotelNote:'Price symbols are relative Mametas bands, not live room rates. Practical / Comfort / Splurge describe the role of the hotel, not a guaranteed tariff.',moreHotels:'See more hotels in this base',plan:'Open the useful plan',share:'Open or share this result',override:'You overruled Mametas. Fair enough.',backVerdict:'Back to the Mametas verdict',escape:'Change the base deliberately',priority:'Priority',season:'Season note'},
      tiers:{practical:'Practical',comfort:'Comfort',splurge:'Splurge'},
      options:{days:{3:'3 days',5:'5 days',7:'7+ days'},mobility:{nocar:'No car',car:'Car',either:'Either'},mood:{sea:'Sea',food:'Food & city life',culture:'Art & villages',glamour:'Glamour',peace:'Peace & beauty',decide:'Decide for me'},pace:{slow:'Slow',balanced:'Balanced',ambitious:'Ambitious'}},
      base:{
        nice:{name:'Nice',headline:'Stay in Nice.',intro:'Nice wins when the trip needs range without making logistics the main character.',mood:{sea:'Keep the sea in the day, not necessarily under the hotel window.',food:'Restaurants, evenings and the strongest all-round city life make this the easy call.',culture:'Nice gives you its own museums and the best launch point for the cultural detours around it.',glamour:'You still get serious hotels and evenings, while keeping Monaco as spectacle rather than postcode.',peace:'This is not the quietest answer, but it can still win when mobility and range matter more.',decide:'For an undecided first trip, there is no cleverer all-round answer.'}},
        cannes:{name:'Cannes',headline:'Stay in Cannes.',intro:'Cannes works when the western Riviera, sand and polished hotel life belong in the same trip.',mood:{sea:'Sand, beach time and an easy western coastline give Cannes the edge.',food:'You get a proper evening base without sacrificing the coast around it.',culture:'Culture is not Cannes’s strongest argument; the win here comes from the rest of your profile.',glamour:'You asked for Riviera theatre. Cannes gives you hotels, sand and a coast that remains usable.',peace:'Cannes is not our default quiet answer, so something else in your profile is doing real work.',decide:'It is the more polished western base when the overall balance points this way.'}},
        antibes:{name:'Antibes',headline:'Stay in Antibes.',intro:'Antibes is the middle path: real town, old streets, proper beach and less ceremony than Cannes.',mood:{sea:'A sandy swim beside a real old town is a surprisingly efficient argument.',food:'The town stays useful after the beach, without needing Nice-scale city energy.',culture:'Picasso, the old town and easy western access give culture enough weight without turning the stay into homework.',glamour:'There is polish here, but less performance. That can be the better version of Riviera.',peace:'Antibes gives you breathing room without withdrawing from the coast.',decide:'When balance matters more than maximum anything, Antibes has a habit of surviving the edit.'}},
        villefranche:{name:'Villefranche / Beaulieu',headline:'Stay in Villefranche or Beaulieu.',intro:'This is the answer when beauty and sea matter more than running the coastline like a transport project.',mood:{sea:'The bay is not a side dish here. Build the stay around the water and stop apologising.',food:'The food scene is smaller, so this only wins when other parts of your profile pull hard.',culture:'Nice remains close enough for culture; the base itself is chosen for beauty rather than museum density.',glamour:'Think quieter Riviera, not Croisette theatre.',peace:'You asked for beauty with the volume turned down. This is exactly the brief.',decide:'This only beats the bigger hubs when your pace allows the base itself to matter more.'}},
        menton:{name:'Menton',headline:'Stay in Menton.',intro:'Menton makes sense when the Riviera should feel softer, slower and slightly less interested in showing off.',mood:{sea:'The sea is part of the rhythm rather than a beach-club project.',food:'There is enough town life to support the stay, with Italy quietly influencing the mood.',culture:'Gardens, old town and Cocteau give the east more substance than a pretty-colour argument.',glamour:'This is elegance at a lower volume, not Monaco theatre.',peace:'You asked for calm without disappearing from civilisation. Menton takes that seriously.',decide:'Menton wins only when your answers clearly prefer the eastern, slower version of the coast.'}},
        monaco:{name:'Monaco',headline:'Stay in Monaco.',intro:'This is an intentional answer. You did not ask for the most flexible base; you asked for Monaco to be part of the experience.',mood:{glamour:'For a slow, longer glamour trip, the palace life, restaurants and spectacle finally justify the postcode.',food:'Monaco can carry serious restaurants, but it rarely wins the whole-base decision on food alone.',sea:'The sea exists; it is not why we send you here.',culture:'There is more culture than the car-counting crowd admits, but this remains an intentional stay.',peace:'If peace was the brief, Monaco has misunderstood the assignment.',decide:'Mametas does not choose Monaco by accident.'}},
        'saint-tropez':{name:'Saint-Tropez',headline:'Stay in Saint-Tropez.',intro:'You have enough time, a car and a strong reason to make the peninsula the holiday rather than a difficult day trip.',mood:{glamour:'This is the rare profile where Saint-Tropez stops being an excursion and becomes the point.',sea:'The peninsula earns the base when beach time is central and the car unlocks the geography.',food:'Restaurants help, but they are not enough on their own to justify the logistics.',culture:'This is not the culture-first answer.',peace:'Quiet exists around the peninsula, but Saint-Tropez is still a deliberate commitment.',decide:'Mametas does not send an undecided first-timer here.'}},
        'saint-paul':{name:'Saint-Paul-de-Vence',headline:'Stay in Saint-Paul-de-Vence.',intro:'This is an inland commitment, not a cute detour dressed up as a base.',mood:{culture:'With a car, enough days and a slow pace, Maeght, the village and inland evenings can finally justify sleeping here.',peace:'The calm is real, but the coast becomes a deliberate outing rather than the default.',sea:'Wrong brief. The Mediterranean is now a drive.',food:'There are good tables, but food alone does not make this the base.',glamour:'The glamour here is retreat, stone and hotels, not Croisette lights.',decide:'An undecided first trip should not begin by hiding inland.'}}
      },
      cuts:{
        nice:{short:'Saint-Tropez. Three days is not the moment to spend one of them proving you can reach it.',normal:'Saint-Tropez unless it is the reason for the trip. The coast does not issue attendance certificates.'},
        cannes:{short:'Monaco and Menton. You picked the west; let it be a decision.',normal:'Do not add the whole eastern Riviera just because trains exist. Cannes already gives you a side.'},
        antibes:{short:'Cannes as an automatic add-on. The train continuing is not an instruction.',normal:'One western add-on is enough. Proximity is not an obligation.'},
        villefranche:{short:'Trying to collect both ends of the Riviera. The point of this base is to slow the geography down.',normal:'Saint-Tropez. You chose beauty and a slower coast, not a day-long logistics demonstration.'},
        menton:{short:'Cannes. Three days from Menton should not become a coast-length commute.',normal:'Cannes as an automatic add-on. You deliberately chose the eastern edge; use it.'},
        monaco:{short:'Trying to use Monaco as a cheap transport trick. Stay because you want Monaco.',normal:'Turning Monaco into a hub for the entire coast. The postcode only makes sense if Monaco itself matters.'},
        'saint-tropez':{short:'Nothing. Mametas would not put you here for three days.',normal:'Nice and Monaco day trips. You chose the peninsula; stop commuting back to another holiday.'},
        'saint-paul':{short:'Nothing. This base is not a three-day first-trip recommendation.',normal:'Beach-hopping every day. This base only works if art, stone and inland calm are genuinely the point.'}
      },
      pace:{slow:'Your slow pace lowers the value of a perfect hub. We are letting the base itself do more of the work.',balanced:'Balanced keeps transport useful without letting the timetable choose the whole holiday.',ambitious:'Ambitious makes hub quality matter. You asked for range, so the base has to move well.'},
      escape:{monaco:'Actually, I want Monte-Carlo and palace life to be the trip.', 'saint-tropez':'Actually, Saint-Tropez is the point of the holiday.', 'saint-paul':'Actually, I want the inland art-and-village stay.', nice:'Prefer the more flexible all-round base.',cannes:'Prefer the more flexible western base.',antibes:'Prefer the lower-friction western base.',villefranche:'Prefer beauty without the intentional-base commitment.',menton:'Prefer the calmer default eastern base.'}
    },
    fr:{
      progress:function(n){return 'Décision '+n+' sur 4';},
      reset:'Recommencer',
      back:'Retour',
      questions:[
        {key:'days',title:'Combien de jours avez-vous vraiment ?',deck:'Le temps est le premier filtre. Trois jours et sept jours ne doivent pas produire la même Riviera.',options:[
          ['3','3 jours','On coupe franchement. Une base, très peu de transferts héroïques.'],
          ['5','5 jours','Le bon milieu : assez de contraste sans transformer le séjour en gestion de projet.'],
          ['7','7 jours ou plus','Plus d’amplitude, sans obligation de collectionner la côte.']
        ]},
        {key:'mobility',title:'Comment allez-vous vous déplacer ?',deck:'Cela change la géographie avant même que vos goûts aient le droit de voter.',options:[
          ['nocar','Sans voiture','Train, bus et pieds. Le parking peut rester l’exercice de caractère de quelqu’un d’autre.'],
          ['car','Avec une voiture','L’intérieur et l’ouest s’ouvrent davantage. Les bouchons existent toujours, pichoun.'],
          ['either','Peu importe','On choisira selon le séjour, pas par principe.']
        ]},
        {key:'mood',title:'Qu’attendez-vous surtout de la Côte d’Azur ?',deck:'Choisissez ce que vous seriez vraiment contrarié de manquer. Si vous ne savez pas, donnez-nous les ciseaux.',options:[
          ['sea','Mer & baignades','Plages, criques, sable ou eau autour de laquelle on peut construire une journée.'],
          ['food','Restaurants & vie de ville','Tables, soirées et une base qui continue à vivre quand le sac de plage est rangé.'],
          ['culture','Art & villages','Musées, fondations, vieilles villes et détours dans les terres qui ont une raison d’exister.'],
          ['glamour','Glamour Riviera','Hôtels, belles soirées et un peu de théâtre. Aucune excuse nécessaire.'],
          ['peace','Calme & beauté','Une belle base avec le volume baissé.'],
          ['decide','Décidez pour moi','Aucune obsession dominante. Donnez-moi la logique la plus solide pour un premier séjour.']
        ]},
        {key:'pace',title:'À quel rythme voyagez-vous ?',deck:'Le rythme ne choisit pas vos goûts. Il décide combien la qualité du hub compte et combien de choses on vous autorise à tenter.',options:[
          ['slow','Lent','Moins de mouvements. La base doit mériter les heures que vous y passez.'],
          ['balanced','Équilibré','Une vraie base, quelques excursions fortes et aucune médaille pour l’épuisement.'],
          ['ambitious','Ambitieux','Vous voulez voir large. D’accord, mais la logistique doit se tenir.']
        ]}
      ],
      labels:{verdict:'LE VERDICT MAMETAS',do:'Ce qui mérite vos journées',cut:'LA COUPE MAMETAS',hotels:'Ensuite, choisissez le niveau d’hôtel',hotelNote:'Les symboles de prix sont des repères relatifs Mametas, jamais des tarifs en temps réel. Pratique / Confort / Grand plaisir décrivent le rôle de l’hôtel, pas une promesse de prix.',moreHotels:'Voir plus d’hôtels dans cette base',plan:'Ouvrir le plan utile',share:'Ouvrir ou partager ce résultat',override:'Vous avez contredit Mametas. Très bien.',backVerdict:'Revenir au verdict Mametas',escape:'Changer de base délibérément',priority:'Priorité',season:'Note saison'},
      tiers:{practical:'Pratique',comfort:'Confort',splurge:'Grand plaisir'},
      options:{days:{3:'3 jours',5:'5 jours',7:'7+ jours'},mobility:{nocar:'Sans voiture',car:'Voiture',either:'Peu importe'},mood:{sea:'Mer',food:'Restaurants & ville',culture:'Art & villages',glamour:'Glamour',peace:'Calme & beauté',decide:'Décidez pour moi'},pace:{slow:'Lent',balanced:'Équilibré',ambitious:'Ambitieux'}},
      base:{
        nice:{name:'Nice',headline:'Dormez à Nice.',intro:'Nice gagne quand le séjour a besoin d’amplitude sans faire de la logistique le personnage principal.',mood:{sea:'Gardez la mer dans la journée, pas forcément sous la fenêtre de l’hôtel.',food:'Restaurants, soirées et la vie de ville la plus complète rendent le choix assez simple.',culture:'Nice offre ses propres musées et le meilleur lancement pour les détours culturels autour.',glamour:'Vous gardez de très beaux hôtels et des soirées, avec Monaco en spectacle plutôt qu’en code postal.',peace:'Ce n’est pas la réponse la plus calme, mais elle peut gagner quand mobilité et amplitude comptent davantage.',decide:'Pour un premier séjour sans obsession dominante, il n’y a pas de réponse plus maligne.'}},
        cannes:{name:'Cannes',headline:'Dormez à Cannes.',intro:'Cannes fonctionne quand l’ouest de la Riviera, le sable et une vie d’hôtel plus soignée appartiennent au même voyage.',mood:{sea:'Sable, plage et côte ouest facile donnent l’avantage à Cannes.',food:'Vous gardez une vraie base le soir sans sacrifier la côte autour.',culture:'La culture n’est pas le meilleur argument de Cannes ; le reste de votre profil fait gagner la ville.',glamour:'Vous avez demandé du théâtre Riviera. Cannes donne hôtels, sable et une côte qui reste praticable.',peace:'Cannes n’est pas notre réponse calme par défaut ; autre chose dans votre profil travaille fort.',decide:'C’est la base ouest plus soignée quand l’équilibre général pointe ici.'}},
        antibes:{name:'Antibes',headline:'Dormez à Antibes.',intro:'Antibes est le milieu juste : vraie ville, vieilles rues, vraie plage et moins de cérémonie que Cannes.',mood:{sea:'Une baignade de sable collée à une vraie vieille ville est un argument remarquablement efficace.',food:'La ville reste utile après la plage sans exiger l’énergie urbaine de Nice.',culture:'Picasso, la vieille ville et l’accès facile à l’ouest donnent assez de matière sans transformer le séjour en devoir.',glamour:'Il y a du vernis, mais moins de représentation. Cela peut être la meilleure version de Riviera.',peace:'Antibes donne de l’air sans se retirer de la côte.',decide:'Quand l’équilibre compte plus que le maximum de quoi que ce soit, Antibes survit très bien à l’édition.'}},
        villefranche:{name:'Villefranche / Beaulieu',headline:'Dormez à Villefranche ou Beaulieu.',intro:'C’est la réponse quand la beauté et la mer comptent plus que l’idée de gérer la côte comme un projet de transport.',mood:{sea:'La rade n’est pas un accompagnement ici. Construisez le séjour autour de l’eau et arrêtez de vous excuser.',food:'La scène food est plus petite ; cette base ne gagne que si d’autres réponses tirent fort.',culture:'Nice reste assez proche pour la culture ; la base elle-même se choisit pour la beauté, pas la densité muséale.',glamour:'Pensez Riviera plus discrète, pas théâtre de Croisette.',peace:'Vous avez demandé la beauté avec le volume baissé. C’est exactement le brief.',decide:'Cette base ne bat les grands hubs que si votre rythme lui permet de compter davantage.'}},
        menton:{name:'Menton',headline:'Dormez à Menton.',intro:'Menton a du sens quand la Riviera doit être plus douce, plus lente et un peu moins intéressée par sa propre mise en scène.',mood:{sea:'La mer fait partie du rythme plutôt que d’un projet de beach club.',food:'Il y a assez de vie de ville pour porter le séjour, avec l’Italie qui influence discrètement l’ambiance.',culture:'Jardins, vieille ville et Cocteau donnent à l’est plus de substance qu’un simple argument de couleurs.',glamour:'C’est l’élégance à volume plus bas, pas le théâtre monégasque.',peace:'Vous avez demandé du calme sans disparaître de la civilisation. Menton prend le brief au sérieux.',decide:'Menton ne gagne que lorsque vos réponses préfèrent clairement cette version orientale et plus lente.'}},
        monaco:{name:'Monaco',headline:'Dormez à Monaco.',intro:'C’est une réponse intentionnelle. Vous n’avez pas demandé la base la plus flexible ; vous avez demandé que Monaco fasse partie de l’expérience.',mood:{glamour:'Sur un séjour long et lent, palace, restaurants et spectacle justifient enfin le code postal.',food:'Monaco peut porter de très grandes tables, mais la food seule suffit rarement à gagner la décision de base.',sea:'La mer existe ; ce n’est pas pour elle qu’on vous envoie ici.',culture:'Il y a plus de culture que ne le suggère le comptage des Ferrari, mais cela reste un séjour intentionnel.',peace:'Si le brief était le calme, Monaco n’a pas bien lu la consigne.',decide:'Mametas ne choisit jamais Monaco par accident.'}},
        'saint-tropez':{name:'Saint-Tropez',headline:'Dormez à Saint-Tropez.',intro:'Vous avez assez de temps, une voiture et une vraie raison de faire de la presqu’île le voyage plutôt qu’une excursion pénible.',mood:{glamour:'C’est le profil rare où Saint-Tropez cesse d’être une excursion et devient le sujet.',sea:'La presqu’île mérite la base quand la plage est centrale et que la voiture ouvre la géographie.',food:'Les restaurants aident, mais ils ne suffisent pas seuls à justifier la logistique.',culture:'Ce n’est pas la réponse culture-first.',peace:'Le calme existe sur la presqu’île, mais Saint-Tropez reste un engagement volontaire.',decide:'Mametas n’envoie pas ici un premier visiteur indécis.'}},
        'saint-paul':{name:'Saint-Paul-de-Vence',headline:'Dormez à Saint-Paul-de-Vence.',intro:'C’est un engagement dans les terres, pas un joli détour déguisé en base.',mood:{culture:'Avec voiture, assez de jours et un rythme lent, Maeght, le village et les soirées intérieures peuvent enfin justifier d’y dormir.',peace:'Le calme est réel, mais la côte devient une sortie volontaire plutôt que le décor par défaut.',sea:'Mauvais brief. La Méditerranée est désormais un trajet.',food:'Il y a de bonnes tables, mais la food seule n’en fait pas la base.',glamour:'Ici, le glamour ressemble davantage à une retraite de pierre et d’hôtel qu’aux lumières de la Croisette.',decide:'Un premier séjour indécis ne devrait pas commencer en se cachant dans les terres.'}}
      },
      cuts:{
        nice:{short:'Saint-Tropez. Trois jours ne sont pas le moment de consacrer une journée à prouver que vous pouvez y arriver.',normal:'Saint-Tropez, sauf si c’est la raison du voyage. La côte ne distribue pas de certificat d’assiduité.'},
        cannes:{short:'Monaco et Menton. Vous avez choisi l’ouest ; faites-en une décision.',normal:'N’ajoutez pas tout l’est simplement parce que les trains existent. Cannes vous donne déjà un côté.'},
        antibes:{short:'Cannes en ajout automatique. Le fait que le train continue n’est pas une consigne.',normal:'Un ajout à l’ouest suffit. La proximité n’est pas une obligation.'},
        villefranche:{short:'Essayer de collectionner les deux extrémités de la Riviera. Le sujet de cette base est justement de ralentir la géographie.',normal:'Saint-Tropez. Vous avez choisi la beauté et une côte plus lente, pas une démonstration de logistique.'},
        menton:{short:'Cannes. Trois jours depuis Menton ne doivent pas devenir une navette sur toute la côte.',normal:'Cannes en ajout automatique. Vous avez volontairement choisi l’extrémité est ; utilisez-la.'},
        monaco:{short:'Essayer d’utiliser Monaco comme astuce de transport. Dormez-y parce que vous voulez Monaco.',normal:'Transformer Monaco en hub pour toute la côte. Le code postal n’a de sens que si Monaco compte vraiment.'},
        'saint-tropez':{short:'Rien. Mametas ne vous mettrait pas ici pour trois jours.',normal:'Nice et Monaco en excursions. Vous avez choisi la presqu’île ; arrêtez de faire la navette vers un autre voyage.'},
        'saint-paul':{short:'Rien. Cette base n’est pas une recommandation de premier séjour sur trois jours.',normal:'Faire des plages tous les jours. Cette base ne fonctionne que si art, pierre et calme intérieur sont vraiment le sujet.'}
      },
      pace:{slow:'Votre rythme lent réduit la valeur d’un hub parfait. On laisse la base elle-même faire davantage du travail.',balanced:'Équilibré garde la logistique utile sans laisser les horaires choisir toutes les vacances.',ambitious:'Ambitieux augmente la valeur d’un bon hub. Vous voulez voir large, donc la base doit bien bouger.'},
      escape:{monaco:'En fait, je veux que Monte-Carlo et les palaces soient le voyage.', 'saint-tropez':'En fait, Saint-Tropez est le sujet des vacances.', 'saint-paul':'En fait, je veux le séjour art et villages dans les terres.', nice:'Préférer la base polyvalente et plus flexible.',cannes:'Préférer la base ouest plus flexible.',antibes:'Préférer la base ouest avec moins de friction.',villefranche:'Préférer la beauté sans l’engagement d’une base intentionnelle.',menton:'Préférer la base orientale calme par défaut.'}
    }
  };

  var TRIPS={
    nice:{
      local:{title:{en:'Give Nice a proper day',fr:'Donnez une vraie journée à Nice'},copy:{en:'Old Nice, Castle Hill, market, sea. A base is not a station with restaurants.',fr:'Vieux-Nice, Colline du Château, marché, mer. Une base n’est pas une gare avec des restaurants.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      villefranche:{title:{en:'Villefranche + one Cap-Ferrat idea',fr:'Villefranche + une seule idée au Cap-Ferrat'},copy:{en:'Bay, swim, then choose walk, garden or long lunch.',fr:'Rade, baignade, puis choisissez : sentier, jardin ou long déjeuner.'},href:{en:'/en/riviera-guide/villefranche-cap-ferrat/',fr:'/riviera-guide/villefranche-cap-ferrat/'}},
      east:{title:{en:'Monaco + Menton, edited',fr:'Monaco + Menton, mais édités'},copy:{en:'Spectacle first, softer old town after. Two stops are enough.',fr:'Le spectacle d’abord, la vieille ville plus douce ensuite. Deux arrêts suffisent.'},href:{en:'/en/day-trips/nice-to-menton-by-train/',fr:'/escapades/nice-menton-en-train/'}},
      antibes:{title:{en:'Antibes for the western counterpoint',fr:'Antibes pour le contrepoint à l’ouest'},copy:{en:'Old town, Picasso and sand without a Cannes-level commitment to polish.',fr:'Vieille ville, Picasso et sable sans engagement cannois envers le vernis.'},href:{en:'/en/riviera-guide/antibes/',fr:'/riviera-guide/antibes/'}},
      eze:{title:{en:'Èze, if the hilltop is the point',fr:'Èze, si le village perché est le sujet'},copy:{en:'Bus, gradient and crowds included. The panorama still makes a case.',fr:'Bus, pente et foule compris. Le panorama conserve de solides arguments.'},href:{en:'/en/riviera-guide/eze/',fr:'/riviera-guide/eze/'}},
      saintpaul:{title:{en:'Saint-Paul when art matters',fr:'Saint-Paul quand l’art compte'},copy:{en:'Village plus Fondation Maeght. Do not bolt it onto an already full day.',fr:'Village plus Fondation Maeght. Ne le greffez pas sur une journée déjà pleine.'},href:{en:'/en/riviera-guide/saint-paul-de-vence/',fr:'/riviera-guide/saint-paul-de-vence/'}},
      cannes:{title:{en:'Cannes, only if you want Cannes',fr:'Cannes, seulement si vous voulez Cannes'},copy:{en:'Croisette, Suquet and beach. Proximity is not an instruction.',fr:'Croisette, Suquet et plage. La proximité n’est pas une consigne.'},href:{en:'/en/riviera-guide/cannes/',fr:'/riviera-guide/cannes/'}},
      orders:{decide:['local','villefranche','east','antibes','eze'],sea:['local','villefranche','antibes','eze','east'],food:['local','antibes','east','cannes'],culture:['local','saintpaul','antibes','eze','east'],glamour:['local','cannes','east','villefranche'],peace:['villefranche','local','eze','east','antibes']}
    },
    cannes:{
      local:{title:{en:'Do Cannes properly',fr:'Faites vraiment Cannes'},copy:{en:'Forville, Le Suquet, Croisette. The town needs more than a red-carpet joke.',fr:'Forville, Le Suquet, Croisette. La ville mérite mieux qu’une blague de tapis rouge.'},href:{en:'/en/riviera-guide/cannes/',fr:'/riviera-guide/cannes/'}},
      lerins:{title:{en:'Take the boat to Lérins',fr:'Prenez le bateau pour Lérins'},copy:{en:'A short crossing changes the mood more than another hour on the Croisette.',fr:'Une courte traversée change davantage l’ambiance qu’une heure de plus sur la Croisette.'},href:{en:'/en/day-trips/iles-de-lerins/',fr:'/escapades/iles-de-lerins/'}},
      antibes:{title:{en:'Antibes for old-town balance',fr:'Antibes pour l’équilibre vieille ville'},copy:{en:'A useful train hop when you want less polish and more stone, market and beach.',fr:'Un saut de train utile pour moins de vernis et davantage de pierre, marché et plage.'},href:{en:'/en/riviera-guide/antibes/',fr:'/riviera-guide/antibes/'}},
      saintpaul:{title:{en:'Saint-Paul for the inland day',fr:'Saint-Paul pour la journée intérieure'},copy:{en:'Art and stone are a better contrast than collecting another seafront.',fr:'Art et pierre offrent un meilleur contraste que de collectionner un front de mer de plus.'},href:{en:'/en/riviera-guide/saint-paul-de-vence/',fr:'/riviera-guide/saint-paul-de-vence/'}},
      nice:{title:{en:'Nice only if city life matters',fr:'Nice seulement si la vie de ville compte'},copy:{en:'Go for the city, not because the TER makes it easy.',fr:'Allez-y pour la ville, pas parce que le TER rend le trajet facile.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      beach:{title:{en:'Protect a real beach half-day',fr:'Protégez une vraie demi-journée plage'},copy:{en:'Cannes has sand. It would be strange to choose it and never use it.',fr:'Cannes a du sable. Il serait étrange de la choisir et de ne jamais l’utiliser.'},href:{en:'/en/beaches/',fr:'/plages/'}},
      orders:{decide:['local','lerins','antibes','saintpaul','beach'],sea:['beach','lerins','local','antibes'],food:['local','antibes','nice','lerins'],culture:['saintpaul','antibes','local','nice'],glamour:['local','beach','lerins','antibes'],peace:['lerins','local','saintpaul','beach']}
    },
    antibes:{
      local:{title:{en:'Old Antibes + Picasso + a swim',fr:'Vieil Antibes + Picasso + une baignade'},copy:{en:'The essentials fit together. That is the whole advantage.',fr:'Les essentiels tiennent ensemble. C’est tout l’avantage.'},href:{en:'/en/riviera-guide/antibes/',fr:'/riviera-guide/antibes/'}},
      cap:{title:{en:'Give Cap d’Antibes its own rhythm',fr:'Donnez son propre rythme au Cap d’Antibes'},copy:{en:'Coves and coastal paths deserve time, not a rushed add-on before dinner.',fr:'Criques et sentiers méritent du temps, pas un ajout pressé avant dîner.'},href:{en:'/en/beaches/antibes/',fr:'/plages/antibes/'}},
      cannes:{title:{en:'Cannes when you want the theatre',fr:'Cannes quand vous voulez le théâtre'},copy:{en:'One easy train stop west. Go because you want Cannes, not because it is there.',fr:'Un arrêt de train facile vers l’ouest. Allez-y parce que vous voulez Cannes.'},href:{en:'/en/riviera-guide/cannes/',fr:'/riviera-guide/cannes/'}},
      nice:{title:{en:'Nice for the bigger-city day',fr:'Nice pour la journée plus urbaine'},copy:{en:'Food, museums and a different scale when Antibes starts feeling too well behaved.',fr:'Restaurants, musées et autre échelle quand Antibes devient trop sage.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      saintpaul:{title:{en:'Saint-Paul + Maeght',fr:'Saint-Paul + Maeght'},copy:{en:'The inland contrast when culture matters more than another beach.',fr:'Le contraste intérieur quand la culture compte plus qu’une plage supplémentaire.'},href:{en:'/en/riviera-guide/saint-paul-de-vence/',fr:'/riviera-guide/saint-paul-de-vence/'}},
      orders:{decide:['local','cap','cannes','nice'],sea:['local','cap','cannes'],food:['local','nice','cannes'],culture:['local','saintpaul','nice','cannes'],glamour:['cap','cannes','local'],peace:['cap','local','saintpaul']}
    },
    villefranche:{
      local:{title:{en:'Let the bay be the programme',fr:'Laissez la rade devenir le programme'},copy:{en:'Old town, harbour, swim and one long lunch. This is not wasted time.',fr:'Vieille ville, port, baignade et un long déjeuner. Ce n’est pas du temps perdu.'},href:{en:'/en/riviera-guide/villefranche-cap-ferrat/',fr:'/riviera-guide/villefranche-cap-ferrat/'}},
      cap:{title:{en:'One Cap-Ferrat objective',fr:'Un seul objectif au Cap-Ferrat'},copy:{en:'Walk, villa or beach. Three at once turns elegance into endurance.',fr:'Sentier, villa ou plage. Les trois d’un coup transforment vite l’élégance en endurance.'},href:{en:'/en/day-trips/cap-ferrat-a-pied/',fr:'/escapades/cap-ferrat-a-pied/'}},
      nice:{title:{en:'Use Nice for the city day',fr:'Utilisez Nice pour la journée de ville'},copy:{en:'Museums, market and evening energy are close enough without needing to sleep there.',fr:'Musées, marché et énergie du soir restent assez proches sans devoir y dormir.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      eze:{title:{en:'Èze for the vertical contrast',fr:'Èze pour le contraste vertical'},copy:{en:'Go early or later. Hilltop beauty is less persuasive behind six tour groups.',fr:'Allez-y tôt ou plus tard. La beauté perchée convainc moins derrière six groupes.'},href:{en:'/en/riviera-guide/eze/',fr:'/riviera-guide/eze/'}},
      east:{title:{en:'Monaco or Menton, not both by reflex',fr:'Monaco ou Menton, pas les deux par réflexe'},copy:{en:'Pick spectacle or softness according to the day.',fr:'Choisissez spectacle ou douceur selon la journée.'},href:{en:'/en/riviera-guide/monaco/',fr:'/riviera-guide/monaco/'}},
      orders:{decide:['local','cap','nice','eze'],sea:['local','cap','eze'],food:['nice','local','east'],culture:['nice','eze','east','local'],glamour:['local','east','cap'],peace:['local','cap','eze','nice']}
    },
    menton:{
      local:{title:{en:'Give Menton the slow day it deserves',fr:'Donnez à Menton la journée lente qu’elle mérite'},copy:{en:'Old town, Saint-Michel, garden or Cocteau, then sea. No need to optimise it to death.',fr:'Vieille ville, Saint-Michel, jardin ou Cocteau, puis mer. Inutile de l’optimiser à mort.'},href:{en:'/en/riviera-guide/menton/',fr:'/riviera-guide/menton/'}},
      monaco:{title:{en:'Monaco for spectacle',fr:'Monaco pour le spectacle'},copy:{en:'The Rock, one major attraction, Monte-Carlo. Edit hard and come back east.',fr:'Le Rocher, une grande visite, Monte-Carlo. Éditez franchement puis revenez vers l’est.'},href:{en:'/en/riviera-guide/monaco/',fr:'/riviera-guide/monaco/'}},
      eze:{title:{en:'Èze when the hilltop matters',fr:'Èze quand le village perché compte'},copy:{en:'A vertical change of mood between Menton softness and Nice energy.',fr:'Un changement vertical d’ambiance entre la douceur de Menton et l’énergie de Nice.'},href:{en:'/en/riviera-guide/eze/',fr:'/riviera-guide/eze/'}},
      villefranche:{title:{en:'Villefranche for the bay day',fr:'Villefranche pour la journée rade'},copy:{en:'A beautiful westward excursion before the distances start becoming silly.',fr:'Une belle excursion vers l’ouest avant que les distances deviennent absurdes.'},href:{en:'/en/riviera-guide/villefranche-cap-ferrat/',fr:'/riviera-guide/villefranche-cap-ferrat/'}},
      nice:{title:{en:'Nice, once, for scale',fr:'Nice, une fois, pour changer d’échelle'},copy:{en:'City life and museums are worth one deliberate day, not a daily commute.',fr:'Vie de ville et musées valent une journée volontaire, pas une navette quotidienne.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      orders:{decide:['local','monaco','eze','villefranche'],sea:['local','villefranche','monaco'],food:['local','nice','monaco'],culture:['local','monaco','eze','nice'],glamour:['monaco','local','nice'],peace:['local','eze','villefranche','monaco']}
    },
    monaco:{
      local:{title:{en:'Do Monaco from the inside',fr:'Faites Monaco de l’intérieur'},copy:{en:'The Rock, museum or palace, harbour and Monte-Carlo. You are sleeping here, so stop rushing it.',fr:'Rocher, musée ou palais, port et Monte-Carlo. Vous dormez ici, donc arrêtez de courir.'},href:{en:'/en/riviera-guide/monaco/',fr:'/riviera-guide/monaco/'}},
      menton:{title:{en:'Menton to exhale',fr:'Menton pour expirer'},copy:{en:'A softer eastbound day is the right counterweight to Monaco ceremony.',fr:'Une journée plus douce vers l’est est le bon contrepoids au cérémonial monégasque.'},href:{en:'/en/riviera-guide/menton/',fr:'/riviera-guide/menton/'}},
      eze:{title:{en:'Èze early or late',fr:'Èze tôt ou tard'},copy:{en:'The hilltop is close enough to be useful, crowded enough to require timing.',fr:'Le village est assez proche pour être utile, assez fréquenté pour exiger un peu de timing.'},href:{en:'/en/riviera-guide/eze/',fr:'/riviera-guide/eze/'}},
      villefranche:{title:{en:'Villefranche for water and less theatre',fr:'Villefranche pour l’eau et moins de théâtre'},copy:{en:'The bay makes a very good antidote to polished Monaco.',fr:'La rade constitue un excellent antidote au Monaco très poli.'},href:{en:'/en/riviera-guide/villefranche-cap-ferrat/',fr:'/riviera-guide/villefranche-cap-ferrat/'}},
      nice:{title:{en:'Nice if you need a real city day',fr:'Nice si vous avez besoin d’une vraie journée de ville'},copy:{en:'Go once for scale, food and culture. Do not turn Monaco into a commuter suburb.',fr:'Allez-y une fois pour l’échelle, la food et la culture. Ne transformez pas Monaco en banlieue pendulaire.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      orders:{decide:['local','menton','eze'],sea:['villefranche','menton','local'],food:['local','nice','menton'],culture:['local','nice','eze','menton'],glamour:['local','menton','eze','villefranche'],peace:['menton','villefranche','eze','local']}
    },
    'saint-tropez':{
      local:{title:{en:'Give Saint-Tropez a day without a car plan',fr:'Donnez une journée à Saint-Tropez sans plan voiture'},copy:{en:'Port, old town, Place des Lices and time after the day-trippers thin out.',fr:'Port, vieille ville, place des Lices et du temps après le départ des visiteurs à la journée.'},href:{en:'/en/riviera-guide/saint-tropez/',fr:'/riviera-guide/saint-tropez/'}},
      beach:{title:{en:'Make Pampelonne an actual beach day',fr:'Faites de Pampelonne une vraie journée plage'},copy:{en:'If the beach is the reason, stop squeezing it between village errands.',fr:'Si la plage est la raison, arrêtez de la coincer entre deux obligations de village.'},href:{en:'/en/beaches/saint-tropez/',fr:'/plages/saint-tropez/'}},
      slow:{title:{en:'Protect one peninsula day with no ambition',fr:'Protégez une journée de presqu’île sans ambition'},copy:{en:'Long lunch, one cove, one village. You chose this base to stop commuting.',fr:'Long déjeuner, une crique, un village. Vous avez choisi cette base pour arrêter les navettes.'},href:{en:'/en/riviera-guide/saint-tropez/',fr:'/riviera-guide/saint-tropez/'}},
      cannes:{title:{en:'One western change of scene, at most',fr:'Un changement de décor à l’ouest, au maximum'},copy:{en:'Cannes or Antibes can be a deliberate day, not a daily rescue mission.',fr:'Cannes ou Antibes peuvent devenir une journée volontaire, pas une mission de secours quotidienne.'},href:{en:'/en/riviera-guide/cannes/',fr:'/riviera-guide/cannes/'}},
      orders:{decide:['local','beach','slow'],sea:['beach','local','slow'],food:['local','slow','beach'],culture:['local','cannes','slow'],glamour:['local','beach','slow'],peace:['slow','beach','local']}
    },
    'saint-paul':{
      local:{title:{en:'Let Saint-Paul exist after the buses leave',fr:'Laissez Saint-Paul exister après le départ des cars'},copy:{en:'Village, evening and morning are the whole reason to sleep here.',fr:'Village, soirée et matin sont toute la raison d’y dormir.'},href:{en:'/en/riviera-guide/saint-paul-de-vence/',fr:'/riviera-guide/saint-paul-de-vence/'}},
      maeght:{title:{en:'Give Fondation Maeght real time',fr:'Donnez du vrai temps à la Fondation Maeght'},copy:{en:'Do not reduce one of the coast’s strongest art stops to the gap before lunch.',fr:'Ne réduisez pas l’un des meilleurs arrêts d’art de la côte au trou avant déjeuner.'},href:{en:'/en/culture/fondation-maeght/',fr:'/culture/fondation-maeght/'}},
      nice:{title:{en:'Nice for one coast-and-city day',fr:'Nice pour une journée côte et ville'},copy:{en:'The sea and city scale make the right contrast when you are based inland.',fr:'La mer et l’échelle urbaine offrent le bon contraste quand vous dormez dans les terres.'},href:{en:'/en/riviera-guide/nice/',fr:'/riviera-guide/nice/'}},
      antibes:{title:{en:'Antibes for sea + old town',fr:'Antibes pour mer + vieille ville'},copy:{en:'A western coastal day that does not require full Cannes theatre.',fr:'Une journée côtière à l’ouest sans exiger tout le théâtre cannois.'},href:{en:'/en/riviera-guide/antibes/',fr:'/riviera-guide/antibes/'}},
      orders:{decide:['local','maeght','nice'],sea:['antibes','nice','local'],food:['local','nice','antibes'],culture:['maeght','local','nice','antibes'],glamour:['local','maeght','nice'],peace:['local','maeght','nice']}
    }
  };

  function validState(s){
    return ['3','5','7'].indexOf(String(s.days))>=0 &&
      ['nocar','car','either'].indexOf(s.mobility)>=0 &&
      ['sea','food','culture','glamour','peace','decide'].indexOf(s.mood)>=0 &&
      ['slow','balanced','ambitious'].indexOf(s.pace)>=0;
  }
  function eligible(base,days,mobility){
    if(days===3 && ['saint-tropez','saint-paul'].indexOf(base)>=0) return false;
    if(mobility==='nocar' && base==='saint-tropez') return false;
    return true;
  }
  function moodScore(d,mood){
    if(mood==='decide') return .9*d.sea+1.15*d.food+1.15*d.culture+.35*d.glamour+.6*d.peace;
    return 2.8*d[mood]+.20*d.food+.16*d.culture+.12*d.sea+.10*d.peace;
  }
  function intentionalCanWin(base,s){
    var days=Number(s.days);
    if(s.mood==='decide') return false;
    if(base==='monaco') return days>=7 && s.mood==='glamour' && s.pace==='slow';
    if(base==='saint-tropez') return days>=7 && s.mobility==='car' && ['glamour','sea'].indexOf(s.mood)>=0 && ['slow','balanced'].indexOf(s.pace)>=0;
    if(base==='saint-paul') return days>=7 && s.mobility==='car' && s.mood==='culture' && s.pace==='slow';
    return false;
  }
  function decision(s){
    var days=Number(s.days),scores={},bestDefault=null,bestDefaultScore=-Infinity;
    Object.keys(MATRIX).forEach(function(base){
      if(!eligible(base,days,s.mobility)) return;
      var d=MATRIX[base];
      var score=moodScore(d,s.mood)+PACE_HUB[s.pace]*d.hub+MOBILITY[s.mobility][base]+DAYS[days][base];
      scores[base]=score;
      if(d.type==='default'){
        if(score>bestDefaultScore+.0001 || (Math.abs(score-bestDefaultScore)<=.0001 && DEFAULT_ORDER.indexOf(base)<DEFAULT_ORDER.indexOf(bestDefault))){
          bestDefault=base;bestDefaultScore=score;
        }
      }
    });
    var winner=bestDefault;
    Object.keys(scores).forEach(function(base){
      if(MATRIX[base].type!=='intentional' || !intentionalCanWin(base,s)) return;
      if(scores[base]>=bestDefaultScore+(INTENT_MARGIN[base]||.5) && scores[base]>scores[winner]) winner=base;
    });
    var escape=null;
    if(MATRIX[winner].type==='intentional'){
      escape=bestDefault;
    }else{
      Object.keys(scores).forEach(function(base){
        if(MATRIX[base].type!=='intentional' || base===winner) return;
        if((INTENT_TRIGGERS[base]||[]).indexOf(s.mood)<0) return;
        if(scores[base] < bestDefaultScore-1.15) return;
        if(!escape || scores[base]>scores[escape]) escape=base;
      });
    }
    return {winner:winner,defaultWinner:bestDefault,escape:escape,scores:scores};
  }
  function limitFor(s){
    var d=Number(s.days);
    if(d===3) return s.pace==='slow'?2:3;
    if(d===5) return s.pace==='slow'?3:4;
    return s.pace==='ambitious'?5:4;
  }
  function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function baseCopy(lang,base,s){
    var c=COPY[lang],b=c.base[base];
    return b.intro+' '+(b.mood[s.mood]||b.mood.decide)+' '+c.pace[s.pace];
  }
  function getPriorities(base,s,lang){
    var group=TRIPS[base],order=(group.orders[s.mood]||group.orders.decide).slice(0,limitFor(s));
    return order.map(function(id){var item=group[id];return {title:item.title[lang],copy:item.copy[lang],href:item.href[lang]};});
  }
  function profileHtml(c,s){
    return '<div class="chooser-profile">'+
      '<span>'+esc(c.options.days[s.days])+'</span>'+
      '<span>'+esc(c.options.mobility[s.mobility])+'</span>'+
      '<span>'+esc(c.options.mood[s.mood])+'</span>'+
      '<span>'+esc(c.options.pace[s.pace])+'</span>'+
    '</div>';
  }
  function finderUrl(lang,base,s){
    var path=lang==='fr'?'/hotels/finder/':'/en/hotels/finder/';
    var q='?base='+encodeURIComponent(base)+'&from=chooser';
    if(s.mobility==='nocar') q+='&mobility=nocar';
    return path+q;
  }
  function shareUrl(lang,s){
    var path=lang==='fr'?'/riviera-chooser/':'/en/riviera-chooser/';
    return path+'?days='+encodeURIComponent(s.days)+'&mobility='+encodeURIComponent(s.mobility)+'&mood='+encodeURIComponent(s.mood)+'&pace='+encodeURIComponent(s.pace);
  }
  function planUrl(lang,base,s){
    if(base==='nice'){
      if(lang==='fr') return '/fr/planifier/cinq-jours-nice-sans-voiture/';
      return '/plan/five-days-nice-no-car/';
    }
    var pages={
      cannes:{en:'/en/riviera-guide/cannes/',fr:'/riviera-guide/cannes/'},
      antibes:{en:'/en/riviera-guide/antibes/',fr:'/riviera-guide/antibes/'},
      villefranche:{en:'/en/riviera-guide/villefranche-cap-ferrat/',fr:'/riviera-guide/villefranche-cap-ferrat/'},
      menton:{en:'/en/riviera-guide/menton/',fr:'/riviera-guide/menton/'},
      monaco:{en:'/en/riviera-guide/monaco/',fr:'/riviera-guide/monaco/'},
      'saint-tropez':{en:'/en/riviera-guide/saint-tropez/',fr:'/riviera-guide/saint-tropez/'},
      'saint-paul':{en:'/en/riviera-guide/saint-paul-de-vence/',fr:'/riviera-guide/saint-paul-de-vence/'}
    };
    return pages[base][lang];
  }
  function hotelCards(lang,base,c){
    var source=window.MametasHotelTiers;
    if(!source || !source.bases[base]) return '';
    return ['practical','comfort','splurge'].map(function(tier){
      var h=source.get(base,tier); if(!h) return '';
      return '<article class="chooser-hotel">'+
        '<div class="chooser-hotel-meta"><span class="chooser-hotel-tier">'+esc(c.tiers[tier])+'</span><span class="chooser-hotel-price">'+esc(source.price(h.priceBand))+'</span></div>'+
        '<h4>'+esc(h.name)+'</h4>'+
        '<p><strong>'+esc(lang==='fr'?'Pourquoi':'Why')+'.</strong> '+esc(h.why[lang])+'</p>'+
        '<p class="chooser-hotel-catch"><strong>'+esc(lang==='fr'?'Le compromis':'The catch')+'.</strong> '+esc(h.catch[lang])+'</p>'+
        '<a href="'+esc(h.href[lang])+'">'+esc(lang==='fr'?'Voir cette adresse →':'See this hotel →')+'</a>'+
      '</article>';
    }).join('');
  }
  function resultHtml(root,lang,s,forcedBase){
    var c=COPY[lang],d=decision(s),base=forcedBase||d.winner,b=c.base[base];
    var priorities=getPriorities(base,s,lang);
    var cut=(c.cuts[base]||c.cuts.nice)[Number(s.days)===3?'short':'normal'];
    var hotels=hotelCards(lang,base,c);
    var escape=forcedBase?d.winner:d.escape;
    if(escape===base) escape=null;
    var escapeHtml='';
    if(escape && c.base[escape]){
      var text=c.escape[escape]||c.base[escape].headline;
      escapeHtml='<div class="chooser-escape"><p><strong>'+esc(c.labels.escape)+'.</strong> '+esc(text)+'</p><button type="button" data-chooser-escape="'+esc(escape)+'">'+esc(c.base[escape].headline.replace(/[.]$/,''))+' →</button></div>';
    }
    var backOverride=forcedBase?'<button class="chooser-back" type="button" data-chooser-restore>'+esc(c.labels.backVerdict)+'</button>':'';
    var priHtml=priorities.map(function(p,i){
      return '<a class="chooser-priority" href="'+esc(p.href)+'"><span>'+esc(c.labels.priority)+' '+String(i+1).padStart(2,'0')+'</span><strong>'+esc(p.title)+'</strong><p>'+esc(p.copy)+'</p></a>';
    }).join('');
    var resultLabel=forcedBase?c.labels.override:c.labels.verdict;
    return '<div class="chooser-result" aria-live="polite">'+
      '<div class="chooser-result-head"><div><p class="chooser-result-label">'+esc(resultLabel)+'</p><h3>'+esc(b.headline)+'</h3><p class="chooser-result-deck">'+esc(baseCopy(lang,base,s))+'</p>'+backOverride+'</div>'+profileHtml(c,s)+'</div>'+
      '<div><h4 class="chooser-subhead">'+esc(c.labels.do)+'</h4><div class="chooser-priorities">'+priHtml+'</div></div>'+
      '<div class="chooser-rule"><strong>'+esc(c.labels.cut)+'</strong><p>'+esc(cut)+'</p></div>'+
      (hotels?'<div class="chooser-hotels"><h4 class="chooser-subhead">'+esc(c.labels.hotels)+'</h4><div class="chooser-hotel-grid">'+hotels+'</div><p class="chooser-hotel-note">'+esc(c.labels.hotelNote)+'</p></div>':'')+
      escapeHtml+
      '<div class="chooser-actions"><a class="button" href="'+esc(planUrl(lang,base,s))+'">'+esc(c.labels.plan)+'</a><a class="button secondary" href="'+esc(finderUrl(lang,base,s))+'">'+esc(c.labels.moreHotels)+'</a></div>'+
      '<p class="chooser-share"><a href="'+esc(shareUrl(lang,s))+'">'+esc(c.labels.share)+' →</a></p>'+
    '</div>';
  }
  function optionButton(value,label,desc,key){
    return '<button class="chooser-option" type="button" data-chooser-answer="'+esc(value)+'" data-chooser-key="'+esc(key)+'"><strong>'+esc(label)+'</strong><span>'+esc(desc)+'</span></button>';
  }
  function renderQuestion(ctx){
    var q=ctx.c.questions[ctx.step],opts=q.options.map(function(o){return optionButton(o[0],o[1],o[2],q.key);}).join('');
    ctx.progress.textContent=ctx.c.progress(ctx.step+1);
    ctx.stage.innerHTML='<div class="chooser-question"><h3>'+esc(q.title)+'</h3><p>'+esc(q.deck)+'</p><div class="chooser-options">'+opts+'</div>'+(ctx.step?'<button class="chooser-back" type="button" data-chooser-back>'+esc(ctx.c.back)+'</button>':'')+'</div>';
  }
  function renderResult(ctx,forcedBase){
    ctx.progress.textContent=ctx.c.labels.verdict;
    ctx.stage.innerHTML=resultHtml(ctx.root,ctx.lang,ctx.state,forcedBase||null);
  }
  function reset(ctx){
    ctx.state={};ctx.step=0;ctx.forcedBase=null;renderQuestion(ctx);
  }
  function wire(root){
    var lang=(root.getAttribute('data-lang')||document.documentElement.lang||'en').toLowerCase().indexOf('fr')===0?'fr':'en';
    var ctx={root:root,lang:lang,c:COPY[lang],state:{},step:0,forcedBase:null,stage:root.querySelector('[data-chooser-stage]'),progress:root.querySelector('[data-chooser-progress]')};
    if(!ctx.stage || !ctx.progress) return;
    var params=new URLSearchParams(window.location.search);
    if(window.location.pathname.indexOf('riviera-chooser')>=0){
      ctx.state={days:params.get('days'),mobility:params.get('mobility'),mood:params.get('mood'),pace:params.get('pace')};
      if(validState(ctx.state)){ctx.step=4;renderResult(ctx);}else{ctx.state={};renderQuestion(ctx);}
    }else renderQuestion(ctx);
    root.addEventListener('click',function(e){
      var answer=e.target.closest('[data-chooser-answer]');
      if(answer){
        ctx.state[answer.getAttribute('data-chooser-key')]=answer.getAttribute('data-chooser-answer');
        ctx.step+=1;
        if(ctx.step>=4) renderResult(ctx); else renderQuestion(ctx);
        return;
      }
      if(e.target.closest('[data-chooser-back]')){
        ctx.step=Math.max(0,ctx.step-1);
        var key=ctx.c.questions[ctx.step].key; delete ctx.state[key];
        renderQuestion(ctx); return;
      }
      if(e.target.closest('[data-chooser-reset]')){reset(ctx);return;}
      var escapeBtn=e.target.closest('[data-chooser-escape]');
      if(escapeBtn){ctx.forcedBase=escapeBtn.getAttribute('data-chooser-escape');renderResult(ctx,ctx.forcedBase);return;}
      if(e.target.closest('[data-chooser-restore]')){ctx.forcedBase=null;renderResult(ctx);return;}
    });
  }
  ROOTS.forEach(wire);
})();