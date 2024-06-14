from parent.code.classes.station_class import Station

class Route:
    """Object class of train routes between stations."""

    def __init__(self) -> None:
        self.connections_used: list = []
        self.stations: list = []
        self.time = 0

    def __repr__(self) -> str:
        return f"Route({self.connections_used})"
    
    def connections(self):
        return self.connections_used

    def add_connection(self, station1: "Station", station2: "Station", duur: int) -> None:
        self.connections_used.append([station1.name, station2.name, duur])
        if self.stations:
            if self.stations[-1] != station1:
                self.stations.append(station1)
        self.stations.append(station2)
        self.time += int(duur)

    def remove_connection(self, connection: tuple[str, str, int]) -> None:
        if connection in self.connections_used:
            self.connections_used.remove(connection)
            self.time -= int(connection[2])
        else:
            raise ValueError("The specified connection does not exist in the route.")
        
    def get_stations(self) -> list:
        return self.stations

    def get_connections_used(self) -> list:
        return self.connections_used
    
    def time(self) -> int:
        return self.time
    
    def is_connection_used(self, station1: "Station", station2: "Station") -> bool:
        """
        Check if a connection between station1 and station2 is already used in this route.
        """
        for connection in self.connections_used:
            if station1.name in connection and station2.name in connection:
                return True
        return False