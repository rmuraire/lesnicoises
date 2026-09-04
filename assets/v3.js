(function () {
  var isFrench = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  var path = window.location.pathname;
  var isHome = path === "/" || path === "/fr/";
  var items;

  if (isFrench) {
    items = isHome ? [
      { label: "Planifier", href: "#planifier" },
      { label: "Lieux", href: "#lieux" },
      { label: "Dormir", href: "#hotels" },
      { label: "Explorer", href: "/explore/" },
      { label: "Maintenant", href: "#maintenant" }
    ] : [
      { label: "Planifier", href: "/fr/#planifier" },
      { label: "Lieux", href: "/riviera-guide/" },
      { label: "Dormir", href: "/fr/dormir/nice/" },
      { label: "Explorer", href: "/explore/" },
      { label: "Maintenant", href: "/bons-plans/" }
    ];
  } else {
    items = isHome ? [
      { label: "Plan", href: "#plan" },
      { label: "Places", href: "#places" },
      { label: "Stay", href: "#stay" },
      { label: "Explore", href: "/en/explore/" },
      { label: "Now", href: "#now" }
    ] : [
      { label: "Plan", href: "/#plan" },
      { label: "Places", href: "/en/riviera-guide/" },
      { label: "Stay", href: "/stay/nice/" },
      { label: "Explore", href: "/en/explore/" },
      { label: "Now", href: "/en/good-finds/" }
    ];
  }

  function currentSection() {
    if (isHome) return -1;
    if (isFrench) {
      if (path.indexOf("/fr/planifier/") === 0) return 0;
      if (path.indexOf("/riviera-guide/") === 0) return 1;
      if (path.indexOf("/fr/dormir/") === 0 || path.indexOf("/hotels/") === 0) return 2;
      if (path.indexOf("/explore/") === 0 || path.indexOf("/culture/") === 0 || path.indexOf("/restaurants/") === 0 || path.indexOf("/plages/") === 0 || path.indexOf("/escapades/") === 0) return 3;
      if (path.indexOf("/bons-plans/") === 0) return 4;
    } else {
      if (path.indexOf("/plan/") === 0) return 0;
      if (path.indexOf("/en/riviera-guide/") === 0) return 1;
      if (path.indexOf("/stay/") === 0 || path.indexOf("/en/hotels/") === 0) return 2;
      if (path.indexOf("/en/explore/") === 0 || path.indexOf("/en/culture/") === 0 || path.indexOf("/en/restaurants/") === 0 || path.indexOf("/en/beaches/") === 0 || path.indexOf("/en/day-trips/") === 0) return 3;
      if (path.indexOf("/en/good-finds/") === 0) return 4;
    }
    return -1;
  }

  var active = currentSection();
  document.querySelectorAll(".v3-nav ul, .mobile-menu nav ul").forEach(function (list) {
    var links = list.querySelectorAll(":scope > li > a");
    if (links.length < 5) return;
    items.forEach(function (item, index) {
      var link = links[index];
      link.textContent = item.label;
      link.setAttribute("href", item.href);
      if (index === active) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  });

  // The homepage shows an editorial shortlist of bases; make the complete comparison explicit.
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

  // Once the hotel decision is made, send the visitor back into the trip rather than leaving a dead end.
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

(function () {
  var menu = document.querySelector("[data-v3-menu]");
  var open = document.querySelector("[data-v3-menu-open]");
  var close = document.querySelector("[data-v3-menu-close]");

  if (!menu || !open || !close) return;

  function showMenu() {
    menu.classList.add("open");
    menu.setAttribute("aria-hidden", "false");
    document.body.classList.add("menu-open");
    close.focus();
  }

  function hideMenu() {
    menu.classList.remove("open");
    menu.setAttribute("aria-hidden", "true");
    document.body.classList.remove("menu-open");
    open.focus();
  }

  open.addEventListener("click", showMenu);
  close.addEventListener("click", hideMenu);
  menu.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      menu.classList.remove("open");
      menu.setAttribute("aria-hidden", "true");
      document.body.classList.remove("menu-open");
    });
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && menu.classList.contains("open")) hideMenu();
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
