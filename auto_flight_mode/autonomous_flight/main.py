from mavlink_messenger import MavLinkMessenger
import time 
def main():
    connection_string = "/dev/ttyUSB0"
    connect = MavLinkMessenger(connection_string)
    if connect == True:
        print("Arming the Copter")
        connect.arm()
        time.sleep(20)
        print("Disarming the copter")
        connect.disarm()
    else:
        print("Error In Arming")

