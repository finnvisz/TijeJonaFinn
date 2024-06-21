from parent.code.experiments.statistics import write_scores_to_csv, read_scores_from_csv, append_scores_to_csv, write_solution_to_csv, read_solution_from_csv, calculate_p_value, plot_scores_fancy, plot_hillclimber
from parent.code.experiments.experiments import Experiment
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.classes.railnl import RailNL

if __name__ == "__main__":
    
    # for i in range(20):
    #     data = RailNL()

    #     # Test Hillclimber algorithm with RandomAlgorithm as starting state
    #     random_alg = Random_Greedy()
    #     random_alg.run()
    #     hillclimber_alg = Hillclimber(data, random_alg, "Holland")
    #     hillclimber_alg.run(1000, data_csv = "test_jona.csv")

    plot_hillclimber("test_jona.csv", title = "Hillclimber: progressie over iteraties")
        


# if __name__ == '__main__':
#     write_solution_to_csv(Random_Greedy().run(), "test_jona.csv")

#     solution = read_solution_from_csv("test_jona.csv")

#     print(solution)