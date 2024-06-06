import random
from typing import Any
from traject import Traject
from load import Load_in
import matplotlib.pyplot as plt

class Algorithm:
    def __init__(self) -> None:
        self.load = Load_in()
        self.trajects: list[Any] = []
    

    def make_picture(self) -> None:
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



