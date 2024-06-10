from typing import Any
from parent.code.classes.railnl import RailNL
import matplotlib.pyplot as plt 

class Algorithm:
    """Algorithm script finding 7 random railroad routes."""

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

        num_routes = len(self.routes)
        num_cols = 2  # Number of columns for subplots
        num_rows = (num_routes + num_cols - 1) // num_cols  # Calculate number of rows

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(40, 40))
        fig.suptitle('Railway Network')

        for ax in axs.flat:
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Y Coordinate')
            ax.grid(False)  # Remove grid from all subplots

        for connection in self.load.connections:
            station1, station2 = connection
            x_values = [self.load.stations[station1.name].long, self.load.stations[station2.name].long]
            y_values = [self.load.stations[station1.name].lat, self.load.stations[station2.name].lat]
            for ax in axs.flat:
                ax.plot(x_values, y_values, marker='o', linestyle='-', color='red')
                ax.text(self.load.stations[station1.name].long, self.load.stations[station1.name].lat, station1.name, ha='center')
                ax.text(self.load.stations[station2.name].long, self.load.stations[station2.name].lat, station2.name, ha='center')

        for i, route in enumerate(self.routes):
            row = i // num_cols
            col = i % num_cols
            ax = axs[row, col]
            for connection in route.connections_used:
                x_values = [self.load.stations[connection[0]].long, self.load.stations[connection[1]].long]
                y_values = [self.load.stations[connection[0]].lat, self.load.stations[connection[1]].lat]
                ax.plot(x_values, y_values, marker='o', linestyle='-', color=colors[i % len(colors)])
            ax.set_title(f'Route {i+1}')  # Set title for each subplot

        # Leave last subplots empty if needed
        for i in range(num_routes, num_cols * num_rows):
            row = i // num_cols
            col = i % num_cols
            fig.delaxes(axs[row, col])

        plt.tight_layout()
        plt.savefig('railway_network.png')
        plt.close()