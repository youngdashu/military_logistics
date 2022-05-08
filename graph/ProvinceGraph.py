from typing import List

from graph.province import Province

from itertools import chain

from graphviz import Graph

class ProvinceGraph:

    def __init__(self, graph: List[Province], capital: int = None, divisions: List[int] = None):
        self.graph = graph
        self.capital = capital
        self.divisions = divisions
        self.clusters = None

    def graphviz_graph(self):
        graphviz_graph = Graph(engine='neato')

        list(map(lambda node: list(map(lambda neighbour:
                                       graphviz_graph.edge(str(node.node_id), str(neighbour)) if str(
                                           neighbour) + " -- " + str(node.node_id) not in str(graphviz_graph) else None,
                                       node.neighbours)),
                 self.graph))

        for cluster, _color in zip(self.clusters, ['red', 'green', 'blue']):
            for node_id in cluster:
                graphviz_graph.node(str(node_id), color=_color)

        return graphviz_graph

    def clusterize_divisions(self) -> List[List[int]]:

        def root(province_id_to_root_id: dict, province_id):
            root_id = province_id_to_root_id.get(province_id, -1)

            if root_id == province_id:
                return root_id
            else:
                return root(province_id_to_root_id, root_id)

        clusters: dict = {}
        province_id_to_root_id: dict = {}

        for province in self.graph:

            if province.division is None:
                continue

            for neighbour in province.neighbours:
                cluster_id = province_id_to_root_id.get(neighbour, -1)
                if cluster_id != -1:
                    province_id_to_root_id[province.node_id] = neighbour
                    break

            if province_id_to_root_id.get(province.node_id, -1) == -1:
                province_id_to_root_id[province.node_id] = province.node_id

        for province in self.graph:

            if province.division is not None:
                continue

            connected_clusters: set = set()

            for neighbour in province.neighbours:
                if self.graph[neighbour].division is not None:
                    connected_clusters.add(root(province_id_to_root_id, neighbour))

            connected_clusters: list = list(connected_clusters)
            if len(connected_clusters) > 1:
                province_id_to_root_id[province.node_id] = province.node_id

                for root_id in connected_clusters:
                    province_id_to_root_id[root_id] = province.node_id

        new_province_id_to_root_id: dict = {}
        for province in self.graph:

            if province_id_to_root_id.get(province.node_id, -1) != -1:
                continue

            conncected_to: int = 0
            root_id = None
            for neighbour in province.neighbours:
                if province_id_to_root_id.get(neighbour, -1) != -1:
                    conncected_to += 1
                    root_id = neighbour

            if conncected_to > 1:
                new_province_id_to_root_id[province.node_id] = root_id

        for key, value in new_province_id_to_root_id.items():
            province_id_to_root_id[key] = value

        for province_id in range(len(self.graph)):
            root_id = root(province_id_to_root_id, province_id)

            if root_id == -1:
                continue

            if not clusters.get(root_id, []):
                clusters[root_id] = [province_id]
            else:
                clusters[root_id].append(province_id)

        self.clusters = list(clusters.values())
        return self.clusters
