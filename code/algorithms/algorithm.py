"""Algorithm script finding 7 random railroad routes."""

from typing import Any
from ..classes import railnl
import matplotlib.pyplot as plt # type: ignore
import matplotlib.cm as cm
import numpy as np

class Algorithm:
    def __init__(self, load: RailNL) -> None:
        self.load = load
        self.trajects: list[Any] = []

    
    def run(self):
        raise NotImplementedError("Subclasses should implement this!")


    def make_picture(self):
        self.run()
        num_trajects = len(self.trajects)
        colors = plt.get_cmap('tab10', num_trajects)  # 'tab10' colormap has 10 distinct colors

        plt.figure(figsize=(15, 15))
        for idx, traject in enumerate(self.trajects):
            color = colors(idx)
            for connection in traject.connections_used:
                x_values = [self.load.stations[connection[0]].long, self.load.stations[connection[1]].long]
                y_values = [self.load.stations[connection[0]].lat, self.load.stations[connection[1]].lat]
                plt.plot(x_values, y_values, marker='o', linestyle='-', color=color)
                plt.text(self.load.stations[connection[0]].long, self.load.stations[connection[0]].lat, connection[0], ha='center')
                plt.text(self.load.stations[connection[1]].long, self.load.stations[connection[1]].lat, connection[1], ha='center')
        plt.title('Railway Network')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.savefig('railway_network.png')
        plt.close()




