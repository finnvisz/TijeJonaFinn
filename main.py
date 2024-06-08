from code.classes.railnl import RailNL
from code.algorithms.algorithm import Algorithm
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.greedy import Greedy
from code.algorithms.score import Score
from code.classes.station_class import Station


if __name__ == "__main__":
    data = RailNL("Holland")
    
    # Test Random Algorithm
    random_algorithm = RandomAlgorithm(data)
    random_algorithm.make_picture()
    random_score = Score(random_algorithm)
    print(f"Random Algorithm Score: {random_score.calculate()}")

    # Test Greedy Algorithm
    greedy_algorithm = Greedy(data)