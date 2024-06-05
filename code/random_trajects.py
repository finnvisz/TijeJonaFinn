"""Algorithm script finding 7 random railroad routes."""

import random
from typing import Any
from our_station import Station # type: ignore
from railnl import Railnl # type: ignore
from traject import Traject # type: ignore
import matplotlib.pyplot as plt # type: ignore

railnl = Railnl() # Load station data 
trajects: list[Any] = []

for _ in range(6):
    time_used = 0
    current_station = random.choice(list(railnl.stations_dictionary().values()))
    traject = Traject()

    while True:

        # Break if current_station has no connections
        if not current_station.has_connections():
            break 
        
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
    trajects.append(traject)

# maak een plaatje
plt.figure(figsize=(15, 15))
for tra in trajects:
    for connection in tra.connections_used:
        x_values = [railnl.stations[connection[0]].long, railnl.stations[connection[1]].long]
        y_values = [railnl.stations[connection[0]].lat, railnl.stations[connection[1]].lat]
        plt.plot(x_values, y_values, marker='o', linestyle='-')
        # Annotate stations
        plt.text(railnl.stations[connection[0]].long, railnl.stations[connection[0]].lat, connection[0], ha='center')
        plt.text(railnl.stations[connection[1]].long, railnl.stations[connection[1]].lat, connection[1], ha='center')
plt.title('Railway Network')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.savefig('railway_network.png')
plt.close()