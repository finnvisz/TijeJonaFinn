import os

from parent.code.classes.route import Route
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.experiments.statistics import write_solution_to_csv, append_single_score_to_csv
from parent.code.algorithms.score import calculate_score


# This function sets parameters for the start state and execution of the
# Hillclimber algorithm. Feel free to adjust these parameters to your
# liking.
def run_hillclimber(maprange: str, project_dir: str) -> list[Route]:
    """
    Set a start state, run the Hillclimber algorithm and return the
    solution.
    """
    
    # Set a start state based on our found heuristics
    start_state = Random_Greedy(maprange).run(
                    starting_stations="original_stations_only_hard",
                    final_number_of_routes = (10, 11, 12),
                    route_time_limit = [180, 140, 160])

    # Run the Hillclimber algorithm and save solution, also log progress
    hillclimber_alg = Hillclimber(start_state, maprange)
    solution = hillclimber_alg.run(iterations = 600000,
                                log_csv=f"{project_dir}/log.csv",
                                simulated_annealing=True,
                                cap = 60000,
                                improve_routes = True,
                                original_connections_only = False)

    return solution


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
        - maprange (str, optional): The map range to use. Defaults to
          "Holland".
        - allow_overwrite (bool, optional): Whether to allow overwriting
          an existing project directory. Defaults to False.
    """

    # Input check
    assert maprange in ["Holland", "Nationaal"], (
        "Maprange should be either 'Holland' or 'Nationaal'.")


    # Set root directory (where all project directories will be created)
    root_dir = "parent/code/algorithms/autorun_hillclimber/"
    # Project dir is subdirectory of root dir
    project_dir = f"{root_dir}{session_name}"


    # Create project directory or append to existing project
    project_created: bool = create_project(session_name, 
                                        project_dir, 
                                        allow_overwrite)
    # If functions returns False: fatal error so return
    if not project_created:
        return


    # Print message that the autorun is starting
    print(f"Starting {n_runs} runs of Hillclimber algorithm on {maprange} map.")
    print("")

    # For the specified number of runs, run the Hillclimber algorithm
    for run_number in range(1, n_runs + 1):
        
        # Try to run the Hillclimber algorithm:
        # Try statement is used to catch very rare overflow error in
        # temperature function of the Hillclimber algorithm
        try:
            
            # Run the Hillclimber algorithm
            solution = run_hillclimber(maprange, project_dir)

            # Write the produced solution to a csv file
            write_run_to_csv(solution, maprange, project_dir)

            # Print succes message seperated by empty lines
            print(
            f"\nRun {run_number} of {n_runs} of project {session_name}", 
            "completed. Proceeding to next run.\n")


        # If an error occurs, log run number and on to the next run
        except Exception as e:
            print(f"\nError occurred in run {run_number}:")    
            print(repr(e))
            print(f"\nProceeding to next run.\n")
            
            # Log the run number to a csv file
            append_single_score_to_csv(run_number, 
                                       f"{project_dir}/runs_with_error.csv", 
                                       custom_file_path=True)

            continue


def create_project(session_name: str, 
                   project_dir: str, 
                   allow_overwrite: bool
                   ) -> bool:
    """
    Tries to create a new project directory. If the directory already
    exists, handles that based on the `allow_overwrite` parameter.

    Returns: True if project was succesfully created or appended, False
    if project already exists and overwriting is not allowed.
    """
    
    
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
        # False to indicate fatal error
        if not allow_overwrite:
            print("")
            print(f"Error: Directory {session_name} already exists.", 
                  "If appending to existing project is deliberate,",
                    "set 'allow_overwrite' to True.")
            return False

        # If overwriting is allowed, print warning message
        print("")
        print(f"Warning: Directory {session_name} already exists.", 
              "Appending to that project.")
        print("")        


    # Return True if project was succesfully created or appended
    return True


def write_run_to_csv(solution: list[Route], 
                     maprange: str, 
                     project_dir: str
                     ) -> None:
    """
    After a run, write the produced solution and endscore to a csv file
    in project directory.
    """
    
    # Calculate score of the solution
    score = calculate_score(solution, maprange)
    
    # Set filename for the solution based on maprange and score
    solution_filename = f"{maprange}_{round(score)}_HC.csv"

    # Write the solution to a csv file in solutions directory
    write_solution_to_csv(solution, 
                        f"{project_dir}/solutions/{solution_filename}", 
                        custom_file_path=True, 
                        map= maprange)
    
    # Append the end score of this run to the end_scores csv file
    append_single_score_to_csv(score, 
                            f"{project_dir}/end_scores.csv", 
                            custom_file_path=True)