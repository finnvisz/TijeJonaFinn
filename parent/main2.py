import sys

from parent.code.autorun_hillclimber.autorun_hillclimber import autorun_hillclimber
from parent.code.helpers.plots import logplot_autorun_hillclimber, plot_endscores_autorun_hillclimber

### 2. AUTORUN HILLCLIMBER ###
# Check that the user has provided a project name
if len(sys.argv) != 2 or sys.argv[1] == "": 
    print("Usage: python3 parent/main2.py <project_name>")
    sys.exit(1)

# Set projectname with command line argument
project_name = sys.argv[1]

# Run the autorun_hillclimber program with the given project name
autorun_hillclimber(n_runs = 10, 
                    project_name = project_name, 
                    maprange = "Holland", 
                    allow_overwrite = True,
                    demo_mode = True
                    )

# Now that you have an autorun hillclimber project, you can get a
# summary of your logfile using a plot:
logplot_autorun_hillclimber(project_name = project_name, 
                         title = f"Logplot voor {project_name}", 
                         use_aggregated = False
                         )

# You can also plot the endscores your hillclimber achieved:
plot_endscores_autorun_hillclimber(project_name = project_name)

print("\nDone! Your first Autorun Hillclimber project is finished.")
print(f"Go to 'parent/code/autorun_hillclimber/{project_name}' to see the results.")

