from manim import MovingCameraScene, Dot, VGroup, LEFT, UP, Text, Line, FadeIn, Transform
from parent.code.classes.railnl import RailNL 
from parent.code.classes.station_class import Station

class Map(MovingCameraScene):

    # Obtain station name object dictionary via load class
    def setup(self) -> None:
        load: "RailNL" = RailNL("Holland")

        self.station_name_dict: dict[str, Station] = load.stations_dictionary()
        self.station_dot_dict: dict[Station, Dot] = {}
        self.dot_location_dict: dict[Dot, list] = {}
        self.traject_line_dict: dict[list[Station, Station, int], Line] = {}

        self.points = self.create_points()
        self.labels = self.create_labels()
        self.connections = self.create_connections()

        self.set_camera()
        
    # Create points VGroup
    def create_points(self) -> VGroup:
        self.station_points = VGroup()

        # Create dot from station object location 
        for station in self.station_name_dict.values():
            lat, long = station.location()
            position = lat * LEFT + long * UP
            dot = Dot(point = position, radius = 0.01)

            # Add dots to relevant dictionaries and VGroup
            self.station_dot_dict[station] = dot
            self.dot_location_dict[dot] = position
            self.station_points.add(dot)

        return self.station_points

    # Create label VGroup
    def create_labels(self) -> VGroup:
        self.station_labels = VGroup()

        # Create label from station name
        for name, station in self.station_name_dict.items():
            dot = self.station_dot_dict[station]
            label = Text(f"{name}").move_to(dot)
            label.scale(0.03)

            # Add label to VGroup
            self.station_labels.add(label)

        return self.station_labels

    # Create connections VGroup
    def create_connections(self) -> VGroup:
        self.station_connections = VGroup()

        # For each station find associated dot and assosiated connection dot
        for station, dot_s in self.station_dot_dict.items():
            for connecting, time in station.connecting_stations().items():
                dot_e = self.station_dot_dict[connecting]
                s = dot_s.get_center()
                e = dot_e.get_center()
                line = Line(start = s, end = e, stroke_width = 0.5)

                # Add connection to dictionary and VGroup
                self.traject_line_dict[station, connecting, time] = line
                self.station_connections.add(line)

        return self.station_connections

    # Place camera appropriately
    def set_camera(self):
        self.camera.frame.move_to(self.points)
        self.camera.frame.set_height(1.1 * self.points.height)

    # Play scene showing labels, points and connections
    def construct(self):
    
        # Fade labels in, transform into points
        self.play(FadeIn(self.labels), run_time = 2)
        self.play(Transform(self.labels, self.points), run_time = 2)
        self.play(FadeIn(self.connections), run_time = 2)
        self.wait(2)