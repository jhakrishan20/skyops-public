from dronekit import connect, Vehicle

class Handler:
    def __init__(self):
        self.vehicle = None
        self.is_connected = False
        self.mode = None

    def connect(self, connection_string, baud):
        if self.vehicle is not None:  # Prevent multiple connections
            print("⚠️ Already connected.")
            return True
        try:
            self.vehicle = connect(connection_string, wait_ready=True, baud=baud)
            self.is_connected = True
            print("✅ Successfully connected to the Pixhawk.")
            return True
        except Exception as e:
            self.is_connected = False
            print("❌ Connection failed:",{e})
            return False

    def disconnect(self):
        if self.vehicle:
            self.vehicle.close()
            self.is_connected = False
            self.vehicle = None
            print("✅ Disconnected from the Pixhawk.")
            return True
        print("❌ No active connection to disconnect.")
        return False

    def get_vehicle_state(self):
        if not self.is_connected or not self.vehicle:
            return {"error": "Vehicle not connected."}

        try:
            state = {
                "mode": self.vehicle.mode.name,
                "armed": self.vehicle.armed,
                "battery": {
                    "voltage": self.vehicle.battery.voltage,
                    "level": self.vehicle.battery.level,
                },
                "gps": {
                    "fix_type": self.vehicle.gps_0.fix_type,
                    "satellites": self.vehicle.gps_0.satellites_visible,
                    "latitude": self.vehicle.location.global_frame.lat,
                    "longitude": self.vehicle.location.global_frame.lon,
                },
                "altitude": self.vehicle.location.global_relative_frame.alt,
                "velocity": self.vehicle.velocity,  # [vx, vy, vz] in m/s
                "attitude": {
                    "yaw": self.vehicle.attitude.yaw,   # Rotation around the Z-axis
                    "pitch": self.vehicle.attitude.pitch,  # Rotation around the Y-axis
                    "roll": self.vehicle.attitude.roll,  # Rotation around the X-axis
                },
                "tilt": (self.vehicle.attitude.pitch ** 2 + self.vehicle.attitude.roll ** 2) ** 0.5,  # Approximate tilt
                "speed": {
                    "airspeed": self.vehicle.airspeed,  # Speed relative to air
                    "groundspeed": self.vehicle.groundspeed,  # Speed relative to ground
                },
            }

            return state
        except Exception as e:
            return {"error": f"Failed to retrieve vehicle state: {e}"}
