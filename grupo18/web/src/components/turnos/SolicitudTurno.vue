<template>
  <div class="pb-5">
    <h1 class="mb-5">Solicitud de turnos</h1>
    <form
      @submit.prevent="checkForm"
      class="w-50 m-auto border border-dark p-5 shadow bg-white rounded"
    >
      <div>
        <p v-if="errors.length" class="alert alert-danger">
          <b class="alert-heading">Por favor, corrija el(los) siguiente(s) error(es):</b>
          <ul>
            <li class="d-flex m-2" v-for="error in errors" v-bind:key="error">{{ error }}</li>
          </ul>
        </p>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="email">Email(*)</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            v-model="reserva.email_donante"
            type="email"
            placeholder="email"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="nombre">Nombre(*)</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            v-model="reserva.nombre"
            type="text"
            placeholder="nombre"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="apellido"
          >Apellido(*)</label
        >
        <div class="col-sm-10">
          <input
            class="form-control"
            v-model="reserva.apellido"
            type="text"
            placeholder="apellido"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="telefono"
          >Telefono(*)</label
        >
        <div class="col-sm-10">
          <input
            class="form-control"
            v-model="reserva.telefono_donante"
            type="text"
            placeholder="Telefono"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="fecha"
          >Fecha del turno(*)</label
        >
        <div class="col-sm-10">
          <input
            v-on:change="turnosEnFecha"
            class="form-control"
            v-model="reserva.fecha"
            type="date"
            placeholder="Fecha"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="centros">Centros(*)</label>
        <div class="col-sm-10">
          <select
            type="time"
            class="form-control"
            v-on:change="turnosCentro"
            ref="seleccionado"
            v-model="reserva.centro_id"
          >
            <option
              v-for="(centro, key) in centros"
              v-bind:key="key"
              :value="key"
            >
              {{ centro.nombre }}
            </option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label" for="turnos">Turnos(*)</label>
        <div class="col-sm-10">
          <select class="form-control" v-model="reserva.hora_inicio">
            <option
              v-for="(turno, keyt) in turnos"
              v-bind:key="keyt"
              :value="keyt"
            >
              {{ turno.hora_inicio }}
            </option>
          </select>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Enviar solicitud</button>
    </form>
  </div>
</template> 

<script>
import axios from "axios";

let regexNum = /^[0-9]*$/;
let regexName = /^[a-zA-Z]*$/;
let regexEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z-]+\.[a-zA-Z]{2,3}$/;

export default {
  data() {
    return {
      values: {},
      msgAceptar: () => alert("Se ha reservado su turno"),
      centros: [],
      turnos: [],
      errors: [],
      reserva: {
        centro_id: "",
        nombre: "",
        apellido: "",
        email_donante: "",
        telefono_donante: "",
        hora_inicio: "",
        hora_fin: "",
        fecha: "",
      },
    };
  },
  created() {
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
  },
  methods: {
    turnosCentro() {
      // alert(this.$refs.seleccionado.value)
      let seleccionado = this.$refs.seleccionado.value;
      let centro = this.centros[seleccionado];

      if (this.reserva.fecha === undefined) {
        axios
          .get(
            // "http://localhost:5000/api/centros/" +
            //   centro.id +
            //   "/turnos_disponibles"
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/" +
              centro.id +
              "/turnos_disponibles"
          )
          .then((response) => {
            console.log(response.data);
            this.turnos = response.data.turnos;
          });
      } else {
        axios
          .get(
            // "http://localhost:5000/api/centros/" +
            //   centro.id +
            //   "/turnos_disponibles?fecha=" +
            //   this.reserva.fecha
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/" +
              centro.id +
              "/turnos_disponibles?fecha=" +
              this.reserva.fecha
          )
          .then((response) => {
            console.log(response.data);
            this.turnos = response.data.turnos;
          });
      }
    },
    turnosEnFecha() {
      let seleccionado = this.$refs.seleccionado.value;
      let centro = this.centros[seleccionado];

      if (centro === undefined) {
        alert("Por favor, seleccione un centro de ayuda");
      } else {
        axios
          .get(
            // "http://localhost:5000/api/centros/" +
            //   centro.id +
            //   "/turnos_disponibles?fecha=" +
            //   this.reserva.fecha
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/" +
              centro.id +
              "/turnos_disponibles?fecha=" +
              this.reserva.fecha
          )
          .then((response) => {
            console.log(response.data);
            this.turnos = response.data.turnos;
          });
      }
    },
    crearJsonReserva() {
      let id_centro;
      if (this.centros[this.reserva.centro_id] === undefined) {
        id_centro = 0;
      } else {
        id_centro = this.centros[this.reserva.centro_id].id;
      } //Para obtener el id del centro seleccionado

      if (this.turnos.length === 0) {
        alert(
          "Lo siento, verifica que los campos marcados con asteriscos estén completos e intenta de nuevo"
        );
      } else {
        axios
          .post(
            // "http://localhost:5000/api/centros/" + id_centro + "/reserva",
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros/" +
              id_centro +
              "/reserva",
            {
              nombre: this.reserva.nombre,
              apellido: this.reserva.apellido,
              email_donante: this.reserva.email_donante,
              telefono_donante: this.reserva.telefono_donante,
              hora_inicio: this.turnos[this.reserva.hora_inicio].hora_inicio, //Si no hay turnos cargados tira un error por consola. Se puede corregir preguntando si this.turnos es undefined
              hora_fin: this.turnos[this.reserva.hora_inicio].hora_fin,
              fecha: this.reserva.fecha,
            }
          )
          .then((response) => {
            console.log(response);
            location.reload();
            alert("La reserva se creo de manera exitosa!", "success");
            this.$router.replace("/turnos");
          })
          .catch((error) => {
            alert(
              "Lo siento, verifica que los campos marcados con asteriscos estén completos e intenta de nuevo"
            );
            console.log(error);
          });
      }
    },
    checkForm: function (e) {
      this.errors = [];

      if (!this.reserva.centro_id) {
        this.errors.push("- El centro es obligatorio");
      }

      if (!this.reserva.nombre) {
        this.errors.push("- El nombre es obligatorio");
      }

      if (regexName.test(this.reserva.nombre) == false) {
        this.errors.push("- Hay caracteres inválidos en nombre");
      }

      if (!this.reserva.apellido) {
        this.errors.push("- El apellido es obligatorio");
      }

      if (regexName.test(this.reserva.apellido) == false) {
        this.errors.push("- Hay caracteres inválidos en apellido");
      }

      if (!this.reserva.email_donante) {
        this.errors.push("- El email es obligatorio");
      }

      if (regexEmail.test(this.reserva.email_donante) == false) {
        this.errors.push("- El email no es correcto");
      }

      if (!this.reserva.telefono_donante) {
        this.errors.push("- El telefono es obligatoria");
      }

      if (regexNum.test(this.reserva.telefono_donante) == false) {
        this.errors.push("- Hay caracteres inválidos en teléfono");
      }

      if (!this.reserva.hora_inicio) {
        this.errors.push("- La hora del turno es obligatoria");
      }

      if (!this.reserva.fecha) {
        this.errors.push("- La fecha es obligatoria");
      }
      alert(
        "Lo siento, verifica que los campos marcados con asteriscos estén completos e intenta de nuevo"
      );
      e.preventDefault();
    },
  },
};
</script>


