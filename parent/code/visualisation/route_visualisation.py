from parent.code.helpers.csv_helpers import read_solution_from_csv
from parent.code.helpers.score import calculate_score
from parent.code.visualisation.map_visualisation import BaseScene

import numpy as np
import manim as m

class RouteVisualisationScene(BaseScene):
    """
    A manim scene animating a collection of train routes on a given map.
    Inherits all BaseScene attributes and methods.

    Attributes
    ---------
    line_colors_dict: Association between connection lines and their colors.
    colors: List of all possible colors used to form visualisation.
    train: Dot object to visualise a train riding the track.
    output: List of lists of route objects. 
    n_routes: Amount of routes to color.

    Methods
    -------
    setup: Defacto initializer. Called upon by Super().__init__().
    setup_train: Method to instantiate dot object representing a train.
    run_algorithm: Reads solution from csv file containing train routes.
    correspondence: Find dot objects corresponding with names in a connection.
    find_connection: Find the connection line associated with two dot objects.
    color_route: Calls upon methods to color given route and moves train.
    set_color: Colors route a color or calls upon set_multiple_colors.
    set_multiple_colors: Colors line with multiple colors using line_colors_dict.
    is_video: Method to infer whether image or video needs to be created.
    place_labels: Places RailNL and score labels within scene.
    construct: Main method called upon by Super.__init__().

    Usage
    -----
    NOTE: Always check visualisation_settings.csv.
    Use VScode manim sideview extension.
    Alternatively run: manim -pql map_visualisation.py RouteVisualisationScene.
    Running should return a video showing Holland or Nationaal train route network
    visualisation dependend on visualisation_settings.csv.
    """

    def setup(self) -> None:
        """
        Defacto initializer called upon by Super.__init__().

        Post
        ---
        Inherits all attributes from BaseScene. Obtains collection of 
        routes to visualise from run_algorithm. Instantiates line_colors_dict
        and sets possible colors.
        """

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

    def setup_train(self, dot_start: m.Dot) -> None:
        """
        Creates train dot object to ride track.

        Pre
        ---
        Dot object corresponding to a station.

        Post
        ---
        Sets self.train as dot placed upon station dot.
        """

        self.train = m.Dot(point = dot_start.get_center(), radius = self.radius)

    def run_algorithm(self) -> None:
        """
        Reads algorithm output from self.filepath.

        Pre
        ---
        Self.filepath is obtained from visualisation_settings.csv in BaseScene 
        class. This must be a relative path to a csv output file formatted 
        as specified by read_solution_from_csv.

        Post
        ---
        self.output 
        """

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
    
    def place_labels(self):
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

    def construct(self):
        self.add(self.dots, self.connections, self.connection_labels)
        self.place_labels()
        
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