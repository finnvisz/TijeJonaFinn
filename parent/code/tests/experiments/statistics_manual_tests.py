import pandas as pd
import numpy as np

from parent.code.experiments.statistics import write_scores_to_csv, read_scores_from_csv, append_scores_to_csv, write_solution_to_csv, read_solution_from_csv, calculate_p_value, plot_scores_fancy, plot_autorun_hillclimber, append_single_score_to_csv, plot_endscores_autorun_hillclimber
from parent.code.experiments.experiments import Experiment
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.classes.railnl import RailNL


        
if __name__ == "__main__":
    connecties_holland = pd.read_csv("parent/data/ConnectiesHolland.csv", header = None, names = ["station1", "station2", "time"], index_col = False)

    sum_time = connecties_holland["time"].sum()
    print(f"Total time for Holland: {sum_time}")

    p = 1
    T = 4
    Min = sum_time

    K = p*10000 - (T*100 + Min)

    print(f"K: {K}")