import functools
from random import shuffle
from typing import List, Tuple

import itertools
import math
import matplotlib.colors as mcolors
from graphviz import Graph
from time import time

from graph.bfs import bfs
from graph.cost_function import CostFunction
from graph.hub import Hub
from graph.province import Province


class ProvinceGraph:

    def __init__(self, graph: List[Province], capital: int = None, divisions: List[int] = None):
        self.graph: List[Province] = graph
        self.graph_tuples: Tuple[Tuple[int]] = None
        self.capital = capital
        self.divisions = divisions
        self.clusters: List[List[int]] = None
        self.hubs = []
        self.small_graph: List[Province] = None
        self.provinces_number = len(self.graph)

        self.colors = []
        self.init_colors()

        self.change_to_tuple()

        self.time_bfs = 0.0
        self.time_copy = 0.0

    def change_to_tuple(self):
        self.graph_tuples = tuple(
            map(lambda province: province.change_to_tuple(), self.graph)
        )



    def __hash__(self):
        return hash((self.capital, tuple(self.graph)))

    def init_colors(self):
        colors = list(mcolors.CSS4_COLORS.keys())
        colors.remove('white')
        colors.remove('green')
        colors.remove('black')
        shuffle(colors)

        self.colors = colors

    def graphviz_graph(self, bees: List[int] = None):
        graphviz_graph = Graph(engine='neato')
        list(map(lambda node:
                 list(map(lambda neighbour:
                          graphviz_graph.edge(str(node.node_id), str(neighbour)) if str(
                              neighbour) + " -- " + str(node.node_id) not in str(graphviz_graph) else None,
                          node.neighbours)),
                 self.graph))

        # color of clusters
        for cluster, _color in zip(self.clusters, self.colors[:len(self.clusters)]):
            for node_id in cluster:
                graphviz_graph.node(str(node_id), fillcolor=_color, style="filled")

        # shape of divisions
        for division in self.divisions:
            graphviz_graph.node(str(division), shape="rectangle")

        # capital
        graphviz_graph.node(str(self.capital), shape="pentagon", fillcolor="green", style="filled", height="1.1",
                            width="1.1")

        # hubs
        for hub in self.hubs:
            graphviz_graph.node(str(hub), shape="diamond")

        for hub_division in set(self.hubs).intersection(set(self.divisions)):
            graphviz_graph.node(str(hub_division), shape="Mdiamond")

        if bees:
            for b in bees:
                graphviz_graph.node(str(b), fontcolor="goldenrod3")

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
        for province_id in range(self.provinces_number):
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
                         graph[province_id].set_required_supplies(
                             graph[province_id].required_supplies() * (1.0 - ratio)),
                         provinces))
            return sum(delivered_supplies, 0.0)

        hub: Hub = Hub(hub_level)
        s = time()
        distance = bfs(self.graph_tuples, hub_index)
        self.time_bfs += (time() - s)
        provinces_in_range = set(distance.keys()).intersection(set(cluster))

        hub_remaining_capacity = Hub.max_capacity

        provinces_by_distance: List[List[int]] = [[]] * len(set(distance.values()))
        [provinces_by_distance[dist].append(node_id) for node_id, dist in distance.items() if
         node_id in provinces_in_range]

        # przejdz po prowincjach posortowanych po dystansie

        for dist, provinces in enumerate(provinces_by_distance):

            required_supplies_in_circle = sum(
                map(lambda province_id:
                    graph[province_id].required_supplies(),
                    provinces
                    ))

            if required_supplies_in_circle <= hub_remaining_capacity:
                if required_supplies_in_circle <= hub.level_to_supplies(dist):

                    list(map(lambda province_id:
                             graph[province_id].set_required_supplies(0.0),
                             provinces
                             ))
                    hub_remaining_capacity -= required_supplies_in_circle

                else:
                    hub_remaining_capacity -= set_supplies(hub.level_to_supplies(dist), required_supplies_in_circle)

            else:
                hub_remaining_capacity -= set_supplies(hub_remaining_capacity, required_supplies_in_circle)

    def __func_cost(self, hub_indexes: List[int], hub_levels: List[int], cluster: List[int], f: CostFunction) -> float:

        s = time()

        supplies_copy = {node_id: self.graph[node_id].required_supplies() for node_id in cluster}

        self.time_copy += (time() - s)

        hubs_cost = sum(
            map(lambda hub_level:
                Hub(hub_level).cost(),
                hub_levels
                ))

        def calculate_required_supplies_in_cluster():
            return sum(map(lambda province_id:
                           self.graph[province_id].required_supplies(),
                           cluster
                           ))

        required_supplies_in_cluster_before = calculate_required_supplies_in_cluster()

        list(map(lambda hub_index_level:
                 self.__place_hub_in_cluster(hub_index_level[0], hub_index_level[1], cluster, self.graph),
                 zip(hub_indexes, hub_levels)
                 ))

        # przejdz po klastrze i policz ile zaopatrzenia nie dostarczono
        required_supplies_in_cluster_after = calculate_required_supplies_in_cluster()

        ratio = required_supplies_in_cluster_after / required_supplies_in_cluster_before
        # monozymy przez procent dostarczonych zapasow
        # dzielimy przez wydane pieniadze

        list(map(
            lambda key_value: self.graph[key_value[0]].set_required_supplies(key_value[1]),
            supplies_copy.items()
        ))

        return f(hubs_cost, ratio)[0]

    def __put_hub_in_cluster(self, cluster: List[int]):

        best_hub_placement = None
        best_evaluation = float('inf')

        # wylicz zapotrzebowanie w calym klastrze
        required_supplies = \
            functools.reduce(lambda node_1, node_2:
                             node_1 + self.graph[node_2].required_supplies(),
                             cluster, 0.0)

        minimal_hub_count = math.ceil(required_supplies / Hub.max_capacity)

        num_of_divisions_in_cluster = sum(
            map(lambda node_id: self.graph[node_id].number_of_divisions_in_province(),
                cluster
                ), 0
        )

        f = CostFunction()(len(cluster))

        for i in range(minimal_hub_count, num_of_divisions_in_cluster):
            suggested_hubs_placement: List[Tuple[int]] = list(itertools.combinations(cluster, i))

            print("len ", len(suggested_hubs_placement))
            for hubs in suggested_hubs_placement:
                levels = list(itertools.combinations_with_replacement([1, 2, 3], i))

                for level in levels:
                    evaluated_hubs_placement: float = self.__func_cost(list(hubs), list(level), cluster, f)

                    if evaluated_hubs_placement < best_evaluation:
                        best_evaluation = evaluated_hubs_placement
                        best_hub_placement = list(hubs), level

                        if best_evaluation == 0.0:
                            print(best_hub_placement)
                            print("time", self.time_copy)
                            return best_hub_placement

        print(best_hub_placement)
        print("time", self.time_copy)

        return best_hub_placement

    def put_hubs_in_clusters(self):
        hubs = list(map(
            lambda cluster:
            self.__put_hub_in_cluster(cluster),
            self.clusters
        ))

        list(map(
            lambda hubs_in_cluster:
            map(
                lambda hub_level:
                self.graph[hub_level[0]].set_hub(hub_level[1]),
                zip(hubs_in_cluster[0], hubs_in_cluster[1])
            ),
            hubs
        ))

        list(map(
            lambda hubs_in_cluster:
            self.hubs.extend(hubs_in_cluster[0]),
            hubs
        ))
