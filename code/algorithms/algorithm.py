"""Algorithm script finding 7 random railroad routes."""

from typing import Any
from ..classes.railnl import RailNL
import matplotlib.pyplot as plt # type: ignore
import matplotlib.cm as cm
import numpy as np

class Algorithm:
    def __init__(self, load: RailNL) -> None:
        self.load = load
        self.routes: list[Any] = []

    
    def run(self):
        raise NotImplementedError("Subclasses should implement this!")


    def make_picture(self):
        self.run()
        num_trajects = len(self.routes)

        plt.figure(figsize=(15, 15))
        for connection in self.load.connections:
            station1, station2 = connection
            x_values = [self.load.stations[station1.name].long, self.load.stations[station2.name].long]
            y_values = [self.load.stations[station1.name].lat, self.load.stations[station2.name].lat]
            plt.plot(x_values, y_values, marker='o', linestyle='-', color='red')
            plt.text(self.load.stations[station1.name].long, self.load.stations[station1.name].long, station1.name, ha='center')
            plt.text(self.load.stations[station2.name].long, self.load.stations[station2.name].long, station2.name, ha='center')
        for route in self.routes:
            for connection in route.connections_used:
                x_values = [self.load.stations[connection[0]].long, self.load.stations[connection[1]].long]
                y_values = [self.load.stations[connection[0]].lat, self.load.stations[connection[1]].lat]
                plt.plot(x_values, y_values, marker='o', linestyle='-', color='green')
        plt.title('Railway Network')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.savefig('railway_network.png')
        plt.close()




