from typing import List

from graph.province import Province

from itertools import chain

from graphviz import Graph


class ProvinceGraph:

    def __init__(self, graph: List[Province], capital: int = None, divisions: List[int] = None):
        self.graph = graph
        self.capital = capital
        self.divisions = divisions

    def graphviz_graph(self):
        graphviz_graph = Graph(engine='neato')

        list(map(lambda node: list(map(lambda neighbour:
                                       graphviz_graph.edge(str(node.node_id), str(neighbour)) if str(
                                           neighbour) + " -- " + str(node.node_id) not in str(graphviz_graph) else None,
                                       node.neighbours)),
                 self.graph))

        return graphviz_graph
