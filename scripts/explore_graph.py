import osmnx as ox

ox.settings.useful_tags_way += ["toll"]

CENTER = (29.7604, -95.3698)  # downtown Houston (lat, lon)

G = ox.graph_from_point(CENTER, dist=15000, network_type="drive")
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

nodes, edges = ox.graph_to_gdfs(G)
print("OSMnx version:", ox.__version__)
print("nodes:", len(nodes), "edges:", len(edges))
print("columns:", list(edges.columns))

if "toll" in edges.columns:
    toll_edges = edges[edges["toll"] == "yes"]
    print("toll edges:", len(toll_edges))
    print(toll_edges[["name", "ref", "highway", "length", "travel_time"]].head(15))
else:
    print("no toll column found")

ox.save_graphml(G, "data/houston_test.graphml")
print("saved")