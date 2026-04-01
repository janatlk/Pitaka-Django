function initMenu() {

  const navItems = document.querySelectorAll(".menu-nav-item");
  const mega = document.querySelector(".menu-mega");
  const sections = document.querySelectorAll(".menu-mega-section");

  if (!navItems.length || !mega) return;

  let closeTimer;

  function openMega() {
    clearTimeout(closeTimer);
    mega.classList.add("open");
  }

  function closeMega() {
    closeTimer = setTimeout(() => {
      mega.classList.remove("open");
      navItems.forEach(i => i.classList.remove("active"));
    }, 300);
  }

  /* ================= ВЕРХНЕЕ МЕНЮ ================= */
  navItems.forEach(item => {
    item.addEventListener("mouseenter", () => {
      openMega();

      navItems.forEach(i => i.classList.remove("active"));
      item.classList.add("active");

      sections.forEach(section => {
        const isActive = section.dataset.menu === item.dataset.menu;
        section.classList.toggle("active", isActive);

        if (isActive) {
          const firstTab = section.querySelector(".menu-mega-tab");
          if (firstTab) activateMegaTab(firstTab);
        }
      });
    });
  });

  mega.addEventListener("mouseenter", openMega);
  mega.addEventListener("mouseleave", closeMega);

  /* ================= MEGA TABS ================= */

  function activateMegaTab(tab) {
    const section = tab.closest(".menu-mega-section");
    const targetId = tab.dataset.tab;

    section.querySelectorAll(".menu-mega-tab")
      .forEach(t => t.classList.remove("active"));

    section.querySelectorAll(".menu-mega-content")
      .forEach(c => c.classList.remove("active"));

    tab.classList.add("active");

    const target = section.querySelector("#" + targetId);
    if (target) target.classList.add("active");
  }

  document.querySelectorAll(".menu-mega-tab").forEach(tab => {
    tab.addEventListener("mouseenter", () => {
      activateMegaTab(tab);
    });
  });

  /* ================= STYLE SUBTABS ================= */

  document.querySelectorAll(".menu-style-link").forEach(link => {
    link.addEventListener("mouseenter", () => {

      const section = link.closest(".menu-mega-content");
      const target = link.dataset.style;

      section.querySelectorAll(".menu-style-link")
        .forEach(l => l.classList.remove("active"));

      section.querySelectorAll(".menu-style-grid")
        .forEach(g => g.classList.remove("active"));

      link.classList.add("active");

      const grid = section.querySelector(`.menu-style-grid[data-style="${target}"]`);
      if (grid) grid.classList.add("active");
    });
  });

  /* ================= WATCH / MAGSAFE ================= */

  document.querySelectorAll(".menu-watch-link").forEach(link => {
    link.addEventListener("mouseenter", () => {

      const section = link.closest(".menu-mega-section");
      const target = link.dataset.watch;

      section.querySelectorAll(".menu-watch-link")
        .forEach(l => l.classList.remove("active"));

      section.querySelectorAll(".menu-watch-grid")
        .forEach(g => g.classList.remove("active"));

      link.classList.add("active");

      const grid = section.querySelector(`.menu-watch-grid[data-watch="${target}"]`);
      if (grid) grid.classList.add("active");
    });
  });

}

/* запуск после загрузки menu.html */
document.addEventListener("DOMContentLoaded", initMenu);
 

document.querySelectorAll('.menu-mega-col a').forEach(link => {
  link.addEventListener('click', function() {
    document.querySelectorAll('.menu-mega-col a')
      .forEach(el => el.classList.remove('active'));

    this.classList.add('active');
  });
});
