fetch("menu.html")
  .then(res => res.text())
  .then(html => {
    document.getElementById("menu").innerHTML = html;

    // ВАЖНО: запуск меню после загрузки
    if (typeof initMenu === "function") {
      initMenu();
    }
  });
