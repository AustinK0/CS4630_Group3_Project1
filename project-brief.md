# Project Brief — Urban Data Cleaning, Integration, and Enrichment with Python

**Course:** CS 4/5630, Python for Computational and Data Sciences  
**Instructor:** Dr. Arijit Khan  
**Project:** Project 1  
**Title:** Urban Data Cleaning, Integration, and Enrichment with Python

## Overview
Build a complete Python pipeline that cleans, enriches, and integrates two heterogeneous urban datasets to enable analysis of service complaints in relation to local business environments. Only classical data science and machine learning methods are allowed (no large language models).

## Data Sources
**NYC 311 Service Requests** (CSV)  
- Link: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
- Content: complaint types, descriptions, timestamps, locations, agency codes

**Yelp Open Dataset** (JSON)  
- Link: https://www.yelp.com/dataset
- Content: business metadata, categories, geolocation, review text

## Pipeline Phases & Requirements
### Phase 1 — Data Acquisition
- Download both datasets.
- Document dataset sizes, formats, and schema differences.
- Store raw vs. processed data separately (e.g., data/raw/ and data/processed/).

### Phase 2 — Data Cleaning & Enrichment
**Required cleaning tasks**
- Standardize column names.
- Normalize complaint types (consistent labels, case-folding, trim whitespace).
- Clean location fields (latitude/longitude, ZIP codes, boroughs).
- Deduplicate records (define and justify rules for identifying the same event/entity).
- Handle missing values with documented strategies.

**Text & category processing tasks**
- Classify complaint descriptions into standardized categories using traditional ML (logistic regression, SVM, random forest).
- Estimate severity or sentiment using lexicon-based methods (VADER/TextBlob) and simple ML classifiers trained on labeled subsets.
- Summarize complaint descriptions via heuristic methods (key phrases, n-grams, informative tokens).
- Normalize Yelp business categories using string matching, grouping rules, or clustering.

### Phase 3 — Data Integration
**Strategy A: Geospatial integration**
- Match 311 complaints to nearby Yelp businesses using distance thresholds or nearest-neighbor search.
- Justify distance metric and radius choice.

**Strategy B: Feature-based integration**
- Engineer numeric/categorical features (one-hot, TF-IDF).
- Use similarity measures (cosine, Jaccard) to relate complaint types to business categories.
- Optionally cluster complaints and map clusters to business types.

**Strategy C: Hybrid integration**
- Combine geospatial proximity with feature-based similarity (e.g., radius filter + category matching).
- Justify design choices and trade-offs.

### Phase 4 — Analysis & Findings
Provide meaningful analyses such as:
- Complaint hotspots by neighborhood.
- Relationship between business density and complaint frequency.
- Clusters of complaint types (classical clustering).
- Differences in complaint patterns near business categories (restaurants vs. retail vs. services).

Visualizations are strongly encouraged (maps, bar charts, time series, cluster plots).

## Deliverables & Deadlines
- **Presentation:** February 24 or 26, 2026 (one slot per group; duration announced later).
- **Report, Source Code, and Cleaned Datasets:** February 26, 2026, 11:59 PM EST.

Late deliverables are not accepted.

## Report Requirements
- Max 10 pages (excluding references and peer assessment).
- Single-column, 11pt Arial font.
- Must emphasize:
  - Key problems studied.
  - Proposed solutions (theory, algorithms, systems).
  - Implementation details (datasets, programming language, tools, code summary/diagram).
  - Experimental results (effectiveness and efficiency).
  - Limitations and future work.
  - Conclusion.
- Append peer assessment at the end; must be signed by all team members.

## Grading Breakdown
- Report: 60% (15 marks)
- Code + Cleaned Output Datasets: 16% (4 marks)
- Presentation + QA: 24% (6 marks)

## Learning Outcomes
- Complete independent analysis of data at significant scale.
- Analyze data of varied volume and variety.
- Execute projects at large scale.
- Deploy environments, libraries, and methods for data science.
- Follow best practices for code development and documentation.

## Peer Assessment (Appendix)
Include a signed peer assessment table with contribution descriptions and percentages totaling 100%.
