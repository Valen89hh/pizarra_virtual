import pyttsx3
import pyaudio
import wave
import re
from wit import Wit


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
        

    def __record_audio(self, seconds):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000


        stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        self.generar_voz("Grabando audio")
        frames = []

        for _ in range(0, int(RATE / CHUNK * seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Terminó de grabar.")
        stream.stop_stream()
        stream.close()
        self.p.terminate()

        wf = wave.open(self.audio_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def __wit_ai_speech_to_text(self):
        headers = {
            'Content-Type': 'audio/wav',
        }


        with open(self.audio_file, 'rb') as audio:
            resp = self.client.speech(audio, headers=headers)
            return resp["text"]
        
    def reconocer_voz(self, seconds=5):
        self.__record_audio(seconds)
        response = self.__wit_ai_speech_to_text()
        print("Texto: ", response)
        self.generar_voz(response)

# Configura tu token de acceso de Wit.ai

# Función para grabar audio desde el micrófono

# Función para enviar el audio a Wit.ai y obtener el texto reconocido


""" if __name__ == "__main__":
    voz = Voz(WIT_AI_ACCESS_TOKEN)
    voz.reconocer_voz() """
