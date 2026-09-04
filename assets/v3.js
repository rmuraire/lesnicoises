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
      if (path.indexOf("/explore/") === 0 || path.indexOf("/culture/") === 0 || path.indexOf("/restaurants/") === 0 || path.indexOf("/plages/") === 0 || path.indexOf("/excursions/") === 0) return 3;
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
