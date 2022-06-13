import tempfile

from graph.ProvinceGraph import ProvinceGraph

def visualize_graph(graph: ProvinceGraph, rails=False):
    graphviz_graph = graph.graphviz_graph(rails=rails)

    graphviz_graph.view(tempfile.mktemp('.gv'))

def visualize_graph_with_terrain(graph: ProvinceGraph, rails=False):
    graph.generate_terrain(1)
    graphviz_graph = graph.vizualize_terrain(rails=rails)
    graphviz_graph.view(tempfile.mktemp('.gv'))

    return graph


def visualize_graph_with_node_ids(graph: ProvinceGraph):
    graphviz_graph = graph.vizualize_terrain(show_node_ids=True)
    graphviz_graph.view(tempfile.mktemp('.gv'))
