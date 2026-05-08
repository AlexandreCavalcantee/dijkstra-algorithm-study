from src.min_heap import MinHeap

INFINITY = float("inf")


def _snapshot(event, current, distances, predecessors, visited, edge, relaxed):
    return {
        "event": event,
        "current": current,
        "distances": dict(distances),
        "predecessors": dict(predecessors),
        "visited": set(visited),
        "edge": edge,
        "relaxed": relaxed,
    }


def dijkstra_trace(graph, source):
    if source not in graph.vertices():
        raise KeyError(f"source vertex {source!r} not in graph")

    distances = {vertex: INFINITY for vertex in graph.vertices()}
    predecessors = {vertex: None for vertex in graph.vertices()}
    distances[source] = 0
    visited = set()

    heap = MinHeap()
    for vertex in graph.vertices():
        heap.push(vertex, distances[vertex])

    yield _snapshot("init", None, distances, predecessors, visited, None, False)

    while not heap.is_empty():
        current, current_distance = heap.pop()
        if current_distance == INFINITY:
            break
        visited.add(current)
        yield _snapshot("extract", current, distances, predecessors, visited, None, False)

        for neighbor, weight in graph.neighbors(current):
            tentative = current_distance + weight
            relaxed = tentative < distances[neighbor]
            if relaxed:
                distances[neighbor] = tentative
                predecessors[neighbor] = current
                heap.decrease_key(neighbor, tentative)
            yield _snapshot(
                "relax",
                current,
                distances,
                predecessors,
                visited,
                (current, neighbor, weight),
                relaxed,
            )

    yield _snapshot("done", None, distances, predecessors, visited, None, False)
