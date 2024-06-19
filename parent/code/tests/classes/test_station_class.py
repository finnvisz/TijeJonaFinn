from parent.code.classes.railnl import RailNL
from parent.code.classes.railnl import Station

railnl = RailNL("Holland")
station = railnl.get_random_station()

# Check station has connections
def test_has_connections():
    assert station.amount_connecting() > 0
