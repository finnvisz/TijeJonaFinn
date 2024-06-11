from parent.code.visualisation.map import Map
from parent.code.classes.route import Route
from manim import manim_colors, Transform

class Display_Route(Map):
    """Show trainroutes on map."""

    def color_route(self, route: list):

        for connection in route:

            if connection in self.route_line_dict:
                line = self.route_line_dict[connection]
            
            else:
                tuple = (connection[1], connection[0], connection[2])
                line = self.route_line_dict[tuple]

            line.set_color(manim_colors.RED)

    def construct(self):
        self.setup()
        self.add(self.points, self.connections, self.connection_labels)
        route = [('Leiden Centraal', 'Schiphol Airport', 15),
                 ('Schiphol Airport', 'Amsterdam Zuid', 6),
                 ('Amsterdam Zuid', 'Amsterdam Sloterdijk', 16)]
        
        print(self.route_line_dict.keys())
        self.color_route(route)
        self.play(Transform(self.connections), run_time = 2)
        self.wait(4)