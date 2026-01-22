# balanced_route_only.py
# Single optimal route balancing distance and heat

import osmnx as ox
import networkx as nx
import geopandas as gpd

# --------- CHANGE THESE TO CHANGE THE ROUTE ---------
distance_factor = 1   # weight on distance   (0 = ignore distance, 1 = only distance)
heat_factor     = 0   # weight on heat_cost (0 = ignore heat, 1 = only heat)
# --------------------------------------------------

ox.settings.log_console = True


def build_graph():
    print("Loading Bologna walking network...")
    return ox.graph_from_place("Bologna, Italy", network_type="walk")


def load_grid_with_heat():
    print("Loading grid_uhei.geojson...")
    uhei = gpd.read_file("grid_uhei.geojson")

    verde_min = uhei["verde_pc"].min()
    verde_max = uhei["verde_pc"].max()
    uhei["verde_pc_norm"] = (uhei["verde_pc"] - verde_min) / (verde_max - verde_min)

    # Less green → more heat
    uhei["heat_score"] = 1 - uhei["verde_pc_norm"]
    return uhei


def attach_costs(G, uhei):
    print("Converting graph to GeoDataFrames...")
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

    # Align CRS
    if edges.crs and uhei.crs and edges.crs != uhei.crs:
        uhei = uhei.to_crs(edges.crs)

    print("Performing spatial join (edges ∩ grid)...")
    joined = gpd.sjoin(edges, uhei[["heat_score", "geometry"]],
                       how="left", predicate="intersects")

    heat_by_edge = (
        joined.groupby(["u", "v", "key"])["heat_score"]
        .mean()
        .reset_index()
    )

    edges = edges.merge(heat_by_edge, on=["u", "v", "key"], how="left")

    mean_heat = edges["heat_score"].mean()
    edges["heat_score"] = edges["heat_score"].fillna(mean_heat)

    # Normalize
    edges["length_norm"] = (edges["length"] - edges["length"].min()) / \
                           (edges["length"].max() - edges["length"].min())

    edges["heat_norm"] = (edges["heat_score"] - edges["heat_score"].min()) / \
                         (edges["heat_score"].max() - edges["heat_score"].min())

    print(f"Using distance_factor = {distance_factor}, heat_factor = {heat_factor}")

    edges["balanced_cost"] = (
        distance_factor * edges["length_norm"] +
        heat_factor     * edges["heat_norm"]
    )

    # Write to graph
    for _, row in edges.iterrows():
        u, v, key = row["u"], row["v"], row["key"]
        G[u][v][key]["heat_cost"] = float(row["heat_score"])
        G[u][v][key]["balanced_cost"] = float(row["balanced_cost"])

    return G


def compute_balanced_route(G):
    # New origin/destination
    origin = ox.geocode("Giardini Margherita, Bologna, Italy")
    dest   = ox.geocode("Università di Bologna, Via Zamboni, Bologna, Italy")

    orig_node = ox.nearest_nodes(G, origin[1], origin[0])
    dest_node = ox.nearest_nodes(G, dest[1], dest[0])

    # Compute baseline routes (NOT plotted)
    shortest_route = nx.shortest_path(G, orig_node, dest_node, weight="length")
    coolest_route  = nx.shortest_path(G, orig_node, dest_node, weight="heat_cost")

    # Compute optimal balanced route
    route = nx.shortest_path(G, orig_node, dest_node, weight="balanced_cost")

    # Stats
    def stats(name, rte):
        d = nx.path_weight(G, rte, weight="length")
        h = nx.path_weight(G, rte, weight="heat_cost")
        print(f"{name:10s} | distance = {d:7.1f} m | heat_cost = {h:.3f}")

    print("\n--- Route statistics ---")
    stats("Shortest", shortest_route)
    stats("Coolest", coolest_route)
    stats("Balanced", route)

    return route


def plot_route(G, route):
    print("\nPlotting balanced optimal route (red)...")
    ox.plot_graph_route(
        G,
        route,
        route_color="red",
        route_linewidth=3,
        node_size=0,
        bgcolor="white",
    )


def main():
    G = build_graph()
    uhei = load_grid_with_heat()
    G = attach_costs(G, uhei)
    route = compute_balanced_route(G)
    plot_route(G, route)


if __name__ == "__main__":
    main()
