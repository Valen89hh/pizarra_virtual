import tkinter as tk
from tkinter import colorchooser
import cv2
from PIL import Image, ImageTk
from Manos import Manos
from voz_command import Voz
import threading
import numpy as np

class AplicacionDibujo:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Dibujo y Reconocimiento de Manos")

        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(fill="both", expand=True)

        self.header = tk.Frame(self.frame_main)
        self.header.pack()

        self.body = tk.Frame(self.frame_main)
        self.body.pack()
        

        # ------------ HEADER -----------------

        # Configurar botones
        self.boton_limpiar = tk.Button(self.header, text="Limpiar", command=self.limpiar_lienzo)
        self.boton_limpiar.grid(row=0, column=0, padx=10)

        self.btn_audio = tk.Button(self.header, text="Grabar 🎙", command=self.grabar_audio)
        self.btn_audio.grid(row=0, column=1, padx=10)

        self.btn_colores = tk.Button(self.header, text="Colores 🖌", command=self.select_color)
        self.btn_colores.grid(row=0, column=2, padx=10)


        # ------------- BODY -----------------
        # Crear un lienzo para dibujar
        self.lienzo = tk.Canvas(self.body, width=800, height=600, bg="white")
        self.lienzo.pack(side="right")

        # Crea un Label para mostrar el video procesado
        self.label_video = tk.Label(self.body)
        self.label_video.pack(side="left")

        # Reconocimiento de voz
        WIT_AI_ACCESS_TOKEN = 'FFKVDNMPF64WRD4IJ4MTDZEXSVL6RBYT'
        self.voz = Voz(acces_token=WIT_AI_ACCESS_TOKEN)

        #Reconocimiento de manos
        self.manos = Manos()
        self.cap = cv2.VideoCapture(0)


        # Configurar eventos del lienzo
        self.lienzo.bind("<Button-1>", self.iniciar_dibujo)
        self.lienzo.bind("<B1-Motion>", self.dibujar)
        self.lienzo.bind("<ButtonRelease-1>", self.finalizar_dibujo)

        self.dibujando = False
        self.ultimo_x = None
        self.ultimo_y = None

        self.ancho, self.alto = (600,600)
        self.pos = None
        self.cursor = self.lienzo.create_oval(0,0,0,0, fill="red")

        # flag 
        self.grabando_audio = False
        self.modo_dibujo = False
        self.modo_grafico = False
        self.modo_imagen = False

        self.screen_x_ini = 0
        self.screen_y_ini = 0
        self.screen_x_fin = 800
        self.screen_y_fin = 600
        self.aspect_ratio = (self.screen_x_fin - self.screen_x_ini) / (self.screen_y_fin - self.screen_y_ini)
        self.x_y_ini = 100 
        print(self.aspect_ratio)

    def __process_recor_audio(self):
        text = self.voz.reconocer_voz()

        self.modo_dibujo = self.voz.comandos_patrones[self.voz.MODO_DIBUJO](text)
        self.modo_grafico = self.voz.comandos_patrones[self.voz.MODO_GRAFICO](text)
        self.modo_imagen = self.voz.comandos_patrones[self.voz.MODO_IMAGEN](text)
            

        self.grabando_audio = False

    def grabar_audio(self):
        if not self.grabando_audio:
            self.grabando_audio = True
            audio_proccess = threading.Thread(target=self.__process_recor_audio)
            audio_proccess.start()

    

    def mostrar_video_en_label(self):
        ret, frame = self.cap.read()
        
        if ret:
            frame = cv2.resize(frame, (self.ancho, self.alto), interpolation=cv2.INTER_AREA)
            # frame = cv2.flip(frame, 1)
            # Procesa el fotograma capturado, por ejemplo, detecta manos
            
            area_width = self.ancho - self.x_y_ini * 2
            area_height = int(area_width/ self.aspect_ratio)
            aux_img = np.zeros(frame.shape, np.uint8)
            aux_img = cv2.rectangle(aux_img, (self.x_y_ini, self.x_y_ini), (self.x_y_ini + area_width, self.x_y_ini + area_height), (255, 0, 0), -1)

            frame_procesado, puntos = self.manos.reconocer_mano(frame, dibujar=True)
            frame_procesado = cv2.addWeighted(frame_procesado, 1, aux_img, 0.7, 0)
            
            if len(puntos) == 1:
                # d = self.manos.get_distance(puntos[0][6], puntos[0][4])
                # print(d)
                x, y = puntos[0][8]

                xm = int(np.interp(x, (self.x_y_ini, self.x_y_ini+area_width), (self.screen_x_ini, self.screen_x_fin)))
                ym = int(np.interp(y, (self.x_y_ini, self.x_y_ini+area_height), (self.screen_y_ini, self.screen_y_fin)))



                self.lienzo.coords(self.cursor, xm-5,ym-5,xm+5,ym+5)
                if puntos[0][12][1] < puntos[0][9][1]:
                    # print("dibujar")

                    
                    # Verificar si self.ultimo_x y self.ultimo_y son None
                    if self.ultimo_x is not None and self.ultimo_y is not None:
                        if self.modo_dibujo:
                            self.lienzo.create_line(self.ultimo_x, self.ultimo_y, xm, ym, fill="black", width=2)
                    
                    
                    self.ultimo_x = xm
                    self.ultimo_y = ym
                else:
                    self.ultimo_x = None
                    self.ultimo_y = None
                # self.lienzo.create_oval(x-5, y-5, x+5, y+5, fill="red")

            elif len(puntos) == 2:
                hand_1_p8 = puntos[0][8]
                hand_2_p8 = puntos[1][8]
                hand_3_p8 = puntos[0][4]
                hand_4_p8 = puntos[1][4]
                print(hand_1_p8, hand_2_p8)
                d1 = self.manos.get_distance(hand_1_p8, hand_2_p8, dibujar=True) 
                d2 = self.manos.get_distance(hand_3_p8, hand_4_p8, dibujar=True) 
               
                x = abs(hand_1_p8[0]-hand_2_p8[0])//2 + min(hand_2_p8[0], hand_1_p8[0])
                y = abs(hand_1_p8[1]-hand_2_p8[1])//2 + min(hand_2_p8[1], hand_1_p8[1])
                punto_1 = (x, y)
                cv2.circle(frame_procesado, punto_1, 10, (255,0,0), thickness=2)
                d3 = self.manos.get_distance(punto_1, hand_4_p8, True)
                if d1 <= 10 and d2 <= 10 and d3 < 10:
                    
                    self.grabar_audio()
            # Convierte la imagen de OpenCV a formato RGB
            imagen_rgb = cv2.cvtColor(frame_procesado, cv2.COLOR_BGR2RGB)
            
            # Convierte la imagen RGB a formato ImageTk
            imagen_tk = ImageTk.PhotoImage(image=Image.fromarray(imagen_rgb))
            
            # Muestra la imagen en el Label
            self.label_video.config(image=imagen_tk)
            self.label_video.image = imagen_tk
            
            # Llama a esta función nuevamente después de un tiempo para actualizar el video
            self.root.after(10, self.mostrar_video_en_label)

    def iniciar_dibujo(self, evento):
        self.dibujando = True
        self.ultimo_x = evento.x
        self.ultimo_y = evento.y

    def dibujar(self, evento):
        if self.dibujando:
            x, y = evento.x, evento.y
            self.lienzo.create_line(self.ultimo_x, self.ultimo_y, x, y, fill="black", width=2)
            self.ultimo_x = x
            self.ultimo_y = y

    def finalizar_dibujo(self, evento):
        self.dibujando = False
        self.ultimo_x = None
        self.ultimo_y = None

    def limpiar_lienzo(self):
        self.lienzo.delete("all")
        self.cursor = self.lienzo.create_oval(0,0,0,0, fill="red")


    def select_color(self):
        color = colorchooser.askcolor(title="Selecciona un color")
        if color[1] is not None:
            color_hex = color[1]
            print(f"Color elegido: {color_hex}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionDibujo(root)
    app.mostrar_video_en_label()  # Lanza la función para mostrar el video
    root.mainloop()
