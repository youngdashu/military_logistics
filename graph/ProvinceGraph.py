import functools
import itertools
import math
from typing import List, Tuple

from graph.bfs import bfs
from graph.cost_function import CostFunction
from graph.hub import Hub
from graph.province import Province

from itertools import chain

from graphviz import Graph

import matplotlib.colors as mcolors

from random import shuffle

from copy import deepcopy


class ProvinceGraph:

    def __init__(self, graph: List[Province], capital: int = None, divisions: List[int] = None):
        self.graph = graph
        self.capital = capital
        self.divisions = divisions
        self.clusters: List[List[int]] = None
        self.hubs = []

    def graphviz_graph(self):
        graphviz_graph = Graph(engine='neato')

        list(map(lambda node:
                 list(map(lambda neighbour:
                          graphviz_graph.edge(str(node.node_id), str(neighbour)) if str(
                              neighbour) + " -- " + str(node.node_id) not in str(graphviz_graph) else None,
                          node.neighbours)),
                 self.graph))

        colors = list(mcolors.CSS4_COLORS.keys())
        colors.remove('white')
        colors.remove('green')
        colors.remove('black')
        shuffle(colors)

        for cluster, _color in zip(self.clusters, colors[:len(self.clusters)]):
            for node_id in cluster:
                graphviz_graph.node(str(node_id), fillcolor=_color, style="filled")

        for division in self.divisions:
            graphviz_graph.node(str(division), shape="rectangle")

        graphviz_graph.node(str(self.capital), shape="pentagon", fillcolor="green", style="filled", height="1.1",
                            width="1.1")

        return graphviz_graph

    def clusterize_divisions(self) -> List[List[int]]:

        def root(province_id_to_root_id: dict, province_id):
            root_id = province_id_to_root_id.get(province_id, -1)

            if root_id == province_id:
                return root_id
            else:
                return root(province_id_to_root_id, root_id)

        clusters: dict = {}
        province_id_to_root_id: dict = {}  # slownik przechowujacy strukture klastrow

        # przechodzimy po prowincjach z dywizjami
        for province in self.graph:

            if province.division is None:
                continue

            # przechodzimy po sasiadach prowincji z dywizja
            for neighbour in province.neighbours:
                # sprawdzamy czy dany sasiad jest juz w jakims klastrze
                cluster_id = province_id_to_root_id.get(neighbour, -1)
                if cluster_id != -1:  # jesli jest w klastrze
                    province_id_to_root_id[province.node_id] = neighbour
                    # aktualnej prowincji przypisujemy sasiada jako rodzica
                    break

            # jesli zaden z sasiadow nie byl w klastrze to tworzymy nowy klaster
            if province_id_to_root_id.get(province.node_id, -1) == -1:
                province_id_to_root_id[province.node_id] = province.node_id

        # wszystkie prowincje z dywizjami sa w klastrach

        # przechodzimy po prowincjach bez dywizji
        for province in self.graph:

            if province.division is not None:
                continue

            connected_clusters: set = set()

            # przechodzimy po sasiadach danej prowincji ktorzy maja dywizje
            for neighbour in province.neighbours:
                if self.graph[neighbour].division is not None:
                    connected_clusters.add(root(province_id_to_root_id, neighbour))
                    # dodajemy id prowincji, ktora jest rootem czyli id klastra

            connected_clusters: list = list(connected_clusters)
            # jesli w otoczeniu danej prowincji znajduje sie wiecej niz jeden klaster to
            # ustawiamy ta prowincje jako nowego roota a sasiednie klastry podpinamy do niej
            if len(connected_clusters) > 1:
                province_id_to_root_id[province.node_id] = province.node_id

                for root_id in connected_clusters:
                    province_id_to_root_id[root_id] = province.node_id

        # struktura dla rozszerzonych klastrow
        new_province_id_to_root_id: dict = {}

        # przechodzimy po prowincjach nieobecnych w strukturze province_id_to_root_id
        for province in self.graph:

            if province_id_to_root_id.get(province.node_id, -1) != -1:
                continue

            # sprawdzamy z ilom prowincjami z jakiegos klastra sasiaduje nasza prowincja
            connected_to: int = 0
            root_id = None
            for neighbour in province.neighbours:
                if province_id_to_root_id.get(neighbour, -1) != -1:
                    connected_to += 1
                    root_id = neighbour

            # jesli sasiaduje z wiecej niz jedna prowincja to dolaczamy ją do klastra
            if connected_to > 1:
                new_province_id_to_root_id[province.node_id] = root_id

        # polaczenie struktur province_id z new_province_id
        for key, value in new_province_id_to_root_id.items():
            province_id_to_root_id[key] = value

        # tworzymy klastry na podstawie struktury province_id
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

    def __place_hub_in_cluster(self, hub_index: int, hub_level: int, cluster: List[int],
                               graph: List["Province"]):

        def set_supplies(supplies_hub_can_supply: float, supplies_circle_needs: float) -> float:
            ratio = supplies_hub_can_supply / supplies_circle_needs
            delivered_supplies = \
                list(map(lambda province_id:
                         graph[province_id].set_required_supplies(graph[province_id].required_supplies() *
                                                                  (1.0 - ratio)),
                         provinces))
            return sum(delivered_supplies, 0.0)

        hub: Hub = Hub(hub_level)

        distance = bfs(self, hub_index)
        provinces_in_range = set(distance.keys()).intersection(set(cluster))
        hub_remaining_capacity = Hub.max_capacity

        provinces_by_distance: List[List[int]] = [[]] * len(set(distance.values()))
        [provinces_by_distance[dist].append(node_id) for node_id, dist in distance.items()]

        # przejdz po prowincjach posortowanych po dystansie

        for dist, provinces in enumerate(provinces_by_distance):

            # for province in provinces:
            #     required_supplies_in_circle += graph[province].required_supplies()
            required_supplies_in_circle = sum(
                map(lambda province_id: graph[province_id].required_supplies(), provinces))

            if required_supplies_in_circle <= hub_remaining_capacity:
                if required_supplies_in_circle <= hub.level_to_supplies(dist):
                    # print("----------------")
                    # for p in provinces:
                    #     print(graph[p].required_supplies())
                    list(map(lambda province_id: graph[province_id].set_required_supplies(0.0),
                             provinces
                             ))
                    hub_remaining_capacity -= required_supplies_in_circle

                    # for p in provinces:
                    #     print(graph[p].required_supplies())
                    # print("$$$$$$")
                else:
                    hub_remaining_capacity -= set_supplies(hub.level_to_supplies(dist), required_supplies_in_circle)

            else:
                hub_remaining_capacity -= set_supplies(hub_remaining_capacity, required_supplies_in_circle)

        print(provinces_by_distance)

    def __func_cost(self, hub_indexes: List[int], hub_levels: List[int], cluster: List[int]):

        graph_copy = deepcopy(self.graph)
        hubs_cost = sum(
            map(lambda hub_level: Hub(hub_level).cost(),
                hub_levels)
        )

        def calculate_required_supplies_in_cluster():
            return sum(map(lambda province_id: graph_copy[province_id].required_supplies(),
                           cluster
                           ))

        required_supplies_in_cluster_before = calculate_required_supplies_in_cluster()

        list(map(lambda hub_index_level:
                 self.__place_hub_in_cluster(hub_index_level[0], hub_index_level[1], cluster, graph_copy),
                 zip(hub_indexes, hub_levels)
                 ))

        # przejdz po klastrze i policz ile zaopatrzenia nie dostarczono
        required_supplies_in_cluster_after = calculate_required_supplies_in_cluster()

        ratio = required_supplies_in_cluster_after / required_supplies_in_cluster_before
        # monozymy przez procent dostarczonych zapasow
        # dzielimy przez wydane pieniadze

        return CostFunction()(ratio, hubs_cost)

    def __put_hub_in_cluster(self, cluster: List[int]):

        print(cluster)
        minimal_hub_count = None

        # wylicz zapotrzebowanie w calym klastrze
        required_supplies = \
            functools.reduce(lambda node_1, node_2:
                             node_1 + self.graph[node_2].required_supplies(),
                             cluster, 0.0)

        print(required_supplies)

        minimal_hub_count = math.ceil(required_supplies / Hub.max_capacity)

        # optimizable len(cluster) -> num of divisions in cluster
        for i in range(minimal_hub_count, len(cluster)):
            suggested_hubs_placement: List[Tuple[int]] = list(itertools.combinations(cluster, i))
            print("s: " + str(suggested_hubs_placement))

            for hubs in suggested_hubs_placement:
                levels = list(itertools.combinations_with_replacement([1, 2, 3], i))
                for level in levels:
                    self.__func_cost(list(hubs), list(level), cluster)

    def put_hubs_in_clusters(self):
        list(map(lambda cluster: self.__put_hub_in_cluster(cluster),
                 self.clusters
                 ))
