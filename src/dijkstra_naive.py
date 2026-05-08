INFINITY = float("inf")


def dijkstra_naive(graph, source):
    if source not in graph.vertices():
        raise KeyError(f"source vertex {source!r} not in graph")

    distances = {vertex: INFINITY for vertex in graph.vertices()}
    predecessors = {vertex: None for vertex in graph.vertices()}
    distances[source] = 0
    visited = set()

    while len(visited) < graph.vertex_count():
        current = None
        current_distance = INFINITY
        for vertex in graph.vertices():
            if vertex not in visited and distances[vertex] < current_distance:
                current = vertex
                current_distance = distances[vertex]
        if current is None:
            break
        visited.add(current)
        for neighbor, weight in graph.neighbors(current):
            tentative = current_distance + weight
            if tentative < distances[neighbor]:
                distances[neighbor] = tentative
                predecessors[neighbor] = current

    return distances, predecessors


def shortest_path_naive(graph, source, target):
    distances, predecessors = dijkstra_naive(graph, source)
    if distances[target] == INFINITY:
        return None, INFINITY
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    return path, distances[target]
