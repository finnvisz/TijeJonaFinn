from parent.code.visualisation.map import Map
from parent.code.classes.route import Route
from manim import manim_colors, Transform

class Display_Route(Map):
    """Show trainroutes on map."""

    def color_route(self, route: list):
        
        for connection in route:
            print(connection)
            line = self.traject_line_dict[connection]
            line.set_color(manim_colors.RED)

    def construct(self):
        self.add(self.points, self.connections)

        alkmaar = self.station_name_dict["Alkmaar"]
        hoorn = self.station_name_dict["Hoorn"]
        traject1 = [alkmaar, hoorn, 24]
        traject2 = [alkmaar, hoorn, 24]
        self.color_route([traject1, traject2])

        self.play(Transform(self.connections))
        self.wait(4)