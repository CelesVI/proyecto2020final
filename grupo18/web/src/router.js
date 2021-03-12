import Vue from 'vue'
import Router from 'vue-router'
import Home from './components/home/Home.vue'
import MapaCentros from './components/maps/MapaCentros.vue'
import Sugerencias from './components/sugerencias/Sugerencias.vue'
import SolicitudTurno from './components/turnos/SolicitudTurno.vue'
import Estadisticas from './components/estadisticas/Estadisticas.vue'

Vue.use(Router)

const routes = [{
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/mapa-centros',
        name: 'mapaCentros',
        component: MapaCentros
    },
    {
        path: '/solicitud-turno',
        name: 'turnos',
        component: SolicitudTurno
    },
    {
        path: '/sugerencias',
        name: 'sugerencias',
        component: Sugerencias
    },
    {
        path: '/estadisticas',
        name: 'estadisticas',
        component: Estadisticas
    }

]

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router