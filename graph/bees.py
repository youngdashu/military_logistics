import random
from queue import PriorityQueue
from typing import List

import math

from graph.ProvinceGraph import ProvinceGraph
from graph.province import Province


def dijkstra(g: ProvinceGraph, root: Province):
    graph = g.graph
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


def find_hub_closest_to_capital(g: ProvinceGraph, hubs: List[Province]):
    root = g.graph[g.capital]

    dist = dijkstra(g, root)



def dijkstra_closest_hub(g: ProvinceGraph, root: Province):
    print(f"root: {root.node_id}")
    dist = dijkstra(g, root)

    print(f"DIST FROM {root.node_id}")
    for province, d in dist.items():
        print(f"{province.node_id} ->  {d}")

    hubs_distances = {province: dist for province, dist in dist.items() if province.node_id in g.hubs}
    print("HUBS")
    for province, d in hubs_distances.items():
        print(f"{province.node_id} ->  {d}")

    min_dist = min(hubs_distances.values())
    closest_hubs = [province for province in hubs_distances if hubs_distances[province] == min_dist]

    print(f"closest hub(s): {closest_hubs}, distance: {min_dist}")

    # TODO: if multiple hubs with min distance -> choose the one with the shortest path to the capital
    if len(closest_hubs) > 1:
        return find_hub_closest_to_capital(g, closest_hubs), min_dist

    return closest_hubs[0], min_dist


class Bees:
    # default ratio of bees to graph vertices (provinces) is set to 0.3
    def __init__(self, graph: ProvinceGraph, bees_ratio: float = .3):
        self.graph = graph
        self.bees_ratio = bees_ratio
        self.bees_number = round(self.graph.provinces_number * self.bees_ratio)
        self.placed_bees = None

    def place_initial_bees(self) -> List[int]:
        print("provinces no.:", len(self.graph.graph))
        print("bees no.:", self.bees_number)
        chosen_provinces = random.sample([province.node_id for province in self.graph.graph], self.bees_number)
        self.placed_bees = chosen_provinces
        return chosen_provinces

    def solve(self):
        print(self.placed_bees)
        for bee in self.placed_bees:
            print(f"Searching for closest hub for bee in [{bee}] province")
            hubs, dist = dijkstra_closest_hub(self.graph, self.graph.graph[bee])
