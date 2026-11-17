import networkx as nx

from src.routing.osm_adapter import osm_to_graph


def test_osm_to_graph_converts_units_and_tolls():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, travel_time=120.0, length=1000.0, toll="yes")
    G.add_edge(2, 3, travel_time=60.0, length=500.0)

    graph = osm_to_graph(G, toll_per_km=0.5)

    assert graph[1] == [(2, 2.0, 0.5)]
    assert graph[2] == [(3, 1.0, 0.0)]
    assert graph[3] == []

def test_congestion_slows_free_freeways_only():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, travel_time=60.0, length=1000.0, highway="motorway")
    G.add_edge(2, 3, travel_time=60.0, length=1000.0, highway="motorway", toll="yes")
    G.add_edge(3, 4, travel_time=60.0, length=1000.0, highway="residential")

    graph = osm_to_graph(G, toll_per_km=0.5, congestion_factor=2.0)

    assert graph[1][0][1] == 2.0  # free freeway slowed
    assert graph[2][0][1] == 1.0  # toll road not slowed
    assert graph[3][0][1] == 1.0  # local street not slowed