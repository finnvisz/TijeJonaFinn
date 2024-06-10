from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
import random

# pick station to start from with most connections if not all connections are already used
# implement greedy algorithm that prioritizes use of all connections
# pick a connection not yet used with shortest length, if not possible, start a new route

class Greedy(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)

    def run(self):
        self.routes = []  # Ensure routes are clear before running
        while self.number_of_routes() < 7 and len(self.connections_used()) < len(set(map(tuple, self.load.connections))):
            time_used = 0
            current_station = random.choice(list(self.load.stations_dictionary().values()))
            route = Route()
            visited_connections = set()

            while current_station.has_connections():
                break
                # pick a connection not yet used with shortest duration, if not possible, start a new route
            break
            