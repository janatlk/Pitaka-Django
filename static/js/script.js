
const header = document.querySelector('.header');
const navItems = document.querySelectorAll('.nav-item[data-menu]');
const mega = document.querySelector('.mega');
const sections = document.querySelectorAll('.mega-section');

let closeTimer;

function openMega() {
  clearTimeout(closeTimer);
  if (mega) mega.classList.add('open');
}

function closeMega() {
  closeTimer = setTimeout(() => {
    if (mega) mega.classList.remove('open');
    navItems.forEach(i => i.classList.remove('active'));
  }, 350);
}

/* Наведение на пункты меню */
navItems.forEach(item => {
  item.addEventListener('mouseenter', () => {
    openMega();

    navItems.forEach(i => i.classList.remove('active'));
    item.classList.add('active');

    sections.forEach(section => {
      const isActive = section.dataset.menu === item.dataset.menu;
      section.classList.toggle('active', isActive);

      if (isActive) {
        const firstTab = section.querySelector('.mega-tab, .watch-link, .style-link');
       if (firstTab) {
  setTimeout(() => firstTab.click(), 0);
}
      }
    });
  });
});

/* Наведение на саму мега-зону */
if (mega) {
  mega.addEventListener('mouseenter', openMega);
  mega.addEventListener('mouseleave', closeMega);
}


// 2. УНИВЕРСАЛЬНЫЙ обработчик для всех вкладок (Phone, Tablet, Watch, Style)
document.addEventListener('click', (e) => {
  /* ================= MEGA TABS (Phone / Tablet) ================= */
  const megaTab = e.target.closest('.mega-tab');
  if (megaTab) {
    const section = megaTab.closest('.mega-section');
    const targetId = megaTab.dataset.tab;

    section.querySelectorAll('.mega-tab')
      .forEach(t => t.classList.remove('active'));
    section.querySelectorAll('.mega-content')
      .forEach(c => c.classList.remove('active'));

    megaTab.classList.add('active');
    const target = section.querySelector('#' + targetId);
    if (target) target.classList.add('active');
    return;
  }

  /* ================= WATCH / MAGSAFE ================= */
  const watchLink = e.target.closest('.watch-link');
  if (watchLink) {
    const section = watchLink.closest('.mega-section');
    const target = watchLink.dataset.watch;

    section.querySelectorAll('.watch-link')
      .forEach(l => l.classList.remove('active'));
    section.querySelectorAll('.watch-grid')
      .forEach(g => g.classList.remove('active'));

    watchLink.classList.add('active');
    const grid = section.querySelector(`.watch-grid[data-watch="${target}"]`);
    if (grid) grid.classList.add('active');
    return;
  }

  /* ================= STYLE ================= */
  const styleLink = e.target.closest('.style-link');
  if (styleLink) {
    const content = styleLink.closest('#style');
    const target = styleLink.dataset.style;

    content.querySelectorAll('.style-link')
      .forEach(l => l.classList.remove('active'));
    content.querySelectorAll('.style-grid')
      .forEach(g => g.classList.remove('active'));

    styleLink.classList.add('active');
    const grid = content.querySelector(`.style-grid[data-style="${target}"]`);
    if (grid) grid.classList.add('active');
  }
});


// ===== SEARCH ELEMENTS =====
const products = [
  { name: "Sunset iPhone 17 Pro Max", img: "menu-sunset.avif" },
  { name: "Moonrise iPhone 17 Pro Max", img: "menu-moonrise.avif" },
  { name: "Over The Horizon iPhone 17 Pro", img: "menu-over-the-horizon.avif" },
  { name: "Black/Grey Summa iPhone 17", img: "menu-black-grey.avif" },
  { name: "AirPods Pro 3 Case", img: "menu-airpodspro3-case.avif" },
  { name: "MagSafe Wallet Sunset", img: "menu-wallet-sunset.avif" },
  { name: "MagSafe Power Bank Moonrise", img: "menu-powerbank-moonrise.avif" },
  { name: "Galaxy Z Fold 7 Case", img: "menu-fold7.avif" }
];

const searchBtn = document.querySelector('.icon-item.search');
const searchOverlay = document.getElementById('searchOverlay');
const closeSearch = document.getElementById('closeSearch');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');

searchBtn.onclick = () => {
  searchOverlay.classList.add('active');
  searchInput.focus();
};

closeSearch.onclick = () => {
  if (searchOverlay) searchOverlay.classList.remove('active');
  if (searchInput) {
    searchInput.value = '';
    searchInput.innerHTML = '';
  }
};

if (searchInput) {
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    if (searchResults) searchResults.innerHTML = '';

    if (query.length < 2) return;

    products
      .filter(p => p.name.toLowerCase().includes(query))
      .forEach(p => {
        const item = document.createElement('div');
        item.className = 'search-item';
        item.innerHTML = `
          <img src="${p.img}">
        <div>
          <span>NEW</span>
          <p>${p.name}</p>
        </div>
      `;
        item.onclick = () => {
          alert(`Открыть товар: ${p.name}`);
        };
        searchResults.appendChild(item);
      });
  });
}


const form = document.getElementById('form');
const switchBtn = document.getElementById('switch');
const title = document.getElementById('title');
const error = document.getElementById('error');
const profile = document.getElementById('profile');
const userEmail = document.getElementById('userEmail');
const logoutBtn = document.getElementById('logout');

const emailInput = document.getElementById('emailInput');
const passwordInput = document.getElementById('passwordInput');

let isLogin = true;

/* ===== Проверка сохранённого пользователя ===== */
if (form) {

  const savedUser = JSON.parse(localStorage.getItem('user'));
  if (savedUser) showProfile(savedUser.email);

  switchBtn.onclick = () => {
    isLogin = !isLogin;
    title.textContent = isLogin ? 'Вход' : 'Регистрация';
    switchBtn.textContent = isLogin ? 'Создать аккаунт' : 'Уже есть аккаунт';
    form.querySelector('.black-btn').textContent =
      isLogin ? 'Войти' : 'Зарегистрироваться';
    error.textContent = '';
  };

  form.onsubmit = (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (password.length < 6) {
      error.textContent = 'Пароль должен быть не менее 6 символов';
      return;
    }

    if (isLogin) {
      const user = JSON.parse(localStorage.getItem('user'));
      if (!user || user.email !== email || user.password !== password) {
        error.textContent = 'Неверный email или пароль';
        return;
      }
      showProfile(email);
    } else {
      localStorage.setItem('user', JSON.stringify({ email, password }));
      showProfile(email);
    }
  };

  if (logoutBtn) {
    logoutBtn.onclick = () => {
      localStorage.removeItem('user');
      location.reload();
    };
  }
}


/* ===== Show profile ===== */
function showProfile(email) {
  form.classList.add('hidden');
  switchBtn.classList.add('hidden');
  title.textContent = 'Аккаунт';
  profile.classList.remove('hidden');
  userEmail.textContent = email;
}
document.addEventListener("DOMContentLoaded", () => {
  console.log('DOM loaded, initializing slider...');

  const heroSlides = document.querySelectorAll('.hero-slider .slide');
  const heroDots = document.querySelectorAll('.hero-slider .dot');
  
  console.log('Found slides:', heroSlides.length);
  console.log('Found dots:', heroDots.length);
  
  let heroIndex = 0;

  function showHero(i) {
    console.log('Showing slide', i);
    heroSlides.forEach(s => s.classList.remove('active'));
    heroDots.forEach(d => d.classList.remove('active'));

    heroSlides[i].classList.add('active');
    heroDots[i].classList.add('active');
    heroIndex = i;
  }

  heroDots.forEach((d, i) => {
    d.onclick = () => {
      console.log('Dot clicked', i);
      showHero(i);
    };
  });

  console.log('Starting auto-rotate...');
  setInterval(() => {
    showHero((heroIndex + 1) % heroSlides.length);
  }, 5000);

});


// ===== BEST SELLERS / NEW ARRIVALS SWITCH =====

const bsTabs = document.querySelectorAll('.bs-header h2');
const bsBlocks = document.querySelectorAll('.bs-products');

bsTabs.forEach((tab, index) => {
  tab.addEventListener('click', () => {

    // убираем active
    bsTabs.forEach(t => t.classList.remove('active'));
    bsBlocks.forEach(b => b.classList.remove('active'));

    // добавляем active
    tab.classList.add('active');
    bsBlocks[index].classList.add('active');

  });
});


// ===== FORCE OPEN MEGA ON CATALOG PAGE =====
if (window.location.pathname.includes("catalog.html")) {

  window.addEventListener("load", () => {

    const mega = document.querySelector(".mega");
    const phoneNav = document.querySelector('.nav-item[data-menu="phone"]');
    const phoneSection = document.querySelector('.mega-section[data-menu="phone"]');

    if (!mega || !phoneNav || !phoneSection) return;

    // Открываем меню
    mega.classList.add("open");

    // Активируем пункт меню
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    phoneNav.classList.add("active");

    // Показываем секцию PHONE
    document.querySelectorAll('.mega-section').forEach(s => s.classList.remove('active'));
    phoneSection.classList.add("active");

    // Включаем вкладку "По устройствам"
    const firstTab = phoneSection.querySelector('.mega-tab[data-tab="devices"]');
    if (firstTab) firstTab.click();

  });

}

const slides = document.querySelectorAll(".green-slide");
const dots = document.querySelectorAll(".gdot");

let current = 0;

function showSlide(i) {
  slides.forEach(s => s.classList.remove("active"));
  dots.forEach(d => d.classList.remove("active"));

  slides[i].classList.add("active");
  dots[i].classList.add("active");
}

dots.forEach((dot, i) => {
  dot.addEventListener("click", () => {
    current = i;
    showSlide(current);
  });
});

setInterval(() => {
  current = (current + 1) % slides.length;
  showSlide(current);
}, 5000);


const reviewItems = document.querySelectorAll(".review");
const dotsWrapper = document.querySelector(".review-dots");

let activeIndex = 0;
let autoSlider;

// создаём точки
reviewItems.forEach((_, index) => {
  const dotElement = document.createElement("span");

  if (index === 0) {
    dotElement.classList.add("active");
  }

  dotElement.addEventListener("click", () => {
    showSlide(index);
    restartAuto();
  });

  dotsWrapper.appendChild(dotElement);
});

const dotItems = document.querySelectorAll(".review-dots span");

function showSlide(index) {
  reviewItems[activeIndex].classList.remove("active");
  dotItems[activeIndex].classList.remove("active");

  activeIndex = index;

  reviewItems[activeIndex].classList.add("active");
  dotItems[activeIndex].classList.add("active");
}

function nextSlide() {
  let nextIndex = activeIndex + 1;
  if (nextIndex >= reviewItems.length) {
    nextIndex = 0;
  }
  showSlide(nextIndex);
}

function startAuto() {
  autoSlider = setInterval(nextSlide, 4000);
}

function restartAuto() {
  clearInterval(autoSlider);
  startAuto();
}

startAuto();