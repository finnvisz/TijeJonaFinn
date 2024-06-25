# External imports
import numpy as np

# Local imports
from parent.code.algorithms.algorithm import Algorithm
from parent.code.algorithms.score import routes_score
from parent.code.algorithms.random_greedy import Random_Greedy

class Experiment:

    def __init__(self, maprange: str = "Holland", algorithm_class: "Algorithm" = Random_Greedy) -> None:
        
        """
        Initialize experiment object with given algorithm and maprange.
        
        - maprange: name of the map to run the algorithm on 
        (default: "Holland" or "Nationaal" for full map).
        - algorithm_class: name of algorithm class to run the experiment on.
        """
        self.algorithm_class: "Algorithm" = algorithm_class
        self.maprange: str = maprange

        
    def run_experiment(self, iterations: int = 100, **algorithm_kwargs) -> float:
        """
        Runs algorithm N times (default 100), and returns the scores in a numpy array.
        
        - Pre: Experiment instance has been initialized with existing algorithm and maprange.
        Necessary keyword arguments for the algorithm's run method have been provided
        to this method (if any).
        - Post: returns a numpy array with N scores.
        """
        
        print(f"Running {self.algorithm_class.__name__} algorithm {iterations} times on {self.maprange} map...")

        # Scores are saved in numpy array, way faster than list!
        # Space in memory is reserved and filled with NaNs
        self.scores: "np.ndarray[float]" = np.full(iterations, np.nan)
        
        for i in range(iterations):
            
            # Initialize algorithm
            algorithm_instance = self.algorithm_class(self.maprange)

            # Run and calculate score
            solution = algorithm_instance.run(**algorithm_kwargs)
            score = routes_score(solution, self.maprange)

            # Add score to array at correct positions
            self.scores[i] = score

        # Check that all scores have been filled in
        assert not any(np.isnan(self.scores)), """Not all scores have been filled in, bug in run_experiment."""

        print(f"Experiment finished! Mean score: {np.mean(self.scores)}")

        # And return the scores
        return self.scores

