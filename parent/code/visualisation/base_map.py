from parent.code.classes.railnl import RailNL 
from parent.code.classes.station_class import Station

from typing import Tuple

import manim as m
import argparse as ap

class BaseScene(m.MovingCameraScene):
    """A class creating dots, lines and labels from RailNL load."""

    # Setup VGroups, dictionaries and camera
    def setup(self) -> None:

        # SET MAP TO VISUALIZE HERE
        self.map = "Nationaal"

        # Set scales for different maps
        if self.map == "Holland":
            self.radius = 0.0075
            self.label_scale = 0.04
            self.line_width = 0.7
            self.time_label_shift = 0.015
            self.zoom_scale = 1.1

        # Get railwaynetwork data 
        self.data: "RailNL" = RailNL(self.map)
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

        # Find minimum dimension to not stretch
        zoom = max(self.dots.get_height(), self.dots.get_width())
        self.camera.frame.set_height(self.zoom_scale * zoom)
        
    def create_dots(self) -> None:

        # VGroup and dictionaries to load into
        self.dots = m.VGroup()
        self.station_dot_dict: dict[Station, m.Dot] = {}
        self.dot_location_dict: dict[m.Dot, list] = {}

        # Create dot for each station
        for station in self.name_station_dict.values():

            # Create dot at station position
            long, lat = station.location()
            position = lat * -m.LEFT + long * m.UP
            dot = m.Dot(point = position, radius = self.radius)

            # Add dots to relevant dictionaries and VGroup
            self.station_dot_dict[station] = dot
            self.dot_location_dict[dot] = position
            self.dots.add(dot)

    def create_dot_labels(self) -> None:

        # VGroup and dictionaries to load into
        self.dot_labels = m.VGroup()
        self.dot_labels_dict: dict[m.Dot, m.Text] = {}

        # Create label from station name
        for name, station in self.name_station_dict.items():
            dot = self.station_dot_dict[station]
            label = m.Text(f"{name}").move_to(dot)
            label.scale(self.label_scale)

            # Add label to VGroup and dictionary
            self.dot_labels_dict[dot] = label
            self.dot_labels.add(label)

    def create_connections(self) -> None:
    
        # VGroup and dictionaries to load into
        self.connections = m.VGroup()
        self.connection_line_dict: dict[Tuple[m.Dot], m.Line] = {}

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
                    line = m.Line(start = s, end = e, stroke_width = self.line_width)

                    # Add connection to dictionary and VGroup 
                    tuple = (dot_start, dot_end, time)
                    self.connection_line_dict[tuple] = line
                    self.connections.add(line)

    def create_connection_labels(self) -> m.VGroup:

        # Create VGroup and dictionaries to load into
        self.connection_labels = m.VGroup()
        self.connection_label_dict: dict[m.Line, m.Text] = {}

        # Iterate over all created connection lines
        for tuple, line in self.connection_line_dict.items():

            # Create time label
            time = tuple[2]
            label = m.Text(f"{time}")
            label.scale(self.label_scale)

            # Place label perpendicular to line for readability
            label.move_to(line.get_center())
            direction = line.get_unit_vector()
            new_direction = direction[0] * m.UP + direction[1] * m.LEFT
            label.shift(-new_direction * self.time_label_shift)

            # Add connection to VGroup and dictionary
            self.connection_labels.add(label)
            self.connection_label_dict[tuple] = label