from pymavlink import mavutil

class MavLinkMessenger:
    def __init__(self,connection_string):
        self.master = mavutil.mavlink_connection(connection_string)
        self.master.wait_heartbeat()
        print("Target System: ",self.master.target_system,"Target Component",self.master.target_component)
    
    def arm(self):
        # Constructing the command to arm the copter
        command_long_msg = self.master.mav.command_long_encode(
            0, #for target system
            0, #for target component
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, #command for what you wanted to do by sending the message
            0, # Confirmation
            1, # Arm
            0,0,0,0,0,0 # parameters (not used)
        )

        self.master.mav.send(command_long_msg)
    
    def disarm(self):
        # Constructing the command to disarm the copter 
        command_long_msg = self.master.mav.command_long_encode(
            0,
            0,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0,
            0,0,0,0,0,0
        )

        self.master.mav.senf(command_long_msg)
    
    def set_home_location(self):
        self.master.mav.command_long_send()(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_SET_HOME,
            1,  #set current location
            0,0,0,0,  #Unused Parameters
            0,0,0  # Latitude ,Longitude,Altitude
        )
        print("Home Location Set")
    
    def get_home_location(self):
        self.master.mav.command_long_send()(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_GET_HOME_POSITION,
            0,0,0,0,0,0,0,0
        )
        msg = self.master.recv_match(type='HOME_POSITION',blocking=True,timeout=10)
        if msg is not None:
            print(f"Home position: Latitude={msg.latitude}, Longitude={msg.longitude}, Altitude={msg.altitude}")
            return (msg.latitude, msg.longitude, msg.altitude)
        else:
            print("Failed to get home position.")
            return None
    
    def 