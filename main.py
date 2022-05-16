from graph.ProvinceGraph import ProvinceGraph
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph

if __name__ == "__main__":
    graph: ProvinceGraph = read_graph('./graph/input.txt')

    graph.clusterize_divisions()

    visualize_graph(graph)

    graph.put_hubs_in_clusters()

    visualize_graph(graph)
