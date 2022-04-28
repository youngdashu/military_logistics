from typing import List

from graph.division import Division
from graph.hub import Hub


class Province:

    def __init__(self, node_id, division: Division = None):
        self.node_id: int = node_id
        self.neighbours: List = []
        self.railway_level: int = 0
        self.terrain = 0
        self.hub: Hub = None
        self.division: Division = division

    def railway_level_to_capacity(self):
        return 0 if self.railway_level == 0 else 15 + ((self.railway_level - 1) * 5)

    # def add_neighbour(self, neighbour):
    #     self.neighbours.append(neighbour)

    def __repr__(self):
        return str(self.node_id) + " " + str(self.neighbours)
