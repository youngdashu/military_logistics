from graph.ProvinceGraph import ProvinceGraph
from graph.read_graph import read_graph
from graph.visualize_graph import visualize_graph

if __name__ == "__main__":

    graph: ProvinceGraph = read_graph('./graph/input.txt')

    visualize_graph(graph)