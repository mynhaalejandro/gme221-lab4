# GmE 221 – Laboratory 4: Spatial Autocorrelation and Cluster Detection

## Overview
Spatial statistical analysis of assessed parcel data using Moran's I and
spatial weights. Identifies hotspots and coldspots in assessed property values.

## How to Run

```bash
# 1. Activate virtual environment
.venv\Scripts\activate          # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the analysis
cd server
python analysis.py
```

## Expected Outputs (`output/`)
| File | Description |
|------|-------------|
| `choropleth.png` | Choropleth map of assessed values |
| `moran_scatter.png` | Global Moran's I scatter plot |
| `lisa_clusters.png` | LISA cluster map (HH / LL / HL / LH / NS) |
| `assessed_parcels_moran.geojson` | Full results with cluster labels |

## Project Structure
```
gme221-lab4/
├── .venv/
├── data/
│   └── assessed_parcels.shp
├── output/
├── server/
│   ├── analysis.py
│   ├── moran.py
│   ├── spatial_weights.py
│   └── visualization.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Commit Milestones and Reflections

### Milestone 1: Project Setup
Project structure created with required directories, dependencies configured, and baseline README established.

### Milestone 2: Spatial Data as Statistical Observations
**Why PostGIS over shapefile?** Database storage enables efficient attribute queries and spatial analysis workflows, essential for statistical operations on parcel valuation data.

**What are spatial units vs. observations?** Parcel geometries define spatial units (where), while assessed values represent statistical observations (what) at those locations.

**Why define spatial neighborhoods?** To measure spatial autocorrelation - whether similar property values cluster geographically rather than being randomly distributed across space.

### Milestone 3: Spatial Weights Construction
**What does the spatial weights matrix represent?** It defines which parcels influence each other spatially, encoding neighborhood relationships as a mathematical structure for spatial statistics.

**How do the three weight methods differ?** Contiguity uses shared boundaries, KNN uses nearest neighbors regardless of distance, while distance band includes all parcels within a threshold distance.

**Why are some parcels "islands"?** Islands are parcels with no neighbors under the chosen weight method, often due to geographic isolation or overly restrictive distance thresholds.

#### Experimentation Process:
Tested different weight methods by modifying `w = distance_weights(gdf)` in analysis.py:
1. **Distance method:** `w = distance_weights(gdf)` → Dense neighbor connections within 20 units
2. **KNN method:** `w = knn_weights(gdf)` → Each parcel connects to exactly 4 nearest neighbors
3. **Contiguity method:** `w = contiguity_weights(gdf)` → Only parcels sharing boundaries are neighbors

Each method produced different neighbor structures, confirming the impact of weight selection on spatial relationship definition. Different weight methods define "neighborhood" differently, affecting which parcels influence each other in spatial analysis. Testing multiple approaches helps identify the most appropriate method for the research question.
