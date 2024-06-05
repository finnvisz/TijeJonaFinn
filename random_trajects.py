#algoritm to make a random solution
import random
from typing import Any
from our_station import Station # type: ingore
from railnl import Railnl # type: ignore
from traject import Traject # type: ignore
import matplotlib.pyplot as plt # type: ingore

railnl = Railnl()
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
            traject.add(current_station, connection, int(current_station.connections[connection]))
            current_station = connection
        else:
            break
    number_of_trajects += 1
    print(traject.connections_used)
    trajects.append(traject)


plt.figure(figsize=(15, 15))
for tra in trajects:
    for connection in tra.connections_used:
        x_values = [railnl.stations[connection[0]].long, railnl.stations[connection[1]].long]
        y_values = [railnl.stations[connection[0]].lat, railnl.stations[connection[1]].lat]
        plt.plot(x_values, y_values, marker='o', linestyle='-')
        # Annotate start station
        plt.text(railnl.stations[connection[0]].long, railnl.stations[connection[0]].lat, connection[0], ha='center')
        # Annotate end station
        plt.text(railnl.stations[connection[1]].long, railnl.stations[connection[1]].lat, connection[1], ha='center')
plt.title('Railway Network')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.savefig('railway_network.png')
plt.close()