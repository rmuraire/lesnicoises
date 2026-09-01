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
