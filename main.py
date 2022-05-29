from graph.ProvinceGraph import ProvinceGraph
from graph.bees import Bees
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph

if __name__ == "__main__":
    graph: ProvinceGraph = read_graph('./graph/input.txt')

    graph.clusterize_divisions()

    # print("///// AFTER CLUSTERIZATION")
    # visualize_graph(graph)

    # print("///// AFTER PUTTING HUBS IN CLUSTERS")
    # graph.put_hubs_in_clusters()

    visualize_graph(graph)

    bees = Bees(graph, 0.3)
    bees.place_initial_bees()

