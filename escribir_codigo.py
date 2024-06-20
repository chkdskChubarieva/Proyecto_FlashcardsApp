import zipfile
import os

def escribirJS():
    contenido_javascript = """
    
let currentFlashcardIndex = 0;
let score = 0;  // Puntaje del usuario

document.addEventListener('DOMContentLoaded', function() {
    mostrarFlashcard();
});

function mostrarFlashcard() {
    const flashcard = flashcards1[currentFlashcardIndex];
    document.getElementById("preguntaFlashcard").textContent = flashcard.pregunta;
    document.getElementById("respuestaFlashcard").textContent = flashcard.respuesta;
}

function siguienteFlashcard() {
    vuelta();   
    mostrarFlashcard();
}

function vuelta() {
    const preguntaSection = document.querySelector('.flashcard-principal-pregunta');
    const respuestaSection = document.querySelector('.flashcard-principal-respuesta');

    if (preguntaSection.style.display === 'none') {
        preguntaSection.style.display = 'block';
        respuestaSection.style.display = 'none';
    } else {
        preguntaSection.style.display = 'none';
        respuestaSection.style.display = 'block';
    }
}   

function comparar(){
    
    const respuesta = document.getElementById('evaluacion').value;

    const flashcard = flashcards1[currentFlashcardIndex];
    
    if(respuesta == flashcard.respuesta){
        document.getElementById("respuesta").textContent = "La respuesta es correcta!";
        document.getElementById("respuesta").style.color = "#5E8D74";
        score++; // Aumentar el puntaje
        
    }else{
        document.getElementById("respuesta").textContent = "La respuesta es incorrecta!";
        document.getElementById("respuesta").style.color = "#b64a4a";
    }
    vuelta();
    document.getElementById('evaluacion').value = ''; // Establecer el valor del input a una cadena vacía

    currentFlashcardIndex++;

    if (currentFlashcardIndex == flashcards1.length) {
        var promedio = (score / flashcards1.length) * 100;
        document.getElementById("respuestaFlashcard").textContent = "TERMINO LAS PREGUNTAS SU PROMEDIO ES: "+promedio.toFixed(2);
        const btn_siguiente = document.querySelector('.btn_siguiente');
        btn_siguiente.style.display = 'none';
        scormSet("cmi.core.score.raw", promedio);
        scormSet("cmi.core.lesson_status", "completed");
        scormCommit();
    }
}
"""
    return contenido_javascript



def generar_JS(datos_flashcards):
     with open("index.js", "w") as file:
        file.write(f"const flashcards1 = {datos_flashcards};")
        file.write(escribirJS())
      
def escribir_HTML():
    with open("index.html", "w") as file:
            file.write("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flashcards - FlashcardsApp</title>

    <link rel="stylesheet" href="plantilla.css">
    <link rel="stylesheet" href="tarjeta-flashcard.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap');
        @import url('https://cdn-uicons.flaticon.com/2.3.0/uicons-regular-rounded/css/uicons-regular-rounded.css');
        @import url('https://cdn-uicons.flaticon.com/2.3.0/uicons-solid-rounded/css/uicons-solid-rounded.css');
        @import url('https://cdn-uicons.flaticon.com/2.3.0/uicons-bold-rounded/css/uicons-bold-rounded.css');
    </style>
    <script src="scormFunctions.js"></script>
    <script src="index.js"></script>
</head>

<body>
    <header>
        <div class="logo">
            <i class="fi fi-sr-layers"></i>
            <span>FlashcardsApp</span>
        </div>
    </header>

    <div class="fondo">
        <div class="contenedor-flashcards">
            <!--FLASHCARD LADO RESPUESTA-->
            <section class="flashcard-principal-respuesta">
                <div class="flashcard-encabezado">
                    <span>Respuesta</span>
                    <div class="opciones"></div>
                </div>
                
                <div class="flashcard-barra">
                    <span id="respuesta"></span>
                </div>

                <div class="flashcard-contenido">
                    <span id="respuestaFlashcard">Respuesta aquí</span>
                    <button type="button" class="btn_siguiente" style="display: flex;" onclick="siguienteFlashcard()"><i class="fa-solid fa-arrow-right"></i>Siguiente</button>
                </div>
            </section>

            <!--FLASHCARD LADO PREGUNTA-->
            <section class="flashcard-principal-pregunta">
                <div class="flashcard-encabezado">
                    <span>Pregunta</span>
                    <div class="opciones"></div>
                </div>

                <div class="flashcard-barra">
                    <span id="pregunta">Responde la Flashcard!</span>
                </div>

                <div class="flashcard-contenido">
                    <span id="preguntaFlashcard">Pregunta aquí</span>
                    <form id="form-evaluacion" class="form-evaluacion">
                        <input type="text" name="evaluacion" id="evaluacion" placeholder="Respuesta:">
                        <button type="button" onclick="comparar()"><i class="fa-solid fa-arrow-right"></i></button>
                    </form>
                </div>
            </section>
        </div>
    </div>
    
    <script >
    
    // Inicializar el API SCORM al cargar la página
    window.onload = function() {
        scormInitialize();
    }

    // Terminar la sesión SCORM al cerrar la página
    window.onunload = function() {
        scormTerminate();
    }
    </script>
</body>
</html>
""")      
 
 
def escribir_MANIFEST():
     with open("imsmanifest.xml", "w") as file:
        file.write(
"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.example.scorm12" version="1.2"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2
                              http://www.imsproject.org/xsd/imscp_rootv1p1p2.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2
                              http://www.adlnet.org/xsd/adlcp_rootv1p2.xsd">
    <metadata>
        <schema>ADL SCORM</schema>
        <schemaversion>1.2</schemaversion>
    </metadata>
    <organizations default="defaultOrg">
        <organization identifier="defaultOrg">
            <title>FLASHCARDS EVALUACION</title>
            <item identifier="item_1" identifierref="resource_1">
                <title>FLASHCARDS EVALUACION</title>
            </item>
        </organization>
    </organizations>
    <resources>
        <resource identifier="resource_1" type="webcontent" adlcp:scormtype="sco" href="index.html">
            <file href="index.html"/>
            <file href="scormFunctions.js"/>
            <file href="index.js"/>
            <file href="plantilla.css"/>
            <file href="tarjeta-flashcard.css"/>
        </resource>
    </resources>
</manifest>""")

def escribir_SCORMFUNCTIONS():
     with open("scormFunctions.js", "w") as file:
        file.write("""
var API = null;

function findAPI(win) {
    while ((win.API == null) && (win.parent != null) && (win.parent != win)) {
        win = win.parent;
    }
    return win.API;
}

function scormInitialize() {
    API = findAPI(window);
    if (API == null) {
        console.log("No se pudo encontrar el API SCORM");
        return false;
    }
    return API.LMSInitialize("");
}

function scormTerminate() {
    if (API == null) return;
    return API.LMSFinish("");
}

function scormGet(parameter) {
    if (API == null) return "";
    return API.LMSGetValue(parameter);
}

function scormSet(parameter, value) {
    if (API == null) return "false";
    return API.LMSSetValue(parameter, value);
}

function scormCommit() {
    if (API == null) return "false";
    return API.LMSCommit("");
}
""")



def escribir_CSS_PLANTILLA():
    with open("plantilla.css", "w") as file:
        file.write(
"""* {
    margin: 0px;
    padding: 0px;
    font-family: "Nunito Sans", sans-serif;
    box-sizing: border-box;
}

body {
    display: flex;
    flex-direction: column;
    background-color: #F5F5F5;
}

/*============================INICIO - HEADER============================*/

header {
    display: flex;
    width: 100%;
    height: 60px;
    justify-content: center;
    align-items: center;
    padding: 0px 20px;
    border-bottom: 1px solid rgba(0, 0, 0, .2);
}

header .logo {
    display: flex;
    align-items: center;
    cursor: pointer;
}

header .logo i {
    font-size: 26px;
    color: rgba(55, 67, 85, .9);
    margin-right: 5px;
    margin-top: 8px;
}

header .logo span {
    font-size: 24px;
    font-weight: 900;
    color: rgba(55, 67, 85, .9);
}

/*INICIO - BARRA DE BUSQUEDA (SOLO EN PANEL FLASHCARDS)*/

header .barra-busqueda {
    /*border: 1px solid black;*/
    width: 400px;
    height: 35px;
    border-radius: 10px;
}

header .barra-busqueda form {
    display: flex;
    width: 100%;
    height: 100%;
}

header .barra-busqueda form input {
    width: 360px;
    height: 100%;
    font-size: 16px;
    font-weight: 600;
    color: #363636;
    padding: 0px 10px;
    outline: none;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 10px 0px 0px 10px;
}

header .barra-busqueda form input:focus {
    border: 1px solid rgba(0, 0, 0, 0.4);
}

header .barra-busqueda form button {
    width: 40px;
    height: 100%;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 0px 10px 10px 0px;
    outline: none;
    cursor: pointer;
}

header .barra-busqueda form button i {
    color: rgba(38, 38, 38, 0.8);
    font-size: 16px;

}

header .barra-busqueda form button:hover {
    background-color: #F5F5F5;
}

header .barra-busqueda form button:focus {
    border: 1px solid rgba(0, 0, 0, 0.4);
}

/*FIN - BARRA DE BUSQUEDA (SOLO EN PANEL FLASHCARDS)*/


header .opciones {
    height: 100%;
    display: flex;
    gap: 40px;
    align-items: center
}

header .opciones button {
    display: flex;
    font-size: 20px;
    font-weight: 600;
    align-items: center;
    padding: 5px;
    border: none;
    border-radius: 10px;
    color: rgba(55, 67, 85, .9);
    background-color: transparent;
    cursor: pointer;
    gap: 10px;
}

header .opciones button:hover {
    background-color: rgba(153, 153, 153, 0.1);
    color: #374355;
}

header .opciones button .info-usuario {
    display: flex;
    flex-direction: column;
}

header .opciones button .info-usuario .username {
    font-size: 18px;
    font-weight: bold;
}

header .opciones button .info-usuario .rol {
    font-size: 14px;
    font-weight: lighter;
}

header .opciones .desplegable {
    display: none;
    flex-direction: column;
    position: absolute;
    align-items: center;
    border: 1px solid rgba(0, 0, 0, .2);
    border-radius: 10px;
    padding: 10px;
    background-color: #F5F5F5;
    gap: 10px;
    top: 60px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    opacity: 0;
}

header .opciones .desplegable span[class="titulo-desplegable"] {
    font-size: 16px;
    font-weight: bold;
    color: rgba(55, 67, 85, .9);
    cursor: default;
}

header .opciones .desplegable button {
    display: flex;
    font-size: 18px;
    font-weight: 600;
    padding: 5px 10px;
    align-items: center;
    background-color: rgba(255, 0, 0, 0.6);
    color: #F5F5F5;
    cursor: pointer;
    transition: ease 0.2s;
}

header .opciones .desplegable button:hover {
    background-color: rgba(255, 0, 0, 0.7);
}

#desplegable.show {
    display: flex;
    opacity: 1;
}

/*============================FIN - HEADER============================*/

main {
    display: flex;
    width: 100%;
    height: calc(100vh - 60px);
}

/*============================INICIO - ASIDE============================*/

aside {
    width: 260px;
    height: calc(100vh - 60px);
    border-right: 1px solid rgba(0, 0, 0, .1);
    overflow-y: auto;
}

aside .boton-principal {
    display: flex;
    width: 100%;
    height: 110px;
    justify-content: center;
    align-items: center;
}

aside .boton-principal button {
    font-size: 20px;
    padding: 10px 15px;
    border-radius: 10px;
    border: none;
    background-color: rgba(55, 67, 85, 0.9);
    color: #FFFFFF;
    box-shadow: 0 2px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

aside .boton-principal button:hover {
    background-color: #374355;
}

aside .separador {
    width: 100%;
    margin: 5px 0px;
    border-bottom: 1px solid rgba(0, 0, 0, .1);
}

aside .botones-secundarios {
    display: flex;
    flex-direction: column;
    width: 100%;
    justify-content: center;
}

aside .botones-clases {
    display: flex;
    flex-direction: column;
    width: 100%;
}

aside .botones-secundarios button,
aside .botones-clases button {
    width: 100%;
    display: flex;
    font-size: 16px;
    font-weight: 600;
    border-radius: 0px 20px 20px 0px;
    padding: 10px 15px;
    align-items: center;
    text-align: left;
    background-color: transparent;
    color: rgba(38, 38, 38, 0.9);
    gap: 15px;
    border: none;
}

aside .botones-secundarios i,
aside .botones-clases i {
    margin-top: 5.4px;
}

aside .botones-secundarios button:hover,
aside .botones-clases button:hover {
    background-color: rgba(38, 38, 38, 0.05);
}

/*============================FIN - ASIDE============================*/

/*============================INICIO - PANEL PRINCIPAL============================*/

main section[class="panel-principal"] {
    width: calc(100% - 260px);
    height: calc(100vh - 60px);
}

main section nav {
    display: flex;
    width: 100%;
    height: 50px;
    justify-content: space-between;
    align-items: center;
    padding: 0px 20px;
    border-bottom: 1px solid rgba(0, 0, 0, .1);
}

main section nav .navbar {
    display: flex;
    justify-content: left;
}

main section nav a {
    font-size: 20px;
    font-weight: 600;
    color: #262626;
    text-decoration: none;
    cursor: default;
}

main section nav a:hover {
    text-decoration: underline 2px solid #262626;
}

main section nav p {
    font-size: 20px;
    font-weight: 600;
    color: #262626;
    margin: 0px 8px 0px 8px;
    cursor: default;
}

main section .contenido-principal {
    width: 100%;
    height: calc(100vh - 110px);
}

/*============================FIN - PANEL PRINCIPAL============================*/""")

def escribir_CSS_TARJETA():
    with open("tarjeta-flashcard.css", "w") as file:
        file.write(
"""/*INICIO - FLASHCARD PREGUNTA*/
.fondo {
    position: absolute;
    display: flex;
    width: 100%;
    min-width: 750px;
    height: 100%;
    justify-content: center;
    align-items: center;
    margin: auto;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.3);
    gap: 15px;
    z-index: 1;
}

.contenedor-flashcards {
    width: 750px;
    height: 420px;
}

.flashcard-principal-pregunta {
    width: 750px;
    height: 420px;
    border-radius: 10px;
    position: absolute;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.flashcard-principal-pregunta .flashcard-encabezado {
    display: flex;
    width: 100%;
    height: 60px;
    padding: 0px 20px;
    background-color: #F5F5F5;
    color: #5E8D74;
    box-shadow: 0 0px 2px rgba(0, 0, 0, 0.2);
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
    position: relative;
    z-index: +1;
}

.flashcard-principal-pregunta span {
    font-size: 22px;
    font-weight: bold;
    cursor: default;
}

.flashcard-principal-pregunta .opciones {
    display: flex;
    gap: 12px;
    align-items: center;
}

.flashcard-principal-pregunta .opciones i {
    display: flex;
    width: 40px;
    height: 40px;
    font-size: 26px;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: #5E8D74;
    color: #F5F5F5;
    cursor: pointer;
    transition: 0.1s ease;
}

.flashcard-principal-pregunta .opciones i:active {
    transform: scale(0.9);
}

.flashcard-principal-respuesta .opciones i:active {
    transform: scale(0.9);
}

.flashcard-principal-pregunta .opciones i:hover {
    background-color: rgba(94, 141, 116, 0.9);
}

.contenedor-flashcards .flashcard-barra {
    display: flex;
    width: 100%;
    height: 45px;
    padding: 0px 20px;
    justify-content: space-between;
    align-items: center;
    background-color: #D9D9D9;
}

.contenedor-flashcards .flashcard-barra #pregunta {
    color: #363636;
    font-size: 20px;
    font-weight: bold;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad {
    display: flex;
    align-items: center;
    gap: 5px;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad span {
    font-size: 18px;
    color: #363636;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button {
    width: 80px;
    font-size: 16px;
    font-weight: 600;
    padding: 5px;
    border: none;
    border-radius: 10px;
    color: #FFFFFF;
    cursor: pointer;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button[id="facil"] {
    background-color: #86CAA1;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button[id="medio"] {
    background-color: #E0C975;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button[id="dificil"] {
    background-color: #CA8686;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button[id="facil"]:hover {
    background-color: #6fbd8e;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button[id="medio"]:hover {
    background-color: #dbc160;
    ;
}

.contenedor-flashcards .flashcard-barra .barra-dificultad button[id="dificil"]:hover {
    background-color: #ce7878;
}

.contenedor-flashcards .flashcard-barra .info-tema {
    display: flex;
    gap: 20px;
}

.contenedor-flashcards .flashcard-barra .info-tema span {
    display: flex;
    font-size: 18px;
    color: #363636;
    gap: 5px;
}

.contenedor-flashcards .flashcard-barra .info-tema span p {
    font-weight: 600;
}

.contenedor-flashcards .flashcard-barra .barra-botones {
    display: flex;
    gap: 10px;
}

.contenedor-flashcards .flashcard-barra .barra-botones button {
    display: flex;
    font-size: 16px;
    font-weight: 600;
    padding: 5px 10px;
    align-items: center;
    border-radius: 10px;
    border: none;
    background-color: #5E8D74;
    color: #F5F5F5;
    gap: 5px;
    cursor: pointer;
}

.contenedor-flashcards .flashcard-barra .barra-botones button:hover {
    background-color: rgba(94, 141, 116, 0.9);
}

.flashcard-principal-pregunta .flashcard-contenido {
    display: flex;
    width: 100%;
    height: 315px;
    padding: 25px;
    align-items: center;
    box-sizing: border-box;
    background-color: #5E8D74;
    overflow-y: auto;
}

.flashcard-principal-pregunta .flashcard-contenido span {
    display: flex;
    width: 100%;
    height: auto;
    /*USAR AUTO PARA MAJERAR CORRECTAMENTE EL DESBORDAMIENTO DE TEXTO*/
    justify-content: center;
    font-size: 34px;
    font-weight: bold;
    color: #f5f5f5;
    cursor: default;
}

.flashcard-principal-pregunta .flashcard-contenido button {
    flex-direction: column;
    position: absolute;
    align-items: center;
    font-size: 16px;
    font-weight: 600;
    padding: 10px 20px;
    margin: 10px;
    border-radius: 10px;
    border: none;
    bottom: 0;
    right: 0;
    background-color: #F5F5F5;
    color: #464646;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

.flashcard-principal-pregunta .flashcard-contenido button i {
    font-size: 22px;
}

.flashcard-principal-pregunta .flashcard-contenido .form-evaluacion {
    display: flex;
    width: 530px;
    position: absolute;
    padding: 10px 20px;
    bottom: 0;
    left: 0;
}

.flashcard-principal-pregunta .flashcard-contenido .form-evaluacion input {
    width: 450px;
    font-size: 16px;
    font-weight: 600;
    padding: 10px;
    color: #363636;
    border-radius: 10px;
    border: 1px solid transparent;
    outline: none;
}

.flashcard-principal-pregunta .flashcard-contenido .form-evaluacion button {
    display: flex;
    width: 30px;
    height: 44px;
    justify-content: center;
    align-items: center;
    color: #464646;
}



/*FIN - FLASHCARD PREGUNTA*/

/*INICIO - FLASHCARD RESPUESTA*/

.flashcard-principal-respuesta {
    /*CAMBIAR ESTE VALOR A NONE/BLOCK PARA OCULTAR/MOSTRAR LA FLASHCARD*/
    width: 750px;
    height: 420px;
    border-radius: 10px;
    position: absolute;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.flashcard-principal-respuesta .flashcard-encabezado {
    display: flex;
    width: 100%;
    height: 60px;
    padding: 0px 20px;
    background-color: #5E8D74;
    color: #F5F5F5;
    box-shadow: 0 0px 2px rgba(0, 0, 0, 0.2);
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
    position: relative;
    z-index: +1;
}

.flashcard-principal-respuesta span {
    font-size: 22px;
    font-weight: bold;
    cursor: default;
}

.flashcard-principal-respuesta .opciones {
    display: flex;
    gap: 12px;
    align-items: center;
}

.flashcard-principal-respuesta .opciones i {
    display: flex;
    width: 40px;
    height: 40px;
    font-size: 26px;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: #F5F5F5;
    color: #5E8D74;
    cursor: pointer;
    transition: 0.1s ease;
}

.flashcard-principal-respuesta .opciones i:hover {
    background-color: rgba(245, 245, 245, 0.9);
}

.flashcard-principal-respuesta .flashcard-contenido {
    display: flex;
    width: 100%;
    height: 315px;
    padding: 25px;
    align-items: center;
    box-sizing: border-box;
    background-color: #F5F5F5;
    overflow-y: auto;
}

.flashcard-principal-respuesta .flashcard-contenido span {
    display: flex;
    width: 100%;
    height: auto;
    /*USAR AUTO PARA MAJERAR CORRECTAMENTE EL DESBORDAMIENTO DE TEXTO*/
    justify-content: center;
    font-size: 34px;
    font-weight: bold;
    color: #5E8D74;
    cursor: default;
}

.flashcard-principal-respuesta .flashcard-contenido button {
    display: flex;
    flex-direction: column;
    position: absolute;
    align-items: center;
    font-size: 16px;
    font-weight: 600;
    padding: 10px 20px;
    margin: 10px;
    border-radius: 10px;
    border: none;
    bottom: 0;
    right: 0;
    background-color: #5E8D74;
    color: #F5F5F5;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

.flashcard-principal-respuesta .flashcard-contenido button i {
    font-size: 22px;
}

/*FIN - FLASHCARD RESPUESTA*/

/*INICIO - FLASHCARD OPCIONES LATERALES*/

.flashcard-opciones-laterales {
    display: flex;
    flex-direction: column;
    width: 250px;
    height: 420px;
    border-radius: 10px;
    background-color: #D9D9D9;
    padding: 10px;
    flex-shrink: 0;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.flashcard-opciones-laterales span {
    font-size: 18px;
    font-weight: bold;
    color: #363636;
    cursor: default;
}

.flashcard-opciones-laterales .estrellas {
    display: flex;
    width: 100%;
    height: 40px;
    margin: 5px 0px 10px 0px;
    padding: 0px 20px;
    border-radius: 10px;
    background-color: #F5F5F5;
    justify-content: center;
    align-items: center;
}

.flashcard-opciones-laterales .estrellas i {
    display: flex;
    width: 35px;
    justify-content: center;
    font-size: 24px;
    color: #D9D9D9;
    cursor: default;
}

.flashcard-opciones-laterales .cuadro-dificultad {
    display: flex;
    width: 50%;
    height: 39px;
    margin: 5px 0px 10px 0px;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
    cursor: default;
}

.flashcard-opciones-laterales .comentario-docente {
    width: 100%;
    height: 130px;
    padding: 10px;
    margin: 5px 0px 10px 0px;
    border-radius: 10px;
    background-color: #F5F5F5;
    color: #464646;
    overflow-y: auto;
    scrollbar-width: thin;
}

.flashcard-opciones-laterales .cuadro-estado {
    display: flex;
    width: 50%;
    height: 35px;
    margin: 5px 0px 10px 0px;
    border-radius: 10px;
    justify-content: center;
    align-items: center;
    background-color: #F5F5F5;
    gap: 5px;
    cursor: default;""")

            
def generar_archivos(datos_flashcards):
    generar_JS(datos_flashcards)
    escribir_HTML()
    escribir_MANIFEST()
    escribir_SCORMFUNCTIONS()
    escribir_CSS_PLANTILLA()
    escribir_CSS_TARJETA()
    
    archivos_a_comprimir = [
    'imsmanifest.xml',
    'index.html',
    'index.js',
    'plantilla.css',
    'scormFunctions.js',
    'tarjeta-flashcard.css'
    ]

    comprimir_archivos(archivos_a_comprimir, 'PAQUETE_SCORM_FLASHCARDS.zip')
    return 'PAQUETE_SCORM_FLASHCARDS.zip'
    


def comprimir_archivos(archivos, archivo_zip):
    with zipfile.ZipFile(archivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for archivo in archivos:
            zipf.write(archivo)