# 🌿 Bologna Cool Routing

> **Heat-aware pedestrian routing for Bologna, Italy**  
> Using the TALEA digital twin to find cooler, greener walking routes.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jeanritah/ai-sustainable-routing/blob/main/notebooks/Bologna_Cool_Routing_Proof_of_Concept.ipynb)

---

## 📌 Project Overview

Standard navigation apps find the **shortest** route — but in a hot city like Bologna, the shortest route is not always the most comfortable one. It may pass through streets in full sun, surrounded by concrete, with no shade or greenery.

**Bologna Cool Routing** finds the **coolest and greenest** walking route instead — using real heat and vegetation data from the TALEA digital twin of Bologna. The system compares a standard shortest route against a comfort-optimised route, measuring the trade-off between distance and walking comfort.

---

## 👥 Team

| Name | Institution |
|------|-------------|
| Birungi Jeanritah Roenah | University of Bologna |
| Þóra Katrín Kolbeins Þorvaldsdóttir | University of Bologna |

**Course:** AI in Industry  
**Project Topic:** Design of Sustainable Cities through Digital Twins and Optimal Routing for Citizens

---

## 🗂️ Repository Structure

```
ai-sustainable-routing/
│
├── notebooks/
│   └── Bologna_Cool_Routing_Proof_of_Concept.ipynb  ← main notebook
│
├── images/
│   ├── bologna_heat_vegetation.png   ← UHEI and NDVI maps of Bologna
│   ├── bologna_streets.png           ← Bologna walking street network
│   └── bologna_cool_routing.html     ← interactive route comparison map
│
├── results/
│   └── route_results.csv             ← results for all 6 tested routes
│
├── src/
│   ├── distance.py                   ← route_distance() function
│   ├── heat.py                       ← route_heat() function
│   ├── vegetation.py                 ← route_ndvi() function
│   └── routing.py                    ← run_route() main function
│
└── README.md
```

---

## 📊 Data Sources

| Dataset | Description | Source |
|---------|-------------|--------|
| **TALEA Green Cells** | Bologna digital twin — 11,560 grid cells (100×100m) with UHEI and NDVI values | [GitHub — SimReale](https://github.com/SimReale/TALEA_Green_Cells) |
| **OpenStreetMap** | Bologna pedestrian walking network — 24,584 nodes, 66,156 edges | via [OSMnx](https://osmnx.readthedocs.io/) |

### Key Variables
- **UHEI** (Urban Heat Exposure Index) — measures heat intensity per grid cell. Higher = hotter.
- **NDVI** (Normalized Difference Vegetation Index) — measures vegetation density. Higher = greener.

---

## ⚙️ Methodology

### Pipeline
1. **Download TALEA data** — 11,560 grid cells with UHEI and NDVI measurements
2. **Download street network** — Bologna walking network via OSMnx
3. **Spatial join** — assign each street its heat and vegetation score from the grid
4. **Fix duplicates** — streets crossing multiple cells are averaged (groupby + mean)
5. **Build comfort cost** — custom weighted formula per street
6. **Route** — Dijkstra's algorithm minimises comfort cost instead of distance
7. **Compare** — measure improvement in heat and greenery vs shortest route

### Comfort Cost Formula

```
comfort_cost = 0.2 × length_norm + 0.4 × uhei_norm + 0.4 × (1 − ndvi_norm)
```

| Component | Weight | Meaning |
|-----------|--------|---------|
| `length_norm` | 20% | Slight preference for shorter streets |
| `uhei_norm` | 40% | Penalise hot streets |
| `1 − ndvi_norm` | 40% | Penalise streets with no greenery |

All values normalised to [0, 1] before combining.  
Weights validated through sensitivity analysis (3 alternative combinations tested).

---

## 📈 Results

### Proof of Concept — Bolognina → Giardini Margherita

| Metric | Shortest Route | Comfort Route | Improvement |
|--------|---------------|--------------|-------------|
| Distance | 4,565 m | 4,801 m | +236 m (+5.2%) |
| Avg UHEI (heat) | 2.1118 | 2.0701 | **−2.0% cooler** |
| Avg NDVI (greenery) | 0.2791 | 0.3035 | **+8.7% greener** |

> For only ~3 minutes of extra walking, the comfort route is meaningfully greener and cooler.

### Multi-Route Analysis (6 Corridors)

| Route | Shortest | Comfort | Heat ↓ | Green ↑ | Extra |
|-------|----------|---------|--------|---------|-------|
| Bolognina → Giardini Margherita | 4,565m | 4,801m | −2.0% | +8.7% | 236m |
| Stazione → Università di Bologna | 2,154m | 2,394m | −2.3%* | −14.4%* | 240m |
| Piazza Maggiore → Parco Villa Ghigi | 2,721m | 2,981m | −1.1% | +3.4% | 260m |
| Fiera District → Parco della Montagnola | 3,552m | 4,344m | −4.7% | +20.3% | 792m |
| Corticella → Giardini Margherita | 7,285m | 9,603m | −5.7% | +19.3% | 2,318m |
| Borgo Panigale → Parco dei Cedri | 5,442m | 6,876m | −4.9% | +17.5% | 1,434m |

*\* Route underperformed — dense city centre with no green alternatives available.*

### Key Findings
- **Vegetation (NDVI) is the stronger signal** — varies more widely than heat across Bologna
- **Longer routes perform better** — more room to find green alternatives
- **Best trade-off:** Bolognina → Giardini Margherita — meaningful gain for minimal extra distance
- **Algorithm is robust** — sensitivity analysis confirmed 20/40/40 weights are near-optimal

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `osmnx` | Download Bologna street network from OpenStreetMap |
| `networkx` | Graph routing — Dijkstra's algorithm |
| `geopandas` | Spatial join — connect streets to heat grid |
| `matplotlib` | Visualise heat and vegetation maps |
| `folium` | Interactive HTML route map |
| `pandas` / `numpy` | Data processing and normalisation |

---

## 🚀 How to Run

1. Open the notebook in Google Colab using the badge at the top
2. Run all cells in order (top to bottom)
3. The notebook downloads all required data automatically
4. The interactive map is saved as `bologna_cool_routing.html`

> ⚠️ The TALEA download (~827 MB) and OSMnx network download take 1–2 minutes each. This is normal.

---

## 📝 Limitations

- TALEA data is static — no time-of-day or seasonal variation
- Cost function weights not calibrated from a user study
- Pedestrian routes only — no cycling or public transport
- Algorithm performs poorly on very short routes (<2.5km) in the dense city centre

---

## 📄 License

This project is for academic purposes — AI in Industry course, University of Bologna, 2026.
