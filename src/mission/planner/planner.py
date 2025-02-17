import time
from dronekit import VehicleMode

class Planner:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def set_mode(self, mode_name):
        try:
            if not self.vehicle:
                print("❌ No vehicle connected!")
                return False

            print(f"🔄 Switching to {mode_name} mode...")
            self.vehicle.mode = VehicleMode(mode_name)
            time.sleep(2)  # Allow mode switch time

            if self.vehicle.mode.name == mode_name:
                print(f"✅ Successfully switched to {mode_name}.")
                return True
            else:
                print(f"❌ Failed to switch to {mode_name}.")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def hold_altitude(self, target_alt, hover_mode="ALT_HOLD"):
     try:
        target_alt = int(target_alt)

        if not self.vehicle:
            print("❌ No vehicle connected!")
            return False

        # Ensure the vehicle is armed
        self.vehicle.armed = True
        time.sleep(2)  # Allow time for arming

        # Switch to MANUAL throttle mode (if needed)
        if not self.set_mode("STABILIZE"):  # Stabilized mode allows manual throttle control
            return False

        print(f"🚀 Taking off to {target_alt} ft ({target_alt * 0.3048:.2f} m)...")

        # Manual throttle control loop
        while True:
            current_alt = self.vehicle.location.global_relative_frame.alt
            print(f"📡 Current Altitude: {current_alt:.2f} m")

            if current_alt < target_alt * 0.3:
                print("⚠️ Altitude rising slowly, increasing throttle...")
                self.vehicle.channels.overrides['3'] = 1700  # High throttle boost
            elif current_alt < target_alt * 0.7:
                self.vehicle.channels.overrides['3'] = 1550  # Moderate throttle
            elif current_alt < target_alt * 0.9:
                self.vehicle.channels.overrides['3'] = 1400  # Fine throttle adjustment
            else:
                break  # Once 90% of target altitude is reached, stop manual control

            time.sleep(1)

        # Reset manual throttle control
        self.vehicle.channels.overrides['3'] = None  

        # Switch to hover mode (ALT_HOLD or LOITER)
        print(f"🔄 Switching to {hover_mode} mode for stable hovering...")
        if not self.set_mode(hover_mode):
            return False

        print(f"✅ Hovering at {target_alt} ft.")
        return True

     except Exception as e:
         print(f"❌ Error: {e}")
         return False
 

    def emergency_landing(self):
        try:
            if not self.vehicle:
                print("❌ No vehicle connected!")
                return False

            print("⚠️ Emergency detected! Initiating RTL...")
            self.set_mode("LAND")
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False
       