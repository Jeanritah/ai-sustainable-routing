

import geopandas as gpd
import osmnx as ox

uhei = gpd.read_file("grid_uhei.geojson")
ndvi = gpd.read_file("grid_ndvi.geojson")

print("UHEI columns:", uhei.columns)
print("NDVI columns:", ndvi.columns)

print("UHEI sample:")
print(uhei.head())

print("NDVI sample:")
print(ndvi.head())



print(uhei[["verde_pc", "area_grid"]].head())

# If verde_pc looks like 0–1:
#   heat_score = 1 - verde_pc
# If it looks like 0–100:
#   heat_score = 1 - (verde_pc / 100)

# Let's handle both cases robustly by normalizing
verde_min = uhei["verde_pc"].min()
verde_max = uhei["verde_pc"].max()

uhei["verde_pc_norm"] = (uhei["verde_pc"] - verde_min) / (verde_max - verde_min)

# Heat proxy: less green → higher heat
uhei["heat_score"] = 1 - uhei["verde_pc_norm"]

print(uhei[["verde_pc", "verde_pc_norm", "heat_score"]].head())
