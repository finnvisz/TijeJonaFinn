from load import Load_in
from algorithm import Algorithm
from random_algorithm import RandomAlgorithm
from score import Score
from our_station import Station


if __name__ == "__main__":
    data = Load_in("Holland")
    algorithm = RandomAlgorithm(data)
    algorithm.make_picture()
    score = Score(algorithm)
    print(score.calculate())
