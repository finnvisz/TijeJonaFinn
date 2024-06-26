# External imports
import scipy.stats as stats
import numpy as np


def calculate_p_value(sample1: "np.ndarray[float]", sample2: "np.ndarray[float]"
                      , return_type: str = "p_value_only") -> float:
    """
    Calculates a p-value to infer if the difference between two sets of
    scores is significant. Function uses the Mann-Whitney U rank test to
    test the null hypothesis that the distribution underlying sample 1 is
    the same as the distribution underlying sample 2. Return value under
    0.05 is a common threshold for significance.

    - Pre: sample1 and sample2 are independent samples, given as numpy
      arrays of floats. The alternative hypothesis is two-sided (no
      specific directionality).
    
    - Post: returns the p-value of a Mann-Whitney U rank test.

    Args: 
    
    - return_type: 
        
        - "p_value_only" (default)
        
        - "object" (returns full object with test statistic inluded)
        
        - "significant" (returns True if p-value < 0.05)
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