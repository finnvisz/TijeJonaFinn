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
        self.routes = algorithm.routes

        # Debug: Print initial routes and their details
        print(f"Initial routes: {self.routes}")

        self.best_score = self.calculate_new_score(self.routes)

        # Debug: Print initial score calculation
        print(f"Initial score: {self.best_score}")

    def new_connections_used(self, routes) -> set:
        new_connections = set()
        for route in routes:
            for connection_list in route.get_connections_used():
                connection = tuple(connection_list)
                reverse_connection = (connection[1], connection[0], connection[2])
                if reverse_connection not in new_connections:
                    new_connections.add(connection)
        return set(new_connections)

    def new_total_minutes(self, routes) -> int:
        total_minutes = 0
        for route in routes:
            total_minutes += route.time
        return total_minutes
    
    def generate_random_route(self) -> "Route":
        time_used = 0
        route = Route()
        current_station = self.load.get_random_station()
        while current_station.has_connections():
            connections = list(current_station.connections_dict())
            connection = random.choice(connections)
            duration = int(current_station.connection_duration(connection))
            total = time_used + duration
            if total < 120:
                time_used = total
                route.add_connection(current_station, connection, duration)
            else:
                break
        return route
        
    def add_random_route(self, routes):
        new_routes = copy.deepcopy(routes)
        new_route = self.generate_random_route() 
        new_routes.append(new_route)
        return new_routes

    def remove_random_route(self, routes):
        if len(routes) > 1:
            new_routes = copy.deepcopy(routes)
            new_routes.pop(random.randint(0, len(new_routes) - 1))
            return new_routes
        return routes

    def calculate_new_score(self, routes) -> float:
        p = len(self.new_connections_used(routes)) / len(self.load.get_total_connections())
        T = len(routes)
        return p * 10000 - (T * 100 + self.new_total_minutes(routes))

    def run(self) -> None:
        iterations = 10000
        start_score = self.best_score
        print(f"{iterations} iteraties")
        print(f"Start score: {round(start_score, 1)}")

        for i in range(iterations):
            new_routes = copy.deepcopy(self.routes)

            new_routes = self.remove_random_route(new_routes)
            new_routes = self.add_random_route(new_routes)
                
            new_score = self.calculate_new_score(new_routes)
            
            if new_score > self.best_score:
                self.routes = new_routes
                self.best_score = new_score
                print(f"Iteratie {i}, New score: {round(new_score, 1)}")

        print(f"Start score: {start_score}, End score: {self.best_score}")

if __name__ == "__main__":
    data = RailNL("Holland")

    # Test Hillclimber algorithm with RandomAlgorithm as starting state
    random_alg = RandomAlgorithm(data)
    random_alg.run()
    hillclimber_alg = Hillclimber(data, random_alg)
    hillclimber_alg.run()
    hillclimber_alg.make_picture() 

    # for i, route in enumerate(hillclimber_alg.routes):
    #     print(f"Route {i} (Time: {route.time} minutes):")
    #     for connection in route.connections_used:
    #         print(f"  {connection[0]} -> {connection[1]} ({connection[2]} minutes)")
    #     print()

    for i, route in enumerate(hillclimber_alg.routes):
        print(f"route {i+1},", end = " ")
        print(route.stations) 

