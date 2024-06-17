# External imports
import numpy as np

# Local imports
from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.finnsroutes import Finn
from parent.code.algorithms.algorithm import Algorithm
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
        
        # Set default export directory (for export of results to CSV etc.)
        self.export_directory: str = "parent/code/experiments/results"


    def run_experiment(self, iterations: int = 100, **algorithm_kwargs) -> float:
        """
        Runs algorithm N times (default 100), and returns the scores in a numpy array.

        Post: returns a numpy array with N scores.
        """
        # Scores are saved in numpy array, way faster than list!
        # Space in memory is reserved and filled with zeros
        self.scores: "nparray[float]" = np.zeros(iterations)
        
        
        for i in range(iterations):
            # Ensure each run starts with a fresh state.
            data_instance = RailNL(self.map)
            # Initialize algorithm
            algorithm_instance = self.algorithm_class(data_instance)
            # Run and calculate score
            score = Score(algorithm_instance, **algorithm_kwargs).calculate()
            # Add score to array at correct positions
            self.scores[i] = score

        assert np.count_nonzero(self.scores) == iterations, "Not all scores have been filled in."
        return self.scores
    

        

# Example usage
if __name__ == "__main__":
    random_experiment = Experiment(algorithm_class = Randomv2)
    results = random_experiment.run_experiment(iterations = 10, starting_stations="prefer_unused")
    # print(results)
    print(f"Random Algorithm Average Score: {np.mean(results)}")
    np.savetxt(f"{random_experiment.export_directory}/randomv2_scores.csv", results, delimiter = ",")

    # finn_experiment = Experiment(Finn, map, iterations=100)
    # print(f"Finn Average Score: {finn_experiment.average_score()}")  # should be 8919
    # print(finn_experiment.scores)