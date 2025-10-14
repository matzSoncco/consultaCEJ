<template>
  <section class="home-container">
    <h1 class="title">Consulta de Expedientes</h1>
    <p class="subtitle">Ingrese los datos para consultar su expediente</p>

    <form @submit.prevent="buscarExpediente" class="form-container">
      <div class="form-group">
        <label for="distrito">Distrito Judicial</label>
        <input
          type="text"
          id="distrito"
          v-model="filtros.distrito"
          placeholder="Ejemplo: Puno"
          required
        />
      </div>

      <div class="form-group">
        <label for="numero">Número de Expediente</label>
        <input
          type="text"
          id="numero"
          v-model="filtros.numero"
          placeholder="Ejemplo: 0101010"
          required
        />
      </div>

      <div class="form-group">
        <label for="parte">Parte</label>
        <input
          type="text"
          id="parte"
          v-model="filtros.parte"
          placeholder="Ejemplo: SONCCO MAX"
          required
        />
      </div>

      <button type="submit" :disabled="cargando" class="btn-buscar">
        {{ cargando ? 'Buscando...' : 'Buscar expediente' }}
      </button>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()

    const filtros = ref({
      distrito: '',
      numero: '',
      parte: ''
    })

    const cargando = ref(false)
    const error = ref(null)

    const buscarExpediente = async () => {
      cargando.value = true
      error.value = null

      try {
        const response = await axios.get('http://127.0.0.1:8000/api/expedientes/', {
          params: {
            distrito_judicial: filtros.value.distrito,
            numero_expediente: filtros.value.numero,
            parte: filtros.value.parte
          }
        })

        if (!response.data.length) {
          error.value = 'No se encontró ningún expediente con esos datos.'
          return
        }

        const expediente = response.data[0]
        localStorage.setItem('expediente_id', expediente.id)
        router.push(`/expediente/${expediente.id}`)
      } catch (err) {
        console.error(err)
        error.value = 'Ocurrió un error al buscar el expediente.'
      } finally {
        cargando.value = false
      }
    }

    return { filtros, cargando, error, buscarExpediente }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 0.3rem;
}

.subtitle {
  text-align: center;
  color: #555;
  margin-bottom: 2rem;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

input {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.btn-buscar {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.btn-buscar:hover {
  background-color: #0056b3;
}

.btn-buscar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  color: #c00;
  text-align: center;
  font-weight: 600;
}
</style>