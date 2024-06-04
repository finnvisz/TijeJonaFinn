class Traject:
    def __init__(self) -> None:
        self.connections_used: list = []
        self.time = 0

    def add_connection(self, station1: "Station", station2: "Station", duur: int) -> None:
