class Station:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.connections: dict["Station", int] = {}

    def add_connection(self, other: "Station", afstand: int) -> None:
        self.connections[other] = afstand

    def number_of_connections(self) -> int:
        return len(self.connections)

