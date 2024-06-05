from our_station import Station # type: ignore

class Railnl:
    """Class loading stations and connections into station objects."""

    def __init__(self) -> None:
        self.stations: dict[str, "Station"] = {}
        self.load_stations()
        self.load_connections()
    
    # Create and append Station objects to self.stations dictionary
    def load_stations(self) -> None:
        with open("data/StationsHolland.csv") as file:
                    for line in file:
                        if line == "\n":
                            break
                        
                        # Create station object from extracted triple
                        name, lat, long = line.strip().split(',')
                        station = Station(name, float(lat), float(long))
                        self.stations[name] = station

    # Add connections to Station objects in self.stations
    def load_connections(self) -> None:
        with open("data/ConnectiesHolland.csv") as f:
                    for line in f:
                        if line == "\n":
                            break
                        
                        # Read station names as strings
                        stat1_s, stat2_s, afstand = line.strip().split(',')

                        # Find station object corresponding to station string
                        stat1_o = self.stations[stat1_s] 
                        stat2_o = self.stations[stat2_s]

                        # Use add_connection method on extracted
                        stat1_o.add_connection(stat2_o, afstand)
                        stat2_o.add_connection(stat1_o, afstand)

    def stations_dictionary(self) -> dict:
         return self.stations

    # Find the highest number of station connections
    def max_connections(self) -> int:
        stations = self.stations.keys()

        # Find amount of connections using amount_connecting method
        connections = lambda station: self.stations[station].amount_connecting()
        return max(connections(station) for station in stations)