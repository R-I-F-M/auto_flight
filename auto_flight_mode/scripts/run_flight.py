# import sys
# import os

# # Add the parent directory to sys.path
# current_dir = os.path.dirname(__file__)
# project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
# sys.path.append(project_root)

# # Import KMLParser from autonomous_flight.kml_parser
# from autonomous_flight.kml_parser import KMLParser

# def main():
#     file_path = "C:\\MyWorkSpace\\RIFM_Autonomous_Flight_Control\\autonomous_flight_system\\auto_flight_mode\\cosmosVDC.kml"

#     kml_parser = KMLParser(file_path)
#     waypoints = kml_parser.parse()

#     for wp in waypoints:
#         print(wp)
#         sys.stdout.flush()  # Print each waypoint

# if __name__ == "__main__":
#     main()

import sys
import os

# Get the directory of the current script (run_flight.py)
current_dir = os.path.dirname(__file__)

# Navigate up one directory to auto_flight_mode/
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

# Add auto_flight_mode/ to the sys.path
sys.path.append(project_root)

# Now import KMLParser from autonomous_flight.kml_parser
from autonomous_flight.kml_parser import KMLParser

def main():
    file_path = os.path.join(project_root, 'autonomous_flight', 'cosmosVDC.kml')

    kml_parser = KMLParser(file_path)
    waypoints = kml_parser.parse()

    for wp in waypoints:
        print(wp)
        sys.stdout.flush()  # Print each waypoint

if __name__ == "__main__":
    main()
