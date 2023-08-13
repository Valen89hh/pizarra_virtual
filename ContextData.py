import socket
import json
import requests
import multiprocessing
import threading
import time
from Voz import ComandosVoz

state = False
microfono = None
voz = ComandosVoz()

def recibir_datos_por_socket():
    # Configurar el socket
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  # Cambiar por la dirección IP del servidor
    port = 5000  # Cambiar por el puerto del servidor
    
    # Vincular el socket al host y puerto
    socket_servidor.bind((host, port))
    
    # Escuchar conexiones entrantes
    socket_servidor.listen()
    
    # Aceptar la conexión del cliente
    cliente_socket, direccion = socket_servidor.accept()
    
    # Recibir los datos
    datos_recibidos = cliente_socket.recv(1024).decode('utf-8')
    
    # Procesar los datos recibidos
    data = json.loads(datos_recibidos)
    
    # Cerrar la conexión
    cliente_socket.close()
    socket_servidor.close()

    return data

# Función para enviar los datos a través del socket
def enviar_datos_por_socket(data):
    # Configurar el socket
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  # Cambiar por la dirección IP del cliente
    port = 5000  # Cambiar por el puerto del cliente
    
    # Conectar al cliente
    socket_cliente.connect((host, port))
    
    # Enviar los datos
    mensaje = json.dumps(data)
    socket_cliente.sendall(mensaje.encode('utf-8'))
    
    # Cerrar la conexión
    socket_cliente.close()


def configurar_socket_servidor():
    # Configurar el socket del servidor
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  # Cambiar por la dirección IP del servidor
    port = 5000  # Cambiar por el puerto del servidor
    
    # Vincular el socket al host y puerto
    socket_servidor.bind((host, port))
    
    # Escuchar conexiones entrantes
    socket_servidor.listen()
    
    return socket_servidor

def voz_alexa():
    time.sleep(1)
    voz.generar_voz("Soy Alexa, En que te puedo ayudar")

def process_microfono():
    # voz.generar_voz("Si dime en que te ayudo")
    url = "http://localhost:8000/activar_detector"
    data = {"message": True}
    print("activando")
    response = requests.post(url, json=data)
    print("Response: " +response.text)

def activate_microfono():
    global state, microfono
    print("Microfono: "  + str(state))
    if not state:
        state = True
        print("ENTRE")
        microfono = multiprocessing.Process(target=process_microfono)
        voz_hilo = threading.Thread(target=voz_alexa)
        voz_hilo.start()
        microfono.start()


    try:
        if not microfono.is_alive():
            print("PROCESO TERMINADO")
            state = False
    except:
        print("No se inicializo el proceso")

