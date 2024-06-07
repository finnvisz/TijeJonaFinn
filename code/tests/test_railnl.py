"""File in root dir because of import difficulties"""
# TODO: Allow relative imports to put tests in pytest folder
# import os

# current = os.pwd()
# previous = ...
# previous/data/station.csv

from load import Load_in as Railnl


def test_load_stations():
    # Create a Railnl object
    railnl = Railnl()

    # Print the stations dictionary directly
    print(railnl.stations)

test_load_stations()