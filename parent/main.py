import random
import copy
import matplotlib.pyplot as plt
import numpy as np

from code.classes.railnl import RailNL
from code.algorithms.algorithm import Algorithm
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.score import Score
from parent.code.experiments.experiments import Experiment

if __name__ == "__main__":
    data = RailNL("Holland") # manipulate

    # Test Random Algorithm
    random_algorithm = RandomAlgorithm(data)
    random_score = Score(random_algorithm)
    #random_algorithm.make_picture()
    print(random_algorithm.output())
    print(f"Random Algorithm Score: {random_score.calculate()}")

    # Perform experiment with RandomAlgorithm and collect scores
    random_experiment = Experiment(RandomAlgorithm, "Holland")
    scores = random_experiment.run_experiment(100000)
    average = random_experiment.average_score()
    print(f"average score: {average}")


    # Plotting the frequency distribution of scores
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=50, edgecolor='black', alpha=0.7)
    plt.title('Frequency Distribution of Scores RandomAlgorithm 7 routes')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("freq.png")

    # Plotting frequency distributions of connections used
    total_connections = RailNL("Holland").get_total_connections()
    connection_labels = [f"{c[0].name} - {c[1].name}" for c in total_connections]
    
    plt.figure(figsize=(10, 10))
    plt.bar(range(len(total_connections)), random_experiment.count_connections_used, tick_label=connection_labels)
    plt.xticks(rotation=90)
    plt.title('Frequency Distribution of Connections Used in Random Algorithm')
    plt.xlabel('Connection')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("freq2.png")

    # Plotting frequency distribution of stations used
    total_stations = list(RailNL("Holland").stations_dict().values())
    station_labels = [station.name for station in total_stations]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(total_stations)), random_experiment.count_stations_used, tick_label=station_labels)
    plt.xticks(rotation=90)
    plt.title('Frequency Distribution of Stations Used in Random Algorithm')
    plt.xlabel('Station')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("freq3.png")

    # # Test Greedy Algorithm
    # greedy_alg = Greedy(data)
    # greedy_score = Score(greedy_alg).calculate()
    # greedy_alg.make_picture()
    # print(f"Greedy algorithm score: {greedy_score}")

    # greedy_experiment = Experiment(Greedy, "Holland", iterations=100)
    # print(f"Greedy Average Score: {greedy_experiment.average_score()}")
    # print(f"greedy scores: {greedy_experiment.get_scores()} ")

    # # Test Hillclimber algorithm
    # hillclimber_alg = Hillclimber(data, RandomAlgorithm(data))
    # hillclimber_alg.make_picture()

    



