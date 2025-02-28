from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO
import threading
import time
from ui.controllers.ui_controller import UiController

class Ui_Routes:
    def __init__(self):
        # Create a Blueprint instance
        self.api_bp = Blueprint('api', __name__)
        # Register all routes
        self.register_routes()
        self.ui=UiController()

    def register_routes(self):
        self.api_bp.add_url_rule('/connection', 'connection', self.connection_route, methods=['POST'])
        self.api_bp.add_url_rule('/disconnection', 'disconnection', self.disconnection_route, methods=['POST'])
        self.api_bp.add_url_rule('/arm', 'arm', self.arming_route, methods=['POST'])
        self.api_bp.add_url_rule('/disarm', 'disarm', self.disarming_route, methods=['POST'])
        self.api_bp.add_url_rule('/throttleup', 'throttleup', self.throttle_up_route, methods=['POST'])
        self.api_bp.add_url_rule('/throttledown', 'throttledown', self.throttle_down_route, methods=['POST'])
        self.api_bp.add_url_rule('/rollright', 'rollright', self.roll_right_route, methods=['POST'])
        self.api_bp.add_url_rule('/rollleft', 'rollleft', self.roll_left_route, methods=['POST'])
        self.api_bp.add_url_rule('/pitchforward', 'pitchforward', self.pitch_forward_route, methods=['POST'])
        self.api_bp.add_url_rule('/pitchbackward', 'pitchbackward', self.pitch_backward_route, methods=['POST'])
        self.api_bp.add_url_rule('/yawclock', 'yawclock', self.yaw_clockwise_route, methods=['POST'])
        self.api_bp.add_url_rule('/yawanticlock', 'yawanticlock', self.yaw_anticlockwise_route, methods=['POST'])
        self.api_bp.add_url_rule('/setalt', 'hold_alt', self.hold_alt_route, methods=['POST'])
        self.api_bp.add_url_rule('/land', 'land', self.land_route, methods=['POST'])
        self.api_bp.add_url_rule('/telemetry', 'telemetry', self.telemetry_route, methods=['GET'])

    def connection_route(self):
        try:
            response = self.ui.start_connection()
            # print(self.ui.start_listening()) 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def disconnection_route(self):
        try:
            response = self.ui.stop_connection() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500    

    def arming_route(self):
        try:
            response = self.ui.start_to_arm() 
            return jsonify({'message': response}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500 

    def disarming_route(self):
        try:
            response = self.ui.start_to_disarm() 
            return jsonify({'message': response}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500 
        
    def throttle_up_route(self):
        try:
            response = self.ui.start_motors() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def throttle_down_route(self):
        try:
            response = self.ui.stop_motors() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def roll_right_route(self):
        try:
            response = self.ui.start_roll() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 

    def roll_left_route(self):
        try:
            response = self.ui.stop_roll() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 

    def pitch_forward_route(self):
        try:
            response = self.ui.start_pitch() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def pitch_backward_route(self):
        try:
            response = self.ui.stop_pitch() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def yaw_clockwise_route(self):
        try:
            response = self.ui.start_yaw() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 

    def yaw_anticlockwise_route(self):
        try:
            response = self.ui.stop_yaw() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def hold_alt_route(self):
        try:
            response = self.ui.hold_alt() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def land_route(self):
        try:
            response = self.ui.return_to_land() 
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500                                          

    def telemetry_route(self):
     try:
        result = []

        def fetch_telemetry():
            try:
                response = self.ui.show_telemetry()
                result.append(response)  # Store response in the list
            except Exception as e:
                result.append(str(e))  # Store error if exception occurs

        # Start the thread
        thread = threading.Thread(target=fetch_telemetry)
        thread.start()
        thread.join()  # Wait for thread to finish

        # Check if error occurred
        if isinstance(result[0], Exception):
            return jsonify({'error': result[0]}), 500

        return jsonify({'message': result[0]}), 200
     except Exception as e:
        return jsonify({'error': str(e)}), 500
           
        
        