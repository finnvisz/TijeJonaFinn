from railnl import RailNL
from algorithms.algorithm import Algorithm
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.score import Score
from station_ import Station


if __name__ == "__main__":
    data = RailNL("Holland")
    algorithm = RandomAlgorithm(data)
    algorithm.make_picture()
    score = Score(algorithm)
    print(score.calculate())
