import json_fix


class Division:
    def __init__(self, required_supplies):
        self.required_supplies = required_supplies

    def __json__(self):
        return self.__dict__

    # def __repr__(self):
    #     return "{" + "\'required_supplies\': " + str(self.required_supplies) + "}"