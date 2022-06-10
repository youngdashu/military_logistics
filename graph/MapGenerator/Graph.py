import random

from graph.ProvinceGraph import ProvinceGraph
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph_with_terrain


class Graph:
    vertices: [int] = []
    terrain: [float] = []
    buckets: [[int]] = []
    number_of_vertices: int = 0
    number_of_buckets: int = 0
    neighbours_list: [{int}] = []
    ring_density: float

    def __init__(self, number_of_vertices, nuber_of_mountains, number_of_buckets, ring_density: float):
        self.vertices = [i for i in range(number_of_vertices)]
        self.terrain = [0 for i in range(number_of_vertices)]
        self.number_of_vertices = number_of_vertices
        self.number_of_buckets = number_of_buckets
        self.neighbours_list = [set() for _ in range(number_of_vertices)]
        self.ring_density = ring_density
        self.generate_buckets()

    def generate_buckets(self):
        # tworzenie podzbiorów wierzchołków
        tmp_verts = [i for i in range(self.number_of_vertices)]
        bucets = []
        for _ in range(self.number_of_buckets):
            bucets.append([])
            for _ in range(int(self.number_of_vertices / self.number_of_buckets)):
                chosen: int = random.choice(tmp_verts)
                tmp_verts.remove(chosen)
                bucets[-1] += [chosen]
        bucets[-1] += tmp_verts
        self.buckets = bucets
        #         Budowanie grafu
        for bucket in bucets:
            center = bucket[0]
            others = bucket[1:]
            self.neighbours_list[center] = set(others[:])
            number_of_edges = int((len(bucket) - 1) * self.ring_density)
            for id, vert in enumerate(bucket[1: number_of_edges + 1]):
                neibour = bucket[1:][(vert % len(bucket) - 1)]
                if (vert != neibour) and (vert not in self.neighbours_list[neibour]):
                    self.neighbours_list[vert] |= {neibour}

    def save_to_file(self):
        with open('mój.txt', 'w') as file:
            file.write(str(self.number_of_vertices) + '\n')
            file.writelines([str(i) + '\n' for i in range(self.number_of_vertices)])
            for id, neibours in enumerate(self.neighbours_list):
                for n in neibours:
                    line = str(id) + " " + str(n) + '\n'
                    file.write(line)
            file.close()

    def generate_terrain(self, number_of_mountains):
        self.terrain = []


if __name__ == '__main__':
    # my_graph = Graph(1000, 1, 100, 1)
    # my_graph.save_to_file()

    graph: ProvinceGraph = read_graph('./mój.txt')
    graph.clusterize_divisions()

    # graph.put_hubs_in_clusters()

    visualize_graph_with_terrain(graph)
