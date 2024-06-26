### 3. MANIM VISUALISATION ###

import os
import subprocess

# CSV files can only tell you so much
# Let's visualise the best solution of your autorun hillclimber project!

# Find files and sort on score
files = os.listdir("parent/code/autorun_hillclimber/mijn_eerste_project/solutions")
files.sort()

# Get highest score 
highest = files[-1]

# Construct path to file from main
path = f"autorun_hillclimber/mijn_eerste_project/solutions/{highest}"

# Set manim settings 
command = ["python3", "set_manim_settings.py", "Holland", path]
subprocess.run(command)

# Now we need to navigate to the correct working directory because we are not software engineers
working_directory = os.getcwd()
new_path = os.chdir(f"{working_directory}/parent/code/visualisation")

# Visualise manim image
command = ["manim", "-pql", "route_visualisation_image.py", "RouteVisualisationImage"]
subprocess.run(command)