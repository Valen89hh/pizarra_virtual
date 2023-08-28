import pyttsx3
import pyaudio
import wave
import re
from wit import Wit
import sounddevice as sd
import threading
import scipy.io.wavfile as wav

class Voz:
    def __init__(self, acces_token, avatar="Alexa", lenguaje='es', audio_file="audio.wav"):
        self.client = Wit(access_token=acces_token)
        self.p = pyaudio.PyAudio()
        self.audio_file = audio_file

        self.engine = pyttsx3.init()
        self.lenguaje = lenguaje
        self.avatar = avatar

        # Objeto de Regex para validar los comandos
        self.comandos_patrones = {
            'modo_dibujo': lambda txt: self.__valid_comand('activa el modo dibujo', txt),
            'modo_grafico': lambda txt: self.__valid_comand('activa el modo gráfico', txt),
            'modo_imagen': lambda txt: self.__valid_comand('activa el modo imagen', txt),
            'desactiva_modo_dibujo': lambda txt: self.__valid_comand('desactiva el modo dibujo', txt),

        }

        # Objeto de comandos
        self.MODO_DIBUJO = 'modo_dibujo'
        self.MODO_GRAFICO = 'modo_grafico'
        self.MODO_IMAGEN = 'modo_imagen'
        self.DESACTIVA_MODO_DIBUJO = 'desactiva_modo_dibujo'

        self.sample_rate = 44100  # Frecuencia de muestreo en Hz


    # Funcion privada para los regex
    def __valid_comand(self, nameComando, txt):
        return bool(re.search(fr'\b{self.avatar.lower()}\b.*\b{nameComando.lower()}\b|\b{nameComando.lower()}\b.*\b{self.avatar.lower()}\b', txt.lower()))

    # Funcion para generar voz
    def generar_voz(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()
        

    def __record_audio(self, seconds):
       

        print(f"Recording {self.audio_file} for {seconds} seconds...")
        audio_data = sd.rec(int(seconds * self.sample_rate), samplerate=self.sample_rate, channels=2)
        sd.wait()  # Esperar a que la grabación termine
        print(f"Recording {self.audio_file} complete.")
    
        # Guardar la grabación en un archivo WAV
        wav.write(self.audio_file, self.sample_rate, audio_data)

    def __wit_ai_speech_to_text(self):
        headers = {
            'Content-Type': 'audio/wav',
        }

        audio = open(self.audio_file, 'rb')
        resp = self.client.speech(audio, headers=headers)
        return resp["text"]
        
    def reconocer_voz(self, seconds=5):
        self.__record_audio(seconds)
        response = self.__wit_ai_speech_to_text()
        print("Texto: ", response)
        self.generar_voz(response)
        return response

# Configura tu token de acceso de Wit.ai

# Función para grabar audio desde el micrófono

# Función para enviar el audio a Wit.ai y obtener el texto reconocido


if __name__ == "__main__":
    voz = Voz('FFKVDNMPF64WRD4IJ4MTDZEXSVL6RBYT')
    voz.reconocer_voz()
