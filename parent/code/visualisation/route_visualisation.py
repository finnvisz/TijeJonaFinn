from manim import MovingCameraScene, ApplyMethod, Line, manim_colors
from manim import PURE_RED, PURE_GREEN, PURE_BLUE, YELLOW, PURPLE, ORANGE, PINK
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.random_algorithm import RandomAlgorithm
from base_map import Map

class route_visualisation(MovingCameraScene):
    """Show trainroutes on map."""

    def setup(self):
        self.map = Map()
        self.line_colors_dict: dict[Line, list] = {}
        self.colors = [PURE_RED, PURE_GREEN, PURE_BLUE, YELLOW, 
                       PURPLE, ORANGE, PINK]

    def color_route(self, route: list, color: manim_colors):

        # Get station dot conversion dictionaries
        name_station_dict = self.map.give_name_station_dict()
        station_dot_dict = self.map.give_station_dot_dict()
        connection_line_dict = self.map.give_connection_line_dict()

        for connection in route:
            time = connection[2]

            # Find corresponding station object 
            station_start = name_station_dict[connection[0]]
            station_end = name_station_dict[connection[1]]

            # Find corresponding dot object
            dot_start = station_dot_dict[station_start]
            dot_end = station_dot_dict[station_end]

            # Check if connection tuple exists
            tuple = (dot_start, dot_end, time)
            if tuple in connection_line_dict:
                line = connection_line_dict[tuple]
                self.set_color(line, color)
            
            # Otherwise search reversed connection
            else:
                tuple = (dot_end, dot_start, time)
                line = connection_line_dict[tuple]
                self.set_color(line, color)

    # Set color depending on if already colored.
    def set_color(self, line: Line, color: manim_colors):

        if not line in self.line_colors_dict:

            # If line not yet colored just color
            self.play(ApplyMethod(line.set_color, color))
            self.line_colors_dict[line] = [color]

        else:

            # If line already has given color do nothing
            if color in self.line_colors_dict[line]:
                pass

            else: 
                # Otherwise update line gradient
                colors = self.line_colors_dict[line]
                colors.append(color)
                self.play(ApplyMethod(line.set_color, colors))

    def construct(self):
        
        # Get all objects from base_map
        dots = self.map.give_dots()
        connections = self.map.give_connections()
        connection_labels = self.map.give_connection_labels()

        # Move camera to capture network
        self.camera.frame.move_to(dots)
        self.camera.frame.set_height(1.1 * dots.get_height())

        self.add(dots, connections, connection_labels)
        self.wait(2)

        data = RailNL("Holland")
        random = RandomAlgorithm(data)
        random.run()
        dienstregeling = random.output()

        for count in range(7):
            route = dienstregeling[count].connections()
            self.color_route(route, self.colors[count])

        self.wait(2)