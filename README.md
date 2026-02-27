# Project 1

## Overview
In this project, we want to integrate messy structured public service data with large-scale unstructured business data to uncover meaningful urban patterns. The goal is to build a pipeline that transforms raw data into a clean and integrated dataset for urban complaint analysis.

### Datasets
- Philly 311 Service Requests (CSV)
- Yelp Open Dataset (JSON)
- Here's the link to the datasets - (https://falconbgsu-my.sharepoint.com/my?id=%2Fpersonal%2Flmoraa%5Fbgsu%5Fedu%2FDocuments%2Fraw&ga=1)
- Here's the link to the datasets - (https://falconbgsu-my.sharepoint.com/my?id=%2Fpersonal%2Flmoraa%5Fbgsu%5Fedu%2FDocuments%2Fraw&ga=1)

### Folder Structure
- `data/raw/`: Original datasets, filenames **must** be `philly_311_raw.csv` and `yelp_academic_dataset_business.json`
- `data/processed/`: Cleaned datasets
- Hidden through `.gitignore` because the datasets are too large for GitHub
- notebooks: contains ipnyb notebooks for data exploration, loading, cleaning and analysis.
- notebooks: contains ipnyb notebooks for data exploration, loading, cleaning and analysis.

### How to Run
1. Install needed packages (pandas, numpy, json, os, matplotlib, sklearn, vaderSentiment, textBlob)
2. Run notebooks in order:
     1. data_loading.ipynb
     3. data_cleaning.ipynb
     4. data_cleaning_text_category_processing.ipynb
     5. yelp_data_cleaning.ipynb
     6. yelp_category_normalization.ipynb
     7. integration_pipeline.ipynb
     8. analysis_visualization.ipynb 

### How to Comprehend Results
The integrated analysis revealed several key findings. A small set of neighborhoods accounts for a large share of all reports, and business density is positively related to complaint frequency. Clustering identified dominant complaint themes, specifically environmental and public safety issues, alongside smaller specialized groups. Complaint patterns vary by nearby business type, suggesting that local commercial content might influence reported issues. The sentiment analysis provided further insight, showing that environmental and public safety complaints seem to have more negative language. Severity comparisons across business groups highlight where serious complaints are concentrated. 
