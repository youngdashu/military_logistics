import tempfile

from graph.ProvinceGraph import ProvinceGraph

import matplotlib.pyplot as plt


def visualize_graph(graph: ProvinceGraph):
    graphviz_graph = graph.graphviz_graph()

    graphviz_graph.view(tempfile.mktemp('.gv'))

def visualize_graph_vectorized(file_name='./graph/out2.emd'):

    with open(file_name, 'r') as f:
        node_count, dims = tuple(f.readline().split(' '))
        node_count = int(node_count)

        nodes = [None] * node_count


        for line in f.readlines():

            node_id, x, y = tuple(line.split(' '))
            node_id = int(node_id)
            x = float(x)
            y = float(y)

            nodes[node_id] = x, y

        xs, ys = tuple(zip(*nodes))
        plt.scatter(list(xs), list(ys))

        for node_id, coords in enumerate(nodes):
            plt.annotate(str(node_id), coords)

        plt.show()





