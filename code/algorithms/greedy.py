from .algorithm import Algorithm
from ..classes.railnl import RailNL
from ..classes.route import Route
import random

# implement greedy algorithm that prioritizes use of all connections
# pick a connection not yet used, if not possible, start a new route

class Greedy(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)

    def run(self):
            time_used = 0
            current_station = self.load.stations_dictionary["Zaandam"]
            traject = Route()