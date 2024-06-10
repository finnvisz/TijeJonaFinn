from .algorithm import Algorithm
from ..classes.railnl import RailNL
from ..classes.route import Route

# pick station to start from with most connections if not all connections are already used
# implement greedy algorithm that prioritizes use of all connections
# pick a connection not yet used with shortest length, if not possible, start a new route

class Greedy(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)
        self.used_connections = set()

    def run(self):
        for _ in range(7):
            time_used = 0
            current_station = max(self.load.stations_dictionary().values(), key=lambda station: station.amount_connecting())
            route = Route()

            # Break when no connections are left in current station
            while current_station.has_connections():
                for connection in current_station.connecting_stations():
                    duration = int(current_station.connection_duration(connection))
                break
                

            self.routes.append(route)