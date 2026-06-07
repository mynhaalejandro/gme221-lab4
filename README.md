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
### Milestone 4: Spatial Weights Visualization and Analysis

**1. How does the spatial weights graph represent neighborhood relationships?** Each parcel centroid becomes a node (dot) on the map, and connecting lines become edges that link neighboring parcels. This creates a spatial network where nodes represent geographic locations and edges represent which parcels influence each other spatially.

**2. How does the structure of the neighbor graph change between methods?**
- **Contiguity weights:** Creates sparse connections only between parcels that share boundaries - realistic but many isolated parcels
- **K-nearest neighbors (KNN):** Ensures every parcel connects to exactly K closest neighbors - eliminates isolation but may create unrealistic long-distance connections
- **Distance-based weights:** Connects all parcels within threshold distance - balances connectivity with geographic realism

**3. What changes do you observe when modifying parameters?**
- **Increasing K in KNN (4→8):** Each parcel gains additional neighbor connections, creating a much denser web of relationships across the map
- **Increasing distance threshold (20→50):** More parcels fall within connection range, reducing isolated parcels and increasing overall network density

**4. Does increasing K or distance create a denser spatial network?** Yes, both parameters create denser networks with more connections between parcels. This affects spatial autocorrelation strength because more parcels can influence each other, potentially amplifying clustering patterns in the statistical analysis.

**5. Which spatial weights method best represents parcel relationships?** Contiguity weights best represent real property relationships because adjacent parcels genuinely influence each other through shared infrastructure, similar zoning, and neighborhood effects. Distance and KNN methods may create artificial connections between properties that don't logically influence each other.

**6. Why is it important to visualize spatial weights before computing Moran's I?** Visualization reveals whether neighborhood definitions make geographic sense before running statistics. Incorrect neighborhood structures could connect unrelated parcels or miss important adjacencies, leading to misleading spatial autocorrelation results that don't reflect actual spatial patterns in property values.

Spatial autocorrelation results are only as meaningful as the neighborhood definition used to compute them. If we define "neighbors" incorrectly, our statistical conclusions about property value clustering will be wrong. The visualization step ensures our neighborhood definitions make real-world sense before we analyze the data.

### Milestone 5: Global Spatial Autocorrelation Analysis

**1. What does positive Moran's I indicate?** Positive Moran's I indicates spatial clustering - similar property values tend to be located near each other. High-value properties cluster together, and low-value properties also cluster together, rather than being randomly distributed across space.

**2. Why is the p-value required for interpretation?** The p-value determines statistical significance. Even if Moran's I shows clustering (positive value), we need p < 0.05 to confirm the pattern isn't due to random chance. Both our results (p=0.023 and p=0.014) are statistically significant.

**3. What would Moran's I near zero suggest?** Moran's I near zero suggests random spatial distribution - property values show no clear spatial pattern. High and low values would be scattered randomly across the map without clustering.

**4. What is the role of the attribute in computing Moran's I?** The attribute (ass_ass_va or ass_market) provides the values being analyzed for spatial patterns. Moran's I measures whether similar attribute values cluster spatially. Different attributes can show different spatial patterns even for the same parcels.

**5. How might results change with different attributes?** Our results show assessed values (I=0.068) have slightly stronger clustering than market values (I=0.060). This suggests assessed values may be more spatially influenced by neighborhood factors, while market values show more variation independent of location.

**6. Why does Moran's I require both spatial weights and attribute variables?** The spatial weights matrix defines "who are neighbors" while the attribute variable defines "what values are being compared." Without spatial weights, we can't determine spatial relationships. Without attributes, we have nothing to measure for clustering patterns.

The results confirm that property values in this area show spatial clustering - similar values tend to be located near each other rather than randomly scattered. Both assessed and market values cluster spatially, but assessed values show slightly stronger clustering. This suggests that neighborhood characteristics (zoning, infrastructure, local amenities) influence property valuations, creating geographic patterns of high-value and low-value areas.

### Milestone 6: Local Spatial Autocorrelation Analysis

**1. What is the difference between Global Moran's I and Local Moran's I?** Global Moran's I provides a single statistic summarizing spatial autocorrelation across the entire study area. Local Moran's I calculates a statistic for each individual parcel, identifying where specific clusters or outliers occur spatially.

**2. How are hotspots and coldspots identified using Local Moran's I?** Hotspots are parcels with positive Local Moran's I values and p < 0.05, indicating high values surrounded by high values. Coldspots have negative Local Moran's I values and p < 0.05, indicating low values surrounded by low values. Non-significant areas (p ≥ 0.05) show no clear clustering pattern. Our analysis identified 210 hotspots, 7 coldspots, and 484 not significant parcels out of 701 total parcels.

**3. Where do hotspots appear in your dataset?** Our analysis identified 210 hotspot parcels out of 701 total parcels. These represent areas where high-value properties cluster together, likely indicating premium neighborhoods or areas with desirable characteristics like good infrastructure, amenities, or zoning.

**4. Where do coldspots appear in your dataset?** Only 7 coldspot parcels were identified, indicating rare areas where low-value properties cluster together. This suggests the study area doesn't have extensive low-value neighborhoods, possibly indicating overall decent property values throughout the region.

**5. Did you observe any spatial outliers?** The analysis classified parcels into three categories: 210 hotspots (high values surrounded by high values), 7 coldspots (low values surrounded by low values), and 484 not significant areas. This simplified classification focused on clustering patterns rather than explicitly identifying spatial outliers like High-Low (expensive property in cheap area) or Low-High (cheap property in expensive area) patterns. The low number of coldspots (only 7) suggests spatial outliers are rare in this dataset, with most clustering being positive (high-value areas).

**6. How does changing spatial weights affect Local Moran's I results?** Different weight methods alter neighbor definitions, changing which parcels qualify as hotspots or coldspots. Distance-based weights capture broader neighborhood effects compared to contiguity weights, which produce more localized clusters. KNN weights ensure no isolated parcels but create artificial long-distance connections affecting cluster patterns.

#### Experimentation Process:
Tested Local Moran's I with three different weight methods:
1. **Distance weights (threshold=20):** 219 hotspots, 9 coldspots, 473 not significant
2. **KNN weights (k=4):** 213 hotspots, 3 coldspots, 485 not significant  
3. **Contiguity weights:** 177 hotspots, 50 coldspots, 474 not significant

Different weight methods produced significantly different cluster patterns. Distance weights detected the most hotspots, while contiguity weights found dramatically more coldspots (50 vs 3-9). This confirms that neighborhood definition critically affects spatial autocorrelation results.

**7. How does changing attributes affect spatial clusters?** The comparison shows that assessed values and market values produce remarkably similar spatial clustering patterns:
- **Assessed values:** 210 hotspots, 7 coldspots, 484 not significant
- **Market values:** 206 hotspots, 9 coldspots, 486 not significant

The minimal differences (4 hotspot variance, 2 coldspot variance) indicate both valuation methods capture similar underlying geographic factors. This suggests assessment procedures closely align with market realities, and neighborhood characteristics equally influence both official assessments and market transactions. For spatial autocorrelation analysis, either attribute leads to similar conclusions about property value clustering patterns.