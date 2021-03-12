<template>
    <div>
        <h1>Donaciones COVID-19</h1>
        <p>
            ¡Bienvenidos!<br>
            Este sitio tiene como finalidad poder brindar información de los centros de donaciones
            de la provincia de Buenos Aires.<br>
            Podrás visualizar los centros más cercanos a tu domicilio, sacar
            turno para llevar tu donación, registrar tu propio centro de donaciones
            y ver las estadisticas de cada centro.
        </p>
        <div>
            <div id="container">
                <div>
                    <h3>Mapa de centros de donación</h3>
                    <img src="../../assets/mapa.png">
                    <p>
                        Encontrá el centro más cercano
                        a tu domicilio
                    </p>
                </div>
                <div>
                    <h3>Reservar turno</h3>
                    <img src="../../assets/turno.png">
                    <p>
                        Reservá un turno en el centro más cercano <br> 
                        a tu domicilio para cuidarnos entre todos
                    </p>
                </div>
                <div>
                    <h3>Registrar centro</h3>
                    <img src="../../assets/register.png">
                    <p>
                        ¿Querés registrar tu centro?<br>
                        Completá el formulario
                    </p>
                </div>
                <div>
                    <h3>Estadísticas</h3>
                    <img src="../../assets/estadisticas.png">
                    <p>
                        Mirá las estadísticas de los centros
                    </p>
                </div>    
            </div>
        </div>
    </div>
</template>
<script>
export default {
    
}
</script>
<style scoped>
    #container{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
    }
    #container > div{
        margin: 20px;
        padding: 20px;
        height: 200px;
    }
    img{
        width: 75px;
        height: 75px;
    }
</style>