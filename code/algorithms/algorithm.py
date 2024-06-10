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

    def number_of_routes(self) -> int:
        return len(self.routes)
    
    def make_picture(self):
        if not self.routes:
            self.run()
        colors = ['green', 'blue', 'yellow', 'pink', 'purple', 'black', 'violet']

        plt.figure(figsize=(20, 20))
        for connection in self.load.connections:
            station1, station2 = connection
            x_values = [self.load.stations[station1.name].long, self.load.stations[station2.name].long]
            y_values = [self.load.stations[station1.name].lat, self.load.stations[station2.name].lat]
            plt.plot(x_values, y_values, marker='o', linestyle='-', color='red')    
            plt.text(self.load.stations[station1.name].long, self.load.stations[station1.name].lat, station1.name, ha='center')
            plt.text(self.load.stations[station2.name].long, self.load.stations[station2.name].lat, station2.name, ha='center')
        for i, route in enumerate(self.routes):
            for connection in route.connections_used:
                x_values = [self.load.stations[connection[0]].long, self.load.stations[connection[1]].long]
                y_values = [self.load.stations[connection[0]].lat, self.load.stations[connection[1]].lat]
                plt.plot(x_values, y_values, marker='o', linestyle='-', color=colors[0])
        plt.title('Railway Network')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.savefig('railway_network.png')
        plt.close()

    




