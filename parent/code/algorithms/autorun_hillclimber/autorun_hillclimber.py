# Function to put the Hillclimber algorithm to work
# Let's leave it for a few hours and see what we can gather

import os
import numpy as np

from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.experiments.statistics import write_solution_to_csv, append_single_score_to_csv
from parent.code.algorithms.score import routes_score


def autorun_hillclimber(n_runs: int, 
                        session_name: str,
                        maprange: str = "Holland", 
                        allow_overwrite: bool = False
                        ):
    """
    Run the Hillclimber algorithm for a specified number of runs.

    Args:
        - n_runs (int): The number of runs to perform.
        - session_name (str): The name of the session or project.
        - maprange (str, optional): The map range to use. Defaults to "Holland".
        - allow_overwrite (bool, optional): Whether to allow overwriting an existing project directory. Defaults to False.


    """

    # Input checks
    assert maprange in ["Holland", "Nationaal"], "Maprange should be either 'Holland' or 'Nationaal'."




    # Set root directory (where all project directories will be created)
    root_dir = "parent/code/algorithms/autorun_hillclimber/"
    
    # Project dir is subdirectory of root dir
    project_dir = f"{root_dir}{session_name}"
    
    # Create project directory
    # If directory already exists, handle that
    try:
        os.mkdir(project_dir)

        # Create subdirectory to store solution of each run
        os.mkdir(f"{project_dir}/solutions")

        print("")
        print(f"New project {session_name} succesfully created.")
        print("") 
    
    # But if project was already created (project is re-run)
    except FileExistsError:
        # If overwriting is not allowed, print error message and return
        if not allow_overwrite:
            print("")
            print(f"Error: Directory {session_name} already exists. If appending to existing project is deliberate, set 'allow_overwrite' to True.")
            return

        # If overwriting is allowed, print warning message
        print("")
        print(f"Warning: Directory {session_name} already exists. Appending to that project.")
        print("")        

    


    # Print message that the autorun is starting
    print(f"Starting {n_runs} runs of Hillclimber algorithm on {maprange} map.")
    print("")

    # For the specified number of runs, run the Hillclimber algorithm
    for run_number in range(1, n_runs + 1):
        
        try:

            # Set a start state based on our found heuristics
            start_state = Random_Greedy(maprange).run(
                            starting_stations="original_stations_only_hard",
                            final_number_of_routes = 4,
                            route_time_limit = [100, 120, 120, 120])

            # Run the Hillclimber algorithm and save solutions
            hillclimber_alg = Hillclimber(start_state, maprange)
            solution = hillclimber_alg.run(iterations = 450000,
                                        log_csv=f"{project_dir}/log.csv",
                                        simulated_annealing=True,
                                        cap = 30000,
                                        improve_routes = True,
                                        original_connections_only = True)
            



            # After a run, write the solution to a csv file in auto_run folder
            score = routes_score(solution, maprange)
            solution_filename = f"{maprange}_{round(score)}_HC.csv"

            write_solution_to_csv(solution, 
                                f"{project_dir}/solutions/{solution_filename}", 
                                custom_file_path=True, 
                                map= maprange)
            
            # Append the end score of this run to the end_scores csv file
            append_single_score_to_csv(score, 
                                    f"{project_dir}/end_scores.csv", 
                                    custom_file_path=True)
            
            # Print succes message seperated by empty lines
            print("")
            print(f"Run {run_number} of {n_runs} succesfully completed.",
                    "Proceeding to next run.")
            print("")
        



        # If an error occurs, log run number and on to the next run
        except:
            print("")
            print(f"Error occurred in run {run_number}. Proceeding to next run.")
            print("")
            
            append_single_score_to_csv(run_number, 
                                       f"{project_dir}/runs_with_error.csv", 
                                       custom_file_path=True)

            continue




if __name__ == "__main__":
    autorun_hillclimber(1000, "maandag_original_connections_only", maprange="Holland", allow_overwrite=False)

