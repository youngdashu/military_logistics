class Province:

    def __init__(self, id, neighbours):
        self.id = id
        self.neighbours = neighbours
        self.railway_level = 0
        self.terrain = 0
        self.hub = None
        self.division = None

    def railway_level_to_capacity(self):
        return 0 if self.railway_level == 0 else 15 + ((self.railway_level - 1) * 5)
