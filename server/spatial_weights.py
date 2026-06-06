from libpysal.weights import Rook, KNN, DistanceBand

def contiguity_weights(gdf):
    return Rook.from_dataframe(gdf)

def knn_weights(gdf, k=4):
    coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
    return KNN(coords, k=k)

def distance_weights(gdf, threshold=20):
    coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
    return DistanceBand(coords, threshold=threshold)