<template>
    <div class="expediente-container">
        <div class="navegador">
            <button @click="volverAtras" class="btn-volver">
                ←
            </button>
        </div>

        <div class="panel">
            <div class="titulo">
                <h2>Reporte de Expediente</h2>
            </div>
            <div class="expediente-item">
                <span class="dato-label">Número de Expediente:</span>
                <strong><span class="dato-valor">{{ expediente.numero_expediente || 'N/A' }}</span></strong>
            </div>
            <div class="datos">
                <div class="izquierda">
                    <div class="dato-item">
                        <span class="dato-label">Órgano Jurisdiccional:</span>
                        <span class="dato-valor">JUZGADO DE TRABAJO - PUNO</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Órgano Jurisdiccional:</span>
                        <span class="dato-valor">{{ expediente.organo_jurisdiccional || 'N/A' }}</span>
                    </div>
                </div>
                <div class="derecha">
                    <div class="dato-item">
                        <span class="dato-label">Especialidad:</span>
                        <span class="dato-valor">{{ expediente.especialidad || 'N/A' }}</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Estado:</span>
                        <span class="dato-valor">{{ expediente.estado || 'N/A' }}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel">
            <div class="titulo">
                <h2>Partes del Proceso</h2>
            </div>
            <div class="datos">
                <div class="dato-item">
                    <span class="dato-label">Demandante/Denunciante:</span>
                    <span class="dato-valor">{{ expediente.parte || 'N/A' }}</span>
                </div>
                <div class="dato-item">
                    <span class="dato-label">Materia:</span>
                    <span class="dato-valor">{{ expediente.materia || 'N/A' }}</span>
                </div>
                <div class="dato-item">
                    <span class="dato-label">Fecha de Inicio:</span>
                    <span class="dato-valor">{{ formatearFecha(expediente.fecha_inicio) }}</span>
                </div>
                <div class="dato-item">
                    <span class="dato-label">Juez/Magistrado:</span>
                    <span class="dato-valor">{{ expediente.juez || 'No asignado' }}</span>
                </div>
            </div>
        </div>

        <div class="panel">
            <div class="titulo">
                <h2>Documentos del Expediente</h2>
            </div>
            <div class="datos-bbdd">
                <div v-if="cargandoDocumentos" class="mensaje-carga">
                    Cargando documentos...
                </div>

                <div v-else-if="errorDocumentos" class="mensaje-error">
                    {{ errorDocumentos }}
                </div>

                <div v-else-if="documentos.length === 0" class="mensaje-vacio">
                    No hay documentos registrados para este expediente.
                </div>

                <div v-else class="lista-documentos">
                    <div 
                        v-for="documento in documentos" 
                        :key="documento.id" 
                        class="documento-card"
                    >
                        <div class="documento-info">
                            <div class="documento-header">
                                <span class="documento-numero">Doc. #{{ documento.id }}</span>
                                <span class="documento-fecha">{{ formatearFecha(documento.fecha) }}</span>
                            </div>
                            
                            <div class="documento-detalle">
                                <p><strong>Acto Procesal:</strong> {{ documento.acto_procesal }}</p>
                                <p><strong>Resolución:</strong> {{ documento.resolucion }}</p>
                                <p><strong>Sumilla:</strong> {{ documento.sumilla }}</p>
                            </div>
                        </div>

                        <div class="documento-acciones">
                            <button 
                                @click="descargarDocumento(documento)" 
                                class="btn-descargar"
                                :disabled="!documento.archivo_pdf"
                            >
                                📄 Descargar PDF
                            </button>
                        </div>
                    </div>

                    <!-- Paginación -->
                    <div v-if="totalPaginas() > 1" class="paginacion">
                        <button 
                            @click="cambiarPagina(paginaActual - 1)"
                            :disabled="paginaActual === 1"
                            class="btn-paginacion"
                        >
                            Anterior
                        </button>
                        
                        <span class="info-paginacion">
                            Página {{ paginaActual }} de {{ totalPaginas() }}
                        </span>
                        
                        <button 
                            @click="cambiarPagina(paginaActual + 1)"
                            :disabled="paginaActual === totalPaginas()"
                            class="btn-paginacion"
                        >
                            Siguiente
                        </button>
                    </div>

                    <div class="info-total">
                        Mostrando {{ documentos.length }} de {{ totalDocumentos }} documentos
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

export default {
    name: 'ExpedienteDetalleView',
    setup() {
        const router = useRouter()
        const route = useRoute()

        const expediente = ref({
            numero_expediente: '',
            distrito_judicial: '',
            organo_jurisdiccional: '',
            especialidad: '',
            estado: '',
            parte: '',
            materia: '',
            fecha_inicio: '',
            juez: ''
        })

        const documentos = ref([])
        const cargandoDocumentos = ref(true)
        const errorDocumentos = ref(null)
        
        // Paginación
        const paginaActual = ref(1)
        const documentosPorPagina = 5
        const totalDocumentos = ref(0)

        const volverAtras = () => {
            router.push(`/expediente/${route.params.id}`)
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
            } catch (err) {
                console.error('Error al cargar expediente:', err)
            }
        }

        const cargarDocumentos = async () => {
            try {
                cargandoDocumentos.value = true
                errorDocumentos.value = null
                const expedienteId = route.params.id
                
                // Obtener todos los documentos y filtrar por expediente
                const response = await axios.get('http://127.0.0.1:8000/api/documentos/')
                const todosDocumentos = response.data.filter(doc => doc.expediente === parseInt(expedienteId))
                
                totalDocumentos.value = todosDocumentos.length
                
                // Aplicar paginación
                const inicio = (paginaActual.value - 1) * documentosPorPagina
                const fin = inicio + documentosPorPagina
                documentos.value = todosDocumentos.slice(inicio, fin)
            } catch (err) {
                console.error('Error al cargar documentos:', err)
                errorDocumentos.value = 'Error al cargar los documentos del expediente'
            } finally {
                cargandoDocumentos.value = false
            }
        }

        const cambiarPagina = (nuevaPagina) => {
            paginaActual.value = nuevaPagina
            cargarDocumentos()
        }

        const totalPaginas = () => {
            return Math.ceil(totalDocumentos.value / documentosPorPagina)
        }

        const descargarDocumento = (documento) => {
            if (!documento.archivo_pdf) {
                alert('Este documento no tiene un archivo PDF asociado')
                return
            }

            // Usar la URL directamente del JSON
            const urlDescarga = documento.archivo_pdf

            // Crear un enlace temporal y hacer clic en él para descargar
            const link = document.createElement('a')
            link.href = urlDescarga
            link.download = `documento_${documento.id}.pdf`
            link.target = '_blank'
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
        }

        onMounted(() => {
            cargarExpediente()
            cargarDocumentos()
        })

        return {
            expediente,
            documentos,
            cargandoDocumentos,
            errorDocumentos,
            paginaActual,
            totalDocumentos,
            documentosPorPagina,
            volverAtras,
            formatearFecha,
            descargarDocumento,
            cambiarPagina,
            totalPaginas
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
    border-radius: 6px;
}

.btn-volver {
    background-color: #cfcfcf;
    color: #000;
    border: none;
    padding: 8px 15px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s;
}

.btn-volver:hover {
    background-color: #5a6268;
    color: white;
}

.panel {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 15px 5px;
    overflow: hidden;
}

.titulo {
    background-color: #5a6268;
    padding: 8px 10px;
}

.titulo h2 {
    margin: 0;
    color: white;
    font-size: 25px;
    font-weight: 100;
    font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}

.expediente-item {
    padding: 5px 10px;
    border-bottom: 1px solid #f0f0f0;
    background-color: #f9f9f9;
    font-size: 15px;
    display: flex;
}

.datos {
    padding: 0 10px 0 10px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    font-size: 15px;
}

.dato-item {
    display: flex;
    padding: 5px 0;
    border-bottom: 1px solid #f0f0f0;
}

.dato-item:last-child {
    border-bottom: none;
}

.dato-label {
    flex: 0 0 250px;
    font-weight: 600;
    font-family: sans-serif;
    color: #721c24;
}

.dato-valor {
    flex: 1;
    color: #000000;
    font-family:'Times New Roman', Times, serif;
    font-size: 14px;
}

/* Estilos para la sección de documentos */
.datos-bbdd {
    padding: 20px;
    min-height: 200px;
}

.mensaje-carga,
.mensaje-error,
.mensaje-vacio {
    text-align: center;
    padding: 40px;
    color: #666;
    font-size: 1.1rem;
}

.mensaje-error {
    color: #721c24;
    background-color: #f8d7da;
    border-radius: 6px;
}

.lista-documentos {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.documento-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background-color: #fafafa;
    transition: box-shadow 0.3s;
}

.documento-card:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.documento-info {
    flex: 1;
}

.documento-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.documento-numero {
    font-weight: 700;
    color: #721c24;
    font-size: 1rem;
}

.documento-fecha {
    color: #666;
    font-size: 0.9rem;
}

.documento-detalle p {
    margin: 5px 0;
    color: #333;
    font-size: 0.95rem;
}

.documento-detalle strong {
    color: #721c24;
}

.documento-acciones {
    margin-left: 20px;
}

.btn-descargar {
    background-color: #721c24;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s;
    white-space: nowrap;
}

.btn-descargar:hover {
    background-color: #5a161c;
}

.btn-descargar:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

/* Paginación */
.paginacion {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 25px;
    padding: 15px;
    border-top: 1px solid #ddd;
}

.btn-paginacion {
    background-color: #5a6268;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s;
}

.btn-paginacion:hover:not(:disabled) {
    background-color: #721c24;
}

.btn-paginacion:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.info-paginacion {
    color: #333;
    font-weight: 600;
}

.info-total {
    text-align: center;
    color: #666;
    font-size: 0.9rem;
    margin-top: 10px;
}

/* Responsive */
@media (max-width: 768px) {
    .dato-item {
        flex-direction: column;
        gap: 5px;
    }

    .dato-label {
        flex: none;
    }

    .documento-card {
        flex-direction: column;
        align-items: stretch;
    }

    .documento-acciones {
        margin-left: 0;
        margin-top: 15px;
    }

    .btn-descargar {
        width: 100%;
    }
}
</style>