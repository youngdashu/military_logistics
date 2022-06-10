class TerrainGenerator:
    provinceGraph = None

    def __init__(self, provinceGraph: ProvinceGraph):
        self.provinceGraph = provinceGraph

    def generateTerrain(self):

        # Function to print a BFS of graph
        def BFS(self, s):
            visited = [False] * (max(self.graph) + 1)
            queue = []
            queue.append(s)
            visited[s] = True
            while queue:
                s = queue.pop(0)
                print(s, end=" ")
                for i in self.graph[s]:
                    if visited[i] == False:
                        queue.append(i)
                        visited[i] = True
