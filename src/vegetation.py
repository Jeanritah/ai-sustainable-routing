# src/vegetation.py
# Bologna Cool Routing — Vegetation (NDVI) Helper
# Birungi Jeanritah Roenah & Þóra Katrín Kolbeins Þorvaldsdóttir

def route_ndvi(G, route):
    """
    Calculate the average Normalized Difference Vegetation Index (NDVI) along a route.
    Higher NDVI = greener, more vegetated street.

    Parameters:
        G     : NetworkX graph (Bologna street network with NDVI values)
        route : list of node IDs representing the route

    Returns:
        float : average NDVI along the route
    """
    values = [
        G[u][v][list(G[u][v].keys())[0]].get('weighted_ndvi', 0.3)
        for u, v in zip(route[:-1], route[1:])
    ]
    return sum(values) / len(values)
