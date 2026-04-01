// Получаем модель из URL
const params = new URLSearchParams(window.location.search);
const model = params.get("model");

// База товаров (можно расширять)
const PRODUCTS = {
  iphone17promax: {
    title: "iPhone 17 Pro Max Case",
    price: "4 990 сом",
    image: "products/iphone17promax.jpg",
    desc: "Премиальный защитный чехол."
  },
  fold7: {
    title: "Galaxy Z Fold 7 Case",
    price: "5 500 сом",
    image: "products/fold7.jpg",
    desc: "Тонкий и прочный карбоновый чехол."
  },
  wallet : {
    title: "MagSafe Wallet Black/Grey",
    price: "3 200 сом",
    image: "products/wallet-bgt.jpg",
    desc: "Тонкий кардхолдер с магнитом."
  }
};

// Если товар найден
if (PRODUCTS[model]) {
  const product = PRODUCTS[model];

  document.getElementById("productTitle").textContent = product.title;
  document.getElementById("productPrice").textContent = product.price;
  document.getElementById("productImage").src = product.image;
  document.getElementById("productDesc").textContent = product.desc;

} else {
  document.getElementById("productTitle").textContent = "Товар не найден";
}
