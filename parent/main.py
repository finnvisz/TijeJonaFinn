from code.classes.railnl import RailNL
from code.algorithms.algorithm import Algorithm
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.greedy import Greedy
from code.algorithms.finnsroutes import Finn
from code.algorithms.score import Score
from code.classes.station_class import Station


if __name__ == "__main__":
    data = RailNL("Holland")

    # Test Greedy Algorithm
    greedy_algorithm = Greedy(data)
    greedy_score = Score(greedy_algorithm)
    greedy_algorithm.make_picture() # after score so a second run doesnt affect the score
    print(f"Greedy Algorithm Score: {greedy_score.calculate()}")





