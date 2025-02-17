from communication.mavlink.handler import Handler
from dronekit import VehicleMode
import time

class Controller():
    def __init__(self,vehicle,is_connected):
        self.vehicle = vehicle
        self.is_connected = is_connected

    def arm_vehicle(self):
        if not self.is_connected or not self.vehicle:
            return "❌ Vehicle not connected."
        
        try:
            # Switch to a mode that doesn't require GPS
            self.vehicle.mode = VehicleMode("STABILIZE")
            print("⏳ Switching to STABILIZE mode...")
            while not self.vehicle.mode.name == "STABILIZE":
                time.sleep(0.5)

            print("✅ Mode set to STABILIZE. Attempting to arm the vehicle...")

            # Arm the vehicle
            self.vehicle.armed = True
            while not self.vehicle.armed:
                print("⏳ Waiting for arming...")
                time.sleep(1)
            
            print("✅ Vehicle armed successfully.")
            return True

        except Exception as e:
            print(f"❌ Arming failed: {e}")
            return False


    def disarm_vehicle(self):
        if not self.is_connected or not self.vehicle:
            return "❌ Vehicle not connected."

        try:
            if not self.vehicle.armed:
                return "✅ Vehicle is already disarmed."

            self.vehicle.armed = False
            print("✅ Vehicle is disarming...")
            return True
        except Exception as e:
            print("❌ Failed to disarm the vehicle: ",{e})
            return False
        
    def disable_prearm_checks(self):
        if self.vehicle is None:
            print("❌ Vehicle not connected. Cannot disable pre-arm checks.")
            return

        try:
            # Disable all pre-arm checks
            self.vehicle.parameters['ARMING_CHECK'] = 0
            print("✅ Pre-arm checks disabled successfully!")
        except Exception as e:
            print(f"❌ Failed to disable pre-arm checks: {e}")

        