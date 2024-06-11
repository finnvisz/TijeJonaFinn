from ..classes.railnl import RailNL

def test_load_stations_Holland():
    # Create a Railnl object
    railnl = RailNL("Holland")

    # Print the stations dictionary directly
    print(railnl.stations)