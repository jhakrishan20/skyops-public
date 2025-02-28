from flask_socketio import emit
import threading
from ui.controllers.ui_controller import UiController

class DroneControlSocket:
    def __init__(self, socketio):
        self.socketio = socketio
        self.ui = UiController()
        self.register_routes()

    def register_routes(self):
        self.socketio.on_event('handshake', self.handshake)  
        self.socketio.on_event('connection', self.connection_route)
        self.socketio.on_event('disconnection', self.disconnection_route)
        self.socketio.on_event('arm', self.arming_route)
        self.socketio.on_event('disarm', self.disarming_route)
        self.socketio.on_event('throttleup', self.throttle_up_route)
        self.socketio.on_event('throttledown', self.throttle_down_route)
        self.socketio.on_event('rollright', self.roll_right_route)
        self.socketio.on_event('rollleft', self.roll_left_route)
        self.socketio.on_event('pitchforward', self.pitch_forward_route)
        self.socketio.on_event('pitchbackward', self.pitch_backward_route)
        self.socketio.on_event('yawclock', self.yaw_clockwise_route)
        self.socketio.on_event('yawanticlock', self.yaw_anticlockwise_route)
        self.socketio.on_event('setalt', self.hold_alt_route)
        self.socketio.on_event('land', self.land_route)
        self.socketio.on_event('telemetry', self.telemetry_route)

    def handshake(self, data=None): 
        print("🤝 Handshake event received from client.")
        self.socketio.emit("handshake_response", {"message": "Handshake successful!"})  

    def connection_route(self, data=None):
        self._handle_event(self.ui.start_connection, 'connection_response')

    def disconnection_route(self, data=None):
        self._handle_event(self.ui.stop_connection, 'disconnection_response')

    def arming_route(self, data=None):
        self._handle_event(self.ui.start_to_arm, 'arm_response')

    def disarming_route(self, data=None):
        self._handle_event(self.ui.start_to_disarm, 'disarm_response')

    def throttle_up_route(self, data=None):
        self._handle_event(self.ui.start_motors, 'throttleup_response')

    def throttle_down_route(self, data=None):
        self._handle_event(self.ui.stop_motors, 'throttledown_response')

    def roll_right_route(self, data=None):
        self._handle_event(self.ui.start_roll, 'rollright_response')

    def roll_left_route(self, data=None):
        self._handle_event(self.ui.stop_roll, 'rollleft_response')

    def pitch_forward_route(self, data=None):
        self._handle_event(self.ui.start_pitch, 'pitchforward_response')

    def pitch_backward_route(self, data=None):
        self._handle_event(self.ui.stop_pitch, 'pitchbackward_response')

    def yaw_clockwise_route(self, data=None):
        self._handle_event(self.ui.start_yaw, 'yawclock_response')

    def yaw_anticlockwise_route(self, data=None):
        self._handle_event(self.ui.stop_yaw, 'yawanticlock_response')

    def hold_alt_route(self, data=None):
        self._handle_event(self.ui.hold_alt, 'setalt_response')

    def land_route(self, data=None):
        self._handle_event(self.ui.return_to_land, 'land_response')

    def telemetry_route(self, data=None):
        threading.Thread(target=self._fetch_telemetry).start()

    def _fetch_telemetry(self):
        self._handle_event(self.ui.show_telemetry, 'telemetry_response')

    def _handle_event(self, function, response_event):
        try:
            response = function()
            self.socketio.emit(response_event, {'message': response})  
        except Exception as e:
            self.socketio.emit('error', {'error': str(e)})   