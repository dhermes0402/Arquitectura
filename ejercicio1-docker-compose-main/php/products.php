<?php
// Obtener la URL del servicio de API desde la variable de entorno
$api_service = getenv('API_SERVICE') ?: 'http://localhost:5001';
?>

<!DOCTYPE html>
<html>
<body>
  <ul id="products"></ul>
  <script>
    const token = localStorage.getItem('jwt');
    if (!token) {
      window.location.href = 'index.php';
    }

    // Leer la URL del servicio de API desde el archivo PHP
    const apiServiceUrl = '<?php echo $api_service; ?>/products';

    fetch(apiServiceUrl, {
      headers: { Authorization: token },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Unauthorized');
        return res.json();
      })
      .then((products) => {
        const ul = document.getElementById('products');
        products.forEach((product) => {
          const li = document.createElement('li');
          li.textContent = `${product.name} - ${product.price}`;
          ul.appendChild(li);
        });
      })
      .catch(() => {
        localStorage.removeItem('jwt');
        window.location.href = 'index.php';
      });
  </script>
</body>
</html>
