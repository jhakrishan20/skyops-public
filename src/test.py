# from flask import Flask
# from flask_socketio import SocketIO, send, emit
# import time

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '12345'
# socketio = SocketIO(app, cors_allowed_origins="*")

# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")  # ✅ Print message in server logs
#     emit("message", "Welcome! You are connected to the server.")  # ✅ Use emit() instead of send()

# # # Periodically send messages from the server
# # def send_periodic_updates():
# #     while True:
# #         time.sleep(5)  # Send a message every 5 seconds
# #         socketio.send("Server update: Keep alive!")

# if __name__ == '__main__':
#     import threading
#     # threading.Thread(target=send_periodic_updates).start()  # Start sending updates
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)
