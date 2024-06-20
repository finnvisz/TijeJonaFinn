# External imports
import numpy as np

# Local imports
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.random_greedy import Random_Greedy
from parent.code.experiments.experiments import Experiment
from parent.code.classes.station_class import Station

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
    print(f"Max connections: {max_connections}")

    for station in Stations.values():
        if station.amount_connecting() == max_connections:
            stations_with_most_connections.append(station)

    print(f"Amount of stations with most connections: {len(stations_with_most_connections)}")

    # 2. Stations with least connections
    stations_with_least_connections = []

    min_connections = railnl.min_connections()
    print(f"Min connections: {min_connections}")

    for station in Stations.values():
        if station.amount_connecting() == min_connections:
            stations_with_least_connections.append(station)

    print(f"Amount of stations with least connections: {len(stations_with_least_connections)}")


    # 3. Stations with 2 connections
    stations_with_2_connections = []

    for station in Stations.values():
        if station.amount_connecting() == 2:
            stations_with_2_connections.append(station)

    print(f"Amount of stations with 2 connections: {len(stations_with_2_connections)}")

    # 4. Stations with 3 connections
    stations_with_3_connections = []

    for station in Stations.values():
        if station.amount_connecting() == 3:
            stations_with_3_connections.append(station)

    print(f"Amount of stations with 3 connections: {len(stations_with_3_connections)}")


    # # 5. Stations in between the two extremes combined (2 or 3 connections for Holland)
    # stations_in_between = []
    
    # amounts_of_connections_in_between = list(range(min_connections + 1, max_connections))
    # print(f": Amounts of connections in between the 2: {amounts_of_connections_in_between}")

    # for station in Stations.values():
    #     if station.amount_connecting() in amounts_of_connections_in_between:
    #         stations_in_between.append(station)

    # print(f"Amount of stations with connections in between: {len(stations_in_between)}")


    # Return the lists of the 4 subgroups
    return stations_with_most_connections, stations_with_least_connections, stations_with_2_connections, stations_with_3_connections
    
if __name__ == "__main__":
    # Get station subgroups
    stations_with_most_connections, stations_with_least_connections, stations_with_2_connections, stations_with_3_connections = get_station_subgroups()

    # Initialize experiment
    randomv2_experiment = Experiment(Random_Greedy, "Holland")


    # Run algorithm with different starting stations:
    iterations = 100000

    # With least connections
    results_least_connections = randomv2_experiment.run_experiment(iterations=iterations, starting_stations="custom_list_without_replacement", 
                                                starting_station_list = stations_with_least_connections)
    randomv2_experiment.write_scores_to_csv(f"best_starting_stations/results/randomv2_least_connections_{iterations}")   

    # With most connections
    results_most_connections = randomv2_experiment.run_experiment(iterations=iterations, starting_stations="custom_list_without_replacement", 
                                                starting_station_list = stations_with_most_connections)
    randomv2_experiment.write_scores_to_csv(f"best_starting_stations/results/randomv2_most_connections_{iterations}")

    # With 2 connections
    results_2_connections = randomv2_experiment.run_experiment(iterations=iterations, starting_stations="custom_list_without_replacement", 
                                                starting_station_list = stations_with_2_connections)
    randomv2_experiment.write_scores_to_csv(f"best_starting_stations/results/randomv2_2_connections_{iterations}")

    # With 3 connections
    results_3_connections = randomv2_experiment.run_experiment(iterations=iterations, starting_stations="custom_list_without_replacement", 
                                                starting_station_list = stations_with_3_connections)
    randomv2_experiment.write_scores_to_csv(f"best_starting_stations/results/randomv2_3_connections_{iterations}")


    # Calculate average scores
    print(f"Average score for stations with least connections: {np.mean(results_least_connections)}")
    print(f"Average score for stations with most connections: {np.mean(results_most_connections)}")
    print(f"Average score for stations with 2 connections: {np.mean(results_2_connections)}")
    print(f"Average score for stations with 3 connections: {np.mean(results_3_connections)}")