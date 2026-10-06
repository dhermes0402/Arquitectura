<?php
// Obtener la URL del servicio de login desde la variable de entorno
$login_service = getenv('LOGIN_SERVICE') ?: 'http://localhost:5000';
?>

<!DOCTYPE html>
<html>
<body>
  <form id="loginForm">
    <input type="text" id="user_name" placeholder="User Name" required />
    <input type="password" id="password" placeholder="Password" required />
    <button type="submit">Login</button>
  </form>
  <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const user_name = document.getElementById('user_name').value;
      const password = document.getElementById('password').value;

      // Leer la URL del servicio de login desde el archivo PHP
      const loginServiceUrl = '<?php echo $login_service; ?>/login';

      const response = await fetch(loginServiceUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_name, password }),
      });

      const data = await response.json();
      if (data.token) {
        localStorage.setItem('jwt', data.token);
        window.location.href = 'products.php';
      } else {
        alert('Login failed');
      }
    });
  </script>
</body>
</html>
