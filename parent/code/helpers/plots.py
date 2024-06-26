# External imports
import numpy as np
import plotnine as p9
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Internal imports
from parent.code.helpers.csv_helpers import read_scores_from_csv

# Default directory for all functions in this file, can be changed if needed
# Don't delete! Used by all functions in this file.
experiments_root_dir = "parent/code/experiments"

def plot_scores(sample1: "np.ndarray[float]", 
                      sample2: "np.ndarray[float]" = None, 
                      sample3: "np.ndarray[float]" = None, 
                      sample4: "np.ndarray[float]" = None, 
                      
                      # save settings
                      save_to_pdf: bool = False,
                      plot_dir: str | None = None, 
                      preview: bool = True, 
                      filename: str | None = None,
                      
                      # plot settings
                      title: str | None = None, 
                      legend_title: str = "Groep",
                      legend_labels: tuple[str] | None = None,
                      binwidth: int = 400, 
                      xlim: tuple[int] | None = None,
                      alpha: float | None = None) -> None:
    """
    Plot the scores of 1 to 4 samples in a histogram.

    - Pre: Each sample is given as a numpy arrays of floats.
    
    - Post: histogram is plotted (default: only preview, save to pdf also
      possible).

    Example usage: `plot_scores(sample1, sample2, title = "Condition 1 vs
    Condition 2", legend_labels = ("Condition 1", "Condition 2"))`

    args:

    Save settings:

    - save_to_pdf: save plot to pdf file in directory `plot_dir`.
    
    - plot_dir: (optional) custom directory to save the plot to. 
    Default is `parent/code/experiments/plots`.
    
    - preview: show preview of plot.
    
    - filename: (optional) custom filename for the plot. When not 
    provided, user-provided `title` is used or else a default name with
    timestamp.
    
    Plot settings:
    
    - title: title of the plot, also used as filename if saved to pdf.
    When not provided, a default name with timestamp is used.
    
    - legend_title: title of the legend in the plot. Default is "Groep".
    
    - legend_labels: custom labels for the legend. Should be a tuple
    of strings with the same length as the number of samples.
    
    - binwidth: width of the bins in the histogram (default is 400, 
    seems a sweet spot).
    
    - xlim: (optional) set custom x-axis limits for the plot.
    
    - alpha: (optional) set custom transparency of the bars in the 
    histogram. Value between 0 and 1. Default is 0.85 for single sample
    and 0.7 for multiple samples.
    """

    # Infer number of samples provided from input
    n_samples: int = sum([sample1 is not None, sample2 is not None, 
                    sample3 is not None, sample4 is not None])

    # Settings for plot
    color_palette = ("lightblue", "lightgrey", "lightsalmon", "lightgreen")
    p9.options.figure_size = (9, 5) # overwritten for single sample
    
    # Complex decision tree to determine filename and title
    # See docs for more info
    if filename is not None:
        if title is None:
            # get current time
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            # Set title
            title = f"Histogram: fancy_plot_{current_time}"
    
    else:
        if title is not None:
            filename = title
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            filename = f"fancy_plot_{current_time}"
            title = f"Histogram: {filename}"

    # Add .pdf extension if not present
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    # Ensure correct legend labels
    # If provided, check for correct amount of labels
    if legend_labels is not None:
        assert len(legend_labels) == n_samples, """
        Number of legend labels should match number of samples."""
    
    # If not provided, use default labels
    else:
        legend_label_options = ("Sample 1", "Sample 2", "Sample 3", "Sample 4")
        legend_labels = legend_label_options[:n_samples]

        
    if xlim is None:
        lower_bound_xlim = min(sample1)
        xlim = (lower_bound_xlim, 10000)

    # If single sample is provided, create plot for single sample
    if n_samples == 1:
        
        # Smaller width for single sample (because no legend)
        p9.options.figure_size = (8, 5)

        # Create dataframe with scores
        df = pd.DataFrame({
            "Score": sample1,
        })

        # Default alpha value
        if alpha is None:
            alpha = 0.85

        # Histogram for single sample
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", fill = color_palette[0], 
                              color = "darkgrey")
        )
    
    # Else create plot for 2 samples
    elif n_samples == 2:
        
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2
        })

        df = df.melt(value_vars=['Sample 1','Sample 2'], 
                     var_name='Groep', 
                     value_name='Score')

        # Default alpha value
        if alpha is None:
            alpha = 0.7

        # Histogram for 2 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Groep", colour = "Groep") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", color = "darkgrey")
        )

    # Else create plot for 3 samples
    elif n_samples == 3:
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2,
            "Sample 3": sample3
        })

        df = df.melt(value_vars=['Sample 1','Sample 2', 'Sample 3'], 
                     var_name='Groep', 
                     value_name='Score')

        # Default alpha value
        if alpha is None:
            alpha = 0.7

        # Histogram for 3 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Groep", colour = "Groep") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", color = "darkgrey")
        )

    # Else create plot for 4 samples
    else:
        # Create dataframe with scores
        df = pd.DataFrame({
            "Sample 1": sample1,
            "Sample 2": sample2,
            "Sample 3": sample3,
            "Sample 4": sample4
        })

        df = df.melt(value_vars=['Sample 1','Sample 2', 'Sample 3', 'Sample 4'], 
                     var_name='Groep', 
                     value_name='Score')

        # Default alpha value
        if alpha is None:
            alpha = 0.7

        # Histogram for 4 samples
        plot = (
            p9.ggplot(df) +
            p9.aes(x = "Score", fill = "Groep", colour = "Groep") +
            p9.geom_histogram(binwidth = binwidth, alpha = alpha, 
                              position = "identity", color = "darkgrey")    
        )
    
    # Add labels, title, theme and limits
    # The same for all plots
    plot += p9.xlim(xlim)
    plot += p9.scale_fill_manual(name = legend_title,
                                values = 
                                color_palette[:n_samples],
                                labels = legend_labels)
    plot += p9.theme_minimal() 
    plot += p9.labs(title = title, 
                    subtitle= f"Runs = {len(sample1)}", 
                    y = "Aantal waarnemingen")

    # Save to pdf if specified
    if save_to_pdf:
        if plot_dir is None:
            plot_dir = f"{experiments_root_dir}/plots"
        
        plot.save(filename = filename, path = plot_dir)
    
    # Show preview of plot if specified
    if preview:
        # Show the plot
        plot.show()

def logplot_autorun_hillclimber(project_name: str | None = None,
                             use_aggregated: bool = False, 
                    
                    # plot settings
                    title: str | None = None,

                    # save settings
                    save_to_pdf: bool = True, 
                    preview: bool = False,
                    custom_file_path: str | None = None
                    ) -> None:
    """
    Create a plot to summarize an autorun_hillclimber log file. 
    (Note: may take a while when run on raw log file, 
    set `use_aggregated` when re-running.)

    - Pre: Project `project_name` with log data created by 
    autorun_hillclimber exists.
    
    - Post: plot is created and saved to the project directory
    (default: only save to pdf, preview also possible).

    Args:
    
    - project_name (str): name of the project in
    `parent/code/autorun_hillclimber/` with log data.
    
    - use_aggregated (bool): if True, use the aggregated log data 
    produced as byproduct of this function. If you rerun this function 
    on an unchanged project, setting this to True will greatly increase 
    speed.
    
    Plot settings:
    
    - title (str): title of the plot, shown in plot and becomes filename
      for pdf file. If not provided, title is set to project name.

    Save settings:
    
    - save_to_pdf (bool): save plot to pdf file in directory
      `pdf_save_dir`. Default is True.
    
    - preview (bool): show preview of plot. Default is False.
    
    - custom_file_path (str): if provided, override `project_name` and
        set custom file path to read log data from. Plot is saved to
        the directory of the custom file path.
    """
    
    # Input check
    if project_name is None and custom_file_path is None:
        raise ValueError("Please provide a project name or custom file path.")


    # If custom file path is set, override default directory and project 
    # name so user can specify path from parent directory
    if custom_file_path is not None:
        log_file_path = custom_file_path

        # Add .csv extension if not present
        if not log_file_path.endswith(".csv"):
            log_file_path += ".csv"

        log_file_dir = custom_file_path.rsplit("/", 1)[0]
    
    # Else fill in project name for autorun_hillclimber
    else:
        log_file_dir = f"parent/code/autorun_hillclimber/{project_name}"
        log_file_path = f"{log_file_dir}/log.csv"
    
    # Prepare the data:

    # If use_aggregated is False, create aggregated log data first
    if not use_aggregated:
        print("Reading raw CSV log data...")

        # Read the existing CSV file into a DataFrame 
        df_data = pd.read_csv(f"{log_file_path}", 
                            header=None)
        
        print("Read-in of raw CSV log data successful.")
        print("Aggregating data. This might take a while...")

        # Create a new dataframe with the mean, max and min
        df_data_aggregated = df_data.agg(['mean', 'max', 'min'], axis=1).reset_index()
        
        print("Aggregation of data successful.")
        print("Melting aggregated data...")

        # Melt dataframe to long format for plotnine
        df_data_aggregated = df_data_aggregated.melt(id_vars='index', 
                                                    var_name="Statistiek", 
                                                    value_name=f"Score (n_runs={len(df_data.columns)})")
        
        # Rename column 0 to "Iteraties"
        df_data_aggregated.rename(columns = {"index": "Iteraties (0 indexed)"},
                                  inplace = True)

        # Save the aggregated data disk for future use
        df_data_aggregated.to_csv(f"{log_file_dir}/log_aggregated.csv",
                                header=True, 
                                index=True)

        print("Melting of aggregated data successful. Saved to log_aggregated.csv.")
        
    # If use_aggregated is True, read the aggregated log data
    else:
        print("Reading aggregated CSV log data...")
        
        # Read the existing CSV file into a DataFrame 
        df_data_aggregated = pd.read_csv(f"{log_file_dir}/log_aggregated.csv", 
                             header = 0, 
                             index_col = 0)

        print("Read-in of aggregated CSV log data successful.")


    print("Creating plot...")

    # Settings for plot
    color_palette = ("lightblue", "darkgrey", "lightsalmon")
    legend_labels = ("Max", "Gemiddelde", "Min")

    p9.options.figure_size = (9, 5)
    p9.geoms.geom_line.DEFAULT_AES['size'] = 2


    # Set default title if not provided
    if title is None:
        if project_name is not None:
            # Set title to input filename
            title = f"Hillclimber: {project_name}"
            
        else:
            # Set title to default
            title = "Hillclimber log"

    # Save column names
    column_names = df_data_aggregated.columns

    # Get number of runs from last column name
    n_runs = column_names[-1].split("=")[1].split(")")[0]

    # Infer max iterations from the last row of the first column
    max_iterations = (df_data_aggregated.iloc[:, 0].values[-1]) + 1

    # Get ylim from df_data_aggregated
    ylim_min = round(df_data_aggregated.iloc[:, -1].values[0])
    
    # If first solution of project is Nationaal, set ylim_max to 7600
    if os.listdir(f"{log_file_dir}/solutions")[0].split("_")[0] == "Nationaal":
        ylim_max = 7600
    # Else set ylim_max to 10000
    else:
        ylim_max = 10000

    # Create plotnine plot with the mean, max and min per iteration
    plot = (
        p9.ggplot(df_data_aggregated) +
        p9.aes(x = column_names[0], 
               y = column_names[2], 
               color = column_names[1]) +
        
        p9.geom_line() +

        p9.ylim(ylim_min, ylim_max) +
        
        p9.scale_color_manual(name = "Per iteratie",
                            values = color_palette, 
                            labels = legend_labels) +
        
        p9.labs(title = title,
                subtitle = f"Aantal runs = {n_runs}, max. iteraties = {max_iterations}",
                x = "Iteraties", 
                y = "Score") +
        
        p9.theme_minimal()
    )

    print("Plot created successfully.")


    # Save to pdf if specified
    if save_to_pdf:
        # Set filename
        if project_name is not None:
            pdf_filename = f"logplot_{project_name}.pdf"
        else:
            pdf_filename = "logplot.pdf"
        
        plot.save(filename = pdf_filename, path = log_file_dir)
        print(f"Plot saved to {log_file_dir}/{pdf_filename}")

    # Show preview of plot if specified
    if preview:
        # Show the plot
        plot.show()
    
def plot_endscores_autorun_hillclimber(project_name: str, 
                                       title: str | None = None
                                       ) -> None:
    """
    Plot the end scores of an autorun_hillclimber project.

    Pre: Project `project_name` with `end_scores.csv` exists in
    `parent/code/autorun_hillclimber/`.

    Post: plot is created and saved to the project directory.

    Args:

    - project_name: name of autorun_hillclimber project
    (without path or extension).

    - title (optional): title of the plot. Default is 
    "Hillclimber 'project_name': verdeling van eindscores".
    """
    
    # Set project directory
    project_dir = f"parent/code/autorun_hillclimber/{project_name}"
    # Set plot directory to root of project (may become subdir in future)
    plot_dir = project_dir
    
    # Read the end_scores from the autorun_hillclimber project directory
    end_scores = read_scores_from_csv(f"{project_dir}/end_scores.csv", 
                                      custom_file_path = True)

    # Set title
    if title is None:
        title = f"Hillclimber '{project_name}': verdeling van eindscores"

    # Plot the end_scores
    plot_scores(end_scores, 
                      title = title, 
                      binwidth=10, 
                      xlim=(min(end_scores), max(end_scores)), 
                      preview = False,
                      save_to_pdf=True,
                      filename = f"end_scores_plot_{project_name}",
                      plot_dir = plot_dir)
    
    print(f"\nEnd scores plot for '{project_name}'", 
          f"created successfully and saved to {plot_dir}")