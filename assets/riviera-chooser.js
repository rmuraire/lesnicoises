(function (rootFactory) {
  var api = rootFactory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document !== 'undefined') api.mount();
  if (typeof process !== 'undefined' && process.argv && process.argv.indexOf('--self-test') >= 0) {
    api.selfTest();
  }
})(function () {
  'use strict';

  var BASES = {
    nice: { type:'default', hub:3, scores:{ decide:3, sea:2, food:3, culture:3, glamour:2, peace:1 } },
    cannes: { type:'default', hub:2.5, scores:{ decide:2.2, sea:3, food:2.2, culture:1.2, glamour:3, peace:1.2 } },
    antibes: { type:'default', hub:2.2, scores:{ decide:2.5, sea:3.15, food:2.2, culture:2.2, glamour:2, peace:2.2 } },
    villefranche: { type:'default', hub:1.5, scores:{ decide:1.9, sea:3.25, food:1.3, culture:1.3, glamour:2.1, peace:3.3 } },
    menton: { type:'default', hub:2, scores:{ decide:1.8, sea:2.1, food:2, culture:2.1, glamour:1.2, peace:3 } },
    monaco: { type:'intentional', hub:1.6, scores:{ decide:1, sea:1.2, food:2.8, culture:2, glamour:3, peace:1 } },
    sainttropez: { type:'intentional', hub:.5, scores:{ decide:.8, sea:3, food:2.4, culture:1, glamour:3, peace:1.5 } },
    saintpaul: { type:'intentional', hub:.5, scores:{ decide:1, sea:0, food:2, culture:3, glamour:2, peace:3 } }
  };

  var PACE_HUB = { slow:.25, balanced:1, ambitious:1.6 };
  var MOBILITY_HUB = { nocar:1.25, either:1, car:.65 };
  var DURATION_HUB = { '3':1.25, '5':1, '7':.8 };

  function scoreBase(id, profile) {
    var base = BASES[id];
    var hubWeight = PACE_HUB[profile.pace] * MOBILITY_HUB[profile.mobility] * DURATION_HUB[profile.days];
    var score = (base.scores[profile.mood] || 0) * 3 + base.hub * hubWeight;
    if (profile.days === '3' && id === 'nice') score += .5;
    return score;
  }

  function intentionalCandidates(profile) {
    var candidates = [];
    if (profile.mood === 'glamour' && profile.days === '7' && profile.pace === 'slow') {
      candidates.push({ id:'monaco', bonus:2.2 });
    }
    if ((profile.mood === 'sea' || profile.mood === 'glamour') &&
        profile.days === '7' && profile.mobility !== 'nocar' &&
        (profile.pace === 'slow' || profile.pace === 'balanced')) {
      candidates.push({ id:'sainttropez', bonus:3 });
    }
    if ((profile.mood === 'culture' || profile.mood === 'peace') &&
        profile.days === '7' && profile.mobility !== 'nocar' && profile.pace === 'slow') {
      candidates.push({ id:'saintpaul', bonus:2.5 });
    }
    return candidates;
  }

  function chooseBase(profile) {
    var defaults = Object.keys(BASES).filter(function (id) { return BASES[id].type === 'default'; })
      .map(function (id) { return { id:id, score:scoreBase(id, profile) }; })
      .sort(function (a,b) { return b.score - a.score || a.id.localeCompare(b.id); });
    var provisional = defaults[0];
    var intent = intentionalCandidates(profile)
      .map(function (item) { return { id:item.id, score:scoreBase(item.id, profile) + item.bonus }; })
      .sort(function (a,b) { return b.score - a.score; });
    for (var i=0; i<intent.length; i++) {
      if (intent[i].score >= provisional.score + 1) {
        return { base:intent[i].id, defaultBase:provisional.id, intentional:true };
      }
    }
    return { base:provisional.id, defaultBase:provisional.id, intentional:false };
  }

  var CONTENT = {
    en: {
      bases: {
        nice:{name:'Nice',guide:'/en/riviera-guide/nice/',hotels:'/stay/nice/',why:'The most useful all-round base on the coast. It gives you a real city at night and the strongest transport spine by day.'},
        cannes:{name:'Cannes',guide:'/en/riviera-guide/cannes/',hotels:'/en/hotels/cannes/',why:'The western Riviera works better from here when sand, polished hotels and an easier beach rhythm matter.'},
        antibes:{name:'Antibes / Juan-les-Pins',guide:'/en/riviera-guide/antibes/',hotels:'/en/hotels/antibes/',why:'Old town, sand and a useful station make this the rare Riviera compromise that does not feel like one.'},
        villefranche:{name:'Villefranche / Beaulieu',guide:'/en/riviera-guide/villefranche-cap-ferrat/',hotels:'/en/hotels/villefranche-sur-mer/',why:'Choose beauty and water first. You give up some hub efficiency in exchange for waking up somewhere that already feels like an excursion.'},
        menton:{name:'Menton',guide:'/en/riviera-guide/menton/',hotels:'/en/hotels/menton/',why:'The slower eastern base. It suits travellers who want colour, gardens and breathing room without losing the train entirely.'},
        monaco:{name:'Monaco',guide:'/en/riviera-guide/monaco/',hotels:'/en/hotels/monaco/',why:'This is the intentional version: stay because Monte-Carlo and the hotel experience are part of the point, not because it is the easiest answer.'},
        sainttropez:{name:'Saint-Tropez',guide:'/en/riviera-guide/saint-tropez/',hotels:'/en/hotels/saint-tropez/',why:'This is a commitment, not a clever central base. Your answers say the peninsula itself is the trip, so Mametas is letting it win.'},
        saintpaul:{name:'Saint-Paul-de-Vence',guide:'/en/riviera-guide/saint-paul-de-vence/',hotels:'/en/hotels/saint-paul-de-vence/',why:'An intentional inland stay for art, stone and a slower rhythm. It only wins when the coast is no longer the main character.'}
      },
      moodLine:{
        decide:'You asked us to decide, so we are choosing the trip with the fewest unnecessary compromises.',
        sea:'Your trip is being organised around swimming and the sea, not around collecting famous postcodes.',
        food:'Restaurants and a real evening atmosphere matter, so the base needs to keep working after the day trips come home.',
        culture:'Art and villages matter most, so access to strong cultural stops beats pure beach convenience.',
        glamour:'You want Riviera theatre. Fine. We still refuse to make logistics ridiculous for the sake of a lobby.',
        peace:'Beauty and quiet matter more than maximum connectivity, so we are deliberately accepting a little less efficiency.'
      },
      pace:{
        slow:'Slow means the base should do more of the work. Plan fewer departures and leave one half-day completely unclaimed.',
        balanced:'Balanced means two or three proper outings, with enough time left to enjoy the place you paid to sleep in.',
        ambitious:'Ambitious makes hub quality matter more. We are giving you efficient departures, not permission to turn the Riviera into a delivery route.'
      },
      priorities:{
        nice:{
          decide:['Nice properly','Villefranche + Cap-Ferrat','Antibes or Monaco/Menton'],
          sea:['A proper Nice swim','Villefranche + Cap-Ferrat','Antibes for sand'],
          food:['Nice markets + dinner','Antibes old town','One eastbound lunch day'],
          culture:['Matisse / Chagall in Nice','Saint-Paul + Fondation Maeght','Picasso in Antibes'],
          glamour:['A dressed-up Nice evening','Monaco as the spectacle day','Cannes for the western contrast'],
          peace:['Villefranche + Cap-Ferrat','Menton','One deliberately slow Nice day']
        },
        cannes:{
          decide:['Cannes + Le Suquet','Antibes','Lérins Islands'],
          sea:['Cannes beach time','Lérins Islands','Antibes / Juan-les-Pins'],
          food:['Forville + Le Suquet','Antibes dinner day','One properly chosen Cannes table'],
          culture:['Antibes + Picasso','Lérins Islands','Saint-Paul if you have a car'],
          glamour:['Croisette without apology','A hotel-led half-day','Antibes for contrast'],
          peace:['Lérins Islands','Théoule / Corniche d’Or if driving','Antibes at a slower pace']
        },
        antibes:{
          decide:['Old Antibes','Cannes','One Cap d’Antibes day'],
          sea:['La Gravette or Salis','Cap d’Antibes','Juan-les-Pins'],
          food:['Old Antibes','Cannes market + dinner','One long lunch instead of another town'],
          culture:['Picasso Museum','Saint-Paul if driving','Nice museums'],
          glamour:['Cap d’Antibes','Cannes','Juan-les-Pins after dark'],
          peace:['Cap d’Antibes','Old Antibes early','One beach day with no second stop']
        },
        villefranche:{
          decide:['Villefranche properly','Cap-Ferrat','Nice or Monaco, not both'],
          sea:['Villefranche bay','Cap-Ferrat coves','Beaulieu'],
          food:['Villefranche lunch','Nice dinner','One Monaco meal if you want theatre'],
          culture:['Nice museums','Èze','Monaco for a very different day'],
          glamour:['Cap-Ferrat','Monaco','One dressed-up Nice evening'],
          peace:['Villefranche bay','Cap-Ferrat on foot','Beaulieu with no agenda']
        },
        menton:{
          decide:['Menton properly','Monaco','One Nice day'],
          sea:['Menton seafront','Roquebrune-Cap-Martin','Monaco only if you want contrast'],
          food:['Menton','Monaco for one big meal','A market-led day with no train'],
          culture:['Cocteau in Menton','Monaco museums','Nice for the major collections'],
          glamour:['Monaco','A better hotel in Menton','Cap-Martin for the view'],
          peace:['Menton gardens','Roquebrune-Cap-Martin','One day with absolutely no westbound train']
        },
        monaco:{decide:['Monaco properly','Menton','Cap-Ferrat'],glamour:['Monte-Carlo properly','One palace / spa half-day','Menton for the exhale'],food:['Monaco restaurants','Menton','Nice for contrast']},
        sainttropez:{decide:['Saint-Tropez village','Pampelonne','Ramatuelle / the peninsula'],sea:['Pampelonne properly','One quieter peninsula beach','Saint-Tropez village late'],glamour:['Saint-Tropez village','A hotel-led afternoon','Pampelonne when you actually want the scene']},
        saintpaul:{decide:['Saint-Paul after the day-trippers','Fondation Maeght','Vence'],culture:['Fondation Maeght','Saint-Paul village','Vence / Matisse chapel'],peace:['Saint-Paul early and late','One long hotel afternoon','Vence or a single coast day']}
      },
      skips:{
        nice:'Skip Saint-Tropez unless it is genuinely one of the reasons you came. It eats too much of a short Riviera trip.',
        cannes:'Skip the automatic Monaco/Menton day. You chose the western Riviera; use it properly.',
        antibes:'Skip crossing the whole coast just because the train makes it technically possible.',
        villefranche:'Skip the western checklist. Cannes and Antibes can survive one trip without you.',
        menton:'Skip the Cannes-and-Antibes collection run. East is not a consolation prize.',
        monaco:'Skip using Monaco as a launch pad for daily coast-hopping. If you sleep here, let Monaco be part of the holiday.',
        sainttropez:'Skip the eastern Riviera this time. You chose the peninsula, so stop pretending Nice and Menton also need attendance.',
        saintpaul:'Skip daily coast commuting. The point of sleeping inland is to stop behaving as if the sea is taking attendance.'
      },
      hotels:{
        nice:[
          {tier:'Practical',price:'€€',name:'Hotel 66 Nice',note:'Station-friendly and built for easy departures.'},
          {tier:'Comfort',price:'€€€',name:'Hôtel Apollinaire Nice',note:'A strong all-rounder when centre and day trips both matter.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel du Couvent',note:'Choose it when the hotel is allowed to become part of the trip.'}
        ],
        cannes:[
          {tier:'Practical',price:'€€€',name:'Hôtel de Provence',note:'A smaller, calmer answer when you do not need palace scale.'},
          {tier:'Comfort',price:'€€€',name:'Le Cavendish',note:'Boutique Cannes with enough polish and less ceremony.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel Martinez',note:'The Croisette in full Riviera mode.'}
        ],
        antibes:[
          {tier:'Practical',price:'€',name:'Hôtel de l’Étoile',note:'Central and rational when the town matters more than the lobby.'},
          {tier:'Comfort',price:'€€€',name:'Royal Antibes',note:'Sea-facing without giving up walkable Antibes.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel Belles Rives',note:'Juan-les-Pins when Riviera history and the water are part of the point.'}
        ],
        villefranche:[
          {tier:'Practical',price:'€€',name:'Hôtel Le Provençal',note:'Village, station and bay before hotel theatre.'},
          {tier:'Comfort',price:'€€€',name:'Welcome Hotel',note:'The harbour fantasy, with the geography doing most of the seducing.'},
          {tier:'Splurge',price:'€€€€',name:'Grand-Hôtel du Cap-Ferrat',note:'The intentional Cap-Ferrat version, where the hotel becomes a destination.'}
        ],
        menton:[
          {tier:'Practical',price:'€',name:'ibis Roquebrune Cap Martin Menton',note:'A rational eastern base when the room is not the main event.'},
          {tier:'Comfort',price:'€€€',name:'Hôtel Napoléon',note:'Sea + pool for a slower stay without palace economics.'},
          {tier:'Splurge',price:'€€€€',name:'Villa Genesis',note:'Boutique luxury that fits Menton’s quieter rhythm.'}
        ],
        monaco:[
          {tier:'Practical',price:'€€€',name:'Columbus Hotel Monte-Carlo',note:'The less ceremonial Monaco answer.'},
          {tier:'Comfort',price:'€€€€',name:'Fairmont Monte Carlo',note:'Big-hotel Monaco with the spectacle close at hand.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel Hermitage Monte-Carlo',note:'Palace logic, deliberately chosen rather than accidentally inherited.'}
        ],
        sainttropez:[
          {tier:'Practical',price:'€€',name:'Hôtel Les Palmiers',note:'A more measured way to stay in the Gulf.'},
          {tier:'Comfort',price:'€€€',name:'La Ferme d’Augustin',note:'A softer peninsula stay when beach time matters.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel La Ponche',note:'Saint-Tropez itself, because in this version the postcode is part of the point.'}
        ],
        saintpaul:[
          {tier:'Practical',price:'€€',name:'Hôtel Les Messugues',note:'A quieter village-area stay without making the hotel the whole event.'},
          {tier:'Comfort',price:'€€€',name:'Toile Blanche',note:'Art-led, grown-up and suitably removed from the coastal machine.'},
          {tier:'Splurge',price:'€€€€',name:'Le Domaine du Mas de Pierre',note:'The retreat version, where staying in is a legitimate part of the plan.'}
        ]
      }
    },
    fr: {
      bases: {
        nice:{name:'Nice',guide:'/riviera-guide/nice/',hotels:'/fr/dormir/nice/',why:'La base la plus polyvalente de la côte. Une vraie ville le soir et le meilleur axe de transport pour rayonner la journée.'},
        cannes:{name:'Cannes',guide:'/riviera-guide/cannes/',hotels:'/hotels/cannes/',why:'L’ouest de la Riviera fonctionne mieux d’ici lorsque le sable, les beaux hôtels et un rythme plus balnéaire comptent.'},
        antibes:{name:'Antibes / Juan-les-Pins',guide:'/riviera-guide/antibes/',hotels:'/hotels/antibes/',why:'Vieille ville, sable et gare utile : l’un des rares compromis azuréens qui ne ressemble pas à un compromis.'},
        villefranche:{name:'Villefranche / Beaulieu',guide:'/riviera-guide/villefranche-cap-ferrat/',hotels:'/hotels/villefranche-sur-mer/',why:'On choisit d’abord la beauté et l’eau. On perd un peu en efficacité de hub pour se réveiller dans un endroit qui ressemble déjà à une excursion.'},
        menton:{name:'Menton',guide:'/riviera-guide/menton/',hotels:'/hotels/menton/',why:'La base plus lente à l’est. Couleur, jardins et respiration, sans renoncer complètement au train.'},
        monaco:{name:'Monaco',guide:'/riviera-guide/monaco/',hotels:'/hotels/monaco/',why:'La version intentionnelle : on dort ici parce que Monte-Carlo et l’hôtel font partie du voyage, pas parce que c’est la réponse la plus facile.'},
        sainttropez:{name:'Saint-Tropez',guide:'/riviera-guide/saint-tropez/',hotels:'/hotels/saint-tropez/',why:'C’est un engagement, pas une base centrale astucieuse. Vos réponses disent que la presqu’île est le voyage, donc Mametas la laisse gagner.'},
        saintpaul:{name:'Saint-Paul-de-Vence',guide:'/riviera-guide/saint-paul-de-vence/',hotels:'/hotels/saint-paul-de-vence/',why:'Un séjour volontairement intérieur pour l’art, la pierre et un rythme plus lent. Il ne gagne que lorsque la côte cesse d’être le personnage principal.'}
      },
      moodLine:{
        decide:'Vous nous avez demandé de décider. On choisit donc le séjour avec le moins de compromis inutiles.',
        sea:'On organise le voyage autour de la baignade et de la mer, pas autour d’une collection de codes postaux célèbres.',
        food:'Les restaurants et une vraie vie le soir comptent : la base doit continuer à fonctionner une fois les excursions rentrées.',
        culture:'L’art et les villages passent devant. L’accès aux bons arrêts culturels compte plus que la commodité balnéaire pure.',
        glamour:'Vous voulez le théâtre Riviera. Très bien. On refuse quand même de rendre la logistique absurde pour un lobby.',
        peace:'La beauté et le calme comptent plus que la connexion maximale. On accepte volontairement un peu moins d’efficacité.'
      },
      pace:{
        slow:'Slow signifie que la base doit faire davantage du travail. Moins de départs, et une demi-journée laissée complètement tranquille.',
        balanced:'Balanced signifie deux ou trois vraies sorties, avec assez de temps pour profiter de l’endroit où vous avez payé pour dormir.',
        ambitious:'Ambitious rend la qualité du hub plus importante. On vous donne des départs efficaces, pas l’autorisation de transformer la Riviera en tournée de livraison.'
      },
      priorities:{
        nice:{
          decide:['Nice correctement','Villefranche + Cap-Ferrat','Antibes ou Monaco/Menton'],
          sea:['Une vraie baignade à Nice','Villefranche + Cap-Ferrat','Antibes pour le sable'],
          food:['Marchés + dîner à Nice','Vieille ville d’Antibes','Une journée déjeuner vers l’est'],
          culture:['Matisse / Chagall à Nice','Saint-Paul + Fondation Maeght','Picasso à Antibes'],
          glamour:['Une belle soirée à Nice','Monaco pour le spectacle','Cannes pour le contraste ouest'],
          peace:['Villefranche + Cap-Ferrat','Menton','Une journée Nice volontairement lente']
        },
        cannes:{
          decide:['Cannes + Le Suquet','Antibes','Îles de Lérins'],
          sea:['Plage à Cannes','Îles de Lérins','Antibes / Juan-les-Pins'],
          food:['Forville + Le Suquet','Un dîner à Antibes','Une vraie table cannoise'],
          culture:['Antibes + Picasso','Îles de Lérins','Saint-Paul si vous avez une voiture'],
          glamour:['Croisette sans complexe','Une demi-journée où l’hôtel compte','Antibes pour le contraste'],
          peace:['Îles de Lérins','Théoule / Corniche d’Or si vous conduisez','Antibes au ralenti']
        },
        antibes:{
          decide:['Vieil Antibes','Cannes','Une journée Cap d’Antibes'],
          sea:['La Gravette ou Salis','Cap d’Antibes','Juan-les-Pins'],
          food:['Vieil Antibes','Marché + dîner à Cannes','Un long déjeuner plutôt qu’une ville de plus'],
          culture:['Musée Picasso','Saint-Paul si vous conduisez','Musées de Nice'],
          glamour:['Cap d’Antibes','Cannes','Juan-les-Pins le soir'],
          peace:['Cap d’Antibes','Vieil Antibes tôt','Une journée plage sans deuxième arrêt']
        },
        villefranche:{
          decide:['Villefranche correctement','Cap-Ferrat','Nice ou Monaco, pas les deux'],
          sea:['Baie de Villefranche','Criques du Cap-Ferrat','Beaulieu'],
          food:['Déjeuner à Villefranche','Dîner à Nice','Un repas à Monaco si vous voulez le théâtre'],
          culture:['Musées de Nice','Èze','Monaco pour une journée très différente'],
          glamour:['Cap-Ferrat','Monaco','Une belle soirée à Nice'],
          peace:['Baie de Villefranche','Cap-Ferrat à pied','Beaulieu sans programme']
        },
        menton:{
          decide:['Menton correctement','Monaco','Une journée à Nice'],
          sea:['Front de mer de Menton','Roquebrune-Cap-Martin','Monaco seulement pour le contraste'],
          food:['Menton','Monaco pour un grand repas','Une journée marché sans train'],
          culture:['Cocteau à Menton','Musées de Monaco','Nice pour les grandes collections'],
          glamour:['Monaco','Un meilleur hôtel à Menton','Cap-Martin pour la vue'],
          peace:['Jardins de Menton','Roquebrune-Cap-Martin','Une journée sans aucun train vers l’ouest']
        },
        monaco:{decide:['Monaco correctement','Menton','Cap-Ferrat'],glamour:['Monte-Carlo correctement','Une demi-journée palace / spa','Menton pour respirer'],food:['Restaurants de Monaco','Menton','Nice pour le contraste']},
        sainttropez:{decide:['Village de Saint-Tropez','Pampelonne','Ramatuelle / la presqu’île'],sea:['Pampelonne correctement','Une plage plus calme de la presqu’île','Saint-Tropez en fin de journée'],glamour:['Village de Saint-Tropez','Un après-midi où l’hôtel compte','Pampelonne quand vous voulez vraiment la scène']},
        saintpaul:{decide:['Saint-Paul après les visiteurs','Fondation Maeght','Vence'],culture:['Fondation Maeght','Village de Saint-Paul','Vence / chapelle Matisse'],peace:['Saint-Paul tôt et tard','Un long après-midi à l’hôtel','Vence ou une seule journée sur la côte']}
      },
      skips:{
        nice:'Laissez Saint-Tropez de côté sauf si c’est réellement une des raisons de votre voyage. Sur un séjour court, il mange trop de Riviera.',
        cannes:'Laissez tomber la journée Monaco/Menton automatique. Vous avez choisi l’ouest : utilisez-le correctement.',
        antibes:'Évitez de traverser toute la côte simplement parce que le train rend la chose techniquement possible.',
        villefranche:'Laissez la checklist de l’ouest tranquille. Cannes et Antibes survivront très bien à votre absence.',
        menton:'Pas de collection Cannes + Antibes par réflexe. L’est n’est pas un lot de consolation.',
        monaco:'N’utilisez pas Monaco comme piste de lancement pour traverser la côte tous les jours. Si vous dormez ici, laissez Monaco faire partie des vacances.',
        sainttropez:'Laissez l’est de la Riviera pour une autre fois. Vous avez choisi la presqu’île, Nice et Menton n’ont pas besoin de votre feuille de présence.',
        saintpaul:'Pas de navette quotidienne vers la côte. Dormir dans l’arrière-pays sert précisément à arrêter de se comporter comme si la mer faisait l’appel.'
      },
      hotels:{
        nice:[
          {tier:'Practical',price:'€€',name:'Hotel 66 Nice',note:'Près de la gare et pensé pour des départs faciles.'},
          {tier:'Comfort',price:'€€€',name:'Hôtel Apollinaire Nice',note:'Très bon équilibre quand centre et excursions comptent tous les deux.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel du Couvent',note:'À choisir quand l’hôtel a le droit de devenir une partie du voyage.'}
        ],
        cannes:[
          {tier:'Practical',price:'€€€',name:'Hôtel de Provence',note:'Une réponse plus petite et plus calme sans échelle palace.'},
          {tier:'Comfort',price:'€€€',name:'Le Cavendish',note:'Cannes en boutique, assez chic et moins cérémoniel.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel Martinez',note:'La Croisette en mode Riviera intégral.'}
        ],
        antibes:[
          {tier:'Practical',price:'€',name:'Hôtel de l’Étoile',note:'Central et rationnel quand la ville compte plus que le lobby.'},
          {tier:'Comfort',price:'€€€',name:'Royal Antibes',note:'Face à la mer sans renoncer à Antibes à pied.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel Belles Rives',note:'Juan-les-Pins quand l’histoire Riviera et l’eau font partie du sujet.'}
        ],
        villefranche:[
          {tier:'Practical',price:'€€',name:'Hôtel Le Provençal',note:'Village, gare et baie avant le théâtre hôtelier.'},
          {tier:'Comfort',price:'€€€',name:'Welcome Hotel',note:'Le fantasme du port, avec la géographie qui fait l’essentiel du travail.'},
          {tier:'Splurge',price:'€€€€',name:'Grand-Hôtel du Cap-Ferrat',note:'La version Cap-Ferrat volontaire, où l’hôtel devient une destination.'}
        ],
        menton:[
          {tier:'Practical',price:'€',name:'ibis Roquebrune Cap Martin Menton',note:'Une base rationnelle à l’est quand la chambre n’est pas l’événement principal.'},
          {tier:'Comfort',price:'€€€',name:'Hôtel Napoléon',note:'Mer + piscine pour ralentir sans entrer dans l’économie palace.'},
          {tier:'Splurge',price:'€€€€',name:'Villa Genesis',note:'Luxe boutique cohérent avec le rythme plus doux de Menton.'}
        ],
        monaco:[
          {tier:'Practical',price:'€€€',name:'Columbus Hotel Monte-Carlo',note:'La réponse Monaco la moins cérémonielle.'},
          {tier:'Comfort',price:'€€€€',name:'Fairmont Monte Carlo',note:'Grand hôtel monégasque, spectacle à portée de main.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel Hermitage Monte-Carlo',note:'Logique palace, choisie volontairement et non héritée par accident.'}
        ],
        sainttropez:[
          {tier:'Practical',price:'€€',name:'Hôtel Les Palmiers',note:'Une façon plus mesurée de dormir dans le Golfe.'},
          {tier:'Comfort',price:'€€€',name:'La Ferme d’Augustin',note:'Une version plus douce de la presqu’île quand la plage compte.'},
          {tier:'Splurge',price:'€€€€',name:'Hôtel La Ponche',note:'Saint-Tropez même, parce qu’ici le code postal fait partie du sujet.'}
        ],
        saintpaul:[
          {tier:'Practical',price:'€€',name:'Hôtel Les Messugues',note:'Une nuit plus calme près du village sans faire de l’hôtel tout le programme.'},
          {tier:'Comfort',price:'€€€',name:'Toile Blanche',note:'Adulte, arty et suffisamment loin de la machine côtière.'},
          {tier:'Splurge',price:'€€€€',name:'Le Domaine du Mas de Pierre',note:'La version retraite, où rester à l’hôtel est une partie légitime du plan.'}
        ]
      }
    }
  };

  function prioritiesFor(content, base, mood, pace) {
    var group = content.priorities[base] || {};
    var list = (group[mood] || group.decide || []).slice(0,3);
    if (pace === 'slow' && list.length >= 3) {
      list[2] = content === CONTENT.fr ? 'Gardez une demi-journée vide. Oui, vraiment.' : 'Keep one half-day empty. Yes, really.';
    }
    return list;
  }

  function escapeFor(profile, winner, lang) {
    var fr = lang === 'fr';
    if (profile.mood === 'glamour' && winner !== 'monaco') {
      return {base:'monaco', title:fr?'Vous êtes vraiment venu pour Monte-Carlo ?':'Really here for Monte-Carlo?',
        body:fr?'C’est une autre décision de base, pas un simple upgrade hôtelier.':'That changes the base itself; it is not a hotel upgrade.'};
    }
    if (profile.mood === 'sea' && profile.days !== '3' && profile.mobility !== 'nocar' && winner !== 'sainttropez') {
      return {base:'sainttropez', title:fr?'La presqu’île est en réalité le voyage ?':'Is the peninsula actually the trip?',
        body:fr?'Alors assumez Saint-Tropez comme base intentionnelle au lieu de l’ajouter à une checklist.':'Then commit to Saint-Tropez as an intentional base instead of adding it to a checklist.'};
    }
    if ((profile.mood === 'culture' || profile.mood === 'peace') && profile.days !== '3' && profile.mobility !== 'nocar' && winner !== 'saintpaul') {
      return {base:'saintpaul', title:fr?'Vous voulez vraiment quitter la côte ?':'Do you actually want to leave the coast?',
        body:fr?'Saint-Paul devient une vraie base seulement si l’arrière-pays fait partie du séjour.':'Saint-Paul becomes a real base only when the inland Riviera is part of the stay.'};
    }
    return null;
  }

  function resultModel(profile, overrideBase, lang) {
    var decision = chooseBase(profile);
    var baseId = overrideBase || decision.base;
    var content = CONTENT[lang];
    var base = content.bases[baseId];
    return {
      baseId:baseId,
      base:base,
      intentional:BASES[baseId].type === 'intentional',
      originalBase:decision.base,
      override:!!overrideBase,
      reason:content.moodLine[profile.mood],
      pace:content.pace[profile.pace],
      priorities:prioritiesFor(content, baseId, profile.mood, profile.pace),
      skip:content.skips[baseId],
      hotels:content.hotels[baseId] || [],
      escape:escapeFor(profile, baseId, lang)
    };
  }

  function esc(value) {
    return String(value || '').replace(/[&<>"']/g, function (ch) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch];
    });
  }

  function mount() {
    var root = document.querySelector('[data-riviera-chooser]');
    if (!root) return;
    var lang = (document.documentElement.lang || '').toLowerCase().indexOf('fr') === 0 ? 'fr' : 'en';
    var state = { days:'', mobility:'', mood:'', pace:'' };
    var params = new URLSearchParams(window.location.search);
    if (['3','5','7'].indexOf(params.get('days')) >= 0) state.days = params.get('days');

    var labels = lang === 'fr' ? {
      incomplete:'Répondez aux quatre questions. Ensuite, Mametas tranche.',
      verdict:'LE VERDICT MAMETAS',
      stay:'Dormez à ',
      do:'Ce qu’on ferait',
      skip:'Ce qu’on laisserait tomber',
      hotel:'Trois niveaux. Même base.',
      hotelNote:'Le tier est éditorial ; les € sont des repères relatifs Mametas, jamais un tarif en temps réel.',
      allHotels:'Voir toute la sélection hôtels',
      guide:'Voir le guide de la base',
      escape:'Voir cette version',
      back:'Revenir au choix Mametas',
      intentional:'BASE INTENTIONNELLE',
      reset:'Recommencer'
    } : {
      incomplete:'Answer all four questions. Then Mametas makes the call.',
      verdict:'THE MAMETAS VERDICT',
      stay:'Stay in ',
      do:'What we would do',
      skip:'What we would skip',
      hotel:'Three levels. Same base.',
      hotelNote:'The tier is editorial; € symbols are Mametas relative guides, never a live rate.',
      allHotels:'See the full hotel selection',
      guide:'See the base guide',
      escape:'Show me this version',
      back:'Back to the Mametas pick',
      intentional:'INTENTIONAL BASE',
      reset:'Start again'
    };

    function syncButtons() {
      root.querySelectorAll('[data-choice]').forEach(function (button) {
        var group = button.getAttribute('data-group');
        var value = button.getAttribute('data-choice');
        var active = state[group] === value;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      var ready = state.days && state.mobility && state.mood && state.pace;
      var submit = root.querySelector('[data-chooser-submit]');
      if (submit) submit.disabled = !ready;
      root.querySelectorAll('[data-step]').forEach(function (step) {
        var n = Number(step.getAttribute('data-step'));
        var visible = n === 1 || (n === 2 && state.days) || (n === 3 && state.days && state.mobility) ||
          (n === 4 && state.days && state.mobility && state.mood);
        step.hidden = !visible;
      });
    }

    function render(overrideBase) {
      if (!(state.days && state.mobility && state.mood && state.pace)) return;
      var model = resultModel(state, overrideBase, lang);
      var out = root.querySelector('[data-chooser-result]');
      var profileText = [
        state.days === '7' ? '7+' : state.days,
        state.mobility === 'nocar' ? (lang==='fr'?'sans voiture':'no car') : (state.mobility === 'car' ? (lang==='fr'?'voiture':'car') : (lang==='fr'?'mobilité flexible':'flexible mobility')),
        state.mood,
        state.pace
      ].join(' · ');
      var priorities = model.priorities.map(function (p, i) {
        return '<li><span>0' + (i+1) + '</span><strong>' + esc(p) + '</strong></li>';
      }).join('');
      var hotelCards = model.hotels.map(function (h) {
        return '<article class="chooser-hotel-card"><div class="chooser-hotel-meta"><span>' + esc(h.tier) + '</span><b>' + esc(h.price) + '</b></div><h4>' + esc(h.name) + '</h4><p>' + esc(h.note) + '</p></article>';
      }).join('');
      var escape = '';
      if (!model.override && model.escape) {
        escape = '<aside class="chooser-escape"><span class="eyebrow">' + (lang==='fr'?'OPTION INTENTIONNELLE':'INTENTIONAL ALTERNATIVE') + '</span><h3>' + esc(model.escape.title) + '</h3><p>' + esc(model.escape.body) + '</p><button type="button" class="button secondary" data-chooser-escape="' + esc(model.escape.base) + '">' + labels.escape + '</button></aside>';
      } else if (model.override) {
        escape = '<aside class="chooser-escape chooser-escape--active"><span class="eyebrow">' + labels.intentional + '</span><p>' + (lang==='fr'?'Vous avez choisi la version plus engagée du même profil. La base change ; le tier hôtelier, lui, restera une décision séparée.':'You chose the more committed version of the same profile. The base changes; hotel tier remains a separate decision.') + '</p><button type="button" class="button secondary" data-chooser-back>' + labels.back + '</button></aside>';
      }
      out.innerHTML =
        '<div class="chooser-result-head"><p class="eyebrow">' + labels.verdict + '</p><p class="chooser-profile">' + esc(profileText) + '</p><h2>' + labels.stay + esc(model.base.name) + '.</h2><p class="chooser-lead">' + esc(model.base.why) + '</p><p>' + esc(model.reason) + '</p><p class="chooser-pace"><strong>' + (lang==='fr'?'Rythme.':'Pace.') + '</strong> ' + esc(model.pace) + '</p></div>' +
        '<div class="chooser-result-grid"><section class="chooser-do"><h3>' + labels.do + '</h3><ol>' + priorities + '</ol></section><section class="chooser-skip"><h3>' + labels.skip + '</h3><p>' + esc(model.skip) + '</p></section></div>' +
        escape +
        '<section class="chooser-hotels"><div class="chooser-hotels-head"><div><p class="eyebrow">' + (lang==='fr'?'VOTRE HÔTEL':'YOUR HOTEL') + '</p><h3>' + labels.hotel + '</h3></div><p>' + labels.hotelNote + '</p></div><div class="chooser-hotel-grid">' + hotelCards + '</div><div class="chooser-actions"><a class="button" href="' + esc(model.base.hotels) + '">' + labels.allHotels + '</a><a class="button secondary" href="' + esc(model.base.guide) + '">' + labels.guide + '</a></div></section>' +
        '<button type="button" class="chooser-reset" data-chooser-reset>' + labels.reset + '</button>';
      out.hidden = false;
      out.scrollIntoView({behavior:'smooth',block:'start'});
    }

    root.addEventListener('click', function (event) {
      var button = event.target.closest('[data-choice]');
      if (button) {
        state[button.getAttribute('data-group')] = button.getAttribute('data-choice');
        syncButtons();
        var next = root.querySelector('[data-step]:not([hidden]) [data-choice].is-active');
        return;
      }
      var escapeButton = event.target.closest('[data-chooser-escape]');
      if (escapeButton) { render(escapeButton.getAttribute('data-chooser-escape')); return; }
      if (event.target.closest('[data-chooser-back]')) { render(null); return; }
      if (event.target.closest('[data-chooser-reset]')) {
        state = {days:'',mobility:'',mood:'',pace:''};
        history.replaceState(null,'',window.location.pathname);
        root.querySelector('[data-chooser-result]').hidden = true;
        syncButtons();
        root.scrollIntoView({behavior:'smooth',block:'start'});
      }
    });

    var submit = root.querySelector('[data-chooser-submit]');
    if (submit) submit.addEventListener('click', function () { render(null); });
    syncButtons();
  }

  function selfTest() {
    var days=['3','5','7'], mobility=['nocar','car','either'], moods=['decide','sea','food','culture','glamour','peace'], pace=['slow','balanced','ambitious'];
    var count=0, errors=[];
    days.forEach(function(d){ mobility.forEach(function(m){ moods.forEach(function(md){ pace.forEach(function(p){
      var profile={days:d,mobility:m,mood:md,pace:p};
      var result=chooseBase(profile); count++;
      if (!BASES[result.base]) errors.push('unknown base '+JSON.stringify(profile));
      if (d==='3' && BASES[result.base].type==='intentional') errors.push('3-day intentional '+JSON.stringify(profile));
      if (m==='nocar' && (result.base==='sainttropez' || result.base==='saintpaul')) errors.push('no-car friction '+JSON.stringify(profile));
    }); }); }); });
    var fixtures=[
      [{days:'5',mobility:'nocar',mood:'glamour',pace:'balanced'},'cannes'],
      [{days:'7',mobility:'nocar',mood:'glamour',pace:'slow'},'monaco'],
      [{days:'7',mobility:'car',mood:'sea',pace:'slow'},'sainttropez'],
      [{days:'7',mobility:'car',mood:'culture',pace:'slow'},'saintpaul'],
      [{days:'3',mobility:'nocar',mood:'decide',pace:'balanced'},'nice']
    ];
    fixtures.forEach(function(f){ var got=chooseBase(f[0]).base; if (got!==f[1]) errors.push('fixture '+JSON.stringify(f[0])+' expected '+f[1]+' got '+got); });
    if (errors.length) { throw new Error('Riviera Chooser self-test failed:\n'+errors.join('\n')); }
    if (typeof console !== 'undefined') console.log('Riviera Chooser self-test passed: '+count+' profiles + '+fixtures.length+' doctrine fixtures.');
    return true;
  }

  return { chooseBase:chooseBase, resultModel:resultModel, mount:mount, selfTest:selfTest };
});