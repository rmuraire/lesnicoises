/* Mametas share surface — 2026-10-01 */
(function () {
  var rawPath = window.location.pathname || "/";
  var path = rawPath.endsWith("/") ? rawPath : rawPath + "/";
  var isFrench = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;

  function begins(prefix) {
    return path.indexOf(prefix) === 0;
  }

  function shareable() {
    if (path === "/" || path === "/fr/") return false;
    if (
      path === "/en/riviera-fit/" || path === "/riviera-fit/" ||
      path === "/en/riviera-chooser/" || path === "/riviera-chooser/" ||
      begins("/en/hotels/") || begins("/hotels/") ||
      begins("/stay/") || begins("/fr/dormir/")
    ) return false;

    return [
      "/en/explore/", "/explore/",
      "/en/riviera-guide/", "/riviera-guide/",
      "/en/good-finds/", "/bons-plans/",
      "/en/culture/", "/culture/",
      "/en/beaches/", "/plages/",
      "/en/day-trips/", "/escapades/",
      "/plan/", "/fr/planifier/",
      "/en/practical/", "/pratique/",
      "/en/solo-female-french-riviera/", "/cote-dazur-femme-solo/",
      "/en/gay-french-riviera/", "/cote-dazur-gay/",
      "/en/gay-nice/", "/guide-gay-nice/"
    ].some(begins);
  }

  function mount() {
    if (!shareable()) return;
    var main = document.querySelector("main");
    var h1 = main && main.querySelector("h1");
    if (!main || !h1 || main.querySelector("[data-mametas-share]")) return;

    var canonical = document.querySelector('link[rel="canonical"]');
    var shareUrl = canonical && canonical.href ? canonical.href : window.location.origin + window.location.pathname;
    var shareTitle = h1.textContent.trim() + " | Mametas";

    var row = document.createElement("div");
    row.className = "mametas-share-row";
    row.setAttribute("data-mametas-share", "");
    row.innerHTML =
      '<button class="mametas-share-button" type="button" aria-label="' +
      (isFrench ? "Partager cette page" : "Share this page") + '">' +
      (isFrench ? "Partager ce guide" : "Share this guide") +
      '</button><span class="mametas-share-status" role="status" aria-live="polite"></span>';

    var hero = h1.closest(".article-hero, .page-hero, .hero, .hero-copy") || h1.parentElement;
    var anchor = hero && hero.querySelector(".article-deck, .lead, .standfirst, .article-meta");
    (anchor || h1).insertAdjacentElement("afterend", row);

    var button = row.querySelector(".mametas-share-button");
    var status = row.querySelector(".mametas-share-status");

    function track(method) {
      if (typeof window.gtag === "function") {
        window.gtag("event", "share_guide", { method: method, page_path: window.location.pathname });
      }
    }

    function showStatus(message) {
      status.textContent = message;
      window.setTimeout(function () { status.textContent = ""; }, 2400);
    }

    function copied() {
      showStatus(isFrench ? "Lien copié" : "Link copied");
      track("copy_link");
    }

    function copyFallback() {
      var input = document.createElement("textarea");
      input.value = shareUrl;
      input.setAttribute("readonly", "");
      input.style.position = "fixed";
      input.style.opacity = "0";
      document.body.appendChild(input);
      input.select();
      try {
        document.execCommand("copy");
        copied();
      } catch (error) {
        showStatus(isFrench ? "Copiez le lien dans la barre d’adresse" : "Copy the link from the address bar");
      } finally {
        input.remove();
      }
    }

    /* Fallback menu: in-app browsers (Instagram, Facebook, Gmail…) and some
       desktop browsers have no native share sheet. Rather than silently
       copying the link, offer the usual channels plus "copy link". */
    var menu = null;
    var enc = encodeURIComponent;
    var isTouchDevice = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ||
      (navigator.maxTouchPoints > 1 && /Macintosh/.test(navigator.userAgent));

    function closeMenu() {
      if (!menu || menu.hidden) return;
      menu.hidden = true;
      button.setAttribute("aria-expanded", "false");
    }

    function copyLink() {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(shareUrl).then(copied).catch(copyFallback);
        return;
      }
      copyFallback();
    }

    function buildMenu() {
      if (menu) return menu;
      var message = shareTitle + " " + shareUrl;
      var items = [["WhatsApp", "https://wa.me/?text=" + enc(message), "whatsapp"]];
      if (isTouchDevice) items.push([isFrench ? "SMS" : "Text message", "sms:?&body=" + enc(message), "sms"]);
      items.push(["E-mail", "mailto:?subject=" + enc(shareTitle) + "&body=" + enc(shareUrl), "email"]);
      items.push(["Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + enc(shareUrl), "facebook"]);

      menu = document.createElement("div");
      menu.className = "mametas-share-menu";
      menu.id = "mametas-share-menu";
      menu.hidden = true;
      items.forEach(function (item) {
        var link = document.createElement("a");
        link.href = item[1];
        link.textContent = item[0];
        if (item[1].indexOf("https://") === 0) {
          link.target = "_blank";
          link.rel = "noopener";
        }
        link.addEventListener("click", function () { track(item[2]); closeMenu(); });
        menu.appendChild(link);
      });
      var copy = document.createElement("button");
      copy.type = "button";
      copy.textContent = isFrench ? "Copier le lien" : "Copy link";
      copy.addEventListener("click", function () { closeMenu(); copyLink(); });
      menu.appendChild(copy);
      row.appendChild(menu);
      button.setAttribute("aria-controls", menu.id);

      document.addEventListener("click", function (event) {
        if (!row.contains(event.target)) closeMenu();
      });
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") closeMenu();
      });
      return menu;
    }

    function openMenu() {
      buildMenu().hidden = false;
      button.setAttribute("aria-expanded", "true");
    }

    button.setAttribute("aria-haspopup", "true");
    button.setAttribute("aria-expanded", "false");

    button.addEventListener("click", function () {
      if (menu && !menu.hidden) {
        closeMenu();
        return;
      }
      if (navigator.share) {
        navigator.share({ title: shareTitle, url: shareUrl }).then(function () {
          track("native_share");
        }).catch(function (error) {
          if (!error || error.name !== "AbortError") openMenu();
        });
        return;
      }
      openMenu();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  } else {
    mount();
  }
})();
