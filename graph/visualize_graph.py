import tempfile

from graph.ProvinceGraph import ProvinceGraph


def visualize_graph(graph: ProvinceGraph):
    graphviz_graph = graph.graphviz_graph()

    graphviz_graph.view(tempfile.mktemp('.gv'))
