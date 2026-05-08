import pytest

from src.graph import Graph


def test_empty_graph():
    graph = Graph()
    assert graph.vertex_count() == 0
    assert graph.edge_count() == 0
    assert graph.vertices() == []


def test_add_vertex_is_idempotent():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("A")
    assert graph.vertex_count() == 1


def test_undirected_edge_creates_both_directions():
    graph = Graph(directed=False)
    graph.add_edge("A", "B", 3)
    assert ("B", 3) in graph.neighbors("A")
    assert ("A", 3) in graph.neighbors("B")
    assert graph.edge_count() == 1


def test_directed_edge_creates_single_direction():
    graph = Graph(directed=True)
    graph.add_edge("A", "B", 3)
    assert ("B", 3) in graph.neighbors("A")
    assert graph.neighbors("B") == []
    assert graph.edge_count() == 1


def test_negative_weight_rejected():
    graph = Graph()
    with pytest.raises(ValueError):
        graph.add_edge("A", "B", -1)


def test_zero_weight_accepted():
    graph = Graph()
    graph.add_edge("A", "B", 0)
    assert ("B", 0) in graph.neighbors("A")


def test_neighbors_of_unknown_vertex_is_empty():
    graph = Graph()
    assert graph.neighbors("ghost") == []


def test_add_edge_registers_vertices():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    assert set(graph.vertices()) == {"A", "B"}
