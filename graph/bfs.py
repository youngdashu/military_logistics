import collections
from functools import cache
from typing import Tuple


@cache
def bfs(graph: Tuple[Tuple[int]], root: int):
    default = lambda: 0

    visited, queue, distance = set(), collections.deque([root]), collections.defaultdict(default)
    visited.add(root)

    while queue:

        # Dequeue a vertex from queue
        vertex: int = queue.popleft()
        if distance[vertex] > 2:
            continue

        # If not visited, mark it as visited, and
        # enqueue it
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                distance[neighbour] += distance[vertex] + 1

    return distance
