import random
from queue import PriorityQueue
from typing import List

import math

from graph.ProvinceGraph import ProvinceGraph
from graph.province import Province


class Bees:
    # default ratio of bees to graph vertices (provinces) is set to 0.3
    def __init__(self, graph: ProvinceGraph, bees_ratio: float = .3):
        self.graph = graph
        self.bees_ratio = bees_ratio
        self.bees_number = round(self.graph.provinces_number * self.bees_ratio)
        self.placed_bees = None
        self.assigned_bees = {}

    def place_initial_bees(self) -> List[int]:
        print("provinces no.:", len(self.graph.graph))
        print("bees no.:", self.bees_number)
        chosen_provinces = random.sample([province.node_id for province in self.graph.graph], self.bees_number)
        self.placed_bees = chosen_provinces
        return chosen_provinces

    def dijkstra(self, root: Province):
        graph = self.graph.graph
        dist = {province: math.inf for province in graph}
        dist[root] = 0
        visited = set()
        pq = PriorityQueue()
        pq.put((0, root))

        while not pq.empty():
            (d, p) = pq.get()
            visited.add(p)

            # neighbors of province p
            for ngh_id in p.neighbours:
                ngh = graph[ngh_id]

                distance = ngh.terrain
                if ngh not in visited:
                    old_cost = dist[ngh]
                    new_cost = dist[p] + distance

                    if new_cost < old_cost:
                        pq.put((new_cost, ngh))
                        dist[ngh] = new_cost
        return dist

    def find_bees_closest_to_capital(self, bees: List[int]):
        root = self.graph.graph[self.graph.capital]

        dist = self.dijkstra(root)
        print("Multiple closest bees, find dist to capital")
        bees_distance = {province: dist for province, dist in dist.items() if province.node_id in bees}

        print("DIST TO CAPITAL")
        for province, d in bees_distance.items():
            print(f"{province.node_id} ->  {d}")

        closest_bee = min(bees_distance, key=bees_distance.get)
        print(f"closest bee: {closest_bee.node_id}")

        return closest_bee.node_id

    def dijkstra_closest_bees(self, root: Province, bees: List[int]):
        print(f"root: {root.node_id}")
        dist = self.dijkstra(root)

        bees_distance = {province: dist for province, dist in dist.items() if province.node_id in bees and
                         province.node_id not in self.assigned_bees.values()}
        print("BEES")
        for province, d in bees_distance.items():
            print(f"{province.node_id} ->  {d}")

        min_dist = min(bees_distance.values())
        closest_bees = [province.node_id for province in bees_distance if bees_distance[province] == min_dist]

        print(f"closest bee(s): {closest_bees}, distance: {min_dist}")

        # if hub has many bees assigned, choose the one with the shortest path to the capital
        if len(closest_bees) > 1:
            return self.find_bees_closest_to_capital(closest_bees), min_dist

        return closest_bees[0], min_dist

    def solve(self):
        print(self.placed_bees)

        for hub in self.graph.hubs:
            print(f"Searching for closest bee for hub in [{hub}] province")

            closest, dist = self.dijkstra_closest_bees(self.graph.graph[hub], self.placed_bees)
            self.assigned_bees[hub] = closest

        print("Assigned bees")
        print(self.assigned_bees)
