from itertools import combinations

from parent.code.classes.station_class import Station
from parent.code.classes.railnl import RailNL

class Sort_Starting():

    def __init__(self):
        railnl = RailNL("Holland")
        self.station_list = railnl.stations_dict().values()
        self.bins = [[] for _ in range(12, 25)]
        
        self.fill_bins()

    def fill_bins(self):

        for combination in combinations(self.station_list, 2):

            amount = 0
            for station in combination:
                amount += station.amount_connecting()
            
            print(amount)
            print(combination)

            self.bins[amount].append(combination)

Sort_Starting()
