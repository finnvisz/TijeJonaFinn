from parent.code.algorithms.autorun_hillclimber import autorun_hillclimber
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.experiments.experiment import Experiment
from parent.code.experiments.statistics import plot_autorun_hillclimber, plot_endscores_autorun_hillclimber, plot_scores_fancy

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
plot_scores_fancy(random_algorithm_results, 
                  greedy_algorithm_results,
                  random_algorithm_with_heuristic,
                  
                  title="Heuristics matter: Random vs Greedy algorithm", 
                  legend_title= "Algorithm",
                  legend_labels=("Random", "Greedy", "Random + heuristic"),
                  save_to_pdf = True)

# There are way more conditions to experiment with! 
# Check out the Random_Greedy algorithm's docs by hovering over "run"
Random_Greedy().run(1)


"""
### 2. AUTORUN HILLCLIMBER ###

# This one takes a bit longer, but it's worth it!

# Choose a name for your new Autorun Hillclimber project (I bet you can do better than "my_first_project"!):
project_name = "my_first_project"

# Run the autorun_hillclimber program with the chosen project name
# Let's start with 10 runs and the smaller map: "Holland"
# This way you can see the results (relatively) quickly and get a feel for the program
autorun_hillclimber(n_runs = 10, 
                    session_name = project_name, 
                    maprange = "Holland", 
                    allow_overwrite = False
                    )

# Now that you have an autorun hillclimber project, you can get a
# summary of your logfile using a plot:
plot_autorun_hillclimber(project_name = project_name, 
                         title = "Logplot: my first Autorun Hillclimber project", 
                         use_aggregated = False
                         )

# You can also plot the endscores your hillclimber achieved:
plot_endscores_autorun_hillclimber(project_name = project_name)

# Both functions will save the plots in your project directory.

# If you go to your project directory, you will find a directory called "solutions".
# This directory contains the solution produced by each run as a csv file.
# Take a look and see what your best solution looks like!
"""


### 3. MANIM VISUALISATION ###

# CSV files can only tell you so much
# Let's visualise the best solution of your autorun hillclimber project!
