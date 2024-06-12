# Library imports
import random

# Local imports
from os.path import abspath, join, dirname
from parent.code.classes.station_class import Station

parent_path = abspath(join(dirname(__file__), '../..'))

class RailNL:
    """Class containing all stations and their connections."""

    def __init__(self, maprange: str) -> None:
        """Creates Railnl object, loads stations and connections into it."""
        self.stations: dict[str, "Station"] = {}
        self.connections = set()
        self.load_stations(f"{parent_path}/data/Stations{maprange}.csv")
        self.load_connections(f"{parent_path}/data/Connecties{maprange}.csv")
    
    def load_stations(self, filepath: str) -> None:
        """Load stations from data file into self.stations.
        
        - Pre: filepath is a valid path to a CSV file containing station data.
        CSV file is formatted as follows:
        `StationName,latitude,longitude`
        
        - Post: self.stations contains all stations from the file.
        """
        # Open file
        with open(filepath) as file:
            # and read lines until EOF
            while (line := file.readline()) != "":
                # Create station object from extracted triple
                name, lat, long = line.strip().split(',')
                station = Station(name, float(lat), float(long))
                # And add to internal dictionary
                self.stations[name] = station

    # Add connections to Station objects in self.stations
    def load_connections(self, filepath: str) -> None:
        """Load connections from data file into the stations of self.stations.
        
        - Pre: filepath is a valid path to a CSV file containing connection data.
        CSV file is formatted as follows:
        `StationName1,StationName2,afstand`
        
        - Post: station objects in self.stations contain their connections.
        """
        # Open file
        with open(filepath) as file:
            # and read lines until EOF
            while (line := file.readline()) != "":      
                # Read station names as strings
                stat1_s, stat2_s, afstand = line.strip().split(',')
                
                # Sort station names alphabetically
                stations_as_string_alfabetical = sorted([stat1_s, stat2_s])

                # Find station object corresponding to station string
                stat1_o = self.stations[stations_as_string_alfabetical[0]] 
                stat2_o = self.stations[stations_as_string_alfabetical[1]]

                # Use add_connection method on station objects
                stat1_o.add_connection(stat2_o, int(afstand))
                stat2_o.add_connection(stat1_o, int(afstand))

                # add the connections to this class
                self.connections.add((stat1_o, stat2_o))

    def stations_dict(self) -> dict:
        return self.stations

    # Find the highest number of station connections
    def max_connections(self) -> int:
        stations = self.stations.keys()

        # Find amount of connections using amount_connecting method
        connections = lambda station: self.stations[station].amount_connecting()
        return max(connections(station) for station in stations)
    
    def get_random_station(self) -> "Station":
        """Return a random station from self.stations."""
        return random.choice(list(self.stations.values()))