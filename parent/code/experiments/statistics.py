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
from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.algorithms.finnsroutes import Finn
from parent.code.experiments.experiments import Experiment
from parent.code.classes.route import Route
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.score import routes_score


# Default directory for plots, can be changed if needed
plot_dir = "parent/code/experiments/plots"


def read_scores_from_csv(filename: str) -> "nparray[float]":
    """
    Read scores from a CSV file and return them as a numpy array.

    - Pre: CSV file with scores exists in the experiments directory (or path to subdirectory).
    - Post: returns a numpy array with scores.
    """
    # Read scores from CSV file
    scores = np.loadtxt(f"parent/code/experiments/{filename}", delimiter=",")
    return scores

def calculate_p_value(sample1: "nparray[float]", sample2: "nparray[float]", return_type: str = "p_value_only") -> float:
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


def plot_scores_fancy(sample1: "nparray[float]", sample2: "nparray[float]" = None, 
                      title: str = "fancy_plot", save_to_pdf: bool = False, preview: bool = True,
                      binwidth: int = 400) -> None:
    """
    Plot the scores of one or two samples in a histogram.

    - Pre: sample1 (and sample2) is and independent sample, given as a numpy arrays of floats.
    - Post: histogram is plotted.
    """
    # If name left on default, add current time
    if title == "fancy_plot":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        title += f"_{current_time}"

    # If sample2 is not provided, create plot for single sample
    if sample2 is None:
        
        # Create dataframe with scores
        df = pd.DataFrame({
            "sample1": sample1,
            # "sample2": sample2
        })

        # Histogram for single sample
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "sample1") +
            p9.geom_histogram(binwidth = binwidth, alpha = .85, position = "identity", fill = "lightblue", color = "darkgrey") +
            p9.xlim(0,10000) + 
            p9.labs(title = f"Histogram: {title}", x = "Score", 
                    y = "Aantal waarnemingen", fill = "Sample", colour = "Sample") + 
            # p9.scale_fill_manual(values = ("lightgreen", "lightsalmon")) +
            p9.theme_minimal()
        )
    
    # Else create plot for 2 samples
    else:
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2
        })

        df = df.melt(value_vars=['Sample 1','Sample 2'], var_name='Group', value_name='Score')


        # Histogram for 2 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Group", colour = "Group") +
            p9.geom_histogram(binwidth = binwidth, alpha = .85, position = "identity", color = "darkgrey") +

            p9.xlim(0,10000) + 
            p9.labs(title = f"Histogram: {title}", y = "Aantal waarnemingen") + 
            p9.scale_fill_manual(values = ("lightgreen", "lightsalmon")) +
            p9.theme_minimal()
        )


    # Show preview of plot if specified
    if preview:
        # Show the plot
        plot.show()

    # Save to pdf if specified
    if save_to_pdf:
        plot.save(filename = f"{title}.pdf", path=plot_dir)


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

    with open(f"route_csv/{filename}.csv", 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["train", "stations"])

        for i in range(len(routes)):
            writer.writerow([f"train_{i+1}", routes[i].stations_list()])

        score = routes_score(routes, "Holland")
        writer.writerow(["score", f"{score}"])

# if __name__ == "__main__":
#     railnl = RailNL("Holland")
#     algorithm = Finn(railnl)
#     algorithm.run()
#     routes = algorithm.output()
#     routes_to_csv(routes, "output")

if __name__ == "__main__":

    # Example usage
    randomv2_least_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_least_connections_100000.csv")
    randomv2_most_connections = read_scores_from_csv("best_starting_stations/results/with_replacement/randomv2_most_connections_100000.csv")

    plot_scores_fancy(randomv2_least_connections, randomv2_most_connections)


# if __name__ == "__main__":
#     # Example usage
    # randomv2_least_connections = read_scores_from_csv("randomv2_least_connections")
    # randomv2_most_connections = read_scores_from_csv("randomv2_most_connections")

    # plot_scores(randomv2_least_connections, randomv2_most_connections)