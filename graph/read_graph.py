import re
from typing import List

from graph.ProvinceGraph import ProvinceGraph
from graph.division import Division
from graph.province import Province


def read_graph(file_name='input.txt'):
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
                nodes = tuple(map(lambda n: int(n), line.split(' ', 1)))
                graph_map[nodes[0]].neighbours.append(nodes[1])
                graph_map[nodes[1]].neighbours.append(nodes[0])

            elif match_node.match(line):  # province
                node_id = int(line)
                graph_map[node_id] = Province(node_id)

            elif match_special_node.match(line):  # special province
                line: List[str] = line.split(' ')
                node_id = int(line[0])
                if 'C' in line:
                    capital = node_id

                division: Division = None
                if 'D' in line:
                    index = line.index('D')
                    division = Division(float(line[index + 1]))
                    divisions.append(node_id)

                graph_map[node_id] = Province(node_id, division)
            else:
                raise Exception()

        print("graph adj list")
        list(map(lambda n: print(n), graph_map))

    return ProvinceGraph(graph_map, capital, divisions)
