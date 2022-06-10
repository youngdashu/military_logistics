import tempfile

from graph.ProvinceGraph import ProvinceGraph
from graph.bees import Bees


def visualize_bees(graph: ProvinceGraph):
    bees = Bees(graph, .4)

    graphviz_graph = graph.graphviz_graph(bees.place_initial_bees())
    graphviz_graph.view(tempfile.mktemp('.gv'))

    return bees
