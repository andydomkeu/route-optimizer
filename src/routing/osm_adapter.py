def _is_toll(value) -> bool:
    return "yes" in str(value)


def _is_freeway(highway) -> bool:
    text = str(highway)
    return "motorway" in text or "trunk" in text


def osm_to_graph(G, toll_per_km: float, congestion_factor: float = 1.0) -> dict:
    graph = {}
    for u, v, data in G.edges(data=True):
        minutes = float(data["travel_time"]) / 60
        toll = 0.0
        if _is_toll(data.get("toll")):
            toll = toll_per_km * float(data["length"]) / 1000
        elif _is_freeway(data.get("highway")):
            minutes *= congestion_factor
        graph.setdefault(u, []).append((v, minutes, toll))
        graph.setdefault(v, [])
    return graph