from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route
from random import choice
from parent.code.algorithms.score import Score

class RandomAlgorithm(Algorithm):
    """Algorithm script finding 7 random routes. Each not exceeding 
    the 120 minute limit
    """

    def __init__(self, load: RailNL) -> None:
        super().__init__(load)

    def run(self) -> None:

        for _ in range(7):
            time_used = 0
            route = Route()

            # Find a random starting station
            stations = list(self.load.stations_dict().values())
            current_station = choice(stations)

            # Break when no connections are left in current station
            while current_station.has_connections():

                # Find random connection from current_station connections
                connections = list(current_station.connections_dict())
                connection = choice(connections)

                # Calculate new total duration of route
                duration = int(current_station.connection_duration(connection))
                total = time_used + duration

                # Continue if connection is possible considering time_used
                if total <= 120:
                    time_used = total
                    route.add(current_station, connection, duration)
                    current_station = connection

                # Else consider traject finished
                else:
                    break
            
<<<<<<< HEAD
            self.routes.append(route)

# Experiment
# runt N times, calculates score, and average score
times = 0
total_score = 0
N = 10000
while times < N:
    data = RailNL("Holland")
    random_algorithm = RandomAlgorithm(data)
    random_score = Score(random_algorithm).calculate()
    print(f"Score {times}: {random_score}")
    total_score += random_score
    times += 1

average_score = total_score / N
print(f"Random Algorithm Average Score: {average_score}")
=======
            self.routes.append(route)
>>>>>>> 80a0d114f9f94a9652a5e9639c0eeb7898bbc2c5
