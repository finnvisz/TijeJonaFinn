from parent.code.algorithms.algorithm import Algorithm

class Score:
    def __init__(self, algorithm: "Algorithm") -> None:
        self.algorithm = algorithm
        self.algorithm.run()  # Ensure routes are generated
        self.total_connections_used = set() # all connections used (one way)

    def calculate(self) -> float:
        Min = self.algorithm.get_total_minutes()
        tot_connections_available = set(map(tuple, self.algorithm.load.connections)) # all connections available (one way)
        p = len(self.algorithm.get_total_connections_used()) / (len(tot_connections_available))
        T = self.algorithm.number_of_routes()

        K = p * 10000 - (T * 100 + Min)
        return K



