from code.classes.railnl import RailNL
from code.algorithms.algorithm import Algorithm
from code.algorithms.greedy import Greedy
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.greedy import Greedy
from code.algorithms.finnsroutes import Finn
from code.algorithms.score import Score
from code.classes.station_class import Station
from code.experiments.experiments import Experiment


if __name__ == "__main__":
    data = RailNL("Holland")
    
    # # Test Finns routes
    # finn = Finn(data)
    # finn_score = Score(finn)
    # finn.make_picture()
    # print(f"Finn Score: {finn_score.calculate()}")

    # # Test Random Algorithm
    # random_algorithm = RandomAlgorithm(data)
    # random_score = Score(random_algorithm)
    # random_algorithm.make_picture() # after score so a second run doesnt affect the score
    # print(f"Random Algorithm Score: {random_score.calculate()}")

    # Test Greedy Algorithm
    greedy_alg = Greedy(data)
    greedy_score = Score(greedy_alg).calculate()
    greedy_alg.make_picture()
    print(f"Greedy algorithm score: {greedy_score}")

    greedy_experiment = Experiment(Greedy, "Holland", iterations=100)
    print(f"Greedy Average Score: {greedy_experiment.average_score()}")
    print(f"greedy scores: {greedy_experiment.get_scores()} ")

    # test best_starting_station
    greedy_alg2 = Greedy(data).best_starting_station()
    greedy2_score = Score(greedy_alg2).calculate()
    print(f"Greedy best starting station score: {greedy2_score}")


    



