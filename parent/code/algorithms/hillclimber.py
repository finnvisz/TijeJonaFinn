import random
import copy
from parent.code.algorithms.algorithm import Algorithm
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.score import routes_score
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
import matplotlib.pyplot as plt

class Hillclimber(Algorithm):
    """Hillclimber algorithm to optimize train routes.

    Attributes:
    load (RailNL): Rail network object.
    algorithm (Algorithm): Initial algorithm for route generation.
    routes (List[Route]): List of initial routes.
    scores (List[float]): List to keep track of scores over iterations.
    maprange: Holland or Nationaal
    best_score (float): Best score achieved during optimization.
        
    """
    def __init__(self, load: RailNL, algorithm: Algorithm, maprange: str) -> None:
        super().__init__(load)
        self.load = load
        self.algorithm = algorithm
        self.routes = algorithm.routes
        self.scores = []
        self.maprange = maprange
        self.best_score = routes_score(self.routes, self.maprange)
        
    def generate_random_route(self) -> Route:
        """
        Generate a random route within the rail network.

        Returns:
            Route: A randomly generated route.

        Pre: `load` is initialized and contains station data.
        Post: Returns a Route object with a random set of connections.
        """
        time_used = 0
        route = Route()
        current_station = self.load.get_random_station()
        while current_station.has_connections():
            if random.random() < 0.05:  # Stop early with 5% probability
                break
            connections = list(current_station.connections_dict().keys())
            connection = random.choice(connections)
            duration = int(current_station.connection_duration(connection))
            total = time_used + duration
            if total < 120:
                time_used = total
                route.add_connection(current_station, connection, duration)
                current_station = connection  # Move to the next station
            else:
                break
        return route
        
    def add_random_route(self, routes: list[Route]) -> list[Route]:
        """
        Add a random route to the list of routes.

        Args:
            routes (List[Route]): List of current routes.

        Returns:
            List[Route]: Updated list of routes with an additional random route.

        Pre: `routes` is a valid list of Route objects.
        Post: Returns an updated list of Route objects including a new random route.
        """
        new_routes = copy.deepcopy(routes)
        new_route = self.generate_random_route()
        new_routes.append(new_route)
        return new_routes

    def remove_random_route(self, routes: list[Route]) -> list[Route]:
        """
        Remove a random route from the list of routes.

        Args:
            routes (List[Route]): List of current routes.

        Returns:
            List[Route]: Updated list of routes with one random route removed.

        Pre: `routes` is a valid list of Route objects.
        Post: Returns an updated list of Route objects with one less route if more than one route exists.
        """
        if len(routes) > 1:
            new_routes = copy.deepcopy(routes)
            new_routes.pop(random.randint(0, len(new_routes) - 1))
            return new_routes
        return routes

    def run(self, iterations: int) -> None:
        """
        Run the Hillclimber optimization for a specified number of iterations.

        Pre: iterations (int) is the number of iterations to run the optimization.
        Post: The Hillclimber algorithm runs for the specified number of iterations, optimizing the routes.
        """
        self.iterations = iterations
        start_score = self.best_score
        print(f"{self.iterations} iterations")
        print(f"Start score: {round(start_score, 1)}")

        for i in range(self.iterations):
            new_routes = copy.deepcopy(self.routes)

            new_routes = self.remove_random_route(new_routes)
            new_routes = self.add_random_route(new_routes)

            new_score = routes_score(new_routes, self.maprange)

            if new_score > self.best_score:
                self.routes = new_routes
                self.best_score = new_score
                self.scores.append(new_score)
                print(f"Iteration {i}, New score: {round(new_score, 1)}")
            else:
                self.scores.append(self.best_score)

        print(f"Start score: {start_score}, End score: {self.best_score}")

if __name__ == "__main__":
    data = RailNL("Holland")

    # Test Hillclimber algorithm with RandomAlgorithm as starting state
    random_alg = Random_Greedy(data)
    random_alg.run(starting_stations="prefer_unused")
    hillclimber_alg = Hillclimber(data, random_alg, "Holland")
    hillclimber_alg.run(10000)
    # hillclimber_alg.make_picture() 

    # Show routes
    for i, route in enumerate(hillclimber_alg.routes):
        print(f"route {i+1} (Time: {route.time} minutes):,")
        print(route.stations) 

    # Plot iteration vs. score
    plt.plot(hillclimber_alg.scores)
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Start: Random prefer unused, Hillclimber Algorithm Holland')
    plt.savefig("/home/finnvisz/TijeJonaFinn/parent/code/experiments/plots/random_prefer_unused_hollans_score_vs_iteration.png")

    

