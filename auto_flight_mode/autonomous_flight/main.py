from kml_parser import KMLParser
import sys

def main():
    file_path = "C:\\MyWorkSpace\\RIFM_Autonomous_Flight_Control\\autonomous_flight_system\\auto_flight_mode\\cosmosVDC.kml"

    kml_parser = KMLParser(file_path)
    waypoints = kml_parser.parse()

    for wp in waypoints:
        print(wp)
        sys.stdout.flush()  # Print each waypoint

if __name__ == "__main__":
    main()




