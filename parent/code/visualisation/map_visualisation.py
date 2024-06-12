from manim import MovingCameraScene
from base_map import Map

class map_visualisation(MovingCameraScene):
    
    def setup(self):
        map = Map()