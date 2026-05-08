class Graph:
    def __init__(self, directed=False):
        self._adjacency = {}
        self._directed = directed

    @property
    def directed(self):
        return self._directed

    def add_vertex(self, vertex):
        if vertex not in self._adjacency:
            self._adjacency[vertex] = []

    def add_edge(self, source, target, weight):
        if weight < 0:
            raise ValueError("Dijkstra requires non-negative edge weights")
        self.add_vertex(source)
        self.add_vertex(target)
        self._adjacency[source].append((target, weight))
        if not self._directed:
            self._adjacency[target].append((source, weight))

    def neighbors(self, vertex):
        return self._adjacency.get(vertex, [])

    def vertices(self):
        return list(self._adjacency.keys())

    def vertex_count(self):
        return len(self._adjacency)

    def edge_count(self):
        total = sum(len(neighbors) for neighbors in self._adjacency.values())
        return total if self._directed else total // 2
