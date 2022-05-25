var password = document.getElementById('password1')
var password_toggle = document.getElementById('password-toggle')

function password_Toggle() {
	if (password.type === 'password') {
		password.type = 'text'
		password_toggle.classList.remove('fa-eye-slash')
		password_toggle.classList.add('fa-eye')
	} else {
		password.type = 'password'
		password_toggle.classList.remove('fa-eye')
		password_toggle.classList.add('fa-eye-slash')
	}
}

var password2 = document.getElementById('password2')
var password_toggle2 = document.getElementById('password-toggle2')

function password_Toggle2() {
	if (password2.type === 'password') {
		password2.type = 'text'
		password_toggle2.classList.remove('fa-eye-slash')
		password_toggle2.classList.add('fa-eye')
	} else {
		password2.type = 'password'
		password_toggle2.classList.remove('fa-eye')
		password_toggle2.classList.add('fa-eye-slash')
	}
}


function success_register() {
	sucsess_register.style.display = "flex";
	console.log("succesRegistered");
  }

  function success_enter() {
	sucsess_enter.style.display = "flex";
	console.log("succesRegistered");
  }
