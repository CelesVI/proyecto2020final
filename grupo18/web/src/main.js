import Vue from 'vue'
import App from './App.vue'
import { Icon } from 'leaflet'
import 'leaflet/dist/leaflet.css'
import router from './router'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

import './assets/formulate.css'
import VueFormulate from '@braid/vue-formulate'
Vue.use(VueFormulate)
Vue.use(Chartkick.use(Chart))

Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')

delete Icon.Default.prototype._getIconUrl
Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})