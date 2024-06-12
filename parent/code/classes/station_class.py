class Station:
    """Station class containing location and connections."""

    def __init__(self, name: str, lat: float, long: float):
        self.name = name    
        self.lat = lat  
        self.long = long
        self.connections: dict["Station", int] = {}

    def __repr__(self):
        """Return string representation of Station object."""
        return f"Station({self.name})"

    def add_connection(self, other: "Station", afstand: int) -> None:
        self.connections[other] = afstand

    def has_connection(self, connection: "Station") -> bool:
        return connection in self.connections

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
    
    def get_connections_sorted(self):
        """
        Get the connections of this station, sorted by duration 
        (shortest connection first).

        Pre: self has connections
        Post: return a list of tuples with the connected stations and their duration
        """
        # Put connections in list of tuples
        connections = list(self.connections.items())

        # Sort list by duration
        connections.sort(key=lambda x: x[1])

        # Return sorted list
        return connections
    
    def get_shortest_connection(self):
        """
        Return the connected station with the shortest connection.
        """
        # Use min function, but it uses values to compare instead of keys
        return min(self.connections, key=self.connections.get)
    
    def get_connection_time(self, station: "Station") -> int:
        """ Return the time it takes to travel to the given station."""
        # Check if station has this connection
        assert self.has_connection(station), f"Station {station.name} is not connected to {self.name}"
        
        # Return the time it takes to travel to the given station
        return self.connections.get(station)