<template>
    <header class="header">
        <div class="header-container">
            <div class="header-left">
            <img src="@/assets/logo-pj.png" alt="Logo PJ" class="header-logo" />
            <div class="header-text">
                <h1>Poder Judicial del Perú</h1>
                <p>Corte Superior de Justicia de Puno</p>
            </div>
            </div>

            <div class="header-right">
            <img src="@/assets/logo-cej.png" alt="Logo CEJ" class="header-logo" />
            </div>
        </div>
    </header>
</template>

<style scoped>
.header {
  background-color: #fafafa;
  color: rgb(12, 12, 12);
  padding: 10px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-logo {
  height: 55px;
  width: auto;
}

.header-text h1 {
  font-size: 1.2rem;
  margin: 0;
  font-weight: 600;
}

.header-text p {
  font-size: 0.9rem;
  margin: 0;
  color: #333333;
}

@media (max-width: 600px) {
  .header-text {
    display: none; /* Oculta texto en pantallas pequeñas */
  }
  .header {
    text-align: center;
  }
}
</style>