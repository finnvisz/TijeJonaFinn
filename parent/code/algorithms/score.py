from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.route import Route

class Score:
    def __init__(self, algorithm: "Algorithm", **algorithm_kwargs) -> None:
        self.algorithm = algorithm
        self.algorithm.run(**algorithm_kwargs)  # Ensure routes are generated
        self.total_connections_used = set() # all connections used (one way)
    
    def fraction_used(self) -> float:
        tot_connections_available = set(map(tuple, self.algorithm.load.connections)) # all connections available (one way)
        return len(self.algorithm.get_total_connections_used()) / (len(tot_connections_available))

    def calculate(self) -> float:
        K = self.fraction_used() * 10000 - (self.algorithm.number_of_routes() * 100 + self.algorithm.get_total_minutes())
        return K

# Calculate score from list of routes
def routes_score(routes: list[Route], map: str):

    # Check map
    if map == "Holland":
        total_connections = 28
    elif map == "Nationaal":
        total_connections = 89
    
    connections_used = set()
    total_minutes = 0
    for route in routes:
        for connection in route.get_connections_used():

            # Create reverse connection 
            reverse = (connection[1], connection[0], connection[2])

            # If reverse not in used, then add
            if reverse not in connections_used:
                connections_used.add(tuple(connection))

            # Add connection duration to total time
            total_minutes += connection[2]

    total_connections_used = len(connections_used)
    fraction = total_connections_used / total_connections
    number_of_routes = len(routes)

    score = fraction * 10000 - (number_of_routes * 100 + total_minutes) 

    return score 

