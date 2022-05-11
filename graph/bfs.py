import collections


# BFS algorithm


def bfs(graph, root: int):
    default = lambda: 0
    visited, queue, distance = set(), collections.deque([root]), collections.defaultdict(default)
    print(distance[root])
    visited.add(root)

    while queue:

        # Dequeue a vertex from queue
        vertex: int = queue.popleft()
        if distance[vertex] > 2:
            continue
        print(str(vertex) + " ", end="")

        # If not visited, mark it as visited, and
        # enqueue it
        for neighbour in graph.graph[vertex].neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                distance[neighbour] += distance[vertex] + 1

    return distance
