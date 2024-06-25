
from parent.code.visualisation.route_visualisation import route_visualisation_Scene
from numpy.linalg import norm
import manim as m

class route_visualisation_image(route_visualisation_Scene):
    """Show trainroutes on map."""

    # Main method calling upon other methods to color route and move train
    def color_route(self, route: list, color: m.manim_colors):

        for connection in route:
            time = connection[2]

            # Find station dot correspondence 
            dot_start, dot_end = self.correspondence(connection[0], connection[1])

            # Find connection
            line = self.find_connection(dot_start, dot_end, time)

            # Set color of line
            self.set_color(line, color)

    # Set color depending on if already colored
    def set_color(self, line: m.Line, color: m.manim_colors):

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
    def set_multiple_colors(self, line: m.Line, colors: list):

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
        return False