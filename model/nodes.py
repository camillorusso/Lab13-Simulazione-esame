from dataclasses import dataclass

@dataclass
class Node:
    driverId: int
    forename: str
    surname: str

    def __hash__(self):
        return self.driverId

    def __eq__(self, other):
        return self.driverId == other.driverId
