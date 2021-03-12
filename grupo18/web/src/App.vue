<template>
  <div id="app">
    <div id="nav">
      <router-link id="router-link" to="/">Home</router-link> |
      <router-link id="router-link" to="/mapa-centros">Mapa de centros</router-link> |
      <router-link id="router-link" to="/solicitud-turno">Solicitar Turno</router-link> |
      <router-link id="router-link" to="/sugerencias">Registrar centro</router-link> |
      <router-link id="router-link" to="/estadisticas">Estadísticas</router-link>
    </div>
    <router-view/>
  </div>
  
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'


</script>

<style>
body {
  
  background: #ECE9E6;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #FFFFFF, #ECE9E6);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #FFFFFF, #ECE9E6); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#router-link{
   text-decoration: none;
    background-image: linear-gradient(currentColor, currentColor);
    background-position: 0% 100%;
    background-repeat: no-repeat;
    background-size: 0% 2px;
    transition: background-size .3s;
    color: #2c3e50;
    font-size: 25px;
  
}
#router-link:hover, #router-link:focus{
  background-size: 100% 2px;
}
#nav{
  padding-bottom: 5%;
  font-size: 25px;
}
</style>
