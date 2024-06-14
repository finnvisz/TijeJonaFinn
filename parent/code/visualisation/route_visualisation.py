from manim import ApplyMethod, Line, Transform, Dot, VGroup, manim_colors
from manim import PURE_RED, PURE_GREEN, PURE_BLUE
from manim import YELLOW, PURPLE, ORANGE, PINK

from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.greedy import Greedy

from base_map import BaseMapScene
from numpy.linalg import norm

class route_visualisation(BaseMapScene):
    """Show trainroutes on map."""

    def setup_2(self):

        # Run a specific algorithm
        self.run_algorithm()

        # Create dictionary to save colors used on lines
        self.line_colors_dict: dict[Line, list] = {}
        self.colors = [PURE_RED, PURE_GREEN, 
                       PURE_BLUE, YELLOW, 
                       PURPLE, ORANGE, PINK]

    # Move camera to capture network
    def setup_camera(self):
        self.camera.frame.move_to(self.dots)
        self.camera.frame.set_height(1.1 * self.dots.get_height())

    # Make train to ride tracks
    def setup_train(self, dot_start: Dot):
        self.train = Dot(point = dot_start.get_center(), radius = 0.0075)

    # Run algorithm here
    def run_algorithm(self):
        self.output = Greedy(self.data).run() # HERE

    def color_route(self, route: list, color: manim_colors):

        start_route = 0
        for connection in route:
            time = connection[2]

            # Find corresponding station object 
            station_start = self.name_station_dict[connection[0]]
            station_end = self.name_station_dict[connection[1]]

            # Find corresponding dot object
            dot_start = self.station_dot_dict[station_start]
            dot_end = self.station_dot_dict[station_end]

            # Place train at start of new route
            if start_route == 0:
                self.setup_train(dot_start)
                start_route += 1

            # Check if connection tuple exists
            tuple = (dot_start, dot_end, time)
            if tuple in self.connection_line_dict:
                line = self.connection_line_dict[tuple]
            
            # Otherwise reversed connection must exist
            else:
                tuple = (dot_end, dot_start, time)
                line = self.connection_line_dict[tuple]

            # Set color of line, move train
            self.set_color(line, color)
            shift = self.train.animate.move_to(dot_end.get_center())
            self.play(shift, run_time = 0.5)

    # Set color depending on if already colored
    def set_color(self, line: Line, color: manim_colors):

        # If line not yet colored just color
        if not line in self.line_colors_dict:
            self.play(ApplyMethod(line.set_color, color), run_time = 0.1)
            self.line_colors_dict[line] = [color]

        else:
            # If line already has given color do nothing
            if color in self.line_colors_dict[line]:
                pass

            # Otherwise update line gradient
            else: 
                colors = self.line_colors_dict[line]
                colors.append(color)
                self.set_multiple_colors(line, colors)

    # Set line with multiple colors 
    def set_multiple_colors(self, line: Line, colors: list):

        # Find start and end brutally
        starting_point = line.start
        ending_point = line.end

        # Get direction and length 
        length = norm(ending_point - starting_point)
        direction = (ending_point - starting_point) / length

        # Get length of each segment
        amount = len(colors)
        segment_length = length / amount

        # Create new line VGroup to replace old
        new_line = VGroup()

        # Create new line consisting of segments
        for i in range(amount):

            # Create ending of segment
            ending_point = starting_point + direction * segment_length

            # Create new segment linepiece
            segment = Line(start = starting_point, end = ending_point, 
                           color = colors[i], stroke_width = 0.75)

            # Add segment and set ending point as new starting
            new_line.add(segment)
            starting_point = ending_point

        # Transformeer oude lijn naar nieuw gesegmenteerde lijn
        self.play(Transform(line, new_line), run_time = 0.1)

    def construct(self):

        self.setup_2()
        self.add(self.dots, self.connections, self.connection_labels)
        self.wait(2)

        # Using seven routes
        for i in range(7):

            # Iterate over route_objects in output
            route_object = self.output[i]

            # Get connections within route_object
            route = route_object.get_connections_used()

            # Color route with ith color
            self.color_route(route, self.colors[i])

        self.wait(2)