#algoritm to make a random solution
from station import Station
from railnl import Railnl

# load in all the stations and connections
railnl = Railnl()
railnl.load_stations()
railnl.load_connections()

time_used = 0

while time_used < 120:
    railnl.stations[alkmaar]
