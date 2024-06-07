from ..classes.railnl import RailNL as Railnl


def test_load_stations():
    # Create a Railnl object
    railnl = Railnl()

    # Print the stations dictionary directly
    print(railnl.stations)

test_load_stations()