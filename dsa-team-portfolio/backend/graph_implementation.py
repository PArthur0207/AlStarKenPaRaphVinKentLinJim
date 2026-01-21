from .graph_detail import Graph
import json
import os

class MetroMap:
    def __init__(self):
        self.graph = Graph()
        self.station_to_line = {}
        self._build_network()

    def _build_network(self):
        # Locate the data folder relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, '..', 'data', 'stations.json')
        
        with open(data_path, 'r') as f:
            data = json.load(f)
            
        lrt1 = data["lrt1"]
        lrt2 = data["lrt2"]
        mrt3 = data["mrt3"]
        interchanges = data["interchanges"]

        # 1. Build station → line lookup
        for s in lrt1: self.station_to_line[s] = "lrt1"
        for s in lrt2: self.station_to_line[s] = "lrt2"
        for s in mrt3: self.station_to_line[s] = "mrt3"

        # 2. Add all stations as vertices
        for station in lrt1 + lrt2 + mrt3:
            self.graph.add_vertex(station)

        # 3. Connect stations within the same line (Standard route)
        for line in [lrt1, lrt2, mrt3]:
            for i in range(len(line) - 1):
                self.graph.add_edge(line[i], line[i + 1])
                # add_edge in our Graph class is already bidirectional

        # 4. Connect interchanges explicitly (Bridging the lines)
        for pair in interchanges:
            if len(pair) == 2:
                u, v = pair[0], pair[1]
                if u in self.graph.vertices and v in self.graph.vertices:
                    self.graph.add_edge(u, v)

    def get_route(self, start, end, method="BFS"):
        if start not in self.graph.vertices or end not in self.graph.vertices:
            return None

        # Shortest route is ALWAYS BFS for unweighted graphs like this
        path = self.graph.bfs(start, end)

        if not path:
            return None

        # Attach line information for the frontend glow-effects
        route_with_lines = []
        for station in path:
            route_with_lines.append({
                "name": station,
                "line": self.station_to_line.get(station, "unknown")
            })

        return route_with_lines