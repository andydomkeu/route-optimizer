from src.routing.compare import compare_routes
from src.routing.osm_adapter import osm_to_graph
from src.routing.osm_loader import load_graph

import osmnx as ox

TOLL_PER_KM = 0.25  # PLACEHOLDER, not a real toll rate

G = load_graph("data/houston_25km.graphml")
print(f"{len(G)} intersections in the strongly connected graph")

nodes, edges = ox.graph_to_gdfs(G)

is_toll = edges["toll"].astype(str).str.contains("yes")
named = edges[is_toll & edges["name"].notna()]

graphs = {f: osm_to_graph(G, TOLL_PER_KM, congestion_factor=f) for f in (1.0, 2.0, 3.0)}

for road, group in named.groupby(named["name"].astype(str)):
    ids = set(group.index.get_level_values("u")) | set(group.index.get_level_values("v"))
    pts = nodes.loc[list(ids)]
    span_y = pts["y"].max() - pts["y"].min()
    span_x = pts["x"].max() - pts["x"].min()
    axis = "y" if span_y >= span_x else "x"
    start = int(pts[axis].idxmin())
    goal = int(pts[axis].idxmax())
    km = group["length"].astype(float).sum() / 1000
    print(f"\n{road}: {len(group)} segments, {km:.1f} km, runs along {axis}")
    print(f"  start ({nodes.loc[start, 'y']:.4f}, {nodes.loc[start, 'x']:.4f})"
          f"  goal ({nodes.loc[goal, 'y']:.4f}, {nodes.loc[goal, 'x']:.4f})")

    for factor, graph in graphs.items():
        print(f"  free freeways {factor}x longer")
        routes = compare_routes(graph, start, goal, value_per_minute=0.50)
        for label, route in routes.items():
            if route is None:
                print(f"    {label}: no route")
            else:
                print(f"    {label}: {route.minutes:.1f} min, ${route.toll:.2f} toll")