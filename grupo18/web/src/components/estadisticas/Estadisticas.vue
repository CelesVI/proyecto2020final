<template>
  <div class="estadisticas">
    <h1>Estadisticas</h1>
    <div>
      <b
        ><h5 class="mt-5">
          Cantidad de turnos en el año - Todos los centros
        </h5></b
      >
      <div class="m-5">
        <column-chart
          :data="alAnioData"
          width="95%"
          style="margin: auto"
        ></column-chart>
      </div>
    </div>
    <div>
      <b><h5 class="mt-5">Cantidad de turnos en el año - Por centro</h5></b>
      <select
        class="form-control form-control-sm w-25 m-auto"
        name="centro_id"
        v-on:change="turnosPorCentro"
        ref="seleccionado"
        v-model="centro_id"
      >
        <option v-for="centro in centros" :key="centro.id" :value="centro.id">
          {{ centro.nombre }}
        </option>
      </select>
      <div class="m-5">
        <column-chart
          :data="alAnioPorCentro"
          width="95%"
          style="margin: auto"
        ></column-chart>
      </div>
    </div>
    <div>
      <b><h5 class="mt-5">Cantidad de centros por municipio</h5></b>

      <select
        class="form-control form-control-sm w-25 m-auto"
        name="municipio_id"
        v-on:change="cambioMunicipio"
        ref="seleccionado"
        v-model="municipio_id"
      >
        <option
          v-for="municipio in municipios"
          :key="municipio.id"
          :value="municipio.id"
        >
          {{ municipio.name }}
        </option>
      </select>
      <div class="m-5">
        <pie-chart
          :data="chartData"
          width="400px"
          style="margin: auto"
        ></pie-chart>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Estadisticas",
  data() {
    return {
      turnosOcupados: [],
      alAnioPorCentro: [],
      centro_id: 0,
      municipio_id: 0,
      centros: [],
      alAnioData: [],
      chartData: [],
      municipios: [],
      meses: [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
      ],
    };
  },
  created() {
    axios
      .get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135"
      )
      .then((response) => {
        this.municipios = response.data.data.Town;
      });

    axios
      .get(
        "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/all"
      )
      .then((response) => {
        this.centros = response.data.centros;
      })
      .catch((e) => {
        console.error(e);
      });
    this.turnosPorCentro();
    this.turnosTotales();
    // this.cambioMunicipio();
  },
  methods: {
    cambioMunicipio() {
      let muni = this.municipios[this.municipio_id];
      if (muni !== "undefined") {
        axios
          .get(
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/all"
          )
          .then((response) => {
            this.centros = response.data.centros;
            const cent = this.centros.filter(
              (c) => c.municipalidad === muni.name
            );
            this.chartData = [
              ["Centros totales", this.centros.length],
              ["Centros " + muni.name, cent.length],
            ];
          });
      }
    },
    turnosTotales() {
      axios
        .get(
          "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/turnos_ocupados"
        )
        .then((response) => {
          this.turnosOcupados = response.data.turnos;
          for (let i = 0; i < 12; i++) {
            this.alAnioData.push([
              this.meses[i],
              this.turnosOcupados.filter((t) => t.mes === i + 1).length,
            ]);
          }
        });
    },
    turnosPorCentro() {
      if (this.centros.filter((c) => c.id === this.centro_id) !== 0) {
        axios
          .get(
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/" +
              this.centro_id +
              "/turnos_ocupados"
          )
          .then((response) => {
            this.turnosOcupadosCentro = response.data.turnos;
            console.log(this.turnosOcupadosCentro);
            for (let i = 0; i < 12; i++) {
              this.alAnioPorCentro.push([
                this.meses[i],
                this.turnosOcupadosCentro.filter((t) => t.mes === i + 1).length,
              ]);
            }
          });
      }
    },
  },
};
</script>