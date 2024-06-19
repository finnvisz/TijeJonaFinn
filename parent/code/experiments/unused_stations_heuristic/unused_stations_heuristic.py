# External imports
import numpy as np

# Local imports
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.greedy import Greedy
from parent.code.algorithms.random_v2 import Randomv2
from parent.code.experiments.experiments import Experiment


if __name__ == "__main__":
    # Set number of iterations for the experiment
    iterations = 100000


    ## 1. Greedy with and without original starting stations

    # Initialize experiment
    greedy_experiment = Experiment(Greedy, "Holland")


    # Run algorithm with 2 conditions:
    
    # With original starting stations
    results_greedy_with_original_stations = greedy_experiment.run_experiment(iterations=iterations, original_starting_station = True)
    greedy_experiment.write_scores_to_csv(f"unused_stations_heuristic/results/greedy_with_original_stations_{iterations}")   

    # Without original starting stations
    results_greedy_without_original_stations = greedy_experiment.run_experiment(iterations=iterations, original_starting_station = False)
    greedy_experiment.write_scores_to_csv(f"unused_stations_heuristic/results/greedy_without_original_stations_{iterations}")  


    # Calculate average scores
    print(f"Average score for Greedy with original starting stations ({iterations} iterations): {np.mean(results_greedy_with_original_stations)}")
    print(f"Average score for Greedy without original starting stations ({iterations} iterations): {np.mean(results_greedy_without_original_stations)}")


    ## 2. Randomv2 with and without original starting stations

    # Initialize experiment
    randomv2_experiment = Experiment(Randomv2, "Holland")


    # Run algorithm with 2 conditions:

    # With original starting stations
    results_randomv2_with_original_stations = randomv2_experiment.run_experiment(iterations=iterations, starting_stations = "prefer_unused")
    randomv2_experiment.write_scores_to_csv(f"unused_stations_heuristic/results/randomv2_with_original_stations_{iterations}")

    # Without original starting stations
    results_randomv2_without_original_stations = randomv2_experiment.run_experiment(iterations=iterations, starting_stations = "fully_random")
    randomv2_experiment.write_scores_to_csv(f"unused_stations_heuristic/results/randomv2_without_original_stations_{iterations}")


    # Calculate average scores
    print(f"Average score for Randomv2 with original starting stations ({iterations} iterations): {np.mean(results_randomv2_with_original_stations)}")
    print(f"Average score for Randomv2 without original starting stations ({iterations} iterations): {np.mean(results_randomv2_without_original_stations)}")

