from communication.mavlink.handler import Handler
from mission.controls.controller import Controller
from telemetry.data.telemetry_model import TelemetryModel
from core.utils.portmanager import PortManager
from mission.controls.motors import MotorControl
from mission.planner.planner import Planner

from core.config.config import config

class UiController:
    def __init__(self):
        self.conn = Handler()
        self.manager = PortManager()
        self.control = None
        self.motors = None
        self.plan = None

    def start_connection(self):
        print(config)
        self.manager.free_port(config["serial_port"])
        message = self.conn.connect(config["serial_port"],config["baud"])

        if message == True:
           self.control = Controller(self.conn.vehicle,self.conn.is_connected)
           print(self.conn.get_vehicle_state())
           self.is_connected = True
        else:
           print("vehicle not connected")    
        return message

    def stop_connection(self):
        if self.is_connected == True:
           message = self.conn.disconnect()
           return message

    def start_to_arm(self):
        if self.conn.is_connected == True:
           self.control.disable_prearm_checks()
           message = self.control.arm_vehicle()
           if message == True:
              self.motors.is_arm = True
           self.motors = MotorControl(self.conn.vehicle)
           self.plan = Planner(self.conn.vehicle)   
           return message

    def start_to_disarm(self):
        if self.conn.is_connected:
            if self.motors.is_arm == True:
               message = self.control.disarm_vehicle()
               if message == True:
                   self.motors.is_arm = False
               self.motors = None   
               self.plan = None   
            return message
            
    def start_motors(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.throttle_up()
        return message

    def stop_motors(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.throttle_down()
           return message

    def start_roll(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.roll_right()
           return message
        
    def stop_roll(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.roll_left()
           return message 

    def start_pitch(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.pitch_forward()
           return message

    def stop_pitch(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.pitch_backward()
           return message

    def start_yaw(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.yaw_clockwise()
           return message

    def stop_yaw(self):
        if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.motors.yaw_anticlockwise()
           return message               

    def hold_alt(self):
       if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.plan.hold_altitude(3)
           return message
       
    def return_to_land(self):
       if self.conn.is_connected == True:
           if self.motors.is_arm == True:
              message = self.plan.emergency_landing()
           return message   


    def show_telemetry(self):
     if not self.conn.is_connected:
        return {"error": "❌ Drone is not connected."}
    
     tm = TelemetryModel(self.conn.vehicle)
     telemetry = {}

     def safe_call(method_name, method):
        """Calls a method safely and handles exceptions."""
        try:
            telemetry[method_name] = method()
        except Exception as e:
            telemetry[method_name] = f"⚠️ Error: {str(e)}"

     # Call each method safely
     safe_call("nav", tm.get_navigation_data)
     safe_call("attitude", tm.get_attitude_data)
     safe_call("gps", tm.get_gps_data)
     safe_call("system", tm.get_system_status)
     safe_call("battery", tm.get_battery_status)
     safe_call("imu", tm.get_imu_data)

     return telemetry

   #  lets talk about the plan segment of mission planner, what are the features of this segment 