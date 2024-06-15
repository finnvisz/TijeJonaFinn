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

    def run(self, original_starting_station: bool = True) -> list[Route]:
        # List to store the various routes
        self.routes: list[Route] = []
        

        # Unused_connections starts off with all connections
        # Unused connections will be moved to used connections when they are used
        self.used_connections: dict = dict()
        
        self.unused_connections: dict = dict()
        for connection in self.load.connections:
            # Save the names of the stations in this connection in a tuple
            station_names_as_tuple = tuple(sorted([connection[0].name, connection[1].name]))

            # Add the connection to the dict with the station name tuple as key
            self.unused_connections[station_names_as_tuple] = connection


        # Unused stations starts off with all stations
        # Unused stations will be moved to used stations when they are used
        self.unused_stations: list = list(self.load.stations.values()) # internal list of stations
        self.used_stations: list = list()

        # DEBUG
        # print(self.unused_stations)

        # While there are less than 7 routes and there are still unused connections
        while self.number_of_routes() < 7 and len(self.unused_connections) > 0:
            # Create a new route
            route = Route()
            # DEBUG
            # print(f"Route {self.number_of_routes() + 1}")

            # And set a first station for this route:
            # if flag is set to true, try to pick unused stations
            if original_starting_station:
                # Option 1: pick a random unused station
                if len(self.unused_stations) > 0:
                    current_station = random.choice(self.unused_stations)
                
                # Option 2: pick station with an unused connection
                else:
                    random_unused_connection = random.choice(list(self.unused_connections.values()))
                    random_index = random.choice([0, 1])
                    
                    current_station = random_unused_connection[random_index]

            # if flag set to false, pick random from all stations
            else:
                current_station = self.load.get_random_station()


            # While time is less than 120 minutes
            while route.time < 120: 
                # DEBUG
                # print(f"Current station: {current_station.name}")
                
                # First: move this station to used stations
                # (if already moved do nothing)
                try:
                    index = self.unused_stations.index(current_station)
                    self.used_stations.append(self.unused_stations.pop(index))
                except ValueError:
                    pass
                
                
                # Get connections of current station, sorted by duration
                # This is a queue of possible connections, with the shortest connection first
                connections = current_station.get_connections_sorted()

                # Pop used connections from queue (as long as there are any left)
                while len(connections) > 0 and route.is_connection_used(current_station, connections[0][0]):
                    connections.pop(0)
                
                # If adding this connection would exceed the time limit, remove this connection
                while len(connections) > 0 and route.time + connections[0][1] > 120:
                    connections.pop(0)

                # If there are no unused connections left, end this route
                if len(connections) == 0:
                    break

                # Shortest unused connection is the next station
                next_station = connections[0][0]

                # DEBUG
                # print(f"Current station: {current_station.name}")
                # print(f"Next station: {next_station.name}")

                # Add the connection to the route
                route.add_connection(current_station, next_station, current_station.get_connection_time(next_station))

                # Move the connection to used connections
                self.set_as_used(current_station, next_station)

                # Set the next station as the current station
                current_station = next_station
                
            self.routes.append(route)
        
        # Return the generated routes
        return self.routes

    def set_as_used(self, current_station: "Station", next_station: "Station") -> None:
        """
        Takes two stations and moves the connection between them from unused to used connections.
        Order of the stations does not matter, connections are handled alphabetically.
        """
        # Extract dictionary key for the connection
        connection_key = tuple(sorted([current_station.name, next_station.name]))

        # If key is currently set as unused: set as used
        if connection_key in self.unused_connections:
            # Pop this key-value pair from unused and add to the used connections
            self.used_connections[connection_key] = self.unused_connections.pop(connection_key)

    
    def create_route_from_station(self, station: "Station") -> Route:
        """
        Create a single route starting from a given station.
        """
        # Create a new route
        route = Route()
        # Route starts at the given station
        current_station = station

        # While time is less than 120 minutes
        while route.time < 120:
            # Get connections of current station, sorted by duration
            # This is a queue of possible connections, with the shortest connection first
            connections = current_station.get_connections_sorted()

            # Pop used connections from queue (as long as there are any left)
            while len(connections) > 0 and route.is_connection_used(current_station, connections[0][0]):
                connections.pop(0)
            
            # If adding this connection would exceed the time limit, remove this connection
            while len(connections) > 0 and route.time + connections[0][1] > 120:
                connections.pop(0)

            # If there are no unused connections left, end this route
            if len(connections) == 0:
                break

            # Shortest unused connection is the next station
            next_station = connections[0][0]

            # DEBUG
            # print(f"Current station: {current_station.name}")
            # print(f"Next station: {next_station.name}")

            # Add the connection to the route
            route.add(current_station, next_station, current_station.get_connection_time(next_station))

            # Set the next station as the current station
            current_station = next_station
        
        return route
    
    
    def best_starting_station(self):
        """
        Create a route from every station and return the amount of connections for each route.
        """ 
        # List to store the amount of connections for each route
        results = []

        # For every station in the dataset
        for station in self.load.stations.values():
            # Create a route starting from this station
            route = self.create_route_from_station(station)
            
            # Get the amount of connections for this route
            amount_of_connections = len(route.connections())

            # Append name, amount of connections and time to results
            results.append([station.name, amount_of_connections, route.time])

        return results
        

# Run standard greedy and print results
if __name__ == "__main__":
    greedy = Greedy(RailNL("Holland"))
    output = greedy.run()
    
    for route in output:
        for connection in route.get_connections_used():
            print(connection[0], connection[2], end=" -> ")
        
        print("")
        print(f"Total time: {route.time}")
        print("")

    print(f"Unused stations: {len(greedy.unused_stations)}")
    print(f"Unused connections: {len(greedy.unused_connections)}")

# # Run best starting station and print results
# if __name__ == "__main__":
#     greedy = Greedy(RailNL("Holland"))
#     results = greedy.best_starting_station()
#     for result in results:
#         if result[1] > 12:
#             print(f"Station: {result[0]}, Connections: {result[1]}, Time: {result[2]}")