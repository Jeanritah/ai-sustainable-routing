# src/heat.py
# Bologna Cool Routing — Heat (UHEI) Helper
# Birungi Jeanritah Roenah & Þóra Katrín Kolbeins Þorvaldsdóttir

def route_heat(G, route):
    """
    Calculate the average Urban Heat Exposure Index (UHEI) along a route.
    Higher UHEI = hotter street.

    Parameters:
        G     : NetworkX graph (Bologna street network with UHEI values)
        route : list of node IDs representing the route

    Returns:
        float : average UHEI along the route
    """
    values = [
        G[u][v][list(G[u][v].keys())[0]].get('weighted_uhei', 2.0)
        for u, v in zip(route[:-1], route[1:])
    ]
    return sum(values) / len(values)
