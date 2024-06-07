from ..classes.railnl import RailNL

def test_load_stations():
    # Create a Railnl object
    railnl = RailNL()

    # Print the stations dictionary directly
    print(railnl.stations)