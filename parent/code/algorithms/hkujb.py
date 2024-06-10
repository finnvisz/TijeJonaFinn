from .algorithm import Algorithm

class Score:
    def __init__(self, algorithm: "Algorithm") -> None:
        self.algorithm = algorithm
        self.algorithm.run()
        self.Min = 0
        self.total_connections_used = set()

    def calculate(self) -> float:
        for route in self.algorithm.routes:
            self.Min += route.time
            for connection in route.connections_used:
                stat1, stat2, duur = connection
                reverse_connection = (stat2, stat1, duur)
                if reverse_connection not in self.total_connections_used and connection not in self.total_connections_used:
                    self.total_connections_used.add(tuple(connection))
        tot_connections_available = set(map(tuple, self.algorithm.load.connections))
        p = len(self.total_connections_used) / len(tot_connections_available)
        T = len(self.algorithm.routes)
        print(f"Unique Connections Used: {self.total_connections_used}")
        print(f"Total Connections Available: {tot_connections_available}")
        print(f"p: {p}, T: {T}, Min: {self.Min}")
        K = p * 10000 - (T * 100 + self.Min)
        return K
