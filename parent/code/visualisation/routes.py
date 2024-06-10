from parent.code.visualisation.map import Map
from parent.code.classes.route import Route
from manim import RED, Transform

class Display_Route(Map):
    """Show trainroutes on map."""

    def color_route(self, route: list):
        
        for connection in list:
            line = self.traject_line_dict[connection]
            line.set_color(RED)

    def construct(self):
        self.add(self.points, self.connections)
        self.color_route()
        self.wait(4)
        
