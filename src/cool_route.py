# cool_route.py
# AI in Industry – Coolest (heat-minimising) walking route
# From Giardini Margherita to the University of Bologna (Via Zamboni)

import osmnx as ox
import networkx as nx
import geopandas as gpd

ox.settings.log_console = True

# 1. Build walking network of Bologna
print("Loading Bologna walking network...")
G = ox.graph_from_place("Bologna, Italy", network_type="walk")

# 2. Load TALEA grid and compute heat_score
print("Loading grid_uhei.geojson...")
uhei = gpd.read_file("grid_uhei.geojson")

print("Sample verde_pc + area_grid:")
print(uhei[["verde_pc", "area_grid"]].head())

verde_min = uhei["verde_pc"].min()
verde_max = uhei["verde_pc"].max()
uhei["verde_pc_norm"] = (uhei["verde_pc"] - verde_min) / (verde_max - verde_min)

# Less green -> more heat
uhei["heat_score"] = 1 - uhei["verde_pc_norm"]

print("Sample verde_pc_norm + heat_score:")
print(uhei[["verde_pc", "verde_pc_norm", "heat_score"]].head())

# 3. Attach heat_score to edges as heat_cost
print("Converting graph to GeoDataFrames...")
nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

print("Edges CRS:", edges.crs)
print("Grid CRS:", uhei.crs)

# Align CRS
if edges.crs is None and uhei.crs is not None:
    edges.set_crs(uhei.crs, inplace=True)
elif edges.crs is not None and uhei.crs is None:
    uhei.set_crs(edges.crs, inplace=True)
elif edges.crs != uhei.crs:
    uhei = uhei.to_crs(edges.crs)

print("Performing spatial join (edges ∩ grid)...")
uhei_slim = uhei[["heat_score", "geometry"]]
joined = gpd.sjoin(edges, uhei_slim, how="left", predicate="intersects")

# Average heat_score if edge intersects multiple cells
heat_by_edge = (
    joined
    .groupby(["u", "v", "key"])["heat_score"]
    .mean()
    .reset_index()
)

# Merge back onto edges
edges = edges.merge(heat_by_edge, on=["u", "v", "key"], how="left")

# Fill missing values with mean
mean_heat = edges["heat_score"].mean()
edges["heat_score"] = edges["heat_score"].fillna(mean_heat)

print("Example edges with heat_score:")
print(edges[["u", "v", "length", "heat_score"]].head())

print("Writing heat_cost back to graph...")
for _, row in edges.iterrows():
    u = row["u"]
    v = row["v"]
    key = row["key"]
    G[u][v][key]["heat_cost"] = float(row["heat_score"])

# 4. Define origin/destination (same as shortest + balanced)
origin_address = "Giardini Margherita, Bologna, Italy"
dest_address   = "Università di Bologna, Via Zamboni, Bologna, Italy"

print("Geocoding origin and destination...")
origin_point = ox.geocode(origin_address)   # (lat, lon)
dest_point   = ox.geocode(dest_address)

orig_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])
dest_node = ox.nearest_nodes(G, dest_point[1], dest_point[0])

# 5. Compute coolest route (minimising heat_cost only)
print("Computing coolest (heat_cost) route...")
coolest_route = nx.shortest_path(G, orig_node, dest_node, weight="heat_cost")

cool_len = nx.path_weight(G, coolest_route, weight="length")
cool_heat = nx.path_weight(G, coolest_route, weight="heat_cost")

print(f"Coolest route distance:   {cool_len:.1f} m")
print(f"Coolest route heat_cost:  {cool_heat:.3f}")

# 6. Plot ONLY the coolest route
print("Plotting coolest route (blue)...")
fig, ax = ox.plot_graph_route(
    G,
    coolest_route,
    route_linewidth=3,
    node_size=0,
    bgcolor="white",
    route_color="blue",
)
