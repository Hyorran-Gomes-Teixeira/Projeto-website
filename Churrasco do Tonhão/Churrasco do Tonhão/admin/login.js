document.getElementById("loginForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Substitua essas credenciais por algo seguro em um sistema real
  const validUsername = "adm";
  const validPassword = "123";

  if (username === validUsername && password === validPassword) {
    window.location.href = "reservar.html";
  } else {
    document.getElementById("errorMessage").textContent = "Usuário ou senha incorretos!";
  }
});
