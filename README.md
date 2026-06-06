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

## Commit Milestones
| Milestone | Description |
|-----------|-------------|
| `init: project structure` | Folders, .gitignore, README scaffolded |
| `feat: spatial weights` | Queen contiguity weights built |
| `feat: global moran` | Global Moran's I computed and printed |
| `feat: local moran` | LISA clusters classified |
| `feat: visualization` | All plots exported to output/ |
| `feat: geojson export` | Results exported as GeoJSON |

## Reflections
*(To be expanded after each milestone.)*
