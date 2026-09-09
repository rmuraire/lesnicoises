(function () {
  "use strict";

  var path = window.location.pathname;
  var fr = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;

  function link(href, label) {
    return '<a class="inline-decision-link" href="' + href + '">' + label + '</a>';
  }

  function regionalItems() {
    return fr ? [
      ["Nice d’abord, pas Nice en transit", "Vieux-Nice, Colline du Château et une vraie baignade suffisent déjà à donner le ton. La ville mérite une journée avant de devenir votre quai de départ.", "/riviera-guide/nice/", "À ignorer : vouloir tout voir dès l’arrivée."],
      ["Villefranche + une seule idée au Cap-Ferrat", "La rade, une baignade, puis un choix : sentier, jardin ou long déjeuner. Les trois si vous avez le temps ; pas parce qu’une carte vous culpabilise.", "/riviera-guide/villefranche-cap-ferrat/", "Le piège : transformer la presqu’île en collection de points Google Maps."],
      ["Une journée Monaco vraiment éditée", "Rocher, Musée océanographique ou Monte-Carlo : choisissez les priorités. Monaco est petit sur la carte, pas dans les dénivelés.", "/riviera-guide/monaco/", "À laisser : l’inventaire complet des vitrines."],
      ["Menton pour ralentir", "Vieille ville, Saint-Michel, un jardin ou Cocteau, puis la mer. Le charme fonctionne mieux sans objectif de rendement.", "/riviera-guide/menton/", "Worth it : surtout si Monaco vous a légèrement épuisé."],
      ["Antibes pour l’équilibre", "Vieille ville, remparts, Picasso et baignade : peu de logistique, beaucoup de Riviera dans une seule journée.", "/riviera-guide/antibes/", "À ne pas ajouter automatiquement : Cannes le même jour."],
      ["Cannes seulement si vous voulez Cannes", "Croisette, grands hôtels, Suquet : le théâtre est assumé. La proximité ferroviaire n’en fait pas une obligation morale.", "/riviera-guide/nice-ou-cannes/", "À faire : pour le vernis. À laisser : pour cocher une ville de plus."],
      ["Èze avec la logistique en tête", "Le village perché mérite le détour si vous acceptez bus, pente et affluence. Une vue célèbre reste une vraie vue ; elle n’abolit pas les jambes.", "/escapades/", "Le piège : confondre Èze-sur-Mer et Èze village."],
      ["Saint-Paul-de-Vence si l’art et la pierre comptent", "Une excursion intérieure forte, à choisir pour son atmosphère et son histoire artistique plutôt que pour remplir une journée déjà chargée.", "/escapades/", "À laisser : si vous n’avez que trois jours sur la côte."],
      ["Une vraie baignade, pas seulement des photos de plage", "Nice, Villefranche ou Antibes : gardez du temps pour entrer dans l’eau. Sur la Riviera, la mer n’est pas un fond d’écran.", "/plages/", "Règle Mametas : une bonne baignade vaut parfois mieux qu’une troisième commune."],
      ["Un demi-jour sans ambition", "Marché, café, déjeuner long, plage ou musée selon l’humeur. Le luxe local le plus sous-estimé reste une marge dans l’agenda.", "/fr/planifier/cinq-jours-nice-sans-voiture/#version-sept", "À éviter : transformer sept jours en dix-sept objectifs."]
    ] : [
      ["Give Nice a day before using it as a station", "Old Nice, Castle Hill and one real swim already give you the measure of the place. Your base deserves a day before becoming your departure platform.", "/en/riviera-guide/nice/", "Skip: trying to finish Nice on arrival day."],
      ["Villefranche + one Cap-Ferrat idea", "The bay, a swim, then choose: coastal walk, garden or long lunch. All three only if time agrees, not because a map is making demands.", "/en/riviera-guide/villefranche-cap-ferrat/", "The catch: turning the peninsula into a Google Maps collection."],
      ["Edit Monaco hard", "The Rock, the Oceanographic Museum or Monte-Carlo: choose priorities. Monaco is small on a map, not in gradients.", "/en/riviera-guide/monaco/", "Skip: the complete inventory of luxury shop windows."],
      ["Use Menton to slow down", "Old town, Saint-Michel, one garden or Cocteau, then the sea. Menton improves when you stop measuring output.", "/en/riviera-guide/menton/", "Worth it: especially after Monaco has slightly exhausted you."],
      ["Choose Antibes for balance", "Old town, ramparts, Picasso and a swim: little logistics, a great deal of Riviera in one day.", "/en/riviera-guide/antibes/", "Do not add automatically: Cannes on the same day."],
      ["Do Cannes only if you want Cannes", "Croisette, grand hotels, Le Suquet: the theatre is deliberate. A convenient train does not make the city compulsory.", "/en/riviera-guide/nice-or-cannes/", "Worth it: for polish. Skip: for completionism."],
      ["Treat Èze as a logistics choice", "The hilltop village earns the detour if you accept bus, gradient and crowds. A famous view remains a real view; it does not abolish legs.", "/en/day-trips/", "The catch: Èze-sur-Mer is not Èze village."],
      ["Use Saint-Paul-de-Vence when art and stone matter", "A strong inland excursion for atmosphere and artistic history, not a decorative add-on to an already crowded day.", "/en/day-trips/", "Skip: if you only have three days on the coast."],
      ["Take one proper swim", "Nice, Villefranche or Antibes: leave enough time to get in the water. On the Riviera, the sea is not wallpaper.", "/en/beaches/", "Mametas rule: one good swim can beat a third municipality."],
      ["Protect one half-day with no ambition", "Market, coffee, long lunch, beach or museum according to mood. The most underrated local luxury is space in the schedule.", "/plan/five-days-nice-no-car/#make-it-seven", "Skip: turning seven days into seventeen objectives."]
    ];
  }

  function renderRegional() {
    var home = path === "/" || path === "/fr/" || path === "/fr";
    if (!home || document.getElementById("riviera-first-trip-edit")) return;
    var anchor = document.getElementById(fr ? "bases" : "bases") || document.getElementById(fr ? "lieux" : "places");
    if (!anchor) return;

    var section = document.createElement("section");
    section.className = "v3-section";
    section.id = "riviera-first-trip-edit";
    var items = regionalItems();
    var cards = items.map(function (item, index) {
      return '<div class="day-card"><span class="day">' + String(index + 1).padStart(2, "0") + '</span><h3>' + item[0] + '</h3><p>' + item[1] + '</p><p><strong>' + (fr ? "Le tri : " : "The edit: ") + '</strong>' + item[3] + '</p><p>' + link(item[2], fr ? "Décider en détail →" : "Make the detailed decision →") + '</p></div>';
    }).join("");
    section.innerHTML = '<div class="wrap"><div class="section-heading"><div><p class="eyebrow">' + (fr ? "Le premier séjour, vraiment édité" : "The first trip, properly edited") + '</p><h2>' + (fr ? "10 expériences qui structurent vraiment la Côte d’Azur" : "10 experiences that actually shape a first Riviera trip") + '</h2></div><p>' + (fr ? "Pas un Top 50. Dix choix qui donnent une colonne vertébrale à trois, cinq ou sept jours — et quelques permissions très utiles de ne pas tout faire." : "Not a Top 50. Ten choices that give three, five or seven days a spine — plus a few useful permissions not to do everything.") + '</p></div><div class="article-body">' + cards + '</div></div>';
    anchor.parentNode.insertBefore(section, anchor.nextSibling);
  }

  function renderThreeSeven() {
    var isPlan = path === "/plan/five-days-nice-no-car/" || path === "/fr/planifier/cinq-jours-nice-sans-voiture/";
    if (!isPlan || document.getElementById("mametas-trip-length-edit")) return;
    var body = document.querySelector(".article-body");
    if (!body) return;
    var target = document.getElementById(fr ? "version-trois" : "make-it-three");
    if (!target) return;

    var box = document.createElement("div");
    box.id = "mametas-trip-length-edit";
    box.className = "verdict-box";
    box.innerHTML = fr
      ? '<span>3, 5 ou 7 jours : la vraie différence</span><p><strong>3 jours :</strong> Nice + une journée à l’est + une journée à l’ouest. Coupez, ne compressez pas. <strong>5 jours :</strong> le bon équilibre pour Villefranche, Monaco/Menton et Antibes sans changer d’hôtel. <strong>7 jours :</strong> ajoutez de l’air — une journée lente et une excursion intérieure ou Cannes — plutôt qu’une nouvelle obligation quotidienne.</p><p>' + link('/fr/#riviera-first-trip-edit', 'Voir les 10 expériences qui méritent vraiment le temps →') + '</p>'
      : '<span>3, 5 or 7 days: what actually changes</span><p><strong>3 days:</strong> Nice + one eastern day + one western day. Cut; do not compress. <strong>5 days:</strong> the sweet spot for Villefranche, Monaco/Menton and Antibes without moving hotels. <strong>7 days:</strong> add air — one slow day and one inland excursion or Cannes — rather than a new obligation every morning.</p><p>' + link('/#riviera-first-trip-edit', 'See the 10 experiences that really deserve the time →') + '</p>';
    target.parentNode.insertBefore(box, target);
  }

  var nextByPath = {
    "/en/riviera-guide/nice/": [["/stay/nice/", "Choose the right Nice hotel"], ["/plan/five-days-nice-no-car/", "Build the 5-day trip"], ["/en/restaurants/nice/", "Decide where to eat"]],
    "/riviera-guide/nice/": [["/fr/dormir/nice/", "Choisir le bon hôtel à Nice"], ["/fr/planifier/cinq-jours-nice-sans-voiture/", "Construire les 5 jours"], ["/restaurants/nice/", "Décider où manger"]],
    "/en/riviera-guide/villefranche-cap-ferrat/": [["/plan/five-days-nice-no-car/#day-two", "Fit it into the 5-day plan"], ["/en/restaurants/villefranche-sur-mer/", "Choose lunch by the bay"], ["/en/day-trips/", "Compare another day trip"]],
    "/riviera-guide/villefranche-cap-ferrat/": [["/fr/planifier/cinq-jours-nice-sans-voiture/#jour-deux", "L’intégrer aux 5 jours"], ["/restaurants/villefranche-sur-mer/", "Choisir le déjeuner sur la rade"], ["/escapades/", "Comparer une autre excursion"]],
    "/en/riviera-guide/antibes/": [["/plan/five-days-nice-no-car/#day-four", "Put Antibes into the itinerary"], ["/en/restaurants/antibes/", "Choose where to eat"], ["/en/beaches/antibes/", "Choose the swim"]],
    "/riviera-guide/antibes/": [["/fr/planifier/cinq-jours-nice-sans-voiture/#jour-quatre", "Mettre Antibes dans le parcours"], ["/restaurants/antibes/", "Choisir où manger"], ["/plages/antibes/", "Choisir la baignade"]],
    "/en/riviera-guide/monaco/": [["/plan/five-days-nice-no-car/#day-three", "Fit Monaco into the 5-day plan"], ["/en/riviera-guide/menton/", "Continue to Menton — or do not"], ["/en/restaurants/monaco/", "Choose where to eat"]],
    "/riviera-guide/monaco/": [["/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois", "Mettre Monaco dans le parcours"], ["/riviera-guide/menton/", "Continuer vers Menton — ou pas"], ["/restaurants/monaco/", "Choisir où manger"]],
    "/en/riviera-guide/menton/": [["/plan/five-days-nice-no-car/#day-three", "See how Menton fits the plan"], ["/en/riviera-guide/monaco/", "Compare the Monaco pairing"], ["/en/restaurants/menton/", "Choose where to eat"]],
    "/riviera-guide/menton/": [["/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois", "Voir comment Menton tient dans le parcours"], ["/riviera-guide/monaco/", "Comparer le duo avec Monaco"], ["/restaurants/menton/", "Choisir où manger"]]
  };

  function renderNextDecision() {
    var links = nextByPath[path];
    if (!links || document.getElementById("mametas-next-decision")) return;
    var article = document.querySelector("article");
    if (!article) return;
    var body = article.querySelector(".article-body");
    if (!body) return;
    var block = document.createElement("div");
    block.id = "mametas-next-decision";
    block.className = "verdict-box";
    block.innerHTML = '<span>' + (fr ? "La prochaine décision" : "The next decision") + '</span><p>' + (fr ? "Vous avez compris le lieu. Maintenant, faites avancer le voyage plutôt que de remonter au menu." : "You understand the place. Now move the trip forward instead of climbing back to the menu.") + '</p><p>' + links.map(function (item) { return link(item[0], item[1] + ' →'); }).join(' &nbsp; ') + '</p>';
    body.appendChild(block);
  }

  renderRegional();
  renderThreeSeven();
  renderNextDecision();
})();
