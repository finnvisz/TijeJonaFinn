from manim import MovingCameraScene, FadeIn, Transform
from base_map import Map

class map_visualisation(MovingCameraScene):

    # Play scene showing labels, points and connections
    def construct(self):
    
        # Get all objects from base_map
        map = Map()
        dots = map.give_dots()
        dot_labels = map.give_dot_labels()
        connections = map.give_connections()
        connection_labels = map.give_connection_labels()

        # Move camera to capture network
        self.camera.frame.move_to(dots)
        self.camera.frame.set_height(1.1 * dots.get_height())

        # Fade labels in, transform into points
        self.play(FadeIn(dot_labels), run_time = 2)
        self.play(Transform(dot_labels, dots), run_time = 2)
        self.play(FadeIn(connections), run_time = 2)
        self.play(FadeIn(connection_labels), run_time = 2)
        self.wait(2)