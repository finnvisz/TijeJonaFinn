# Library imports
import random
import copy

# Local imports
from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
from parent.code.classes.station_class import Station

# pick station to start from with most connections if not all connections are already used
# implement randomv2 algorithm that prioritizes use of all connections
# pick a connection not yet used with shortest length, if not possible, start a new route

class Randomv2(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)

        
    def run(self, original_connections_only: bool = False, starting_stations: str = "fully_random", starting_station_list: None | list["Station"] = None) -> list[Route]:
        """
        Random algorithm with various options for starting stations per route.

        args:
        - original_connections_only: (NOTE: leave on False, creates solutions with very short connections)
        When True, each route uses only unused connections.
        i.e.: within a route, no connection is used more than once. When False,
        connections are fully random and can be used multiple times within a route.
        - starting_stations: Specify how to pick the starting station for each route.
        Options: "fully_random", "prefer_unused", "custom_list_with_replacement", "custom_list_without_replacement". 
        NOTE: When picking without replacement from a custom list, options will be reused when length of list is < 7.
        - starting_station_list: list of stations to pick from. Only used when starting_stations is set to "custom_list_with_replacement" or "custom_list_without_replacement"
        """
        
        # Check for correct input
        if starting_stations == "custom_list_with_replacement" or starting_stations == "custom_list_without_replacement":
            assert starting_station_list is not None, "Starting station list must be provided when starting_stations is set to 'custom_list_with_replacement' or 'custom_list_without_replacement'."
        
        # If starting_station_list is provided and we draw without replacement,
        # randomize it's order
        if starting_stations == "custom_list_without_replacement":
 
            # Make a copy of the list to avoid changing the original list
            starting_station_list_copy = copy.deepcopy(starting_station_list)
            
            random.shuffle(starting_station_list_copy)


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
        # i.e. for each route
        while self.number_of_routes() < 7 and len(self.unused_connections) > 0:
            # Create a new route
            route = Route()
            # DEBUG
            # print(f"Route {self.number_of_routes() + 1}")



            # And set a first station for this route (method depends on starting_stations argument):
            
            # If "starting_stations" is set to "prefer_unused", try to pick unused stations
            if starting_stations == "prefer_unused":
                # Plan A: pick a random unused station
                if len(self.unused_stations) > 0:
                    current_station = random.choice(self.unused_stations)
                
                # Option 2: pick station with an unused connection
                else:
                    random_unused_connection = random.choice(list(self.unused_connections.values()))
                    random_index = random.choice([0, 1])
                    
                    current_station = random_unused_connection[random_index]

            # If flag set to "fully_random", pick random from all stations
            elif starting_stations == "fully_random":
                current_station = self.load.get_random_station()

            # If flag set to "custom_list_with_replacement", pick from the custom list
            elif starting_stations == "custom_list_with_replacement":
                current_station = random.choice(starting_station_list)

            # If flag set to "custom_list_without_replacement", 
            # pop from randomized version of custom list
            elif starting_stations == "custom_list_without_replacement":
                # If list is empty, refill it
                if len(starting_station_list_copy) == 0:
                    starting_station_list_copy = copy.deepcopy(self.used_stations)
                    random.shuffle(starting_station_list_copy)

                current_station = starting_station_list_copy.pop()


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

                # Randomize the order of the connections (to add the randomness to the algorithm)
                random.shuffle(connections)

                # If arg. original_connections_only set to True
                if original_connections_only:
                    # Pop used connections from queue (until unused connection is found)
                    while len(connections) > 0 and route.is_connection_used(current_station, connections[0][0]):
                        connections.pop(0)
                
                # If adding this connection would exceed the time limit, remove this connection
                while len(connections) > 0 and route.time + connections[0][1] > 120:
                    connections.pop(0)

                # If there are no unused connections left, end this route
                if len(connections) == 0:
                    break

                # First connection in queue is the next station
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

    
        

# Run  and print results
if __name__ == "__main__":
    
    # Run algorithm with desired settings
    randomv2 = Randomv2(RailNL("Holland"))
    
    custom_starting_stations = [randomv2.load.stations["Rotterdam Centraal"], randomv2.load.stations["Amsterdam Centraal"]]
    
    output = randomv2.run(starting_stations="custom_list_with_replacement", starting_station_list = custom_starting_stations)
    

    # Print results + extra info
    for route in output:
        for connection in route.get_connections_used():
            print(connection[0], " - ", connection[1], connection[2], end=" -> ")
        
        print("")
        print(f"Total time: {route.time}")
        print("")

    print(f"Unused stations: {len(randomv2.unused_stations)}")
    print(f"Unused connections: {len(randomv2.unused_connections)}")