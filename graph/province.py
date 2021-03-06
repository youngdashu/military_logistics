from typing import List, Tuple

from graph.division import Division
from graph.hub import Hub


class Province(object):

    def __init__(self, node_id, division: Division = None):
        self.node_id: int = node_id
        self.neighbours: List[int] = []
        self.railway_level: int = 0
        # railwayline:parent (int:int)
        self.railway_parent = dict()
        self.terrain = 0
        self.hub: Hub = None
        self.division: Division = division
        self.parent = None
        self.levelCosts = [5,10,15,20,25]

    def railway_level_to_capacity(self):
        return 0 if self.railway_level == 0 else 15 + ((self.railway_level - 1) * 5)

    def __repr__(self) -> str:
        return str(self.node_id) + " " + str(self.neighbours)

    def __lt__(self, other):
        return self.terrain < other.terrain

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

    def set_hub(self, level, required_supplies):
        self.hub = Hub(level, required_supplies)

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        return self.node_id == other.node_id

    def upgrade_railway(self, new_supplies_going_through_province: float):
        self.railway_level += 1
        while self.railway_level_to_capacity() < new_supplies_going_through_province and self.railway_level < 5:
            self.railway_level += 1

    def get_railway_build_cost(self,level=1):
        if level<= self.railway_level:
            return 0
        return self.terrain+self.levelCosts[(level-self.railway_level)]

