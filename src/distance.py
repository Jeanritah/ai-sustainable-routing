# src/distance.py
# Bologna Cool Routing — Distance Helper
# Birungi Jeanritah Roenah & Þóra Katrín Kolbeins Þorvaldsdóttir

def route_distance(G, route):
    """
    Calculate the total walking distance of a route in metres.
    
    Parameters:
        G     : NetworkX graph (Bologna street network)
        route : list of node IDs representing the route
    
    Returns:
        float : total distance in metres
    """
    return sum(
        G[u][v][list(G[u][v].keys())[0]].get('length', 0)
        for u, v in zip(route[:-1], route[1:])
    )
