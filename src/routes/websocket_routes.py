from flask_socketio import  emit
import threading

def register_routes(socketio, ui):
        
    def connection(self):
        @socketio.on('connection')
        def connection_route():
            try:
                response = self.ui.start_connection()
                emit('connection_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('disconnection')
        def disconnection_route():
            try:
                response = self.ui.stop_connection()
                emit('disconnection_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('arm')
        def arming_route():
            try:
                response = self.ui.start_to_arm()
                emit('arm_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('disarm')
        def disarming_route():
            try:
                response = self.ui.start_to_disarm()
                emit('disarm_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('throttleup')
        def throttle_up_route():
            try:
                response = self.ui.start_motors()
                emit('throttleup_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('throttledown')
        def throttle_down_route():
            try:
                response = self.ui.stop_motors()
                emit('throttledown_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('rollright')
        def roll_right_route():
            try:
                response = self.ui.start_roll()
                emit('rollright_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('rollleft')
        def roll_left_route():
            try:
                response = self.ui.stop_roll()
                emit('rollleft_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('pitchforward')
        def pitch_forward_route():
            try:
                response = self.ui.start_pitch()
                emit('pitchforward_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('pitchbackward')
        def pitch_backward_route():
            try:
                response = self.ui.stop_pitch()
                emit('pitchbackward_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('yawclock')
        def yaw_clockwise_route():
            try:
                response = self.ui.start_yaw()
                emit('yawclock_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('yawanticlock')
        def yaw_anticlockwise_route():
            try:
                response = self.ui.stop_yaw()
                emit('yawanticlock_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('setalt')
        def hold_alt_route():
            try:
                response = self.ui.hold_alt()
                emit('setalt_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('land')
        def land_route():
            try:
                response = self.ui.return_to_land()
                emit('land_response', {'message': response})
            except Exception as e:
                emit('error', {'error': str(e)})

        @socketio.on('telemetry')
        def telemetry_route():
            try:
                def fetch_telemetry():
                    try:
                        response = self.ui.show_telemetry()
                        emit('telemetry_response', {'message': response})
                    except Exception as e:
                        emit('error', {'error': str(e)})
                
                thread = threading.Thread(target=fetch_telemetry)
                thread.start()
            except Exception as e:
                emit('error', {'error': str(e)})
