# Library imports
import random
import copy
import numpy as np

# Local imports
from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
from parent.code.classes.station_class import Station


class Random_Greedy(Algorithm):
    """
    Initialize fresh Random_Greedy algorithm class with given maprange.
    NOTE: make sure to reinitialize the class each time you run the algorithm.

    - Pre: Class of this method is initialized for either "Holland" or 
    "Nationaal" maprange.
    - Post: Random_Greedy object is created and ready to run the algorithm.
    """
    def __init__(self, maprange: str = "Holland") -> None:
        # Load RailNL data with given maprange
        self.load = RailNL(maprange)
        super().__init__(self.load)
        

    def run(self,
            # Options per connection:
            # How to pick the next connection in the route
            next_connection_choice: str = "random",
            original_connections_only: bool = False, 
            
            # Options for starting station per route:
            starting_stations: str = "fully_random", 
            starting_station_list: None | list["Station"] = None,
             
            # Options for number + length of routes: 
            final_number_of_routes: int | tuple[int] | None = None, 
            route_time_limit: int | tuple[int] | list[int] | None = None,

            # Options for early route end (before time limit):
            # USE AT OWN RISK, CREATES ROUTES WITH ZERO CONNECTIONS
            chance_of_early_route_end: bool = False) -> list[Route]:
        """
        
        Random and/or greedy algorithm to generate routes, with lots of options.
        Meant for running random-based tests and comparing various 
        subsets of the total state space.

        NOTE: make sure to reinitialize the class when running multiple times.

        - Pre: run method is called on a fresh Random_Greedy object 
        (i.e. this is the first time run is called on this object).
        - Post: Returns a list of routes

        args:
        
        Options per connection (How to pick the next connection in the
        route):
        
        - next_connection_choice: Specify how to pick the next connection 
        in the route. Options: "random" (default), or "shortest" for a
        greedy approach to connections.
        
        - original_connections_only: (NOTE: leave on False when 
        `next_connection_choice = "random", creates solutions with very
        short connections) When True, each route uses only unused
        connections. i.e.: within a route, no connection is used more
        than once. When False, connections are fully random and can be
        used multiple times within a route.

        Options for starting station per route:

        - starting_stations: Specify how to pick the starting station for 
        each route. Options: 
        1. fully_random: pick random with replacement from all stations.
        2. original_stations_only_soft: (Tije version) pick random
        with replacement, but if another route starts at this station, 
        pick another.
        3. original_stations_only_hard: (Jona version) pick 
        random station with 0 connections, or else random station with
        unused connections.
        
        4. custom_list_with_replacement: pick random from custom list
        (with replacement)
        5. `custom_list_without_replacement`: pick random from custom list
        (without replacement; NOTE: make sure the list length is equal to
        the number of routes generated.)
        
        - starting_station_list: list of stations to pick from,
        OR list with multiple station lists is also possible 
        (in that case one of the station lists will be chosen randomly).
        Only used when starting_stations is set to
        "custom_list_with_replacement" or
        "custom_list_without_replacement"

        
        Options for number + length of routes:

        - final_number_of_routes: Number of routes to generate. Default
          is 7 for Holland map, 20 for Nationaal map. Can be set with
          `int` to override this. If set to `tuple[int]`, a random value
          out of the tuple will be chosen as number of routes.

        - route_time_limit: Maximum time for each route. Default is 120 
          minutes for Holland map, 180 minutes for Nationaal map. Can be set
          with `int` to override this fixed time limit. If set to `tuple[int]`, 
          a random value out of the tuple will be chosen as fixed time limit
          for all routes. If set to `list[int]`, each route will have a 
          different time limit randomly chosen from the list.


        Experimental (USE AT OWN RISK):
        
        - chance_of_early_route_end (bool): (CREATE ROUTES WITH 0 CONNECTIONS)
        If set to True, routes can end before `route_time_limit` minutes.
        Default is False.
        """

        # Check for correct input
        starting_station_list = self.check_input(final_number_of_routes, 
                        route_time_limit, next_connection_choice, 
                        original_connections_only, starting_stations, 
                        starting_station_list)


        # Set values for final_number_of_routes and route_time_limit:
        final_number_of_routes = self.set_final_number_of_routes(
                                        final_number_of_routes)

        # NOTE: time_limit_this_route is different from route_time_limit
        time_limit_this_route = self.set_time_limit_this_route(
                                        route_time_limit)


        # Load data and set up tracking of used connections and stations
        self.setup_used_connection_and_station_tracking(
            starting_stations = starting_stations,
            starting_station_list = starting_station_list)


        # Generate a solution with the given parameters
        solution = self.generate_solution(final_number_of_routes,
                                        route_time_limit,
                                        time_limit_this_route,
                                        starting_stations,
                                        starting_station_list,
                                        next_connection_choice,
                                        original_connections_only,
                                        chance_of_early_route_end)
        
        # And return the solution
        return solution


    def check_input(self, 
                    final_number_of_routes: int | tuple[int] | None, 
                    route_time_limit: int | tuple[int] | list[int] | None,
                    next_connection_choice: str,
                    original_connections_only: bool,
                    starting_stations: str,
                    starting_station_list: None | list["Station"]) -> None:
        """
        Check if the input for the run method is correct.
        
        Returns only the `starting_station_list`, because when user 
        provides list of lists for it, it must be changed during the 
        input checks: one of the lists is chosen randomly to be used as
        `starting_station_list`, and after that a final check is done.
        """
        
        # Check for correct input:

        # final_number_of_routes must be an integer or a tuple of integers
        assert final_number_of_routes is None or type(
            final_number_of_routes) in (int, tuple), """
            final_number_of_routes must be an int or tuple of ints."""

        # route_time_limit  input check
        assert route_time_limit is None or type(
            route_time_limit) in (int, tuple, list), """
            When set, route_time_limit must be an int, tuple of ints
            or list of ints (tuple and list generates different results, 
            read the docstring)."""


        # Check for correct input for next_connection_choice
        assert next_connection_choice in ["random", "shortest"], """
        next_connection_choice must be set to 'random' or 'shortest'."""

        # Check for correct input for starting_stations
        assert starting_stations in ["fully_random",
                                    "original_stations_only_soft", 
                                    "original_stations_only_hard",
                                    "custom_list_with_replacement", 
                                    "custom_list_without_replacement"], """
        starting_stations must be set to 'fully_random', 
        'original_stations_only_soft', 'original_stations_only_hard', 
        'custom_list_with_replacement' or 'custom_list_without_replacement'."""


        # With greedy approach, original connections only is required 
        # for correct functioning
        if next_connection_choice == "shortest" and original_connections_only == False:
            raise ValueError("""You are about to run an algorithm 
                             greedy on connections. Set 
                             original_connections_only to True. 
                             If not your algorithm 
                             will get stuck going back and forth between 
                             two stations.""")
        

        # With custom list, list must be provided
        if (starting_stations == "custom_list_with_replacement" or 
            starting_stations == "custom_list_without_replacement"):
            assert starting_station_list is not None, """Starting station list 
                must be provided when starting_stations is set to 
                'custom_list_with_replacement' or 'custom_list_without_replacement'."""

            assert type(starting_station_list) == list, """Starting station""" 
            """list must be provided as either a list with stations, or"""
            """a list containing multiple lists of stations'."""


            # If list of lists is provided, check if all elements are lists
            # And afterwords randomly select a list from the list of lists.
            # (For the TA reading this, I'm a bit confused as well.) 
            if type(starting_station_list[0]) is list:
                # Assert all elements are lists
                assert all(
                isinstance(element, list) 
                for element in starting_station_list), """
                Provide either a single list of stations,
                or a list of lists of stations. Don't mix the two!"""

                # And choose a random list from the list of lists
                starting_station_list = random.choice(starting_station_list)


        # For custom list without replacement, list must be long enough
        if starting_stations == "custom_list_without_replacement":
            
            if type(final_number_of_routes) == int:
                assert len(starting_station_list) == final_number_of_routes, """
                Starting station list must be exactly as long as the number 
                of routes."""

            if type(final_number_of_routes) == tuple:
                assert len(starting_station_list) == max(final_number_of_routes), """
                Starting station list must be exactly as long as the maximum 
                number of routes."""


        # Function returns starting_station_list because when 
        # provided by user it must be changed during the input checks 
        # (so one final check can be done after changing it)
        return starting_station_list


    def set_final_number_of_routes(self, 
                                   final_number_of_routes: int | tuple[int] | None) -> int:
        """
        Set the final number of routes to generate, depending on user 
        input and the map.
        """
        
        # For Holland map, the default number of routes is 7
        # For the Netherlands map, the default number of routes is 20
        if final_number_of_routes is None:
            if self.load.mapname == "Holland":
                final_number_of_routes = 7
            elif self.load.mapname == "Nationaal":
                final_number_of_routes = 20
            else:
                raise ValueError("Invalid mapname. Please use 'Holland' or 'Nationaal'.")
        
        # final_number_of_routes can be set to a tuple of numbers, 
        # if so the number of routes will be randomly chosen from this tuple
        elif type(final_number_of_routes) is tuple:
            final_number_of_routes = np.random.choice(final_number_of_routes)

        
        # (If it is an int, do nothing, just pass it on)

        return final_number_of_routes
    

    def set_time_limit_this_route(self, 
                                  route_time_limit: int | tuple[int] | list[int]) -> int:
        """
        Set the time limit for each route, depending on user input and 
        the map. 
        
        NOTE: output var is different from input var. This is because if 
        user provides a list for route_time_limit, assignment of 
        time_limit_this_route will be different for each route and 
        handled later in the code (i.e not in this function).
        """
        
        # For Holland map, the default time limit is 120 minutes
        # For the Netherlands map, the default time limit is 180 minutes
        if route_time_limit is None:
            if self.load.mapname == "Holland":
                time_limit_this_route = 120
            elif self.load.mapname == "Nationaal":
                time_limit_this_route = 180
            else:
                raise ValueError("Invalid mapname. Please use 'Holland' or 'Nationaal'.")
        
        # If an int is provided, just pass it on
        elif type(route_time_limit) is int:
            time_limit_this_route = route_time_limit
        
        # Else if route_time_limit is a tuple, choose a random value,
        # all routes will have this same time limit
        elif type(route_time_limit) is tuple:
            time_limit_this_route = np.random.choice(route_time_limit)

        # If a list was provided, assignment will be different for each 
        # route and handled later in the code
        else:
            time_limit_this_route = None


        return time_limit_this_route


    def setup_used_connection_and_station_tracking(self, 
                                                   starting_stations: str,
                                                   starting_station_list: None | list["Station"]
                                                   ) -> None:
        """ 
        Unused_connections starts off with all connections. Unused 
        connections will be moved to used connections when they are used.
        
        Unused stations starts off with all stations. Unused stations
        will be moved to used stations when they are used.

        In the case of "original_stations_only_soft", a list of used
        starting stations will be kept track of as well.
        """
        
        # 1. Setup tracking of used connections:
        self.used_connections: dict = dict()
        
        self.unused_connections: dict = dict()
        for connection in self.load.connections:

            # Save the names of the stations in this connection in a tuple
            station_names_as_tuple = tuple(sorted([connection[0].name, 
                                                   connection[1].name]))

            # Add the connection to the dict with the station name tuple as key
            self.unused_connections[station_names_as_tuple] = connection


        # 2. Setup tracking of used stations:

        # Internal list of stations
        self.unused_stations: list = list(self.load.stations.values()) 
        self.used_stations: list = list()


        # 3. If starting_stations is set to "original_stations_only_soft",
        # create list to keep track of used starting stations
        if starting_stations == "original_stations_only_soft":
            self.used_starting_stations = []


        # 4. If starting_station_list is provided and we draw without
        # replacement, make a deepcopy
        if starting_stations == "custom_list_without_replacement":
 
            # Make a copy of the list to avoid changing the original list
            self.starting_station_list_copy = copy.deepcopy(starting_station_list)


    def generate_solution(self,
                            final_number_of_routes: int,
                            route_time_limit: int,
                            time_limit_this_route: int,
                            starting_stations: str,
                            starting_station_list: list["Station"],
                            next_connection_choice: str,
                            original_connections_only: bool,
                            chance_of_early_route_end: bool
                          ) -> list[Route]:
        """
        Generate a solution with the given parameters.
        """
        
        # Solution is a list to store the various routes
        solution: list[Route] = []

        # While there are less than <final_number_of_routes> routes and 
        # there are still unused connections
        # i.e. for each route
        while(len(solution) < final_number_of_routes
               and len(self.unused_connections) > 0):
            
            # If route_time_limit is a list, pick random again for each route
            if type(route_time_limit) == list:
                time_limit_this_route = np.random.choice(route_time_limit)
            
            # Set the first station for this route (method depends on 
            # starting_stations argument)
            current_station = self.set_starting_station(starting_stations,
                                                    starting_station_list)

            # Create a new route with the given parameters
            new_route = self.create_a_route(current_station,
                                            time_limit_this_route,
                                            next_connection_choice,
                                            original_connections_only,
                                            chance_of_early_route_end)
            
            # And add it to the list of routes
            solution.append(new_route)


        # Return the generated routes
        return solution


    def set_starting_station(self, 
                             starting_stations: str, 
                             starting_station_list: list["Station"]
                             ) -> "Station":
        """
        Set a first station for this route (method depends on 
        starting_stations argument; lots of options!)
        """

        # If flag set to "fully_random", pick random from all stations
        if starting_stations == "fully_random":
            current_station = self.load.get_random_station()
        
        # If flag set to "original_stations_only_soft:
        # Pick random, but if another route starts at this station,
        # pick another
        elif starting_stations == "original_stations_only_soft":
            # Random pick ("do while" loop)
            current_station = self.load.get_random_station()
            
            # Pick again until a station is found that has not been 
            # used as a starting station in another route
            while current_station in self.used_starting_stations:
                current_station = self.load.get_random_station()

            # Add this station to the list of used starting stations
            self.used_starting_stations.append(current_station)

        # If "starting_stations" is set to "original_stations_only_hard", 
        # try to pick unused stations
        elif starting_stations == "original_stations_only_hard":

            # Plan A: pick a random unused station
            if len(self.unused_stations) > 0:
                current_station = random.choice(self.unused_stations)
            
            # Plan B: pick station with an unused connection
            else:
                random_unused_connection = random.choice(list(self.unused_connections.values()))
                random_index = random.choice([0, 1])
                
                current_station = random_unused_connection[random_index]   

        # If flag set to "custom_list_with_replacement", pick from the custom list
        elif starting_stations == "custom_list_with_replacement":
            current_station = random.choice(starting_station_list)

        # If flag set to "custom_list_without_replacement", 
        # pop from randomized version of custom list
        elif starting_stations == "custom_list_without_replacement":

            # Shuffle before each pop, just in case
            random.shuffle(self.starting_station_list_copy)
            
            # Pop the last station from the list
            current_station = self.starting_station_list_copy.pop()


        return current_station
    

    def create_a_route(self, current_station: "Station",
                       time_limit_this_route: int,
                       next_connection_choice: str,
                       original_connections_only: bool,
                       chance_of_early_route_end: bool    
                       ) -> Route:
        """
        Create a route with the given parameters.
        """
            
        # Create a new route
        route = Route()
        
        # While time is less than time_limit_this_route
        # i.e. for each connection in this route
        while route.time < time_limit_this_route: 
            
            # First: move this station to used stations
            # (if already moved do nothing)
            try:
                index = self.unused_stations.index(current_station)
                self.used_stations.append(self.unused_stations.pop(index))
            except ValueError:
                pass
            

            # Set next station (method depends on many parameters)
            # Function returns "break" if no next station is possible
            next_station: "Station" | str = self.set_next_station(
                                            current_station,
                                            route,
                                            next_connection_choice,
                                            original_connections_only,
                                            chance_of_early_route_end,
                                            time_limit_this_route)
            if next_station == "break":
                break
            

            # Add the connection to the route
            route.add_connection(current_station, 
                                    next_station, 
                                    current_station.get_connection_time(next_station))

            # Move the connection to used connections
            self.set_as_used(current_station, next_station)

            # Set the next station as the current station
            current_station = next_station


        return route


    def set_next_station(self, current_station: "Station",
                         route: Route,
                         next_connection_choice: str, 
                         original_connections_only: bool,
                         chance_of_early_route_end: bool,
                         time_limit_this_route: int) -> "Station":
        # Get connections of current station, sorted by duration
        # This is a queue of possible connections, with the shortest connection first
        connections = current_station.get_connections()

        # If chance_of_early_route_end is set to True, add a chance to 
        # end the route early. This is done by adding a connection to the
        # current station with a duration of 0 which when found will end 
        # the route. connections must only contain tuples with station 
        # and duration, otherwise bugs.
        if chance_of_early_route_end:
            connections.append(tuple([current_station, 0]))

        # Randomize the order of the connections (to add random choice next connection)
        # Only if the next_connection_choice is set to "random"
        if next_connection_choice == "random":
            random.shuffle(connections)
        # If set to "shortest", sort by duration
        else:
            # Sort list by duration
            connections.sort(key=lambda x: x[1])

        # If arg. original_connections_only set to True
        if original_connections_only:
            # Pop used connections from queue (until unused connection is found)
            while len(connections) > 0 and route.is_connection_used(current_station, connections[0][0]):
                connections.pop(0)
        
        # If adding this connection would exceed the time limit, remove this connection
        while len(connections) > 0 and route.time + connections[0][1] > time_limit_this_route:
            connections.pop(0)

        # If there are no unused connections left, end this route
        if len(connections) == 0:
            return "break"

        # For chance_of_early_route_end, check if connection with duration of 0 is next
        # This means the route will end here
        if chance_of_early_route_end:
            # If the connection has a duration of 0, end the route
            if connections[0][1] == 0:
                return "break"


        # First connection in queue is the next station
        next_station = connections[0][0]
        return next_station


    def set_as_used(self, current_station: "Station", 
                    next_station: "Station") -> None:
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




# Run and print results
if __name__ == "__main__":
    # Run the Random_Greedy algorithm on the Holland map
    # with default settings
    random_greedy = Random_Greedy("Holland")
    # list consisting of 4 lists with 2 stations each
    custom_starting_stations = [[random_greedy.load.stations["Alkmaar"], random_greedy.load.stations["Amsterdam Amstel"]], 
                                [random_greedy.load.stations["Rotterdam Alexander"], random_greedy.load.stations["Rotterdam Centraal"]], 
                                [random_greedy.load.stations["Castricum"], random_greedy.load.stations["Beverwijk"]], 
                                [random_greedy.load.stations["Schiphol Airport"], random_greedy.load.stations["Zaandam"]]]
    
    # results = random_greedy.run(starting_stations="custom_list_without_replacement", 
    #                             starting_station_list = custom_starting_stations, 
    #                             final_number_of_routes=2)
    
    results = random_greedy.run(route_time_limit = 40, final_number_of_routes= 3, starting_stations="original_stations_only_soft")

    for route in results:
        print(f"Route time: {route.time} minutes")
    # print(f"Number of routes: {len(results)}")