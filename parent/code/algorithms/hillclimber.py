import random
import copy
import matplotlib.pyplot as plt

from parent.code.algorithms.algorithm import Algorithm
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.score import routes_score
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
from parent.code.experiments.statistics import append_scores_to_csv

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
    def __init__(self, start_position: list[Route], 
                 maprange: str = "Holland") -> None:
        """
        Initialize a HillClimber object.

        - Pre: Hillclimber object is initialized with a RailNL object, 
        a set of routes to start off with and `maprange` is correctly 
        set to "Holland" or "Nationaal".

        - Post: Hillclimber is initialized with the given parameters, 
        and ready to run.

        Args:
            - `start_position` `(list[Route])`: The set of routes to 
            start off with.
            - `maprange` `(str)`: The map to run the algorithm on 
            ("Holland" or "Nationaal")
        """
        # Load RailNL data with given maprange
        self.load = RailNL(maprange)
        super().__init__(self.load)
        
        self.start_score = 0
        self.routes: list[Route] = start_position
        self.scores = []
        self.maprange = self.load.mapname
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
    
    def improve_routes(self, routes: list[Route]) -> list[Route]:
        """Removes the first/last connection (head/tail) of a route if
        it is already used somewhere else
        
        Post: Returns an updated list of Route object, hopefully with 
        less stupid extra connections
        """
        updated_routes = []

        for route in routes:
            # Check head
            if len(route.connections_used) > 0:
                first_conn = route.connections_used[0]
                first_conn_reverse = (first_conn[1], first_conn[0], first_conn[2])

                total_conn = self.get_total_connections_used()

                if first_conn not in total_conn and first_conn_reverse not in total_conn:
                    route.connections_used.pop(0)
                    route.stations.pop(0)

            # Check tail
            if len(route.connections_used) > 0:
                last_conn = route.connections_used[-1]
                last_conn_reverse = (last_conn[1], last_conn[0], last_conn[2])

                total_conn = self.get_total_connections_used()

                if last_conn not in total_conn and last_conn_reverse not in total_conn:
                    route.connections_used.pop(-1)
                    route.stations.pop(-1)

            # Append route if it still has connections
            if route.get_connections_used():
                updated_routes.append(route)

        return updated_routes

        

    def run(self, iterations: int, simulated_annealing=False, cap=10**99,
            
            log_csv: str | None = None) -> list[Route]:
        """
        Run the Hillclimber optimization for a specified number of iterations.

        Pre: 


        Post: The Hillclimber algorithm runs for the specified number
          of iterations, optimizing the routes.

        Args:
        
        Algorithm settings:
        - iterations: max number of iterations to run the algorithm.
        - simulated_annealing: if True, accept worse scores sometimes
        - cap: if True, stop running when there hasn't been a change in a while

        Data collection settings:
        - log_csv: if not None, append score per iteration to specified 
        csv file (`hillclimber_data.csv`). Default dir is `parent`, so 
        set a full path yourself.
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

            new_routes = self.improve_routes(new_routes)

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

        
        # When done:
        # If set, log score per iteration to csv file
        if log_csv is not None:
            append_scores_to_csv(self.scores, log_csv, custom_file_path=True)

        # Print summary
        print(f"Start score: {self.start_score}, End score: {self.best_score}")

        # And return the found solution
        return self.routes


# Example/test usage
if __name__ == "__main__":
    maprange = "Nationaal"
    # Test Hillclimber algorithm with RandomAlgorithm as starting state
    random_alg = Random_Greedy(maprange).run(
                            final_number_of_routes=(14),
                            route_time_limit=[180],
                            starting_stations = 'original_stations_only_hard')
    hillclimber_alg = Hillclimber(random_alg, maprange).run(100)