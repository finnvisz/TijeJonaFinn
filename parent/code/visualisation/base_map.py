from parent.code.classes.railnl import RailNL 
from parent.code.classes.station_class import Station
from manim import Text, Line, Dot, VGroup, LEFT, UP
from typing import Tuple
from numpy import ndarray

class Map():

    # Setup VGroups, dictionaries and camera
    def __init__(self) -> None:
        super().__init__()

        # Get railwaynetwork data 
        railnl: "RailNL" = RailNL("Holland") 
        self.name_station_dict: dict[str, Station] = railnl.stations_dict()

        # Create VGroups 
        self.create_dots()
        self.create_dot_labels()
        self.create_connections()
        self.create_connection_labels()
        
    def create_dots(self) -> None:

        # VGroup and dictionaries to load into
        self.station_dots = VGroup()
        self.station_dot_dict: dict[Station, Dot] = {}
        self.dot_location_dict: dict[Dot, ndarray] = {}

        # Create dot for each station
        for station in self.name_station_dict.values():

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
        self.dot_connections = VGroup()
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
                    line = Line(start = s, end = e, stroke_width = 0.5)

                    # Add connection to dictionary and VGroup 
                    tuple = (dot_start, dot_end, time)
                    self.connection_line_dict[tuple] = line
                    self.dot_connections.add(line)

    def create_connection_labels(self) -> VGroup:

        # Create VGroup and dictionaries to load into
        self.connection_labels = VGroup()
        self.connection_label_dict: dict[Line, Text] = {}

        # Iterate over all created connection lines
        for tuple, line in self.connection_line_dict.items():

            # Create time label
            time = tuple[2]
            label = Text(f"{time}")
            label.scale(0.025)

            # Place label perpendicular to line for readability
            label.move_to(line.get_center())
            direction = line.get_unit_vector()
            new_direction = direction[0] * UP + direction[1] * LEFT
            label.shift(-new_direction * 0.015)

            # Add connection to VGroup and dictionary
            self.connection_labels.add(label)
            self.connection_label_dict[tuple] = label

    def give_dots(self) -> VGroup:
        return self.station_dots
    
    def give_dot_labels(self) -> VGroup:
        return self.dot_labels
    
    def give_connections(self) -> VGroup:
        return self.dot_connections
    
    def give_connection_labels(self) -> VGroup:
        return self.connection_labels