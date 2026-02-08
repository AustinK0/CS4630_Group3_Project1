## NYC 311 Dataset

|Column | Description | Type | Notes |
|------|------------|----|-----|
| Unique Key | Unique identifier for each complaint | object | Primary key |
| Created Date | Date and time when the complaint was created | object | Format: YYYY-MM-DD HH:MM:SS |
| Closed Date | Date and time when the complaint was closed | object | May be empty if not resolved |
| Agency | Abbreviated name of the city agency handling the complaint | object | e.g., NYPD, DOT |
| Agency Name | Full name of the city agency | object | - |
| Problem (formerly Complaint Type) | General type of complaint | object | e.g., Noise, Water Leak |
| Problem Detail (formerly Descriptor) | Detailed description of the complaint | object | Free text |
| Additional Details | Any extra information provided | object | Optional field |
| Location Type | Type of location where incident occurred | object | e.g., Street/Sidewalk, Building |
| Incident Zip | Zip code of the incident location | object | 5-digit code |
| Incident Address | Address of the incident | object | - |
| Street Name | Name of the street where the incident occurred | object | - |
| Cross Street 1 | First intersecting street | object | Optional |
| Cross Street 2 | Second intersecting street | object | Optional |
| Intersection Street 1 | First street at intersection (alternate field) | object | Optional |
| Intersection Street 2 | Second street at intersection (alternate field) | object | Optional |
| Address Type | Type of address provided | object | e.g., Standard, Intersection |
| City | City name | string | Typically "NEW YORK" |
| Landmark | Nearby landmark if applicable | object | Optional |
| Facility Type | Type of facility involved | object | e.g., Park, School |
| Status | Current status of complaint | object | e.g., Open, Closed, Pending |
| Due Date | Date when the complaint is due to be resolved | object | May be empty |
| Resolution Description | Explanation of how the complaint was resolved | object | Free text |
| Resolution Action Updated Date | Date when resolution action was last updated | object | - |
| Community Board | NYC community board number | object | 1–59 |
| Council District | NYC council district number | object | 1–51 |
| Police Precinct | Police precinct number | object | - |
| BBL | Borough, Block, Lot identifier for property | object | Unique property ID |
| Borough | NYC borough | object | One of: Bronx, Brooklyn, Manhattan, Queens, Staten Island |
| X Coordinate (State Plane) | X coordinate in State Plane system | object | - |
| Y Coordinate (State Plane) | Y coordinate in State Plane system | object | - |
| Open Data Channel Type | Source channel for the complaint | object | e.g., 311 Call Center, Mobile App |
| Park Facility Name | Name of the park involved, if applicable | object | Optional |
| Park Borough | Borough of park facility | object | Optional |
| Vehicle Type | Type of vehicle involved | object | Optional |
| Taxi Company Borough | Borough of taxi company involved | object | Optional |
| Taxi Pick Up Location | Taxi pick-up location | object | Optional |
| Bridge Highway Name | Name of bridge or highway involved | object | Optional |
| Bridge Highway Direction | Direction of travel | object | Optional |
| Road Ramp | Ramp identifier | object | Optional |
| Bridge Highway Segment | Highway segment | object | Optional |
| Latitude | Latitude of incident | float64 | Decimal degrees |
| Longitude | Longitude of incident | float64 | Decimal degrees |
| Location | Combined location string | object | Usually "latitude, longitude" |

---

## Yelp Business Dataset
| Column | Description | Type | Notes |
|--------|------------|------|------|
| business_id | Unique Yelp business identifier | object | Primary key |
| name | Business name | object | - |
| address | Street address | object | - |
| city | City where the business is located | object | - |
| state | State code (abbreviation) | object | e.g., NY, CA |
| postal_code | Postal/zip code | object | 5-digit code |
| latitude | Latitude of business | float64 | Decimal degrees |
| longitude | Longitude of business | float64 | Decimal degrees |
| stars | Average rating of business | float64 | 1.0–5.0 |
| review_count | Number of reviews | int64 | - |
| is_open | Whether business is open (1) or closed (0) | int64 | Binary |
| attributes | Additional business attributes | object | JSON/dictionary format |
| categories | Business categories | object | Comma-separated list |
| hours | Business hours | object | JSON/dictionary format |
