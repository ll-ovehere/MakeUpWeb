let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(productName, price) {
  const item = { name: productName, price: price, quantity: 1 };
  cart.push(item);
  localStorage.setItem("cart", JSON.stringify(cart));
  alert(productName + " added to cart!");
}

