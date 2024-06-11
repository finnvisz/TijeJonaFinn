import matplotlib.pyplot as plt 

class Visualise():
    
    def make_picture(self):
            if not self.routes:
                self.run()

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
                station1_o = self.load.stations[station1.name]
                station2_o = self.load.stations[station2.name]

                x_values = [station1_o.long, station2_o.long]
                y_values = [station1_o.lat, station2_o.lat]
                for ax in axs.flat:
                    ax.plot(x_values, y_values, marker='o', linestyle='-', color='red')
                    ax.text(station1_o.long, station1_o.lat, station1.name, ha='center')
                    ax.text(station2_o.long, station2_o.lat, station2.name, ha='center')

            for i, route in enumerate(self.routes):
                row = i // num_cols
                col = i % num_cols
                ax = axs[row, col]
                for connection in route.connections_used:
                    con_0 = self.load.stations[connection[0]]
                    con_1 = self.load.stations[connection[1]]

                    x_values = [con_0.long, con_1.long]
                    y_values = [con_0.lat, con_1.lat]
                    ax.plot(x_values, y_values, marker='o', linestyle='-', color='blue')
                ax.set_title(f'Route {i+1}')  # Set title for each subplot

            # Leave last subplots empty if needed
            for i in range(num_routes, num_cols * num_rows):
                row = i // num_cols
                col = i % num_cols
                fig.delaxes(axs[row, col])

            plt.tight_layout()
            plt.savefig('railway_network.png')
            plt.close()