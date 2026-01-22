function validateContactForm(event) {
  event.preventDefault();
  const email = document.querySelector("#contactEmail").value;

  if (!email.includes("@")) {
    alert("Please enter a valid email address");
    return;
  }
  alert("Message sent successfully!");
}
