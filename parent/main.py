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
    random_algorithm.make_picture()
    print(random_algorithm.output())
    print(f"Random Algorithm Score: {random_score.calculate()}")

    # Perform experiment with RandomAlgorithm and collect scores
    random_experiment = Experiment(RandomAlgorithm, "Holland")
    scores = random_experiment.run_experiment()
    average = random_experiment.average_score()
    print(f"average score: {average}")


    # Plotting the frequency distribution of scores
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=50, edgecolor='black', alpha=0.7)
    plt.title('Frequency Distribution of Scores RandomAlgorithm N routes (0-7)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("freq.png")

    # Plotting frequency distributions of connections used
    plt.figure(figsize=(10, 6))
    plt.hist(connections, bins=50, edgecolor='black', alpha=0.7)
    plt.title('Frequency Distribution of connections Random Algorithm')
    plt.xlabel('Connection')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("freq2.png")


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

    



