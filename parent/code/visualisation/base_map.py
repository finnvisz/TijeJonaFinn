from parent.code.classes.railnl import RailNL 
from parent.code.classes.station_class import Station

from manim import Text, Line, Dot, VGroup, LEFT, UP, MovingCameraScene
from typing import Tuple

class BaseScene(MovingCameraScene):
    """A class creating dots, lines and labels from RailNL load."""

    # Setup VGroups, dictionaries and camera
    def setup(self) -> None:

        # Get railwaynetwork data 
        self.data: "RailNL" = RailNL("Holland") 
        self.name_station_dict: dict[str, Station] = self.data.stations_dict()

        # Create VGroups 
        self.create_dots()
        self.create_dot_labels()
        self.create_connections()
        self.create_connection_labels()

        # Set camera to capture network
        self.setup_camera()

    # Move camera to capture network
    def setup_camera(self):
        self.camera.frame.move_to(self.dots)
        self.camera.frame.set_height(1.1 * self.dots.get_height())
        
    def create_dots(self) -> None:

        # VGroup and dictionaries to load into
        self.dots = VGroup()
        self.station_dot_dict: dict[Station, Dot] = {}
        self.dot_location_dict: dict[Dot, list] = {}

        # Create dot for each station
        for station in self.name_station_dict.values():

            # Create dot at station position
            lat, long = station.location()
            position = lat * LEFT + long * UP
            dot = Dot(point = position, radius = 0.0075)

            # Add dots to relevant dictionaries and VGroup
            self.station_dot_dict[station] = dot
            self.dot_location_dict[dot] = position
            self.dots.add(dot)

    def create_dot_labels(self) -> None:

        # VGroup and dictionaries to load into
        self.dot_labels = VGroup()
        self.dot_labels_dict: dict[Dot, Text] = {}

        # Create label from station name
        for name, station in self.name_station_dict.items():
            dot = self.station_dot_dict[station]
            label = Text(f"{name}").move_to(dot)
            label.scale(0.03)

            # Add label to VGroup and dictionary
            self.dot_labels_dict[dot] = label
            self.dot_labels.add(label)

    def create_connections(self) -> None:
    
        # VGroup and dictionaries to load into
        self.connections = VGroup()
        self.connection_line_dict: dict[Tuple[Dot, Dot], Line] = {}

        # For each station find associated dot and assosiated connection dot
        for station, dot_start in self.station_dot_dict.items():
            for connecting, time in station.connections_dict().items():

                # Find connecting station dot
                dot_end = self.station_dot_dict[connecting]

                # Check if connection is not already made
                if not (dot_end, dot_start, time) in self.connection_line_dict:

                    # If not construct connection line
                    s = dot_start.get_center()
                    e = dot_end.get_center()
                    line = Line(start = s, end = e, stroke_width = 0.75)

                    # Add connection to dictionary and VGroup 
                    tuple = (dot_start, dot_end, time)
                    self.connection_line_dict[tuple] = line
                    self.connections.add(line)

    def create_connection_labels(self) -> VGroup:

        # Create VGroup and dictionaries to load into
        self.connection_labels = VGroup()
        self.connection_label_dict: dict[Line, Text] = {}

        # Iterate over all created connection lines
        for tuple, line in self.connection_line_dict.items():

            # Create time label
            time = tuple[2]
            label = Text(f"{time}")
            label.scale(0.02)

            # Place label perpendicular to line for readability
            label.move_to(line.get_center())
            direction = line.get_unit_vector()
            new_direction = direction[0] * UP + direction[1] * LEFT
            label.shift(-new_direction * 0.015)

            # Add connection to VGroup and dictionary
            self.connection_labels.add(label)
            self.connection_label_dict[tuple] = label