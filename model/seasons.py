from dataclasses import dataclass

@dataclass
class Season:
    year: int
    url: str

    def __hash__(self):
        return self.year

    def __eq__(self, other):
        return self.year == other.year
