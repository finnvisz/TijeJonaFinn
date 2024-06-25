from parent.code.experiments.statistics import read_solution_from_csv
from parent.code.algorithms.score import calculate_score
from parent.code.visualisation.map_visualisation import BaseScene

import numpy as np
import manim as m

class RouteVisualisationScene(BaseScene):
    """Show trainroutes on map."""

    def setup(self) -> None:

        # Inherit setup
        super().setup()

        # Run a specific algorithm
        self.run_algorithm()

        # Create dictionary to save colors used on lines
        self.line_colors_dict: dict[m.Line, list] = {}
        self.colors = [m.PURE_RED, m.RED_A, m.PURE_GREEN, m.GREEN_A,
                       m.PURE_BLUE, m.BLUE_A, m.YELLOW, m.YELLOW_A,
                       m.PURPLE, m.PURPLE_A, m.ORANGE, m.PINK,
                       m.TEAL, m.TEAL_A, m.GRAY, m.GRAY_A,
                       m.GOLD, m.GOLD_A, m.MAROON, m.MAROON_A]

    # Make train to ride tracks
    def setup_train(self, dot_start: m.Dot) -> None:
        self.train = m.Dot(point = dot_start.get_center(), radius = self.radius)

    # Run algorithm here
    def run_algorithm(self) -> None:
        self.output = read_solution_from_csv(self.filepath, file_path = "for_manim", map = self.map)
        
        # Save number of routes for later reference
        self.n_routes = len(self.output)

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
    def find_connection(self, dot_start: m.Dot, dot_end: m.Dot, time: int) -> m.Line:

        # Check if connection exists
        if (dot_start, dot_end, time) in self.connection_line_dict:
            line = self.connection_line_dict[(dot_start, dot_end, time)]
            
        # Otherwise reversed connection must exist
        else:
            line = self.connection_line_dict[(dot_end, dot_start, time)]

        return line

    # Main method calling upon other methods to color route and move train
    def color_route(self, route: list, color: m.manim_colors) -> None:

        start_route = 0
        for connection in route:
            time = connection[2]

            # Find station dot correspondence 
            dot_start, dot_end = self.correspondence(connection[0], connection[1])

            # Place train at start of new route
            if start_route == 0:
                self.setup_train(dot_start)
                start_route += 1

            # Find connection
            line = self.find_connection(dot_start, dot_end, time)

            # Set color of line
            self.set_color(line, color)

            # Move train
            shift = self.train.animate.move_to(dot_end.get_center())
            self.play(shift, run_time = 0.4, rate_func = m.smooth)

    # Set color depending on if already colored
    def set_color(self, line: m.Line, color: m.manim_colors) -> None:

        # If line not yet colored just color
        if not line in self.line_colors_dict:
            self.play(m.ApplyMethod(line.set_color, color), run_time = 0.1)
            self.line_colors_dict[line] = [color]

        else:
            # If line not already has given color update gradient
            if not color in self.line_colors_dict[line]:
                colors = self.line_colors_dict[line]
                colors.append(color)
                self.set_multiple_colors(line, colors)

    # Set line with multiple colors 
    def set_multiple_colors(self, line: m.Line, colors: list) -> None:

        # Find start and end brutally
        starting_point = line.start
        ending_point = line.end

        # Get direction and length 
        length = np.norm(ending_point - starting_point)
        direction = (ending_point - starting_point) / length

        # Get length of each segment
        amount = len(colors)
        segment_length = length / amount

        # Create new line VGroup to replace old
        new_line = m.VGroup()

        # Create new line consisting of segments
        for i in range(amount):

            # Create ending of segment
            ending_point = starting_point + direction * segment_length

            # Create new segment linepiece
            segment = m.Line(start = starting_point, end = ending_point, 
                           color = colors[i], stroke_width = self.line_width)

            # Add segment and set ending point as new starting
            new_line.add(segment)
            starting_point = ending_point

        # Transformeer oude lijn naar nieuw gesegmenteerde lijn
        self.play(m.Transform(line, new_line), run_time = 0.1)

    def is_video(self):
        return True

    def construct(self):
        self.add(self.dots, self.connections, self.connection_labels)
        
        label = m.Text(f"RailNL - {self.map}")
        score = m.Text(f"Score = {calculate_score(self.output, self.map)}")

        position = self.camera.frame.get_center()
        height = self.camera.frame.get_height()
        width = self.camera.frame.get_width()

        label.move_to(position)
        score.move_to(position)

        label.scale(self.label_scale)
        score.scale(self.label_scale)

        label.shift(m.LEFT * width * 0.25 - m.UP * height * 0.25)
        score.shift(m.LEFT * width * 0.25 - m.UP * height * 0.3)

        self.add(label)
        self.add(score)
        
        if self.is_video():
            self.wait(2)

        # Using seven routes
        for i in range(self.n_routes):

            # Iterate over route_objects in output
            route_object = self.output[i]

            # Get connections within route_object
            route = route_object.get_connections_used()

            # Color route with ith color
            self.color_route(route, self.colors[i])

        if self.is_video():
            self.wait(2)