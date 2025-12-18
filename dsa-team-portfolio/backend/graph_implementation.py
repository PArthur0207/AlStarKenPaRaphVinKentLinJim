from .graph_detail import Graph
from .stations import lrt1, lrt2, mrt3, interchanges

class MetroMap:
    def __init__(self):
        self.graph = Graph()
        self._build_network()

    def _build_network(self):
        for station in lrt1 + lrt2 + mrt3:
            self.graph.add_vertex(station)

        for line in [lrt1, lrt2, mrt3]:
            for i in range(len(line) - 1):
                self.graph.add_edge(line[i], line[i+1])
                self.graph.add_edge(line[i+1], line[i])

        for a, b in interchanges:
            self.graph.add_edge(a, b)            
            self.graph.add_edge(b, a)

    def get_route(self, start, end):
        if start not in self.graph.vertices or end not in self.graph.vertices:
            return "Station not found."
        return self.graph.bfs(start, end)