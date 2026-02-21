# Visualization (Phase 4)

**Project:** Urban Data Cleaning, Integration, and Enrichment with Python

## Overview
This phase generates visual analyses from the integrated dataset
`data/processed/final_integrated_dataset.csv`

All figures are produced in the notebook:
`notebooks/analysis_visualization.ipynb`

Outputs are saved in:
`outputs/visualizations/`


## Visuals Produced

### 1) Complaint Hotspots (Hexbin Heatmap)
- **File:** outputs/visualizations/hotspots_hexbin.png
- **Purpose:** To Show spatial clustering of complaints across the city.
- **Method:** Hexbin density on complaint latitude/longitude.
- **Interpretation:** The brightest hexes represent the highest complaint density, indicating geographic hotspots. These hotspots typically align with dense residential or commercial corridors and should be interpreted as areas with higher service demand or reporting frequency, not necessarily worse service quality. The spatial concentration suggests that targeted interventions in those zones could address a large share of complaints.

### 2) Business Density vs Complaint Frequency
- **File:** outputs/visualizations/density_vs_complaints.png
- **Purpose:** Compare complaint counts against local business density.
- **Method:** Grid-based aggregation with scatter plot and trend line.
- **Interpretation:** The upward trend line indicates a positive relationship between business density and complaint volume. This is expected as more businesses correlate with more foot traffic, activity, and service interactions, which increases opportunities for complaints. Points above the trend line may represent unusually high complaint areas relative to business density and could warrant closer inspection.

### 3) Complaint Clusters (TF-IDF + KMeans)
- **Files:**
  - outputs/visualizations/cluster_sizes.png
  - outputs/visualizations/cluster_pca.png
- **Purpose:** Group complaint types by text similarity.
- **Method:** TF-IDF vectors from complaint category + service name, KMeans clustering, PCA projection.
- **Interpretation:**
  - **Cluster sizes bar chart:** Uneven cluster sizes indicate that some complaint themes are far more common than others. Larger clusters represent dominant complaint types in the dataset.
  - **PCA plot:** The PCA projection provides a 2D view of cluster separation. The Visible separation suggests distinct complaint themes, while overlap indicates shared vocabulary or similar complaint descriptions.

### 4) Complaint Patterns Near Business Categories
- **File:** outputs/visualizations/complaint_patterns_by_business_group.png
- **Purpose:** Compare complaint patterns near different business groups.
- **Method:** Map business categories into restaurant / retail / services, then plot a category-by-group heatmap.
- **Interpretation:** The heatmap highlights how complaint categories distribute across nearby business groups. Higher intensity in a specific cell means that complaints of that category are more frequent near that business group. For example, if “Public Safety” is darker near “services,” it may indicate that those areas experience more safety related complaints relative to retail or restaurants.


## How to Reproduce
Open and run:
`notebooks/analysis_visualization.ipynb`

The notebook loads the integrated dataset, generates the plots, and saves them to the outputs folder.


## Summary of the Interpretation
- Complaint activity is spatially concentrated, implying a small set of neighborhoods accounts for a large share of reports.
- Business density is positively related to complaint frequency, consistent with higher activity and exposure.
- Clustering reveals a few dominant complaint themes alongside several smaller, specialized clusters.
- Complaint patterns differ by nearby business group, suggesting local business context influences the type of issues reported.
