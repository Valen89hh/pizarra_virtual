# Importamos la librerias necesarias
import pyttsx3
import subprocess
import re
import webbrowser

# Clase para procesar los comando de voz
class ComandosVoz():

    # iniciamos las propiedadaes para la deteccion de la voz
    def __init__(self, avatar="Alexa", lenguaje='es'):
        # Motor de sintezi de vos
        self.engine = pyttsx3.init()
        self.lenguaje = lenguaje
        self.avatar = avatar

        # Objeto de Regex para validar los comandos
        self.comandos_patrones = {
            'modo_dibujo': lambda txt: self.__valid_comand('activa el modo dibujo', txt),
            'desactiva_modo_dibujo': lambda txt: self.__valid_comand('desactiva el modo dibujo', txt),

        }

        # Objeto de comandos
        self.MODO_DIBUJO = 'modo_dibujo'
        self.DESACTIVA_MODO_DIBUJO = 'desactiva_modo_dibujo'



    # Funcion privada para los regex
    def __valid_comand(self, nameComando, txt):
        return bool(re.search(fr'\b{self.avatar.lower()}\b.*\b{nameComando.lower()}\b|\b{nameComando.lower()}\b.*\b{self.avatar.lower()}\b', txt.lower()))

    # Funcion para generar voz
    def generar_voz(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()


    # Comando para activar el modo dibujo
    def modo_dibujo(self):
        # Le inidicamos que ha elegido este modo
        self.generar_voz("Okey activando el modo dibujo")
        
        # Regex para validar el comando
        # Abrimos pain para dibujar
        subprocess.run(['mspaint'])

    # Comando para desactivar el modo dibujo
    def desactiva_modo_dibujo(self):
        try:
            # Le indicamos que vamos ha desactivar el modo
            self.generar_voz("Okey desactivando el modo dibujo")

            # Desactivamos o cerramos el paint
            subprocess.run(['taskkill', '/f', '/im', 'mspaint.exe'])
        except:
            self.generar_voz("No se pudo cerrar Paint")


    # Metodo para abrir el site web de la deteccionde voz
    def open_detector(self, siteDetector):
        webbrowser.open(siteDetector)



