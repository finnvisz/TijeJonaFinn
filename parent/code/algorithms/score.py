from parent.code.algorithms.algorithm import Algorithm

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



