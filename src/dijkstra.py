from src.min_heap import MinHeap

INFINITY = float("inf")


def dijkstra(graph, source):
    if source not in graph.vertices():
        raise KeyError(f"source vertex {source!r} not in graph")

    distances = {vertex: INFINITY for vertex in graph.vertices()}
    predecessors = {vertex: None for vertex in graph.vertices()}
    distances[source] = 0

    heap = MinHeap()
    for vertex in graph.vertices():
        heap.push(vertex, distances[vertex])

    while not heap.is_empty():
        current, current_distance = heap.pop()
        if current_distance == INFINITY:
            break
        for neighbor, weight in graph.neighbors(current):
            tentative = current_distance + weight
            if tentative < distances[neighbor]:
                distances[neighbor] = tentative
                predecessors[neighbor] = current
                heap.decrease_key(neighbor, tentative)

    return distances, predecessors


def shortest_path(graph, source, target):
    distances, predecessors = dijkstra(graph, source)
    if distances[target] == INFINITY:
        return None, INFINITY
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    return path, distances[target]
