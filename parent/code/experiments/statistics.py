# External imports
import numpy as np
import scipy.stats as stats


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


if __name__ == "__main__":
    # Example usage
    randomv2_least_connections = read_scores_from_csv("randomv2_least_connections")
    randomv2_most_connections = read_scores_from_csv("randomv2_most_connections")

    print(calculate_p_value(randomv2_least_connections, randomv2_most_connections, return_type="p_value_only"))