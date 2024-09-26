"""
Single Drone: Yes, the code can connect to a single drone by scanning available ports and establishing a connection to one Pixhawk.
Multiple Drones: Yes, the code supports connecting to multiple drones by scanning all available ports and attempting to establish a connection for each detected Pixhawk.
"""

import serial.tools.list_ports
from pymavlink import mavutil
import time

class DroneAutoConnect:
    def __init__(self):
        # List to hold connected drones' information (each item is a dict)
        self.drones = []

    def find_serial_ports(self):
        """ 
        Find all available serial ports on the system.
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def auto_connect(self, baudrate=57600):
        """
        Automatically scan all available serial ports and attempt to connect to Pixhawks (multiple drones).
        """
        available_ports = self.find_serial_ports()

        for port in available_ports:
            print(f"Trying to connect to port: {port}")
            try:
                # Attempt to connect to Pixhawk on the given port
                self.master = mavutil.mavlink_connection(port, baud=baudrate)
                # Wait for the heartbeat message to confirm connection
                heartbeat = self.master.wait_heartbeat(timeout=10)
                print(f"Pixhawk Heartbeat {heartbeat}")
                print(f"Connected to Pixhawk on {port}")

                # Retrieve system and component IDs
                system_id = self.master.target_system
                component_id = self.master.target_component
                print(f"System ID: {system_id}, Component ID: {component_id}")

                # Store this drone's connection and system details in the list
                self.drones.append({
                    'master': self.master,
                    'system_id': system_id,
                    'component_id': component_id,
                    'port': port
                })

            except Exception as e:
                print(f"Failed to connect on {port}: {e}")

        if not self.drones:
            print("No drones connected.")
        else:
            print(f"Total drones connected: {len(self.drones)}")

    def request_autopilot_capabilities(self, system_id):
        """
        Request autopilot capabilities for the specific drone identified by system_id.
        """
        drone = next((d for d in self.drones if d['system_id'] == system_id), None)

        if drone:
            try:
                print(f"Requesting capabilities for drone with System ID: {system_id}")

                # Send the request for autopilot capabilities
                drone['master'].mav.command_long_send(
                    drone['system_id'],
                    drone['component_id'],
                    mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,
                    0, 1, 0, 0, 0, 0, 0, 0
                )

                # Wait for the autopilot version response
                message = drone['master'].recv_match(type='AUTOPILOT_VERSION', blocking=True, timeout=5)
                if message:
                    print(f"Drone (System ID: {system_id}) firmware version: {message.flight_sw_version}")
                else:
                    print(f"No autopilot version received for drone with System ID: {system_id}.")
            except Exception as e:
                print(f"Error while requesting capabilities for drone {system_id}: {e}")
        else:
            print(f"Drone with System ID {system_id} not found.")

    def send_command_to_all_drones(self):
        """
        Example function to send a command to all connected drones.
        """
        for drone in self.drones:
            system_id = drone['system_id']
            component_id = drone['component_id']
            print(f"Sending command to drone with System ID: {system_id}")

            # Example: Sending a command to all drones to request capabilities
            self.request_autopilot_capabilities(system_id)

    def BatteryStatus(self):
            if self.master.heartbeat()
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

# Example usage
if __name__ == "__main__":
    drone_connect = DroneAutoConnect()

    # Automatically connect to all drones on available ports
    drone_connect.auto_connect()
    # Send command to request capabilities for all drones
    drone_connect.send_command_to_all_drones()



