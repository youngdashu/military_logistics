from scipy.interpolate import interp2d
import numpy as np

from graph.hub import Hub


class CostFunction:
    ratios = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    results = [[0]]

    def __init__(self, cluster_size: int):

        minV = Hub(1).cost()
        maxV = Hub(3).cost() * cluster_size
        diff = (maxV - minV)/10.0

        costs = [minV]
        for i in range(1, 10):
            costs.append(costs[i-1] + diff)
        costs.append(maxV)
        self.costs = costs



    def __call__(self, ratio: float, hubs_cost: float, alfa: float = 0.1):
        print(self.ratios)
        exit(0)
