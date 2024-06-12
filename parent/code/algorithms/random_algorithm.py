from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
from random import choice
from parent.code.algorithms.score import Score

class RandomAlgorithm(Algorithm):
    """Algorithm script finding 7 random routes. Each not exceeding 
    the 120 minute limit
    """

    def __init__(self, load: RailNL) -> None:
        super().__init__(load) # Inherits everything from ALgorithm class


    def run(self) -> None:

        for _ in range(7):
            time_used = 0
            route = Route()

            # Find a random starting station
            current_station = self.load.get_random_station()

            # Break when no connections are left in current station
            while current_station.has_connections():

                # Find random connection from current_station connections
                connections = list(current_station.connections_dict())
                connection = choice(connections)

                # Calculate new total duration of route
                duration = int(current_station.connection_duration(connection))
                total = time_used + duration

                # Continue if adding a connection is 
                # possible considering time_used
                if total <= 120:
                    time_used = total
                    route.add(current_station, connection, duration)
                    current_station = connection

                # Else, route is finished
                else:
                    break
            
            self.routes.append(route)

