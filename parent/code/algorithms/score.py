from parent.code.algorithms.algorithm import Algorithm

class Score:
    def __init__(self, algorithm: "Algorithm") -> None:
        self.algorithm = algorithm
        self.algorithm.run()  # Ensure routes are generated
        self.Min = 0
        self.total_connections_used = set() # all connections used (one way)

    def calculate(self) -> float:
        K = 0
        for route in self.algorithm.routes:
            self.Min += route.time
            for connection_list in route.get_connections_used():
                connection = tuple(connection_list)  # Ensure connection is a tuple
                reverse_connection = (connection[1], connection[0], connection[2])  # Create the reverse connection tuple
                if reverse_connection not in self.total_connections_used:
                    self.total_connections_used.add(connection)

        tot_connections_available = set(map(tuple, self.algorithm.load.connections)) # all connections available (one way)
        p = len(self.total_connections_used) / (len(tot_connections_available))
        T = self.algorithm.number_of_routes()
        print(f"p: {p}")
        print(f"T: {T}")
        print(f"Min: {self.Min}")
        K = p * 10000 - (T * 100 + self.Min)
        return K


