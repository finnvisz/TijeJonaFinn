from code.classes.railnl import RailNL
from code.algorithms.algorithm import Algorithm
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.score import Score
from code.classes.station_class import Station


if __name__ == "__main__":
    data = RailNL("Holland")
    algorithm = RandomAlgorithm(data)
    algorithm.make_picture()
    score = Score(algorithm)
    print(score.calculate())
