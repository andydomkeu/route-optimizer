import pytest
from src.routing.dijkstra import best_route

GRAPH = {
    "A": [("B", 15, 0.0), ("C", 5, 0.0)],
    "B": [("D", 15, 0.0)],
    "C": [("D", 15, 4.0)],
    "D": [],
    "Z": [],
}


def test_toll_route_when_time_is_valuable():
    route = best_route(GRAPH, "A", "D", value_per_minute=0.50)
    assert route.path == ["A", "C", "D"]
    assert route.minutes == 20
    assert route.toll == 4.0


def test_free_route_when_time_is_cheap():
    route = best_route(GRAPH, "A", "D", value_per_minute=0.20)
    assert route.path == ["A", "B", "D"]
    assert route.toll == 0.0


def test_no_route_returns_none():
    assert best_route(GRAPH, "A", "Z", value_per_minute=0.50) is None


def test_invalid_value_raises():
    with pytest.raises(ValueError):
        best_route(GRAPH, "A", "D", value_per_minute=0)