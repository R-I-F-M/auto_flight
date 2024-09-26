from drone_auto_connect import DroneAutoConnect
from drone_actions import DroneActions

if __name__ == "__main__":
    # Instantiate the DroneAutoConnect class
    drone_connect = DroneAutoConnect()

    # Automatically connect to Pixhawks (multiple drones)
    drone_connect.auto_connect()

    # Instantiate DroneActions with the connected drones
    drone_actions = DroneActions(drone_connect)

    # Loop through all connected drones and perform actions
    for drone in drone_connect.drones:
        system_id = drone['system_id']
        
        # Arm the drone
        drone_actions.arm_drone(system_id)

        # Check battery status
        drone_actions.check_battery_status(system_id)

        # Disarm the drone
        drone_actions.disarm_drone(system_id)