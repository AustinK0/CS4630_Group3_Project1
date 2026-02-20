**Integration:** Urban Data Cleaning, Integration, and Enrichment with Python

## Integration Summary
This phase integrates Philly 311 complaints 2025 with Yelp business data 2005–2022 using a hybrid match. Per the last project brief, temporal alignment is intentionally ignored. The integration relies only on geospatial proximity and feature similarity.

## Data Sources
- Philly 311 (2025): 245,808 complaint records
- Yelp businesses (2005–2022): 150,243 business records

## Environment & Technologies used
- Virtual environment: .venv-1
- Python 3.14.2
- Libraries: pandas, numpy, scikit-learn

## Method
We applied a two-part matching strategy:
1. **Geospatial proximity:** Businesses within a 500m radius of each complaint were treated as candidates (Haversine distance).
2. **Semantic similarity:** Complaint category + service name were compared to business category + name using Jaccard similarity on token sets.

The final score is:
$$\text{score} = 0.6 \times \text{geo\_score} + 0.4 \times \text{similarity}$$

Each complaint retains the top 3 highest scoring matches.

## Process Steps
1. Load the cleaned Philly 311 CSV and Yelp JSONL files.
2. Validate required columns.
3. Build a grid index to speed up proximity search.
4. Tokenize complaint and business text fields.
5. For each complaint:
	- find nearby business candidates via the grid
	- compute Haversine distance
	- compute Jaccard similarity
	- calculate hybrid score
	- keep the top 3 matches
6. Save all matches to a single CSV output.

## Output
- File: data/processed/final_integrated_dataset.csv
- Records: 707,348
- Coverage: 242,190 / 245,808 complaints matched (98.5%)
- Avg matches per complaint: 2.92

## Output Columns
- complaint_id, complaint_category, complaint_service, complaint_lat, complaint_lon
- business_id, business_name, business_category, business_lat, business_lon
- distance_m, similarity, score

## Results - Key Statistics
- distance_m: mean 177m, median 153m, max 500m
- similarity: mostly 0, max 0.20
- score: mean 0.387, median 0.417

## Notes and Limits
- Category overlap is often low which was expected.
- Dense areas yield more matches.
