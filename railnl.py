from our_station import Station # type: ignore

class Railnl:

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

                        # Use our_station add_connection method on extracted
                        station1, station2, afstand = line.strip().split(',')
                        station1 = self.stations[station1]
                        station2 = self.stations[station2]
                        station1.add_connection(station2, afstand)
                        station1.add_connection(station2, afstand)

    def stations_dictionary(self) -> dict:
         return self.stations

    # Find the highest number of station connections
    def max_connections(self) -> int:
        connections = lambda station: self.stations[station].number_of_connections()
        return max(connections(station) for station in self.stations.keys())
          

    