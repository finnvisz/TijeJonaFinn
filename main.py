from code.load import Load_in
from code.algorithm import Algorithm
from code.random_algorithm import RandomAlgorithm
from code.score import Score


if __name__ == "__main__":
    data = Load_in("Holland")
    algorithm = Algorithm()
    random_alg = RandomAlgorithm()