# import time
# from dronekit import VehicleMode

# class Planner:
#     def __init__(self, vehicle):
#         self.vehicle = vehicle

#     def set_mode(self, mode_name):
#         try:
#             if not self.vehicle:
#                 print("❌ No vehicle connected!")
#                 return False

#             print(f"🔄 Switching to {mode_name} mode...")
#             self.vehicle.mode = VehicleMode(mode_name)
#             time.sleep(2)  # Allow mode switch time

#             if self.vehicle.mode.name == mode_name:
#                 print(f"✅ Successfully switched to {mode_name}.")
#                 return True
#             else:
#                 print(f"❌ Failed to switch to {mode_name}.")
#                 return False

#         except Exception as e:
#             print(f"❌ Error: {e}")
#             return False

#     def hold_altitude(self, target_alt, hover_mode="LOITER"):
#      try:
#         target_alt = int(target_alt)

#         if not self.vehicle:
#             print("❌ No vehicle connected!")
#             return False

#         # Ensure the vehicle is armed
#         self.vehicle.armed = True
#         # time.sleep(2)  # Allow time for arming

#         # Switch to MANUAL throttle mode (if needed)
#         if not self.set_mode("LOITER"):  # Stabilized mode allows manual throttle control
#             return False

#         print(f"🚀 Taking off to {target_alt} ft ({target_alt * 0.3048:.2f} m)...")

#         # Manual throttle control loop
#         while True:
#             current_alt = self.vehicle.location.global_relative_frame.alt
#             print(f"📡 Current Altitude: {current_alt:.2f} m")

#             if current_alt < target_alt * 0.3:
#                 print("⚠️ Altitude rising slowly, increasing throttle...")
#                 self.vehicle.channels.overrides['3'] = 1700  # High throttle boost
#             elif current_alt < target_alt * 0.7:
#                 self.vehicle.channels.overrides['3'] = 1550  # Moderate throttle
#             elif current_alt < target_alt * 0.9:
#                 self.vehicle.channels.overrides['3'] = 1400  # Fine throttle adjustment
#             else:
#                 break  # Once 90% of target altitude is reached, stop manual control

#             time.sleep(1)

#         # Reset manual throttle control
#         self.vehicle.channels.overrides['3'] = None  

#         # Switch to hover mode (ALT_HOLD or LOITER)
#         print(f"🔄 Switching to {hover_mode} mode for stable hovering...")
#         if not self.set_mode(hover_mode):
#             return False

#         print(f"✅ Hovering at {target_alt} ft.")
#         return True

#      except Exception as e:
#          print(f"❌ Error: {e}")
#          return False
 

#     def emergency_landing(self):
#         try:
#             if not self.vehicle:
#                 print("❌ No vehicle connected!")
#                 return False

#             print("⚠️ Emergency detected! Initiating RTL...")
#             self.set_mode("LAND")
#             return True

#         except Exception as e:
#             print(f"❌ Error: {e}")
#             return False
       

import time
from dronekit import VehicleMode

class Planner:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def set_mode(self, mode_name):
        """Set the flight mode and confirm the switch."""
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

    def hold_altitude(self, target_alt, hover_mode="LOITER"):
        try:
            target_alt = float(target_alt)  # Ensure it's a float for comparison

            if not self.vehicle:
                print("❌ No vehicle connected!")
                return False

            if self.vehicle.location.global_relative_frame.alt >= target_alt:
                print(f"🚀 Already above {target_alt}m. No climb needed.")
                return True

            # Switch to GUIDED mode for takeoff
            if not self.set_mode("GUIDED"):
                return False

            print(f"🚀 Taking off to {target_alt}m...")
            self.vehicle.simple_takeoff(target_alt)

            # Wait until the drone reaches the target altitude
            while True:
                current_alt = self.vehicle.location.global_relative_frame.alt
                print(f"📡 Current Altitude: {current_alt:.2f} m")

                if current_alt >= target_alt * 0.95:  # Reached 95% of target altitude
                    print(f"✅ Altitude {target_alt}m reached.")
                    break

                time.sleep(1)

            # Transition to hover mode (ALT_HOLD or LOITER)
            print(f"🔄 Switching to {hover_mode} mode for stable hovering...")
            if not self.set_mode(hover_mode):
                return False

            print(f"✅ Hovering at {target_alt}m.")
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def emergency_landing(self):
        """Safely land the drone in case of emergency."""
        try:
            if not self.vehicle:
                print("❌ No vehicle connected!")
                return False

            print("⚠️ Emergency detected! Initiating landing...")

            # Check GPS fix before deciding to LAND or RTL
            if self.vehicle.gps_0.fix_type < 3:  # Weak GPS fix
                print("⚠️ Weak GPS! Performing immediate LAND.")
                self.set_mode("LAND")
            else:
                print("🏡 GPS fix strong. Returning to launch (RTL).")
                self.set_mode("RTL")

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        