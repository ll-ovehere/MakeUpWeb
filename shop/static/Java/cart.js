let cart = JSON.parse(localStorage.getItem("cart")) || [];

function loadCart() {
  const cartTable = document.querySelector(".cart-table tbody");
  const totalDisplay = document.querySelector(".cart-total");
  cartTable.innerHTML = "";
  let total = 0;

  if (cart.length === 0) {
    cartTable.innerHTML = "<tr><td colspan='4'>No items in your cart yet.</td></tr>";
  } else {
    cart.forEach((item) => {
      const row = `
        <tr>
          <td>${item.name}</td>
          <td>${item.quantity}</td>
          <td>$${item.price}</td>
          <td>$${item.price * item.quantity}</td>
        </tr>`;
      cartTable.innerHTML += row;
      total += item.price * item.quantity;
    });
  }
  totalDisplay.innerHTML = `<strong>Total:</strong> $${total}`;
}

window.onload = loadCart;
