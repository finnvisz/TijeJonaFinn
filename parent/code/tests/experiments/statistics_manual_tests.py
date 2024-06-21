from parent.code.experiments.statistics import write_scores_to_csv, read_scores_from_csv, append_scores_to_csv, write_solution_to_csv, read_solution_from_csv, calculate_p_value, plot_scores_fancy
from parent.code.experiments.experiments import Experiment
from parent.code.algorithms.random_greedy import Random_Greedy

if __name__ == '__main__':
    write_solution_to_csv(Random_Greedy().run(), "test_jona.csv")

    solution = read_solution_from_csv("test_jona.csv")

    print(solution)