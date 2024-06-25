from parent.code.classes.station_class import Station
from typing import Tuple

class Route:
    """Object class of train routes between stations."""

    def __init__(self) -> None:
        """
        Initialize a Route object.
        
        - Post: A Route object is created with empty connections, 
          stations list, and zero time.
        """
        self.connections_used: list[Tuple[str, str, int]] = []
        self.stations: list[Station] = []
        self.time = 0

    def __repr__(self) -> str:
        """
        Return a string representation of the Route object.
        
        - Post: Returns a string showing the connections used in the route.
        """
        return f"Route({self.connections_used})"

    def add_connection(self, station1: "Station", station2: "Station", duration: int) -> None:
        """
        Add a connection between two stations to the route.
        
        - Pre: station1 and station2 are valid Station objects, and duration 
          is a positive integer representing the travel time.
        - Post: The connection is added to the route, updating the stations list 
          and total travel time.
        """
        self.connections_used.append((station1.name, station2.name, duration))
        # Add station1 only if it's the first station or not already in the list
        if not self.stations or self.stations[-1] != station1:
            self.stations.append(station1)
        # Add station2 to ensure it's appended after station1
        self.stations.append(station2)
        self.time += duration

    def remove_connection(self, connection: tuple[str, str, int]) -> None:
        """
        Remove a connection from the route.
        
        - Pre: connection is a tuple of two station names and the duration 
          of the connection.
        - Post: If the connection exists, it is removed from the route, 
          and the total travel time is updated. Otherwise, raises ValueError.
        """
        if connection in self.connections_used:
            self.connections_used.remove(connection)
            self.time -= int(connection[2])
        else:
            raise ValueError("The specified connection does not exist in the route.")
        
    def get_stations(self) -> list:
        """
        Return the list of stations in the route.
        
        - Post: Returns a list of Station objects in the route.
        """
        return self.stations

    def get_connections_used(self) -> list:
        """
        Return the list of connections used in the route.
        
        - Post: Returns a list of tuples representing the connections 
          used in the route with each tuple containing the station 
          names and the duration.
        """
        return self.connections_used
    
    def time(self) -> int:
        """
        Return the total travel time of the route.
        
        - Post: Returns an integer representing the total travel time.
        """
        return self.time
    
    def is_connection_used(self, station1: "Station", station2: "Station") -> bool:
        """
        Check if a connection between station1 and station2 is already 
        used in this route. Order of station1 and station2 does not 
        matter(!), as the connection is bidirectional.
        """
        for connection in self.connections_used:
            if station1.name in connection and station2.name in connection:
                return True
        return False
    
    def stations_string(self) -> str:
        """
        Return a string of station names in the route.
        
        - Post: Returns a string with the names of the stations in the route, 
          ordered as they appear. (used to write the csv files)
        """
        station_names = []

        # Vraag van elk station de naam op
        for station in self.stations:
            station_names.append(station.station_name())

        station_names = f"{station_names}"

        string = station_names.replace("'", "")

        return string
