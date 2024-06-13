from manim import MovingCameraScene, FadeIn, Transform
from base_map import Map

class map_visualisation(MovingCameraScene):

    def setup(self):
        self.setup_map()
        self.setup_camera()

    # Get all relevant objects from base_map
    def setup_map(self):
        map = Map()
        self.dots = map.give_dots()
        self.dot_labels = map.give_dot_labels()
        self.connections = map.give_connections()
        self.connection_labels = map.give_connection_labels()

    # Move camera to capture network
    def setup_camera(self):
        self.camera.frame.move_to(self.dots)
        self.camera.frame.set_height(1.1 * self.dots.get_height())

    # Play scene showing labels, points and connections
    def construct(self):
        self.play(FadeIn(self.dot_labels), run_time = 2)
        self.play(Transform(self.dot_labels, self.dots), run_time = 2)
        self.play(FadeIn(self.connections), run_time = 2)
        self.play(FadeIn(self.connection_labels), run_time = 2)
        self.wait(2)