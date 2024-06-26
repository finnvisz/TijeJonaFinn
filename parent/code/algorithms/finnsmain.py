
from parent.code.experiments.statistics import plot_autorun_hillclimber, plot_endscores_autorun_hillclimber, plot_scores


plot_autorun_hillclimber(project_name = "nationaal_30000_iteraties_20_routes", 
                         title = "Logplot: nationaal_30000_iteraties_20_routes", 
                         use_aggregated = False
                         )


plot_endscores_autorun_hillclimber(project_name = "nationaal_30000_iteraties_20_routes")