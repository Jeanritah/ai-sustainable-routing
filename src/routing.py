# src/routing.py
# Bologna Cool Routing — Main Routing Function
# Birungi Jeanritah Roenah & Þóra Katrín Kolbeins Þorvaldsdóttir

import osmnx as ox
import networkx as nx

from distance import route_distance
from heat import route_heat
from vegetation import route_ndvi


def run_route(G, name, start_lat, start_lon, end_lat, end_lon):
    """
    Run comfort vs shortest routing for a given start/end coordinate pair.
    Prints a comparison of distance, heat (UHEI), and vegetation (NDVI).

    Parameters:
        G         : NetworkX graph with comfort_cost, weighted_uhei, weighted_ndvi on edges
        name      : string label for this route (e.g. 'Bolognina → Giardini Margherita')
        start_lat : latitude of start point
        start_lon : longitude of start point
        end_lat   : latitude of end point
        end_lon   : longitude of end point
    """
    # Find nearest graph nodes to coordinates
    s_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    e_node = ox.distance.nearest_nodes(G, end_lon,   end_lat)

    # Compute both routes
    r_short   = nx.shortest_path(G, s_node, e_node, weight='length')
    r_comfort = nx.shortest_path(G, s_node, e_node, weight='comfort_cost')

    # Measure results
    d_s, d_c = route_distance(G, r_short), route_distance(G, r_comfort)
    h_s, h_c = route_heat(G, r_short),     route_heat(G, r_comfort)
    n_s, n_c = route_ndvi(G, r_short),     route_ndvi(G, r_comfort)

    # Print comparison
    print(f"\n📍 {name}")
    print(f"   Shortest:  {d_s:.0f}m  |  UHEI: {h_s:.4f}  |  NDVI: {n_s:.4f}")
    print(f"   Comfort:   {d_c:.0f}m  |  UHEI: {h_c:.4f}  |  NDVI: {n_c:.4f}")
    print(f"   Heat reduction:  {((h_s - h_c) / h_s * 100):.1f}%")
    print(f"   Green increase:  {((n_c - n_s) / n_s * 100):.1f}%")
    print(f"   Extra distance:  {d_c - d_s:.0f}m")
