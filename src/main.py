from flask import Flask
from flask_socketio import SocketIO
from routes.websocket_routes import DroneControlSocket
from core.config.config import config

# Create Flask instance
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize WebSocket routes BEFORE running the app
drone_socket = DroneControlSocket(socketio)

if __name__ == "__main__":
    socketio.run(app, host=config["host"], port=config["server_port"], debug=True)
