import pandas as pd
import numpy as np

from parent.code.experiments.statistics import write_scores_to_csv, read_scores_from_csv, append_scores_to_csv, write_solution_to_csv, read_solution_from_csv, calculate_p_value, plot_scores_fancy, plot_autorun_hillclimber, append_single_score_to_csv
from parent.code.experiments.experiments import Experiment
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.algorithms.hillclimber import Hillclimber
from parent.code.classes.railnl import RailNL


        
if __name__ == "__main__":
    # solution = read_solution_from_csv("../../algorithms/autorun_hillclimber/4_routes_zondag/solutions/Holland_9192_HC")

    # i = 1
    # for route in solution:
    #     print(f"Route {i}: {route.time} minuten")
    #     i += 1

    plot_autorun_hillclimber(project_name="zondagnacht_cap_30000", title="Hillclimber: zondagnacht_cap_30000", use_aggregated=False)

    # end_scores_zaterdag = read_scores_from_csv("parent/code/algorithms/autorun_hillclimber/agile_zaterdag/end_scores.csv", custom_file_path=True)
    # end_scores_zondag = read_scores_from_csv("parent/code/algorithms/autorun_hillclimber/4_routes_zondag/end_scores.csv", custom_file_path=True)

    # plot_scores_fancy(end_scores_zondag, title="Hillclimber '4_routes_zondag': verdeling van eindscores", binwidth=10, xlim=(min(end_scores_zondag), max(end_scores_zondag)), save_to_pdf=True)



    # np.savetxt("parent/code/algorithms/autorun_hillclimber/agile_zaterdag/test_error_bericht.csv", 
    #                [230])
    
    




    # ConnectiesHolland = pd.read_csv("parent/data/ConnectiesHolland.csv", 
    #                     header=None)
    
    # ConnectiesHolland.columns = ["Station1", "Station2", "Afstand"]

    # ConnectiesHolland["Afstand"] = ConnectiesHolland["Afstand"].astype(int)

    # print(sum(ConnectiesHolland["Afstand"])/ 120)

