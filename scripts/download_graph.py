import osmnx as ox

ox.settings.log_console = True
ox.settings.requests_timeout = 600
ox.settings.useful_tags_way += ["toll"]

CENTER = (29.7604, -95.3698)  # downtown Houston (lat, lon)
DIST_M = 25000

G = ox.graph_from_point(CENTER, dist=DIST_M, network_type="drive")
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

ox.save_graphml(G, "data/houston_25km.graphml")
print("saved:", len(G), "intersections,", G.number_of_edges(), "segments")