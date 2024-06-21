# External imports
import numpy as np
import scipy.stats as stats
import plotnine as p9
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime

# Internal imports
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.algorithms.finnsroutes import Finn
from parent.code.experiments.experiments import Experiment
from parent.code.classes.route import Route
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.score import routes_score
from parent.code.algorithms.random_greedy import Random_Greedy

# Default directory for all functions in this file, can be changed if needed
# Don't delete! Used by all functions in this file.
experiments_root_dir = "parent/code/experiments"


def write_scores_to_csv(scores: "np.ndarray", filename: str) -> None:
        """
        Write single numpy array of scores to a CSV file. 
        Default export directory is `parent/code/experiments/results`.

        - Pre: `scores` contains numpy array of scores,
        argument 2 `filename` is a string (extension is allowed but optional).
        - Post: scores are written to `filename`.csv in the results subdirectory.
        Each score is written in a new row.
        """
        # Add .csv extension if not present
        if not filename.endswith(".csv"):
            filename += ".csv"

        np.savetxt(f"{experiments_root_dir}/results/{filename}", 
                   scores, delimiter = ",")


def read_scores_from_csv(filename: str) -> "np.ndarray[float]":
    """
    Read scores from a CSV file with single column
    and return them as a single numpy array.

    - Pre: CSV file with scores exists in the `experiments/results/` directory
      and has a single column without header.
    - Post: returns a numpy array with scores.
    """
    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Read scores from CSV file
    scores = np.loadtxt(f"{experiments_root_dir}/results/{filename}", delimiter=",")
    return scores


def append_scores_to_csv(scores: "np.ndarray", filename: str) -> None:
    """
    Append a numpy array of scores to an existing CSV file. If 
    `filename.csv` does not yet exist, a new file will be created.
    Default directory is `parent/code/experiments/results`.

    - Pre: `scores` contains numpy array of scores,
    `filename.csv` exists (extension is allowed but optional).
    - Post: a new column with scores is appended to `filename.csv`
    in the results subdirectory.
    """
    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Try to open existing CSV file, if not found run write_scores_to_csv
    try:
        # Read the existing CSV file into a DataFrame 
        df = pd.read_csv(f"{experiments_root_dir}/results/{filename}", 
                         header=None) 
    except FileNotFoundError:
        # If file not found, run write_scores_to_csv
        write_scores_to_csv(scores, filename)
        return

    # Add the new column 
    df['new_column'] = scores

    # Write the updated DataFrame back to the CSV file 
    df.to_csv(f"{experiments_root_dir}/results/{filename}",
               index=False, header=False) 


def write_solution_to_csv(routes: list[Route], filename: str, map: str):
    """
    Translate algorithm output (solution consisting of multiple Route objects) 
    to required .csv file.
    
    - Pre: `routes` is a list of route objects, `filename` contains 
    filename to write to in `experiments/route_csv` 
    (extension is allowed but optional).
    - Post: csv-file of given format is located in `route_csv` folder. 
    """
    # Add .csv extension if not present
    if not filename.endswith(".csv"):
        filename += ".csv"

    with open(f"{experiments_root_dir}/route_csv/{filename}", 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["train", "stations"])

        for i in range(len(routes)):
            writer.writerow([f"train_{i+1}", routes[i].stations_list()])

        score = routes_score(routes, map)
        writer.writerow(["score", f"{score}"])


def calculate_p_value(sample1: "np.ndarray[float]", sample2: "np.ndarray[float]"
                      , return_type: str = "p_value_only") -> float:
    """
    Calculates a p-value to infer if the difference between two sets of scores
    is significant. Function uses the Mann-Whitney U rank test to test the null
    hypothesis that the distribution underlying sample 1 is the same as
    the distribution underlying sample 2. Return value under 0.05 is a common
    threshold for significance.

    - Pre: sample1 and sample2 are independent samples, given as numpy arrays
    of floats. The alternative hypothesis is two-sided 
    (no specific directionality).
    - Post: returns the p-value of a Mann-Whitney U rank test.

    options:
    - return_type: "p_value_only" (default), "object" (returns full object with
      test statistic inluded),
    "significant" (returns True if p-value < 0.05)
    """
    result_as_object = stats.mannwhitneyu(sample1, sample2)

    if return_type == "p_value_only":
        return result_as_object.pvalue
    elif return_type == "object":
        return result_as_object
    elif return_type == "significant":
        return result_as_object.pvalue < 0.05
    else:
        raise ValueError("Invalid return_type argument, choose 'p_value_only', 'object' or 'significant'.")


def plot_scores_fancy(sample1: "np.ndarray[float]", 
                      sample2: "np.ndarray[float]" = None, 
                      sample3: "np.ndarray[float]" = None, 
                      sample4: "np.ndarray[float]" = None, 
                      
                      # save settings
                      save_to_pdf: bool = False, preview: bool = True, 
                      filename: str | None = None,
                      
                      # plot settings
                      title: str | None = None, 
                      legend_title: str = "Groep",
                      legend_labels: tuple[str] | None = None,
                      binwidth: int = 400, 
                      alpha: float | None = None) -> None:
    """
    Plot the scores of 1 to 4 samples in a histogram.

    - Pre: Each sample is given as a numpy arrays of floats.
    - Post: histogram is plotted (default: only preview, save to pdf also possible).

    Example usage:
    `plot_scores_fancy(sample1, sample2,
    title = "Condition 1 vs Condition 2", 
    legend_labels = ("Condition 1", "Condition 2"))`

    args:

    Save settings:
    - `save_to_pdf`: save plot to pdf file in directory `plot_dir` 
    (which is defined right after the imports of this script).
    - `preview`: show preview of plot.
    - `filename`: (optional) custom filename for the plot. When not 
    provided, user-provided `title` is used or else a default name with 
    timestamp.
    
    Plot settings:
    - `title`: title of the plot, also used as filename if saved to pdf.
    When not provided, a default name with timestamp is used.
    - `legend_title`: title of the legend in the plot. Default is "Groep".
    - `legend_labels`: custom labels for the legend. Should be a tuple
    of strings with the same length as the number of samples.
    
    - `binwidth`: width of the bins in the histogram (default is 400, 
    seems a sweet spot).
    - `alpha`: (optional) set custom transparency of the bars in the 
    histogram. Value between 0 and 1. Default is 0.85 for single sample 
    and 0.7 for multiple samples.
    """

    # Settings for plot
    color_palette = ("lightblue", "lightgrey", "lightsalmon", "lightgreen")
    p9.options.figure_size = (9, 5) # overwritten for single sample

    
    # Complex decision tree to determine filename and title
    # See docs for more info
    if filename is not None:
        if title is None:
            # get current time
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            # Set title
            title = f"Histogram: fancy_plot_{current_time}"
    
    else:
        if title is not None:
            filename = title
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            filename = f"fancy_plot_{current_time}"
            title = f"Histogram: {filename}"

    # Add .pdf extension if not present
    if not filename.endswith(".pdf"):
        filename += ".pdf"
    

    # Ensure correct legend labels
    # If provided, check for correct amount of labels
    if legend_labels is not None:
        assert len(legend_labels) == sum([sample1 is not None,
                                            sample2 is not None, 
                                            sample3 is not None, 
                                            sample4 is not None]), """
        Number of legend labels should match number of samples."""
    
    # If not provided, use default labels
    else:
        legend_label_options = ("Sample 1", "Sample 2", "Sample 3", "Sample 4")
        legend_labels = legend_label_options[:sum([sample1 is not None,
                                                    sample2 is not None, 
                                                    sample3 is not None, 
                                                    sample4 is not None])]

        

    # If sample2 is not provided, create plot for single sample
    if sample2 is None:
        
        # Smaller width for single sample (because no legend)
        p9.options.figure_size = (8, 5)

        # Create dataframe with scores
        df = pd.DataFrame({
            "Score": sample1,
        })

        # Default alpha value
        if alpha is None:
            alpha = 0.85

        # Histogram for single sample
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", fill = color_palette[0], 
                              color = "darkgrey")
        )
    
    # Else create plot for 2 samples
    elif sample3 is None:
        
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2
        })

        df = df.melt(value_vars=['Sample 1','Sample 2'], var_name='Groep', value_name='Score')

        # Default alpha value
        if alpha is None:
            alpha = 0.7

        # Histogram for 2 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Groep", colour = "Groep") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", color = "darkgrey")
        )

    # Else create plot for 3 samples
    elif sample4 is None:
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2,
            "Sample 3": sample3
        })

        df = df.melt(value_vars=['Sample 1','Sample 2', 'Sample 3'], var_name='Groep', value_name='Score')

        # Default alpha value
        if alpha is None:
            alpha = 0.7

        # Histogram for 3 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Groep", colour = "Groep") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", color = "darkgrey")
        )

    # Else create plot for 4 samples
    else:
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2,
            "Sample 3": sample3,
            "Sample 4": sample4
        })

        df = df.melt(value_vars=['Sample 1','Sample 2', 'Sample 3', 'Sample 4'], var_name='Groep', value_name='Score')

        # Default alpha value
        if alpha is None:
            alpha = 0.7

        # Histogram for 4 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Groep", colour = "Groep") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", color = "darkgrey")    
        )
    
    
    # Add labels, title, theme and limits
    # The same for all plots
    plot += p9.xlim(0,10000)
    plot += p9.scale_fill_manual(name = legend_title,
                                values = 
                                color_palette[:sum([sample1 is not None,
                                                    sample2 is not None, 
                                                    sample3 is not None, 
                                                    sample4 is not None])],
                                labels = legend_labels)
    plot += p9.theme_minimal() 
    plot += p9.labs(title = title, 
                    subtitle= f"Iteraties = {len(sample1)}", 
                    y = "Aantal waarnemingen")



    # Save to pdf if specified
    if save_to_pdf:
        plot.save(filename = filename, path=f"{experiments_root_dir}/plots")
    
    # Show preview of plot if specified
    if preview:
        # Show the plot
        plot.show()


def plot_scores(filename: str, scores: list[float]):
    # Plotting the frequency distribution of scores
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=50, edgecolor='black', alpha=0.7)
    plt.title(f"{filename}")
    plt.xlabel('Score')
    plt.xlim(0, 10000)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(f"{experiments_root_dir}/plots/{filename}.png")





#example/test usage
if __name__ == "__main__":
    map = "Nationaal"
    data = RailNL(map)
    scores2 = []
    for i in range(100):
        print(f"{i+1}-de run")
        algorithm = Random_Greedy(data)
        algorithm.run(final_number_of_routes=20, starting_stations="original_stations_only_hard")
        hillclimber_alg = Hillclimber(data, algorithm, map)
        hillclimber_alg.run(10000)
        routes = hillclimber_alg.output()
        write_solution_to_csv(routes, "output", map)
        scores2.append(routes_score(routes, map))
    scores1 = []
    for i in range(100):
        print(f"{i+1}-de run")
        algorithm = Random_Greedy(data)
        algorithm.run(final_number_of_routes=20)
        hillclimber_alg = Hillclimber(data, algorithm, map)
        hillclimber_alg.run(10000)
        routes = hillclimber_alg.output()
        write_solution_to_csv(routes, "output", map)
        scores1.append(routes_score(routes, map))

    plot_scores_fancy(scores1, scores2, title="Nationaal 10000 iteraties 100 keer", save_to_pdf=True, preview=True, binwidth=50)


# if __name__ == "__main__":
#     map = "Holland"
#     data = RailNL(map)
#     scores = []
#     for _ in range(100):
#         algorithm = Random_Greedy(data)
#         algorithm.run()
#         hillclimber_alg = Hillclimber(data, algorithm, map)
#         hillclimber_alg.run(1000)
#         routes = hillclimber_alg.output()
#         write_solution_to_csv(routes, "output")
#         scores.append(routes_score(routes, map))
#     plot_scores_fancy(scores, title="end scores 1000 iteraties 100 keer, random", save_to_pdf=True)

# if __name__ == "__main__":
#     railnl = RailNL("Holland")
#     algorithm = Random_Greedy(railnl)
#     algorithm.run()
#     routes = algorithm.output()
#     write_solution_to_csv(routes, "output")

# if __name__ == "__main__":
#     result_90 = read_scores_from_csv("time_experiment_results/90.csv")
#     result_100 = read_scores_from_csv("time_experiment_results/100.csv")
#     result_110 = read_scores_from_csv("time_experiment_results/110.csv")
#     result_120 = read_scores_from_csv("time_experiment_results/120.csv")
#     plot_scores_fancy(result_120, result_110, result_100, result_90, 
#                       title = "Random scores given different uniform route time limit.")

# """Example usage plot_scores"""
# if __name__ == "__main__":

#     randomv2_least_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_least_connections_100000.csv")
#     randomv2_most_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_most_connections_100000.csv")

#     plot_scores(randomv2_least_connections, randomv2_most_connections)


# """Example usage plot_scores_fancy"""
if __name__ == "__main__":
    # write_solution_to_csv(Random_Greedy(RailNL("Holland")).run(), "output2")
    
    # randomv2_least_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_least_connections_100000.csv")
    # randomv2_2_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_2_connections_100000.csv")
    # randomv2_3_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_3_connections_100000.csv")
    # randomv2_most_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_most_connections_100000.csv")

    # plot_scores_fancy(Experiment(Random_Greedy).run_experiment(1000),
    #                 Experiment(Random_Greedy).run_experiment(1000, 
    #                 next_connection_choice = "shortest", original_connections_only = True),
                      
    #                   title= "Random algorithm scores",
    #                   legend_labels=("Random", "Greedy"))

    # write_scores_to_csv(Experiment(Random_Greedy).run_experiment(10), "test")
    append_scores_to_csv(Experiment(Random_Greedy).run_experiment(10), "test")