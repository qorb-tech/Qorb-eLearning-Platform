var password = document.getElementById("password");
var password_toggle = document.getElementById("password-toggle");

function password_Toggle() {
  if (password.type === "password") {
    password.type = "text";
    password_toggle.classList.remove("fa-eye-slash");
    password_toggle.classList.add("fa-eye");
  } else {
    password.type = "password";
    password_toggle.classList.remove("fa-eye");
    password_toggle.classList.add("fa-eye-slash");
  }
}
function success_register() {
  sucsess_register.style.display = "flex";
  console.log("succesRegistered");
}
