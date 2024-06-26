from itertools import combinations

from parent.code.classes.station_class import Station
from parent.code.classes.railnl import RailNL

class Sort_Starting():
    """
    A class sorting all possible combinations of starting stations on the 
    sum of their connections.

    Attributes
    -------
    station_list: list of all stations in loaded map.
    bins: association between a sum of connections and a list of starting stations.

    Methods
    ----------
    fill_bins: iterates over all starting station combinations and places them in appropriate bin.
    """

    def __init__(self):
        railnl = RailNL("Holland")
        self.station_list = railnl.stations_dict().values()
        self.bins: dict[int, list[Station]] = {i: [] for i in range(8, 19)}
        
        self.fill_bins()

    def fill_bins(self):
        """
        Iterates over all starting station combinations and places them in appropriate bin.

        Post
        ----
        self.bins dictionary is filled with starting station combinations.
        """

        # For each non-repeating combination of 7 stations
        for combination in combinations(self.station_list, 5):

            # Calculate connectivity sum
            amount = 0
            for station in combination:
                amount += station.amount_connecting()

            # Place in correct connectivity degree bin
            self.bins[amount].append(list(combination))

    def give_connectivity_degree(self, degree: int):
        """
        Returns bin of input degree.
        """
        return self.bins[degree]
