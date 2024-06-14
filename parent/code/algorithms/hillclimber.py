import random
import copy

from parent.code.algorithms.algorithm import Algorithm
from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.score import Score
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route

class Hillclimber(Algorithm):
    def __init__(self, load: RailNL, algorithm: Algorithm) -> None:
        super().__init__(load)
        self.load = load
        self.algorithm = algorithm
        self.algorithm.run()
        self.routes = copy.deepcopy(self.algorithm.routes)
        self.score = Score(self.algorithm).calculate()
        self.total_minutes = self.get_total_minutes()
        self.total_connections_used = self.get_total_connections_used()

    def new_connections_used(self, routes):
        new_connections_used = set()
        for route in routes:
            for connection_list in route.get_connections_used():

                # Ensure connection is a tuple
                connection = tuple(connection_list)  

                # Create the reverse connection tuple
                reverse_connection = (connection[1], connection[0], connection[2]) 

                # check if the connection has already been used, 
                # add the connection if not
                if reverse_connection not in new_connections_used:
                    new_connections_used.add(connection)
        return new_connections_used
    
    def new_total_minutes(self, routes) -> int:
        return sum(route.time for route in routes)


    def calculate_new_score(self, routes) -> float:
        p = len(self.new_connections_used(routes)) / len(self.load.get_total_connections())
        T = len(routes)
        return p * 10000 - (T * 100 + self.new_total_minutes(routes))

    def add_random_route(self, routes):
        new_routes = copy.deepcopy(routes)
        current_station = self.load.get_random_station()
        route = Route()
        time_used = 0

        while current_station.has_connections():
            # Debugging: print the current station and its connections
            print(f"Current station: {current_station.name}")
            print(f"Connections: {current_station.connections_dict()}")

            # Choose a random connection
            connection, duration = random.choice(list(current_station.connections_dict().items()))

            # # Debugging: print the chosen connection and duration
            # print(f"Chosen connection: {connection}, duration: {duration}")

            if time_used + duration <= 120:
                route.add_connection(current_station, connection, duration)
                current_station = connection  # Assuming connection is the next station
                time_used += duration
            else:
                break

        if route.connections:
            new_routes.append(route)
        return new_routes


    def run(self, iterations: int = 10) -> None:
        
        print(f"Initial score: {self.score}")

        for iteration in range(iterations):
            print(f"Iteration: {iteration + 1}")
            if not self.routes:
                print("No routes to change!")
                return

            new_routes = copy.deepcopy(self.routes)
            route_to_remove = random.choice(new_routes)
            new_routes.remove(route_to_remove)

            new_score = self.calculate_new_score(new_routes)

            if new_score > self.score:
                print(f"New score: {new_score}")
                self.routes = new_routes
                self.score = new_score
                self.total_minutes = sum(route.time for route in new_routes)
                self.total_connections_used = self.new_connections_used(new_routes)
            else:
                new_routes = self.add_random_route(new_routes)
                new_score = self.calculate_new_score(new_routes)

                if new_score > self.score:
                    print(f"New score: {new_score}")
                    self.routes = new_routes
                    self.score = new_score
                    self.total_minutes = sum(route.time for route in new_routes)
                    self.total_connections_used = self.new_connections_used(new_routes)
                else:
                    print(f"No change made, current score: {self.score}")

if __name__ == "__main__":
    data = RailNL("Holland")

    # Test Hillclimber algorithm with RandomAlgorithm as starting state
    hillclimber_alg = Hillclimber(data, RandomAlgorithm(data))
    hillclimber_alg.run()
    hillclimber_alg.make_picture()

# This algorithm is trash :)
