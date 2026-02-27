# Urban Data Integration and Enrichment  
## Hybrid Geospatial–Semantic Matching of Philly 311 and Yelp Data

## 1. Introduction

This project integrates 2025 Philly 311 complaint records with Yelp business data (2005–2022) using a hybrid geospatial–semantic matching framework.Due to the temporal gap between datasets, temporal alignment was intentionally excluded. Instead, integration relies on:

- Geographic proximity between complaints and businesses  
- Textual similarity between complaint descriptions and business metadata  

The goal is to link each complaint to nearby and contextually relevant businesses while maintaining computational efficiency at scale.


## 2. Data Sources

- **Philly 311 (2025)**  
  - 245,808 complaint records  
  - Includes complaint category, service name, subject, sentiment score, severity, and coordinates  

- **Yelp Business Dataset (2005–2022)**  
  - 150,243 business records  
  - Includes business name, category, and geographic coordinates  


## 3. Technical Environment

- Python 3.14.2  
- Virtual environment (.venv-1)  
- Libraries:
  - pandas
  - numpy
  - scikit-learn

## 4. Methodology

A two-stage hybrid matching strategy was implemented.

### 4.1 Geospatial Filtering

Candidate businesses were identified within a 500-meter radius of each complaint using the Haversine distance formula.

#### Haversine Distance Formula

The Haversine distance is defined as:

$$d = 2R \cdot \arctan2(\sqrt{a}, \sqrt{1-a})$$

where:

$$a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)$$

**Variables:**

- $d$ = distance in meters  
- $R = 6{,}371{,}000$ m (Earth's mean radius)  
- $\phi_1, \phi_2$ = latitudes in radians  
- $\lambda_1, \lambda_2$ = longitudes in radians  
- $\Delta\phi = \phi_2 - \phi_1$, $\Delta\lambda = \lambda_2 - \lambda_1$

**Note:** Using $\arctan2$ instead of $\arcsin$ for numerical stability at small and antipodal distances.

Only businesses with:

$$0 \leq d \leq 500 \text{ meters}$$

were considered candidates.

### 4.2 Spatial Indexing for Efficiency

To avoid brute force comparison between all complaints and businesses (O($n^2$)), a spatial grid index was implemented.

#### Grid Cell Dimensions

Grid cell sizes were defined as:

$$\text{lat\_cell\_size} = \frac{R_{\text{max}}}{111{,}320 \text{ m/deg}}$$

$$\text{lon\_cell\_size} = \frac{R_{\text{max}}}{111{,}320 \cdot \cos(\phi_{\text{mean}})}$$

**Variables:**

- $R_{\text{max}} = 500$ m (search radius)
- $111{,}320$ m/deg (meters per degree latitude using spherical Earth approximation)
- $\phi_{\text{mean}}$ = mean latitude of all businesses (radians)

**Approximation:** Using spherical Earth model mean radius. For 500m search radius, approximation error is negligible.

#### Indexing Strategy

- Creates 22,360 grid cells indexing all 150,243 businesses
- For each complaint, searches only 3×3 neighboring cells 50–200 candidates

### 4.3 Semantic Similarity

Text similarity was computed using **Jaccard similarity**, which measures overlap between token sets:

$$J(A,B) = \frac{|A \cap B|}{|A \cup B|}$$

Where:

- $A, B \subseteq V$ (where $V$ is the vocabulary space of all unique tokens)
- $A$ = tokens from complaint (service category + service name)  
- $B$ = tokens from business (category + name)  

#### Tokenization

Preprocessing steps:

- Lowercasing all text  
- Removal of non alphanumeric characters  
- Tokenization by whitespace  

Jaccard similarity ranges from 0 to 1:
- $J = 0$: no token overlap
- $J = 1$: identical token sets
- $0 < J < 1$: partial overlap

### 4.4 Geospatial Score

Distance is converted to a proximity score:

$$\text{geo\_score} = 1 - \frac{d}{R_{\text{max}}}$$

**Domain:** Defined only for $0 \leq d \leq R_{\text{max}}$ candidates beyond 500m are filtered prior to scoring.

**Score interpretation:**
- $d = 0$ m (co-located) → geo_score = 1.0 (perfect)
- $d = 250$ m (halfway) → geo_score = 0.5
- $d = 500$ m (boundary) → geo_score = 0.0 (minimum)


### 4.5 Hybrid Score

Geographic proximity and semantic similarity were combined into a single score

$$\text{score} = w_{\text{geo}} \cdot \text{geo\_score} + w_{\text{sim}} \cdot J(A,B)$$

Where

- $w_{\text{geo}}, w_{\text{sim}} \in [0, 1]$ with $w_{\text{geo}} + w_{\text{sim}} = 1.0$ (normalized convex combination)
- $w_{\text{geo}} = 0.6$ (60% weight on geospatial proximity)  
- $w_{\text{sim}} = 0.4$ (40% weight on semantic similarity)

**Rationale:** Geospatial proximity is more reliable than semantic matching due to
- Temporal gap (Yelp 2005–2022 vs Complaints 2025)
- Vocabulary differences (business categories ≠ complaint descriptions)
- K-means normalized categories don't perfectly align with complaint categories

#### Top-K Selection

Each complaint retained its **top 3 highest-scoring business matches** based on the hybrid score.

## 5. Output

- **Output file:** `data/processed/final_integrated_dataset.csv`
- **Total matched records:** 707,348
- **Complaints matched:** 242,190 / 245,808
- **Unique businesses matched:** 12,527
- **Average matches per complaint:** 2.92

### Output Columns

- complaint_id, complaint_category, complaint_service, complaint_subject
- complaint_sentiment (VADER score, range −1 to +1)
- complaint_severity (Low/Medium/High)
- complaint_lat, complaint_lon
- business_id, business_name, business_category
- business_lat, business_lon
- distance_m, similarity, score


## 6. Results

### 6.1 Coverage

- **98.53% of complaints successfully matched** (242,190 / 245,808)
- **3,618 complaints unmatched** (1.47%)
  - Primary reasons: missing coordinates or geographically isolated locations


### 6.2 Distance Statistics

| Metric | Value |
|--------|--------|
| Mean Distance | 177.43 m |
| Median Distance | 153.02 m |
| 90th Percentile | 363.13 m |
| Maximum | 500.0 m |
| Std Dev | 122.99 m |

**Interpretation:** Most complaints have nearby businesses. The distribution is left-skewed, indicating clustering in dense urban areas.

### 6.3 Jaccard Similarity

| Metric | Value |
|--------|--------|
| Mean | 0.0006 |
| Median | 0.0000 |
| Maximum | 0.2000 |
| Non-zero Records | 3,947 (0.56%) |
| Non-zero Percentage | 0.56% |

**Interpretation:** Minimal lexical overlap between complaint descriptions and business metadata is expected due to vocabulary differences and temporal gaps. Only 0.56% of pairs share any tokens.


### 6.4 Hybrid Score Distribution

| Metric | Value |
|--------|--------|
| Mean | 0.3873 |
| Median | 0.4166 |
| Maximum | 0.6535 |
| Minimum | 0.0000 |
| Std Dev | 0.1477 |

**Interpretation:** Given the sparse semantic similarity (median = 0), the hybrid score distribution closely reflects normalized inverse distance. The mean of 0.387 corresponds to an average distance of ~206m (since $0.387 \approx 0.6 \times (1 - 206/500)$).


A scalable hybrid matching system was implemented to integrate urban complaint data with business metadata. The approach achieved high coverage (98.53%) while maintaining computational efficiency through spatial indexing.Results indicate that **geographic proximity is the dominant signal** for matching in this cross-temporal dataset, accounting for the majority of score variance. Semantic similarity provides minor refinement in rare cases of vocabulary overlap.

### Future Improvements

Potential enhancements to strengthen semantic alignment:
- Advanced NLP techniques (TF-IDF, word embeddings, BERT)
- Category hierarchies and business type ontologies
- Historical business data alignment
- Machine learning ranking models trained on labeled complaint business pairs

