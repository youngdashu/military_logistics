from graph.ProvinceGraph import ProvinceGraph
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph, visualize_graph_vectorized

if __name__ == "__main__":


    # visualize_graph_vectorized()

    # exit(0)

    graph: ProvinceGraph = read_graph('./graph/input.txt')

    visualize_graph(graph)


