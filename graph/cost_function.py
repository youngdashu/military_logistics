from functools import cache
from math import ceil

from scipy.interpolate import interp2d
import numpy as np

from graph.hub import Hub

import matplotlib.pyplot as plt


class CostFunction:
    ratios = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    def __init__(self):
        pass

    def __plot_3d(self, f):
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        x = np.linspace(self.costs[0], self.costs[-1], 1000)
        y = np.linspace(self.ratios[0], self.ratios[-1], 1000)

        Z = f(x, y)

        ax.contour3D(x, y, Z, 50, cmap='binary')
        ax.set_xlabel('costs')
        ax.set_ylabel('ratios')
        ax.set_zlabel('values')

        ax.view_init(10, -30)

        fig.show()
        exit(0)

    @cache
    def __call__(self, cluster_size: int, alfa: float = 0.1):

        minV = Hub(1).cost()
        maxV = Hub(3).cost() * cluster_size
        diff = (maxV - minV) / 10.0

        costs = [minV]
        for i in range(1, 10):
            costs.append(costs[i - 1] + diff)
        costs.append(maxV)
        self.costs = costs
        self.results = [[0 for _ in range(len(self.costs))] for _ in range(len(self.ratios))]

        step_i = 0.1 / (len(self.ratios) * alfa)
        for i in range(0, int(len(self.ratios) * alfa)):
            step_j = 0.1 / (len(self.costs) // 2)

            for j in range(0, int(ceil(len(self.costs) / 2))):
                self.results[i][j] = (i * step_i + j * step_j)

            step_j = (0.45 - 0.1) / (len(self.costs) // 2)
            for j in range(int(ceil(len(self.costs) / 2)), len(self.costs)):
                self.results[i][j] = self.results[i][j - 1] + step_j

        step_i = (0.4 - 0.1) / (len(self.ratios) * alfa)
        for i in range(int(len(self.ratios) * alfa), int(len(self.ratios) * 2 * alfa)):
            step_j = 0.55 / len(self.costs)

            for j in range(0, len(self.costs)):
                self.results[i][j] = (i * step_i + j * step_j)

        step_i = (5 - 0.4) / (len(self.ratios) - (len(self.ratios) * alfa))
        for i in range(int(len(self.ratios) * 2 * alfa), len(self.ratios)):
            step_j = 1 / len(self.costs)

            for j in range(0, len(self.costs)):
                self.results[i][j] = (i * step_i + j * step_j)

        f = interp2d(self.costs, self.ratios, self.results, kind='linear')

        return f
