from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.finnsroutes import Finn
from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.score import Score

class Experiment:
    def __init__(self, algorithm_class: "Algorithm", data_params: str, iterations: int = 100) -> None:
        self.algorithm_class = algorithm_class
        self.data_params = data_params
        self.iterations = iterations

    def average_score(self) -> float:
        # runt N times, calculates score, and average score over N times
        times = 0
        total_score = 0
        while times < self.iterations:
            # Ensure each run starts with a fresh state.
            data_instance = RailNL(self.data_params)
            algorithm_instance = self.algorithm_class(data_instance)
            score = Score(algorithm_instance).calculate()
            total_score += score
            times += 1

        average_score = total_score / self.iterations
        return average_score

# Example usage
data_params = "Holland"
random_experiment = Experiment(RandomAlgorithm, data_params, iterations=100)
print(f"Random Algorithm Average Score: {random_experiment.average_score()}")

finn_experiment = Experiment(Finn, data_params, iterations=100)
print(f"Finn Average Score: {finn_experiment.average_score()}")  # should be 8919