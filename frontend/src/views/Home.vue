<template>
  <section class="home-container">
    <h1 class="title">Búsqueda de Expedientes</h1>

    <form @submit.prevent="buscarExpediente" class="form-container">
      <div class="form-group">
        <label for="distrito">Distrito Judicial</label>
        <input
          type="text"
          id="distrito"
          v-model="filtros.distrito"
          placeholder="PUNO"
          required
        />
      </div>

      <div class="form-group">
        <label for="numero">Número de Expediente</label>
        <input
          type="text"
          id="numero"
          v-model="numeroFormateado"
          @input="formatearNumeroExpediente"
          placeholder="00704-2021-0-2101-JR-LA-01"
          maxlength="29"
          required
        />
      </div>

      <div class="form-group">
        <label for="parte">Parte</label>
        <input
          type="text"
          id="parte"
          v-model="filtros.parte"
          placeholder="BUSTINZA CARCASI"
          required
        />
      </div>

      <div class="captcha-container">
        <div class="captcha-display">{{ captchaTexto }}</div>
        <button type="button" class="btn-refresh" @click="generarCaptcha">
          🔄
        </button>
      </div>

      <div class="form-group">
        <label for="captchaInput">Ingrese el texto del captcha</label>
        <input
          type="text"
          id="captchaInput"
          v-model="captchaInput"
          placeholder="Escriba el código mostrado"
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
import { ref, onMounted } from 'vue'
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
    const captchaTexto = ref('')
    const captchaInput = ref('')

    const numeroFormateado = ref('')

    const formatearNumeroExpediente = (event) => {
      let valor = event.target.value.replace(/[^0-9A-Za-z]/g, '') // Solo alfanuméricos
      let formateado = ''
      
      // Formato: 00704-2021-0-2101-JR-LA-01
      // Patrón: 5-4-1-4-2-2-2
      if (valor.length > 0) formateado += valor.substring(0, 5)
      if (valor.length > 5) formateado += '-' + valor.substring(5, 9)
      if (valor.length > 9) formateado += '-' + valor.substring(9, 10)
      if (valor.length > 10) formateado += '-' + valor.substring(10, 14)
      if (valor.length > 14) formateado += '-' + valor.substring(14, 16)
      if (valor.length > 16) formateado += '-' + valor.substring(16, 18)
      if (valor.length > 18) formateado += '-' + valor.substring(18, 20)
      
      numeroFormateado.value = formateado
      // Guardar el valor sin guiones para enviar al backend
      filtros.value.numero = valor
    }

    const generarCaptcha = () => {
      const caracteres = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'
      captchaTexto.value = Array.from(
        { length: 5 },
        () => caracteres[Math.floor(Math.random() * caracteres.length)]
      ).join('')
      captchaInput.value = ''
    }

    const buscarExpediente = async () => {
  error.value = null

  // 1️⃣ Revisar el valor del captcha
  console.log('Captcha ingresado:', captchaInput.value)
  console.log('Captcha correcto:', captchaTexto.value)

  if (captchaInput.value.trim() !== captchaTexto.value.trim()) {
    error.value = 'Captcha incorrecto. Intente nuevamente.'
    generarCaptcha()
    return
  }

  cargando.value = true

  const api = import.meta.env.VITE_API_BASE_URL;
  console.log('API Base URL:', api)

  try {
    // 2️⃣ Revisar los filtros formateados antes de enviarlos
    const distrito = filtros.value.distrito.trim().toUpperCase()
    const numero = filtros.value.numero.replace(/[^0-9A-Za-z]/g, '').toUpperCase()
    const parte = filtros.value.parte.trim().toUpperCase()

    console.log('Filtros a enviar:', { distrito, numero, parte })

    const response = await axios.get(`${api}/expedientes/`, {
      params: {
        distrito_judicial: distrito,
        numero_expediente: numero,
        parte: parte
      }
    })

    // 3️⃣ Revisar la respuesta completa de la API
    console.log('Respuesta de la API:', response)

    if (!response.data.length) {
      console.log('No se encontró ningún expediente.')
      error.value = 'No se encontró ningún expediente con esos datos.'
      generarCaptcha()
      return
    }

    const expediente = response.data[0]
    console.log('Expediente encontrado:', expediente)

    sessionStorage.setItem('expediente_id', expediente.id)
    router.push(`/expediente/${expediente.id}`)
  } catch (err) {
    // 4️⃣ Mostrar el error completo
    console.error('Error al hacer la consulta:', err)
    error.value = 'Ocurrió un error al buscar el expediente.'
    generarCaptcha()
  } finally {
    cargando.value = false
  }
}

    onMounted(() => {
      generarCaptcha()
    })

    return { 
      filtros, 
      cargando, 
      error, 
      captchaTexto,
      captchaInput,
      numeroFormateado,
      formatearNumeroExpediente,
      buscarExpediente,
      generarCaptcha
    }
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
  color: #7e1010;
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

label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #7e1010;
}

input {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.captcha-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
}

.captcha-display {
  flex: 1;
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 0.3rem;
  text-align: center;
  background: white;
  padding: 0.8rem;
  border-radius: 4px;
  font-family: monospace;
}

.btn-refresh {
  background: #9b9b9b;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.2rem;
}

.btn-refresh:hover {
  background: #8d8d8d;
}

.btn-buscar {
  background-color: #7b1113;
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.btn-buscar:hover {
  background-color: #690c0d;
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