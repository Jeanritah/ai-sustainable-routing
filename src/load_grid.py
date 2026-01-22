
import geopandas as gpd

uhei = gpd.read_file("grid_uhei.geojson")

print("UHEI columns:", uhei.columns)
print(uhei[["verde_pc", "area_grid"]].head())
print("verde_pc min/max:", uhei["verde_pc"].min(), uhei["verde_pc"].max())

# Heat proxy: less green -> more heat
uhei["heat_score"] = 1 - (uhei["verde_pc"] / 100.0)

print(uhei[["verde_pc", "heat_score"]].head())

