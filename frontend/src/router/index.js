import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Expediente from '@/views/Expediente.vue'
import ExpedienteDetalle from '@/views/ExpedienteDetalle.vue'
import SubirDocumentos from '@/views/SubirDocumentos.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/expediente/:id', name: 'expediente', component: Expediente, props: true },
    { path: '/expediente/:id/detalle', name: 'expediente-detalle', component: ExpedienteDetalle, props: true },
    { path: '/subir-documento', name: 'subir-documento', component: SubirDocumentos },
  ],
})

export default router
