import random

import pytest

from src.dijkstra import INFINITY, dijkstra, shortest_path
from src.dijkstra_naive import dijkstra_naive, shortest_path_naive
from src.graph import Graph


def build_classic_graph():
    graph = Graph(directed=False)
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "B", 2)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "D", 5)
    graph.add_edge("D", "E", 3)
    return graph


def build_directed_graph():
    graph = Graph(directed=True)
    graph.add_edge("S", "A", 10)
    graph.add_edge("S", "B", 5)
    graph.add_edge("B", "A", 3)
    graph.add_edge("A", "T", 1)
    graph.add_edge("B", "T", 9)
    return graph


def test_distances_on_classic_graph():
    graph = build_classic_graph()
    distances, _ = dijkstra(graph, "A")
    assert distances == {"A": 0, "B": 3, "C": 1, "D": 4, "E": 7}


def test_path_reconstruction():
    graph = build_classic_graph()
    path, cost = shortest_path(graph, "A", "E")
    assert path == ["A", "C", "B", "D", "E"]
    assert cost == 7


def test_source_to_itself_is_zero():
    graph = build_classic_graph()
    distances, _ = dijkstra(graph, "A")
    assert distances["A"] == 0


def test_directed_graph_respects_direction():
    graph = build_directed_graph()
    distances, _ = dijkstra(graph, "S")
    assert distances == {"S": 0, "A": 8, "B": 5, "T": 9}


def test_disconnected_vertex_has_infinite_distance():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_vertex("Z")
    distances, _ = dijkstra(graph, "A")
    assert distances["A"] == 0
    assert distances["B"] == 1
    assert distances["Z"] == INFINITY


def test_unreachable_target_returns_none_path():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_vertex("Z")
    path, cost = shortest_path(graph, "A", "Z")
    assert path is None
    assert cost == INFINITY


def test_single_vertex_graph():
    graph = Graph()
    graph.add_vertex("solo")
    distances, predecessors = dijkstra(graph, "solo")
    assert distances == {"solo": 0}
    assert predecessors == {"solo": None}


def test_zero_weight_edges():
    graph = Graph()
    graph.add_edge("A", "B", 0)
    graph.add_edge("B", "C", 0)
    distances, _ = dijkstra(graph, "A")
    assert distances == {"A": 0, "B": 0, "C": 0}


def test_cycle_does_not_break_algorithm():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 1)
    graph.add_edge("C", "A", 1)
    distances, _ = dijkstra(graph, "A")
    assert distances == {"A": 0, "B": 1, "C": 1}


def test_source_not_in_graph_raises():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    with pytest.raises(KeyError):
        dijkstra(graph, "ghost")


def test_predecessors_form_valid_tree():
    graph = build_classic_graph()
    distances, predecessors = dijkstra(graph, "A")
    for vertex, distance in distances.items():
        if vertex == "A" or distance == INFINITY:
            continue
        parent = predecessors[vertex]
        assert parent is not None
        edge_weight = next(w for n, w in graph.neighbors(parent) if n == vertex)
        assert distances[parent] + edge_weight == distance


def test_naive_and_heap_agree_on_random_graphs():
    random.seed(123)
    for trial in range(20):
        graph = Graph(directed=random.choice([True, False]))
        vertex_count = random.randint(2, 15)
        vertices = list(range(vertex_count))
        for vertex in vertices:
            graph.add_vertex(vertex)
        edge_count = random.randint(vertex_count, vertex_count * 3)
        for _ in range(edge_count):
            source = random.choice(vertices)
            target = random.choice(vertices)
            if source == target:
                continue
            weight = random.randint(0, 50)
            graph.add_edge(source, target, weight)

        source = vertices[0]
        heap_distances, _ = dijkstra(graph, source)
        naive_distances, _ = dijkstra_naive(graph, source)
        assert heap_distances == naive_distances


def test_naive_path_matches_heap_path():
    graph = build_classic_graph()
    heap_path, heap_cost = shortest_path(graph, "A", "E")
    naive_path, naive_cost = shortest_path_naive(graph, "A", "E")
    assert heap_cost == naive_cost
    assert heap_path == naive_path


def test_multiple_paths_picks_minimum():
    graph = Graph()
    graph.add_edge("A", "B", 10)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "B", 1)
    distances, _ = dijkstra(graph, "A")
    assert distances["B"] == 2
