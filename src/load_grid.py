import geopandas as gpd

# Load TALEA grid with weighted UHEI
uhei = gpd.read_file("grid_uhei.geojson")

print("UHEI columns:", uhei.columns)
print("UHEI sample:")
print(uhei.head())

# Check heat-related column
print(uhei[["weighted_uhei"]].head())

# Normalize weighted UHEI for routing (0–1)
uhei_min = uhei["weighted_uhei"].min()
uhei_max = uhei["weighted_uhei"].max()

uhei["heat_score"] = (
    (uhei["weighted_uhei"] - uhei_min) /
    (uhei_max - uhei_min)
)

print(uhei[["weighted_uhei", "heat_score"]].head())
