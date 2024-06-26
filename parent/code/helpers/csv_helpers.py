# External imports
import numpy as np
import pandas as pd
import numpy as np
import csv
from datetime import datetime
import os

# Internal imports
from parent.code.classes.route import Route
from parent.code.classes.railnl import RailNL
from parent.code.helpers.score import calculate_score

# Default directory for all functions in this file, can be changed if needed
# Don't delete! Used by all functions in this file.
experiments_root_dir = "parent/code/experiments"
code_root_dir = "parent/code"

def write_scores_to_csv(scores: "np.ndarray", 
                        filename: str, 
                        custom_file_path: bool = False) -> None:
        """
        Write single numpy array of scores to a CSV file. Default export
        directory is `parent/code/experiments/results`.

        - Pre: `scores` contains numpy array of scores,
        argument 2 `filename` is a string (extension is allowed but
        optional).
        
        - Post: scores are written to `filename`.csv in the results
          subdirectory. Each score is written in a new row.

        Args:
        
        - scores: numpy array of scores.
        
        - filename: name of the file to write to, extension is
          optional.
        
        - custom_file_path: if True, override default directory so 
        `filename` becomes a path from root directory of this project.
        """

        # If custom file path is True, override default directory so 
        # user can specify path from parent directory
        if custom_file_path:
            csv_results_dir = ""
        else:
            csv_results_dir = f"{experiments_root_dir}/results/"
        
        # Add .csv extension if not present
        if not filename.endswith(".csv"):
            filename += ".csv"

        np.savetxt(f"{csv_results_dir}{filename}", 
                   scores, delimiter = ",")

def read_scores_from_csv(filename: str,
                         custom_file_path: bool = False
                         ) -> "np.ndarray[float]":
    """
    Read scores from a CSV file with single column and return them as a
    single numpy array.

    - Pre: CSV file with scores exists in the `experiments/results/`
      directory and has a single column without header.
    
    - Post: returns a numpy array with scores.

    Args: 
    
    - filename: name of the file to read from, extension is optional.
    
    - custom_file_path: if True, override default directory so
    `filename` becomes a path from root directory of this project.
    """
    
    # If custom file path is True, override default directory so 
    # user can specify path from parent directory
    if custom_file_path:
        csv_results_dir = ""
    else:
        csv_results_dir = f"{experiments_root_dir}/results/"
    
    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Read scores from CSV file
    scores = np.loadtxt(f"{csv_results_dir}{filename}", delimiter=",")
    return scores

def append_scores_to_csv(scores: "np.ndarray", 
                         filename: str,
                         custom_file_path: bool = False) -> None:
    """
    Append a numpy array of scores to an existing CSV file as a new
    column. If `filename.csv` does not yet exist, a new file will be
    created. Default directory is `parent/code/experiments/results`.

    - Pre: `scores` contains numpy array of scores,
    `filename.csv` exists (extension is allowed but optional).
    
    - Post: a new column with scores is appended to `filename.csv`
    in the results subdirectory.

    Args: 
    
    - scores: numpy array of scores.
    
    - filename: name of the file to append to, extension is optional.
    
    - custom_file_path: if True, override default directory so
    `filename` becomes a path from root directory of this project.
    """
    
    # If custom file path is True, override default directory so 
    # user can specify path from parent directory
    if custom_file_path:
        csv_results_dir = ""
    else:
        csv_results_dir = f"{experiments_root_dir}/results/"

    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"


    # Try to open existing CSV file, if not found run write_scores_to_csv
    try:
        # Read the existing CSV file into a DataFrame 
        df_original = pd.read_csv(f"{csv_results_dir}{filename}", 
                         header=None) 
    
    except FileNotFoundError:
        # If file not found, run write_scores_to_csv
        write_scores_to_csv(scores, 
                            filename, 
                            custom_file_path = custom_file_path)
        return


    # Create dataframe for the new scores
    df_additional = pd.DataFrame({"new_column": scores})
    
    # Combine old df and new df
    df_concatenated = pd.concat([df_original, df_additional], axis=1)
        

    # Write the updated DataFrame back to the CSV file 
    df_concatenated.to_csv(f"{csv_results_dir}{filename}",
                            index=False, header=False)
        
def append_single_score_to_csv(score: float,
                               filename: str,
                               custom_file_path: bool = False) -> None:
    """
    Append a single score to an existing CSV file as a new row.
    If `filename.csv` does not yet exist, a new file will be created.
    Default directory is `parent/code/experiments/results`.

    - Pre: `score` is a single float score.
    
    - Post: a new row with `score` is appended to `filename.csv`, or
    a new file is created with `score` as the only row.
    
    Args:
    
    - score: single float score to append.
    
    - filename: name of the file to append to, extension is optional.
    
    - custom_file_path: if True, override default directory so
    `filename` becomes a path from root directory of this project.
    """
    
    # If custom file path is True, override default directory so 
    # user can specify path from parent directory
    if custom_file_path:
        csv_results_dir = ""
    else:
        csv_results_dir = f"{experiments_root_dir}/results/"

    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Try to open existing CSV file, if not found run write_scores_to_csv
    try:
        # Read the existing CSV file into a DataFrame 
        df_original = pd.read_csv(f"{csv_results_dir}{filename}", 
                         header=None) 
    
    # But if file not found or empty, run write_scores_to_csv
    except:
        
        write_scores_to_csv(np.array([score]), 
                            filename, 
                            custom_file_path = custom_file_path)
        return
    

    # Turn column 1 of df into numpy array
    scores_array = df_original.iloc[:,0].to_numpy()
    
    # Append the new score to the numpy array
    scores_array = np.append(scores_array, score)

    # Write the updated numpy array back to the CSV file
    np.savetxt(f"{csv_results_dir}{filename}",
                scores_array, delimiter = ",")

def write_solution_to_csv(routes: list[Route], 
                          filename: str, 
                          map="Holland", 
                          custom_file_path: bool = False):
    """
    Export algorithm output (list consisting of multiple Route objects)
    to required .csv file.
    
    - Pre: `routes` is a list of route objects, `filename` contains 
    filename to write to in `experiments/route_csv` (unless
    `custom_file_path`; extension is optional).
    
    - Post: csv-file of given format is located in `route_csv` folder
      (unless `custom_file_path`).

    Args:
    
    - routes: list of Route objects, output of algorithm.
    
    - filename: name of the file to write to, extension is optional.
    
    - map: name of the map used in the algorithm. Default is "Holland".
    
    - custom_file_path: if True, override default directory so
    `filename` becomes a path from root directory of this project.
    """
    # If custom file path is True, override default directory so 
    # user can specify path from parent directory
    if custom_file_path:
        csv_solution_dir = ""
    else:
        csv_solution_dir = f"{experiments_root_dir}/route_csv/"
    
    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Check whether file already exists
    # If so, add timestamp to filename to avoid overwriting
    if os.path.exists(f"{csv_solution_dir}{filename}"):
        # get current time
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        
        filename = filename.split(".csv")[0]
        filename += f"_{current_time}.csv"

    
    with open(f"{csv_solution_dir}{filename}", 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["train", "stations"])

        for i in range(len(routes)):
            writer.writerow([f"train_{i+1}", routes[i].get_stations_as_string()])

        score = calculate_score(routes, map)
        writer.writerow(["score", f"{score}"])

def read_solution_from_csv(filename: str, 
                           map="Holland", 
                           file_path = "default") -> list[Route]:
    """
    Read a solution for the RailNL problem from a CSV file.

    - Pre: CSV file `filename` with solution created by 
    `write_solution_to_csv()` exists in the directory chosen by
    `file_path` argument.
    
    - Post: return a list of Route objects

    Args:
    
    - filename: name of the file to read from, extension is optional.
    
    - map: name of the map used in the algorithm 
    (Holland or Nationaal; default is Holland).
    
    - file_path: choose between "default", "for_manim" or 
    "custom_file_path":
    
        - default: read from `experiments/route_csv/`
    
        - for_manim: read from `experiments/route_csv/` with relative
          path from manim script
        
        - custom_file_path: read from root of git repository, so user can
          specify path manually
    """
    
    # Set directory for reading the CSV file:
    
    # Default directory is experiments/route_csv/
    if file_path == "default":
        global experiments_root_dir
        csv_results_dir = f"{experiments_root_dir}/route_csv/"

    # Manim needs relative path from it's script to the default directory
    elif file_path == "for_manim":
        csv_results_dir = "../"

    # If custom file path, override default directory so user can specify
    # path from parent directory
    elif file_path == "custom_file_path":
        csv_results_dir = ""
    
    # Else raise error
    else:
        raise ValueError("Invalid file_path argument, choose 'default',"
                         " 'for_manim' or 'custom_file_path'")

    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Initialize the RailNL object once
    rail_network = RailNL(map)

    # Read the solution from the CSV file
    solution = []
    with open(f"{csv_results_dir}{filename}", 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] != "score":
                route = Route()
                station_names = row[1].strip("[]").split(", ")
                stations = []
                for station_name in station_names:
                    stations.append(rail_network.stations_dict()[station_name])
                for i in range(len(stations)-1):
                    connection_duration = stations[i].connections[stations[i + 1]]
                    route.add_connection(stations[i], 
                                         stations[i+1], 
                                         connection_duration)
                solution.append(route)
    
    return solution