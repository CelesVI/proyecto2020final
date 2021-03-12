<template>
  <div class="sugerencias pb-5">
    <h1 class="mb-5">Sugerir un centro</h1>
    <form
      @submit.prevent="checkForm"
      class="w-50 m-auto border border-dark p-5"
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
        <label class="col-sm-2 col-form-label">Nombre(*):</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="nombre"
            placeholder="Nombre"
            v-model="form.nombre"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Direccion(*):</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="direccion"
            placeholder="Direccion"
            v-model="form.direccion"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Telefono(*):</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="telefono"
            placeholder="Telefono"
            v-model="form.telefono"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Hora de apertura(*):</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="hora_de_apertura"
            type="time"
            v-model="form.hora_de_apertura"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Hora de cierre(*):</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="hora_de_cierre"
            type="time"
            v-model="form.hora_de_cierre"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Tipo(*):</label>
        <div class="col-sm-10">
          <select
            class="form-control"
            name="tipo_centro_id"
            v-model="form.tipo_centro_id"
          >
            <option value="1">Comida</option>
            <option value="2">Ropa</option>
            <option value="3">Abrigos</option>
            <option value="4">Merendero</option>
            <option value="5">Variado</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Municipio(*):</label>
        <div class="col-sm-10">
          <select
            class="form-control"
            name="municipio_id"
            v-model="form.municipio_id"
          >
            <option
              v-for="municipio in municipios"
              :key="municipio.id"
              :value="municipio.id"
            >
              {{ municipio.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Web:</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="web"
            placeholder="Web"
            v-model="form.web"
          />
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-sm-2 col-form-label">Email:</label>
        <div class="col-sm-10">
          <input
            class="form-control"
            name="email"
            placeholder="Email"
            v-model="form.email"
          />
        </div>
      </div>
      <div>
        <label class="col-sm-3 col-form-label">Ubicacion:</label>
        <div v-if="form.latitud">
          <p style="color: green">
            El marcador se coloca en: {{ form.latitud }}, {{ form.longitud }}
          </p>
        </div>

        <div style="height: 400px; width: 100%">
          <l-map
            class="border border-dark"
            style="height: 80%; width: 100%; margin: auto"
            :zoom="zoom"
            :center="center"
            @update:zoom="zoomUpdated"
            @update:center="centerUpdated"
            @click="addMarker"
          >
            <l-tile-layer :url="url"></l-tile-layer>
            <l-marker
              v-for="(point, index) in points"
              :lat-lng="point"
              v-bind:key="index"
              @click="removeMarker()"
            />
          </l-map>
        </div>
        <input
          type="hidden"
          id="latitud"
          name="latitud"
          v-model="form.latitud"
        />
        <input
          type="hidden"
          id="longitud"
          name="longitud"
          v-model="form.longitud"
        />
      </div>
      <div class="mb-3">
        <vue-recaptcha
          ref="recaptcha"
          :sitekey="sitekey"
          @verify="onVerify"
        ></vue-recaptcha>
      </div>
      <div>
        <button type="submit" class="btn btn-primary m-1">Guardar</button>
        <button type="reset" class="btn btn-danger m-1">Limpiar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import VueRecaptcha from "vue-recaptcha";
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";

let regexNum = /^[0-9]*$/;
/*let regexName = /^[a-zA-Z]*$/;
let regexEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z-]+\.[a-zA-Z]{2,3}$/;*/

export default {
  name: "Sugerencias",

  data() {
    return {
      zoom: 13,
      center: latLng(-34.920457, -57.953536),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      recaptcha: false,
      sitekey: "6LcsNgEaAAAAAMKXYANWommFHsxEPrZCtugAJ94I",
      errors: [],
      municipios: [],
      points: [],
      form: {
        nombre: null,
        direccion: null,
        telefono: null,
        hora_de_apertura: null,
        hora_de_cierre: null,
        tipo_centro_id: null,
        municipio_id: null,
        web: "",
        email: "",
        latitud: "",
        longitud: "",
      },
    };
  },
  components: {
    "vue-recaptcha": VueRecaptcha,
    LMap,
    LTileLayer,
    LMarker,
  },
  created() {
    fetch("https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios")
      .then((response) => response.json())
      .then((json) => {
        this.municipios = json.data.Town;
      });
  },
  methods: {
    onPost() {
      if (this.recaptcha) {
        axios
          .post(
            // "http://localhost:5000/api/centros",
            "https://admin-grupo18.proyecto2020.linti.unlp.edu.ar/api/centros",
            {
              nombre: this.form["nombre"],
              direccion: this.form["direccion"],
              telefono: this.form["telefono"],
              hora_de_apertura: this.form["hora_de_apertura"],
              hora_de_cierre: this.form["hora_de_cierre"],
              tipo_centro_id: this.form["tipo_centro_id"],
              municipio_id: this.form["municipio_id"],
              web: this.form["web"],
              email: this.form["email"],
              latitud: this.form["latitud"],
              longitud: this.form["longitud"],
            }
          )
          .then((response) => {
            if (response.status === 201) {
              console.info(response.data);
              location.reload();
              alert("Centro sugerido exitosamente");
              this.$router.push("/centros");
            } else {
              alert(
                "Lo siento, verifica que los campos marcados con asteriscos estén completos e intenta de nuevo"
              );
            }
          })
          .catch((error) => {
            this.checkForm;
            alert(
              "Lo siento, verifica que los campos marcados con asteriscos estén completos e intenta de nuevo"
            );
            console.error(error);
          });
      } else {
        alert("Debe completar el reCAPTCHA");
      }
    },
    checkForm: function (e) {
      
      this.errors = [];

      if (!this.form.nombre) {
        this.errors.push("- El nombre es obligatorio");
      }

      if (!this.form.direccion) {
        this.errors.push("- La direccion es obligatoria");
      }

      if (!this.form.telefono) {
        this.errors.push("- El telefono es obligatorio");
      }

      if (!regexNum.test(this.form.telefono)) {
        this.errors.push("- Hay caracteres inválidos en teléfono");
      }

      if (!this.form.hora_de_apertura) {
        this.errors.push("- La hora de apertura es obligatoria");
      }

      if (!this.form.hora_de_cierre) {
        this.errors.push("- La hora de cierre es obligatoria");
      }

      if (!this.form.tipo_centro_id) {
        this.errors.push("- El tipo de centro es obligatorio");
      }

      if (!this.form.municipio_id) {
        this.errors.push("- El municipio es obligatorio");
      }

      /*En caso que necesitemos del email. Habilitar regex del email*/
      /*if (!regexEmail.test(this.form.email)) {
        this.errors.push("- El email no es correcto");
      }*/

      if (!this.recaptcha) {
        alert("Debe completar el reCAPTCHA");
      }
      alert(
        "Lo siento, verifica que los campos marcados con asteriscos estén completos e intenta de nuevo"
      );
      e.preventDefault();

      if (
        this.form.nombre &&
        this.form.direccion &&
        this.form.telefono &&
        this.form.hora_de_apertura &&
        this.form.hora_de_cierre &&
        this.form.tipo_centro_id &&
        this.form.municipio_id
      ) {
        this.onPost();
        return true;
      }
    },
    removeMarker() {
      this.points.splice(0, 1);
      this.form.latitud = "";
      this.form.longitud = "";
    },
    addMarker(point) {
      this.removeMarker();
      this.points.push(point.latlng);
      this.form.latitud = point.latlng.lat;
      this.form.longitud = point.latlng.lng;
    },
    onVerify: function (response) {
      if (response) this.recaptcha = true;
    },
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    centerUpdated(center) {
      this.center = center;
    },
  },
};
</script>