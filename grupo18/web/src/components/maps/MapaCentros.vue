<template>
    <div style="height: 550px"> 
        <h1>Centros de ayuda - Mapa</h1>
        <l-map
            class="border border-dark"
            style="height: 85%; width: 95%; margin: auto"
            :zoom="zoom"
            :center="center"
            @update:zoom="zoomUpdated"
            @update:center="centerUpdated"
        >
        <!-- l-map es el componente principal para los mapas
        todo lo que se quiera agregar ya sea una capa, un marcador, figuras y demas
        va adentro de l-map como el l-tile-layer -->
            <l-tile-layer :url="url"></l-tile-layer>
            <l-marker v-for="centro in centros" :lat-lng="[centro.latitud, centro.longitud]" v-bind:key="centro.id">
                <l-popup> 
                    <h2>{{ centro.nombre }}</h2>
                    <p>Direccion: {{ centro.direccion }}</p>
                    <p>Horario: {{ centro.hora_apertura }} - {{ centro.hora_cierre }} </p>
                    <p v-if="centro.telefono != ''">Telefono: {{ centro.telefono }}</p>
                    <p v-else>Telefono: - </p>
                </l-popup>
            </l-marker>
        </l-map>
    </div>
</template>

<script>
import axios from 'axios'
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data () {
      return  {
          url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          zoom: 14,
          center: [-34.9187, -57.956],
          centros: []
      }      
  },
    created () {
      axios.get('https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/all')
        .then(response => {
            this.centros = response.data.centros;
        })
        .catch(e => {
            this.errors.push(e)
        })
  },
  methods: {
      zoomUpdated (zoom) {
          this.zoom = zoom
      },
      centerUpdated (center) {
          //center devuelve un objeto con las claves latitud y longitud
          //con hacer this.center = center alcanza
          this.center = center
      }
  },
  datos: {
      errors: []
  },
};
</script>
