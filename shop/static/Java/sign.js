function validateSignup(event) {
  event.preventDefault();
  const email = document.querySelector("#signupEmail").value;
  const pass = document.querySelector("#signupPassword").value;

  if (pass.length < 6) {
    alert("Password must be at least 6 characters long");
    return;
  }
  alert("Signup successful!");
}
