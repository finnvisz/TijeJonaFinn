# External imports
import numpy as np

# Local imports
from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.station_class import Station
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.score import Score
from parent.code.algorithms.random_v2 import Randomv2

class Experiment:
    def __init__(self, algorithm_class: "Algorithm", map: str = "Holland") -> None:
        """
        Initialize experiment object with given algorithm and map.
        
        - algorithm_class: name of algorithm class to run the experiment on.
        - map: name of the map to run the algorithm on 
        (default: "Holland" or "Nationaal" for full map).
        - **algorithm_kwargs: keyword arguments to pass to the algorithm's run method.
        """
        self.algorithm_class: "Algorithm" = algorithm_class
        self.map: str = map

        # Get the total stations and connections and create an index mapping
        total_connections = list(RailNL(self.map).get_total_connections())
        self.connection_indices = {tuple(sorted((conn[0].name, conn[1].name))): idx for idx, conn in enumerate(total_connections)}
        self.count_connections_used = np.zeros(len(total_connections))
        self.connection_labels = [f"{conn[0].name} - {conn[1].name}" for conn in total_connections]

        self.total_stations = list(RailNL(self.map).stations_dict().keys())
        self.station_indices = {station: idx for idx, station in enumerate(self.total_stations)}
        self.count_stations_used = np.zeros(len(self.total_stations))
        

        # Set default export directory (for export of results to CSV etc.)
        self.export_directory: str = "parent/code/experiments/results"


    def run_experiment(self, iterations: int = 100, **algorithm_kwargs) -> float:
        """
        Runs algorithm N times (default 100), and returns the scores in a numpy array.
        
        - Pre: Experiment instance has been initialized with existing algorithm and map.
        Necessary keyword arguments for the algorithm's run method have been provided
        to this method (if any).
        - Post: returns a numpy array with N scores.
        """
        # Scores are saved in numpy array, way faster than list!
        # Space in memory is reserved and filled with zeros
        self.scores: "nparray[float]" = np.full(iterations, np.nan)
        
        for i in range(iterations):
            # Ensure each run starts with a fresh state.
            data_instance = RailNL(self.map)
            # Initialize algorithm
            algorithm_instance = self.algorithm_class(data_instance)
            # Run and calculate score
            score = Score(algorithm_instance, **algorithm_kwargs).calculate()
            # Add score to array at correct positions
            self.scores[i] = score

<<<<<<< HEAD
            # Count each connection used
            used_connections = algorithm_instance.get_total_connections_used()
            for connection in used_connections:
                # Normalize the connection tuple to match the total connections format
                normalized_connection = tuple(sorted(connection[:2]))
                if normalized_connection in self.connection_indices:
                    self.count_connections_used[self.connection_indices[normalized_connection]] += 1
                else:
                    print(f"Warning: Connection {normalized_connection} not found in connection_indices.")

            # Count each station used
            used_stations = algorithm_instance.get_stations_used()
            
            if used_stations is not None:
                for station in used_stations:
                    if station.name in self.station_indices:
                        self.count_stations_used[self.station_indices[station.name]] += 1
                    else:
                        print(f"Warning: Station {station.name} not found in station_indices.")
            else:
                print("Warning: get_stations_used() returned None.")

        assert np.count_nonzero(self.scores) == iterations, "Not all scores have been filled in, bug in run_experiment."
=======
        assert any(np.isnan(self.scores)), "Not all scores have been filled in, bug in run_experiment."
>>>>>>> db92ca17aa064f6bca0c3924910cd452a81b2ceb
        return self.scores
    
    def average_score(self) -> float:
        return np.mean(self.scores)
    
    def write_scores_to_csv(self, filename: str) -> None:
        """
        Write scores to a CSV file. 

        - Pre: scores have been calculated (i.e. run_experiment has been called).
        `filename` is a string without extension.
        - Post: scores are written to `filename`.csv in the results subdirectory.
        """
        np.savetxt(f"{self.export_directory}/{filename}.csv", self.scores, delimiter = ",")
        

# Example usage
if __name__ == "__main__":
    random_experiment = Experiment(algorithm_class = Randomv2)
    results = random_experiment.run_experiment(iterations = 10, starting_stations="prefer_unused")
    # print(results)
    print(f"Random Algorithm Average Score: {np.mean(results)}")
    random_experiment.write_scores_to_csv("randomv2_scores")

    # finn_experiment = Experiment(Finn, map, iterations=100)
    # print(f"Finn Average Score: {finn_experiment.average_score()}")  # should be 8919
    # print(finn_experiment.scores)