const form = document.getElementById('form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

form.addEventListener('submit', e => {
  e.preventDefault();

  localStorage.setItem(
    'user',
    JSON.stringify({
      email: emailInput.value,
      password: passwordInput.value
    })
  );

  alert('Вход выполнен');
});

const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
let index = 0;

function showSlide(i) {
  slides.forEach(s => s.classList.remove('active'));
  dots.forEach(d => d.classList.remove('active'));
  slides[i].classList.add('active');
  dots[i].classList.add('active');
  index = i;
}

dots.forEach((dot, i) => {
  dot.addEventListener('click', () => showSlide(i));
});

setInterval(() => {
  index = (index + 1) % slides.length;
  showSlide(index);
}, 6000);

document.addEventListener("DOMContentLoaded", () => {

  const tabs = document.querySelectorAll(".bs-header h2");
  const products = document.querySelectorAll(".bs-products");

  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => {

      tabs.forEach(t => t.classList.remove("active"));
      products.forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      products[i].classList.add("active");

    });
  });

});

