from flask_cors import CORS
from flask import Flask
from flask_socketio import SocketIO
from routes.ui_routes import Ui_Routes
from routes.websocket_routes import register_routes
from ui.controllers.ui_controller import UiController

#create instance of flask
app = Flask(__name__)
CORS(app)
# ui = UiController()
# socketio = SocketIO(app, cors_allowed_origins="*")

ui_routes = Ui_Routes().api_bp

# Register the Blueprint
app.register_blueprint(ui_routes, url_prefix='/api')

# Register routes from websockets_routes.py
# register_routes(socketio, ui)

if __name__ == "__main__":

 app.run(host='0.0.0.0', port=5000)
#  socketio.run(app, host="0.0.0.0", port=5000, debug=True)


