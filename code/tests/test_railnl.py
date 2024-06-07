from ..classes import railnl


def test_load_stations():
    # Create a Railnl object
    railnl = RailNL()

    # Print the stations dictionary directly
    print(railnl.stations)

test_load_stations()