# Ai-sustainable-routing
Sustainable city routing using TALEA data and heat-aware optimization

# AI in Industry – Sustainable Routing Project

## Team

Birungi Jeanritah Roenah

Þóra Katrín Kolbeins Þorvaldsdóttir

## Course
AI in Industry

## Project Topic
Design of Sustainable Cities through Digital Twins and Optimal Routing for Citizens

## Description
This project explores heat-aware routing for pedestrians or cyclists using
urban digital twin data from the TALEA project. We compute routes that
minimize heat exposure and maximize thermal comfort using Urban Heat Exposure
Index (UHEI), NDVI, and green infrastructure data.

## Data Sources
- TALEA Green Cells (11,560 grid cells of 100x100m covering Bologna)
- OpenStreetMap (walking network: 24,584 nodes, 66,156 edges)
- Urban Heat Exposure Index (UHEI)
- Normalized Difference Vegetation Index (NDVI)

## Methods
- Graph-based routing with OSMnx
- Dijkstra's algorithm with custom comfort cost function
- Comfort cost = 20% distance + 40% heat penalty + 40% greenery bonus
- Spatial join between street network and TALEA heat/vegetation grid

## Results (Proof of Concept)
Test route: Bolognina (hot north) → Giardini Margherita (green south park)
- Comfort route is **8.5% greener** and **2.2% cooler**
- Only 236m longer (~3 minutes extra walking)

## Status
✅ Proof of concept complete — comfort routing works!

## Steps
- [x] Extract UHEI and NDVI data from TALEA Green Cells dataset
- [x] Load road network using OpenStreetMap
- [x] Assign heat-aware cost to road segments
- [x] Implement shortest-path vs heat-optimized routing
- [x] Visualize routes on interactive map
- [ ] Test multiple route pairs across Bologna
- [ ] Write final report
- [ ] Create presentation slides

## Repository Structure
```
ai-sustainable-routing/
├── data/               ← TALEA geojson files (UHEI, NDVI grids)
├── docs/               ← TALEA report PDF, data notes
├── src/                ← Python source files
│   ├── load_grid.py
│   ├── cool_route.py
│   ├── balanced_route.py
│   ├── main.py
│   └── TESTING.py
├── notebooks/          ← Colab notebooks
│   └── Bologna_Cool_Routing_Proof_of_Concept.ipynb
└── README.md
```
