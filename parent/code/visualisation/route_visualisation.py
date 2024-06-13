from manim import MovingCameraScene, ApplyMethod, Line, manim_colors, Dot
from manim import PURE_RED, PURE_GREEN, PURE_BLUE
from manim import YELLOW, PURPLE, ORANGE, PINK
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.random_algorithm import RandomAlgorithm
from base_map import Map

class route_visualisation(MovingCameraScene):
    """Show trainroutes on map."""

    def setup(self):
        self.setup_map()
        self.setup_camera()
        self.run_algorithm()

        self.line_colors_dict: dict[Line, list] = {}
        self.colors = [PURE_RED, PURE_GREEN, 
                       PURE_BLUE, YELLOW, 
                       PURPLE, ORANGE, PINK]
        
    # Get all relevant objects from base_map
    def setup_map(self):
        self.map = Map()
        self.dots = self.map.give_dots()
        self.dot_labels = self.map.give_dot_labels()
        self.connections = self.map.give_connections()
        self.connection_labels = self.map.give_connection_labels()

    # Move camera to capture network
    def setup_camera(self):
        self.camera.frame.move_to(self.dots)
        self.camera.frame.set_height(1.1 * self.dots.get_height())

    # Make train to ride tracks
    def setup_train(self, dot_start: Dot):
        self.train = Dot(point = dot_start.get_center(), radius = 0.0075)

    # Run algorithm here
    def run_algorithm(self):
        data = RailNL("Holland")
        algorithm = RandomAlgorithm(data) # HERE
        algorithm.run()
        self.dienstregeling = algorithm.output()

    def color_route(self, route: list, color: manim_colors):

        # Get station dot conversion dictionaries
        name_station_dict = self.map.give_name_station_dict()
        station_dot_dict = self.map.give_station_dot_dict()
        connection_line_dict = self.map.give_connection_line_dict()

        start_route = 0
        for connection in route:
            time = connection[2]

            # Find corresponding station object 
            station_start = name_station_dict[connection[0]]
            station_end = name_station_dict[connection[1]]

            # Find corresponding dot object
            dot_start = station_dot_dict[station_start]
            dot_end = station_dot_dict[station_end]

            if start_route == 0:
                self.setup_train(dot_start)
                start_route += 1

            # Check if connection tuple exists
            tuple = (dot_start, dot_end, time)
            if tuple in connection_line_dict:
                line = connection_line_dict[tuple]
            
            # Otherwise search reversed connection
            else:
                tuple = (dot_end, dot_start, time)
                line = connection_line_dict[tuple]
            
            self.set_color(line, color)
            shift = self.train.animate.move_to(dot_end.get_center())
            self.play(shift, run_time = 0.5)

    # Set color depending on if already colored.
    def set_color(self, line: Line, color: manim_colors):

        if not line in self.line_colors_dict:

            # If line not yet colored just color
            self.play(ApplyMethod(line.set_color, color), run_time = 0.1)
            self.line_colors_dict[line] = [color]

        else:

            # If line already has given color do nothing
            if color in self.line_colors_dict[line]:
                pass

            else: 
                # Otherwise update line gradient
                colors = self.line_colors_dict[line]
                colors.append(color)
                self.play(ApplyMethod(line.set_color, colors), run_time = 0.1)

    def construct(self):

        self.add(self.dots, self.connections, self.connection_labels)
        self.wait(2)

        for count in range(7):
            route_object = self.dienstregeling[count]
            route = route_object.connections()
            self.color_route(route, self.colors[count])

        self.wait(2)