from parent.code.visualisation.map import Map
from parent.code.classes.route import Route
from manim import manim_colors, MovingCameraScene, ApplyMethod
from typing import Type

class Display_Route(Map):
    """Show trainroutes on map."""

    def color_route(self, route: list):
        for connection in route:

            station1 = self.station_name_dict[connection[0]]
            station2 = self.station_name_dict[connection[1]]
            time = connection[2]
            tuple = (station1, station2, time)

            if tuple in self.route_line_dict:
                line = self.route_line_dict[tuple]
            
            else:
                tuple = (station2, station1, time)
                line = self.route_line_dict[tuple]

            self.play(ApplyMethod(line.set_color, manim_colors.RED))

    def construct(self):
        self.setup()
        self.add(self.points, self.connections, self.connection_labels)
        self.wait(2)

        route = [('Leiden Centraal', 'Schiphol Airport', '15'),
                 ('Schiphol Airport', 'Amsterdam Zuid', '6')]
        self.color_route(route)

        self.wait(2)