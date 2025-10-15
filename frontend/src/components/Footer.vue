<template>
  <footer class="footer">
    <div class="footer-container">
      <p><strong>Dirección:</strong> Jr. Puno N° 459, Plaza de Armas, Puno</p>
      <p><strong>Central telefónica:</strong> 051-599200</p>
      <p class="footer-copy">
        © {{ new Date().getFullYear() }} Todos los derechos reservados.
      </p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #7b1113;
  color: white;
  text-align: center;
  padding: 20px 10px;
  margin-top: auto;
}

.footer-container p {
  margin: 4px 0;
  font-size: 0.9rem;
}

.footer-copy {
  margin-top: 8px;
  font-size: 0.8rem;
  color: #dcdcdc;
}
</style>