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
