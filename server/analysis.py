import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="libpysal")

import geopandas as gpd
from sqlalchemy import create_engine
import os
from esda.moran import Moran_Local
from spatial_weights import contiguity_weights, knn_weights, distance_weights
from visualization import visualize_neighbors, visualize_local_moran
from moran import calculate_global_morans_I

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

print(gdf.head())
print("CRS:", gdf.crs)

# Test different weight methods for Local Moran's I
print("\n=== Local Moran's I with Different Weight Methods ===")

# Method 1: Distance weights (threshold=20)
print("\n1. Distance Weights (threshold=20)")
w_dist = distance_weights(gdf, threshold=20)
local_dist = Moran_Local(gdf["ass_ass_va"], w_dist)
gdf_dist = gdf.copy()
gdf_dist["cluster"] = "Not Significant"
gdf_dist.loc[(local_dist.Is > 0) & (local_dist.p_sim < 0.05), "cluster"] = "Hotspot"
gdf_dist.loc[(local_dist.Is < 0) & (local_dist.p_sim < 0.05), "cluster"] = "Coldspot"
print("Distance weights cluster counts:")
print(gdf_dist["cluster"].value_counts())
visualize_local_moran(gdf_dist, "local_moran_distance.png")

# Method 2: KNN weights (k=4)
print("\n2. KNN Weights (k=4)")
w_knn = knn_weights(gdf, k=4)
local_knn = Moran_Local(gdf["ass_ass_va"], w_knn)
gdf_knn = gdf.copy()
gdf_knn["cluster"] = "Not Significant"
gdf_knn.loc[(local_knn.Is > 0) & (local_knn.p_sim < 0.05), "cluster"] = "Hotspot"
gdf_knn.loc[(local_knn.Is < 0) & (local_knn.p_sim < 0.05), "cluster"] = "Coldspot"
print("KNN weights cluster counts:")
print(gdf_knn["cluster"].value_counts())
visualize_local_moran(gdf_knn, "local_moran_knn.png")

# Method 3: Contiguity weights
print("\n3. Contiguity Weights")
w_contig = contiguity_weights(gdf)
local_contig = Moran_Local(gdf["ass_ass_va"], w_contig)
gdf_contig = gdf.copy()
gdf_contig["cluster"] = "Not Significant"
gdf_contig.loc[(local_contig.Is > 0) & (local_contig.p_sim < 0.05), "cluster"] = "Hotspot"
gdf_contig.loc[(local_contig.Is < 0) & (local_contig.p_sim < 0.05), "cluster"] = "Coldspot"
print("Contiguity weights cluster counts:")
print(gdf_contig["cluster"].value_counts())
visualize_local_moran(gdf_contig, "local_moran_contiguity.png")

# Save results for comparison
os.makedirs("output", exist_ok=True)
gdf_dist.to_file("output/clusters_distance.geojson", driver="GeoJSON")
gdf_knn.to_file("output/clusters_knn.geojson", driver="GeoJSON")
gdf_contig.to_file("output/clusters_contiguity.geojson", driver="GeoJSON")

print("\n=== Weight Method Comparison Summary ===")
print("All cluster maps and GeoJSON files saved to output/ folder")
print("Compare the three PNG files to see how hotspot locations change")