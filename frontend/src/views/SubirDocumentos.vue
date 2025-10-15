<template>
    <div class="subir-documentos-container">
        <div class="navegador">
            <button @click="volverAtras" class="btn-volver">
                ← Volver
            </button>
        </div>

        <div class="formulario-panel">
            <div class="titulo">
                <h2>Subir Nuevo Documento</h2>
            </div>

            <form @submit.prevent="subirDocumento" class="formulario">
                <!-- Selección de Expediente -->
                <div class="form-group">
                    <label for="expediente">
                        Expediente <span class="requerido">*</span>
                    </label>
                    <select 
                        id="expediente" 
                        v-model="formulario.expediente" 
                        required
                    >
                        <option value="">Seleccione un expediente</option>
                        <option 
                            v-for="exp in expedientes" 
                            :key="exp.id" 
                            :value="exp.id"
                        >
                            {{ exp.numero_expediente }} - {{ exp.parte }}
                        </option>
                    </select>
                </div>

                <!-- Fecha -->
                <div class="form-group">
                    <label for="fecha">
                        Fecha <span class="requerido">*</span>
                    </label>
                    <input 
                        type="date" 
                        id="fecha" 
                        v-model="formulario.fecha" 
                        required
                    />
                </div>

                <!-- Acto Procesal -->
                <div class="form-group">
                    <label for="acto_procesal">
                        Acto Procesal <span class="requerido">*</span>
                    </label>
                    <input 
                        type="text" 
                        id="acto_procesal" 
                        v-model="formulario.acto_procesal" 
                        placeholder="Ejemplo: SUMARIO"
                        maxlength="200"
                        required
                    />
                </div>

                <!-- Resolución -->
                <div class="form-group">
                    <label for="resolucion">
                        Resolución <span class="requerido">*</span>
                    </label>
                    <input 
                        type="text" 
                        id="resolucion" 
                        v-model="formulario.resolucion" 
                        placeholder="Ejemplo: 03"
                        maxlength="200"
                        required
                    />
                </div>

                <!-- Sumilla -->
                <div class="form-group">
                    <label for="sumilla">
                        Sumilla <span class="requerido">*</span>
                    </label>
                    <textarea 
                        id="sumilla" 
                        v-model="formulario.sumilla" 
                        placeholder="Ingrese la sumilla del documento"
                        maxlength="500"
                        rows="4"
                        required
                    ></textarea>
                    <small class="contador">{{ formulario.sumilla.length }}/500 caracteres</small>
                </div>

                <!-- Archivo PDF -->
                <div class="form-group">
                    <label for="archivo_pdf">
                        Archivo PDF <span class="requerido">*</span>
                    </label>
                    <div class="file-input-container">
                        <input 
                            type="file" 
                            id="archivo_pdf" 
                            @change="manejarArchivo"
                            accept=".pdf"
                            required
                        />
                        <div v-if="nombreArchivo" class="archivo-seleccionado">
                            📄 {{ nombreArchivo }}
                        </div>
                    </div>
                </div>

                <!-- Mensaje de error -->
                <div v-if="error" class="mensaje-error">
                    {{ error }}
                </div>

                <!-- Mensaje de éxito -->
                <div v-if="exito" class="mensaje-exito">
                    {{ exito }}
                </div>

                <!-- Botones -->
                <div class="botones">
                    <button 
                        type="button" 
                        @click="limpiarFormulario" 
                        class="btn-limpiar"
                        :disabled="cargando"
                    >
                        Limpiar
                    </button>
                    <button 
                        type="submit" 
                        class="btn-subir"
                        :disabled="cargando"
                    >
                        {{ cargando ? 'Subiendo...' : 'Subir Documento' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { uploadDocumento } from '@/services/documentoService'

export default {
    name: 'SubirDocumentosView',
    setup() {
        const router = useRouter()

        const formulario = ref({
            expediente: '',
            fecha: '',
            acto_procesal: '',
            resolucion: '',
            sumilla: '',
            archivo_pdf: null
        })

        const expedientes = ref([])
        const nombreArchivo = ref('')
        const cargando = ref(false)
        const error = ref(null)
        const exito = ref(null)

        const volverAtras = () => {
            router.go(-1)
        }

        const api = import.meta.env.VITE_API_BASE_URL;

        const cargarExpedientes = async () => {
            try {
                const response = await axios.get(`${api}/expedientes/`)
                expedientes.value = response.data
            } catch (err) {
                console.error('Error al cargar expedientes:', err)
                error.value = 'No se pudieron cargar los expedientes'
            }
        }

        const manejarArchivo = (event) => {
            const archivo = event.target.files[0]
            if (archivo) {
                if (archivo.type !== 'application/pdf') {
                    error.value = 'Solo se permiten archivos PDF'
                    event.target.value = ''
                    return
                }
                if (archivo.size > 10 * 1024 * 1024) { // 10MB
                    error.value = 'El archivo no debe superar los 10MB'
                    event.target.value = ''
                    return
                }
                formulario.value.archivo_pdf = archivo
                nombreArchivo.value = archivo.name
                error.value = null
            }
        }

        const formatearFechaParaAPI = (fecha) => {
            // Asegurar formato YYYY-MM-DD para la API
            if (!fecha) return ''
            const date = new Date(fecha)
            const year = date.getFullYear()
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const day = String(date.getDate()).padStart(2, '0')
            return `${year}-${month}-${day}`
        }

        const subirDocumento = async () => {
            error.value = null
            exito.value = null
            cargando.value = true

            try {
                // Validar que todos los campos estén completos
                if (!formulario.value.expediente || !formulario.value.fecha || 
                    !formulario.value.acto_procesal || !formulario.value.resolucion || 
                    !formulario.value.sumilla || !formulario.value.archivo_pdf) {
                    error.value = 'Por favor complete todos los campos'
                    cargando.value = false
                    return
                }

                // Crear FormData
                const formData = new FormData()
                formData.append('expediente', formulario.value.expediente)
                formData.append('fecha', formatearFechaParaAPI(formulario.value.fecha))
                formData.append('acto_procesal', formulario.value.acto_procesal)
                formData.append('resolucion', formulario.value.resolucion)
                formData.append('sumilla', formulario.value.sumilla)
                formData.append('archivo_pdf', formulario.value.archivo_pdf)

                // Subir documento
                await uploadDocumento(formData)

                exito.value = 'Documento subido exitosamente'
                
                // Limpiar formulario después de 2 segundos
                setTimeout(() => {
                    limpiarFormulario()
                    exito.value = null
                }, 2000)

            } catch (err) {
                console.error('Error al subir documento:', err)
                if (err.response?.data) {
                    error.value = JSON.stringify(err.response.data)
                } else {
                    error.value = 'Error al subir el documento. Intente nuevamente.'
                }
            } finally {
                cargando.value = false
            }
        }

        const limpiarFormulario = () => {
            formulario.value = {
                expediente: '',
                fecha: '',
                acto_procesal: '',
                resolucion: '',
                sumilla: '',
                archivo_pdf: null
            }
            nombreArchivo.value = ''
            error.value = null
            exito.value = null
            
            // Limpiar input file
            const fileInput = document.getElementById('archivo_pdf')
            if (fileInput) fileInput.value = ''
        }

        onMounted(() => {
            cargarExpedientes()
        })

        return {
            formulario,
            expedientes,
            nombreArchivo,
            cargando,
            error,
            exito,
            volverAtras,
            manejarArchivo,
            subirDocumento,
            limpiarFormulario
        }
    }
}
</script>

<style scoped>
.subir-documentos-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.navegador {
    background-color: #ebebeb;
    display: flex;
    justify-content: flex-end;
    margin: 5px 0 20px 0;
    padding: 5px;
    border-radius: 6px;
}

.btn-volver {
    background-color: #cfcfcf;
    color: #000;
    border: none;
    padding: 8px 15px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s;
}

.btn-volver:hover {
    background-color: #5a6268;
    color: white;
}

.formulario-panel {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.titulo {
    background-color: #721c24;
    padding: 15px 20px;
}

.titulo h2 {
    margin: 0;
    color: white;
    font-size: 1.4rem;
    font-weight: 600;
}

.formulario {
    padding: 30px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #721c24;
    font-weight: 600;
    font-size: 0.95rem;
}

.requerido {
    color: #d9534f;
}

.form-group input[type="text"],
.form-group input[type="date"],
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 0.95rem;
    font-family: inherit;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #721c24;
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.contador {
    display: block;
    text-align: right;
    color: #666;
    font-size: 0.85rem;
    margin-top: 5px;
}

.file-input-container {
    border: 2px dashed #ccc;
    border-radius: 6px;
    padding: 20px;
    text-align: center;
    transition: border-color 0.3s;
}

.file-input-container:hover {
    border-color: #721c24;
}

.file-input-container input[type="file"] {
    width: 100%;
    cursor: pointer;
}

.archivo-seleccionado {
    margin-top: 10px;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 4px;
    color: #333;
    font-weight: 500;
}

.mensaje-error {
    padding: 12px;
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 6px;
    margin-bottom: 20px;
}

.mensaje-exito {
    padding: 12px;
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 6px;
    margin-bottom: 20px;
}

.botones {
    display: flex;
    gap: 15px;
    justify-content: flex-end;
    margin-top: 30px;
}

.btn-limpiar,
.btn-subir {
    padding: 12px 30px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 1rem;
}

.btn-limpiar {
    background-color: #6c757d;
    color: white;
}

.btn-limpiar:hover:not(:disabled) {
    background-color: #5a6268;
}

.btn-subir {
    background-color: #721c24;
    color: white;
}

.btn-subir:hover:not(:disabled) {
    background-color: #5a161c;
}

.btn-limpiar:disabled,
.btn-subir:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
    .subir-documentos-container {
        padding: 10px;
    }

    .formulario {
        padding: 20px;
    }

    .botones {
        flex-direction: column;
    }

    .btn-limpiar,
    .btn-subir {
        width: 100%;
    }
}
</style>