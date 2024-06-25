class Station:
    """Station class containing location and connections."""

    def __init__(self, name: str, lat: float, long: float):
        self.name = name    
        self.lat = lat  
        self.long = long
        self.connections: dict["Station", int] = {}

    def __repr__(self):
        """
        Return string representation of Station object.
        """
        return f"Station({self.name})"

    def add_connection(self, other: "Station", duration: int) -> None:
        """
        Add a connection to another station.
        
        - Pre: other is a valid Station object, and duration is a positive integer.
        - Post: The connection is added to the connections 
                dictionary of this station.
        """
        self.connections[other] = duration

    def has_connection(self, station: "Station") -> bool:
        """
        Check if this station is connected to another station. Return 
        true or false.
        """
        return station in self.connections

    def amount_connecting(self) -> int:
        """
        Return the number of connections this station has.
        """
        return len(self.connections)
    
    def location(self) -> tuple:
        """
        Return the location of the station.
        
        - Post: Returns a tuple containing the latitude and longitude of 
                the station.
        """
        return (self.lat, self.long)
    
    def connections_dict(self):
        """
        Return the connections dictionary of the station.
        
        - Post: Returns a dictionary with connected stations as keys and 
                durations as values.
        """
        return self.connections
    
    def connection_duration(self, other: "Station") -> int:
        """
        Return the duration of the connection to another station.
        """
        return self.connections[other]
    
    def station_name(self) -> str:
        return self.name
    
    # Check if station has connections
    def has_connections(self):
        """
        Check if this station has any connections. Return 
        true or false.
        """
        if len(self.connections) > 0:
            return True
        return False
    
    def get_connections(self):
        """
        Get the connections of this station, sorted as they were read from the CSV file.

        - Pre: self has connections
        - Post: return a list of tuples with the connected stations and their duration
        """
        # Put connections in list of tuples
        connections = list(self.connections.items())

        # Return list
        return connections
    
    def get_connections_sorted(self):
        """
        NOTE: Legacy function. Only used by old greedy.py.
        
        Get the connections of this station, sorted by duration 
        (shortest connection first).

        - Pre: self has connections
        - Post: return a list of tuples with the connected stations and 
                their duration
        """
        # Put connections in list of tuples
        connections = list(self.connections.items())

        # Sort connections by duration
        connections.sort(key=lambda x: x[1])

        # Return list
        return connections
    
    def get_shortest_connection(self):
        """
        Returns a Station object representing the connected station with the 
        shortest connection.
        """
        # Use min function, but it uses values to compare instead of keys
        return min(self.connections, key=self.connections.get)
    
    def get_connection_time(self, station: "Station") -> int:
        """ 
        Return the time it takes to travel to the given station.
        """
        # Check if station has this connection
        assert self.has_connection(station), f"Station {station.name} is not connected to {self.name}"
        
        # Return the time it takes to travel to the given station
        return self.connections.get(station)