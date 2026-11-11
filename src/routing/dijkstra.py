import heapq
from dataclasses import dataclass

Graph = dict[str, list[tuple[str, float, float]]]

@dataclass
class Route:
    path: list[str]
    minutes: float
    toll: float
    cost: float

def edge_cost(minutes: float, toll: float, value_per_minute: float) -> float:
    if value_per_minute <= 0:
        raise ValueError("value_per_minute must be positive")
    return minutes + toll / value_per_minute

def best_route(graph: Graph, start: str, goal: str, value_per_minute: float) -> Route | None:
    best = {start: 0.0}
    prev = {}  # node -> (parent, minutes, toll)
    heap = [(0.0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node == goal:
            return _build_route(prev, start, goal, cost)
        if cost > best.get(node, float("inf")):
            continue
        for neighbor, minutes, toll in graph.get(node, []):
            new_cost = cost + edge_cost(minutes, toll, value_per_minute)
            if new_cost < best.get(neighbor, float("inf")):
                best[neighbor] = new_cost
                prev[neighbor] = (node, minutes, toll)
                heapq.heappush(heap, (new_cost, neighbor))
    return None

def _build_route(prev, start, goal, cost) -> Route:
    path = [goal]
    minutes = toll = 0.0
    node = goal
    while node != start:
        parent, m, t = prev[node]
        minutes += m
        toll += t
        path.append(parent)
        node = parent
    path.reverse()
    return Route(path, minutes, toll, cost)