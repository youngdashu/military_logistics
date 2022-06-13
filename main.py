from graph.ProvinceGraph import ProvinceGraph
from graph.bees_visualization import visualize_bees
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph_with_terrain, visualize_graph_with_node_ids

if __name__ == "__main__":
    graph: ProvinceGraph = read_graph('./graph/input.txt')

    graph.clusterize_divisions()
    graph.put_hubs_in_clusters()

    g = visualize_graph_with_terrain(graph)
    visualize_graph_with_node_ids(g)

    bees = visualize_bees(graph)
    print("Placed bees:")
    print(bees.placed_bees)
    bees.solve()
    bees.sendBeesFromStartVert()

    visualize_graph_with_terrain(graph, True)