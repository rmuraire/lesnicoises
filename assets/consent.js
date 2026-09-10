(function () {
  "use strict";
  var STORAGE_KEY = "mametas_optional_consent_v2";
  var LEGACY_STORAGE_KEY = "mametas_analytics_consent";
  var ANALYTICS_ID = "G-9FXW5HMLWG";
  var DRIVE_SRC = "https://tp-em.com/NTcyMzE4.js?t=572318";
  var language = (document.documentElement.lang || "en").toLowerCase().indexOf("fr") === 0 ? "fr" : "en";
  var analyticsLoaded = false;
  var driveLoaded = false;
  var copy = language === "fr" ? {
    title:"Vos choix, sans détour",
    text:"Mametas utilise des outils optionnels pour mesurer l’audience et améliorer la monétisation affiliée. Vous pouvez tout accepter, tout refuser ou choisir.",
    accept:"Tout accepter",
    reject:"Tout refuser",
    choose:"Choisir",
    save:"Enregistrer mes choix",
    settings:"Choix des cookies",
    privacy:"En savoir plus",
    privacyUrl:"/fr/confidentialite/",
    analytics:"Mesure d’audience",
    analyticsHelp:"Google Analytics nous aide à comprendre quelles pages sont réellement utiles.",
    drive:"Outils affiliés intelligents",
    driveHelp:"Travelpayouts Drive analyse le contenu et l’usage du site pour proposer ou optimiser des éléments d’affiliation."
  } : {
    title:"Your choices, no fuss",
    text:"Mametas uses optional tools for audience measurement and affiliate monetisation. You can accept all, reject all or choose.",
    accept:"Accept all",
    reject:"Reject all",
    choose:"Choose",
    save:"Save my choices",
    settings:"Cookie choices",
    privacy:"Learn more",
    privacyUrl:"/privacy/",
    analytics:"Audience measurement",
    analyticsHelp:"Google Analytics helps us understand which pages are genuinely useful.",
    drive:"Smart affiliate tools",
    driveHelp:"Travelpayouts Drive analyses site content and usage to add or optimise affiliate elements."
  };

  function readChoices(){
    try{
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if(!raw)return null;
      var parsed = JSON.parse(raw);
      if(typeof parsed.analytics !== "boolean" || typeof parsed.drive !== "boolean")return null;
      return parsed;
    }catch(error){return null;}
  }

  function saveChoices(value){
    try{
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
      window.localStorage.removeItem(LEGACY_STORAGE_KEY);
    }catch(error){}
  }

  function loadAnalytics(){
    if(analyticsLoaded || document.querySelector('script[data-mametas-analytics]'))return;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){window.dataLayer.push(arguments);};
    window.gtag("consent","default",{analytics_storage:"granted"});
    window.gtag("js",new Date());
    window.gtag("config",ANALYTICS_ID,{anonymize_ip:true});
    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + ANALYTICS_ID;
    script.setAttribute("data-mametas-analytics","true");
    document.head.appendChild(script);
  }

  function loadDrive(){
    if(driveLoaded || document.querySelector('script[data-mametas-travelpayouts-drive]'))return;
    driveLoaded = true;
    var script = document.createElement("script");
    script.async = true;
    script.src = DRIVE_SRC;
    script.setAttribute("data-cmp-ab","2");
    script.setAttribute("data-mametas-travelpayouts-drive","true");
    document.head.appendChild(script);
  }

  function removeAnalyticsCookies(){
    document.cookie.split(";").forEach(function(part){
      var name = part.split("=")[0].trim();
      if(name.indexOf("_ga") !== 0)return;
      document.cookie = name + "=; Max-Age=0; path=/; SameSite=Lax";
      document.cookie = name + "=; Max-Age=0; path=/; domain=.mametas.com; SameSite=Lax";
    });
  }

  function disableAnalytics(){
    if(typeof window.gtag === "function")window.gtag("consent","update",{analytics_storage:"denied"});
    removeAnalyticsCookies();
  }

  function closeBanner(){
    var banner = document.querySelector("[data-consent-banner]");
    if(banner)banner.remove();
  }

  function applyChoices(value){
    if(value.analytics)loadAnalytics();
    else disableAnalytics();
    if(value.drive)loadDrive();
  }

  function persistChoices(value){
    var previous = readChoices();
    var mustReload = !!(previous && ((previous.analytics && !value.analytics) || (previous.drive && !value.drive)));
    saveChoices(value);
    closeBanner();
    if(mustReload){window.location.reload();return;}
    applyChoices(value);
  }

  function showBanner(expanded){
    if(document.querySelector("[data-consent-banner]"))return;
    var current = readChoices() || {analytics:false,drive:false};
    var banner = document.createElement("section");
    banner.className = "consent-banner";
    banner.setAttribute("data-consent-banner","true");
    banner.setAttribute("role","dialog");
    banner.setAttribute("aria-modal","false");
    banner.setAttribute("aria-labelledby","consent-title");
    banner.innerHTML = '<div class="consent-copy"><strong id="consent-title">'+copy.title+'</strong><p>'+copy.text+' <a href="'+copy.privacyUrl+'">'+copy.privacy+'</a></p><div data-consent-options '+(expanded?'':'hidden')+' style="margin-top:12px"><label style="display:block;margin:8px 0"><input type="checkbox" data-consent-analytics> <strong>'+copy.analytics+'</strong><br><span style="font-size:.92em">'+copy.analyticsHelp+'</span></label><label style="display:block;margin:8px 0"><input type="checkbox" data-consent-drive> <strong>'+copy.drive+'</strong><br><span style="font-size:.92em">'+copy.driveHelp+'</span></label></div></div><div class="consent-actions"><button type="button" class="consent-reject" data-consent-reject>'+copy.reject+'</button><button type="button" class="consent-reject" data-consent-choose '+(expanded?'hidden':'')+'>'+copy.choose+'</button><button type="button" class="consent-accept" data-consent-save '+(expanded?'':'hidden')+'>'+copy.save+'</button><button type="button" class="consent-accept" data-consent-accept>'+copy.accept+'</button></div>';
    document.body.appendChild(banner);
    var options = banner.querySelector("[data-consent-options]");
    var analyticsBox = banner.querySelector("[data-consent-analytics]");
    var driveBox = banner.querySelector("[data-consent-drive]");
    var chooseButton = banner.querySelector("[data-consent-choose]");
    var saveButton = banner.querySelector("[data-consent-save]");
    analyticsBox.checked = current.analytics;
    driveBox.checked = current.drive;
    banner.querySelector("[data-consent-accept]").addEventListener("click",function(){persistChoices({analytics:true,drive:true});});
    banner.querySelector("[data-consent-reject]").addEventListener("click",function(){persistChoices({analytics:false,drive:false});});
    chooseButton.addEventListener("click",function(){options.hidden=false;chooseButton.hidden=true;saveButton.hidden=false;});
    saveButton.addEventListener("click",function(){persistChoices({analytics:analyticsBox.checked,drive:driveBox.checked});});
    banner.querySelector("[data-consent-reject]").focus();
  }

  function addSettingsControl(){
    var footer = document.querySelector("footer");
    if(!footer || footer.querySelector("[data-consent-settings]"))return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "consent-settings";
    button.setAttribute("data-consent-settings","true");
    button.textContent = copy.settings;
    button.addEventListener("click",function(){showBanner(true);});
    var links = footer.querySelector(".privacy-links") || footer;
    links.appendChild(button);
  }

  function loadLayer(src,attr){
    if(document.querySelector('script['+attr+']'))return;
    var script = document.createElement("script");
    script.src = src;
    script.defer = true;
    script.setAttribute(attr,"true");
    document.head.appendChild(script);
  }

  function initialise(){
    addSettingsControl();
    loadLayer("/assets/editorial-layer.js?v=1.0","data-mametas-editorial-layer");
    loadLayer("/assets/practical-layer.js?v=1.0","data-mametas-practical-layer");
    loadLayer("/assets/journey-layer.js?v=1.0","data-mametas-journey-layer");
    var choices = readChoices();
    if(choices)applyChoices(choices);
    else showBanner(false);
  }

  if(document.readyState === "loading")document.addEventListener("DOMContentLoaded",initialise);
  else initialise();
})();
