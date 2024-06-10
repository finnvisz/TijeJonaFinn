from .algorithm import Algorithm
from ..classes.railnl import RailNL
from ..classes.route import Route

# implement greedy algorithm that prioritizes use of all connections
# pick a connection not yet used with shortest length, if not possible, start a new route

class Greedy(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)

    def run(self):
        for _ in range(7):
            time_used = 0
            current_station = self.load.stations_dictionary['Zaandam']
            route = Route()

            # Break when no connections are left in current station
            while current_station.has_connections():