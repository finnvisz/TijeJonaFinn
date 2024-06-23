# Function to put the Hillclimber algorithm to work
# Let's leave it for a few hours and see what we can gather

import os
import numpy as np

from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.experiments.statistics import write_solution_to_csv, write_scores_to_csv, append_single_score_to_csv
from parent.code.algorithms.score import routes_score


def autorun_hillclimber(n_runs: int, 
                        session_name: str,
                        maprange: str = "Holland", 
                        allow_overwrite: bool = False
                        ):
    """
    Run the Hillclimber algorithm for a specified number of runs.

    Args:
        n_runs (int): The number of runs to perform.
        session_name (str): The name of the session or project.
        maprange (str, optional): The map range to use. Defaults to "Holland".
        allow_overwrite (bool, optional): Whether to allow overwriting an existing project directory. Defaults to False.


    """

    # Input checks
    assert maprange in ["Holland", "Nationaal"], "Maprange should be either 'Holland' or 'Nationaal'."




    # Set root directory (where all project directories will be created)
    root_dir = "parent/code/algorithms/autorun_hillclimber/"
    
    # Project dir is subdirectory of root dir
    project_dir = f"{root_dir}{session_name}"
    
    # Create project directory
    # If directory already exists, print error message and return
    try:
        os.mkdir(project_dir)

        # Create subdirectory to store solution of each run
        os.mkdir(f"{project_dir}/solutions")
    
    # But if project was already created (project is re-run)
    except FileExistsError:
        if not allow_overwrite:
            print(f"Error: Directory {session_name} already exists. If appending to existing project is deliberate, set 'allow_overwrite' to True.")
            return

        print(f"Warning: Directory {session_name} already exists. Appending to that project.")
        

    


    # For the specified number of runs, run the Hillclimber algorithm
    for _ in range(n_runs):
        try:
            # Set a start state based on our found heuristics
            start_state = Random_Greedy(maprange).run(
                            starting_stations="original_stations_only_hard",
                            final_number_of_routes = 4,
                            route_time_limit = 100)

            # Run the Hillclimber algorithm and save solutions
            hillclimber_alg = Hillclimber(start_state, maprange)
            solution = hillclimber_alg.run(iterations = 350000,
                                        log_csv=f"{project_dir}/log.csv",
                                        simulated_annealing=True,
                                        cap = 10000)
            


            # After a run, write the solution to a csv file in auto_run folder
            score = routes_score(solution, maprange)
            solution_filename = f"{maprange}_{round(score)}_HC.csv"

            write_solution_to_csv(solution, 
                                f"{project_dir}/solutions/{solution_filename}", 
                                custom_file_path=True)
            
            # Append the end score of this run to the end_scores csv file
            append_single_score_to_csv(score, 
                                    f"{project_dir}/end_scores.csv", 
                                    custom_file_path=True)
        


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
            
            # Als de overflow error zich voordoet, door naar de volgende run
        except:
            continue




if __name__ == "__main__":
    autorun_hillclimber(100000, "4_routes_zondag", maprange="Holland", allow_overwrite=True)

