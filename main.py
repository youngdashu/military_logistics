from graph.ProvinceGraph import ProvinceGraph
from graph.bees import dijkstra_closest_hub
from graph.bees_visualization import visualize_bees
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph

if __name__ == "__main__":
    graph: ProvinceGraph = read_graph('./graph/input.txt')

    # graph.clusterize_divisions()
    #
    # # visualize_graph(graph)
    #
    # graph.put_hubs_in_clusters()
    #
    # # visualize_graph(graph)
    #
    # bees = visualize_bees(graph)
    # print("Placed bees:")
    # print(bees.placed_bees)
    #
    # bees.solve()

    dijkstra_closest_hub(graph, graph.graph[0])

