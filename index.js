const flashcards1 = [
    {
        "ID_flashcard": 20,
        "pregunta": "Verbo to be",
        "respuesta": "Respuesta",
        "dificultad": "medio"
    },
    {
        "ID_flashcard": 25,
        "pregunta": "Pronombres",
        "respuesta": "Resp Pronombre",
        "dificultad": "medio"
    },
    {
        "ID_flashcard": 28,
        "pregunta": "Nuevo pronombre",
        "respuesta": "Nueva respuesta",
        "dificultad": "medio"
    }
];
    
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
