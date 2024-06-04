#algoritm to make a random solution
from station import Station
from railnl import Railnl
from traject import Traject
import random

# load in all the stations and connections
railnl = Railnl()
railnl.load_stations()
railnl.load_connections()

time_used = 0
current_location = 'alkmaar'
traject = Traject()

while time_used < 120:
    # kies random verbinding uit de connections die je hebt
    connection = random.choice(railnl.stations[current_location].connections.keys())
    # tel de duur van die verbinding op bij time_used
    time_used += railnl.stations[current_location].connection[connection]
