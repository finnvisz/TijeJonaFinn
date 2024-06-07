from manim import *
from railnl import RailNL 

class Map(MovingCameraScene):

    # Obtain station name object dictionary via Railnl class
    def setup(self):
        load = RailNL("Holland")
        self.station_dictionary = load.stations_dictionary()
        self.dot_dictionary = {}

    # Instantiate points and labels to appear
    def create_points_labels(self):
        self.station_points = VGroup()
        self.station_labels = VGroup()

        # Iterate over station name, object tuples in dictionary
        for name, object in self.station_dictionary.items():

            # Create dot from station object location 
            lat, long = object.location()
            position = lat * LEFT + long * UP
            dot = Dot(point = position, radius = 0.008)

            # Add station dot pair to dict
            self.dot_dictionary[object] = dot

            # Create label from station name 
            label = Text(f"{name}").move_to(dot)
            label.scale(0.03)

            # Add point and label to VGroups
            self.station_points.add(dot)
            self.station_labels.add(label)

    def create_connections(self):
        self.station_connections = VGroup()
        for station, dot_start in self.dot_dictionary.items():
            for connecting in station.connecting_stations():
                dot_end = self.dot_dictionary[connecting]
                line = Line(start = dot_start.get_center(), end = dot_end.get_center(), stroke_width = 0.25)
                self.station_connections.add(line)

    def construct(self):
    
        self.create_points_labels()
        self.create_connections()

        # Set camera to instantiated points and labels
        self.camera.frame.move_to(self.station_points)
        self.camera.frame.set_height(1.25 * self.station_points.height)
    
        # Fade labels in, transform into points
        self.play(FadeIn(self.station_labels), run_time = 2)
        self.play(Transform(self.station_labels, self.station_points), run_time = 2)
        self.play(FadeIn(self.station_connections), run_time = 2)
        self.wait(2)