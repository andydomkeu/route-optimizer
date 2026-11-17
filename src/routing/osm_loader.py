import osmnx as ox


def load_graph(path: str):
    G = ox.load_graphml(path)
    return ox.truncate.largest_component(G, strongly=True)