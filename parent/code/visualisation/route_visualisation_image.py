from manim import Line, Dot, VGroup, manim_colors, Text, UP, LEFT

from manim import PURE_RED, PURE_GREEN, PURE_BLUE
from manim import YELLOW, PURPLE, ORANGE, PINK

from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.greedy import Greedy

from base_map import BaseScene
from numpy.linalg import norm

class route_visualisation_image(BaseScene):
    """Show trainroutes on map."""

    def setup_2(self) -> None:

        # Run a specific algorithm
        self.run_algorithm()

        # Create dictionary to save colors used on lines
        self.line_colors_dict: dict[Line, list] = {}
        self.colors = [PURE_RED, PURE_GREEN, 
                       PURE_BLUE, YELLOW, 
                       PURPLE, ORANGE, PINK]

    # Move camera to capture network
    def setup_camera(self) -> None:
        self.camera.frame.move_to(self.dots)
        self.camera.frame.set_height(1.1 * self.dots.get_height())

    # Run algorithm here
    def run_algorithm(self) -> None:
        self.output = Greedy(self.data).run() # HERE

    # Find dots associated to station name
    def correspondence(self, name_start: str, name_end: str) -> tuple:
            
            # Find corresponding station object 
            station_start = self.name_station_dict[name_start]
            station_end = self.name_station_dict[name_end]

            # Find corresponding dot object
            dot_start = self.station_dot_dict[station_start]
            dot_end = self.station_dot_dict[station_end]

            return (dot_start, dot_end)
    
    # Find line associated with connection    
    def find_connection(self, dot_start: Dot, dot_end: Dot, time: int) -> Line:

        # Check if connection exists
        if (dot_start, dot_end, time) in self.connection_line_dict:
            line = self.connection_line_dict[(dot_start, dot_end, time)]
            
        # Otherwise reversed connection must exist
        else:
            line = self.connection_line_dict[(dot_end, dot_start, time)]

        return line

    # Main method calling upon other methods to color route and move train
    def color_route(self, route: list, color: manim_colors):

        for connection in route:
            time = connection[2]

            # Find station dot correspondence 
            dot_start, dot_end = self.correspondence(connection[0], connection[1])

            # Find connection
            line = self.find_connection(dot_start, dot_end, time)

            # Set color of line
            self.set_color(line, color)

    # Set color depending on if already colored
    def set_color(self, line: Line, color: manim_colors):

        # If line not yet colored just color
        if not line in self.line_colors_dict:
            line.set_color(color = color)
            self.line_colors_dict[line] = [color]

        else:
            # If line not already has given color update gradient
            if not color in self.line_colors_dict[line]:
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
        self.add(new_line)

    def place(self, label: VGroup) -> None:
        pass

    def construct(self):

        self.setup_2()
        self.add(self.dots, self.connections, self.connection_labels)
        label = Text("Greedy Algorithm")
        score = Text("Score = ")

        position = self.camera.frame.get_center()
        height = self.camera.frame.get_height()
        width = self.camera.frame.get_width()

        label.move_to(position)
        score.move_to(position)

        label.scale(0.05)
        score.scale(0.05)

        label.shift(LEFT * width * 0.25 - UP * height * 0.25)
        score.shift(LEFT * width * 0.25 - UP * height * 0.3)

        self.add(label)
        self.add(score)

        # Using seven routes
        for i in range(7):

            # Iterate over route_objects in output
            route_object = self.output[i]

            # Get connections within route_object
            route = route_object.get_connections_used()

            # Color route with ith color
            self.color_route(route, self.colors[i])