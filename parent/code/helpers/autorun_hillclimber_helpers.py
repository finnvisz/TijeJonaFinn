import numpy as np
import pandas as pd
import os
import shutil

def combine_projects(project_names: tuple[str]):
    """
    Combine multiple projects into one (the first project). Useful when
    you ran the same project multiple times in parallel.

    - Pre: Projects in `project_names` all exist, with solutions, log
      file
    and end_scores file.

    - Post: Projects are combined into a the first project. Log files are
    combined, end_scores files are combined, and solution directories are
    combined. Original files in first project are renamed to indicate
    they were combined.

    Args:

    - project_names: tuple of strings, names of the projects to combine.
    """
    # Set the root directory where the projects are stored
    root_dir = "parent/code/autorun_hillclimber"

    # Check input
    assert len(project_names) > 1, "Need at least two projects to combine."
    # Assert that the project directories exist
    assert all([os.path.exists(f"{root_dir}/{project_name}") for project_name in project_names]), "Not all projects exist."

    # Combine log files
    combine_logfiles(project_names, root_dir)

    # Combine end_scores files
    combine_endscores(project_names, root_dir)

    # Combine solution directories
    combine_solution_directories(project_names, root_dir)

    print(f"\nCombining projects complete.\n")

def combine_logfiles(project_names: tuple[str], 
                     root_dir: str = "parent/code/autorun_hillclimber"
                     ) -> None:
    """
    Combine log files from multiple projects into a single file.
    Subfunction of `combine_projects`.
    """

    assert len(project_names) > 1, "Need at least two projects to combine."

    print(f"Combining log files.\n")

    # List to store DataFrames of log files
    list_of_df_logs: list[pd.DataFrame] = []

    # For each project, read the log file and store in list
    for project_name in project_names:
        print(f"Reading log file from '{project_name}'...")
        
        df_log = pd.read_csv(f"{root_dir}/{project_name}/log.csv", 
                            header=None)
        list_of_df_logs.append(df_log)

    # Combine the DataFrames in the list
    df_log_combined = pd.concat(list_of_df_logs, axis=1)

    # Rename old logfile
    os.rename(f"{root_dir}/{project_names[0]}/log.csv",
                f"{root_dir}/{project_names[0]}/log_before_merge.csv")
    
    # If there is an aggregated log file, rename that as well
    if os.path.exists(f"{root_dir}/{project_names[0]}/log_aggregated.csv"):
        os.rename(f"{root_dir}/{project_names[0]}/log_aggregated.csv",
                    f"{root_dir}/{project_names[0]}/log_aggregated_before_merge.csv")

    # Write the combined DataFrame back to CSV, put in first project folder
    print("Writing combined log file...")
    df_log_combined.to_csv(f"{root_dir}/{project_names[0]}/log.csv",
                            index=False, header=False)
    
    # When done, print number of columns for each log file
    print(f"Combining log files complete.\n")
    for i in range(len(project_names)):
        print(f"Log file from '{project_names[i]}' had {list_of_df_logs[i].shape[1]} columns.")

    print(f"Combined log file has {df_log_combined.shape[1]} columns.")

    # Rename the logfiles that were integrated with the first to make
    # room for new data in these duplicate projects
    for project_name in project_names[1:]:
        os.rename(f"{root_dir}/{project_name}/log.csv",
                    f"{root_dir}/{project_name}/log_already_merged.csv")
        if os.path.exists(f"{root_dir}/{project_name}/log_aggregated.csv"):
            os.rename(f"{root_dir}/{project_name}/log_aggregated.csv",
                        f"{root_dir}/{project_name}/log_aggregated_already_merged.csv")

def combine_endscores(project_names: tuple[str], 
                      root_dir: str = "parent/code/autorun_hillclimber"
                      ) -> None:
    """
    Combine end_scores files from multiple projects into a single file.
    Subfunction of `combine_projects`.
    """
    assert len(project_names) > 1, "Need at least two projects to combine."

    print(f"\nCombining end_scores files.\n")

    # List to store DataFrames of end_scores files
    list_of_np_arrays: list[np.ndarray] = []

    # For each project, read the end_scores file and store in list
    for project_name in project_names:
        end_scores: np.ndarray = np.loadtxt(f"{root_dir}/{project_name}/end_scores.csv", delimiter=",")
        list_of_np_arrays.append(end_scores)

    # Combine the numpy arrays in the list
    end_scores_combined = np.concatenate(list_of_np_arrays)

    # Rename old end_scores file
    os.rename(f"{root_dir}/{project_names[0]}/end_scores.csv",
                f"{root_dir}/{project_names[0]}/end_scores_before_merge.csv")

    # Write the combined DataFrame back to CSV, put in first project folder
    np.savetxt(f"{root_dir}/{project_names[0]}/end_scores.csv", 
                   end_scores_combined, delimiter = ",")
    
    # When done, print number of rows for each end_scores file
    for i in range(len(project_names)):
        print(f"End scores file from '{project_names[i]}' had {list_of_np_arrays[i].size} rows.")

    print(f"Combined end_scores file has {end_scores_combined.size} rows.")

    # Rename the end_scores files that were integrated with the first to make
    # room for new data in these duplicate projects
    for project_name in project_names[1:]:
        os.rename(f"{root_dir}/{project_name}/end_scores.csv",
                    f"{root_dir}/{project_name}/end_scores_already_merged.csv")

def combine_solution_directories(project_names: tuple[str], 
                                 root_dir: str = "parent/code/autorun_hillclimber"
                                 ) -> None:
    """
    Combine solution directories from multiple projects into a single
    directory. Subfunction of `combine_projects`.
    """
    assert len(project_names) > 1, "Need at least two projects to combine."

    # Assert that the project directories exist
    for project_name in project_names:
        assert os.path.exists(f"{root_dir}/{project_name}")

    print(f"\nCombining solution directories.\n")

    # Make backup of the first project's solutions directory
    shutil.copytree(f"{root_dir}/{project_names[0]}/solutions",
                    f"{root_dir}/{project_names[0]}/solutions_before_merge")


    # For each project except the first, copy the solutions to the
    # solutions directory of the first project
    first_project_solutions_dir = f"{root_dir}/{project_names[0]}/solutions"
    
    for project_name in project_names[1:]:
        this_project_solutions_dir = f"{root_dir}/{project_name}/solutions"
        
        # For all files in the solutions directory of the project
        for filename in os.listdir(this_project_solutions_dir):
            
            # print(filename)
            # Destination filename is the same as the source filename
            dest_filename = filename

            # Unless name conflict occurs, then add _ii suffix to
            # destination filename to avoid overwriting
            if os.path.exists(f"{first_project_solutions_dir}/{dest_filename}"):
                ii = 1
                while True:
                    print(f"Name conflict for '{dest_filename}'")
                    
                    # Remove the .csv extension
                    dest_filename = dest_filename.split(".csv")[0]
                    # If the filename already has a _ii suffix, remove it
                    if ii > 1:
                        # print(f"Removing _{ii-1} suffix.")
                        dest_filename = dest_filename.split(f"_{ii-1}")[0]
                    # Try again with a new _ii suffix
                    dest_filename += f"_{ii}.csv"

                    # If new filename does not exist, break the loop
                    if not os.path.exists(f"{first_project_solutions_dir}/{dest_filename}"):
                        print(f"New filename: '{dest_filename}'\n")
                        break
                    
                    # Otherwise, try again with a higher _ii suffix
                    ii += 1

            # Copy the file to the solutions directory of the first project
            shutil.copy2(f"{this_project_solutions_dir}/{filename}", 
                            f"{first_project_solutions_dir}/{dest_filename}")
        
            # print(dest_filename)

    # When done, print summary
    print(f"Combining solution directories complete.")
    
    n_solutions = len(os.listdir(f"{root_dir}/{project_names[0]}/solutions_before_merge"))
    print(f"Project '{project_names[0]}' had {n_solutions} solutions.")
    
    for project_name in project_names[1:]:
        n_solutions = len(os.listdir(f"{root_dir}/{project_name}/solutions"))
        print(f"Project '{project_name}' had {n_solutions} solutions.")

    n_solutions_combined = len(os.listdir(f"{root_dir}/{project_names[0]}/solutions"))
    print(f"Combined solution directory has {n_solutions_combined} solutions.")

    # Rename the solutions directories that were integrated with the first to make
    # room for new data in these duplicate projects
    for project_name in project_names[1:]:
        os.rename(f"{root_dir}/{project_name}/solutions",
                    f"{root_dir}/{project_name}/solutions_already_merged")
        
        os.mkdir(f"{root_dir}/{project_name}/solutions")