(function () {
  "use strict";

  var STORAGE_KEY = "mametas_analytics_consent";
  var ANALYTICS_ID = "G-9FXW5HMLWG";
  var language = (document.documentElement.lang || "en").toLowerCase().indexOf("fr") === 0 ? "fr" : "en";
  var analyticsLoaded = false;

  var copy = language === "fr" ? {
    title: "Votre choix, sans détour",
    text: "Mametas utilise Google Analytics uniquement avec votre accord pour comprendre les pages réellement utiles. Refuser ne change rien au site.",
    accept: "Accepter la mesure",
    reject: "Continuer sans mesure",
    settings: "Choix des cookies",
    privacy: "En savoir plus",
    privacyUrl: "/fr/confidentialite/"
  } : {
    title: "Your choice, no fuss",
    text: "Mametas uses Google Analytics only with your permission to understand which pages are genuinely useful. Declining changes nothing on the site.",
    accept: "Allow analytics",
    reject: "Continue without analytics",
    settings: "Cookie choices",
    privacy: "Learn more",
    privacyUrl: "/privacy/"
  };

  function readChoice() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (error) { return null; }
  }

  function saveChoice(value) {
    try { window.localStorage.setItem(STORAGE_KEY, value); } catch (error) { /* Storage can be unavailable. */ }
  }

  function loadAnalytics() {
    if (analyticsLoaded || document.querySelector('script[data-mametas-analytics]')) return;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", ANALYTICS_ID, { anonymize_ip: true });

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + ANALYTICS_ID;
    script.setAttribute("data-mametas-analytics", "true");
    document.head.appendChild(script);
  }

  function removeAnalyticsCookies() {
    document.cookie.split(";").forEach(function (part) {
      var name = part.split("=")[0].trim();
      if (name.indexOf("_ga") !== 0) return;
      document.cookie = name + "=; Max-Age=0; path=/; SameSite=Lax";
      document.cookie = name + "=; Max-Age=0; path=/; domain=.mametas.com; SameSite=Lax";
    });
  }

  function closeBanner() {
    var banner = document.querySelector("[data-consent-banner]");
    if (banner) banner.remove();
  }

  function choose(value) {
    saveChoice(value);
    if (value === "granted") {
      loadAnalytics();
    } else {
      if (typeof window.gtag === "function") {
        window.gtag("consent", "update", { analytics_storage: "denied" });
      }
      removeAnalyticsCookies();
    }
    closeBanner();
  }

  function showBanner() {
    if (document.querySelector("[data-consent-banner]")) return;

    var banner = document.createElement("section");
    banner.className = "consent-banner";
    banner.setAttribute("data-consent-banner", "true");
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-modal", "false");
    banner.setAttribute("aria-labelledby", "consent-title");
    banner.innerHTML =
      '<div class="consent-copy"><strong id="consent-title">' + copy.title + '</strong><p>' + copy.text +
      ' <a href="' + copy.privacyUrl + '">' + copy.privacy + '</a></p></div>' +
      '<div class="consent-actions"><button type="button" class="consent-reject" data-consent-reject>' + copy.reject +
      '</button><button type="button" class="consent-accept" data-consent-accept>' + copy.accept + '</button></div>';
    document.body.appendChild(banner);
    banner.querySelector("[data-consent-accept]").addEventListener("click", function () { choose("granted"); });
    banner.querySelector("[data-consent-reject]").addEventListener("click", function () { choose("denied"); });
    banner.querySelector("[data-consent-reject]").focus();
  }

  function addSettingsControl() {
    var footer = document.querySelector("footer");
    if (!footer || footer.querySelector("[data-consent-settings]")) return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "consent-settings";
    button.setAttribute("data-consent-settings", "true");
    button.textContent = copy.settings;
    button.addEventListener("click", showBanner);
    var links = footer.querySelector(".privacy-links") || footer;
    links.appendChild(button);
  }

  function initialise() {
    addSettingsControl();
    var choice = readChoice();
    if (choice === "granted") loadAnalytics();
    if (choice !== "granted" && choice !== "denied") showBanner();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialise);
  } else {
    initialise();
  }
})();
