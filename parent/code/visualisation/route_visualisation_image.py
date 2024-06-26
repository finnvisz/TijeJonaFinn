from parent.code.visualisation.route_visualisation import RouteVisualisationScene

import numpy.linalg as np
import manim as m

class RouteVisualisationImage(RouteVisualisationScene):
    """
    A manim scene animating a collection of train routes on a given map
    as an image. Inherits all RouteVisualisationScene attributes, but
    overwrites certain methods to create image instead of video.
    """

    def color_route(self, route: list, color: m.manim_colors):
        """
        Main route coloring method calling upon other class methods to color
        all train routes in self.output.

        Pre
        ---
        Route input is a list of route objects. Color is a manim color 
        contained in self.colors.

        Post
        ---
        Calls upon set_color() to set color of line in route. 
        """ 
        for connection in route:
            time = connection[2]

            # Find station dot correspondence 
            dot_start, dot_end = self.correspondence(connection[0], connection[1])

            # Find connection
            line = self.find_connection(dot_start, dot_end, time)

            # Set color of line
            self.set_color(line, color)

    def set_color(self, line: m.Line, color: m.manim_colors):
        """
        Colors route a color or calls upon set_multiple_colors.

        Pre
        ---
        Line is a line object corresponding to an existing connection in 
        RailNL(self.map). Color is a manim color contained in self.colors.

        Post
        ---
        Sets color of line uniformly if line is not already colored by 
        adding color to line statically.
        Calls upon set_multiple_color if color must be added to an already
        colored line.
        """

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
 
    def set_multiple_colors(self, line: m.Line, colors: list):
        """
        Colors line with multiple colors using line_colors_dict.

        Pre
        ---
        Line is a line object corresponding to an existing connection in 
        RailNL(self.map). Color is a manim color contained in self.colors.

        Post
        ---
        Statically creates a new line on top of old line. New line is
        created with an additional color by creating several uniquely 
        colored line segments.
        """

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
                           color = colors[i], stroke_width = 0.75)

            # Add segment and set ending point as new starting
            new_line.add(segment)
            starting_point = ending_point

        # Transformeer oude lijn naar nieuw gesegmenteerde lijn
        self.add(new_line)

    def is_video(self):
        """
        Method to use in construct() to create either image or video.
        """       
        return False