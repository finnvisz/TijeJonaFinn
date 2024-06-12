from parent.code.classes.railnl import RailNL 
from parent.code.classes.station_class import Station
from manim import Camera, Text, Line, Dot, VGroup, LEFT, UP
from typing import Tuple
from numpy import ndarray

class Map(Camera):

    # Setup VGroups, dictionaries and camera
    def setup(self) -> None:

        # Get railwaynetwork data 
        railnl:             "RailNL" = RailNL("Holland") 
        self.name_station:  dict[str, Station] = railnl.stations_dictionary()

        # Create VGroups 
        self.create_dots()
        self.create_dot_labels()
        self.create_dot_connections()
        self.create_dot_connection_labels()

        # Set camera to capture created network
        self.set_camera()
        
    def create_dots(self) -> None:

        # VGroup and dictionaries to load into
        self.station_dots = VGroup()
        self.station_dot_dict: dict[Station, Dot] = {}
        self.dot_location_dict: dict[Dot, ndarray] = {}

        # Create dot for each station
        for station in self.name_station.values():

            # Create dot at station position
            lat, long = station.location()
            position = lat * LEFT + long * UP
            dot = Dot(point = position, radius = 0.0075)

            # Add dots to relevant dictionaries and VGroup
            self.station_dot_dict[station] = dot
            self.dot_location_dict[dot] = position
            self.station_dots.add(dot)

    def create_dot_labels(self) -> None:

        # VGroup and dictionaries to load into
        self.station_labels = VGroup()
        self.dot_labels_dict: dict[Dot, Text]

        # Create label from station name
        for name, station in self.station_name_dict.items():
            dot = self.station_dot_dict[station]
            label = Text(f"{name}").move_to(dot)
            label.scale(0.03)

            # Add label to VGroup
            self.dot_labels_dict[dot] = label
            self.station_labels.add(label)

    def create_dot_connections(self) -> None:
    
        # VGroup and dictionaries to load into
        self.station_connections = VGroup()
        self.connection_line:   dict[Tuple[Station, Station, str], Line] = {}

        # For each station find associated dot and assosiated connection dot
        for station, dot_s in self.station_dot_dict.items():
            for connecting, time in station.connecting_stations().items():
                
                # Check if connection is not already made
                if not (connecting, station, time) in self.route_line_dict:
                    dot_e = self.station_dot_dict[connecting]
                    s = dot_s.get_center()
                    e = dot_e.get_center()
                    line = Line(start = s, end = e, stroke_width = 0.5)

                    # Add connection to dictionary and VGroup 
                    tuple = (station, connecting, time)
                    self.route_line_dict[tuple] = line
                    self.station_connections.add(line)

    def create_dot_connection_labels(self) -> VGroup:

        # Create VGroup and dictionaries to load into
        self.connection_labels = VGroup()
        self.connection_label:  dict[Line, Text] = {}

        for tuple, line in self.route_line_dict.items():
            time = tuple[2]
            label = Text(f"{time}")
            label.scale(0.025)

            # Shift label perpendicular to line for readability
            label.move_to(line.get_center())
            direction = line.get_unit_vector()
            new_direction = direction[0] * UP + direction[1] * LEFT
            label.shift(-new_direction * 0.015)

            self.connection_labels.add(label)

    def set_camera(self):
        self.camera.frame.move_to(self.points)
        self.camera.frame.set_height(1.1 * self.points.height)