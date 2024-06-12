# Library imports
import random
import copy

# Local imports
from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
from parent.code.classes.station_class import Station

# pick station to start from with most connections if not all connections are already used
# implement greedy algorithm that prioritizes use of all connections
# pick a connection not yet used with shortest length, if not possible, start a new route

class Greedy(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)



    def run(self):
        # List to store the various routes
        self.routes = []
        
        # unused_connections starts off with all connections
        # Unused connections will be moved to used connections when they are used
        self.unused_connections: set[tuple] = copy.deepcopy(self.load.connections)
        self.used_connections: set  = set()

        # DEBUG
        print(self.unused_connections)

        # While there are less than 7 routes and there are still unused connections
        while self.number_of_routes() < 7 and len(self.unused_connections) > 0:
            # Create a new route
            route = Route()

            # And set a random first station for this route
            current_station = self.load.get_random_station()

            # While time is less than 120 minutes
            while route.time < 120:
                # Select the connection with the shortest duration
                next_station: "Station" = current_station.get_shortest_connection()

                # Add the connection to the route
                route.add(current_station, next_station, current_station.get_connection_time(next_station))

                # Move the connection to used connections
                self.set_as_used(current_station, next_station)

                # Set the next station as the current station
                current_station = next_station
                
            self.routes.append(route)
        
        # Return the generated routes
        return self.routes

    def set_as_used(self, current_station: "Station", next_station: "Station"):
        """
        Takes two stations and moves the connection between them from unused to used connections.
        Order of the stations does not matter, connections are handled alphabetically.
        """
        # Sort the connection alphabetically and create tuple
        connection_sorted = tuple(sorted([current_station, next_station], key=lambda x: x.name))
        
        # Move the connection from unused to used connections
        self.unused_connections.remove(connection_sorted)
        self.used_connections.add(connection_sorted)

if __name__ == "__main__":
    greedy = Greedy(RailNL("Holland"))
    
    
    
    output = greedy.run()
    print(output)