from esda.moran import Moran, Moran_Local

def calculate_global_morans_I(gdf, weights_obj, attribute):

    y = gdf[attribute].values
    moran = Moran(y, weights_obj)

    return moran.I, moran.p_sim