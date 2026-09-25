(function () {
  var isFrench = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  var path = window.location.pathname;
  var isHome = path === "/" || path === "/fr/";
  var items = isFrench ? [
    { label: "Plan", href: "/fr/planifier/" },
    { label: "Destinations", href: "/riviera-guide/" },
    { label: "Dormir", href: "/hotels/" },
    { label: "Explorer", href: "/explore/" },
    { label: "Pratique", href: "/pratique/" }
  ] : [
    { label: "Plan", href: "/plan/" },
    { label: "Places", href: "/en/riviera-guide/" },
    { label: "Stay", href: "/en/hotels/" },
    { label: "Explore", href: "/en/explore/" },
    { label: "Practical", href: "/en/practical/" }
  ];

  function currentSection() {
    if (isHome) return -1;
    if (isFrench) {
      if (path.indexOf("/riviera-fit/") === 0 || path.indexOf("/fr/planifier/") === 0) return 0;
      if (path.indexOf("/riviera-guide/") === 0) return 1;
      if (path.indexOf("/fr/dormir/") === 0 || path.indexOf("/hotels/") === 0) return 2;
      if (path.indexOf("/explore/") === 0 || path.indexOf("/culture/") === 0 || path.indexOf("/restaurants/") === 0 || path.indexOf("/plages/") === 0 || path.indexOf("/escapades/") === 0) return 3;
      if (path.indexOf("/pratique/") === 0 || path.indexOf("/bons-plans/transfert-aeroport-nice/") === 0 || path.indexOf("/bons-plans/train-ou-bus/") === 0 || path.indexOf("/bons-plans/que-reserver/") === 0 || path.indexOf("/bons-plans/nice-quand-il-pleut/") === 0) return 4;
    } else {
      if (path.indexOf("/en/riviera-fit/") === 0 || path.indexOf("/plan/") === 0) return 0;
      if (path.indexOf("/en/riviera-guide/") === 0) return 1;
      if (path.indexOf("/stay/") === 0 || path.indexOf("/en/hotels/") === 0) return 2;
      if (path.indexOf("/en/explore/") === 0 || path.indexOf("/en/culture/") === 0 || path.indexOf("/en/restaurants/") === 0 || path.indexOf("/en/beaches/") === 0 || path.indexOf("/en/day-trips/") === 0) return 3;
      if (path.indexOf("/en/practical/") === 0 || path.indexOf("/en/good-finds/nice-airport-transfer/") === 0 || path.indexOf("/en/good-finds/train-or-bus/") === 0 || path.indexOf("/en/good-finds/what-to-book/") === 0 || path.indexOf("/en/good-finds/nice-in-the-rain/") === 0) return 4;
    }
    return -1;
  }

  function navMarkup() {
    var active = currentSection();
    return items.map(function (item, index) {
      return '<li><a href="' + item.href + '"' + (index === active ? ' aria-current="page"' : '') + '>' + item.label + '</a></li>';
    }).join("");
  }

  function alternate(lang) {
    var link = document.querySelector('link[rel~="alternate"][hreflang="' + lang + '"]');
    if (link && link.href) return link.href;
    if (lang === "fr") return isFrench ? path : "/fr/";
    return isFrench ? "/" : path;
  }

  function languageMarkup() {
    return '<a href="' + alternate("fr") + '"' + (isFrench ? ' aria-current="page"' : '') + '>FR</a><span>/</span><a href="' + alternate("en") + '"' + (!isFrench ? ' aria-current="page"' : '') + '>EN</a>';
  }

  var header = document.querySelector(".v3-header");
  var inner = header && header.querySelector(".v3-header-inner");
  var desktopNav = inner && inner.querySelector(".v3-nav");
  if (desktopNav) {
    var desktopList = desktopNav.querySelector("ul");
    if (!desktopList) {
      desktopList = document.createElement("ul");
      desktopNav.appendChild(desktopList);
    }
    desktopList.innerHTML = navMarkup();
  }

  if (inner) {
    var desktopLang = inner.querySelector(".lang-switch");
    if (!desktopLang) {
      desktopLang = document.createElement("div");
      desktopLang.className = "lang-switch";
      desktopLang.setAttribute("aria-label", isFrench ? "Langue" : "Language");
      inner.appendChild(desktopLang);
    }
    desktopLang.innerHTML = languageMarkup();

    var buttons = inner.querySelectorAll("[data-v3-menu-open]");
    var openButton = buttons[0];
    Array.prototype.slice.call(buttons, 1).forEach(function (button) { button.remove(); });
    if (!openButton) {
      openButton = document.createElement("button");
      openButton.className = "menu-button";
      openButton.type = "button";
      openButton.setAttribute("data-v3-menu-open", "");
      openButton.innerHTML = "<span></span><span></span><span></span>";
      inner.appendChild(openButton);
    }
    openButton.setAttribute("aria-label", isFrench ? "Ouvrir le menu" : "Open menu");
    openButton.setAttribute("aria-expanded", "false");
  }

  var menu = document.querySelector("[data-v3-menu]");
  if (!menu && header) {
    menu = document.createElement("div");
    menu.className = "mobile-menu";
    menu.setAttribute("data-v3-menu", "");
    menu.setAttribute("aria-hidden", "true");
    header.insertAdjacentElement("afterend", menu);
  }
  if (menu) {
    menu.innerHTML =
      '<div class="mobile-menu-top"><span class="v3-brand-name">Mametas</span><button class="mobile-menu-close" type="button" aria-label="' +
      (isFrench ? "Fermer le menu" : "Close menu") +
      '" data-v3-menu-close>×</button></div><nav aria-label="' +
      (isFrench ? "Navigation mobile" : "Mobile navigation") +
      '"><ul>' + navMarkup() + '</ul></nav><div class="lang-switch">' + languageMarkup() + "</div>";
  }

  if (isHome) {
    var baseSection = document.getElementById("bases");
    var baseCopy = baseSection && baseSection.querySelector(".section-heading > p");
    if (baseCopy && !baseCopy.querySelector(".all-bases-link")) {
      var allBases = document.createElement("a");
      allBases.className = "text-link all-bases-link";
      allBases.href = isFrench ? "/riviera-guide/" : "/en/riviera-guide/";
      allBases.textContent = isFrench ? "Voir toutes les bases, Monaco et Menton compris →" : "See all bases, including Monaco and Menton →";
      baseCopy.appendChild(document.createElement("br"));
      baseCopy.appendChild(allBases);
    }
  }
})();

(function () {
  var isFrench = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  var path = window.location.pathname;
  var isNiceChooser = path === "/stay/nice/" || path === "/fr/dormir/nice/";
  if (!isNiceChooser) return;

  var section = document.getElementById(isFrench ? "pratique" : "practical");
  var copy = section && section.querySelector(".hotel-style-heading > p");
  if (copy && !copy.querySelector(".journey-link")) {
    var link = document.createElement("a");
    link.className = "text-link journey-link";
    link.href = isFrench ? "/fr/planifier/cinq-jours-nice-sans-voiture/" : "/plan/five-days-nice-no-car/";
    link.textContent = isFrench ? "Voir comment notre parcours de 5 jours utilise le train →" : "See how our 5-day no-car plan uses the train →";
    copy.appendChild(document.createElement("br"));
    copy.appendChild(link);
  }

  var intro = document.querySelector(".chooser-intro > p");
  if (intro && !intro.querySelector(".base-link")) {
    var baseLink = document.createElement("a");
    baseLink.className = "text-link base-link";
    baseLink.href = isFrench ? "/riviera-guide/" : "/en/riviera-guide/";
    baseLink.textContent = isFrench ? "Pas encore sûr de dormir à Nice ? Comparez d’abord les bases →" : "Not sure Nice should be your base? Compare the bases first →";
    intro.appendChild(document.createElement("br"));
    intro.appendChild(baseLink);
  }

  var main = document.querySelector("main");
  if (main && !main.querySelector(".journey-next-section")) {
    var next = document.createElement("section");
    next.className = "v3-section journey-next-section";
    next.innerHTML = isFrench
      ? '<div class="wrap"><div class="section-heading"><div><p class="eyebrow">Hôtel choisi ? Très bien.</p><h2>Maintenant, organisez le séjour.</h2></div><p>Continuer à comparer des hôtels après avoir choisi le vôtre est une activité, mais pas encore des vacances.</p></div><div class="decision-grid"><a class="decision-card" href="/fr/planifier/cinq-jours-nice-sans-voiture/"><span class="decision-number">01</span><h3>Construire les journées</h3><p>Le parcours de 5 jours relie Nice aux excursions réalistes.</p><span class="text-link">Ouvrir le parcours →</span></a><a class="decision-card" href="/restaurants/"><span class="decision-number">02</span><h3>Choisir où manger</h3><p>Des adresses sélectionnées, pas un inventaire de tables.</p><span class="text-link">Voir les restaurants →</span></a><a class="decision-card" href="/bons-plans/transfert-aeroport-nice/"><span class="decision-number">03</span><h3>Arriver sans cagade</h3><p>Tram, train ou taxi depuis l’aéroport de Nice.</p><span class="text-link">Voir le transfert →</span></a></div></div>'
      : '<div class="wrap"><div class="section-heading"><div><p class="eyebrow">Hotel sorted? Good.</p><h2>Now build the trip.</h2></div><p>Continuing to compare hotels after choosing one is a hobby, not yet a holiday.</p></div><div class="decision-grid"><a class="decision-card" href="/plan/five-days-nice-no-car/"><span class="decision-number">01</span><h3>Build the days</h3><p>The 5-day plan connects Nice to realistic excursions.</p><span class="text-link">Open the plan →</span></a><a class="decision-card" href="/en/restaurants/"><span class="decision-number">02</span><h3>Choose where to eat</h3><p>Selected addresses, not a census of tables.</p><span class="text-link">See restaurants →</span></a><a class="decision-card" href="/en/good-finds/nice-airport-transfer/"><span class="decision-number">03</span><h3>Arrive without a cagade</h3><p>Tram, train or taxi from Nice Airport.</p><span class="text-link">See the transfer →</span></a></div></div>';
    main.appendChild(next);
  }
})();

/* Translate the shared hotel-decision layer on French hotel pages. */
(function () {
  var isFrench = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  if (!isFrench || window.location.pathname.indexOf('/hotels/') !== 0) return;
  var path = window.location.pathname;
  var fr = {
    '/hotels/nice/anantara-plaza-nice/':['Carré d’Or / Albert 1er','Central en bord de mer · idéal pour tout faire à pied','Premier séjour avec centre, mer et grand confort','Luxe'],
    '/hotels/nice/apollinaire-nice/':['Centre / Durandy','Central · entre transports et Vieux-Nice','Séjour urbain à pied sans payer le front de mer','Haut de gamme'],
    '/hotels/nice/boutique-hotel-nice-cote-dazur/':['Nice-Ville / Musiciens','Central côté gare · départs faciles','Séjour sans voiture et budget maîtrisé','Milieu de gamme'],
    '/hotels/nice/hotel-66/':['Nice-Ville / Jean Médecin','Central côté gare · idéal pour rayonner','Séjour sans voiture et itinéraires en train','Milieu de gamme'],
    '/hotels/nice/hotel-du-couvent/':['Vieux-Nice','Cœur historique · priorité à l’atmosphère','Séjour où l’hôtel compte autant que la ville','Luxe'],
    '/hotels/nice/la-perouse/':['Colline du Château / bord de mer','Aux portes du Vieux-Nice · mer et caractère','Séjour romantique avec le Nice carte postale tout près','Haut de gamme'],
    '/hotels/nice/le-negresco/':['Promenade / Carré d’Or','Monument du front de mer · central et destination en soi','Séjour iconique où l’hôtel fait partie du voyage','Luxe'],
    '/hotels/nice/maison-albar-le-victoria/':['Jean Médecin / bord de mer','Hyper-central · mer, shopping et transports réunis','Séjour urbain luxe avec logistique minimale','Luxe'],
    '/hotels/nice/palais-de-la-mediterranee/':['Promenade / Carré d’Or','Central en bord de mer · plage et ville faciles','Séjour Riviera classique avec tout à proximité','Luxe'],
    '/hotels/nice/villa-victoria/':['Musiciens / Carré d’Or','Central et calme · base plus paisible à pied','Séjour urbain au calme sans s’exiler','Haut de gamme'],
    '/hotels/antibes/hotel-la-place/':['Centre / Vieil Antibes','Central · vieille ville et gare pratiques','Antibes sans voiture et courts séjours','Milieu de gamme'],
    '/hotels/antibes/la-villa-port-antibes/':['Port Vauban / Vieil Antibes','Central côté port · idéal à pied','Antibes comme base sans sacrifier l’atmosphère','Haut de gamme'],
    '/hotels/cap-d-antibes/cap-d-antibes-beach-hotel/':['Cap d’Antibes / bord de mer','Adresse resort · volontairement loin du centre','Séjour plage où l’hôtel est la destination','Luxe'],
    '/hotels/cap-d-antibes/la-villa-cap-d-antibes/':['Juan-les-Pins / bord du Cap','Résidentiel et balnéaire · plus calme que le centre','Piscine et plage avec la ville encore accessible','Haut de gamme'],
    '/hotels/cannes/carlton-cannes/':['Croisette','Front de mer premium · Cannes au pied de l’hôtel','Cannes iconique et séjours liés aux événements','Luxe'],
    '/hotels/cannes/hotel-martinez/':['Croisette','Front de mer premium · élégant et très praticable à pied','Plage, glamour et Cannes en période d’événement','Luxe'],
    '/hotels/cannes/le-cavendish/':['Centre / Carnot','Lisière du centre · pratique plutôt que balnéaire','Cannes à pied avec davantage de discrétion','Haut de gamme'],
    '/hotels/cannes/majestic-cannes/':['Palais / Croisette','Hyper-central · idéal pour événements et Suquet','Premier Cannes sans envie de perdre du temps en trajets','Luxe'],
    '/hotels/eze/la-chevre-d-or/':['Èze Village','Village perché · spectaculaire et volontairement isolé','Séjour-destination plutôt que base de transport','Luxe'],
    '/hotels/menton/villa-genesis/':['Borrigo / bord de mer','Résidentiel en bord de mer · calme avec centre accessible','Menton au ralenti avec priorité plage','Luxe'],
    '/hotels/monaco/hotel-de-paris-monte-carlo/':['Carré d’Or / Casino','Hyper-central Monaco · l’adresse est le sujet','Parenthèse monégasque avec tout le cérémonial à proximité','Luxe'],
    '/hotels/roquebrune-cap-martin/the-maybourne-riviera/':['Falaises de Roquebrune','Retraite panoramique · volontairement loin de la vie urbaine','Séjour centré sur l’hôtel et la vue','Luxe'],
    '/hotels/saint-jean-cap-ferrat/royal-riviera/':['Baie des Fourmis / Cap Ferrat','Resort en bord de mer · entre Beaulieu et la presqu’île','Séjour plage avec excursions Riviera possibles','Luxe'],
    '/hotels/saint-tropez/lou-pinet/':['Saint-Tropez résidentiel','En retrait du centre · intimité avant animation immédiate','Piscine et hôtel avec Saint-Tropez à proximité','Luxe'],
    '/hotels/antibes/royal-antibes/':['Bord de mer / lisière vieille ville','Central en bord de mer · plage et vieille ville faciles','Antibes entre plage et ville','Haut de gamme'],
    '/hotels/antibes/best-western-hotel-journel-antibes/':['Antibes résidentiel / bord du centre','Proche centre · plus calme, moins carte postale','Séjour à prix contenu avec Antibes encore accessible à pied','Milieu de gamme'],
    '/hotels/monaco/port-palace/':['Port Hercule','Central côté port · Monaco facile à pied','Premier séjour avec vue sans le cérémonial de la place du Casino','Luxe'],
    '/hotels/monaco/columbus-hotel-monte-carlo/':['Fontvieille','Monaco plus calme · loin du cœur Casino','Séjour plus posé et journées centrées sur Fontvieille','Haut de gamme'],
    '/hotels/beaulieu-sur-mer/hotel-carlton-beaulieu-sur-mer/':['Beaulieu centre / Baie des Fourmis','Central et calme · plage et gare utiles','Séjour Riviera sans voiture à l’est de Nice','Haut de gamme'],
    '/hotels/beaulieu-sur-mer/hotel-marcellin/':['Beaulieu centre','Petit centre pratique · gare et mer faciles','Séjour simple sans voiture avec Beaulieu comme base','Milieu de gamme'],
    '/hotels/saint-tropez/pastis-hotel-saint-tropez/':['Saint-Tropez / bord du centre','Retraite proche centre · plus calme que le port','Boutique-hôtel avec la ville proche mais pas sous les fenêtres','Haut de gamme'],
    '/hotels/saint-tropez/hotel-de-paris-saint-tropez/':['Centre / bord du port','Hyper-central · idéal pour Saint-Tropez à pied','Court séjour glamour sans envie de conduire','Luxe'],
    '/hotels/cannes/hotel-le-canberra/':['Rue d’Antibes / bord Croisette','Central · shopping, plage et gare gérables à pied','Cannes à pied sans l’échelle d’un palace','Haut de gamme'],
    '/hotels/menton/ibis-styles-menton-centre/':['Menton centre','Central · gare, vieille ville et budget bien placés','Séjour sans voiture et itinéraires Riviera pratiques','Milieu de gamme']
  };
  var values = fr[path];
  var facts = document.querySelector('.hotel-facts');
  if (!values || !facts) return;
  var labels=['Quartier','Logique de localisation','Idéal pour','Budget'];
  facts.querySelectorAll(':scope > div').forEach(function(cell,i){
    var label=cell.querySelector('span'); var value=cell.querySelector('b');
    if(label) label.textContent=labels[i]||label.textContent;
    if(value && values[i]) value.textContent=values[i];
  });
})();

(function () {
  var menu = document.querySelector("[data-v3-menu]");
  var open = document.querySelector("[data-v3-menu-open]");
  var close = document.querySelector("[data-v3-menu-close]");

  if (!menu || !open || !close || open.getAttribute("data-menu-bound") === "true") return;
  open.setAttribute("data-menu-bound", "true");

  function showMenu() {
    menu.classList.add("open");
    menu.setAttribute("aria-hidden", "false");
    open.setAttribute("aria-expanded", "true");
    document.body.classList.add("menu-open");
    close.focus();
  }

  function hideMenu(returnFocus) {
    menu.classList.remove("open");
    menu.setAttribute("aria-hidden", "true");
    open.setAttribute("aria-expanded", "false");
    document.body.classList.remove("menu-open");
    if (returnFocus !== false) open.focus();
  }

  open.addEventListener("click", showMenu);
  close.addEventListener("click", function () { hideMenu(true); });
  menu.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () { hideMenu(false); });
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && menu.classList.contains("open")) hideMenu(true);
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1080 && menu.classList.contains("open")) hideMenu(false);
  });
})();

(function () {
  document.querySelectorAll("[data-affiliate-network][data-affiliate-hotel]").forEach(function (link) {
    link.addEventListener("click", function () {
      var detail = {
        network: link.getAttribute("data-affiliate-network"),
        hotel: link.getAttribute("data-affiliate-hotel"),
        language: document.documentElement.lang || "",
        path: window.location.pathname
      };

      window.dispatchEvent(new CustomEvent("mametas:affiliate-click", { detail: detail }));

      if (typeof window.gtag === "function") {
        window.gtag("event", "affiliate_click", {
          affiliate_network: detail.network,
          hotel_id: detail.hotel,
          page_language: detail.language,
          page_path: detail.path
        });
      }
    });
  });
})();

/* Audit guard: canonical internal anchors. */
(function(){
  var fixes={
    '/fr/dormir/nice/#anime':'/fr/dormir/nice/#vivant',
    '/fr/dormir/nice/#paisible':'/fr/dormir/nice/#calme',
    '/fr/planifier/cinq-jours-nice-sans-voiture/#day-three':'/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois'
  };
  document.querySelectorAll('a[href]').forEach(function(link){
    var href=link.getAttribute('href');
    if(fixes[href]) link.setAttribute('href',fixes[href]);
  });
})();


/* Mametas dialect: link one first-use term per page to the mini-lexicon. */
(function(){
  function addDialectLink(){
    if(!document.body || document.documentElement.dataset.mametasDialectLink === '1') return;
    var lang=(document.documentElement.lang || 'en').toLowerCase().indexOf('fr') === 0 ? 'fr' : 'en';
    if(location.pathname.indexOf('/lexique/') >= 0 || location.pathname.indexOf('/en/lexicon/') >= 0) return;
    var base=lang === 'fr' ? '/lexique/' : '/en/lexicon/';
    var terms=[
      {re:/(mèfi)/i,id:'mefi'},
      {re:/(pichoun|pitchoun)/i,id:'pichoun'},
      {re:/(cagade)/i,id:'cagade'},
      {re:/(dégun)/i,id:'degun'},
      {re:/(niocou)/i,id:'niocou'},
      {re:/(paillassou)/i,id:'paillassou'},
      {re:/(empégué)/i,id:'empegue'},
      {re:/(ficanas)/i,id:'ficanas'}
    ];
    var walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    var nodes=[],node;
    while((node=walker.nextNode())) nodes.push(node);
    for(var i=0;i<nodes.length;i++){
      node=nodes[i];
      var parent=node.parentElement;
      if(!parent || parent.closest('a,script,style,button,code,pre,noscript,textarea')) continue;
      for(var j=0;j<terms.length;j++){
        var match=node.nodeValue.match(terms[j].re);
        if(!match) continue;
        var at=match.index, before=node.nodeValue.slice(0,at), after=node.nodeValue.slice(at+match[0].length);
        var frag=document.createDocumentFragment();
        if(before) frag.appendChild(document.createTextNode(before));
        var link=document.createElement('a');
        link.className='dialect-inline';
        link.href=base+'#'+terms[j].id;
        link.title=lang === 'fr' ? 'Voir le petit lexique niçois' : 'See the Niçois mini-lexicon';
        link.textContent=match[0];
        frag.appendChild(link);
        if(after) frag.appendChild(document.createTextNode(after));
        parent.replaceChild(frag,node);
        document.documentElement.dataset.mametasDialectLink='1';
        return;
      }
    }
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded',addDialectLink);
  else addDialectLink();
})();
