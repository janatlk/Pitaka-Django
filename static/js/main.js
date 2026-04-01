// Load mega menu if menu container exists
const menuContainer = document.getElementById('menu');
if (menuContainer) {
  fetch("menu.html")
    .then(res => res.text())
    .then(html => {
      menuContainer.innerHTML = html;
    });
}
