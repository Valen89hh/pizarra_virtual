const microfono = document.getElementById('startButton');

addEventListener("load", ()=>{
    let reconociendo = false;

    // Verificar si la API de reconocimiento de voz es compatible con el navegador
  if ('webkitSpeechRecognition' in window) {
    console.log("Hola")
    const socket = io();  // Cambia la URL si el servidor se ejecuta en otro lugar

    socket.on('connect', function(){
        console.log("Conectado")

        // Codigo para hacer cuano nos conectemos
        socket.on('event', function(res){
            console.log(res)
        })

        socket.on("activate_voz", function(res){
            console.log("DETECCCION: ", res)
            reconocerVoz()
        })
    })


    socket.on('disconnect', function(){
        console.log("Desconectado")
    })


    // Crear una instancia de la API de reconocimiento de voz
    const recognition = new webkitSpeechRecognition();
  
    // Configurar el reconocimiento de voz
    recognition.lang = 'es'; // Establecer el idioma de reconocimiento
    recognition.continuous = false; // No reconocimiento continuo
  
    // Escuchar el evento de resultado de reconocimiento de voz
    recognition.onresult = function(event) {
      reconociendo = false; 
      microfono.style.animation = "none";
      const transcript = event.results[0][0].transcript; // Obtener el texto reconocido
      console.log('Texto reconocido:', transcript);
      txtReconocido.value = transcript;
      enviarVoz(transcript)
    }
  
    // Iniciar el reconocimiento de voz cuando se presiona un botón, por ejemplo
    microfono.addEventListener('click', reconocerVoz);

    function enviarVoz(texto){
        socket.emit('reconocido', texto)
    }

    function reconocerVoz(){
        if(!reconociendo){
            msgSuccess.style.display = "none";
            msgError.style.display = "none";
            txtReconocido.value = "Reconociendo...";
            microfono.style.animation = "scaleAnimation 2s infinite";
            recognition.start();
            reconociendo = true;
        }
        else{
            console.log("Ya se esta reconociendo la voz")
        }
    }
    
  }else{
    alert("Lo siento, tu navegador no soporta el reconocimiento de voz")
  }

})

