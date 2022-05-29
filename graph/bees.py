import random
from typing import List

from graph.ProvinceGraph import ProvinceGraph


class Bees:
    # default ratio of bees to graph vertices (provinces) is set to 0.3
    def __init__(self, graph: ProvinceGraph, bees_ratio: float = .3):
        self.graph = graph
        self.bees_ratio = bees_ratio
        self.bees_number = round(self.graph.provinces_number * self.bees_ratio)

    def place_initial_bees(self) -> List[int]:
        print("provinces no.:", len(self.graph.graph))
        print("bees no.:", self.bees_number)
        chosen_provinces = random.sample([province.node_id for province in self.graph.graph], self.bees_number)
        print(chosen_provinces)
        return chosen_provinces

    def solve(self):
        pass
