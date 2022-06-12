import collections
from queue import PriorityQueue
from typing import Iterable, List, Tuple

from graph.ProvinceGraph import ProvinceGraph
from graph.bees import Bees


class RailwayPlacer(Bees):
    def __init__(self, graph: ProvinceGraph):
        super().__init__(graph)
        self.costs: List[int] = []
        print(self.graph.hubs)

    def bfs(self, graph: Tuple[Tuple[int]], root: int):
        default = lambda: 0

        visited, queue, distance = set(), collections.deque([root]), collections.defaultdict(default)
        visited.add(root)

        while queue:
            vertex: int = queue.popleft()

            for neighbour in graph[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
                    distance[neighbour] += distance[vertex] + 1

        return distance

    def place_rails(self):
        distances = self.bfs(self.graph.graph_tuples, self.graph.capital)
        parents = []
        terrain_divider = 20

        def recreate_path(start: int, end: int):
            path = []
            current_v = end
            while current_v != start:
                path.append(current_v)
                current_v = parents[current_v]
            return path

        # reverse sort by distance from capital
        distances = [(hub_index, distances[hub_index]) for hub_index in self.graph.hubs]
        distances.sort(reverse=True, key=lambda index_distance: index_distance[1])

        # add costs of going through provinces
        self.costs = [40 * ( 1 + node.terrain/terrain_divider) for node in self.graph.graph]
        self.costs[self.graph.capital] = 0

        supplies_going_through_provinces: List[float] = [0.0 for _ in range(len(self.graph.graph))]

        for hub_index, distance in distances:

            print("hubindex", hub_index)

            while self.graph.graph[hub_index].hub.required_supplies != 0:
                print(hub_index, " required supplies: ", self.graph.graph[hub_index].hub.required_supplies)

                D, parents = self.dijkstra(self.graph.capital)
                path = recreate_path(self.graph.capital, hub_index)
                print("path", path)

                path_max_capacity = float("inf")
                for province_index in path:
                    if 35 - supplies_going_through_provinces[province_index] < path_max_capacity:
                        path_max_capacity = 35 - supplies_going_through_provinces[province_index]

                supplies_transported_for_this_hub = self.graph.graph[hub_index].hub.required_supplies
                self.graph.graph[hub_index].hub.required_supplies = 0.0
                set_costs_to_inf = False
                if supplies_transported_for_this_hub > path_max_capacity:
                    supplies_transported_for_this_hub = path_max_capacity
                    self.graph.graph[hub_index].hub.required_supplies = supplies_transported_for_this_hub - path_max_capacity
                    set_costs_to_inf = True

                for province_index in path:
                    new_supplies_going_through_province = supplies_going_through_provinces[province_index] + \
                                                          supplies_transported_for_this_hub
                    if new_supplies_going_through_province > self.graph.graph[province_index].railway_level_to_capacity():
                        self.graph.graph[province_index].upgrade_railway(new_supplies_going_through_province)
                        self.costs[province_index] = (40 - self.graph.graph[province_index].railway_level_to_capacity())*(1+self.graph.graph[province_index].terrain/terrain_divider)
                        if set_costs_to_inf:
                            self.costs[province_index] = float("inf")

                    supplies_going_through_provinces[province_index] = new_supplies_going_through_province

        print(distances)



    def dijkstra(self, root: int):
        n = len(self.graph.graph)
        D = [float('inf') for _ in range(n)]
        D[root] = 0
        pq = PriorityQueue()
        pq.put((0, root))

        parents: List[int] = [None for _ in range(n)]
        parents[root] = root
        visited = []

        while not pq.empty():
            (dist, current_vertex) = pq.get()
            visited.append(current_vertex)

            for neighbor in self.graph.graph[current_vertex].neighbours:

                distance = max(self.costs[neighbor], self.costs[current_vertex])
                if neighbor not in visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
                        parents[neighbor] = current_vertex
        return D, parents

