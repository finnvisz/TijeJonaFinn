# External imports
import numpy as np

# Local imports
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.random_v2 import Randomv2
from parent.code.experiments.experiments import Experiment

def get_station_subgroups() -> tuple[list["Station"], list["Station"]]:
    """
    Returns two lists of stations: one with the stations with 
    the most connections and one with the stations with the least connections.
    """
    # Initialize RailNL to get station data
    railnl = RailNL("Holland")

    # Create collection with various subgroups of stations:
    Stations = railnl.stations_dict()

    # 1. Stations with most connections
    stations_with_most_connections = []

    max_connections = railnl.max_connections()

    for station in Stations.values():
        if station.amount_connecting() == max_connections:
            stations_with_most_connections.append(station)

    # 2. Stations with least connections
    stations_with_least_connections = []

    min_connections = railnl.min_connections()

    for station in Stations.values():
        if station.amount_connecting() == min_connections:
            stations_with_least_connections.append(station)

    # Return the lists of both subgroups
    return stations_with_most_connections, stations_with_least_connections
    

if __name__ == "__main__":
    # Get station subgroups
    stations_with_most_connections, stations_with_least_connections = get_station_subgroups()

    # Initialize experiment
    randomv2_experiment = Experiment(Randomv2, "Holland")


    # Run algorithm with different starting stations:
    iterations = 12
    # With least connections
    results_least_connections = randomv2_experiment.run_experiment(iterations=iterations, starting_stations="custom_list_with_replacement", 
                                                starting_station_list = stations_with_least_connections)
    randomv2_experiment.write_scores_to_csv("randomv2_least_connections")

    # With most connections
    results_most_connections = randomv2_experiment.run_experiment(iterations=iterations, starting_stations="custom_list_with_replacement", 
                                                starting_station_list = stations_with_most_connections)
    randomv2_experiment.write_scores_to_csv("randomv2_most_connections")


    # Calculate average scores
    print(f"Average score for stations with least connections: {np.mean(results_least_connections)}")
    print(f"Average score for stations with most connections: {np.mean(results_most_connections)}")