from pykml import parser

class KMLParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        with open(self.file_path, 'rb') as f:
            root = parser.parse(f).getroot()

        waypoints = []

        for placemark in root.Document.Folder.Placemark:
            name = None
            if hasattr(placemark, 'name'):
                name = str(placemark.name)

            coords_str = str(placemark.Point.coordinates).strip()
            coords = [float(c) for c in coords_str.split(',')]

            waypoint = {
                'latitude': coords[1],
                'longitude': coords[0],
                'altitude': coords[2] if len(coords) > 2 else 0
            }
            waypoints.append(waypoint)

        return waypoints if waypoints else []  # Return empty list if no waypoints found
