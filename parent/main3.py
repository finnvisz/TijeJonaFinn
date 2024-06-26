### 3. MANIM VISUALISATION ###
import sys
import os
import subprocess

# CSV files can only tell you so much
# Let's visualise the best solution of your autorun hillclimber project!

# Check that the user has provided a project name
if len(sys.argv) != 2 or sys.argv[1] == "": 
    print("Usage: python3 parent/main3.py <project_name>")
    sys.exit(1)

# Set projectname with command line argument
project_name = sys.argv[1]

# Find files and sort on score
files = os.listdir(f"parent/code/autorun_hillclimber/{project_name}/solutions")
files.sort()

# Get highest score 
highest = files[-1]

# Construct path to file from main
path = f"autorun_hillclimber/{project_name}/solutions/{highest}"

# Now we need to navigate to the correct working directory because we are not software engineers
working_directory = os.getcwd()
new_path = os.chdir(f"{working_directory}/parent/code/visualisation")

# Set manim settings 
command = ["python3", "set_manim_settings.py", "Holland", path]
subprocess.run(command)

# Visualise manim image
command = ["manim", "-pql", "route_visualisation_image.py", "RouteVisualisationImage"]
subprocess.run(command)