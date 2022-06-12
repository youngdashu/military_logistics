import collections
import random
from functools import cache

from numpy import arange

from graph import ProvinceGraph

def default():
    return 0

random.seed(11)

@cache
def mountainGenerator(graph: ProvinceGraph, root: int, startHeight: float):
    visited, queue, distance = set(), collections.deque([root]), collections.defaultdict(default)
    visited.add(root)
    neighbour_obj = graph.graph[root]
    neighbour_obj.terrain = min(startHeight, 100)
    actual_height = startHeight
    while queue:
        vertex: int = queue.popleft()
        if distance[vertex] > 5:
            continue
        for neighbour in graph.graph[vertex].neighbours:
            neighbour_obj = graph.graph[neighbour]
            if neighbour not in visited:
                neighbour_obj.terrain = min(actual_height, 100)
                visited.add(neighbour)
                queue.append(neighbour)
                distance[neighbour] += distance[vertex] + 1
        actual_height = abs(actual_height)
        actual_height = random.sample(list(arange(0.5, actual_height + 5, 0.5)), 1)[0]


@cache
def riverGenerator(graph: ProvinceGraph, root: int, len=8):
    visited, stack, distance = set(), list(), collections.defaultdict(default)
    visited.add(root)
    stack.append(root)
    id = root
    for _ in range(len):
        actual = graph.graph[id]
        actual.terrain = 13.256
        id = graph.graph[id].neighbours[0]
