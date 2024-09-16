from pymavlink import mavutil

class Connection:
    def __init__(self,connection_string,baud=57600):
        try:
            self.connection_string = connection_string

            connection = mavutil.mavlink_connection(self.connection_string,baud=baud)

            connection.wait_heartbeat()

            self.system_id = connection.target_system
            self.component_id = connection.target_component

            print(f"Target System:  {self.system_id} , Target Component: {self.component_id}")
        except Exception as e:
            print("Connection Error : ",e)
            
     
if "__name__" == "__main__":
    drone_connection = Connection('/dev/ttyUSB0')
