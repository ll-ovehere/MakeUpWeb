function validateLogin(event) {
  event.preventDefault();
  const email = document.querySelector("#loginEmail").value;
  const pass = document.querySelector("#loginPassword").value;

  if (email === "" || pass === "") {
    alert("Please fill all fields");
    return;
  }
  alert("Login successful!");
}
