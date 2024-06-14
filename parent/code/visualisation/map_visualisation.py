from manim import FadeIn, Transform
from base_map import BaseMapScene

class map_visualisation(BaseMapScene):

    # Play scene showing labels, points and connections
    def construct(self):
        self.play(FadeIn(self.dot_labels), run_time = 2)
        self.play(Transform(self.dot_labels, self.dots), run_time = 2)
        self.play(FadeIn(self.connections), run_time = 2)
        self.play(FadeIn(self.connection_labels), run_time = 2)
        self.wait(2)