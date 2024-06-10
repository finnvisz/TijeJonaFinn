from parent.code.visualisation.map import Map
from parent.code.classes.route import Route
from manim import Create, MovingCameraScene

class Display_Route(Map):
    """Show trainroutes on map."""

    def color_route(self, route: Route):
        pass

    def construct(self):
        self.add(self.points, self.connections)
        self.wait(4)
        
