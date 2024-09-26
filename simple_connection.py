from pymavlink import mavutil

class Connection:
    def __init__(self,connection_string,baud=57600):
        try:
            self.connection_string = connection_string

            self.master = mavutil.mavlink_connection(self.connection_string,baud=baud)

            self.master.wait_heartbeat()  ## Heart Beat is the way of sending the response from the Pixhawk

            self.system_id = self.master.target_system
            self.component_id = self.master.target_component

            print(f"Target System:  {self.system_id} , Target Component: {self.component_id}")
        except Exception as e:
            print("Connection Error : ",e)
        
    def BatteryStatus(self):
            message = self.master.mav.command_long_encode(
                self.master.target_system,  # Target system ID
                self.master.target_component,  # Target component ID
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # ID of command to send
                0,  # Confirmation
                mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS,  # param1: Message ID to be streamed
                1000000, # param2: Interval in microseconds (1 second here)
                0,       # param3 (unused)
                0,       # param4 (unused)
                0,       # param5 (unused)
                0,       # param6 (unused)
                0        # param7 (unused)
                )

            self.master.mav.send(message)

            while True:
                 msg = self.master.recv_match(type="BATTERY_STATUS",blocking=True)
                 if msg:
                      battery_remaining = msg.battery_remaining # Battery Percentage remaining
                    #   print(f"Battery Remaining : {battery_remaining}%")

            return battery_remaining + "%"
    
    
    
            
     
if "__name__" == "__main__":
    drone_connection = Connection('/dev/ttyUSB0')
    drone_connection.BatteryStatus()
