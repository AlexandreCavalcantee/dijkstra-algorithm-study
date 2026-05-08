import pytest

from src.min_heap import MinHeap


def test_empty_heap():
    heap = MinHeap()
    assert heap.is_empty()
    assert len(heap) == 0


def test_pop_returns_minimum_priority():
    heap = MinHeap()
    heap.push("a", 5)
    heap.push("b", 2)
    heap.push("c", 8)
    heap.push("d", 1)
    heap.push("e", 3)

    order = []
    while not heap.is_empty():
        item, _ = heap.pop()
        order.append(item)

    assert order == ["d", "b", "e", "a", "c"]


def test_peek_does_not_remove():
    heap = MinHeap()
    heap.push("x", 10)
    heap.push("y", 1)
    heap.push("z", 5)

    item, priority = heap.peek()
    assert item == "y"
    assert priority == 1
    assert len(heap) == 3


def test_decrease_key_updates_position():
    heap = MinHeap()
    heap.push("a", 10)
    heap.push("b", 20)
    heap.push("c", 30)

    heap.decrease_key("c", 1)
    item, priority = heap.pop()
    assert item == "c"
    assert priority == 1


def test_decrease_key_ignores_higher_priority():
    heap = MinHeap()
    heap.push("a", 5)
    heap.decrease_key("a", 100)
    item, priority = heap.pop()
    assert priority == 5


def test_decrease_key_missing_item_raises():
    heap = MinHeap()
    with pytest.raises(KeyError):
        heap.decrease_key("ghost", 1)


def test_push_existing_item_decreases_key():
    heap = MinHeap()
    heap.push("a", 50)
    heap.push("a", 5)
    assert len(heap) == 1
    item, priority = heap.pop()
    assert item == "a"
    assert priority == 5


def test_contains_reflects_membership():
    heap = MinHeap()
    heap.push("a", 1)
    heap.push("b", 2)
    assert heap.contains("a")
    assert heap.contains("b")
    assert not heap.contains("c")
    heap.pop()
    assert not heap.contains("a")


def test_pop_from_empty_raises():
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.pop()


def test_peek_from_empty_raises():
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.peek()


def test_heap_handles_equal_priorities():
    heap = MinHeap()
    heap.push("a", 5)
    heap.push("b", 5)
    heap.push("c", 5)

    priorities = []
    while not heap.is_empty():
        _, priority = heap.pop()
        priorities.append(priority)

    assert priorities == [5, 5, 5]


def test_heap_property_after_many_operations():
    import random

    random.seed(42)
    heap = MinHeap()
    items = [(f"item_{i}", random.randint(0, 1000)) for i in range(200)]
    for item, priority in items:
        heap.push(item, priority)

    popped = []
    while not heap.is_empty():
        _, priority = heap.pop()
        popped.append(priority)

    assert popped == sorted(popped)
