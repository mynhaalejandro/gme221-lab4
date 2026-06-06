import matplotlib.pyplot as plt
import pathlib

def visualize_neighbors(gdf, weights_obj, output_name="spatial_weights_graph.png"):
    
    # Create output directory if it doesn't exist
    output_dir = pathlib.Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10,8))

    # plot parcels
    gdf.plot(ax=ax, color="lightblue", edgecolor="black")

    # compute centroids
    centroids = gdf.geometry.centroid

    # plot centroid points
    ax.scatter(
        centroids.x,
        centroids.y,
        color="red",
        s=10,
        label="Parcel Centroids"
    )

    # draw neighbor connections
    for i, neighbors in weights_obj.neighbors.items():

        x1 = centroids.iloc[i].x
        y1 = centroids.iloc[i].y

        for j in neighbors:

            x2 = centroids.iloc[j].x
            y2 = centroids.iloc[j].y

            ax.plot(
                [x1, x2],
                [y1, y2],
                color="green",
                alpha=0.4
            )

    plt.title("Spatial Weights Graph")
    plt.legend()
    
    # Save to output folder
    output_path = output_dir / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")