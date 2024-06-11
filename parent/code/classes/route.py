from parent.code.classes.station_class import Station

class Route:
    """Object class of train routes between stations."""

    def __init__(self) -> None:
        self.connections_used: list = []
        self.time = 0

    def connections(self):
        return self.connections_used

    def add(self, station1: "Station", station2: "Station", duur: int) -> None:
        self.connections_used.append([station1.name, station2.name, duur])
        self.time += int(duur)

    def get_connections_used(self) -> list:
        return self.connections_used
    
    def time(self) -> int:
        return self.time