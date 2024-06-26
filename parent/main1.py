from parent.code.experiments.experiment import Experiment
from parent.code.helpers.plots import plot_scores

### 1. EXPERIMENTATION ###
# If you want to get a feel for what the samplespace of this problem looks like,
# you can use our experiment-focused algorithm for that.

# Let's compare a basic random algorithm, a basic greedy algorithm
# and a random algorithm + heuristic to see how much difference a 
# heuristic can make.
print("Running experiment 1: Random algorithm")
random_algorithm_results = Experiment("Holland").run_experiment(1000, 
                                                                next_connection_choice = "random")

print("Running experiment 2: Greedy algorithm")
greedy_algorithm_results = Experiment("Holland").run_experiment(1000, 
                                                                next_connection_choice = "shortest")

print("Running experiment 3: Random algorithm with original starting stations heuristic")
random_algorithm_with_heuristic = Experiment("Holland").run_experiment(1000, 
                                                                       next_connection_choice = "random", 
                                                                       starting_stations = "original_stations_only_hard")

# And plot the results (plot should open in pop-up window,
# but is also saved as pdf to parent/code/experiments/plots)
plot_scores(random_algorithm_results, 
                  greedy_algorithm_results,
                  random_algorithm_with_heuristic,
                  
                  title="Heuristics matter: Random vs Greedy algorithm", 
                  legend_title= "Algorithm",
                  legend_labels=("Random", "Greedy", "Random + heuristic"),
                  save_to_pdf = True)

