from .dijkstra import Graph, Route, best_route

FASTEST_VALUE = 1_000_000.0   # time is worth so much that tolls barely matter
CHEAPEST_VALUE = 0.0001       # time is worth so little that tolls dominate


def compare_routes(
    graph: Graph, start: str, goal: str, value_per_minute: float
) -> dict[str, Route | None]:
    return {
        "fastest": best_route(graph, start, goal, FASTEST_VALUE),
        "cheapest": best_route(graph, start, goal, CHEAPEST_VALUE),
        "balanced": best_route(graph, start, goal, value_per_minute),
    }