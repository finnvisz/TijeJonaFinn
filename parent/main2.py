from parent.code.autorun_hillclimber.autorun_hillclimber import autorun_hillclimber
from parent.code.helpers.plots import logplot_autorun_hillclimber, plot_endscores_autorun_hillclimber

### 2. AUTORUN HILLCLIMBER ###

# This one takes a bit longer, but it's worth it!

project_name = "my_first_project"

# Run the autorun_hillclimber program with the project name "my_first_project"
# Let's start with 10 runs and the smaller map: "Holland"
# This way you can see the results (relatively) quickly and get a feel for the program
autorun_hillclimber(n_runs = 10, 
                    project_name = project_name, 
                    maprange = "Holland", 
                    allow_overwrite = False
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
# Both functions will save the plots in your project directory.

# If you go to your project directory, you will find a directory called "solutions".
# This directory contains the solution produced by each run as a csv file.
# Take a look and see what your best solution looks like!
