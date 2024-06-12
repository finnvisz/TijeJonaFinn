from code.classes.railnl import RailNL
from code.algorithms.algorithm import Algorithm
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.greedy import Greedy
from code.algorithms.finnsroutes import Finn
from code.algorithms.score import Score
from code.classes.station_class import Station


if __name__ == "__main__":
    data = RailNL("Holland")
    
    # Test Finns routes
    finn = Finn(data)
    finn_score = Score(finn)
    finn.make_picture()
    print(f"Finn Score: {finn_score.calculate()}")

    # Test Random Algorithm
    random_algorithm = RandomAlgorithm(data)
    random_score = Score(random_algorithm)
    random_algorithm.make_picture() # after score so a second run doesnt affect the score
    print(f"Random Algorithm Score: {random_score.calculate()}")

    # Test Greedy Algorithm
    greedy_algorithm = Greedy(data)
    greedy_score = Score(greedy_algorithm)
    greedy_algorithm.make_picture()
    print(f"Greedy Algorithm Score: {greedy_score.calculate()}")

    



