import random

from src.graph import Graph


def random_sparse_graph(num_vertices, average_degree, seed=None, max_weight=100):
    rng = random.Random(seed)
    graph = Graph(directed=False)
    for vertex in range(num_vertices):
        graph.add_vertex(vertex)

    target_edges = (num_vertices * average_degree) // 2
    edges_added = 0
    seen = set()
    while edges_added < target_edges:
        source = rng.randrange(num_vertices)
        target = rng.randrange(num_vertices)
        if source == target:
            continue
        key = (min(source, target), max(source, target))
        if key in seen:
            continue
        seen.add(key)
        graph.add_edge(source, target, rng.randint(1, max_weight))
        edges_added += 1
    return graph


def random_dense_graph(num_vertices, edge_probability, seed=None, max_weight=100):
    rng = random.Random(seed)
    graph = Graph(directed=False)
    for vertex in range(num_vertices):
        graph.add_vertex(vertex)

    for source in range(num_vertices):
        for target in range(source + 1, num_vertices):
            if rng.random() < edge_probability:
                graph.add_edge(source, target, rng.randint(1, max_weight))
    return graph
