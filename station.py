class Station:
    """Station class containing location and connections."""

    def __init__(self, name: str, lat: float, long: float):
        self.name = name    
        self.lat = lat  
        self.long = long  
        self.connections: dict["Station", int] = {}

    def add_connection(self, other: "Station", afstand: int) -> None:
        self.connections[other] = afstand

    def number_of_connections(self) -> int:
        return len(self.connections)
    
    def location(self) -> tuple:
        return (self.lat, self.long)