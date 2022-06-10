import tempfile

from graph.ProvinceGraph import ProvinceGraph


def visualize_graph_with_terrain(graph: ProvinceGraph):
    graph.generate_terrain(1)
    graphviz_graph = graph.vizualize_terrain()
    graphviz_graph.view(tempfile.mktemp('.gv'))

    return graph


def visualize_graph_with_node_ids(graph: ProvinceGraph):
    graphviz_graph = graph.vizualize_terrain(show_node_ids=True)
    graphviz_graph.view(tempfile.mktemp('.gv'))
