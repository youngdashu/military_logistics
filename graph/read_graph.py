from typing import List
import re

from graph.ProvinceGraph import ProvinceGraph
from graph.division import Division
from graph.province import Province


def read_graph(file_name='input.txt'):
    graph_map = None
    match_edge = re.compile('^[0-9]+ [0-9]+$')
    match_node = re.compile('^[0-9]+$')
    match_special_node = re.compile('^[0-9]+ ((C( D [0-9]+.[0-9]+)?)|(D [0-9]+.[0-9]+( C)?))$')

    with open(file_name, 'r') as f:
        count_line = f.readline()
        lines: List[str] = list(map(lambda l: l.removesuffix('\n'), f.readlines()))

        count = int(count_line)
        graph_map: List[Province] = [None] * count
        capital = None
        divisions = []

        for line in lines:
            line: str = line
            if match_edge.match(line):  # edge
                print(line)
                nodes = tuple(map(lambda n: int(n), line.split(' ', 1)))
                graph_map[nodes[0]].neighbours.append(nodes[1])
                graph_map[nodes[1]].neighbours.append(nodes[0])

                print("edge " + str(nodes))
            elif match_node.match(line):  # province
                node_id = int(line)
                graph_map[node_id] = Province(node_id)
                print("id " + str(node_id))
            elif match_special_node.match(line):  # special province
                line: List[str] = line.split(' ')
                node_id = int(line[0])
                if 'C' in line:
                    capital = node_id

                division: Division = None
                if 'D' in line:
                    index = line.index('D')
                    division = Division(float(line[index+1]))
                    divisions.append(node_id)

                graph_map[node_id] = Province(node_id, division)
                print("special " + str(line))
            else:
                print("Wrong line: " + line)
                raise Exception()

        list(map(lambda n: print(n), graph_map))

    return ProvinceGraph(graph_map, capital, divisions)
        # print(graph_map)