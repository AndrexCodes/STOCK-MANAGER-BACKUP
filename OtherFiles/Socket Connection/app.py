from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store client sessions
clients = []

def send_message_to_client():
    while True:
        for client_sid in clients:
            count = 50
            message = f'Message {count + 1}'
            print(f'Sending message to client {client_sid}: {message}')
            socketio.emit('message', {"message": message}, room=client_sid)
            time.sleep(2)  # Wait for 2 seconds between messages

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(request.args.get("identity"))
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    print('Client disconnected')

if __name__ == '__main__':
    x = threading.Thread(target=send_message_to_client)
    x.daemon = True
    x.start()
    socketio.run(app, port=3333)
