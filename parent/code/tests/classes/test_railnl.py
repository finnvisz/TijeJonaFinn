from parent.code.classes.railnl import RailNL
from parent.code.classes.railnl import Station

railnl = RailNL("Holland")

# Check all stations present
def test_station_amount():
    assert len(railnl.stations_dict()) == 22

# Check all connections exist
def test_connections():
    assert len(railnl.get_total_connections()) == 28

# Check minimum number of connections correct
def test_min():
    assert railnl.min_connections() == 1

# Check maximum number of connections correct
def test_max():
    assert railnl.max_connections() == 4

# Check if random station is of type Station
def test_random():
    assert isinstance(railnl.get_random_station(), Station)