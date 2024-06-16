# Imports
from parent.code.classes.railnl import RailNL
from parent.code.algorithms.random_v2 import Randomv2


# Initialize algorithm
randomv2 = Randomv2(RailNL("Holland"))


# Create collection with various subgroups of stations:
Stations = randomv2.load.stations_dict()

# 1. Stations with most connections
stations_with_most_connections = []

max_connections = randomv2.load.max_connections()

for station in Stations.values():
    if station.amount_connecting() == max_connections:
        stations_with_most_connections.append(station)

# 2. Stations with least connections
stations_with_least_connections = []

min_connections = randomv2.load.min_connections()

for station in Stations.values():
    if station.amount_connecting() == min_connections:
        stations_with_least_connections.append(station)
    

# Run algorithm with different starting stations
output = randomv2.run(starting_stations="custom_list_with_replacement", starting_station_list = stations_with_least_connections)


# Print results + extra info
for route in output:
    for connection in route.get_connections_used():
        print(connection[0], " - ", connection[1], connection[2], end=" -> ")
    
    print("")
    print(f"Total time: {route.time}")
    print("")

print(f"Unused stations: {len(randomv2.unused_stations)}")
print(f"Unused connections: {len(randomv2.unused_connections)}")