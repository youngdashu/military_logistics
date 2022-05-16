import json_fix

class Hub:

    max_capacity = 20.0
    hub_range = 3
    base_cost = 200.0

    def __init__(self, level=1):
        self.level = level

    def __json__(self):
        return self.__dict__

    def __level_to_factor(self):
        if self.level == 1:
            return 1
        elif self.level == 2:
            return 1.1
        elif self.level == 3:
            return 1.2

    def level_to_supplies(self, distance_from_province):
        res = None
        if distance_from_province == 0:
            return 20
        elif distance_from_province == 1:
            res = 15
        elif distance_from_province == 2:
            res = 10
        elif distance_from_province == 3:
            res = 5
        return res * self.__level_to_factor()

    def cost(self):
        return self.base_cost * self.__level_to_factor()
