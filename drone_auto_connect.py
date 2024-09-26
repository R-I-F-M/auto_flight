import serial.tools.list_ports
from pymavlink import mavutil

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
                master = mavutil.mavlink_connection(port, baud=baudrate)
                # Wait for the heartbeat message to confirm connection
                master.wait_heartbeat(timeout=10)
                print(f"Connected to Pixhawk on {port}")

                # Retrieve system and component IDs
                system_id = master.target_system
                component_id = master.target_component
                print(f"System ID: {system_id}, Component ID: {component_id}")

                # Store this drone's connection and system details in the list
                self.drones.append({
                    'master': master,
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

    def is_connected(self, system_id):
        """
        Check if the drone with the given system_id is still connected by checking the heartbeat.
        """
        drone = next((d for d in self.drones if d['system_id'] == system_id), None)
        if drone:
            try:
                drone['master'].wait_heartbeat(timeout=5)
                print(f"Heartbeat received from drone with System ID: {system_id}. Drone is still connected.")
                return True
            except:
                print(f"No heartbeat received from drone with System ID: {system_id}. Drone disconnected.")
                self.drones.remove(drone)  # Remove disconnected drone
                return False
        return False

    def get_drone(self, system_id):
        """
        Return the drone object with the given system_id from the drones list.
        """
        return next((d for d in self.drones if d['system_id'] == system_id), None)
