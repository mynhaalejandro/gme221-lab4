import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="libpysal")

import geopandas as gpd
from sqlalchemy import create_engine
from spatial_weights import contiguity_weights, knn_weights, distance_weights
from visualization import visualize_neighbors

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

# Test different weight methods and save visualizations
print("\nGenerating spatial weights visualizations...")

# Distance weights
w_dist = distance_weights(gdf)
visualize_neighbors(gdf, w_dist, "weights_distance_20.png")

# Contiguity weights  
w_contig = contiguity_weights(gdf)
visualize_neighbors(gdf, w_contig, "weights_contiguity.png")

# KNN weights (k=4)
w_knn4 = knn_weights(gdf, k=4)
visualize_neighbors(gdf, w_knn4, "weights_knn_4.png")

# KNN weights (k=8) - denser network
w_knn8 = knn_weights(gdf, k=8)
visualize_neighbors(gdf, w_knn8, "weights_knn_8.png")

# Distance weights with larger threshold
w_dist50 = distance_weights(gdf, threshold=50)
visualize_neighbors(gdf, w_dist50, "weights_distance_50.png")

print("All visualizations saved to output/ folder")