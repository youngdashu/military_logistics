import collections
import random
from queue import PriorityQueue
from typing import List

import math

from graph.ProvinceGraph import ProvinceGraph
from graph.province import Province


def bfs_closest_hub(g: ProvinceGraph, root: int):
    graph = g.graph_tuples
    # print("graph")
    # print(g.graph_tuples)

    if root in g.hubs:
        return root, 0

    visited, queue, distance = set(), collections.deque([root]), collections.defaultdict(lambda: 0)
    visited.add(root)

    closest_hubs = []
    closest_hub_dist = math.inf

    while queue:
        vertex: int = queue.popleft()
        # if distance[vertex] > 2:
        #     continue

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                distance[neighbour] += distance[vertex] + 1
                if neighbour in g.hubs:
                    closest_hubs.append(neighbour)
                    closest_hub_dist = distance[neighbour]

        if len(closest_hubs) > 0:
            break
    return closest_hubs, closest_hub_dist


def dijkstra_closest_hub(g: ProvinceGraph, root: Province):
    graph = g.graph  # List[Province]
    dist = {province: math.inf for province in graph}
    dist[root] = 0
    visited = set()
    pq = PriorityQueue()
    pq.put((0, root))

    while not pq.empty():
        (d, p) = pq.get()
        visited.add(p)

        # neighbors of p
        # print(f"neighbors of {p.node_id}")
        for ngh_id in p.neighbours:
            # print(f"ngh: {ngh_id}")
            ngh = graph[ngh_id]
            # print(ngh)
            # print(visited)
            distance = ngh.terrain
            # print(f"dist {distance}")
            if ngh not in visited:
                old_cost = dist[ngh]
                new_cost = dist[p] + distance

                if new_cost < old_cost:

                    # print(f"cost: {new_cost}")
                    # print(f"put:    {(new_cost, ngh)}")
                    pq.put((new_cost, ngh))
                    dist[ngh] = new_cost

    print(dist)
    return dist

    #
    # for neighbor in range(graph.v):
    #     if graph.edges[v][neighbor] != -1:
    #         distance = graph.edges[v][neighbor]
    #         if neighbor not in graph.visited:
    #             old_cost = dist[neighbor]
    #             new_cost = dist[v] + distance
    #             if new_cost < old_cost:
    #                 pq.put((new_cost, neighbor))
    #                 dist[neighbor] = new_cost
    return dist


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
            hubs, dist = bfs_closest_hub(self.graph, bee)
            print(f"found hub(s), distance: {dist}")
            print(hubs)
            print()
