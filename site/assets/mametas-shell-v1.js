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

/* Affiliate tracking: CJ "sid" per source page and link slot, plus one GA4 "partner_click" event
   for every partner link (the older affiliate_click / affiliate_outbound events stay untouched).
   The sid reads <lang>-<page>-<slot>, e.g. "fr-hotels-nice-la-perouse-top" (64 characters max, CJ limit).
   Slot comes from the nearest [data-aff-slot], otherwise from the component the link sits in. */
(() => {
  const CJ = /^https?:\/\/(www\.)?(kqzyfj\.com|jdoqocy\.com|anrdoezrs\.net|tkqlhce\.com|dpbolvw\.net)\/click-/i;
  const PARTNER = /kqzyfj\.com|jdoqocy\.com|anrdoezrs\.net|tkqlhce\.com|dpbolvw\.net|booking\.com\/|expedia\.com\/affiliates\/|getyourguide\.|tp\.media|travelpayouts/i;

  const clean = (value) => String(value || "").toLowerCase().normalize("NFD")
    .replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");

  function pageKey() {
    let parts = location.pathname.split("/").filter(Boolean).map(clean).filter(Boolean);
    if (parts[0] === "en" || parts[0] === "fr") parts = parts.slice(1);
    if (!parts.length) return "home";
    let key = parts.join("-");
    if (key.length > 44) key = parts.slice(-2).join("-").slice(-44);
    return key;
  }

  function slotOf(link) {
    const tagged = link.closest("[data-aff-slot]");
    if (tagged) return clean(tagged.getAttribute("data-aff-slot")).slice(0, 10) || "link";
    if (link.closest(".hotel-engine-result, .hotel-engine-actions")) return "hotelfit";
    if (link.closest(".chooser-hotels, .chooser-result-grid")) return "rivfit";
    if (link.closest(".hotel-choice-card, .hotel-card, .segment-hotel-card")) return "card";
    if (link.closest(".itinerary-stay-prompt")) return "stay";
    if (link.closest(".affiliate-cta")) return "bottom";
    return "link";
  }

  const lang = (document.documentElement.lang || "en").toLowerCase().indexOf("fr") === 0 ? "fr" : "en";
  const sidFor = (link) => `${lang}-${pageKey()}-${slotOf(link)}`.slice(0, 64);

  function decorate(link) {
    const href = link.getAttribute("href") || "";
    if (!CJ.test(href)) return;
    const sid = sidFor(link);
    let next;
    if (/[?&]sid=[^&]*/.test(href)) next = href.replace(/([?&]sid=)[^&]*/, `$1${sid}`);
    else if (href.indexOf("?") >= 0) next = href.replace("?", `?sid=${sid}&`);
    else next = `${href}?sid=${sid}`;
    if (next !== href) link.setAttribute("href", next);
  }

  function itemName(link) {
    const named = link.getAttribute("data-affiliate-hotel");
    if (named) return named.slice(0, 100);
    const card = link.closest(".hotel-choice-card, .hotel-card, .segment-hotel-card, .hotel-engine-result, .chooser-hotels li, .chooser-hotels article, li");
    const heading = card && card.querySelector("h3, h4, strong");
    const text = (heading || document.querySelector("main h1") || {}).textContent || "";
    return text.trim().replace(/\s+/g, " ").slice(0, 100);
  }

  function track(link) {
    const href = link.getAttribute("href") || "";
    if (!PARTNER.test(href) || typeof window.gtag !== "function") return;
    // Source page, language, device and traffic source come from GA4's own dimensions,
    // so the event only adds what GA4 cannot know: the slot and the hotel or activity.
    // The CJ sid (page + slot) stays on the link for CJ reports but is not sent to GA4.
    window.gtag("event", "partner_click", {
      aff_slot: slotOf(link),
      aff_item: itemName(link),
      link_url: href.replace(/([?&])sid=[^&]*&?/, "$1").replace(/[?&]$/, "").slice(0, 300),
      link_domain: (href.match(/^https?:\/\/([^/?#]+)/i) || [])[1] || "",
      transport_type: "beacon"
    });
  }

  const linkFrom = (event) => event.target && event.target.closest ? event.target.closest("a[href]") : null;

  document.querySelectorAll("a[href]").forEach(decorate);
  // Links rendered later by Hotel Fit or Riviera Fit get their sid just before they are followed.
  document.addEventListener("pointerdown", (event) => { const link = linkFrom(event); if (link) decorate(link); }, true);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Enter") { const link = linkFrom(event); if (link) decorate(link); }
  }, true);
  document.addEventListener("click", (event) => {
    const link = linkFrom(event);
    if (!link) return;
    decorate(link);
    track(link);
  }, true);
  document.addEventListener("auxclick", (event) => {
    const link = linkFrom(event);
    if (link) { decorate(link); track(link); }
  }, true);
})();
