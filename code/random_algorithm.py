from algorithm import Algorithm
from load import Load_in
from traject import Traject
import random

class RandomAlgorithm:
    def __init__(self) -> None:
        self.algorithm = Algorithm()
        self.trajects = self.algorithm.trajects
        self.data = Load_in("Holland")

    def make_trajects(self) -> None:
        for _ in range(7):
            time_used = 0
            current_station = random.choice(list(self.data.stations_dictionary().values()))
            traject = Traject()

            # Break when no connections are left in current station
            while current_station.has_connections():
                # Find random connection from current_station
                connection = random.choice(list(current_station.connecting_stations()))

                # Calculate new total duration of route
                duration = int(current_station.connection_duration(connection))
                total = time_used + duration

                # Continue if connection is possible considering time_used
                if total <= 120:
                    time_used = total
                    traject.add(current_station, connection, duration)
                    current_station = connection

                # Else consider traject finished
                else:
                    break
            self.trajects.append(traject)

