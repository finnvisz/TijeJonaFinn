#algoritm to make a random solution
import random
from typing import Any
from our_station import Station
from railnl import Railnl
from traject import Traject

# load in all the stations and connections
railnl = Railnl()
railnl.load_stations()
railnl.load_connections()

number_of_trajects = 0
trajects: list[Any] = []

while number_of_trajects < 7:
    time_used = 0
    current_station = random.choice(list(railnl.stations.values()))
    traject = Traject()

    while True:
        # kies random verbinding uit de connections die je hebt
        if not current_station.connections:
            # If there are no connections available, break out of the loop
            break
        connection = random.choice(list(current_station.connections.keys()))
        # tel de duur van die verbinding op bij time_used als dat <= 120 is
        if time_used + int(current_station.connections[connection]) <= 120:
            time_used += int(current_station.connections[connection])
            traject.add_connection(current_station, connection, int(current_station.connections[connection]))
            current_station = connection
        else:
            break
    number_of_trajects += 1
    print(traject.connections_used)
    trajects.append(traject)
