# External imports
import numpy as np

# Local imports
from parent.code.classes.route import Route
from parent.code.algorithms.algorithm import Algorithm
from parent.code.helpers.score import calculate_score
from parent.code.algorithms.random_greedy import Random_Greedy


class Experiment:

    def __init__(self, maprange: str = "Holland", algorithm_class: "Algorithm" = Random_Greedy) -> None:
        
        """
        Initialize experiment object with given algorithm and maprange.
        
        - maprange: name of the map to run the algorithm on 
        (default: "Holland" or "Nationaal" for full map).
        - algorithm_class: name of algorithm class to run the experiment
        on.
        """
        self.maprange: str = maprange
        self.algorithm_class: "Algorithm" = algorithm_class
        

    def run_experiment(self, iterations: int, **algorithm_kwargs) -> float:
        """
        Runs algorithm N times, and returns the scores in a numpy array.
        
        - Pre: Experiment instance has been initialized with existing 
        algorithm and maprange. Necessary keyword arguments for the 
        algorithm's run method have been provided (if any).
        
        - Post: returns a numpy array with N scores.

        Args:
            - iterations (int): number of times to run the algorithm.
            - **algorithm_kwargs: keyword arguments for the algorithm's 
            run method.
        """
        
        print(f"Running {self.algorithm_class.__name__} algorithm", 
              f"{iterations} times on {self.maprange} map...")

        # Scores are saved in numpy array, way faster than list!
        # Space in memory is reserved and filled with NaNs
        self.scores: "np.ndarray[float]" = np.full(iterations, np.nan)
        
        for i in range(iterations):
            
            # Initialize algorithm
            algorithm_instance = self.algorithm_class(self.maprange)

            # Run and calculate score
            solution: list[Route] = algorithm_instance.run(**algorithm_kwargs)
            score: float = calculate_score(solution, self.maprange)

            # Add score to array at correct positions
            self.scores[i] = score

        # Check that all scores have been filled in
        assert not any(np.isnan(self.scores)), (
        "Not all scores have been filled in, bug in run_experiment.")

        print(f"Experiment finished! Mean score: {np.mean(self.scores)}")

        # And return the scores
        return self.scores