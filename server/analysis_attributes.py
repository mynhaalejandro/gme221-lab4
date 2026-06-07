import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="libpysal")

import geopandas as gpd
from sqlalchemy import create_engine
import os
from esda.moran import Moran_Local
from spatial_weights import distance_weights
from visualization import visualize_local_moran

host = "localhost"
port = "5432"
dbname = "gme221_exer4"
user = "postgres"
password = "postgres"

conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(conn_str)

sql_query = """
SELECT gid, ass_ass_va, ass_market, geom
FROM public.assessed_parcels;
"""

gdf = gpd.read_postgis(sql_query, engine, geom_col="geom")

print("=== Local Moran's I with Different Attributes ===")

# Use distance weights for both analyses
w = distance_weights(gdf, threshold=20)

# Test 1: ass_ass_va attribute
print("\n1. Assessed Value (ass_ass_va)")
local_assessed = Moran_Local(gdf["ass_ass_va"], w)
gdf_assessed = gdf.copy()
gdf_assessed["cluster"] = "Not Significant"
gdf_assessed.loc[(local_assessed.Is > 0) & (local_assessed.p_sim < 0.05), "cluster"] = "Hotspot"
gdf_assessed.loc[(local_assessed.Is < 0) & (local_assessed.p_sim < 0.05), "cluster"] = "Coldspot"
print("Assessed value cluster counts:")
print(gdf_assessed["cluster"].value_counts())
visualize_local_moran(gdf_assessed, "local_moran_assessed_value.png")

# Test 2: ass_market attribute  
print("\n2. Market Value (ass_market)")
local_market = Moran_Local(gdf["ass_market"], w)
gdf_market = gdf.copy()
gdf_market["cluster"] = "Not Significant"
gdf_market.loc[(local_market.Is > 0) & (local_market.p_sim < 0.05), "cluster"] = "Hotspot"
gdf_market.loc[(local_market.Is < 0) & (local_market.p_sim < 0.05), "cluster"] = "Coldspot"
print("Market value cluster counts:")
print(gdf_market["cluster"].value_counts())
visualize_local_moran(gdf_market, "local_moran_market_value.png")

# Save results for comparison
os.makedirs("output", exist_ok=True)
gdf_assessed.to_file("output/clusters_assessed_value.geojson", driver="GeoJSON")
gdf_market.to_file("output/clusters_market_value.geojson", driver="GeoJSON")

print("\n=== Attribute Comparison Summary ===")
print("Cluster maps saved:")
print("- local_moran_assessed_value.png")
print("- local_moran_market_value.png")
print("GeoJSON files saved for further analysis")