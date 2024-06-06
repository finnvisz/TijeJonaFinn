from random_algorithm import RandomAlgorithm

class Score:
    def __init__(self) -> None:
        self.algorithm = Algorithm()
        self.algorithm.make_trajects()  # Ensure trajects are generated
        self.Min = 0
        self.T = 0
        self.total_connections_used = set()

    def calculate(self) -> float:
        for traject in self.algorithm.trajects:
            self.Min += traject.time
            for con in traject.connections_used:
                # Ensure that each connection is a tuple
                self.total_connections_used.add(tuple(con))
            if traject.time != 0:
                self.T += 1

        tot_connections_available = set(map(tuple, self.algorithm.data.connections))
        print(tot_connections_available)
        p = len(self.total_connections_used) / len(tot_connections_available)
        K = p * 10000 - (self.T * 100 + self.Min)
        return K

score = Score()
print(score.calculate())

