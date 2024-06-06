"""Algorithm script finding 7 random railroad routes."""

import random
from typing import Any
from our_station import Station # type: ignore
from load import Load_in # type: ignore
from traject import Traject # type: ignore
import matplotlib.pyplot as plt # type: ignore

class Algorithm:
    def __init__(self) -> None:
        self.load = Load_in("Holland")
        self.trajects: list[Any] = []


    def random_algorithm(self):
        for _ in range(7):
            time_used = 0
            current_station = random.choice(list(self.load.stations_dictionary().values()))
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

            print(traject.connections_used)
            self.trajects.append(traject)


    def make_picture(self):
        self.random_algorithm()
        plt.figure(figsize=(15, 15))
        for tra in self.trajects:
            for connection in tra.connections_used:
                x_values = [self.load.stations[connection[0]].long, self.load.stations[connection[1]].long]
                y_values = [self.load.stations[connection[0]].lat, self.load.stations[connection[1]].lat]
                plt.plot(x_values, y_values, marker='o', linestyle='-')
                # Annotate stations
                plt.text(self.load.stations[connection[0]].long, self.load.stations[connection[0]].lat, connection[0], ha='center')
                plt.text(self.load.stations[connection[1]].long, self.load.stations[connection[1]].lat, connection[1], ha='center')
        plt.title('Railway Network')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.savefig('railway_network.png')
        plt.close()

    def calculate_K(self) -> int:
        T = 0
        Min = 0
        total_connections_used = set()

        for tra in self.trajects:
            Min += tra.time
            for con in tra.connections_used:
                # Ensure that each connection is a tuple
                total_connections_used.add(tuple(con))
            if tra.time != 0:
                T += 1

        tot_connections_available = set(self.load.connections)
        p = len(total_connections_used) / len(tot_connections_available)
        K = p * 10000 - (T * 100 + Min)
        return K


algorithm = Algorithm()
algorithm.make_picture()
print(algorithm.calculate_K())


