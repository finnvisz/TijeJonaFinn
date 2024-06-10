from .algorithm import Algorithm
from .random_algorithm import RandomAlgorithm

class Score:
    def __init__(self, algorithm: "Algorithm") -> None:
        self.algorithm = algorithm
        self.algorithm.run()  # Ensure trajects are generated
        self.Min = 0
        self.T = 0
        self.total_connections_used = set()

    def calculate(self) -> float:
        for route in self.algorithm.routes:
            self.Min += route.time
            for connection in route.connections_used:
                # Ensure that each connection is a tuple
                self.total_connections_used.add(tuple(connection))
            if route.time != 0:
                self.T += 1

        tot_connections_available = set(map(tuple, self.algorithm.load.connections))
        p = len(self.total_connections_used) / len(tot_connections_available)
        K = p * 10000 - (self.T * 100 + self.Min)
        return K

