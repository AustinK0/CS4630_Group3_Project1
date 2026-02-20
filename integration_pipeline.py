"""
Hybrid Integration Pipeline

# Purpose: To link Philly 311 complaints (2025) with Yelp business data (2005-2022)
# It Focuses on geospatial proximity and category similarity ignoring temporal differences

# Steps taken in the pipeline
# 1) Geospatial Filter: select Yelp businesses near each complaint
# 2) Semantic Matching: measure similarity between complaint text and business categories
# 3) Hybrid Score: combine location 60% and category similarity 40%
# 4) Output: return top-k matching businesses per complaint with scores
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd
import numpy as np


@dataclass
class IntegrationConfig:
    # Paths Philly 311 + Yelp clustered categories
    complaint_path: str = "data/processed/philly_311_cleaned.csv"
    business_path: str = "data/processed/yelp_business_cleaned.json"
    output_path: str = "data/processed/final_integrated_dataset.csv"

    # Complaint columns (Philly 311)
    complaint_id_col: str = "service_request_id"
    complaint_lat_col: str = "lat"
    complaint_lon_col: str = "lon"
    complaint_category_col: str = "service_category"
    complaint_text_col: str = "service_name"

    # Business columns (Yelp)
    business_id_col: str = "business_id"
    business_lat_col: str = "latitude"
    business_lon_col: str = "longitude"
    business_category_col: str = "normal_category"  # K-means normalized
    business_name_col: str = "name"

    # Integration parameters
    radius_m: float = 500.0  # Match businesses within 500m
    top_k: int = 3  # Keep top 3 matches per complaint

    # Hybrid scoring weights must sum to 1.0
    weight_geo: float = 0.6
    weight_text: float = 0.4


# Utility Functions

def load_dataset(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if path.endswith('.json'):
        return pd.read_json(path, lines=True)
    else:
        return pd.read_csv(path)


def validate_columns(df: pd.DataFrame, required: Iterable[str], df_name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{df_name} missing required columns: {missing}")


def validate_config(cfg: IntegrationConfig) -> None:
    # Validate parameters (temporal data intentionally ignored per project spec)
    if cfg.radius_m <= 0:
        raise ValueError("radius_m must be > 0")
    if cfg.top_k <= 0:
        raise ValueError("top_k must be > 0")
    if cfg.weight_geo <= 0 or cfg.weight_text <= 0:
        raise ValueError("Hybrid approach requires both weight_geo and weight_text > 0")
    weight_sum = cfg.weight_geo + cfg.weight_text
    if not math.isclose(weight_sum, 1.0, rel_tol=1e-6):
        raise ValueError(f"weight_geo + weight_text must equal 1.0 (got {weight_sum})")


def normalize_text(text: Optional[str]) -> List[str]:
    if text is None or (isinstance(text, float) and math.isnan(text)):
        return []
    cleaned = []
    for ch in str(text).lower():
        cleaned.append(ch if ch.isalnum() else " ")
    return [t for t in "".join(cleaned).split() if t]


def token_set(*parts: Optional[str]) -> set:
    tokens: List[str] = []
    for part in parts:
        tokens.extend(normalize_text(part))
    return set(tokens)


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


# Spatial Grid Indexing for Efficient Geospatial Filtering

def build_grid_index(
    lat_values: np.ndarray,
    lon_values: np.ndarray,
    radius_m: float,
) -> Tuple[Dict[Tuple[int, int], List[int]], float, float]:
    lat_deg = radius_m / 111_320
    mean_lat = np.nanmean(lat_values)
    lon_deg = radius_m / (111_320 * math.cos(math.radians(mean_lat)))

    grid: Dict[Tuple[int, int], List[int]] = {}
    for idx in range(len(lat_values)):
        lat = lat_values[idx]
        lon = lon_values[idx]
        if pd.isna(lat) or pd.isna(lon):
            continue
        key = (int(lat / lat_deg), int(lon / lon_deg))
        grid.setdefault(key, []).append(idx)

    return grid, lat_deg, lon_deg


def get_neighbor_cells(cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    (cx, cy) = cell
    return [(cx + dx, cy + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]


# Integration Pipeline

def integrate_datasets(cfg: IntegrationConfig) -> pd.DataFrame:
    validate_config(cfg)
    
    # Stage 1: Load datasets
    print("\nStage 1: Load datasets")
    print(f"Complaints: {cfg.complaint_path}")
    complaints = load_dataset(cfg.complaint_path)
    print(f"Loaded complaints: {len(complaints):,}")
    
    print(f"Businesses: {cfg.business_path}")
    businesses = load_dataset(cfg.business_path)
    print(f"Loaded businesses: {len(businesses):,}")

    # Validate columns
    validate_columns(
        complaints,
        [
            cfg.complaint_id_col,
            cfg.complaint_lat_col,
            cfg.complaint_lon_col,
            cfg.complaint_category_col,
        ],
        "Complaint",
    )
    validate_columns(
        businesses,
        [
            cfg.business_id_col,
            cfg.business_lat_col,
            cfg.business_lon_col,
            cfg.business_category_col,
        ],
        "Business",
    )

    # Stage 2: Build spatial index
    print("\nStage 2: Build spatial index")
    print(f"Radius: {cfg.radius_m}m")
    
    business_lats = businesses[cfg.business_lat_col].values
    business_lons = businesses[cfg.business_lon_col].values
    
    grid, lat_deg, lon_deg = build_grid_index(business_lats, business_lons, cfg.radius_m)
    print(f"Grid cells: {len(grid):,}")

    # Stage 3: Tokenize
    print("\nStage 3: Tokenize")
    print(f"Complaints: {len(complaints):,}")
    complaint_tokens = {}
    for idx, row in complaints.iterrows():
        complaint_tokens[idx] = token_set(
            row.get(cfg.complaint_category_col), 
            row.get(cfg.complaint_text_col)
        )
    print("Complaint tokens: done")
    
    print(f"Businesses: {len(businesses):,}")
    business_tokens = {}
    for idx in range(len(businesses)):
        business_tokens[idx] = token_set(
            businesses.iloc[idx].get(cfg.business_category_col), 
            businesses.iloc[idx].get(cfg.business_name_col)
        )
    print("Business tokens: done")

    # Stage 4: Match
    print("\nStage 4: Match")
    print(f"Complaints to process: {len(complaints):,}")
    rows = []
    matched_complaints = 0
    
    # Cache business data for faster access
    business_ids = businesses[cfg.business_id_col].values
    business_names = businesses[cfg.business_name_col].values
    business_cats = businesses[cfg.business_category_col].values
    
    for c_idx, c_row in complaints.iterrows():
        if (c_idx + 1) % 50000 == 0:
            print(f"Progress: {c_idx + 1:,} / {len(complaints):,}")
        
        c_lat = c_row[cfg.complaint_lat_col]
        c_lon = c_row[cfg.complaint_lon_col]
        if pd.isna(c_lat) or pd.isna(c_lon):
            continue

        # Find neighboring grid cells for the geospatial filter
        c_cell = (int(c_lat / lat_deg), int(c_lon / lon_deg))
        candidate_indices: List[int] = []
        for cell in get_neighbor_cells(c_cell):
            candidate_indices.extend(grid.get(cell, []))

        # Score candidates hybridly geospatial and semantic
        scored: List[Tuple[int, float, float, float]] = []
        for b_idx in candidate_indices:
            b_lat = business_lats[b_idx]
            b_lon = business_lons[b_idx]
            if pd.isna(b_lat) or pd.isna(b_lon):
                continue

            # Geospatial component
            dist = haversine_m(c_lat, c_lon, b_lat, b_lon)
            if dist > cfg.radius_m:
                continue

            # Semantic component
            sim = jaccard_similarity(complaint_tokens[c_idx], business_tokens[b_idx])
            
            # Hybrid score combine both components
            geo_score = 1.0 - (dist / cfg.radius_m)
            score = (cfg.weight_geo * geo_score) + (cfg.weight_text * sim)
            scored.append((b_idx, score, dist, sim))

        # Keep top k matches per complaint
        if scored:
            matched_complaints += 1
            scored.sort(key=lambda x: x[1], reverse=True)
            for b_idx, score, dist, sim in scored[: cfg.top_k]:
                rows.append(
                    {
                        "complaint_id": c_row[cfg.complaint_id_col],
                        "complaint_category": c_row.get(cfg.complaint_category_col),
                        "complaint_service": c_row.get(cfg.complaint_text_col),
                        "complaint_lat": c_lat,
                        "complaint_lon": c_lon,
                        "business_id": business_ids[b_idx],
                        "business_name": business_names[b_idx],
                        "business_category": business_cats[b_idx],
                        "business_lat": business_lats[b_idx],
                        "business_lon": business_lons[b_idx],
                        "distance_m": round(dist, 2),
                        "similarity": round(sim, 4),
                        "score": round(score, 4),
                    }
                )

    print(f"Matched complaints: {matched_complaints:,}")
    integrated = pd.DataFrame(rows)
    print(f"Match records: {len(integrated):,}")
    return integrated


def summarize_matches(integrated: pd.DataFrame) -> None:
    if integrated.empty:
        print("No matches to summarize.")
        return

    print("\nMatch summary")
    print(f"Total matches: {len(integrated):,}")

    if "distance_m" in integrated.columns:
        print("\nDistance (m):")
        print(integrated["distance_m"].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]))

    if "similarity" in integrated.columns:
        print("\nSimilarity:")
        print(integrated["similarity"].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]))

    if "score" in integrated.columns:
        print("\nScore:")
        print(integrated["score"].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]))

    if "complaint_id" in integrated.columns:
        unique_complaints = integrated["complaint_id"].nunique()
        print(f"\nUnique complaints: {unique_complaints:,}")
        print(f"Avg matches/complaint: {len(integrated) / max(1, unique_complaints):.2f}")


def main() -> None:
    cfg = IntegrationConfig()
    print("\nHybrid integration")
    print(f"Complaint file: {cfg.complaint_path}")
    print(f"Business file: {cfg.business_path}")
    print(f"Output file: {cfg.output_path}")
    print(f"Radius: {cfg.radius_m}m | Top-k: {cfg.top_k}")
    print(f"Weights: geo={cfg.weight_geo}, text={cfg.weight_text}")

    integrated = integrate_datasets(cfg)

    if integrated.empty:
        print("\n✗ No matches found. Check radius, coordinate ranges, and input columns.")
        return

    print("\nStage 5: Save output")
    os.makedirs(os.path.dirname(cfg.output_path), exist_ok=True)
    integrated.to_csv(cfg.output_path, index=False)
    print(f"Saved: {cfg.output_path}")

    print("\nDone")
    summarize_matches(integrated)


if __name__ == "__main__":
    main()
