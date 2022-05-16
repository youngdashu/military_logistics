from json import JSONEncoder
from typing import List, Tuple, Union

from graph.division import Division
from graph.hub import Hub

import json_fix

class Province(object):

    def __init__(self, node_id, division: Division = None):
        self.node_id: int = node_id
        self.neighbours: List[int] = []
        self.railway_level: int = 0
        self.terrain = 0
        self.hub: Hub = None
        self.division: Division = division

    # def __hash__(self):
    #     return hash((self.node_id, tuple(self.neighbours)))



    def __json__(self):
        d = self.__dict__
        if d["hub"] is None:
            d["hub"] = "None"
        if d["division"] is None:
            d["division"] = "None"
        return str(d)

    def railway_level_to_capacity(self):
        return 0 if self.railway_level == 0 else 15 + ((self.railway_level - 1) * 5)

    # def add_neighbour(self, neighbour):
    #     self.neighbours.append(neighbour)

    def __repr__(self) -> str:
        return str(self.node_id) + " " + str(self.neighbours)

    def required_supplies(self) -> float:
        return 0.0 if self.division is None else self.division.required_supplies

    def set_required_supplies(self, supplies) -> float:
        diff = 0.0
        if self.division is not None:
            diff = (self.division.required_supplies - supplies)
            self.division.required_supplies = supplies
        return diff

    def change_to_tuple(self) -> Tuple[int]:
        return tuple(self.neighbours)

    def number_of_divisions_in_province(self):
        return int(bool(self.division))

    def set_hub(self, level):
        self.hub = Hub(level)
