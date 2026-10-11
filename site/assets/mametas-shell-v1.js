(() => {
  "use strict";

  const breakpoint = 1080;

  function closeMenu(details, restoreFocus = false) {
    if (!details || !details.open) return;
    details.open = false;
    const summary = details.querySelector(":scope > summary");
    if (summary) summary.setAttribute("aria-expanded", "false");
    document.documentElement.classList.remove("mametas-menu-open");
    document.body.classList.remove("mametas-menu-open");
    if (restoreFocus && summary) summary.focus();
  }

  function syncMenu(details) {
    const summary = details.querySelector(":scope > summary");
    const open = details.open;
    if (summary) summary.setAttribute("aria-expanded", open ? "true" : "false");
    document.documentElement.classList.toggle("mametas-menu-open", open);
    document.body.classList.toggle("mametas-menu-open", open);
  }

  function initMenu(details) {
    const summary = details.querySelector(":scope > summary");
    if (!summary) return;

    summary.setAttribute("aria-expanded", details.open ? "true" : "false");

    details.addEventListener("toggle", () => syncMenu(details));

    details.querySelectorAll(".mametas-global-mobile-panel a").forEach((link) => {
      link.addEventListener("click", () => closeMenu(details, false));
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && details.open) {
        event.preventDefault();
        closeMenu(details, true);
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > breakpoint && details.open) {
        closeMenu(details, false);
      }
    }, { passive: true });
  }

  document.querySelectorAll("details.mametas-global-mobile").forEach(initMenu);
})();
