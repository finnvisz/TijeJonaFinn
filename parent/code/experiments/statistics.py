# External imports
import numpy as np
import scipy.stats as stats
# import plotnine
# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

# Internal imports
from parent.code.algorithms.random_algorithm import RandomAlgorithm
from parent.code.experiments.experiments import Experiment
from parent.code.classes.route import Route
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.score import routes_score

plot_dir = "parent/code/experiments/plots/"

def read_scores_from_csv(filename: str) -> "nparray[float]":
    """
    Read scores from a CSV file and return them as a numpy array.

    - Pre: CSV file with scores exists in the results directory.
    - Post: returns a numpy array with scores.
    """
    # Read scores from CSV file
    scores = np.loadtxt(f"parent/code/experiments/results/{filename}.csv", delimiter=",")
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

def plot_scores(sample1: "nparray[float]", sample2: "nparray[float]") -> None:
    """
    Plot the scores of two samples in a histogram.

    - Pre: sample1 and sample2 are independent samples, given as numpy arrays of floats.
    - Post: histogram is plotted.
    """
    # Create dataframe with scores
    df = pd.DataFrame({
        "sample1": sample1,
        "sample2": sample2
    })

    # Plot the histogram
    plot = (
        plotnine.ggplot(df) +
        plotnine.aes(x="sample1") +
        plotnine.geom_histogram(bins=20, fill="blue", alpha=0.7) +
        plotnine.aes(x="sample2") +
        plotnine.geom_histogram(bins=20, fill="red", alpha=0.7) +
        plotnine.ggtitle("Frequency Distribution of Scores") +
        plotnine.xlab("Score") +
        plotnine.ylab("Frequency") +
        plotnine.theme_minimal()
    )

    # Show the plot
    plot.show()
    # plot.save(filename = "test.pdf", path=plot_dir)

def plot_frequency_of_scores(filename: str, scores: list[float]):
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
    
#     - Pre: list of route objects and filename to write to.
#     - Post: csv-file of given format located in route_csv map. 
#     """

    with open(f"route_csv/{filename}.csv", 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["train", "stations"])

        for i in range(1, len(routes) + 1):
            writer.writerow([f"train_{i}", routes[i - 1].stations_list()])

        score = routes_score(routes, "Holland")
        writer.writerow(["score", f"{score}"])

if __name__ == "__main__":
    railnl = RailNL("Holland")
    algorithm = RandomAlgorithm(railnl, [7], 120)
    algorithm.run()
    routes = algorithm.output()
    routes_to_csv(routes, "output")

# if __name__ == "__main__":

#     # Example usage
#     randomv2_least_connections = read_scores_from_csv("randomv2_least_connections")
#     randomv2_most_connections = read_scores_from_csv("randomv2_most_connections")

# if __name__ == "__main__":
#     # Example usage
    # randomv2_least_connections = read_scores_from_csv("randomv2_least_connections")
    # randomv2_most_connections = read_scores_from_csv("randomv2_most_connections")

    # plot_scores(randomv2_least_connections, randomv2_most_connections)


