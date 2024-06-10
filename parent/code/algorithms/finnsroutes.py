from parent.code.algorithms.algorithm import Algorithm
from parent.code.classes.railnl import RailNL
from parent.code.classes.route import Route


class Finn(Algorithm):
    def __init__(self, load: RailNL) -> None:
        super().__init__(load)

    def run(self) -> None:
        route1 = Route()
        lijst_route1 = ['Den Helder', 'Alkmaar', 'Castricum', 'Beverwijk', 'Haarlem', 'Heemstede-Aerdenhout', 'Leiden Centraal']
        for i in range(len(lijst_route1) - 1):
            station1 = self.load.stations[lijst_route1[i]]
            station2 = self.load.stations[lijst_route1[i + 1]]
            route1.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route1)

        route2 = Route()
        lijst_route2 = ['Castricum', 'Zaandam', 'Beverwijk']
        for i in range(len(lijst_route2) - 1):
            station1 = self.load.stations[lijst_route2[i]]
            station2 = self.load.stations[lijst_route2[i + 1]]
            route2.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route2)

        route3 = Route()
        lijst_route3 = ['Alkmaar', 'Hoorn', 'Zaandam', 'Amsterdam Sloterdijk', 'Amsterdam Zuid', 'Amsterdam Amstel']
        for i in range(len(lijst_route3) - 1):
            station1 = self.load.stations[lijst_route3[i]]
            station2 = self.load.stations[lijst_route3[i + 1]]
            route3.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route3)

        route4 = Route()
        lijst_route4 = ['Haarlem', 'Amsterdam Sloterdijk', 'Amsterdam Centraal', 'Amsterdam Amstel']
        for i in range(len(lijst_route4) - 1):
            station1 = self.load.stations[lijst_route4[i]]
            station2 = self.load.stations[lijst_route4[i + 1]]
            route4.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route4)

        route5 = Route()
        lijst_route5 = ['Amsterdam Zuid', 'Schiphol Airport', 'Leiden Centraal', 'Alphen a/d Rijn', 'Gouda']
        for i in range(len(lijst_route5) - 1):
            station1 = self.load.stations[lijst_route5[i]]
            station2 = self.load.stations[lijst_route5[i + 1]]
            route5.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route5)

        route6 = Route()
        lijst_route6 = ['Leiden Centraal', 'Den Haag Centraal', 'Gouda', 'Rotterdam Alexander', 'Rotterdam Centraal']
        for i in range(len(lijst_route6) - 1):
            station1 = self.load.stations[lijst_route6[i]]
            station2 = self.load.stations[lijst_route6[i + 1]]
            route6.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route6)

        route7 = Route()
        lijst_route7 = ['Den Haag Centraal', 'Delft', 'Schiedam Centrum', 'Rotterdam Centraal', 'Dordrecht']
        for i in range(len(lijst_route7) - 1):
            station1 = self.load.stations[lijst_route7[i]]
            station2 = self.load.stations[lijst_route7[i + 1]]
            route7.add(station1, station2, station1.connection_duration(station2))
        self.routes.append(route7)