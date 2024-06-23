from parent.code.experiments.statistics import write_scores_to_csv, read_scores_from_csv, append_scores_to_csv, write_solution_to_csv, read_solution_from_csv, calculate_p_value, plot_scores_fancy, plot_hillclimber, append_single_score_to_csv
from parent.code.experiments.experiments import Experiment
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.classes.railnl import RailNL


        
if __name__ == "__main__":
    # append_single_score_to_csv(300.0, "test_jona_3.csv")
    # plot_hillclimber("parent/code/algorithms/autorun_hillclimber/cap_50000/log.csv", title = "Hillclimber: cap_50000", custom_file_path=True)

    solution = read_solution_from_csv("../../algorithms/autorun_hillclimber/agile_zaterdag/solutions/Holland_9188_HC.csv")

