class Station:
    """Station class containing location and connections."""

    def __init__(self, name: str, lat: float, long: float):
        self.name = name    
        self.lat = lat  
        self.long = long
        self.connections: dict["Station", int] = {}

    def __repr__(self):
        """Return string representation of Station object."""
        return f"Station(name={self.name}, lat={self.lat}, long={self.long})"

    def add_connection(self, other: "Station", afstand: int) -> None:
        self.connections[other] = afstand

    def amount_connecting(self) -> int:
        return len(self.connections)
    
    def location(self) -> tuple:
        return (self.lat, self.long)
    
    def connections_dict(self):
        return self.connections
    
    def connection_duration(self, other: "Station") -> int:
        return self.connections[other]
    
    def station_name(self):
        return self.name
    
    # Check if station has connections
    def has_connections(self):
        if len(self.connections) > 0:
            return True
        return False