import osmnx as ox

from src.routing.compare import compare_routes
from src.routing.osm_adapter import osm_to_graph

TOLL_PER_KM = 0.25  # PLACEHOLDER, not a real toll rate

G = ox.load_graphml("data/houston_test.graphml")

TRIPS = {
    "Downtown to west (I-10 / Katy corridor)": ((29.7604, -95.3698), (29.7790, -95.4800)),
    "Downtown to north (Hardy corridor)": ((29.7604, -95.3698), (29.8500, -95.3700)),
}

snapped = {}
for name, (origin, dest) in TRIPS.items():
    start = int(ox.distance.nearest_nodes(G, X=origin[1], Y=origin[0]))
    goal = int(ox.distance.nearest_nodes(G, X=dest[1], Y=dest[0]))
    snapped[name] = (start, goal)

for factor in (1.0, 1.5, 2.0, 3.0):
    graph = osm_to_graph(G, TOLL_PER_KM, congestion_factor=factor)
    print(f"\n=== free freeways take {factor}x longer ===")
    for name, (start, goal) in snapped.items():
        print(f"{name}")
        routes = compare_routes(graph, start, goal, value_per_minute=0.50)
        for label, route in routes.items():
            if route is None:
                print(f"  {label}: no route")
            else:
                print(f"  {label}: {route.minutes:.1f} min, ${route.toll:.2f} toll")