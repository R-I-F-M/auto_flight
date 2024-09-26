from drone_auto_connect import DroneAutoConnect
from pymavlink import mavutil

class DroneActions:
    def __init__(self, drone_connection):
        self.drone_connection = drone_connection

    def arm_drone(self, system_id):
        """
        Arm the drone with the given system_id.
        """
        drone = self.drone_connection.get_drone(system_id)
        if drone and self.drone_connection.is_connected(system_id):
            print(f"Arming drone with System ID: {system_id}...")
            drone['master'].mav.command_long_send(
                drone['system_id'],
                drone['component_id'],
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0, 1, 0, 0, 0, 0, 0, 0
            )
            print(f"Drone {system_id} armed.")
        else:
            print(f"Drone {system_id} is not connected or not found. Unable to arm.")

    def disarm_drone(self, system_id):
        """
        Disarm the drone with the given system_id.
        """
        drone = self.drone_connection.get_drone(system_id)
        if drone and self.drone_connection.is_connected(system_id):
            print(f"Disarming drone with System ID: {system_id}...")
            drone['master'].mav.command_long_send(
                drone['system_id'],
                drone['component_id'],
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0, 0, 0, 0, 0, 0, 0, 0
            )
            print(f"Drone {system_id} disarmed.")
        else:
            print(f"Drone {system_id} is not connected or not found. Unable to disarm.")

    def check_battery_status(self, system_id):
        """
        Check the battery status of the drone with the given system_id.
        """
        drone = self.drone_connection.get_drone(system_id)
        if drone and self.drone_connection.is_connected(system_id):
            battery_msg = drone['master'].recv_match(type='BATTERY_STATUS', blocking=True, timeout=5)
            if battery_msg:
                print(f"Drone {system_id} battery voltage: {battery_msg.voltages[0] / 1000.0}V")
            else:
                print(f"Failed to receive battery status for drone {system_id}.")
        else:
            print(f"Drone {system_id} is not connected or not found. Unable to check battery status.")
