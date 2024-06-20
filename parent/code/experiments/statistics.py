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
# Don't delete! Used in plot_scores_fancy function
experiments_root_dir = "parent/code/experiments"

def read_scores_from_csv(filename: str) -> "np.array[float]":
    """
    Read scores from a CSV file and return them as a numpy array.

    - Pre: CSV file with scores exists in the experiments directory (or path to subdirectory).
    - Post: returns a numpy array with scores.
    """
    # Read scores from CSV file
    scores = np.loadtxt(f"parent/code/experiments/{filename}", delimiter=",")
    return scores

def calculate_p_value(sample1: "np.array[float]", sample2: "np.array[float]", return_type: str = "p_value_only") -> float:
    """
    Calculates a p-value to infer if the difference between two sets of scores is significant.
    Function uses the Mann-Whitney U rank test to test the null hypothesis that 
    the distribution underlying sample 1 is the same as the distribution underlying sample 2.
    Return value under 0.05 is a common threshold for significance.

    - Pre: sample1 and sample2 are independent samples, given as numpy arrays of floats.
    The alternative hypothesis is two-sided (no specific directionality).
    - Post: returns the p-value of a Mann-Whitney U rank test.

    options:
    - return_type: "p_value_only" (default), "object" (returns full object with test statistic inluded),
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

def plot_scores_fancy(sample1: "np.array[float]", sample2: "np.array[float]" = None, 
                      sample3: "np.array[float]" = None, sample4: "np.array[float]" = None, 
                      
                      save_to_pdf: bool = False, preview: bool = True, # save settings
                      filename: str | None = None,
                      
                      title: str | None = None, binwidth: int = 400, # plot settings
                      alpha: float | None = None) -> None:
    """
    Plot the scores of 1 to 4 samples in a histogram.

    - Pre: Each sample is given as a numpy arrays of floats.
    - Post: histogram is plotted (default: only preview, save to pdf also possible).

    args:

    Save settings:
    - `save_to_pdf`: save plot to pdf file in directory `plot_dir` (which is defined right after
    the imports of this script).
    - `preview`: show preview of plot.
    - `filename`: (optional) custom filename for the plot. 
    When not provided, user-provided `title` is used or else a default name with timestamp.
    
    Plot settings:
    - `title`: (optional) title of the plot, also used as filename if saved to pdf.
    When not provided, a default name with timestamp is used.
    - `binwidth`: width of the bins in the histogram (default is 400, seems a sweet spot).
    - `alpha`: (optional) set custom transparency of the bars in the histogram
    """
    # Settings for plot
    color_palette = ("lightblue", "lightgrey", "lightsalmon", "lightgreen")
    p9.options.figure_size = (9, 5) # overwritten for single sample

    
    # Complex decision tree to determine filename and title
    # See docs for more info
    if filename is not None:
        if title is None:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
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
    
        
    # If sample2 is not provided, create plot for single sample
    if sample2 is None:
        
        # Smaller width for single sample (because no legend)
        p9.options.figure_size = (8, 5)

        # Create dataframe with scores
        df = pd.DataFrame({
            "sample1": sample1,
        })

        # Default alpha value
        if alpha is None:
            alpha = 0.85

        # Histogram for single sample
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "sample1") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, position = "identity", fill = color_palette[0], color = "darkgrey") +
            p9.xlim(0,10000) + 
            p9.labs(title = title, x = "Score", 
                    y = "Aantal waarnemingen") + 
            p9.theme_minimal()
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
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, position = "identity", color = "darkgrey") +
            p9.xlim(0,10000) + 
            p9.labs(title = title, y = "Aantal waarnemingen") + 
            p9.scale_fill_manual(values = color_palette[:2]) +
            p9.theme_minimal()
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
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, position = "identity", color = "darkgrey") +

            p9.xlim(0,10000) + 
            p9.labs(title = title, y = "Aantal waarnemingen") + 
            p9.scale_fill_manual(values = color_palette[:3]) +
            p9.theme_minimal()
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
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, position = "identity", color = "darkgrey") +

            p9.xlim(0,10000) + 
            p9.labs(title = title, y = "Aantal waarnemingen") + 
            p9.scale_fill_manual(values = color_palette) +
            p9.theme_minimal() 
            # + p9.theme(figure_size=(16, 8))
        )

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
    
    plt.savefig(f"plots/{filename}.png")

def routes_to_csv(routes: list[Route], filename: str):
    """
    Translate algorithm output to required csv file.
    
    - Pre: list of route objects and filename to write to.
    - Post: csv-file of given format located in route_csv map. 
    """
    
    with open(f"{experiments_root_dir}/route_csv/{filename}.csv", 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["train", "stations"])

        for i in range(len(routes)):
            writer.writerow([f"train_{i+1}", routes[i].stations_list()])

        score = routes_score(routes, "Holland")
        writer.writerow(["score", f"{score}"])

if __name__ == "__main__":
    map = "Holland"
    data = RailNL(map)
    scores = []
    for _ in range(10):
        algorithm = Random_Greedy(data)
        algorithm.run()
        hillclimber_alg = Hillclimber(data, algorithm, map)
        hillclimber_alg.run(100)
        routes = hillclimber_alg.output()
        routes_to_csv(routes, "output")
        scores.append(routes_score(routes, map))
    plot_scores_fancy(scores, title="end scores 100 iteraties, random", save_to_pdf=True)

# if __name__ == "__main__":
#     railnl = RailNL("Holland")
#     algorithm = Finn(railnl)
#     algorithm.run()
#     routes = algorithm.output()
#     routes_to_csv(routes, "output")

# if __name__ == "__main__":

#     # Example usage
#     randomv2_least_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_least_connections_100000.csv")
#     randomv2_most_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_most_connections_100000.csv")

#     plot_scores_fancy(randomv2_least_connections, randomv2_most_connections)

    # # Example usage
    # randomv2_least_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_least_connections_100000.csv")
    # randomv2_2_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_2_connections_100000.csv")
    # randomv2_3_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_3_connections_100000.csv")
    # randomv2_most_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_most_connections_100000.csv")

    # plot_scores_fancy(randomv2_least_connections, randomv2_2_connections, randomv2_3_connections, randomv2_most_connections, title="Bewijs dat 4 datasets werkt")

# if __name__ == "__main__":
#     # Example usage
    # randomv2_least_connections = read_scores_from_csv("randomv2_least_connections")
    # randomv2_most_connections = read_scores_from_csv("randomv2_most_connections")

    # plot_scores(randomv2_least_connections, randomv2_most_connections)