from src.routing.compare import compare_routes

GRAPH = {
    "A": [("B", 15, 0.0), ("C", 5, 0.0)],
    "B": [("D", 15, 0.0)],
    "C": [("D", 15, 4.0)],
    "D": [],
    "Z": [],
}


def test_compare_returns_three_routes():
    result = compare_routes(GRAPH, "A", "D", value_per_minute=0.50)
    assert set(result) == {"fastest", "cheapest", "balanced"}
    assert result["fastest"].path == ["A", "C", "D"]
    assert result["cheapest"].path == ["A", "B", "D"]
    assert result["cheapest"].toll == 0.0
    assert result["balanced"].path == ["A", "C", "D"]


def test_compare_unreachable_gives_none():
    result = compare_routes(GRAPH, "A", "Z", value_per_minute=0.50)
    assert all(route is None for route in result.values())