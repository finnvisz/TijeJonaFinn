from our_station import Station # type: ignore

class Load_in:
    """Class containing all stations and their connections."""

    def __init__(self) -> None:
        """Creates Railnl object, loads stations and connections into it."""
        self.stations: dict[str, "Station"] = {}
        self.connections = []
        self.load_stations("data/StationsHolland.csv")
        self.load_connections("data/ConnectiesHolland.csv")
    
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

                # Find station object corresponding to station string
                stat1_o = self.stations[stat1_s] 
                stat2_o = self.stations[stat2_s]

                # Use add_connection method on station objects
                stat1_o.add_connection(stat2_o, afstand)
                stat2_o.add_connection(stat1_o, afstand)

                # add the connections to this class
                self.connections.append((stat1_o, stat2_o))
                self.connections.append((stat2_o, stat1_o))

    def stations_dictionary(self) -> dict:
        return self.stations

    # Find the highest number of station connections
    def max_connections(self) -> int:
        stations = self.stations.keys()

        # Find amount of connections using amount_connecting method
        connections = lambda station: self.stations[station].amount_connecting()
        return max(connections(station) for station in stations)