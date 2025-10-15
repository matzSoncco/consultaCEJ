<template>
  <div class="expediente-container">
    <div class="navegador">
      <button @click="volverAtras" class="btn-volver">
        ←
      </button>
    </div>

    <div class="titulo">
      <h1>RESULTADO DE LA BÚSQUEDA</h1>
    </div>

    <div class="buscador">
        <div class="texto">
            <p><strong>Expedientes encontrados: 1</strong></p>
            <p><strong>Coincidencia con datos de la parte: 1</strong></p>
        </div>
        <div class="caja-buscador">
            <div class="campo">
            <input 
                type="text" 
                v-model="busquedaTexto"
                placeholder="Parte procesal"
            />
            </div>
            <div class="boton-buscar">
            <button @click="buscarEnExpedientes">Buscar</button>
            </div>
        </div>
    </div>

    <div class="resumen-expediente">
      <div class="left-part">
        <div class="numero-expediente">1</div>
      </div>

      <div class="center">
        <div class="datos-expediente">
          <p><strong>{{ expediente.numero_expediente }}</strong></p>
          <p><strong>JUZGADO DE TRABAJO - {{ expediente.distrito_judicial }}</strong></p>
        </div>
        <div class="partes">
            <p>DEMANDANTE: BUSTINZA CARCASI, ISMAEL ALEJANDRO. DEMANDADO: PROCURADOR PUBLICO DEL GOBIERNO REGIONAL DE PUNO . DEMANDADO: RED DE SALUD EL COLLAO ILAVE .</p>
        </div>
      </div>

      <div class="right-part">
        <button @click="verDetalles" class="btn-detalles">
          <img src="@/assets/lupa.png"></img>
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="cargando" class="loading">
      Cargando expediente...
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'ExpedienteView',
  setup() {
    const router = useRouter()
    const route = useRoute()

    const expediente = ref({
      numero_expediente: '',
      distrito_judicial: '',
      parte: '',
    })

    const cargando = ref(true)
    const error = ref(null)

    const volverAtras = () => {
      router.push('/')
    }

    const verDetalles = () => {
      const expedienteId = route.params.id
      router.push(`/expediente/${expedienteId}/detalle`)
    }

    const formatearFecha = (fecha) => {
      if (!fecha) return 'N/A'
      const date = new Date(fecha)
      return date.toLocaleDateString('es-PE', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const cargarExpediente = async () => {
      try {
        const expedienteId = route.params.id
        const response = await axios.get(`http://127.0.0.1:8000/api/expedientes/${expedienteId}/`)
        
        expediente.value = response.data
        cargando.value = false
      } catch (err) {
        console.error(err)
        error.value = 'Error al cargar el expediente'
        cargando.value = false
      }
    }

    onMounted(() => {
      cargarExpediente()
    })

    return {
      expediente,
      cargando,
      error,
      volverAtras,
      verDetalles,
      formatearFecha
    }
  }
}
</script>

<style scoped>
.expediente-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 10px;
}

.navegador {
    background-color: #ebebeb;
    display: flex;
    justify-content: flex-end;
    margin: 5px;
    padding: 5px;
}

.btn-volver {
    background-color: #cfcfcf;
    color: rgb(0, 0, 0);
    border: none;
    padding: 5px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s;
}

.btn-volver:hover {
    background-color: #5a6268;
}

.titulo {
    text-align: center;
    margin: 10px 0 10px 0 ;
}

.titulo h1 {
    font-size: 25px;
    color: #721c24;
    font-family: 'Courier New', Courier, monospace;
    font-weight: 700;
    margin: 0;
}

.buscador{
    height: 45px;
    margin-bottom: 10px;
    background: #8f8f8f;
    padding: 1.2rem;
    display: flex;
    justify-content: space-between;
}

.texto {
  margin-bottom: 1rem;
}

.texto p {
  margin: 0.3rem 0;
  color: #000000;
  font-size: 0.95rem;
}

.caja-buscador {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.campo {
  flex: 1;
}

.campo input {
  width: 90%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.95rem;
}

.campo input:focus {
  outline: none;
  border-color: #999;
}

.boton-buscar button {
  padding: 0.6rem 1.5rem;
  background-color: #5a6268;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
}

.boton-buscar button:hover {
  background-color: #4a5258;
}

.resumen-expediente {
  display: flex;
  align-items: stretch;
  background: rgb(197, 197, 197);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 15px;
  gap: 15px;
}

.left-part {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 50px;
}

.numero-expediente {
    color: rgb(0, 0, 0);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.center {
    display: block;
    align-items: center;
}

.datos-expediente {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.datos-expediente p {
    margin: 5px;
    color: #000000;
}

.datos-expediente strong {
  color: #000000;
  font-weight: 600;
}

.right-part {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 50px;
}

.btn-detalles img {
    height: 20px;
    width: auto;
    border: none;
}

.btn-detalles:hover {
  transform: translateY(-2px);
}

.error-message {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
}
</style>