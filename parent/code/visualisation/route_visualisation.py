from manim import manim_colors, MovingCameraScene, ApplyMethod
from base_map import Map

class route_visualisation(MovingCameraScene):
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
        
        # Get all objects from base_map
        map = Map()
        dots = map.give_dots()
        connections = map.give_connections()
        connection_labels = map.give_connection_labels()

        # Move camera to capture network
        self.camera.frame.move_to(dots)
        self.camera.frame.set_height(1.1 * dots.get_height())

        self.add(dots, connections, connection_labels)
        self.wait(2)

        # route = [('Leiden Centraal', 'Schiphol Airport', '15'),
        #          ('Schiphol Airport', 'Amsterdam Zuid', '6')]
        # self.color_route(route)

        # self.wait(2)