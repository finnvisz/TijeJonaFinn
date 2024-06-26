from parent.code.classes.railnl import RailNL 
from parent.code.classes.station_class import Station

from typing import Tuple
from manim import MovingCameraScene

import manim as m
import csv as c

class BaseScene(MovingCameraScene):
    """
    A manim Scene creating and displaying several objects formed from 
    Holland or National train network.

    Attributes
    ---------
    data: Instance of RailNL load class given specific 
          settings obtained from visualisation_settings.csv
    map: Map to create, either Holland or Nationaal.
    filepath: Relative path to list of route objects to visualise.
    radius: Radius of dot objects meant to visualise stations.
    label_scale: Size of station-name, connection-time and map labels.
    line_width: Thickness of connection lines.
    zoom_scale: Camera zoom factor.
    dots: Manim VGroup of dot objects
    station_dot_dict: Association between station objects and dots.
    dot_location_dict: Association between dot objects and locations.
    dot_labels: Manim VGroup of station name dot labels.
    dot_labels_dict: Association between dot objects and their labels.
    connections: Manim VGroup of lines.
    connection_line_dict: Association between two dots in connection and line object.
    connection_labels: Manim VGroup of connection time labels.
    connection_labels_dict: Association between connections and time labels.

    Methods
    --------
    setup: Defacto initializer. Called upon by MovingCameraScene.__init__().
    setup_camera: Places camera appropriately.
    create_dots: Creates dot objects to represent stations.
    create_connections: Creates line objects to represent connections.
    create_dot_labels: Creates name labels for dot objects.
    create_connection_labels: Creates time labels for line objects.
    construct: Main method called upon by MovingCameraScene.__init__().

    Usage
    ----
    NOTE: Always check visualisation_settings.csv.
    Use VScode manim sideview extension.
    Alternatively run: manim -pql map_visualisation.py BaseScene.
    Running should return a video showing Holland or Nationaal visualisation
    dependend on visualisation_settings.csv.
    """

    def setup(self) -> None:
        """
        Defacto initializer called upon by MovingCameraScene.__init__().

        Pre
        ---
        Reads from visualisation_settings.csv. A csv file containing:
            "map","relative path to routes to visualise csv format".

        Post
        ---
        Instantiates all class attributes by calling upon methods.
        """

        # Get visualisation settings
        with open('visualisation_settings.csv', newline = '') as file:
            csvreader = c.reader(file, delimiter = ',')
            body = next(csvreader)

            # Map to visualize
            self.map = body[0]

            # Relative path to list of route objects to visualise 
            self.filepath = body[1]

        # Get railwaynetwork data 
        self.data: "RailNL" = RailNL(self.map)
        self.name_station_dict: dict[str, Station] = self.data.stations_dict()

        # Set scales for different maps
        if self.map == "Holland":
            self.radius = 0.0075
            self.label_scale = 0.04
            self.line_width = 0.7
            self.time_label_shift = 0.015
            self.zoom_scale = 1.1

        elif self.map == "Nationaal":
            self.radius = 0.015
            self.label_scale = 0.07
            self.line_width = 1.2
            self.time_label_shift = 0.03
            self.zoom_scale = 0.8

        else:
            raise ValueError("Map in visualisation_settings.csv must be Holland or Nationaal.")

        # Create VGroups 
        self.create_dots()
        self.create_dot_labels()
        self.create_connections()
        self.create_connection_labels()

        # Set camera to capture network
        self.setup_camera()

    def setup_camera(self):
        """
        Places camera appropriately.

        Post
        ---
        Places and zooms camera depending on instantiated dots attribute.
        
        """

        self.camera.frame.move_to(self.dots)

        # Find minimum dimension to not stretch
        zoom = max(self.dots.get_height(), self.dots.get_width())
        self.camera.frame.set_height(self.zoom_scale * zoom)
        
    def create_dots(self) -> None:
        """
        Creates dot objects to represent stations.

        Post
        ---
        Creates dots, station_dot_dict and dot_location_dict.
        """

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
        """
        Creates name labels for dot objects.

        Post
        ---
        Creates dot_labels and dot_labels_dict.
        """

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
        """
        Creates line objects to represent connections.

        Post
        ---
        Creates connections and connection_line_dict.
        """
    
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
        """
        Creates time labels for line objects.

        Post
        ---
        Creates connection_labels and connection_label_dict.
        """

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

    # Play scene showing labels, points and connections
    def construct(self):
        """
        Main method called upon by MovingCameraScene.__init__().

        Pre
        ---
        dot_labels, dots, connections and connection_labels need to be 
        instantiated.

        Post
        ---
        Creates visualisation of complete Holland/Nationaal train network.
        """

        self.play(m.FadeIn(self.dot_labels), run_time = 2)
        self.play(m.Transform(self.dot_labels, self.dots), run_time = 2)
        self.play(m.FadeIn(self.connections), run_time = 2)
        self.play(m.FadeIn(self.connection_labels), run_time = 2)
        self.wait(2)