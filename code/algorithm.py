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

    
    def run(self):
        raise NotImplementedError("Subclasses should implement this!")


    def make_picture(self):
        self.run()
        plt.figure(figsize=(15, 15))
        for traject in self.trajects:
            for connection in traject.connections_used:
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




