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
                        <span class="dato-label">Juez:</span>
                        <span class="dato-valor">RAMOS CHAHUARES KELLY YESENIA</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Fecha de Inicio:</span>
                        <span class="dato-valor">02/09/2021</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Observación:</span>
                        <span class="dato-valor">NINGUNA</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Materia(s):</span>
                        <span class="dato-valor">ACCION COTENCIOSA ADMINISTRATIVA</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Etapa Procesal:</span>
                        <span class="dato-valor">GENERAL</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Ubicación:</span>
                        <span class="dato-valor">POOL ASIST. JUDICIAL</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Sumilla:</span>
                        <span class="dato-valor">DEMANDA COTENCIOSA ADMINISTRATIVA</span>
                    </div>
                </div>
                <div class="derecha">
                    <div class="dato-item">
                        <span class="dato-label">Distrito Judicial:</span>
                        <span class="dato-valor">{{ expediente.distrito_judicial || '-------' }}</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Especialista Legal:</span>
                        <span class="dato-valor">OBANDO MAMANI MELISSA ARIAN</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Proceso:</span>
                        <span class="dato-valor">Urgente</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Especialidad:</span>
                        <span class="dato-valor">LABORAL</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Sumilla:</span>
                        <span class="dato-valor">DEMANDA COTENCIOSA ADMINISTRATIVA</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Fecha Conclusión:</span>
                        <span class="dato-valor">{{ expediente.especialidad || '------' }}</span>
                    </div>
                    <div class="dato-item">
                        <span class="dato-label">Motivo Conclusión:</span>
                        <span class="dato-valor">{{ expediente.estado || '------' }}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel">
            <div class="titulo">
                <h2>Partes Procesales</h2>
            </div>
            <table>
                <thead class="tabla-partes">
                    <tr>
                    <th>Parte</th>
                    <th>Tipo de Persona</th>
                    <th>Apellido Paterno/Razón Social</th>
                    <th>Apellido Materno</th>
                    <th>Nombres</th>
                    </tr>
                </thead>
                <tbody class="tabla-partes-body">
                    <tr>
                    <td>DEMANDANTE</td>
                    <td>NATURAL</td>
                    <td>BUSTINZA</td>
                    <td>CARCASI</td>
                    <td>ISMAEL ALEJANDRO</td>
                    </tr>
                    <tr>
                    <td>DEMANDADO</td>
                    <td>JURÍDICA</td>
                    <td>PROCURADOR PUBLICO DEL GOBIERNO REGIONAL DE PUNO</td>
                    </tr>
                    <tr>
                    <td>DEMANDADO</td>
                    <td>JURÍDICA</td>
                    <td>RED DE SALUD EL COLLAO ILAVE</td>
                    </tr>
                    <tr>
                    
                    </tr>
                    <tr>
                    
                    </tr>
                </tbody>
            </table>
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

/* Estilos para la tabla de Partes Procesales */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0;
}

.tabla-partes th {
    color: #721c24;
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    font-size: 0.95rem;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
}

.tabla-partes th:last-child {
    border-right: none;
}

.tabla-partes-body tr {
    border-bottom: 1px solid #ddd;
}

.tabla-partes-body tr:last-child {
    border-bottom: none;
}

.tabla-partes-body td {
    padding: 12px 15px;
    color: #000000;
    font-size: 0.9rem;
    vertical-align: top;
}

.tabla-partes-body tr:nth-child(odd) {
    background-color: #f9f9f9;
}

.tabla-partes-body tr:hover {
    background-color: #f0f0f0;
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
    font-family: sans-serif;
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
    flex-wrap: nowrap;
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