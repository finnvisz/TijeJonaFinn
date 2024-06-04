from station import Station

class Railnl:
    def __init__(self) -> None:
        self.stations: dict[str, "Station"] = {}
    
    def load_stations(self) -> None:
        with open("data/StationsHolland.csv") as f:
                    for line in f:
                        if line == "\n":
                            break
                        name, x, y = line.strip().split(',')
                        station = Station(name, x, y)
                        self.stations[name] = station

    def load_connections(self) -> None:
        with open("data/ConnectiesHolland.csv") as f:
                    for line in f:
                        if line == "\n":
                            break
                        station1, station2, afstand = line.strip().split(',')
                        station1.add_connection(station2, afstand)

    # Git commit oefen
