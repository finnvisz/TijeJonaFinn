from itertools import combinations

from parent.code.classes.station_class import Station
from parent.code.classes.railnl import RailNL

class Sort_Starting():

    def __init__(self):
        railnl = RailNL("Holland")
        self.station_list = railnl.stations_dict().values()
        self.bins: dict[int, list[Station]] = {i: [] for i in range(12, 25)}
        
        self.fill_bins()
        print(self.bins)

    def fill_bins(self):

        # For each non-repeating combination of 7 stations
        for combination in combinations(self.station_list, 7):

            # Calculate connectivity sum
            amount = 0
            for station in combination:
                amount += station.amount_connecting()

            # Place in correct connectivity degree bin
            self.bins[amount].append(list(combination))

    def give_connectivity_bin_dict(self):
        return self.bins