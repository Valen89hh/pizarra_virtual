from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from ContextData import enviar_datos_por_socket

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = "secret!"

socketio = SocketIO(app)

@app.route("/")
def hello_world():
    return render_template('index.html')

""" def send_message():
    while True:
        message = "Mensaje programado desde el servidor"
        socketio.emit('server_message', message)
        time.sleep(5)  # Espera 5 segundos antes de enviar el siguiente mensaje """

@app.route("/activar_detector", methods=["POST"])
def send_message():
    message = request.json.get("message")
    print(message)
    if message:
        socketio.emit('activate_voz', message)
        return "Mensaje enviado exitosamente"
    else:
        return "Error: No se proporcionó un mensaje"

@socketio.on('reconocido')
def handle_disconnect(datos):
    print("Voz: " + datos)
    enviar_datos_por_socket(datos)

@socketio.on('disconnect')
def handle_disconnect():
    print("Terminado")

if __name__ == "__main__":
    """ sendMessageThread = threading.Thread(target=send_message)
    sendMessageThread.daemon = True
    sendMessageThread.start() """

    socketio.run(app, host='127.0.0.1', port=8000)
