class Hub:

    max_capacity = 20.0
    hub_range = 3

    def __init__(self, level=1):
        self.level = level

    def level_to_factor(self):
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
        return res * self.level_to_factor()
