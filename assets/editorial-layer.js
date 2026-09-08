(function () {
  "use strict";
  var path = window.location.pathname;
  var fr = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;

  var destinationData = {
    nice: {
      en: {
        title: "What not to miss in Nice",
        intro: "Five things earn their place on a first visit. The rest can negotiate for your second trip.",
        items: [
          ["Old Nice + Cours Saleya", "Go in the morning, then lose the map for a while. The market and the old town belong together; treating them as two attractions is how checklists reproduce.", "/en/restaurants/nice/", "Worth it: early. Skip if: you only have time for a noon crowd."],
          ["Castle Hill", "The fastest way to understand Nice geographically: Baie des Anges on one side, port on the other. There is no castle. The view has coped.", "#", "Worth it: for a first visit, yes."],
          ["The Port + Cap de Nice", "Walk east from Port Lympia towards Franck Pilatte for a less ceremonial coastline and a city that suddenly lowers its voice.", "/en/beaches/nice/", "The catch: save proper shoes for the coastal path."],
          ["One proper swim", "Nice is not a seaside backdrop. Get in. Ponchettes is easy; La Réserve and Coco Beach change the mood.", "/en/beaches/nice/", "Skip if: rough sea or conditions say no. The Mediterranean wins arguments."],
          ["Cimiez — if you have a second day", "Matisse, Roman remains, olive gardens and the monastery gardens make this the useful counterpoint to seafront Nice.", "/en/culture/", "Worth it: with two days. Skip if: you are compressing Nice into one."],
          ["The Promenade — but not all of it", "Walk enough of the Promenade des Anglais to understand the scale of the bay. Seven kilometres is a fact, not an assignment.", "/en/riviera-guide/nice/", "Mametas edit: see it; do not spend the entire day proving you did."]
        ]
      },
      fr: {
        title: "Les choses à voir absolument à Nice",
        intro: "Six choses méritent vraiment leur place lors d’une première visite. Le reste peut attendre le deuxième séjour.",
        items: [
          ["Vieux-Nice + Cours Saleya", "Venez le matin, puis rangez la carte un moment. Le marché et la vieille ville forment un même mouvement ; les traiter comme deux attractions, c’est déjà commencer la checklist.", "/restaurants/nice/", "À faire : tôt. À éviter : découvrir Saleya uniquement dans la foule de midi."],
          ["La Colline du Château", "Le moyen le plus rapide de comprendre Nice : baie des Anges d’un côté, port de l’autre. Le château n’existe plus. La vue s’en remet très bien.", "#", "À faire : oui, pour une première visite."],
          ["Le Port + le Cap de Nice", "Marchez vers l’est depuis Port Lympia jusqu’à Franck Pilatte : la côte devient moins cérémonieuse et la ville baisse soudain d’un ton.", "/plages/nice/", "Le piège : prévoyez de vraies chaussures pour le sentier littoral."],
          ["Une vraie baignade", "Nice n’est pas un décor maritime. Entrez dans l’eau. Ponchettes est simple ; La Réserve et Coco Beach changent l’ambiance.", "/plages/nice/", "À ignorer si la mer est mauvaise. Sur ce point, elle décide."],
          ["Cimiez — si vous avez un deuxième jour", "Matisse, vestiges romains, oliveraie et jardins du monastère offrent le bon contrepoint au Nice du bord de mer.", "/culture/", "À faire : avec deux jours. À laisser : si vous compressez Nice en une journée."],
          ["La Promenade — mais pas ses 7 km", "Marchez assez sur la Promenade des Anglais pour comprendre l’échelle de la baie. Sept kilomètres est une mesure, pas une consigne.", "/riviera-guide/nice/", "Le tri Mametas : la voir, oui ; y consacrer toute la journée, non."]
        ]
      }
    },
    villefranche: {
      en: {title:"What not to miss: Villefranche & Cap-Ferrat",intro:"The bay is the headline. Do not bury it under twelve stops.",items:[
        ["Villefranche old town + harbour","Walk down through the old town to the waterfront before doing anything ambitious. The bay is not the transfer point; it is the reason you came.","/en/restaurants/villefranche-sur-mer/","Worth it: first, before the peninsula."],
        ["A swim in Villefranche","This is one of the places where building the day around a swim makes sense rather than feeling like lost sightseeing time.","/en/beaches/","The catch: summer rewards an early start."],
        ["One Cap-Ferrat coastal walk","Choose a section of coast and actually walk it. The peninsula makes more sense at foot speed than through a taxi window.","/en/day-trips/cap-ferrat-a-pied/","Worth it: if shoes and heat agree."],
        ["Villa Ephrussi — if gardens are your thing","A strong single cultural stop on the peninsula. Pair it with a walk or swim, not an inventory of every villa nearby.","/en/culture/","Skip if: gardens leave you cold. Beauty is not compulsory homework."],
        ["One long lunch, not three rushed sights","Villefranche and Cap-Ferrat reward slack in the schedule. Protect some.","/en/restaurants/villefranche-sur-mer/","Mametas rule: one peninsula, one main objective."]]},
      fr: {title:"Les indispensables : Villefranche & Cap-Ferrat",intro:"La rade est le sujet. Inutile de l’enterrer sous douze étapes.",items:[
        ["Vieille ville + port de Villefranche","Descendez par la vieille ville jusqu’au front de mer avant toute ambition supplémentaire. La rade n’est pas un point de correspondance : c’est la raison de venir.","/restaurants/villefranche-sur-mer/","À faire : en premier, avant la presqu’île."],
        ["Une baignade à Villefranche","Ici, construire la journée autour d’une baignade a du sens ; ce n’est pas du temps volé aux visites.","/plages/","Le piège : en été, commencez tôt."],
        ["Un morceau du sentier du Cap-Ferrat","Choisissez une portion de côte et marchez-la vraiment. La presqu’île se comprend mieux à vitesse humaine que depuis un taxi.","/escapades/cap-ferrat-a-pied/","À faire : si chaussures et chaleur sont d’accord."],
        ["Villa Ephrussi — si les jardins vous parlent","Un excellent grand arrêt culturel sur la presqu’île. Associez-le à une marche ou une baignade, pas à l’inventaire des villas voisines.","/culture/","À laisser si les jardins vous indiffèrent. La beauté n’est pas un devoir scolaire."],
        ["Un long déjeuner plutôt que trois visites pressées","Villefranche et Cap-Ferrat récompensent le vide dans l’agenda. Protégez-en un peu.","/restaurants/villefranche-sur-mer/","Règle Mametas : une presqu’île, un objectif principal."]]}
    },
    antibes: {
      en:{title:"What not to miss in Antibes",intro:"Antibes works because the essentials fit together. Resist the urge to add an entire cape before lunch.",items:[
        ["Old Antibes + the ramparts","Walk the old town, market area and ramparts as one sequence. This is the core of Antibes, not the warm-up.","/en/restaurants/antibes/","Worth it: absolutely."],
        ["Picasso Museum","The museum occupies the Château Grimaldi and is the cultural stop that most naturally belongs in a first Antibes day.","/en/culture/picasso-museum-antibes/","The catch: closed Mondays; check current hours."],
        ["La Gravette","A sandy beach beside the old town is an unusually convenient Riviera proposition. Use it.","/en/beaches/antibes/","Worth it: for an easy swim without reorganising the day."],
        ["Cap d’Antibes — only with time","The Cap deserves a separate rhythm: coves, walks and hotels rather than a quick extension of the centre.","/en/beaches/antibes/","Skip if: you only have one day and are already enjoying town."],
        ["Cannes — only if you want Cannes","The train makes it easy. That does not make it mandatory.","/en/riviera-guide/nice-or-cannes/","Mametas edit: add the Croisette for glamour, not for completionism."]]},
      fr:{title:"Les choses à voir absolument à Antibes",intro:"Antibes fonctionne parce que l’essentiel tient bien ensemble. Résistez à l’envie d’ajouter tout le Cap avant le déjeuner.",items:[
        ["Vieil Antibes + remparts","Faites vieille ville, marché et remparts dans un même mouvement. C’est le cœur d’Antibes, pas l’échauffement.","/restaurants/antibes/","À faire : sans hésiter."],
        ["Musée Picasso","Installé dans le château Grimaldi, c’est l’arrêt culturel qui s’intègre le plus naturellement à une première journée à Antibes.","/culture/musee-picasso-antibes/","Le piège : fermé le lundi ; vérifiez les horaires."],
        ["La Gravette","Une plage de sable collée à la vieille ville est une proposition assez rare sur la Riviera. Profitez-en.","/plages/antibes/","À faire : pour se baigner sans réorganiser toute la journée."],
        ["Cap d’Antibes — seulement si vous avez le temps","Le Cap mérite un autre rythme : criques, promenades et hôtels plutôt qu’une extension rapide du centre.","/plages/antibes/","À laisser : si vous n’avez qu’une journée et que la ville vous retient déjà."],
        ["Cannes — seulement si vous voulez vraiment Cannes","Le train rend l’ajout facile. Il ne le rend pas obligatoire.","/riviera-guide/nice-ou-cannes/","Le tri Mametas : ajoutez la Croisette pour le glamour, pas pour compléter une collection."]]}
    },
    monaco: {
      en:{title:"What not to miss in Monaco",intro:"Monaco is small enough to edit hard. Four priorities are plenty for a first day.",items:[
        ["The Rock + old town","Start with Monaco-Ville and the Palace area. It gives the Principality history and altitude before the polished theatre below.","/en/riviera-guide/monaco/","Worth it: yes. The vertical geography is part of the visit."],
        ["Oceanographic Museum","If you choose one major attraction, this is the most distinctive first-trip candidate and sits naturally on the Rock.","/en/culture/","The catch: allow real time; it is not a twenty-minute photo stop."],
        ["Port Hercule on foot","Walk between the Rock and Monte-Carlo rather than teleporting between icons. The harbour explains a lot about the place.","/en/restaurants/monaco/","Worth it: as the connective tissue, not another box."],
        ["Monte-Carlo + Casino square","See the architecture and spectacle even if gambling and luxury shopping are not your hobbies.","/en/riviera-guide/monaco/","Skip if: you planned an afternoon of shop-window anthropology."],
        ["Menton afterwards — only if Monaco stays edited","The pair works by contrast: Monaco performs, Menton exhales.","/en/riviera-guide/menton/","The catch: two full museum programmes do not fit into one civilised day."]]},
      fr:{title:"Les choses à voir absolument à Monaco",intro:"Monaco est assez petit pour trier sévèrement. Quatre priorités suffisent largement à une première journée.",items:[
        ["Le Rocher + Monaco-Ville","Commencez par la vieille ville et le secteur du Palais. Vous aurez l’histoire et la hauteur avant le théâtre plus poli d’en bas.","/riviera-guide/monaco/","À faire : oui. La verticalité fait partie de la visite."],
        ["Musée océanographique","S’il faut choisir une grande visite, c’est la candidate la plus singulière pour une première fois et elle s’insère naturellement sur le Rocher.","/culture/","Le piège : prévoyez du temps ; ce n’est pas un arrêt photo de vingt minutes."],
        ["Port Hercule à pied","Marchez entre le Rocher et Monte-Carlo plutôt que de téléporter votre visite d’icône en icône. Le port explique beaucoup de Monaco.","/restaurants/monaco/","À faire : comme lien entre les lieux, pas comme case supplémentaire."],
        ["Monte-Carlo + place du Casino","Regardez l’architecture et le spectacle même si le jeu et le shopping de luxe ne sont pas vos hobbies.","/riviera-guide/monaco/","À laisser : l’après-midi entier à observer les vitrines et leurs propriétaires."],
        ["Menton ensuite — seulement si Monaco reste édité","Le duo fonctionne par contraste : Monaco montre, Menton respire.","/riviera-guide/menton/","Le piège : deux programmes complets de musées ne tiennent pas dans une journée civilisée."]]}
    },
    menton: {
      en:{title:"What not to miss in Menton",intro:"Menton is best when you stop trying to justify the train ride with quantity.",items:[
        ["Old town + Saint-Michel","Climb through the old town to the basilica and the viewpoints above it. This is the image of Menton that actually deserves the stairs.","/en/riviera-guide/menton/","Worth it: first thing or late afternoon."],
        ["One garden","Menton's gardens are part of its identity. Pick one rather than turning horticulture into endurance sport.","/en/culture/","Worth it: if gardens matter to you. Otherwise keep the sea."],
        ["One Cocteau stop","The Bastion or the wedding room gives Menton a cultural thread beyond lemons and pastel façades.","/en/culture/cocteau-bastion/","The catch: choose one if the day is short."],
        ["Sablettes + a swim","The seafront below the old town is the obvious place to let the itinerary loosen.","/en/beaches/","Worth it: especially after the climb."],
        ["Do less","A long lunch, old town and one afternoon choice is a successful Menton day, not an underachieving one.","/en/restaurants/menton/","Mametas rule: leave with something unseen."]]},
      fr:{title:"Les choses à voir absolument à Menton",intro:"Menton devient meilleure dès qu’on arrête de vouloir rentabiliser le billet de train par la quantité.",items:[
        ["Vieille ville + Saint-Michel","Montez par la vieille ville jusqu’à la basilique et aux points de vue au-dessus. Voilà une image de Menton qui mérite réellement les escaliers.","/riviera-guide/menton/","À faire : tôt ou en fin d’après-midi."],
        ["Un jardin","Les jardins font partie de l’identité de Menton. Choisissez-en un au lieu de transformer la botanique en sport d’endurance.","/culture/","À faire si les jardins vous intéressent. Sinon, gardez la mer."],
        ["Un arrêt Cocteau","Le Bastion ou la salle des mariages donnent à Menton un fil culturel au-delà des citrons et des façades pastel.","/culture/musee-cocteau-bastion/","Le piège : si la journée est courte, choisissez-en un."],
        ["Les Sablettes + une baignade","Le front de mer sous la vieille ville est l’endroit évident pour laisser le programme se détendre.","/plages/","À faire : particulièrement après la montée."],
        ["En faire moins","Un long déjeuner, la vieille ville et un vrai choix l’après-midi constituent une journée réussie, pas une journée incomplète.","/restaurants/menton/","Règle Mametas : repartez avec quelque chose que vous n’avez pas vu."]]}
    }
  };

  function destinationKey() {
    if (/\/riviera-guide\/nice\/$/.test(path)) return "nice";
    if (/\/riviera-guide\/villefranche-cap-ferrat\/$/.test(path)) return "villefranche";
    if (/\/riviera-guide\/antibes\/$/.test(path)) return "antibes";
    if (/\/riviera-guide\/monaco\/$/.test(path)) return "monaco";
    if (/\/riviera-guide\/menton\/$/.test(path)) return "menton";
    return null;
  }

  function renderMustSee(data) {
    var body = document.querySelector(".article-body") || document.querySelector("article.article");
    if (!body || body.querySelector("[data-mametas-must-see]")) return;
    var section = document.createElement("section");
    section.setAttribute("data-mametas-must-see", "true");
    section.id = fr ? "indispensables" : "what-not-to-miss";
    var html = '<h2>' + data.title + '</h2><p>' + data.intro + '</p>';
    data.items.forEach(function (item, i) {
      var title = item[2] && item[2] !== "#" ? '<a href="' + item[2] + '">' + item[0] + '</a>' : item[0];
      html += '<div class="day-card"><span class="day">' + String(i + 1).padStart(2, "0") + '</span><h3>' + title + '</h3><p>' + item[1] + '</p><p><strong>' + (fr ? "Le tri :" : "The edit:") + '</strong> ' + item[3] + '</p></div>';
    });
    section.innerHTML = html;
    var verdict = body.querySelector(".verdict-box, .verdict");
    if (verdict && verdict.nextSibling) body.insertBefore(section, verdict.nextSibling);
    else body.insertBefore(section, body.firstChild);
  }

  function enrichItinerary() {
    var isEn = path === "/plan/five-days-nice-no-car/";
    var isFr = path === "/fr/planifier/cinq-jours-nice-sans-voiture/";
    if (!isEn && !isFr) return;
    var body = document.querySelector(".article-body");
    if (!body) return;
    var days = isFr ? [
      ["jour-un","Absolument : Vieux-Nice + Colline du Château","En plus : baignade ou Port si le rythme le permet.","À ignorer : vouloir « finir Nice » le premier jour."],
      ["jour-deux","Absolument : Villefranche + un seul objectif au Cap-Ferrat","En plus : baignade ou long déjeuner.","À ignorer : collectionner toutes les criques et villas."],
      ["jour-trois","Absolument : le Rocher à Monaco + vieille ville de Menton","En plus : Musée océanographique ou un arrêt Cocteau, pas les deux par principe.","À ignorer : transformer Monaco en après-midi shopping obligatoire."],
      ["jour-quatre","Absolument : Vieil Antibes + remparts","En plus : Musée Picasso ou Gravette selon l’envie.","À ignorer : ajouter Cannes simplement parce que le train continue."],
      ["jour-cinq","Absolument : Èze village si vous y allez ; sinon une vraie journée lente à Nice","En plus : un musée ou une baignade.","À ignorer : culpabiliser parce qu’une demi-journée reste vide."]
    ] : [
      ["day-one","Must: Old Nice + Castle Hill","If there is room: a swim or the Port.","Skip: trying to ‘finish Nice’ on day one."],
      ["day-two","Must: Villefranche + one Cap-Ferrat objective","If there is room: a swim or a long lunch.","Skip: collecting every cove and villa."],
      ["day-three","Must: the Rock in Monaco + Menton old town","If there is room: Oceanographic Museum or one Cocteau stop, not both by reflex.","Skip: treating luxury shopping as compulsory sightseeing."],
      ["day-four","Must: Old Antibes + the ramparts","If there is room: Picasso Museum or La Gravette, according to mood.","Skip: adding Cannes merely because the train continues."],
      ["day-five","Must: Èze village if you go; otherwise a genuinely slow Nice day","If there is room: one museum or a swim.","Skip: feeling guilty because half a day remains empty."]
    ];
    days.forEach(function (d) {
      var card = document.getElementById(d[0]);
      if (!card || card.querySelector(".must-see-day")) return;
      var p = document.createElement("p");
      p.className = "must-see-day";
      p.innerHTML = '<strong>' + d[1] + '</strong><br>' + d[2] + '<br><em>' + d[3] + '</em>';
      var link = card.querySelector(".inline-decision-link");
      if (link && link.parentNode) card.insertBefore(p, link.parentNode);
      else card.appendChild(p);
    });

    if (!body.querySelector("[data-itinerary-must-see]")) {
      var recap = document.createElement("section");
      recap.setAttribute("data-itinerary-must-see", "true");
      recap.id = isFr ? "indispensables-parcours" : "itinerary-must-sees";
      recap.innerHTML = isFr
        ? '<h2>Les choses à voir absolument sur ce parcours</h2><p>Le noyau dur tient en cinq décisions : <a href="/riviera-guide/nice/#indispensables">Nice</a> pour comprendre la base ; <a href="/riviera-guide/villefranche-cap-ferrat/#indispensables">Villefranche et un choix au Cap-Ferrat</a> ; <a href="/riviera-guide/monaco/#indispensables">le Rocher à Monaco</a> puis <a href="/riviera-guide/menton/#indispensables">la vieille ville de Menton</a> ; <a href="/riviera-guide/antibes/#indispensables">le Vieil Antibes et ses remparts</a> ; enfin Èze ou une vraie respiration niçoise. Tout le reste est complément. Oui, même si Instagram insiste.</p>'
        : '<h2>What not to miss on this itinerary</h2><p>The hard core is five decisions: <a href="/en/riviera-guide/nice/#what-not-to-miss">Nice</a> to understand your base; <a href="/en/riviera-guide/villefranche-cap-ferrat/#what-not-to-miss">Villefranche plus one Cap-Ferrat choice</a>; <a href="/en/riviera-guide/monaco/#what-not-to-miss">the Rock in Monaco</a> then <a href="/en/riviera-guide/menton/#what-not-to-miss">Menton old town</a>; <a href="/en/riviera-guide/antibes/#what-not-to-miss">Old Antibes and the ramparts</a>; finally Èze or a genuinely slow Nice day. Everything else is optional. Yes, even if Instagram objects.</p>';
      var transport = document.getElementById(isFr ? "transports" : "transport");
      if (transport) body.insertBefore(recap, transport);
      else body.appendChild(recap);
    }
  }

  function init() {
    var key = destinationKey();
    if (key) renderMustSee(destinationData[key][fr ? "fr" : "en"]);
    enrichItinerary();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
