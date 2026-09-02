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
  var isFrench = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  var target = isFrench ? "/explore/" : "/en/explore/";
  var label = isFrench ? "Explorer" : "Explore";

  document.querySelectorAll(".v3-nav a, .mobile-menu nav a").forEach(function (link) {
    var href = link.getAttribute("href");
    if (href === "/restaurants/" || href === "/en/restaurants/") {
      link.setAttribute("href", target);
      link.textContent = label;
    }
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
