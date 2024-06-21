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
        self.start_score = 0
        self.algorithm = algorithm
        self.routes = algorithm.routes
        self.scores = []
        self.maprange = maprange
        self.best_score = routes_score(self.routes, self.maprange)
        

    def generate_random_route(self) -> Route:
        """Generate a random route within the rail network.

        Post: Returns a Route object with a random set of connections.
        """
        if self.maprange == "Holland":
            max_time = 120
        elif self.maprange  == "Nationaal":
            max_time = 180

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
            if total < max_time:
                time_used = total
                route.add_connection(current_station, connection, duration)
                current_station = connection  # Move to the next station
            else:
                break
        return route
        

    def add_random_route(self, routes: list[Route]) -> list[Route]:
        """Add a random route to the list of routes.

        Pre: routes (List[Route]): List of current routes.
        Post: Returns an updated list of Route objects including a new random route.
        """
        # We want to be able to go back so we make a deepcopy
        new_routes = copy.deepcopy(routes)

        # generate a random route
        new_route = self.generate_random_route()

        # add it to the list of routes
        new_routes.append(new_route)
        return new_routes


    def remove_random_route(self, routes: list[Route]) -> list[Route]:
        """Remove a random route from the list of routes.

        Post: Returns an updated list of Route objects with one less route if at least one route exists.
        """
        if len(routes) > 1: # check list is not empty
            new_routes = copy.deepcopy(routes)

            #remove a random route from the list
            new_routes.pop(random.randint(0, len(new_routes) - 1))
            return new_routes
        return routes


    def run(self, iterations: int, simulated_annealing=False, cap=10**99) -> None:
        """
        Run the Hillclimber optimization for a specified number of iterations.

        Pre: 
        - iterations (int) is the number of iterations to run the optimization.
        - if cap=True then it stops running when there hasn't been a change in a while
        - If simulated_annealing=True, then it accepts worse scores sometimes


        Post: The Hillclimber algorithm runs for the specified number of iterations, optimizing the routes.
        """
        self.iterations = iterations
        self.start_score = self.best_score
        print(f"start score: {self.start_score}")
        count_no_change = 0
        self.simulated_annealing = simulated_annealing
        self.cap = cap

        for i in range(self.iterations):
            # each iteration, remove a random route and add another
            new_routes = copy.deepcopy(self.routes)

            new_routes = self.remove_random_route(new_routes)
            new_routes = self.add_random_route(new_routes)

            new_score = routes_score(new_routes, self.maprange)

            accept_new = False
            if self.simulated_annealing == True:
                # Simulated annealing, always accept a higher or equal score
                temperature = self.best_score / 10000
                if random.random() < 2 ** (temperature * (new_score - self.best_score)):
                    accept_new = True
            else:
                if new_score > self.best_score:
                    accept_new = True

            
            if accept_new:
            #if new_score > self.best_score:
                # use the new routes next iteration
                self.routes = new_routes
                self.best_score = new_score
                self.scores.append(new_score)

                # if there is an empty route, remove it
                for route in self.routes:
                    if route.get_connections_used() == []:
                        self.routes.pop(self.routes.index(route))
                
                count_no_change = 0
                print(f"iteratie {i}, score {new_score}")

            else:
                # use the old routes next iteration
                self.scores.append(self.best_score)
                count_no_change += 1

            if self.cap < self.iterations:
                if count_no_change == self.cap:
                    print("Too long no change")
                    break

        print(f"Start score: {self.start_score}, End score: {self.best_score}")


# Example/test usage
if __name__ == "__main__":
    data = RailNL("Nationaal")

    # Test Hillclimber algorithm with RandomAlgorithm as starting state
    random_alg = Random_Greedy(data)
    random_alg.run()
    hillclimber_alg = Hillclimber(data, random_alg, "Nationaal")
    hillclimber_alg.run(10000)

    # Show routes
    for i, route in enumerate(hillclimber_alg.routes):
        print(f"route {i+1} (Time: {route.time} minutes):,")
        print(route.stations) 

    # Plot iteration vs. score
    plt.plot(hillclimber_alg.scores)
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Start: Random prefer unused, Hillclimber Algorithm Holland')
    plt.savefig("/home/finnvisz/TijeJonaFinn/parent/code/experiments/plots/score_vs_iteration.png")