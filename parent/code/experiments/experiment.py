from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.finnsroutes import Finn
from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.score import Score
from parent.code.algorithms.random_v2 import Randomv2

class Experiment:
    def __init__(self, algorithm_class: "Algorithm", data_params: str = "Holland", iterations: int = 100, **algorithm_kwargs) -> None:
        """
        - **algorithm_kwargs: keyword arguments to pass to the algorithm's run method.
        """
        self.algorithm_class = algorithm_class
        self.data_params = data_params
        self.iterations = iterations
        self.scores: list[float] = []
        
        self.average_score(**algorithm_kwargs)


    def average_score(self, **algorithm_kwargs) -> float:
        # runt N times, calculates score, and average score over N times
        times = 0
        total_score = 0
        while times < self.iterations:
            # Ensure each run starts with a fresh state.
            data_instance = RailNL(self.data_params)
            algorithm_instance = self.algorithm_class(data_instance)
            score = Score(algorithm_instance, **algorithm_kwargs).calculate()
            self.scores.append(score)
            total_score += score
            times += 1

        average_score = total_score / self.iterations
        return average_score
    

    def get_scores(self) -> list:
        return self.scores

# Example usage
data_params = "Holland"
random_experiment = Experiment(Randomv2, data_params, iterations=100, starting_stations="prefer_unused")
print(f"Random Algorithm Average Score: {random_experiment.average_score()}")
print(random_experiment.scores)

# finn_experiment = Experiment(Finn, data_params, iterations=100)
# print(f"Finn Average Score: {finn_experiment.average_score()}")  # should be 8919
# print(finn_experiment.scores)