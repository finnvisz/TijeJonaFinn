class Score:
    def __init__(self) -> None:
        self.Min = 0
        self.T = 0
        self.total_connections_used = set()

        for traject in self.trajects:
            self.Min += traject.time
            for con in tra.connections_used:
                # Ensure that each connection is a tuple
                total_connections_used.add(tuple(con))
            if tra.time != 0:
                T += 1

        tot_connections_available = set(self.load.connections)
        p = len(total_connections_used) / len(tot_connections_available)
        K = p * 10000 - (T * 100 + Min)
        return K