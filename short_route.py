# shortest_route.py
# AI in Industry – Shortest walking route from Giardini Margherita to the University of Bologna

import osmnx as ox
import networkx as nx

ox.settings.log_console = True

# 1. Build walking network of Bologna
print("Loading Bologna walking network...")
G = ox.graph_from_place("Bologna, Italy", network_type="walk")

# 2. Define new origin/destination addresses
origin_address = "Giardini Margherita, Bologna, Italy"
dest_address   = "Università di Bologna, Via Zamboni, Bologna, Italy"

# 3. Geocode addresses to (lat, lon)
print("Geocoding origin and destination...")
origin_point = ox.geocode(origin_address)
dest_point   = ox.geocode(dest_address)

# 4. Convert (lat, lon) to nearest street nodes
orig_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])
dest_node = ox.nearest_nodes(G, dest_point[1], dest_point[0])

# 5. Compute the shortest path by distance
print("Computing shortest (distance) route...")
shortest_route = nx.shortest_path(G, orig_node, dest_node, weight="length")

# 6. Get route distance
shortest_len = nx.path_weight(G, shortest_route, weight="length")
print(f"Shortest route distance: {shortest_len:.1f} m")

# 7. Plot ONLY the shortest route
print("Plotting shortest route...")
ox.plot_graph_route(
    G,
    shortest_route,
    route_color="red",
    route_linewidth=3,
    node_size=0,
    bgcolor="white",
)
