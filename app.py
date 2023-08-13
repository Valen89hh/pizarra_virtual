from ContextData import recibir_datos_por_socket, activate_microfono
from run import socketio, app   
import multiprocessing
import numpy as np
import cv2
from Manos import Manos
from Voz import ComandosVoz
import tkinter as tk

cmd_voz = ComandosVoz()
terminar_frame = False
terminar_socket = False
server_process = None
client_process = None
img_process = None
ventana = None

# Obtenemos las medidas de la pantalla del user
SCREEN_X_START = 0
SCREEN_Y_START = 0
SCREEN_X_END = None
SCREEN_Y_END = None
aspect_ratio = None
X_Y_START = 100

def run_server():
    socketio.run(app, host='127.0.0.1', port=8000)

# Procesos para abrir algunos comandos en segundo plano
def open_dibujo():
    cmd_voz.modo_dibujo()

def run_client():
    while not terminar_socket:
        print("--------------------- CLIENTE ---------------")
        datos = recibir_datos_por_socket()
        cmd_voz.generar_voz(datos)
        print("DaTA: " + datos)
        if cmd_voz.comandos_patrones[cmd_voz.MODO_DIBUJO](datos):
            dibujo_process = multiprocessing.Process(target=open_dibujo)
            dibujo_process.start()
        
        if cmd_voz.comandos_patrones[cmd_voz.DESACTIVA_MODO_DIBUJO](datos):
            cmd_voz.desactiva_modo_dibujo()
        print("--------------------- CLIENTE END ---------------")
        

def process_frame(aspect_ratio, sc_x_fin, sc_y_fin):
    global terminar_frame
    print("DESDE FRAME-----------: ", aspect_ratio)

    cmd_voz.open_detector("http://127.0.0.1:8000")

    cap = cv2.VideoCapture(1)

    manos = Manos()

    ancho, alto = (600, 600)

    time = 0

    # Dibujamos una area proporcional a la del juego
    area_width = ancho - X_Y_START * 2
    area_height = int(area_width / aspect_ratio)
    aux_img = np.zeros((ancho, alto, 3), dtype=np.uint8)
    cv2.rectangle(aux_img, (X_Y_START, X_Y_START, area_width, area_height), (255,0,0), -1)


    threshold = 70  # Umbral para detectar cambios bruscos

    previous_distance = None  # Almacena la distancia anterior
    while not terminar_frame:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (ancho, alto), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1)
        frame, puntos = manos.reconocer_mano(frame)

        
        

        frame = cv2.addWeighted(frame, 1, aux_img, 0.7, 0)
        if len(puntos) == 2:
            # print("Puntos")

            # Evaluamos el gesto para reconocer los comandos de voz
            d = manos.get_distance(puntos[0][12], puntos[1][12], True)
            mouse = puntos[0][8]
            


            if previous_distance is not None:
                if abs(d - previous_distance) > threshold:
                    print("Cambio brusco detectado:", d, " (anterior:", previous_distance, ")")
                    time = 0
                else:
                    
                    if d < 10 and puntos[0][0][1] > puntos[0][12][1] and puntos[1][0][1] > puntos[1][12][1]:
                        time += 1
                        print(time)
                        if time == 5:

                            print("Activando")
                            activate_microfono()
                            time = 0
            previous_distance = d
                # print("Habla")
                # activate_microfono()
            


        cv2.imshow("Manos", frame)
        # cv2.imshow("aspect", aux_img)
        t = cv2.waitKey(1)
        if t == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()

def iniciar_procesos():
    global server_process, client_process, img_process, terminar_frame, terminar_socket

    terminar_socket = False
    terminar_frame = False

    try:
        if not server_process.is_alive() and not client_process.is_alive() and not img_process.is_alive():
            server_process = multiprocessing.Process(target=run_server)
            client_process = multiprocessing.Process(target=run_client)
            img_process = multiprocessing.Process(target=process_frame, args=(aspect_ratio, SCREEN_X_END, SCREEN_Y_END))

            server_process.start()
            client_process.start()
            img_process.start()
        else:
            print("Los procesos siguen activos")
    except:
        print("Iniciando 1 proceso")
        server_process = multiprocessing.Process(target=run_server)
        client_process = multiprocessing.Process(target=run_client)
        img_process = multiprocessing.Process(target=process_frame, args=(aspect_ratio, SCREEN_X_END, SCREEN_Y_END))
        server_process.daemon = True
        client_process.daemon = False
        img_process.daemon = False
        server_process.start()
        client_process.start()
        img_process.start()

def detener_procesos():
    global server_process, client_process, img_process, terminar_socket, terminar_frame
    if server_process is not None and client_process is not None and img_process is not None:
        print(server_process)
        print("Procesos terminados")
        server_process.terminate()
        server_process.join()
        client_process.terminate()
        client_process.join()
        img_process.terminate()
        img_process.join()
        terminar_socket = True
        terminar_frame = True
    else:
        print("El proceso no ha sido iniciado")

def cerrar_procesos():
    detener_procesos()
    ventana.destroy()

def start_tkinter():
    global ventana, SCREEN_Y_END, SCREEN_X_END, aspect_ratio

    ventana = tk.Tk()

    # Ancho y alto
    SCREEN_X_END = ventana.winfo_screenwidth()
    SCREEN_Y_END = ventana.winfo_screenheight()

    # Calculamos el aspect ratio
    aspect_ratio = (SCREEN_X_END - SCREEN_X_START) / (SCREEN_Y_END - SCREEN_Y_START)

    print(SCREEN_X_END, SCREEN_Y_END, aspect_ratio)


    button = tk.Button(ventana, text="Ejecutar", command=iniciar_procesos)
    button.pack()

    stop_button = tk.Button(ventana, text="Detener", command=detener_procesos)
    stop_button.pack()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_procesos)

    ventana.mainloop()

if __name__ == '__main__':
    print(SCREEN_X_END, SCREEN_Y_END)
    start_tkinter()


