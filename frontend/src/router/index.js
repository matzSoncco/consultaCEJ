import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Expediente from '@/views/Expediente.vue'
import ExpedienteDetalle from '@/views/ExpedienteDetalle.vue'
import SubirDocumento from '@/views/SubirDocumento.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/expediente', name: 'expediente', component: Expediente },
  { path: '/expediente/:id', name: 'expediente-detalle', component: ExpedienteDetalle, props: true },
  { path: '/subir-documento', name: 'subir-documento', component: SubirDocumento },
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [],
})

export default router
